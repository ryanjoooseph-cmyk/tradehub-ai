from __future__ import annotations
import os, sys, time, uuid, traceback
from typing import Dict, Any, List
from feed_from_manifest import load_tasks
from reviewer_agent import review, APPROVE
from builder_agent import build_files
from git_ops import open_pr_with_files
from gh_api import get_repo_default_branch

def _execute(task: Dict[str, Any]) -> None:
    repo = os.environ.get("TARGET_REPO")
    if not repo:
        print("[error] TARGET_REPO not set", file=sys.stderr)
        return
    files = build_files(task)
    if not files:
        print("[warn] no files to commit")
        return
    base = get_repo_default_branch(repo)
    if not base:
        print("[error] could not determine default branch", file=sys.stderr)
        return
    feature = str(task.get("feature") or "task")
    branch = f"agent-{feature}-{uuid.uuid4().hex[:8]}".replace("/", "-")
    pr = open_pr_with_files(repo=repo, base_branch=base, branch_name=branch, files=files, title=f"{feature}", body=f"Automated PR for {feature}")
    if pr:
        print(f"[pr] {pr}")

def dispatch(loop_interval_seconds: int = 30) -> None:
    print("[boot] worker started")
    tick = 0
    while True:
        tasks: List[Dict[str, Any]] = load_tasks()
        print(f"[feed] loaded {len(tasks)} task definitions")
        for task in tasks:
            try:
                decision = review(task)
                dec = (decision or {}).get("decision", "").upper()
                rsn = (decision or {}).get("reason", "")
                if dec == APPROVE:
                    print("[review] APPROVE —", rsn)
                    _execute(task)
                else:
                    print("[review] REJECT —", rsn)
            except Exception as e:
                print(f"[err] {e}", file=sys.stderr)
                traceback.print_exc()
        tick += 1
        print(f"[loop] sleeping {loop_interval_seconds}s (tick {tick})")
        try:
            time.sleep(loop_interval_seconds)
        except KeyboardInterrupt:
            print("[shutdown] graceful exit")
            return

if __name__ == "__main__":
    dispatch()
