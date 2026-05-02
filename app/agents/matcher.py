from crewai import Agent
from llm.gemini import get_llm

def create_matcher():
    llm = get_llm()
    
    return Agent(
        role="Resume Matcher",
        goal="Strictly evaluate job fit and assign a score",
        backstory="A strict technical recruiter who never inflates scores",
        llm=llm,
        verbose=True
    )