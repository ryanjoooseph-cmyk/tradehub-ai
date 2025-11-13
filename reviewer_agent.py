# reviewer_agent.py
# Drop-in reviewer that matches the dispatcher’s expectations.
# - Signature: review(task, result_text)
# - Return: {"decision": "APPROVE" | "REJECT", "notes": str}

from typing import Dict
import re

APPROVE = "APPROVE"
REJECT = "REJECT"

# Quick safety patterns; extend as needed.
DANGEROUS_PATTERNS = [
    r"rm\s+-rf\s+/?",                   # nuking filesystem
    r"\bDROP\s+TABLE\b",                # destructive SQL
    r"\bTRUNCATE\s+TABLE\b",
    r"\bALTER\s+TABLE\b.*\bDROP\b",
    r"chmod\s+777\b",                   # overly permissive perms
    r"/etc/passwd",                     # sensitive file access
]

def review(task: dict, result_text: str) -> Dict[str, str]:
    """
    Minimal, predictable reviewer that always returns a dict so the
    dispatcher can do .get('decision') without blowing up.
    """
    text = result_text or ""

    # Block obviously dangerous changes
    for pat in DANGEROUS_PATTERNS:
        if re.search(pat, text, flags=re.IGNORECASE):
            return {
                "decision": REJECT,
                "notes": f"Rejected: matched dangerous pattern: {pat}",
            }

    # Otherwise approve (mirrors what you saw in logs)
    return {
        "decision": APPROVE,
        "notes": "approve: no dangerous patterns detected",
    }