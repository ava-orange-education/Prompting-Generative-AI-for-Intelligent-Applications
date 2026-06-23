import os
from openai import OpenAI
from dotenv import load_dotenv

# Load env from config.env in the same folder
load_dotenv(r'.\config.env')

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
)

def summarize_article(content):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant that writes short, factual summaries."},
            {"role": "user", "content": f"Summarize the following article in three clear bullet points:\n\n{content}"}
        ],
        temperature=0.3,
        max_tokens=200
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    text = input("Paste the article you want to summarize:\n")
    
    try:
        summary = summarize_article(text)
        print("\nSummary:\n")
        print(summary)
    except Exception as e:
        print("\nSomething went wrong. Please check your connection or API key.\n")
        print("Error details:", e)
