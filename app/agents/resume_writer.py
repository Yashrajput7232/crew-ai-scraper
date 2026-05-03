from crewai import Agent
from llm.gemini import get_llm


def create_resume_writer():
    llm = get_llm()

    return Agent(
        role="Expert Resume Writer and ATS Strategist",
        goal=(
            "Rewrite the candidate's resume tailored to the job description. "
            "Output ONLY a complete, compilable LaTeX document. No explanation. No markdown."
        ),
        backstory=(
            "You are a senior resume strategist with 15 years of experience. "
            "You know ATS systems, recruiter psychology, and LaTeX inside out."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )