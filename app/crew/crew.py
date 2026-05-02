import os
from dotenv import load_dotenv
from crewai import Crew

from agents.job_analyzer import create_job_analyzer
from agents.matcher import create_matcher

from tasks.extract_tasks import create_extraction_task
from tasks.match_tasks import create_match_task

load_dotenv()


def run_pipeline(job_description, resume):
    # Create agents
    analyzer = create_job_analyzer()
    matcher = create_matcher()

    # Create tasks
    extraction_task = create_extraction_task(analyzer, job_description)
    match_task = create_match_task(matcher, resume, extraction_task)

    # Create crew
    crew = Crew(
        agents=[analyzer, matcher],
        tasks=[extraction_task, match_task],
        verbose=True
    )

    result = crew.kickoff()

    return result