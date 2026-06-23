from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client  = OpenAI(api_key=api_key)

ingredients = ["tomato", "rice", "potato"]
goal = "Cook a simple dish using available ingredients"

prompt = f"""
You are an AI chef. Your goal is: {goal}

Ingredients: {ingredients}

Think about what dish you can make.
Then choose the next actionable step.
Provide your reasoning and clearly mention next_step.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

print(response.choices[0].message.content)

next_step = "prepare tomato rice base"   # extracted from the model
print("Agent performs action:", next_step)

review_prompt = f"""
You suggested the step: {next_step}.
Did this step move you closer to the goal: {goal}?
Should you continue or stop?
Explain briefly and clearly say continue or stop.
"""

review = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": review_prompt}]
)

print("Review:", review.choices[0].message.content)


