import os
from crewai import LLM

def get_llm():
    """Get a CrewAI-compatible LLM instance for Ollama Mistral."""
    
    return LLM(
        model="ollama/gemma4:31b-cloud",
        base_url="http://localhost:11434",
        temperature=0.2
    )
