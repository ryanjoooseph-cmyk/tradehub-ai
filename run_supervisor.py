import time
import subprocess

while True:
    # 1) make sure required tasks exist
    subprocess.run(["python", "feed_from_manifest.py"])

    # 2) run one task
    subprocess.run(["python", "agent_dispatcher.py"])

    # 3) pause a bit (you can drop to 2 later)
    time.sleep(5)
