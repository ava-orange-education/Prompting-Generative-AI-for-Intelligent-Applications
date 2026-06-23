from openai import OpenAI
import os
from dotenv import load_dotenv
import chromadb

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client_ai = OpenAI(api_key=api_key)

long_note= '''

Cell division is one of the most fundamental processes in biology. It is the mechanism by which a living cell divides to form new cells. Every living organism, from the simplest bacteria to complex human beings, depends on cell division for survival, growth, and reproduction. Without this process, life as we know it would not be possible.

At its core, cell division is the process by which a parent cell divides into two or more daughter cells. These daughter cells may be identical to the parent cell or different, depending on the type of division taking place. Cell division allows organisms to grow from a single cell into a fully developed body made up of trillions of cells. It also helps replace old, damaged, or dead cells, ensuring that tissues and organs continue to function properly.

There are two major types of cell division in multicellular organisms: mitosis and meiosis. Each serves a very different purpose and occurs in different parts of the body.

Mitosis is the type of cell division responsible for growth, repair, and maintenance. When you grow taller, heal a wound, or replace worn-out skin cells, mitosis is at work. In mitosis, a single parent cell divides to produce two daughter cells that are genetically identical to each other and to the original cell. This ensures that all body cells maintain the same genetic information. Mitosis is especially important in tissues that undergo constant wear and tear, such as the skin, blood, and lining of the digestive system.

The process of mitosis follows a series of well-defined stages. First, the cell prepares by copying its genetic material. Then, the chromosomes are carefully separated so that each new cell receives an exact copy. Finally, the cell splits into two independent cells. This precise control helps prevent errors and maintains stability within the body.

Meiosis, on the other hand, is a special type of cell division used to produce reproductive cells, such as sperm and eggs. Unlike mitosis, meiosis results in four daughter cells, each containing half the genetic material of the parent cell. These cells are not genetically identical. Instead, they carry unique combinations of genes. This variation is important because it contributes to genetic diversity, which helps populations adapt and survive over time.

Meiosis occurs in two stages of division. During this process, chromosomes pair up, exchange genetic material, and then separate. The final result is reproductive cells that are ready to combine during fertilization. When a sperm cell and an egg cell join, they restore the full set of genetic material, creating a new individual with traits inherited from both parents.

In summary, cell division is a vital biological process that supports life in many ways. Mitosis helps organisms grow, repair tissues, and maintain healthy cells, while meiosis enables sexual reproduction and genetic diversity. Together, these processes ensure continuity of life across generations. Understanding cell division provides a foundation for learning more advanced topics in biology, such as genetics, development, and evolution.

'''

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

overlapping_chunks = create_overlapping_chunks(long_note)

client = chromadb.Client()
collection = client.create_collection("subject_notes-chunking")

embeddings_response = client_ai.embeddings.create(
    model="text-embedding-3-small",
    input=overlapping_chunks
)

embeddings = [item.embedding for item in embeddings_response.data]

print("Embeddings created:", len(embeddings))


# Create or load your collection
collection = client.create_collection("subject_notes")

# Add chunks and embeddings
collection.add(
    ids=[f"c{i}" for i in range(len(overlapping_chunks))],
    documents=overlapping_chunks,
    embeddings=embeddings
)

print("All chunks stored successfully")

query = "What is the main idea behind cell division?"

query_embedding = client_ai.embeddings.create(
    model="text-embedding-3-small",
    input=query
).data[0].embedding

print("Query embedding created")

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3      # top 3 most relevant chunks
)

retrieved_chunks = results["documents"]

print("Retrieved chunks:")
for chunk in retrieved_chunks:
    print(chunk[:120], "...")

print("Scores:", results["distances"])

#print(results["documents"])

# Combine chunks into a single context block
all_chunks = []
for docs in results["documents"]:
    all_chunks.extend(docs)

context = "\n".join(all_chunks)

prompt = f"""
Use the notes below to answer the question.

Notes:
{context}

Question:
{query}

Write the answer in simple and clear words.
"""

response = client_ai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

answer = response.choices[0].message.content
print("Final answer:")
print(answer)




