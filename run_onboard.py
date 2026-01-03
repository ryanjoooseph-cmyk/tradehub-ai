from crewai import Crew
from crew_test import onboarding, onboard_task

if __name__ == "__main__":
    crew = Crew(agents=[onboarding], tasks=[onboard_task])
    results = crew.kickoff()
    for r in results:
        print(r)
