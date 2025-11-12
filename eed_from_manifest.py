import os
import json
import psycopg2

DB_DSN = os.environ["TRADEHUB_DB_DSN"]

def get_conn():
    return psycopg2.connect(DB_DSN)

def task_exists(feature: str) -> bool:
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 1
                FROM agent_tasks
                WHERE (payload->>'feature') = %s
                  AND status IN ('pending','running','done')
                LIMIT 1;
            """, (feature,))
            return cur.fetchone() is not None
    finally:
        conn.close()

def insert_backend_task(feature: str, table: str = None, route: str = None, notes: str = None):
    conn = get_conn()
    try:
        payload = {
            "feature": feature,
        }
        if table:
            payload["table"] = table
        if route:
            payload["route"] = route
        if notes:
            payload["notes"] = notes

        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO agent_tasks (task_type, payload) VALUES (%s, %s::jsonb);",
                ('codegen_backend', json.dumps(payload))
            )
        conn.commit()
    finally:
        conn.close()

def insert_frontend_task(feature: str, route: str, notes: str = None):
    conn = get_conn()
    try:
        payload = {
            "feature": feature,
            "route": route,
        }
        if notes:
            payload["notes"] = notes
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO agent_tasks (task_type, payload) VALUES (%s, %s::jsonb);",
                ('codegen_frontend', json.dumps(payload))
            )
        conn.commit()
    finally:
        conn.close()

def main():
    # load manifest.json (sitting next to this file)
    with open("manifest.json", "r") as f:
        manifest = json.load(f)

    # walk through sections
    for section, parts in manifest.items():
        backend_items = parts.get("backend", [])
        frontend_items = parts.get("frontend", [])

        # backend
        for item in backend_items:
            feature = item["feature"]
            table = item.get("table")
            route = item.get("route")
            notes = item.get("notes")
            if not task_exists(feature):
                insert_backend_task(feature, table, route, notes)

        # frontend
        for item in frontend_items:
            feature = item["feature"]
            route = item["route"]
            notes = item.get("notes")
            if not task_exists(feature):
                insert_frontend_task(feature, route, notes)

if __name__ == "__main__":
    main()
