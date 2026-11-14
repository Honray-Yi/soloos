"""Exact intent routing, separate from host-model natural language reasoning."""

ROUTES = {
    "onboard": ["CEO"], "validate": ["BI"], "kpis": ["CFO"],
    "weekly-report": ["CEO", "CFO"], "marketing-budget": ["CEO", "CFO", "CMO"],
    "strategy": ["CEO", "CFO", "COO"], "sales-pipeline": ["Sales", "CMO", "COO"],
    "operations": ["COO", "Sales", "CTO/Product"], "product": ["CTO/Product", "CEO", "COO"],
    "partnership": ["HR/Partnership", "COO", "CFO"], "data-quality": ["BI", "CFO"],
    "report": ["CEO", "CFO", "BI"], "forecast": ["CFO", "CEO"],
    "decision-outcome": ["CEO", "BI"], "action-proposal": ["CEO", "COO"],
}


def route(intent):
    if intent not in ROUTES:
        return {"supported": False, "departments": [], "next_step": "Clarify the requested workflow and available capability"}
    return {"supported": True, "departments": ROUTES[intent], "next_step": intent}
