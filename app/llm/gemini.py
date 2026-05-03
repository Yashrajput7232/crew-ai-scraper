import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    """Get a CrewAI-compatible LLM instance for Google Generative AI."""
    from crewai import LLM
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY environment variable is not set. "
            "Please add: GOOGLE_API_KEY=<your-key> to your .env file"
        )
    
    return LLM(
        # model="gemini/gemini-2.5",
        # model="gemini/gemma-3-27b",
        # model="gemini/gemma-4-31b",
        model="gemini/gemma-4-31b-it",
        api_key=api_key,
        temperature=0.2
    )