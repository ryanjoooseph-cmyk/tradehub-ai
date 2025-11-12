from crewai import Agent, Task
from crewai.llm import LLM

llm = LLM(model="gpt-4o")

frontend_agent = Agent(
    role="Next.js frontend generator",
    goal="Generate Next.js pages/components for TradeHub.",
    backstory="Output ONLY code.",
    llm=llm,
)

backend_agent = Agent(
    role="Supabase/backend generator",
    goal="Generate SQL and API handlers for TradeHub.",
    backstory="Output ONLY code.",
    llm=llm,
)

def make_frontend_task(payload: dict) -> Task:
    return Task(
        name="generate_frontend",
        description=(
            "Generate a Next.js 14 app-router page at /jobs/new with a form. "
            "Use TypeScript and Tailwind. Fields come from payload. POST to /api/jobs.\n"
            f"Payload: {payload}"
        ),
        agent=frontend_agent,
        expected_output="```tsx\n// Next.js page code here\n```"
    )

def make_backend_task(payload: dict) -> Task:
    return Task(
        name="generate_backend",
        description=(
            "Generate SQL to create a jobs table (if not exists) and a Next.js route handler "
            "at /app/api/jobs/route.ts to insert into Supabase.\n"
            f"Payload: {payload}"
        ),
        agent=backend_agent,
        expected_output="```sql\n-- SQL here\n```\n```ts\n// route handler here\n```"
    )
