import os
import json
import psycopg2

DB_DSN = os.environ["TRADEHUB_DB_DSN"]  # already set on Render


def get_conn():
    return psycopg2.connect(DB_DSN)


def main():
    # load manifest from file
    with open("manifest.json", "r") as f:
        manifest = json.load(f)

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            for item in manifest:
                feature = item["feature"]
                task_type = item["task_type"]
                route = item.get("route", "")
                notes = item.get("notes", "")

                # check if this feature already exists in agent_tasks
                cur.execute(
                    """
                    SELECT 1
                    FROM agent_tasks
                    WHERE payload->>'feature' = %s
                    LIMIT 1;
                    """,
                    (feature,),
                )
                exists = cur.fetchone()

                if not exists:
                    payload = json.dumps(
                        {
                            "feature": feature,
                            "route": route,
                            "notes": notes,
                        }
                    )
                    cur.execute(
                        """
                        INSERT INTO agent_tasks (task_type, payload, status)
                        VALUES (%s, %s::jsonb, 'pending');
                        """,
                        (task_type, payload),
                    )
                    print(f"feed_from_manifest: inserted {feature}")
                else:
                    # nothing to do
                    pass

        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    main()