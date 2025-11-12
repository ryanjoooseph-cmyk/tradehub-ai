import os
import json
import psycopg2
import tempfile
import subprocess
from datetime import datetime

DB_DSN = os.environ["TRADEHUB_DB_DSN"]

# all of these must exist, otherwise we skip
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
TARGET_REPO = os.environ.get("TARGET_REPO")      # e.g. "yourname/tradehub-app"
GIT_USER_NAME = os.environ.get("GIT_USER_NAME")  # e.g. "Ryan"
GIT_USER_EMAIL = os.environ.get("GIT_USER_EMAIL")  # e.g. "you@example.com"


def get_conn():
    return psycopg2.connect(DB_DSN)


def fetch_done_tasks(limit=5):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, payload, result
                FROM agent_tasks
                WHERE status = 'done'
                  AND result IS NOT NULL
                ORDER BY updated_at DESC
                LIMIT %s;
                """,
                (limit,),
            )
            return cur.fetchall()
    finally:
        conn.close()


def main():
    # if ANY of these are missing, just skip — don't error
    if not (GITHUB_TOKEN and TARGET_REPO and GIT_USER_NAME and GIT_USER_EMAIL):
        print("sync_to_github: missing git/env config, skipping")
        return

    rows = fetch_done_tasks()
    if not rows:
        print("sync_to_github: no done tasks to sync")
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        repo_url = f"https://{GITHUB_TOKEN}:x-oauth-basic@github.com/{TARGET_REPO}.git"
        subprocess.check_call(["git", "clone", repo_url, tmpdir])

        # set identity inside this repo
        subprocess.check_call(["git", "-C", tmpdir, "config", "user.name", GIT_USER_NAME])
        subprocess.check_call(["git", "-C", tmpdir, "config", "user.email", GIT_USER_EMAIL])

        ai_dir = os.path.join(tmpdir, "app", "ai_generated")
        os.makedirs(ai_dir, exist_ok=True)

        for (task_id, payload, result) in rows:
            feature = None
            if isinstance(payload, dict):
                feature = payload.get("feature")
            if not feature:
                feature = f"task_{task_id}"

            out_path = os.path.join(ai_dir, f"{feature}.json")
            with open(out_path, "w") as f:
                json.dump(
                    {
                        "task_id": str(task_id),
                        "payload": payload,
                        "result": result,
                    },
                    f,
                    indent=2,
                )

        subprocess.check_call(["git", "-C", tmpdir, "add", "."])
        msg = f"AI sync {datetime.utcnow().isoformat()}"
        subprocess.check_call(["git", "-C", tmpdir, "commit", "-m", msg])
        subprocess.check_call(["git", "-C", tmpdir, "push"])

        print("sync_to_github: pushed")


if __name__ == "__main__":
    main()