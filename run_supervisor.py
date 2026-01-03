import time
import subprocess

INTERVAL_SECONDS = 60

def run_once():
    subprocess.run(["python", "agent_dispatcher.py"], check=False)

if __name__ == "__main__":
    while True:
        run_once()
        time.sleep(INTERVAL_SECONDS)
