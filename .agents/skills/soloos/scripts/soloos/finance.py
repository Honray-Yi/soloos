"""Cash-basis arithmetic. No exchange-rate guesses or model-generated totals."""

from datetime import date
from decimal import Decimal, ROUND_HALF_UP
import re

from .data import local_date, trusted, validate


def money(value, minor_units):
    return format(value.quantize(Decimal(1).scaleb(-minor_units), rounding=ROUND_HALF_UP), "f")


def calculate(data, start, end):
    validate(data)
    if any(not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) for value in (start, end)):
        raise ValueError("Period dates must use YYYY-MM-DD")
    first, last = date.fromisoformat(start), date.fromisoformat(end)
    if first > last:
        raise ValueError("Period start must not exceed end")
    company, coverage = data["company"], data["coverage"]
    timezone = company["metadata"]["timezone"]
    minor = company["minor_units"]
    warnings, excluded, included = [], [], []
    totals = {kind: Decimal(0) for kind in (
        "revenue", "expense", "revenue_refund", "expense_refund", "financing_in", "financing_out"
    )}
    for transaction in data["transactions"]:
        if first <= local_date(transaction["occurred_at"], timezone) <= last:
            if not trusted(transaction):
                excluded.append(transaction["id"])
                continue
            included.append(transaction["id"])
            totals[transaction["kind"]] += Decimal(transaction["amount"])
    complete = (coverage["complete"] and trusted(coverage) and trusted(company)
                and coverage["start"] <= start <= end <= coverage["end"] and not excluded)
    revenue = totals["revenue"] - totals["revenue_refund"]
    expenses = totals["expense"] - totals["expense_refund"]
    profit = revenue - expenses
    if not complete:
        warnings.append("Incomplete or unconfirmed evidence: observed totals are partial; authoritative KPIs and runway withheld.")
    if excluded:
        warnings.append("Excluded unconfirmed/unvalidated transactions: " + ", ".join(excluded))
    days = (last - first).days + 1
    burn = max(-profit, Decimal(0)) * Decimal(30) / Decimal(days)
    snapshot = data.get("cash_snapshot")
    runway, runway_status = None, "insufficient_data"
    if complete and snapshot and trusted(snapshot) and snapshot["as_of"] == end:
        cash = Decimal(snapshot["available_cash"])
        if cash == 0:
            runway, runway_status = "0.00", "no_cash_reserve"
        elif burn > 0:
            runway = money(cash / burn, 2)
            runway_status = "estimated_from_period"
        else:
            runway_status = "no_positive_operating_burn"
    else:
        warnings.append("Runway needs complete actuals and a confirmed cash snapshot dated at period end.")
    warnings.append("Runway extrapolates this period to a 30-day month; financing, future obligations and seasonality are not projected.")
    observed = {"revenue": money(revenue, minor), "expenses": money(expenses, minor), "profit": money(profit, minor)}
    return {
        "start": start, "end": end, "days": days, "currency": company["metadata"]["currency"],
        "timezone": timezone, "basis": "cash", "complete": complete,
        "observed": observed, **{key: value if complete else None for key, value in observed.items()},
        "net_financing": money(totals["financing_in"] - totals["financing_out"], minor),
        "monthly_operating_burn": money(burn, minor) if complete else None,
        "runway_months": runway, "runway_status": runway_status,
        "included_transaction_ids": included, "excluded_transaction_ids": excluded, "warnings": warnings,
    }
