# agent_dispatcher.py
# Orchestrates: load tasks -> review -> (optionally) execute.
# The execute step is a stub; wire it to your real builders as you grow.

from __future__ import annotations
import sys, uuid, traceback
from typing import Dict, Any, List

from feed_from_manifest import load_tasks
from reviewer_agent import review, APPROVE

def _execute(task: Dict[str, Any]) -> None:
    """
    Replace this with your actual execution (codegen / migrations / PRs).
    For now, it's a no-op so production won't crash while wiring things up.
    """
    # Example debug print (kept terse for Render logs):
    print(f"[runner] executing feature={task.get('feature')}")

def dispatch() -> None:
    tasks: List[Dict[str, Any]] = load_tasks()
    print(f"[feed] loaded {len(tasks)} task definitions")

    for task in tasks:
        task_id = str(uuid.uuid4())
        try:
            # Ensure the task is a dict (defensive against bad inputs)
            if not isinstance(task, dict):
                raise TypeError(f"Bad task type: {type(task).__name__}")

            decision = review(task)
            dec = (decision or {}).get("decision", "").upper()
            rsn = (decision or {}).get("reason", "")

            if dec == APPROVE:
                print("Would you like to view your execution traces? [y/N]: REVIEW DECISION:",
                      "APPROVE —", rsn)
                _execute(task)
            else:
                print(f"agent_dispatcher: task {task_id} REJECTED by reviewer")
        except Exception as e:
            print(f"agent_dispatcher: task {task_id} ERROR: {e}", file=sys.stderr)
            traceback.print_exc()

if __name__ == "__main__":
    dispatch()