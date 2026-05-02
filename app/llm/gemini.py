# import os
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI

# load_dotenv()


# def get_llm():
#     """
#     Initialize and return a ChatGoogleGenerativeAI LLM instance.
#     Properly configured for CrewAI compatibility.
#     """
#     api_key = os.getenv("GOOGLE_API_KEY")
#     if not api_key:
#         raise ValueError(
#             "GOOGLE_API_KEY environment variable is not set. "
#             "Please add: GOOGLE_API_KEY=<your-key> to your .env file"
#         )
    
#     # Initialize the Google Generative AI LLM
#     llm = ChatGoogleGenerativeAI(
#         model="gemini-1.5-flash",
#         temperature=0.2,
#         google_api_key=api_key,
#         convert_system_message_to_human=True,
#         max_output_tokens=1024,
#     )
    
#     return llm

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
        model="gemini/gemini-3-flash-preview",
        api_key=api_key,
        temperature=0.2
    )