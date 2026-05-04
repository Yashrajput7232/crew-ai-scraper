from crewai import Agent
from llm import get_llm

def create_job_analyzer():
    llm = get_llm()
    
    return Agent(
        role="Job Analyzer",
        goal="Extract structured requirements from job descriptions",
        backstory="Expert recruiter who extracts key skills and requirements precisely",
        llm=llm,
        verbose=True
    )