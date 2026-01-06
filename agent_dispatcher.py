# agent_dispatcher.py
import os, sys, time, signal
import json
from typing import List, Dict

# Ensure imports work both locally and on Render
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, "/opt/render/project/src")

from feed_from_manifest import load_tasks  # relies on manifest/tasks.json

SHUTDOWN = False
POLL_SECONDS = int(os.getenv("POLL_SECONDS", "30"))

def _handle_sigterm(*_):
    global SHUTDOWN
    SHUTDOWN = True
signal.signal(signal.SIGTERM, _handle_sigterm)
signal.signal(signal.SIGINT, _handle_sigterm)

def review(task: Dict) -> bool:
    # super-basic guard so bad entries don't crash the loop
    ok = all(k in task for k in ("task_type", "feature"))
    print(f"[review] {'APPROVE' if ok else 'REJECT'} — basic validation {'passed' if ok else 'failed'}", flush=True)
    return ok

def run_once() -> None:
    tasks: List[Dict] = load_tasks()
    print(f"[feed] loaded {len(tasks)} task definitions", flush=True)

    for t in tasks:
        if not review(t):
            continue
        tt = t.get("task_type")
        feature = t.get("feature")
        route = t.get("route", "")
        print(f"[runner] executing task_type={tt} feature={feature} route={route}", flush=True)
        # TODO: call your real executors here
        # e.g., execute_codegen_backend(t) / execute_codegen_frontend(t)
        # Keep each run guarded so one failure doesn't kill the worker:
        try:
            time.sleep(0.5)  # simulate work
        except Exception as e:
            print(f"[runner] ERROR: {e!r}", flush=True)

def main() -> None:
    print("[boot] worker started", flush=True)
    tick = 0
    while not SHUTDOWN:
        try:
            run_once()
        except Exception as e:
            # Log and continue; don’t exit the process
            print(f"[fatal] run_once crashed: {e!r}", file=sys.stderr, flush=True)
        tick += 1
        print(f"[loop] sleeping {POLL_SECONDS}s (tick {tick})", flush=True)
        for _ in range(POLL_SECONDS):
            if SHUTDOWN:
                break
            time.sleep(1)
    print("[shutdown] graceful exit", flush=True)

if __name__ == "__main__":
    main()
