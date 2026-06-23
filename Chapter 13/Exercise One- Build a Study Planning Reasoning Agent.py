from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client  = OpenAI(api_key=api_key)

goal = "Prepare for final exam"

syllabus = [
    "Introduction",
    "Core Concepts",
    "Examples",
    "Practice Questions",
    "Revision"
]

memory = {
    "completed": ["Core Concepts"],
    "notes": []
}


prompt = f"""
You are a study planning AI.

Goal: {goal}
Syllabus: {syllabus}
Completed so far: {memory["completed"]}

Think step by step.

Choose the next chapter to study.
Do not repeat completed chapters.
Explain briefly why you chose it.
Clearly mention next_step.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

output = response.choices[0].message.content
print(output)
