import os, json
from openai import OpenAI

MODEL = os.getenv("REVIEWER_MODEL", "gpt-4o")
RULES = """
You are a strict code reviewer for a Next.js 14 + TypeScript + Supabase app.
Inputs:
- task_desc: human description of intent
- diff: JSON array of items: {"file_path","operation","content?"}
Checks:
- Path safety: only app/**, app/api/**, lib/**, db/**, tests/**.
- SQL idempotency in db/sql/*.sql (CREATE IF NOT EXISTS, safe ALTER; no destructive operations).
- TypeScript/TSX syntactic plausibility (imports, exported handlers, no obvious errors).
- Next.js 14 route structure in /app/api/**/route.ts with correct exports (GET/POST/...).
- No secrets in code; environment variables are read via process.env only.
- Minimal Tailwind; no stray CSS frameworks.
- For deletes, ensure file_path is reasonable and not critical (avoid mass deletions).

Return STRICT JSON only:
{"decision":"approve"|"reject","notes":"brief reason(s)","risk":"low|med|high"}
"""

def review(diff_json_text: str, task_desc: str) -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = (
        "task_desc:\n" + task_desc + "\n\n"
        "diff:\n" + diff_json_text + "\n\n" + RULES
    )
    resp = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[{"role":"user","content":prompt}]
    )
    content = resp.choices[0].message.content.strip()
    try:
        return json.loads(content)
    except Exception:
        return {"decision":"reject","notes":"Non-JSON response from reviewer","risk":"high"}
