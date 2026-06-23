import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv('.\config.env')

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
)



def summarize(text):
    prompt = f"Summarize the text in three short bullet points.\n\nText:\n{text}"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You write crisp and faithful summaries."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=180
    )
    
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    content = input("Paste the text to summarize:\n")
    print("\nSummary:\n")
    print(summarize(content))
