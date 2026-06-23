import os
from openai import OpenAI
from dotenv import load_dotenv

# Load env from config.env in the same folder
load_dotenv(r'.\config.env')

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
)


def rewrite_text(text, tone):
    prompt = f"Rewrite the following text in a {tone} tone:\n\n{text}"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional writing assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=250
    )
    
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    text = input("Enter the text you want to rewrite:\n")
    tone = input("Choose tone (formal, casual, persuasive, concise):\n")
    
    print("\nRewritten text:\n")
    print(rewrite_text(text, tone))
