# project/src/reviewer_agent.py
# Simple, predictable reviewer with the exact API the dispatcher expects.
# - Signature: review(task: dict, result_text: str) -> dict
# - Return shape: {"decision": "APPROVE" | "REJECT", "notes": str}

from typing import Dict
import re

APPROVE = "APPROVE"
REJECT = "REJECT"

# Extend as needed; these are intentionally conservative.
_DANGEROUS = [
    r"rm\s+-rf\s+/?",                    # destructive shell
    r"\bDROP\s+TABLE\b",                 # destructive SQL
    r"\bTRUNCATE\s+TABLE\b",
    r"\bALTER\s+TABLE\b.*\bDROP\b",
    r"chmod\s+777\b",                    # overly permissive perms
    r"/etc/passwd",                      # sensitive file path
]

def review(task: dict, result_text: str) -> Dict[str, str]:
    text = (result_text or "").strip()

    for pat in _DANGEROUS:
        if re.search(pat, text, flags=re.IGNORECASE):
            return {
                "decision": REJECT,
                "notes": f"Rejected: matched dangerous pattern: {pat}",
            }

    return {
        "decision": APPROVE,
        "notes": "approve: no dangerous patterns detected",
    }