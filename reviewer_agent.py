# project/src/reviewer_agent.py
# Returns a STRUCTURED dict so the dispatcher never sees a tuple.

from typing import Any, Dict

RED_FLAG_SNIPPETS = [
    "drop table", "delete from", "truncate table",
    "os.system(", "subprocess.", "rm -rf /", "curl http",
    "alter role", "grant all", "xp_cmdshell"
]

def _to_text(x: Any) -> str:
    try:
        return x if isinstance(x, str) else str(x)
    except Exception:
        return ""

def review(task: Dict[str, Any]) -> Dict[str, Any]:
    """
    Inspect a task and return a structured decision.

    Must return:
      {
        "decision": "approve" | "reject",
        "approved": True|False,
        "reason": "<short explanation>"
      }
    """
    payload = task.get("payload") if isinstance(task, dict) else {}
    preview = ""
    if isinstance(payload, dict):
        preview += _to_text(payload.get("expected_output", ""))
        preview += "\n" + _to_text(payload.get("result_preview", ""))

    text = (_to_text(task.get("result")) + "\n" + preview).lower()

    red = [flag for flag in RED_FLAG_SNIPPETS if flag in text]
    if red:
        reason = f"Found potentially dangerous patterns: {', '.join(red)}"
        print("REVIEW DECISION: REJECT —", reason)
        return {"decision": "reject", "approved": False, "reason": reason}

    reason = "approve: no dangerous patterns detected"
    print("REVIEW DECISION: APPROVE —", reason)
    return {"decision": "approve", "approved": True, "reason": reason}