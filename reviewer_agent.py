# reviewer_agent.py
# Minimal, deterministic reviewer. Returns a dict with a decision and reason.

from __future__ import annotations
from typing import Dict, Any

APPROVE = "APPROVE"
REJECT  = "REJECT"

def review(task: Dict[str, Any]) -> Dict[str, str]:
    """
    Input: task dict with at least {"feature": "<name>", ...}
    Output: {"decision": "APPROVE"|"REJECT", "reason": "<text>"}
    """
    name = str(task.get("feature", "")).strip()
    if not name:
        return {"decision": REJECT, "reason": "Missing 'feature' field."}

    # Super simple guardrails; extend as needed
    bad = {"drop database", "rm -rf", "exfiltrate", "cryptominer"}
    blob = (name + " " + str(task)).lower()
    if any(b in blob for b in bad):
        return {"decision": REJECT, "reason": "Dangerous pattern detected."}

    return {"decision": APPROVE, "reason": "approve: no dangerous patterns detected"}