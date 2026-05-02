from crewai import Task

def create_match_task(agent, resume, extraction_task):
    return Task(
        description=f"""
        You are a STRICT evaluator.

        Resume:
        {resume}

        Based on the extracted job requirements from previous task:

        Output ONLY JSON:
        {{
          "score": int,
          "matching_skills": [],
          "missing_skills": [],
          "reason": ""
        }}

        Rules:
        - Do NOT inflate scores
        - Penalize missing core skills heavily
        - Be consistent
        """,
        expected_output="Structured JSON with score, matching_skills, missing_skills, and reason fields",
        agent=agent,
        context=[extraction_task]
    )