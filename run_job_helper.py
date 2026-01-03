from crewai import Crew
from crew_test import job_helper, job_task

if __name__ == "__main__":
    crew = Crew(agents=[job_helper], tasks=[job_task])
    results = crew.kickoff()
    for r in results:
        print(r)
