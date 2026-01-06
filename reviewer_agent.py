from __future__ import annotations
from typing import Dict, Any

APPROVE = "APPROVE"
REJECT = "REJECT"

ALLOWED_TYPES = {"codegen_backend", "codegen_frontend"}

def review(task: Dict[str, Any]) -> Dict[str, str]:
    tt = str(task.get("task_type", "")).strip()
    route = str(task.get("route", "")).strip()
    feature = str(task.get("feature", "")).strip()

    if tt not in ALLOWED_TYPES:
        return {"decision": REJECT, "reason": f"unsupported task_type '{tt}'"}
    if not route.startswith("/"):
        return {"decision": REJECT, "reason": f"route must start with '/': got '{route}'"}
    if not feature:
        return {"decision": REJECT, "reason": "missing feature id"}
    return {"decision": APPROVE, "reason": "basic validation passed"}
