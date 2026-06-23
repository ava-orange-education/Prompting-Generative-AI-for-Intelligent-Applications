import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv('.\config.env')

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
)

text = input("Enter the paragraph you want to summarize:\n")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are an assistant that summarizes text clearly."},
        {"role": "user", "content": f"Summarize this paragraph in three bullet points:\n\n{text}"}
    ]
)

print("\nSummary:\n")
print(response.choices[0].message.content.strip())
