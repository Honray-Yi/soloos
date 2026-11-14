import json
import re

from jsonschema import Draft202012Validator
import pytest
import yaml

from soloos.data import ROOT, FORMAT_CHECKER
from soloos.finance import calculate
from soloos.records import validate_record
from soloos.reporting import weekly_report


def test_skill_metadata_and_references():
    content = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    meta = yaml.safe_load(content.split("---", 2)[1])
    assert meta["name"] == ROOT.name == "soloos"
    assert 0 < len(meta["description"]) <= 1024
    for reference in re.findall(r"\]\(([^)]+)\)", content):
        assert (ROOT / reference).is_file()
    ui = yaml.safe_load((ROOT / "agents/openai.yaml").read_text(encoding="utf-8"))
    assert "$soloos" in ui["interface"]["default_prompt"]
    assert 25 <= len(ui["interface"]["short_description"]) <= 64


def test_business_schema_is_valid():
    schema = json.loads((ROOT / "assets/business.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    output = json.loads((ROOT / "assets/output.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(output)
    assert schema["$defs"]["metadata"] == output["$defs"]["metadata"]


@pytest.mark.parametrize("value", ["2026-11-01T10:00:00+00:99", "2026-11-01T10:00:00+24:00", "2026-11-01T10:00:00", "2026-02-30T10:00:00Z"])
def test_timestamp_validation_without_optional_packages(value):
    assert not FORMAT_CHECKER.conforms(value, "date-time")


def test_noncanonical_period_rejected(business):
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        calculate(business, "20261102", "20261108")


def test_output_validation_rejects_missing_payload(business):
    from jsonschema.exceptions import ValidationError
    report = weekly_report(business, "2026-11-02", "2026-11-08")
    del report["payload"]["kpis"]
    with pytest.raises(ValidationError):
        validate_record(report)
