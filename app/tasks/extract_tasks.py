from crewai import Task

def create_extraction_task(agent, job_description):
    return Task(
        description=f"""
        Extract structured information from this job description:

        {job_description}

        Output ONLY JSON:
        {{
          "required_skills": [],
          "good_to_have_skills": [],
          "experience_level": ""
        }}
        """,
        expected_output="Structured JSON with required_skills, good_to_have_skills, and experience_level",
        agent=agent
    )