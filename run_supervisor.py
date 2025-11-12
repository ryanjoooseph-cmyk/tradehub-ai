import time
import subprocess

while True:
    # 1) run one task
    subprocess.run(["python", "agent_dispatcher.py"])

    # 2) (later) feed from manifest
    # subprocess.run(["python", "feed_from_manifest.py"])

    # 3) (later) sync finished tasks
    # subprocess.run(["python", "sync_to_github.py"])

    # 4) sleep
    time.sleep(2)