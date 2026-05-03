import os
from dotenv import load_dotenv
from crewai import Crew

from agents.job_analyzer import create_job_analyzer
from agents.matcher import create_matcher
from agents.resume_writer import create_resume_writer
from agents.latex_compiler_agent import create_latex_compiler_agent

from tasks.extract_tasks import create_extraction_task
from tasks.match_tasks import create_match_task
from tasks.resume_tasks import create_resume_write_task, create_latex_compile_task

load_dotenv()


def run_pipeline(job_description, resume):
    # Agents
    analyzer = create_job_analyzer()
    matcher = create_matcher()
    resume_writer = create_resume_writer()
    latex_compiler = create_latex_compiler_agent()

    # Tasks
    extraction_task = create_extraction_task(analyzer, job_description)
    match_task = create_match_task(matcher, resume, extraction_task)
    resume_write_task = create_resume_write_task(
        agent=resume_writer,
        resume=resume,
        job_description=job_description,
        context_tasks=[extraction_task, match_task]  # gets evaluated job context
    )
    compile_task = create_latex_compile_task(
        agent=latex_compiler,
        resume_write_task=resume_write_task
    )

    # Crew
    crew = Crew(
        agents=[analyzer, matcher, resume_writer, latex_compiler],
        tasks=[extraction_task, match_task, resume_write_task, compile_task],
        verbose=True,
        max_rpm=10  # Prevents hitting the Gemini free-tier rate limits
    )

    result = crew.kickoff()
    return result