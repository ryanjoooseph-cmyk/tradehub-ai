from crewai import Agent, Task
from crewai.llm import LLM

llm = LLM(model="gpt-4o-mini")

# simple agents so dispatcher doesn't crash
onboarding = Agent(
    role="Onboarding agent",
    goal="Turn a tradie payload into a structured onboarding summary.",
    backstory="You help TradeHub onboard tradies.",
    llm=llm,
)

job_helper = Agent(
    role="Job creation agent",
    goal="Turn a job request into a clean job posting.",
    backstory="You help homeowners post jobs.",
    llm=llm,
)

dispute_agent = Agent(
    role="Dispute agent",
    goal="Summarize customer vs tradie disputes.",
    backstory="You help resolve disputes.",
    llm=llm,
)

def make_onboard_task(payload: dict) -> Task:
    return Task(
        name="onboard_tradie",
        description=f"Create an onboarding summary for this tradie:\n{payload}",
        agent=onboarding,
        expected_output="A JSON-like onboarding summary."
    )

def make_job_task(payload: dict) -> Task:
    return Task(
        name="create_job",
        description=f"Create a job posting from this payload:\n{payload}",
        agent=job_helper,
        expected_output="A job posting structure."
    )

def make_dispute_task(payload: dict) -> Task:
    return Task(
        name="resolve_dispute",
        description=f"Summarize and propose resolution for this dispute:\n{payload}",
        agent=dispute_agent,
        expected_output="A dispute summary and resolution."
    )
