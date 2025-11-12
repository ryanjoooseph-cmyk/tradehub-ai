import os
import json
import psycopg2
import subprocess
import tempfile
from datetime import datetime

DB_DSN = os.environ["TRADEHUB_DB_DSN"]
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
TARGET_REPO = os.environ.get("TARGET_REPO")  # e.g. "ryanjoooseph-cmyk/tradehub-app"

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
            return cur.fetchall()
    finally:
        conn.close()

def main():
    tasks = fetch_done_tasks()
    if not tasks:
        print("sync: nothing to sync")
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        repo_url = f"https://{GITHUB_TOKEN}:x-oauth-basic@github.com/{TARGET_REPO}.git"
        subprocess.check_call(["git", "clone", repo_url, tmpdir])

        # set identity so commit works in Render
        subprocess.check_call(["git", "-C", tmpdir, "config", "user.email", "bot@tradehub.local"])
        subprocess.check_call(["git", "-C", tmpdir, "config", "user.name", "TradeHub Bot"])

        ai_dir = os.path.join(tmpdir, "app", "ai_generated")
        os.makedirs(ai_dir, exist_ok=True)

        for (task_id, task_type, payload, result) in tasks:
            payload = payload or {}
            feature = payload.get("feature") or f"task_{task_id}"
            out_path = os.path.join(ai_dir, f"{feature}.txt")
            with open(out_path, "w") as f:
                f.write(json.dumps({
                    "task_id": str(task_id),
                    "task_type": task_type,
                    "payload": payload,
                    "result": result,
                }, indent=2))

        now = datetime.utcnow().isoformat()
        subprocess.check_call(["git", "-C", tmpdir, "add", "."])
        try:
            subprocess.check_call(["git", "-C", tmpdir, "commit", "-m", f"ai sync {now}"])
            subprocess.check_call(["git", "-C", tmpdir, "push"])
        except subprocess.CalledProcessError:
            print("sync: nothing new to commit")

if __name__ == "__main__":
    main()
