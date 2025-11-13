import os, json, psycopg2, uuid, datetime, traceback
from typing import Optional, Dict, Any, List
from crewai import Crew
from codegen_agents import make_frontend_task, make_backend_task
from reviewer_agent import review
from diff_applier import apply_and_diff, commit_and_push

DB_DSN = os.environ["TRADEHUB_DB_DSN"]

# Optional Git sync (safe: if missing, we skip commits)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
TARGET_REPO  = os.environ.get("TARGET_REPO")        # e.g. "yourname/tradehub-app"
GIT_USER     = os.environ.get("GIT_COMMIT_NAME")    # e.g. "TradeHub AI"
GIT_EMAIL    = os.environ.get("GIT_COMMIT_EMAIL")   # e.g. "bot@tradehub.ai"

def conn():
    return psycopg2.connect(DB_DSN)

def fetch_one_pending(cur) -> Optional[Dict[str,Any]]:
    cur.execute("""
        SELECT id, task_type, payload
        FROM agent_tasks
        WHERE status='pending'
        ORDER BY created_at ASC
        FOR UPDATE SKIP LOCKED
        LIMIT 1;
    """)
    row = cur.fetchone()
    if not row:
        return None
    return {"id": row[0], "task_type": row[1], "payload": row[2]}

def set_status(cur, task_id, status, err: Optional[str]=None, result: Optional[Any]=None):
    if err is not None and len(err) > 2000:
        err = err[:2000]
    cur.execute("""
        UPDATE agent_tasks
        SET status=%s,
            error=%s,
            result=%s,
            updated_at=now()
        WHERE id=%s;
    """, (status, err, json.dumps(result) if result is not None else None, task_id))

def kickoff_codegen(task_type: str, payload: dict) -> str:
    """Run CrewAI with the right agent/task; return raw model text."""
    if task_type == "codegen_frontend":
        task = make_frontend_task(payload)
    else:
        task = make_backend_task(payload)
    crew = Crew(agents=[task.agent], tasks=[task])
    out = crew.kickoff()
    # Crew returns an object that usually has .raw or str()
    text = ""
    try:
        text = out.raw if hasattr(out, "raw") else str(out)
    except Exception:
        text = str(out)
    return text

def parse_diff_json(raw: str) -> List[Dict[str,Any]]:
    """Extract first JSON array/object from raw text and return as list of items."""
    # find first '[' or '{'
    s = raw.strip()
    start = min([i for i in [s.find("["), s.find("{")] if i != -1] or [-1])
    if start > 0:
        s = s[start:]
    data = json.loads(s)
    if isinstance(data, dict):
        data = [data]
    # basic validation
    for it in data:
        if not all(k in it for k in ["file_path","operation"]):
            raise ValueError("Invalid diff item; missing keys")
    return data

def main():
    with conn() as c:
        with c.cursor() as cur:
            job = fetch_one_pending(cur)
            if not job:
                print("agent_dispatcher: no tasks")
                return
            task_id = job["id"]
            cur.execute("UPDATE agent_tasks SET status='in_progress', updated_at=now() WHERE id=%s;", (task_id,))
        c.commit()

    # process outside the lock
    try:
        payload = job["payload"] if isinstance(job["payload"], dict) else json.loads(job["payload"])
        raw = kickoff_codegen(job["task_type"], payload)
        diff_items = parse_diff_json(raw)

        # Generate a real diff text for review (clone if creds, else temp)
        applied = apply_and_diff(
            diff_items,
            github_token=GITHUB_TOKEN,
            target_repo=TARGET_REPO,
            git_name=GIT_USER,
            git_email=GIT_EMAIL
        )
        diff_text = applied.get("diff_text","")

        # Reviewer gate
        decision = review(json.dumps(diff_items, ensure_ascii=False), payload.get("notes",""))
        if decision.get("decision") != "approve":
            # Mark as error with reviewer notes
            with conn() as c:
                with c.cursor() as cur:
                    set_status(cur, task_id, "error", f"REVIEW_REJECT: {decision.get('notes','')}", {"diff": diff_items})
                c.commit()
            print(f"agent_dispatcher: task {task_id} REJECTED by reviewer")
            return

        # Approved: if git creds exist, commit+push; else save result only
        committed = False
        if GITHUB_TOKEN and TARGET_REPO and GIT_USER and GIT_EMAIL:
            commit_and_push(
                diff_items,
                github_token=GITHUB_TOKEN,
                target_repo=TARGET_REPO,
                git_name=GIT_USER,
                git_email=GIT_EMAIL,
                commit_msg=f"AI: {job['task_type']} {payload.get('feature','')}"
            )
            committed = True

        with conn() as c:
            with c.cursor() as cur:
                set_status(cur, task_id, "done", None, {
                    "diff_items": diff_items,
                    "committed": committed
                })
            c.commit()
        print(f"agent_dispatcher: task {task_id} DONE (committed={committed})")

    except Exception as e:
        err = f"{type(e).__name__}: {e}\n{traceback.format_exc()}"
        with conn() as c:
            with c.cursor() as cur:
                set_status(cur, job["id"], "error", err, None)
            c.commit()
        print(f"agent_dispatcher: task {job['id']} ERROR: {e}")

if __name__ == "__main__":
    main()