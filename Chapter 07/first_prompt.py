import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv('.\config.env')

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
)

response = client.chat.completions.create(
    model="gpt-4o-mini",  
    messages=[
        {"role": "user", "content": "Write a two-line motivational quote about learning AI."}
    ]
)

print(response.choices[0].message.content)
