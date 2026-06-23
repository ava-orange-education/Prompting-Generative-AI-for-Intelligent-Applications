from openai import OpenAI
import os
from dotenv import load_dotenv
import chromadb

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client_ai = OpenAI(api_key=api_key)

faqs = [
    "Attendance requirement is seventy five percent.",
    "Assignments must be submitted before the due date.",
    "The final exam covers chapters one to eight.",
    "Project submission carries twenty five percent weightage.",
    "Class tests will be held twice in the semester."
]

faq_embeddings = client_ai.embeddings.create(
    model="text-embedding-3-small",
    input=faqs
)
faq_vectors = [item.embedding for item in faq_embeddings.data]

client = chromadb.Client()
faq_collection = client.create_collection("course_faqs")

faq_collection.add(
    ids=[f"faq_{i}" for i in range(len(faqs))],
    documents=faqs,
    embeddings=faq_vectors
)

question = "How much attendance do I need?"
q_emb = client_ai.embeddings.create(
    model="text-embedding-3-small",
    input=question
).data[0].embedding

results = faq_collection.query(
    query_embeddings=[q_emb],
    n_results=1
)

match = results["documents"][0]
print("Closest match:", match)

prompt = f"""
Here is the relevant course information:

{match}

Use it to answer the question:
{question}

Explain it in a clear and friendly manner.
"""

response = client_ai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

print(response.choices[0].message.content)
