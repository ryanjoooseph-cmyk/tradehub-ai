from __future__ import annotations
from typing import Dict, Any

APPROVE = "APPROVE"
REJECT = "REJECT"
_REQ = ("task_type","feature","route")

def review(task: Dict[str, Any]) -> Dict[str, str]:
    missing = [k for k in _REQ if not task.get(k)]
    if missing:
        return {"decision": REJECT, "reason": "missing: " + ", ".join(missing)}
    return {"decision": APPROVE, "reason": "basic validation passed"}
