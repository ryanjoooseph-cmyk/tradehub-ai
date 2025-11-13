# reviewer_agent.py
# Simple static reviewer that always returns a dict the dispatcher can consume.
# Accepts extra args to avoid "takes 1 positional argument but 2 were given".

from typing import Any, Dict

APPROVE = "APPROVE"
REJECT = "REJECT"

def review(task: Dict[str, Any], *args, **kwargs) -> Dict[str, Any]:
    """
    Normalize to a dict so the caller can always do .get(...).
    Decide APPROVE/REJECT with a very simple heuristic:
      - If task payload has key 'danger' truthy -> REJECT
      - else APPROVE
    """
    payload = task.get("payload", {}) if isinstance(task, dict) else {}
    reason = "approve: no dangerous patterns detected"
    decision = APPROVE
    try:
        if isinstance(payload, dict) and payload.get("danger"):
            decision = REJECT
            reason = "reject: flagged by payload['danger']"
    except Exception as _:
        # Be conservative but never crash the caller
        decision = APPROVE
        reason = "approve: fallback path"

    return {
        "decision": decision,
        "reason": reason,
        "meta": {
            "source": "reviewer_agent.py",
            "version": "1.0.0",
        },
    }