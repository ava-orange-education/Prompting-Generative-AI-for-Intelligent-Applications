import os
from openai import OpenAI
from dotenv import load_dotenv

# Load env from config.env in the same folder
load_dotenv(r'.\config.env')

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
)

def quick_answer(question):
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Answer briefly and clearly. If unsure, say you are not certain."},
        {"role": "user", "content": f"Question: {question}\nAnswer in two or three sentences."}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2,
        max_tokens=160
    )
    
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    q = input("Ask your question:\n")
    print("\nAnswer:\n")
    print(quick_answer(q))
