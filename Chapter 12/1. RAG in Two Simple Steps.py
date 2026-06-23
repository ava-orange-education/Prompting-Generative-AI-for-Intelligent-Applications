from openai import OpenAI
import os
from dotenv import load_dotenv
import chromadb

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client_ai = OpenAI(api_key=api_key)

# Create a client
client = chromadb.Client()

collection = client.create_collection(
    name="subject_notes")

collection.add(
    ids=["n1", "n2", "n3"],
    documents=[
        "Cell division is the process by which a parent cell divides into two or more daughter cells.",
        "Mitosis is a type of cell division that helps in growth and repair of tissues.",
        "Meiosis is a special type of cell division that produces reproductive cells with half the genetic material."
    ]
)

# Load your saved collection of notes
collection = client.get_collection("subject_notes")

# Your question
query = "What is the main idea behind cell division?"

# Retrieve the closest chunks
results = collection.query(
    query_texts=[query],
    n_results=3
)

print("Retrieved chunks:")
for doc in results["documents"]:
    print(doc)


# Combine retrieved text
retrieved_text = " ".join(results["documents"][0])

prompt = f"""
Use the notes below to answer the question.

Notes:
{retrieved_text}

Question:
{query}

Answer in simple words that a beginner can understand.
"""

response = client_ai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

print("Final answer:")
print(response.choices[0].message.content)
