import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from soloos.cli import main
from soloos.decisions import marketing_budget
from soloos.permissions import execute, execution_policy
from soloos.records import validate_record
from soloos.reporting import weekly_report, markdown
from soloos.routing import route
from soloos.data import ROOT

START, END = "2026-11-02", "2026-11-08"
NOW = "2026-11-09T00:00:00Z"


def test_report_reproducible_and_traceable(business):
    report = weekly_report(business, START, END, NOW)
    assert report == weekly_report(business, START, END, NOW)
    validate_record(report)
    text = markdown(report)
    assert "2000.00" in text and "2700.00" in text and "-700.00" in text
    assert "Synthetic data: True" in text and "dataset:sha256:" in text
    business["transactions"][0]["amount"] = "2001.00"
    assert weekly_report(business, START, END, NOW)["id"] != report["id"]


def test_partial_report_does_not_present_zero_as_fact(business):
    business["coverage"]["complete"] = False
    report = weekly_report(business, START, END, NOW)
    assert "Unavailable" in markdown(report)
    assert report["payload"]["kpis"]["revenue"] is None


def test_report_requires_week(business):
    with pytest.raises(ValueError, match="seven"):
        weekly_report(business, START, "2026-11-09")


def test_marketing_cross_functional_scenario(business):
    decision = marketing_budget(business, START, END, "600.00", "0.60", NOW)
    validate_record(decision)
    p = decision["payload"]
    assert set(p["perspectives"]) == {"CEO", "CFO", "CMO"}
    assert p["scenario"]["required_incremental_monthly_revenue"] == "1000.00"
    assert p["scenario"]["stressed_runway_months"] == "3.33"
    assert p["status"] == "proposed" and p["policy"]["allowed"] is False
    assert decision["metadata"]["evidence"] == "forecast"


def test_profitable_baseline_absorbs_increase(business):
    business["transactions"][0]["amount"] = "5000.00"
    result = marketing_budget(business, START, END, "600.00", "0.60")["payload"]["scenario"]
    assert result["stressed_monthly_operating_burn"] == "0.00"
    assert result["stressed_runway_months"] is None


def test_missing_inputs_defer_commitment(business):
    del business["cash_snapshot"]
    p = marketing_budget(business, START, END, "600.00")["payload"]
    assert p["recommendation"].startswith("Defer")
    assert p["scenario"]["stressed_runway_months"] is None
    assert p["scenario"]["required_incremental_monthly_revenue"] is None


@pytest.mark.parametrize("increase", ["0", "-1", "NaN", "Infinity", "1e3", "0.001", "abc"])
def test_bad_budget_rejected(business, increase):
    with pytest.raises(ValueError):
        marketing_budget(business, START, END, increase)


@pytest.mark.parametrize("margin", ["0", "-1", "1.01", "NaN", "Infinity", "abc"])
def test_bad_margin_rejected(business, margin):
    with pytest.raises(ValueError):
        marketing_budget(business, START, END, "100", margin)


@pytest.mark.parametrize("action", ["marketing_budget_write", "payment", "contract", "delete", "public_post", "binding_communication", "unknown"])
@pytest.mark.parametrize("approval", [None, True, {"approved": True, "role": "owner"}])
def test_external_execution_denied_even_with_unverifiable_approval(action, approval):
    assert execution_policy(action, approval)["allowed"] is False
    with pytest.raises(PermissionError):
        execute(action, approval)


def test_separate_approval_for_high_risk_actions():
    assert execution_policy("payment")["required_approval"] == "separate_explicit"


@pytest.mark.parametrize("intent,departments", [("onboard", ["CEO"]), ("kpis", ["CFO"]),
    ("weekly-report", ["CEO", "CFO"]), ("marketing-budget", ["CEO", "CFO", "CMO"])])
def test_routes(intent, departments):
    assert route(intent)["departments"] == departments


def test_unknown_route_does_not_guess_execution():
    assert not route("send a payment")["supported"]


def test_cli_roundtrip_and_no_overwrite(tmp_path, capsys):
    data = tmp_path / "company.json"
    report = tmp_path / "weekly.md"
    assert main(["init", "--demo", "--out", str(data)]) == 0
    assert main(["validate", str(data)]) == 0
    assert main(["weekly-report", str(data), "--start", START, "--end", END, "--out", str(report)]) == 0
    original = report.read_bytes()
    assert main(["weekly-report", str(data), "--start", START, "--end", END, "--out", str(report)]) == 2
    assert report.read_bytes() == original
    assert "SoloOS error" in capsys.readouterr().err


def test_copied_skill_runs_without_development_repo(tmp_path):
    copied = tmp_path / "soloos"
    shutil.copytree(ROOT, copied, ignore=shutil.ignore_patterns("__pycache__"))
    result = subprocess.run([sys.executable, str(copied / "scripts/soloos_cli.py"), "kpis",
                             str(copied / "assets/demo-business.json"), "--start", START, "--end", END],
                            cwd=tmp_path, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["profit"] == "-700.00"


def test_capabilities_does_not_claim_host_execution(capsys):
    assert main(["capabilities"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["external_execution"] is False and result["scheduler"] is False
    assert result["host_capabilities"] == "not inspected"
