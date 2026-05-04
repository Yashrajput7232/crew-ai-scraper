import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    """Get the configured LLM based on LLM_PROVIDER environment variable."""
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    if provider == "ollama" or provider == "mistral":
        from .mistral import get_llm as get_ollama_llm
        return get_ollama_llm()
    else:
        from .gemini import get_llm as get_gemini_llm
        return get_gemini_llm()