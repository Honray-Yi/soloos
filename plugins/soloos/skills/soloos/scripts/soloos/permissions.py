"""Legacy unscoped calls always fail closed; use the separate journaled action API."""


def execution_policy(action, approval=None):
    """Unverified inline approval data can never enable execution."""
    high_risk = action in {"payment", "contract", "delete", "public_post", "binding_communication"}
    return {
        "allowed": False,
        "status": "proposal_only",
        "reason": "Unscoped execution is disabled; prepare an action and use a capable connector with journaled scoped approvals.",
        "required_approval": "separate_explicit" if high_risk else "explicit_external_write",
        "approval_verified": False,
    }


def execute(action, approval=None):
    raise PermissionError(execution_policy(action, approval)["reason"])
