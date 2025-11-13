import time, subprocess

SLEEP_SECONDS = 2  # keep aggressive loop

while True:
    # 1) Ensure one-off required features exist
    subprocess.run(["python", "feed_from_manifest.py"])

    # 2) Keep the backlog topped up to your threshold
    subprocess.run(["python", "auto_topup.py"])

    # 3) Process one task
    subprocess.run(["python", "agent_dispatcher.py"])

    # 4) Wait
    time.sleep(SLEEP_SECONDS)