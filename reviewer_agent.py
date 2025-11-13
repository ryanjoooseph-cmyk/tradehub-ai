# project/src/reviewer_agent.py
# Approve-by-default reviewer that returns a DICT (dispatcher expects .get()).

import os, re, json
from typing import Any, Dict, List

STRICT = (os.getenv("REVIEW_STRICT", "report").lower() == "enforce")

# Very basic risk patterns; expand later.
DANGEROUS: List[str] = [
    r"\bdrop\s+table\b",
    r"\balter\s+table\b.*\bdrop\s+column\b",
    r"\bdelete\s+from\b(?!.*\bwhere\b)",     # DELETE without WHERE
    r"rm\s+-rf\s+/",
    r"OPENAI_API_KEY\s*=",
    r"sk-[A-Za-z0-9]{10,}",                  # API keys
]

def _collect_text(args, kwargs) -> str:
    parts = []
    for a in args:
        if isinstance(a, str):
            parts.append(a)
        else:
            try:
                parts.append(json.dumps(a, default=str)[:8000])
            except Exception:
                pass
    if kwargs:
        try:
            parts.append(json.dumps(kwargs, default=str)[:8000])
        except Exception:
            pass
    return "\n".join(parts)

def review(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    """
    Returns a dict:
      {
        "approved": bool,
        "reason": str,
        "findings": [patterns],
        "strict": bool
      }
    Dispatcher calls decision.get("approved"), so dict is required.
    """
    text = _collect_text(args, kwargs)
    findings = [pat for pat in DANGEROUS
                if re.search(pat, text, flags=re.IGNORECASE | re.MULTILINE)]

    if findings and STRICT:
        reason = f"reject: matched dangerous patterns: {findings}"
        decision = {"approved": False, "reason": reason, "findings": findings, "strict": True}
        print(f"REVIEW DECISION: REJECT — {reason}")
        return decision

    if findings and not STRICT:
        reason = f"approve(report): risky patterns found but STRICT=off: {findings}"
        decision = {"approved": True, "reason": reason, "findings": findings, "strict": False}
        print(f"REVIEW DECISION: APPROVE (report-only) — {reason}")
        return decision

    reason = "approve: no dangerous patterns detected"
    decision = {"approved": True, "reason": reason, "findings": [], "strict": STRICT}
    print(f"REVIEW DECISION: APPROVE — {reason}")
    return decision