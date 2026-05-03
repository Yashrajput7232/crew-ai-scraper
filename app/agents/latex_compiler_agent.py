from crewai import Agent
from llm.gemini import get_llm
from services.latex_compiler import compile_latex_to_pdf


def create_latex_compiler_agent():
    llm = get_llm()

    return Agent(
        role="LaTeX Compilation and Error Recovery Specialist",
        goal=(
            "Compile the LaTeX resume to PDF. "
            "If it fails, read the error log, fix only the broken part, and retry."
        ),
        backstory=(
            "You are a LaTeX expert who reads pdflatex error logs instantly "
            "and fixes the exact broken line. You retry until the PDF compiles."
        ),
        tools=[compile_latex_to_pdf],
        verbose=True,
        allow_delegation=False,
        llm=llm
    )