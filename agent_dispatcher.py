# agent_dispatcher.py
import os, sys, time, signal
from typing import List, Dict

# make imports work both locally and on Render
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, "/opt/render/project/src")

from feed_from_manifest import load_tasks

SHUTDOWN = False
POLL_SECONDS = int(os.getenv("POLL_SECONDS", "30"))

def _sigterm(*_):
    global SHUTDOWN
    SHUTDOWN = True
signal.signal(signal.SIGTERM, _sigterm)
signal.signal(signal.SIGINT, _sigterm)

def review(task: Dict) -> bool:
    ok = all(k in task for k in ("task_type", "feature"))
    print(f"[review] {'APPROVE' if ok else 'REJECT'} — basic validation {'passed' if ok else 'failed'}", flush=True)
    return ok

def run_once() -> None:
    tasks: List[Dict] = load_tasks()
    print(f"[feed] loaded {len(tasks)} task definitions", flush=True)
    for t in tasks:
        if not review(t):
            continue
        print(
            f"[runner] executing task_type={t.get('task_type')} "
            f"feature={t.get('feature')} route={t.get('route','')}",
            flush=True,
        )
        time.sleep(0.5)  # TODO: call real executors

def main() -> None:
    print("[boot] worker started", flush=True)
    tick = 0
    while not SHUTDOWN:
        try:
            run_once()
        except Exception as e:
            print(f"[fatal] run_once crashed: {e!r}", flush=True)
        tick += 1
        print(f"[loop] sleeping {POLL_SECONDS}s (tick {tick})", flush=True)
        for _ in range(POLL_SECONDS):
            if SHUTDOWN:
                break
            time.sleep(1)
    print("[shutdown] graceful exit", flush=True)

if __name__ == "__main__":
    main()
