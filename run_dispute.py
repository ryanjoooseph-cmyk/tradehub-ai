from crewai import Crew
from crew_test import dispute_agent, dispute_task

if __name__ == "__main__":
    crew = Crew(agents=[dispute_agent], tasks=[dispute_task])
    results = crew.kickoff()
    for r in results:
        print(r)
