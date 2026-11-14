from copy import deepcopy
from decimal import Decimal

import pytest

from soloos.finance import calculate

START, END = "2026-11-02", "2026-11-08"


def test_known_cash_basis_totals_and_runway(business):
    k = calculate(business, START, END)
    assert (k["revenue"], k["expenses"], k["profit"]) == ("2000.00", "2700.00", "-700.00")
    assert k["monthly_operating_burn"] == "3000.00"
    assert k["runway_months"] == "4.00"
    assert k["net_financing"] == "500.00"


def test_refunds_and_financing_do_not_inflate_profit(business):
    template = business["transactions"][0]
    for kind, amount in [("revenue_refund", "100.00"), ("expense_refund", "20.00"), ("financing_in", "9000.00")]:
        row = deepcopy(template)
        row.update(id=kind, kind=kind, amount=amount)
        business["transactions"].append(row)
    k = calculate(business, START, END)
    assert k["profit"] == "-780.00"
    assert k["net_financing"] == "9500.00"


def test_decimal_precision(business):
    business["transactions"] = business["transactions"][:2]
    for row, amount in zip(business["transactions"], ["0.10", "0.20"]):
        row.update(kind="revenue", amount=amount)
    assert calculate(business, START, END)["revenue"] == "0.30"


@pytest.mark.parametrize("change", ["incomplete", "forecast", "unverified", "coverage", "company"])
def test_uncertain_evidence_withholds_authoritative_kpis(business, change):
    if change == "incomplete":
        business["coverage"]["complete"] = False
    elif change == "forecast":
        business["transactions"][0]["metadata"]["evidence"] = "forecast"
    elif change == "unverified":
        business["transactions"][0]["metadata"]["validation_status"] = "unverified"
    elif change == "coverage":
        business["coverage"]["start"] = "2026-11-03"
    else:
        business["company"]["metadata"]["evidence"] = "assumption"
    k = calculate(business, START, END)
    assert not k["complete"]
    assert k["revenue"] is None and k["profit"] is None and k["runway_months"] is None


@pytest.mark.parametrize("snapshot", [None, "stale", "future", "estimate"])
def test_cash_snapshot_must_be_current_and_confirmed(business, snapshot):
    if snapshot is None:
        del business["cash_snapshot"]
    elif snapshot == "estimate":
        business["cash_snapshot"]["metadata"]["evidence"] = "estimate"
    else:
        business["cash_snapshot"]["as_of"] = "2026-11-01" if snapshot == "stale" else "2026-11-09"
    k = calculate(business, START, END)
    assert k["revenue"] == "2000.00"
    assert k["runway_months"] is None


def test_zero_cash_and_no_burn(business):
    business["cash_snapshot"]["available_cash"] = "0.00"
    assert calculate(business, START, END)["runway_months"] == "0.00"
    business["cash_snapshot"]["available_cash"] = "100.00"
    business["transactions"] = []
    k = calculate(business, START, END)
    assert k["profit"] == "0.00" and k["runway_months"] is None
    assert k["runway_status"] == "no_positive_operating_burn"


def test_timezone_boundaries_and_excluded_period(business):
    row = business["transactions"][0]
    row["occurred_at"] = "2026-11-08T16:00:00Z"  # Nov 9 in Kuala Lumpur
    assert calculate(business, START, END)["revenue"] == "0.00"
    row["occurred_at"] = "2026-11-01T16:00:00Z"  # Nov 2 locally
    assert calculate(business, START, END)["revenue"] == "2000.00"


def test_invalid_period(business):
    with pytest.raises(ValueError):
        calculate(business, END, START)


def test_sum_invariant_for_many_amounts(business):
    template = business["transactions"][0]
    rows = []
    for n in range(1, 101):
        row = deepcopy(template)
        row.update(id=str(n), amount=f"{n // 100}.{n % 100:02d}")
        rows.append(row)
    business["transactions"] = rows
    assert Decimal(calculate(business, START, END)["revenue"]) == Decimal("50.50")
