# project/src/reviewer_agent.py
# Approve-by-default reviewer with simple guardrails.
import os, re, json
from typing import Any, Tuple

STRICT = (os.getenv("REVIEW_STRICT", "report").lower() == "enforce")

# Patterns that are truly risky; expand later as needed.
DANGEROUS = [
    r"\bdrop\s+table\b",
    r"\balter\s+table\b.*\bdrop\s+column\b",
    r"\bdelete\s+from\b(?!.*\bwhere\b)",     # DELETE without WHERE
    r"rm\s+-rf\s+/",
    r"OPENAI_API_KEY\s*=",
    r"sk-[A-Za-z0-9]{10,}",                  # keys in text
]

def _collect_text(args, kwargs) -> str:
    chunks = []
    for a in args:
        if isinstance(a, str):
            chunks.append(a)
        else:
            try:
                chunks.append(json.dumps(a, default=str)[:8000])
            except Exception:
                pass
    if kwargs:
        try:
            chunks.append(json.dumps(kwargs, default=str)[:8000])
        except Exception:
            pass
    return "\n".join(chunks)

def review(*args: Any, **kwargs: Any) -> Tuple[bool, str]:
    """
    Accepts anything (string, dict, etc.) and returns (approved, reason).
    In 'report' mode we approve and log reasons; in 'enforce' we reject on DANGEROUS.
    """
    text = _collect_text(args, kwargs)
    findings = []
    for pat in DANGEROUS:
        if re.search(pat, text, flags=re.IGNORECASE | re.MULTILINE):
            findings.append(pat)

    if findings and STRICT:
        reason = f"reject: matched dangerous patterns: {findings}"
        print(f"REVIEW DECISION: REJECT — {reason}")
        return (False, reason)

    if findings and not STRICT:
        reason = f"approve(report): risky patterns found but STRICT=off: {findings}"
        print(f"REVIEW DECISION: APPROVE (report-only) — {reason}")
        return (True, reason)

    reason = "approve: no dangerous patterns detected"
    print(f"REVIEW DECISION: APPROVE — {reason}")
    return (True, reason)