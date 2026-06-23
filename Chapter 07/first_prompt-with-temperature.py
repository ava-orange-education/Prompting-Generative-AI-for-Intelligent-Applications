import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv('.\config.env')

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
)

response = client.chat.completions.create(
    model='gpt-4o-mini',  
    messages=[
        {"role": "user", "content": "Write a short message about learning Python."}
    ],
    temperature=0.5,
    max_tokens=150

)

print(response)
