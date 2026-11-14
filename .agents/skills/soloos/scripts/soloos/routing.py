"""Exact intent routing, separate from host-model natural language reasoning."""

ROUTES = {
    "onboard": ["CEO"], "validate": ["BI"], "kpis": ["CFO"],
    "weekly-report": ["CEO", "CFO"], "marketing-budget": ["CEO", "CFO", "CMO"],
}


def route(intent):
    if intent not in ROUTES:
        return {"supported": False, "departments": [], "next_step": "Clarify intent or explain Phase 1 scope"}
    return {"supported": True, "departments": ROUTES[intent], "next_step": intent}
