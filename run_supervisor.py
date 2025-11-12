import time
import subprocess

while True:
    # 1) make sure required tasks exist
    subprocess.run(["python", "feed_from_manifest.py"])

    # 2) run one agent task
    subprocess.run(["python", "agent_dispatcher.py"])

    # 3) try to sync (this will now skip if env not set)
    subprocess.run(["python", "sync_to_github.py"])

    # 4) sleep
    time.sleep(2)