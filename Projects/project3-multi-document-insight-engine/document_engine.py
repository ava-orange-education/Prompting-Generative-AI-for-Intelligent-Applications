# document_engine.py
# Core logic: multi-document chunking, embedding, metadata storage,
# filtered retrieval, source citation, cross-document comparison, and RAG

import os
from openai import OpenAI
from dotenv import load_dotenv
import chromadb

# Load environment variables
load_dotenv()

# --- Constants ---
EMBEDDING_MODEL = "text-embedding-3-small"
GENERATION_MODEL = "gpt-4o-mini"
CHUNK_SIZE = 200
CHUNK_OVERLAP = 40
TOP_K_RESULTS = 5       # Higher K for multi-document retrieval


def get_openai_client():
    """
    Create and return the OpenAI client on demand.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found. "
            "Please add it to your .env file."
        )
    return OpenAI(api_key=api_key)


def create_chunks(text, source_name, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Break text into overlapping chunks.
    Each chunk is tagged with its source document name and chunk number.
    """
    words = text.split()
    chunks = []
    start = 0
    chunk_number = 1

    while start < len(words):
        end = start + size
        chunk_text = " ".join(words[start:end])
        chunks.append({
            "text": chunk_text,
            "source": source_name,
            "chunk_number": chunk_number
        })
        start = end - overlap
        chunk_number += 1

    return chunks


def process_documents(documents):
    """
    Take a list of documents (each with 'name' and 'content'),
    chunk them, embed them, and store in ChromaDB with metadata.

    Parameters:
        documents: list of dicts with keys 'name' and 'content'

    Returns:
        collection: ChromaDB collection ready for querying
        stats: dict with processing statistics
    """
    # Chunk all documents
    all_chunks = []
    for doc in documents:
        doc_chunks = create_chunks(doc["content"], doc["name"])
        all_chunks.extend(doc_chunks)

    if len(all_chunks) == 0:
        raise ValueError("No content found in the uploaded documents.")

    # Generate embeddings
    texts = [c["text"] for c in all_chunks]
    response = get_openai_client().embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )
    embeddings = [item.embedding for item in response.data]

    # Store in ChromaDB with metadata
    chroma_client = chromadb.PersistentClient(path="./chroma_db")

    existing = [c.name for c in chroma_client.list_collections()]
    if "multi_doc_store" in existing:
        chroma_client.delete_collection("multi_doc_store")

    collection = chroma_client.create_collection(name="multi_doc_store")

    ids = [f"chunk_{i}" for i in range(len(all_chunks))]
    metadatas = [
        {
            "source": c["source"],
            "chunk_number": c["chunk_number"]
        }
        for c in all_chunks
    ]

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    # Gather stats
    stats = {
        "total_documents": len(documents),
        "total_chunks": len(all_chunks),
        "document_names": [doc["name"] for doc in documents]
    }

    return collection, stats


def retrieve_chunks(collection, query, source_filter=None, top_k=TOP_K_RESULTS):
    """
    Retrieve relevant chunks with optional metadata filtering.

    Parameters:
        collection: ChromaDB collection
        query: user question string
        source_filter: document name to filter by, or None for all
        top_k: number of results to return

    Returns:
        results: list of dicts with text, source, chunk_number, and distance
    """
    query_embedding = get_openai_client().embeddings.create(
        model=EMBEDDING_MODEL,
        input=query
    ).data[0].embedding

    # Build query arguments
    query_args = {
        "query_embeddings": [query_embedding],
        "n_results": top_k
    }

    # Add metadata filter if a specific document is selected
    if source_filter and source_filter != "All Documents":
        query_args["where"] = {"source": source_filter}

    raw_results = collection.query(**query_args)

    # Package results into a clean format
    results = []
    for i in range(len(raw_results["documents"][0])):
        results.append({
            "text": raw_results["documents"][0][i],
            "source": raw_results["metadatas"][0][i]["source"],
            "chunk_number": raw_results["metadatas"][0][i]["chunk_number"],
            "distance": round(raw_results["distances"][0][i], 4)
        })

    return results


def is_comparison_query(query):
    """
    Simple check to detect if the user is asking for a comparison
    across documents. Looks for common comparison keywords.
    """
    comparison_keywords = [
        "compare", "comparison", "difference", "differ",
        "contrast", "versus", "vs", "both documents",
        "across documents", "conflict", "overlap",
        "which documents", "all documents"
    ]
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in comparison_keywords)


def generate_answer(query, retrieved_results):
    """
    Use RAG to generate a grounded answer with source citations.
    """
    # Build context with source labels
    context_parts = []
    for r in retrieved_results:
        label = f"[{r['source']}, Chunk {r['chunk_number']}]"
        context_parts.append(f"{label}\n{r['text']}")

    context = "\n\n".join(context_parts)

    prompt = f"""You are a helpful document assistant.

A user has asked a question, and the following relevant sections have been retrieved from their uploaded documents. Each section is labeled with its source document name and chunk number.

Instructions:
- Answer only using the provided context. Do not guess or add information that is not present.
- For each key point in your answer, mention which document it came from using the format (Source: document name).
- If the context does not contain enough information, say so clearly.
- Keep your answer clear, organized, and easy to read.

Question:
{query}

Retrieved Context:
{context}

Please provide your answer now."""

    response = get_openai_client().chat.completions.create(
        model=GENERATION_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=800
    )

    return response.choices[0].message.content


def generate_comparison(query, retrieved_results):
    """
    Use RAG with a comparison-specific prompt that asks the model
    to compare information from different documents side by side.
    """
    # Build context with source labels
    context_parts = []
    for r in retrieved_results:
        label = f"[{r['source']}, Chunk {r['chunk_number']}]"
        context_parts.append(f"{label}\n{r['text']}")

    context = "\n\n".join(context_parts)

    # Identify unique sources in results
    sources = list(set(r["source"] for r in retrieved_results))
    source_list = ", ".join(sources)

    prompt = f"""You are a helpful document comparison assistant.

A user wants to compare information across multiple documents. The following relevant sections have been retrieved from these documents: {source_list}.

Each section is labeled with its source document name and chunk number.

Instructions:
- Compare the information from different documents side by side.
- Highlight similarities and differences clearly.
- For each point, mention which document it comes from using the format (Source: document name).
- If certain documents do not address a particular topic, note that clearly.
- Do not guess or add information that is not present in the context.
- Keep the comparison organized and easy to follow.

Question:
{query}

Retrieved Context:
{context}

Please provide your comparison now."""

    response = get_openai_client().chat.completions.create(
        model=GENERATION_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1000
    )

    return response.choices[0].message.content


def answer_query(collection, query, source_filter=None):
    """
    Full pipeline: retrieve relevant chunks, detect query type,
    and generate the appropriate response.

    Returns:
        answer: the generated response string
        retrieved_results: list of retrieved chunk details
        query_type: 'comparison' or 'standard'
    """
    if not query.strip():
        return "Please enter a question.", [], "standard"

    # Retrieve relevant chunks
    retrieved_results = retrieve_chunks(
        collection, query, source_filter=source_filter
    )

    if len(retrieved_results) == 0:
        return (
            "No relevant information was found for your question. "
            "Try rephrasing or selecting a different document filter."
        ), [], "standard"

    # Detect if this is a comparison query
    if is_comparison_query(query):
        answer = generate_comparison(query, retrieved_results)
        query_type = "comparison"
    else:
        answer = generate_answer(query, retrieved_results)
        query_type = "standard"

    return answer, retrieved_results, query_type
