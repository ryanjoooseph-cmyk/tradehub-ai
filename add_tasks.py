import os
import json
import psycopg2

DSN = os.environ["TRADEHUB_DB_DSN"]

TASKS = [
    {
        "task_type": "onboard",
        "payload": {
            "name": "Perth Plumbing Co",
            "abn": "12345678901",
            "trade_type": "Plumber",
            "service_area": "Perth, WA",
            "phone": "0400000000",
            "email": "hello@perthplumbing.com"
        }
    },
    {
        "task_type": "job",
        "payload": {
            "job_title": "Bathroom tiling repair",
            "description": "Tiles laid but not grouted properly, water getting through.",
            "location": "Perth, WA",
            "budget": "$400 - $700",
            "photos": ["https://example.com/bathroom-before.jpg"]
        }
    },
    {
        "task_type": "dispute",
        "payload": {
            "job_id": 9912,
            "customer": "Kate",
            "tradie": "Perth Plumbing Co",
            "issue": "tiling not finished, edges exposed, water ingress",
            "evidence": [
                "https://example.com/before.jpg",
                "https://example.com/after.jpg"
            ]
        }
    }
]

conn = psycopg2.connect(DSN)
try:
    with conn.cursor() as cur:
        for t in TASKS:
            cur.execute(
                "INSERT INTO agent_tasks (task_type, payload) VALUES (%s, %s);",
                (t["task_type"], json.dumps(t["payload"]))
            )
    conn.commit()
    print(f"inserted {len(TASKS)} tasks")
finally:
    conn.close()
