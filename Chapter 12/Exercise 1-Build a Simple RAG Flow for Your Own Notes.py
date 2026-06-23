from openai import OpenAI
import os
from dotenv import load_dotenv
import chromadb

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client_ai = OpenAI(api_key=api_key)

notes = """
Cell division is the process where a parent cell divides into two daughter cells.
This is used for growth, repair, and reproduction.
Mitosis creates identical cells. Meiosis creates cells with half the chromosomes.
"""

def create_overlapping_chunks(text, size=50, overlap=10):
    words = text.split()
    chunks = []
    start = 0
    
    while start < len(words):
        end = start + size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap
    
    return chunks


chunks = create_overlapping_chunks(notes, size=40, overlap=10)
print(chunks)

emb_response = client_ai.embeddings.create(
    model="text-embedding-3-small",
    input=chunks
)
embeddings = [e.embedding for e in emb_response.data]
client = chromadb.Client()
collection = client.create_collection("practice_notes")
collection.add(
    ids=[f"id_{i}" for i in range(len(chunks))],
    documents=chunks,
    embeddings=embeddings
)
query = "Why does cell division happen?"
q_emb = client_ai.embeddings.create(
    model="text-embedding-3-small",
    input=query
).data[0].embedding

results = collection.query(
    query_embeddings=[q_emb],
    n_results=3
)
retrieved_chunks = results["documents"]

all_chunks = []
for docs in results["documents"]:
    all_chunks.extend(docs)

context = "\n".join(all_chunks)

prompt = f"""
Use the notes to answer the question.

Notes:
{context}

Question:
{query}

Explain in simple words.
"""

response = client_ai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

print(response.choices[0].message.content)
