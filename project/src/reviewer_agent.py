# reviewer_agent.py
import os, json, datetime
from openai import OpenAI

MODEL = os.getenv("REVIEWER_MODEL", "gpt-4o")
RULES = """
You are a strict code reviewer for a Next.js 14 + TS + Supabase app.
- Approve only if the diff is syntactically valid, typed, and matches the task intent.
- SQL must be idempotent (CREATE TABLE IF NOT EXISTS, safe ALTERs).
- No secrets, no breaking RLS/policies, no wide deletes.
- Files must live under: app/api/**, app/**/page.tsx, db/** (SQL), lib/** (utils), tests/**.
Return STRICT JSON: {"decision":"approve"|"reject","notes":"...brief reasons..."} and nothing else.
"""

def review(diff: str, task_desc: str) -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = f"Task: {task_desc}\n\nDiff:\n{diff}\n\n{RULES}"
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    try:
        return json.loads(r.choices[0].message.content.strip())
    except Exception:
        return {"decision": "reject", "notes": "Non-JSON or invalid review response."}