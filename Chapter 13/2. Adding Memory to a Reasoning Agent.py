from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client  = OpenAI(api_key=api_key)

agent_memory = {
    "ingredients": ["tomato", "rice", "potato"],
    "completed_steps": [],
    "user_preferences": ["mild spice"],
    "notes": []
}
agent_memory["completed_steps"].append("prepared tomato base") #run once with empty completed_steps list and once with ["prepared tomato base"] 
agent_memory["notes"].append("Keep spice mild")


goal = "Cook a simple dish using available ingredients"

prompt = f"""
You are an AI chef. Your goal is: {goal}

Here is your current memory:
{agent_memory}

Based on the memory, decide the next best action.
Avoid repeating completed steps.
Clearly state your reasoning and the next_step.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

print(response.choices[0].message.content)

next_step = "prepare tomato rice base"
agent_memory["completed_steps"].append(next_step)

review_prompt = f"""
You completed the step: {next_step}.
Here is your memory so far: {agent_memory}

Does this step help you move closer to the goal?
Should you continue or stop?
"""

review = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": review_prompt}]
)

print('--------------------------------------')
print(review.choices[0].message.content)
