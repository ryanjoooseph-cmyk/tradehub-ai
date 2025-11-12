import time
import subprocess

while True:
    # 1) make sure required tasks exist
    subprocess.run(["python", "feed_from_manifest.py"])

    # 2) run one agent task
    subprocess.run(["python", "agent_dispatcher.py"])

    # 3) try to sync finished tasks into app repo (no-op if env missing)
    subprocess.run(["python", "sync_to_github.py"])

    # 4) sleep
    time.sleep(2)