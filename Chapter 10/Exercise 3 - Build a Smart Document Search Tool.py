import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

documents = {
    "Company Leave Policy": "Employees are entitled to 20 days of paid leave per year. Leave requests must be submitted at least two weeks in advance. Emergency leave can be approved by your manager on short notice.",
    
    "Health Insurance Guide": "The company provides comprehensive health insurance coverage for all full-time employees. Coverage includes hospitalization, outpatient care, and annual health checkups. Dependents can be added for an additional premium.",
    
    "Remote Work Guidelines": "Employees may work remotely up to three days per week with manager approval. Remote workers must be available during core hours from 10 AM to 4 PM. All remote work must be logged in the attendance system.",
    
    "Performance Review Process": "Performance reviews are conducted twice a year in January and July. Employees receive feedback on goals, competencies, and development areas. Reviews are used to determine promotions and salary adjustments.",
    
    "Expense Reimbursement Policy": "Business expenses must be submitted within 30 days with valid receipts. Approved categories include travel, meals, accommodation, and client entertainment. All expenses require manager approval before reimbursement."
}

document_embeddings = {}
for title, content in documents.items():
    full_text = f"{title}: {content}"
    document_embeddings[title] = get_embedding(full_text)

print("Embeddings generated for all documents.")

def search_documents(query, top_n=3):
    query_embedding = get_embedding(query)
    results = []
    
    for title, embedding in document_embeddings.items():
        score = cosine_similarity(query_embedding, embedding)
        results.append((title, score))
    
    results.sort(key=lambda x: x[1], reverse=True)
    
    print(f"Top {top_n} relevant documents for: '{query}'\n")
    for i, (title, score) in enumerate(results[:top_n], 1):
        print(f"{i}. {title}")
        print(f"   Relevance score: {score:.2f}")
        print(f"   Content: {documents[title][:100]}...")
        print()

def smart_document_search(query, relevance_threshold=0.5):
    query_embedding = get_embedding(query)
    results = []
    
    for title, embedding in document_embeddings.items():
        score = cosine_similarity(query_embedding, embedding)
        if score >= relevance_threshold:
            results.append((title, score))
    
    if results:
        results.sort(key=lambda x: x[1], reverse=True)
        print(f"Found {len(results)} relevant document(s) for: '{query}'\n")
        for title, score in results:
            print(f"- {title} (relevance: {score:.2f})")
            print(f"  {documents[title]}\n")
    else:
        print(f"No relevant documents found for: '{query}'")
        print("Try rephrasing your question or check the document library.")

search_documents("I want to work from home twice a week")
print("-" * 60)
print()

search_documents("How many vacation days do I get?")
print("-" * 60)
print()

search_documents("I need to claim money for a business trip")
print("-" * 60)
print()

search_documents("When will my manager review my performance?")

# Test the smart search
smart_document_search("How do I get medical coverage for my family?")


