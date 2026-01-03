import json
from crewai import Agent, Task, Crew
from crewai.llm import LLM

llm = LLM(model="gpt-4o-mini")

onboarding = Agent(
    role="Onboarding specialist",
    goal="Collect tradie details (name, abn, trade_type, service_area, phone, email).",
    backstory="You onboard WA tradies for TradeHub and must mark MISSING fields.",
    llm=llm,
)

job_helper = Agent(
    role="Job helper",
    goal="Guide homeowners to post jobs with enough detail for tradies to quote.",
    backstory="You know job_title, description, location, budget, photos.",
    llm=llm,
)

dispute_agent = Agent(
    role="Dispute resolver",
    goal="Summarise both sides and propose a fair resolution without releasing funds.",
    backstory="You follow TradeHub dispute rules.",
    llm=llm,
)

def make_onboard_task(payload: dict | None = None) -> Task:
    extra = f"Use this data if present: {json.dumps(payload)}. " if payload else ""
    return Task(
        name="onboard_tradie",
        description=(
            extra +
            "Collect tradie profile for TradeHub. Fields: name, abn, trade_type, service_area, phone, email. "
            "If a field is not provided, set it to 'MISSING'. Return ONLY JSON."
        ),
        agent=onboarding,
        expected_output='{"name": "...", "abn": "...", "trade_type": "...", "service_area": "...", "phone": "...", "email": "..."}',
    )

def make_job_task(payload: dict | None = None) -> Task:
    extra = f"Job context: {json.dumps(payload)}. " if payload else ""
    return Task(
        name="create_job",
        description=(
            extra +
            "Explain to a homeowner how to post a job on TradeHub. "
            "Fields: job_title, description, location, budget, photos. Make it 5 numbered steps."
        ),
        agent=job_helper,
        expected_output="1. ... 2. ... 3. ... 4. ... 5. ...",
    )

def make_dispute_task(payload: dict | None = None) -> Task:
    extra = f"Dispute context: {json.dumps(payload)}. " if payload else ""
    return Task(
        name="resolve_dispute",
        description=(
            extra +
            "Resolve a dispute between a customer and a tradie. "
            "Summarise customer position, tradie position, evidence, and propose a fair resolution. "
            "Do NOT say you released funds; only recommend."
        ),
        agent=dispute_agent,
        expected_output="Sections: Customer position; Tradie position; Evidence; Proposed resolution.",
    )

crew = Crew(
    agents=[onboarding, job_helper, dispute_agent],
    tasks=[make_onboard_task(), make_job_task(), make_dispute_task()],
)

if __name__ == "__main__":
    results = crew.kickoff()
    for r in results:
        print(r)
