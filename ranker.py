from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_resume_score(resume_text, job_description):
    prompt = f"""
You are an expert resume evaluator. Given the following resume and job description, evaluate the match.

Resume:
{resume_text}

Job Description:
{job_description}

Return:
1. A match score out of 100
2. Missing skills or experiences
3. Suggestions to improve the resume
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )

    return response.choices[0].message.content