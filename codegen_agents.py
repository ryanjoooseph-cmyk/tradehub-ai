# codegen_agents.py  — FULL REPLACEMENT
from crewai import Agent, Task
from crewai.llm import LLM

# Use the stronger model you switched to
llm = LLM(model="gpt-4o")

frontend_agent = Agent(
    role="Next.js frontend generator",
    goal="Generate Next.js 14 app-router pages/components for TradeHub.",
    backstory="Output ONLY code. No explanations. Use TypeScript + Tailwind.",
    llm=llm,
)

backend_agent = Agent(
    role="Supabase/backend generator",
    goal="Generate SQL (DDL/DML) and Next.js 14 route handlers for TradeHub.",
    backstory="Output ONLY code. No explanations.",
    llm=llm,
)

def make_frontend_task(payload: dict) -> Task:
    """
    payload keys we rely on:
      - feature (str)
      - route (str) e.g., '/dashboard/jobs'
      - notes (str) optional guidance
    """
    return Task(
        name=f"generate_frontend_{payload.get('feature','unknown')}",
        description=(
            "Generate a Next.js 14 (app router) page component in TypeScript at the given route. "
            "Use Tailwind classes. Fetch from the referenced API route(s) in payload if present. "
            "Do not include explanations, ONLY the code."
            f"\nPayload: {payload}"
        ),
        agent=frontend_agent,
        # CrewAI >=0.40 requires this field
        expected_output=(
            "A single valid TSX file representing a Next.js page or component. "
            "The code must be wrapped in one markdown code block with language hint tsx."
        ),
    )

def make_backend_task(payload: dict) -> Task:
    """
    payload keys we rely on:
      - feature (str)
      - route (str) e.g., '/api/jobs'
      - notes (str) optional guidance
    """
    return Task(
        name=f"generate_backend_{payload.get('feature','unknown')}",
        description=(
            "Generate SQL to create/alter required tables IF NOT EXISTS, and a Next.js 14 route handler "
            "at the given route (e.g., /app/api/.../route.ts) using TypeScript. "
            "Use Supabase client/server as appropriate. "
            "Do not include explanations, ONLY the code."
            f"\nPayload: {payload}"
        ),
        agent=backend_agent,
        expected_output=(
            "Two outputs in one code block: first SQL (DDL/DML), then a Next.js route.ts (TypeScript). "
            "Wrap everything in a single markdown code block with language hint ts (not tsx)."
        ),
    )
