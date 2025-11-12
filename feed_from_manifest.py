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

def insert_backend(feature, table=None, route=None, notes=None):
    conn = get_conn()
    try:
      payload = {"feature": feature}
      if table: payload["table"] = table
      if route: payload["route"] = route
      if notes: payload["notes"] = notes

      with conn.cursor() as cur:
        cur.execute(
          "INSERT INTO agent_tasks (task_type, payload) VALUES (%s, %s::jsonb);",
          ('codegen_backend', json.dumps(payload))
        )
      conn.commit()
    finally:
      conn.close()

def insert_frontend(feature, route, notes=None):
    conn = get_conn()
    try:
      payload = {"feature": feature, "route": route}
      if notes: payload["notes"] = notes
      with conn.cursor() as cur:
        cur.execute(
          "INSERT INTO agent_tasks (task_type, payload) VALUES (%s, %s::jsonb);",
          ('codegen_frontend', json.dumps(payload))
        )
      conn.commit()
    finally:
      conn.close()

def main():
    # manifest.json must be in the same folder
    with open("manifest.json", "r") as f:
      manifest = json.load(f)

    for section, parts in manifest.items():
      for item in parts.get("backend", []):
        feat = item["feature"]
        if not task_exists(feat):
          insert_backend(
            feat,
            item.get("table"),
            item.get("route"),
            item.get("notes")
          )
      for item in parts.get("frontend", []):
        feat = item["feature"]
        if not task_exists(feat):
          insert_frontend(
            feat,
            item["route"],
            item.get("notes")
          )

if __name__ == "__main__":
    main()
