# resume_analyzer.py
# Core logic: chunking, embedding, vector storage, retrieval, and RAG evaluation

import os
from openai import OpenAI
from dotenv import load_dotenv
import chromadb

from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# --- Constants ---
EMBEDDING_MODEL = "text-embedding-3-small"
GENERATION_MODEL = "gpt-4o-mini"
CHUNK_SIZE = 200        # Number of words per chunk
CHUNK_OVERLAP = 40      # Number of overlapping words between chunks
TOP_K_RESULTS = 3       # Number of chunks to retrieve


def get_openai_client():
    """
    Create and return the OpenAI client.
    The client is created when needed, not at import time.
    This avoids errors when the module is first loaded.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found. "
            "Please add it to your .env file."
        )
    return OpenAI(api_key=api_key)


def create_chunks(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Break a long text into smaller overlapping chunks.
    Each chunk contains roughly 'size' words.
    Overlap ensures no important idea is lost between chunks.
    """
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap

    return chunks


def generate_embeddings(texts):
    """
    Convert a list of text strings into embeddings using OpenAI.
    Returns a list of embedding vectors.
    """
    response = get_openai_client().embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )
    embeddings = [item.embedding for item in response.data]
    return embeddings


def store_in_vector_db(chunks, embeddings):
    """
    Store chunks and their embeddings in a ChromaDB collection.
    Returns the collection for later querying.
    """
    chroma_client = chromadb.PersistentClient(path="./chroma_db")

    # Delete existing collection if it exists (fresh start each time)
    existing = [c.name for c in chroma_client.list_collections()]
    if "resume_chunks" in existing:
        chroma_client.delete_collection("resume_chunks")

    collection = chroma_client.create_collection(name="resume_chunks")

    # Create unique IDs for each chunk
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

    return collection


def retrieve_relevant_chunks(collection, job_description, top_k=TOP_K_RESULTS):
    """
    Convert the job description into an embedding and retrieve
    the most relevant resume chunks from the vector database.
    """
    query_embedding = get_openai_client().embeddings.create(
        model=EMBEDDING_MODEL,
        input=job_description
    ).data[0].embedding

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    # Return the matched document texts and their distances
    matched_chunks = results["documents"][0]
    distances = results["distances"][0]

    return matched_chunks, distances


def generate_evaluation(job_description, matched_chunks):
    """
    Use RAG to generate a structured evaluation report.
    The model receives the job description and the most relevant
    resume sections, then produces a clear analysis.
    """
    context = "\n\n".join(matched_chunks)

    prompt = f"""You are a professional HR assistant that evaluates resumes.

You have been given a job description and the most relevant sections from a candidate's resume.

Your task is to generate a structured evaluation report with the following sections:

1. Match Summary: A brief paragraph explaining how well the resume matches the job description overall.

2. Strength Areas: List the specific skills, experiences, or qualifications from the resume that align well with the job requirements.

3. Skill Gaps: List the requirements from the job description that are not clearly addressed in the resume.

4. Improvement Suggestions: Provide helpful and constructive suggestions for the candidate to strengthen their application.

Be fair, balanced, and specific in your analysis. Do not guess or make up information that is not present in the resume sections provided.

Job Description:
{job_description}

Relevant Resume Sections:
{context}

Please provide the evaluation report now."""

    response = get_openai_client().chat.completions.create(
        model=GENERATION_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1000
    )

    return response.choices[0].message.content


def analyze_resume(resume_text, job_description):
    """
    Full pipeline: chunk the resume, embed it, store it,
    retrieve relevant sections, and generate an evaluation.
    Returns the evaluation report as a string.
    """
    # Step 1: Chunk the resume
    chunks = create_chunks(resume_text)

    if len(chunks) == 0:
        return "The resume appears to be empty. Please upload a valid resume."

    # Step 2: Generate embeddings for each chunk
    embeddings = generate_embeddings(chunks)

    # Step 3: Store in vector database
    collection = store_in_vector_db(chunks, embeddings)

    # Step 4: Retrieve the most relevant chunks
    matched_chunks, distances = retrieve_relevant_chunks(
        collection, job_description
    )

    # Step 5: Generate evaluation using RAG
    report = generate_evaluation(job_description, matched_chunks)

    return report
