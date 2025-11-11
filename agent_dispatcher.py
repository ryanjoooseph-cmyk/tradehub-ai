import os, json, psycopg2
from crewai import Crew
from crew_test import (
    onboarding,
    job_helper,
    dispute_agent,
    make_onboard_task,
    make_job_task,
    make_dispute_task,
)
from codegen_agents import (
    frontend_agent,
    backend_agent,
    make_frontend_task,
    make_backend_task,
)

DB_DSN = os.environ["TRADEHUB_DB_DSN"]

def get_conn():
    return psycopg2.connect(DB_DSN)

def get_one_pending_task():
    conn = get_conn()
    conn.autocommit = False
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, task_type, payload
                FROM agent_tasks
                WHERE status='pending'
                ORDER BY created_at
                FOR UPDATE SKIP LOCKED
                LIMIT 1;
            """)
            row = cur.fetchone()
            if not row:
                conn.commit()
                return None
            task_id, task_type, payload = row
            cur.execute("UPDATE agent_tasks SET status='running', updated_at=NOW() WHERE id=%s;", (task_id,))
            conn.commit()
            return {"id": task_id, "task_type": task_type, "payload": payload}
    finally:
        conn.close()

def save_result(task_id, result_json):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE agent_tasks SET status='done', result=%s, updated_at=NOW() WHERE id=%s;",
                (json.dumps(result_json), task_id)
            )
        conn.commit()
    finally:
        conn.close()

def save_error(task_id, msg):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE agent_tasks SET status='error', error=%s, updated_at=NOW() WHERE id=%s;",
                (msg, task_id)
            )
        conn.commit()
    finally:
        conn.close()

if __name__ == "__main__":
    task = get_one_pending_task()
    if not task:
        print("no tasks")
        raise SystemExit(0)

    ttype = task["task_type"]
    payload = task["payload"] or {}

    try:
        if ttype == "onboard":
            crew = Crew(agents=[onboarding], tasks=[make_onboard_task(payload)])
        elif ttype == "job":
            crew = Crew(agents=[job_helper], tasks=[make_job_task(payload)])
        elif ttype == "dispute":
            crew = Crew(agents=[dispute_agent], tasks=[make_dispute_task(payload)])
        elif ttype == "codegen_frontend":
            crew = Crew(agents=[frontend_agent], tasks=[make_frontend_task(payload)])
        elif ttype == "codegen_backend":
            crew = Crew(agents=[backend_agent], tasks=[make_backend_task(payload)])
        else:
            raise ValueError(f"unknown task_type: {ttype}")

        results = crew.kickoff()
        out = [str(r) for r in results]
        save_result(task["id"], out)
        print("done", task["id"])
    except Exception as e:
        save_error(task["id"], str(e))
        raise
