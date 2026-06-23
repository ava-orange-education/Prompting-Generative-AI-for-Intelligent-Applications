from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client  = OpenAI(api_key=api_key)

preferences = {
    "city": "Jaipur",
    "budget": "medium",
    "interest": "culture",
    "duration": "2 days"
}

memory = {
    "planned": [],
    "notes": []
}


prompt = f"""
You are a travel planning AI.

Preferences: {preferences}
Already planned: {memory["planned"]}

Think step by step.

Decide what to plan next.
Explain your reasoning.
Clearly mention next_step.
"""
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

output = response.choices[0].message.content
print(output)
