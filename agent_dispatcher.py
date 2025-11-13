# agent_dispatcher.py
# Robust dispatcher: never assumes perfect JSON, never assumes reviewer shape.
# Fixes:
#  - tolerate tuple returns ("tuple has no attribute 'get'")
#  - tolerate reviewer(task, something) arity
#  - tolerate LLM/non-JSON payload strings ("Extra data..." decoder issues)

import json
import re
import traceback
from typing import Any, Dict, Tuple, Union
from reviewer_agent import review

JSON_OBJ_RE = re.compile(r"\{.*\}", re.DOTALL)

def _extract_first_json_obj(text: str) -> Union[Dict[str, Any], None]:
    """Try strict JSON, then best-effort first balanced-ish object."""
    if not isinstance(text, str):
        return None
    # 1) Strict
    try:
        return json.loads(text)
    except Exception:
        pass
    # 2) Grab first {...}
    m = JSON_OBJ_RE.search(text)
    if m:
        candidate = m.group(0)
        try:
            return json.loads(candidate)
        except Exception:
            return None
    return None

def smart_json(value: Any) -> Any:
    """
    - dict/list → return as is
    - str → try to JSON-decode; if 'extra data' or mixed text, extract first object
    - otherwise return as-is
    """
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            obj = _extract_first_json_obj(value)
            return obj if obj is not None else {"raw": value}
        except Exception:
            return {"raw": value}
    return value

def normalize_review(ret: Any) -> Dict[str, Any]:
    """
    Accept tuple, dict, string, etc. Always yield a dict with .get available.
    """
    if isinstance(ret, dict):
        return ret
    if isinstance(ret, tuple):
        # e.g., ("APPROVE", "reason")
        out: Dict[str, Any] = {}
        if len(ret) > 0:
            out["decision"] = ret[0]
        if len(ret) > 1:
            out["reason"] = ret[1]
        return out
    if isinstance(ret, str):
        # Try JSON in the string; else treat as reason with APPROVE
        maybe = _extract_first_json_obj(ret)
        if isinstance(maybe, dict):
            return maybe
        return {"decision": "APPROVE", "reason": ret}
    return {"decision": "APPROVE", "reason": "fallback normalization"}

def run_task(task: Dict[str, Any]) -> None:
    """
    Placeholder runner. This is where you'd call your backend/frontend codegen, etc.
    Kept minimal to avoid crashes while we stabilize the pipeline.
    """
    # Example: mark as 'done' or emit any side-effect your system expects.
    print(f"[dispatcher] executed task feature={task.get('feature')}")

def handle_task(task: Dict[str, Any]) -> Tuple[str, str]:
    """
    Returns (status, message)
    status ∈ {"APPROVED","REJECTED","SKIPPED","ERROR"}
    """
    try:
        # Normalize payload & feature fields; callers sometimes pass strings.
        payload = smart_json(task.get("payload"))
        if isinstance(task.get("feature"), dict) or task.get("feature") is None:
            # If 'feature' was a dict or missing, try to lift from payload/name
            feat = None
            if isinstance(payload, dict):
                feat = payload.get("feature") or payload.get("name")
            task["feature"] = feat or task.get("feature")

        task["payload"] = payload

        # Safe review call (accepts extra args)
        raw_rev = review(task, {"caller": "agent_dispatcher"})
        rev = normalize_review(raw_rev)
        decision = (rev.get("decision") or "APPROVE").upper()

        if decision.startswith("REJECT"):
            return "REJECTED", rev.get("reason", "rejected")

        # APPROVED path
        run_task(task)
        return "APPROVED", rev.get("reason", "approved")
    except Exception as e:
        tb = traceback.format_exc(limit=2)
        return "ERROR", f"{e.__class__.__name__}: {e}; {tb}"

def main():
    """
    Your real runner likely loops over queued tasks. Here we show one-shot safety.
    Wire this up to whatever fetch mechanism you already have.
    """
    # Example single task shell (replace with your real task fetch)
    example_task = {
        "feature": "example",
        "payload": '{"name": "example", "instructions": "do work"}'
    }
    status, msg = handle_task(example_task)
    print(f"agent_dispatcher: task example {status}: {msg}")

if __name__ == "__main__":
    main()