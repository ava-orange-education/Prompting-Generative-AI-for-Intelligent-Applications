# support_assistant.py
# Core logic: load FAQ docs, chunk, embed, store, retrieve with confidence, and RAG response

import os
import glob
from openai import OpenAI
from dotenv import load_dotenv
import chromadb

# Load environment variables
load_dotenv()

# --- Constants ---
EMBEDDING_MODEL = "text-embedding-3-small"
GENERATION_MODEL = "gpt-4o-mini"
CHUNK_SIZE = 150        # Words per chunk (FAQ entries are shorter than resumes)
CHUNK_OVERLAP = 30      # Overlapping words between chunks
TOP_K_RESULTS = 3       # Number of chunks to retrieve
CONFIDENCE_HIGH = 0.8   # Distance below this = high confidence
CONFIDENCE_LOW = 1.3    # Distance above this = low confidence (suggest escalation)


def get_openai_client():
    """
    Create and return the OpenAI client.
    The client is created when needed, not at import time.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found. "
            "Please add it to your .env file."
        )
    return OpenAI(api_key=api_key)


def load_knowledge_base(folder_path="knowledge_base"):
    """
    Load all .txt files from the knowledge base folder.
    Returns a list of dictionaries with filename and content.
    """
    documents = []
    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))

    if len(txt_files) == 0:
        raise FileNotFoundError(
            f"No .txt files found in '{folder_path}/' folder. "
            "Please add FAQ documents."
        )

    for filepath in txt_files:
        filename = os.path.basename(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if content:
            documents.append({
                "filename": filename,
                "content": content
            })

    return documents


def create_chunks(text, source_name, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Break text into smaller overlapping chunks.
    Each chunk is tagged with its source file name.
    """
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + size
        chunk = " ".join(words[start:end])
        chunks.append({
            "text": chunk,
            "source": source_name
        })
        start = end - overlap

    return chunks


def chunk_all_documents(documents):
    """
    Chunk all documents from the knowledge base.
    Returns a flat list of chunk dictionaries.
    """
    all_chunks = []
    for doc in documents:
        doc_chunks = create_chunks(doc["content"], doc["filename"])
        all_chunks.extend(doc_chunks)
    return all_chunks


def generate_embeddings(texts):
    """
    Convert a list of text strings into embeddings using OpenAI.
    """
    response = get_openai_client().embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )
    return [item.embedding for item in response.data]


def build_vector_store(chunks):
    """
    Store all chunks in ChromaDB with source metadata.
    Returns the collection for querying.
    """
    chroma_client = chromadb.PersistentClient(path="./chroma_db")

    # Fresh start each time
    existing = [c.name for c in chroma_client.list_collections()]
    if "support_kb" in existing:
        chroma_client.delete_collection("support_kb")

    collection = chroma_client.create_collection(name="support_kb")

    # Prepare data for insertion
    texts = [c["text"] for c in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source": c["source"]} for c in chunks]

    # Generate embeddings
    embeddings = generate_embeddings(texts)

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return collection


def retrieve_with_confidence(collection, query, top_k=TOP_K_RESULTS):
    """
    Retrieve relevant chunks and calculate a confidence level
    based on the similarity distance.

    Returns matched chunks, distances, sources, and confidence level.
    """
    query_embedding = get_openai_client().embeddings.create(
        model=EMBEDDING_MODEL,
        input=query
    ).data[0].embedding

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    matched_chunks = results["documents"][0]
    distances = results["distances"][0]
    sources = [m["source"] for m in results["metadatas"][0]]

    # Determine confidence based on the best (lowest) distance
    best_distance = distances[0] if distances else 999

    if best_distance <= CONFIDENCE_HIGH:
        confidence = "High"
    elif best_distance <= CONFIDENCE_LOW:
        confidence = "Medium"
    else:
        confidence = "Low"

    return matched_chunks, distances, sources, confidence


def generate_support_response(query, matched_chunks, sources, confidence):
    """
    Use RAG to generate a polite, customer-friendly response.
    If confidence is low, the response includes an escalation notice.
    """
    context = "\n\n".join(matched_chunks)
    source_list = ", ".join(set(sources))

    # Adjust instructions based on confidence
    if confidence == "Low":
        confidence_instruction = (
            "The retrieved information may not fully address the customer's question. "
            "Provide the best answer you can from the context, but clearly mention "
            "at the end that the customer may want to contact a human support agent "
            "for more detailed assistance."
        )
    else:
        confidence_instruction = (
            "The retrieved information is relevant. Provide a clear and "
            "complete answer based on the context."
        )

    prompt = f"""You are a friendly and professional customer support assistant.

A customer has asked the following question:
"{query}"

Here is the relevant information from the knowledge base:
{context}

Instructions:
- Answer in a warm, polite, and helpful tone.
- Keep the response clear and easy to understand.
- Only use information from the provided context. Do not guess or make up details.
- If the context does not contain enough information to answer fully, say so honestly.
- {confidence_instruction}

Please provide your response now."""

    response = get_openai_client().chat.completions.create(
        model=GENERATION_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content


def answer_query(collection, query):
    """
    Full pipeline: retrieve relevant chunks with confidence,
    then generate a customer-friendly response.
    Returns the response, confidence level, and sources.
    """
    if not query.strip():
        return "Please enter a question.", "Low", []

    # Retrieve with confidence scoring
    matched_chunks, distances, sources, confidence = retrieve_with_confidence(
        collection, query
    )

    # Generate response using RAG
    response = generate_support_response(
        query, matched_chunks, sources, confidence
    )

    return response, confidence, sources
