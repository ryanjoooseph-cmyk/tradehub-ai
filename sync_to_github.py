import os
import json
import psycopg2
import tempfile
import subprocess
from datetime import datetime

DB_DSN = os.environ["TRADEHUB_DB_DSN"]
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # set later in Render
TARGET_REPO = os.environ.get("TARGET_REPO")    # e.g. "yourname/tradehub-app"


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
    # if we don't have git creds, don't die
    if not GITHUB_TOKEN or not TARGET_REPO:
        print("sync_to_github: missing GITHUB_TOKEN or TARGET_REPO, skipping")
        return

    rows = fetch_done_tasks()
    if not rows:
        print("sync_to_github: no done tasks to sync")
        return

    # clone repo to temp dir
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_url = f"https://{GITHUB_TOKEN}:x-oauth-basic@github.com/{TARGET_REPO}.git"
        subprocess.check_call(["git", "clone", repo_url, tmpdir])

        # we'll drop outputs in app/ai_generated
        ai_dir = os.path.join(tmpdir, "app", "ai_generated")
        os.makedirs(ai_dir, exist_ok=True)

        for (task_id, payload, result) in rows:
            # payload/result from psycopg come as dict already (because jsonb)
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

        # git add/commit/push
        subprocess.check_call(["git", "-C", tmpdir, "add", "."])
        msg = f"AI sync {datetime.utcnow().isoformat()}"
        subprocess.check_call(["git", "-C", tmpdir, "commit", "-m", msg])
        subprocess.check_call(["git", "-C", tmpdir, "push"])

        print("sync_to_github: pushed")


if __name__ == "__main__":
    main()