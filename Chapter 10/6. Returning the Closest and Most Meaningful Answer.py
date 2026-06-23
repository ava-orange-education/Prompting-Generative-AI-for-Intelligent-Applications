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

SIMILARITY_THRESHOLD = 0.59

def answer_query(query, stored_embeddings, answers):
    query_embedding = get_embedding(query)
    best_match = None
    best_score = -1
    
    for text, embedding in stored_embeddings.items():
        score = cosine_similarity(query_embedding, embedding)
        if score > best_score:
            best_score = score
            best_match = text
    
    if best_score >= SIMILARITY_THRESHOLD:
        return answers[best_match]
    else:
        return "I am not sure I understand. Could you rephrase your question?"

stored_embeddings = {
    "How do I reset my password?": get_embedding("How do I reset my password?"),
    "How can I apply for leave?": get_embedding("How can I apply for leave?"),
    "How do I raise an IT ticket?": get_embedding("How do I raise an IT ticket?")
}

answers = {
    "How do I reset my password?": 
        "You can reset your password using the Self-Service Portal or contact IT support.",
    "How can I apply for leave?": 
        "You can apply for leave through the HR portal under the Leave section.",
    "How do I raise an IT ticket?": 
        "You can raise an IT ticket using the ServiceNow portal."
}
query = "How do I log into my account?"
response = answer_query(query, stored_embeddings, answers)
print(response)