import os
import json
import psycopg2
import subprocess
import tempfile
from datetime import datetime

DB_DSN = os.environ["TRADEHUB_DB_DSN"]
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
TARGET_REPO = os.environ.get("TARGET_REPO")  # e.g. "yourname/tradehub-app"

if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN not set")
if not TARGET_REPO:
    raise RuntimeError("TARGET_REPO not set")

def get_conn():
    return psycopg2.connect(DB_DSN)

def fetch_done_tasks(limit: int = 5):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, task_type, payload, result
                FROM agent_tasks
                WHERE status='done'
                  AND result IS NOT NULL
                ORDER BY updated_at ASC
                LIMIT %s;
            """, (limit,))
            rows = cur.fetchall()
            return rows
    finally:
        conn.close()

def mark_synced(task_id):
    # we can reuse error column or add a tiny flag – for now just leave as done
    # if you want to avoid re-syncing, you can update result to NULL or add a column
    pass

def main():
    tasks = fetch_done_tasks()
    if not tasks:
        print("sync: nothing to sync")
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        repo_url = f"https://{GITHUB_TOKEN}:x-oauth-basic@github.com/{TARGET_REPO}.git"
        subprocess.check_call(["git", "clone", repo_url, tmpdir])

        # make sure folder exists
        ai_dir = os.path.join(tmpdir, "app", "ai_generated")
        os.makedirs(ai_dir, exist_ok=True)

        for (task_id, task_type, payload, result) in tasks:
            payload = payload or {}
            feature = payload.get("feature") or f"task_{task_id}"
            # normalize to txt for now – we can split TSX later
            out_path = os.path.join(ai_dir, f"{feature}.txt")
            with open(out_path, "w") as f:
                f.write(json.dumps({
                    "task_id": str(task_id),
                    "task_type": task_type,
                    "payload": payload,
                    "result": result,
                }, indent=2))

            mark_synced(task_id)

        now = datetime.utcnow().isoformat()
        subprocess.check_call(["git", "-C", tmpdir, "add", "."])
        # if there's nothing to commit, this will fail – so wrap it
        try:
            subprocess.check_call(["git", "-C", tmpdir, "commit", "-m", f"ai sync {now}"])
            subprocess.check_call(["git", "-C", tmpdir, "push"])
        except subprocess.CalledProcessError:
            print("sync: nothing new to commit")

if __name__ == "__main__":
    main()
