from crewai import Agent, Task
from crewai.llm import LLM

# Use strong model for higher quality; you can switch to "gpt-4o-mini" for bulk
llm = LLM(model="gpt-4o")

SYSTEM_JSON_DIFF = (
    "You generate STRICT JSON diffs for a Next.js 14 (app router) + TypeScript + Supabase app.\n"
    "Output ONLY JSON (no markdown, no prose). Each item must be an object with:\n"
    '{"file_path": "string", "operation": "write|append|delete", "content": "string optional for delete"}\n'
    "Paths must be under: app/**, app/api/**, lib/**, db/**, tests/**.\n"
    "SQL migrations go under db/sql/*.sql and must be idempotent (CREATE IF NOT EXISTS, safe ALTERs).\n"
    "Route handlers must be Next.js 14 /app/api/**/route.ts using TypeScript.\n"
    "Frontend pages must be TSX with minimal Tailwind and correct imports.\n"
    "NEVER include explanations; ONLY return a JSON array of diff items."
)

frontend_agent = Agent(
    role="Next.js frontend generator",
    goal="Produce minimal, correct TSX pages/components and related files via STRICT JSON diffs.",
    backstory=SYSTEM_JSON_DIFF,
    llm=llm,
)

backend_agent = Agent(
    role="Supabase/backend generator",
    goal="Produce idempotent SQL and Next.js 14 route handlers via STRICT JSON diffs.",
    backstory=SYSTEM_JSON_DIFF,
    llm=llm,
)

def make_frontend_task(payload: dict) -> Task:
    return Task(
        name=f"generate_frontend_{payload.get('feature','unknown')}",
        description=(
            "Create or update the specified frontend route/page/component for TradeHub using STRICT JSON diff format.\n"
            "Use TypeScript + Tailwind. Fetch from referenced API routes if given.\n"
            f"Payload: {payload}"
        ),
        agent=frontend_agent,
        expected_output=(
            "A JSON array of diff items: "
            '[{"file_path":"app/.../page.tsx","operation":"write","content":"<tsx>..."}]'
        ),
    )

def make_backend_task(payload: dict) -> Task:
    return Task(
        name=f"generate_backend_{payload.get('feature','unknown')}",
        description=(
            "Generate idempotent SQL (tables, indexes, RLS if needed) and Next.js 14 route handlers "
            "for the given feature using STRICT JSON diff format.\n"
            f"Payload: {payload}"
        ),
        agent=backend_agent,
        expected_output=(
            "A JSON array of diff items. Example:\n"
            '[{"file_path":"db/sql/001_jobs.sql","operation":"write","content":"CREATE TABLE IF NOT EXISTS ...;"},'
            '{"file_path":"app/api/jobs/route.ts","operation":"write","content":"import ...; export async function ..."}]'
        ),
    )