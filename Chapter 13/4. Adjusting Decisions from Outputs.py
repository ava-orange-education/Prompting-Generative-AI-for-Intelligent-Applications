from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client  = OpenAI(api_key=api_key)

goal = "plan a weekend trip to Darjeleing"
steps = [
    "find quiet gardens and temples",
    "search for affordable guesthouses",
    "build a one-day itinerary"
]

for next_step in steps:
    review_prompt = f"""
    You suggested the step: {next_step}.
    Did this step move you closer to the goal: {goal}?
    Should you continue or stop?
    Explain briefly and clearly say continue or stop.
    """

    print("[Think]  Goal:", goal)
    print("[Think]  Current step:", next_step)

    review = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": review_prompt}]
    )

    print("[Act]    Sending step to model for review...")
    print("[Review]", review.choices[0].message.content)
    print()
