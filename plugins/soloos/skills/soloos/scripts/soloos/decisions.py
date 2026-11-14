"""Bounded marketing scenario arithmetic plus explicit management perspectives."""

import re
from datetime import date, timedelta
from decimal import Decimal, ROUND_CEILING

from .data import trusted
from .finance import calculate, money
from .permissions import execution_policy
from .records import record


def marketing_budget(data, start, end, increase, contribution_margin=None, recorded_at=None):
    kpis = calculate(data, start, end)
    minor = data["company"]["minor_units"]
    if not isinstance(increase, str) or not re.fullmatch(r"(0|[1-9][0-9]{0,14})(\.[0-9]{1,4})?", increase):
        raise ValueError("Budget increase must be a finite positive decimal money string")
    extra = Decimal(increase)
    if extra <= 0 or -extra.as_tuple().exponent > minor:
        raise ValueError("Budget increase must be positive and match currency precision")
    margin = None
    if contribution_margin is not None:
        try:
            margin = Decimal(str(contribution_margin))
        except Exception as exc:
            raise ValueError("Contribution margin must be a decimal between 0 and 1") from exc
        if not margin.is_finite() or not 0 < margin <= 1:
            raise ValueError("Contribution margin must be greater than 0 and at most 1")
    snapshot = data.get("cash_snapshot")
    cash_known = bool(snapshot and trusted(snapshot) and snapshot["as_of"] == end)
    cash = Decimal(snapshot["available_cash"]) if cash_known else None
    baseline_burn = None
    if kpis["complete"]:
        # Preserve profitable baseline cash generation, rather than clamping before adding spend.
        baseline_burn = -Decimal(kpis["profit"]) * Decimal(30) / Decimal(kpis["days"])
    stressed_burn = max(baseline_burn + extra, Decimal(0)) if baseline_burn is not None else None
    stressed_runway = None
    if cash is not None and stressed_burn is not None:
        if cash == 0:
            stressed_runway = "0.00"
        elif stressed_burn > 0:
            stressed_runway = money(cash / stressed_burn, 2)
    breakeven = None
    if margin is not None:
        # Round up: the target must cover the entire incremental spend.
        breakeven = format((extra / margin).quantize(Decimal(1).scaleb(-minor), rounding=ROUND_CEILING), "f")
    if not kpis["complete"] or cash is None or margin is None:
        recommendation = "Defer commitment; resolve missing actuals, current cash or contribution-margin evidence."
    elif extra > cash:
        recommendation = "Do not commit this increase: one month of incremental spend exceeds available cash."
    else:
        recommendation = "Consider only a capped experiment after validating acquisition economics, cash obligations and founder capacity."
    payload = {
        "status": "proposed", "intent": "marketing-budget", "period": {"start": start, "end": end},
        "scenario": {
            "monthly_increment": money(extra, minor), "currency": kpis["currency"],
            "contribution_margin_assumption": str(margin) if margin is not None else None,
            "required_incremental_monthly_revenue": breakeven,
            "baseline_runway_months": kpis["runway_months"],
            "stressed_runway_months": stressed_runway,
            "stressed_monthly_operating_burn": money(stressed_burn, minor) if stressed_burn is not None else None,
            "assumptions": ["Increase is recurring monthly spend, not a one-time payment.",
                            "Downside scenario assumes no incremental revenue and unchanged baseline operations.",
                            "Contribution margin, when supplied, is an unverified assumption, not measured campaign ROI."],
        },
        "perspectives": {
            "CEO": "Check strategic fit, founder delivery capacity and opportunity cost; preserve an explicit cash reserve.",
            "CFO": "Compare downside cash burn and break-even revenue; account for upcoming obligations before approval.",
            "CMO": "Require channel-level acquisition cost, conversion, attribution and payback evidence; test before scaling.",
        },
        "recommendation": recommendation,
        "next_action": {"owner": "founder", "action": "Collect channel economics and set an affordable experiment cap before seeking approval.",
                        "review_date": (date.fromisoformat(end) + timedelta(days=7)).isoformat(),
                        "success_criterion": "Observed incremental contribution covers incremental spend within the founder-approved payback window."},
        "missing_evidence": ["Channel-level conversion and acquisition costs", "Payback window and upcoming cash obligations", "Founder capacity"],
        "warnings": kpis["warnings"], "policy": execution_policy("marketing_budget_write"),
    }
    return record("Decision", data, payload, "forecast", recorded_at)
