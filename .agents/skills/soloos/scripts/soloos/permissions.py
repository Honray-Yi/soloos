"""Fail-closed boundary. Phase 1 has no external execution implementation."""


def execution_policy(action, approval=None):
    """Approval data is not verified in Phase 1 and can never enable execution."""
    high_risk = action in {"payment", "contract", "delete", "public_post", "binding_communication"}
    return {
        "allowed": False,
        "status": "proposal_only",
        "reason": "External execution is unavailable in Phase 1; approval cannot enable an absent connector.",
        "required_approval": "separate_explicit" if high_risk else "explicit_external_write",
        "approval_verified": False,
    }


def execute(action, approval=None):
    raise PermissionError(execution_policy(action, approval)["reason"])
