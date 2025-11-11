import time
import subprocess

while True:
    subprocess.run(["python", "agent_dispatcher.py"])
    time.sleep(10)
