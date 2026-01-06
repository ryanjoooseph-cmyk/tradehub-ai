from __future__ import annotations
import sys, uuid, traceback
from typing import Dict, Any, List

from feed_from_manifest import load_tasks
from reviewer_agent import review, APPROVE

def _execute(task: Dict[str, Any]) -> None:
    # Wire this to your real builders later
    print(f"[runner] executing task_type={task.get('task_type')} feature={task.get('feature')} route={task.get('route')}")

def dispatch() -> None:
    tasks: List[Dict[str, Any]] = load_tasks()
    print(f"[feed] loaded {len(tasks)} task definitions")

    for task in tasks:
        task_id = str(uuid.uuid4())
        try:
            if not isinstance(task, dict):
                raise TypeError(f"Bad task type: {type(task).__name__}")

            decision = review(task)
            dec = (decision or {}).get("decision", "").upper()
            rsn = (decision or {}).get("reason", "")

            if dec == APPROVE:
                print(f"[review] {dec} — {rsn}")
                _execute(task)
            else:
                print(f"[review] REJECT — {rsn}")
        except Exception as e:
            print(f"[dispatcher] task {task_id} ERROR: {e}", file=sys.stderr)
            traceback.print_exc()

if __name__ == "__main__":
    dispatch()
