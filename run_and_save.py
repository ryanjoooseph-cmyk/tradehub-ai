import json
import datetime
from crew_test import crew

try:
    results = crew.kickoff()
    payload = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "results": [str(r) for r in results],
    }
    with open("agent_output.log", "a") as f:
        f.write(json.dumps(payload) + "\n")
    print("saved")
except KeyboardInterrupt:
    print("stopped by user")
except Exception as e:
    print(f"error: {e}")
