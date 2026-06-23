
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


def find_best_match(query, stored_embeddings):
    query_embedding = get_embedding(query)
    best_match = None
    best_score = -1
    
    for text, embedding in stored_embeddings.items():
        score = cosine_similarity(query_embedding, embedding)
        if score > best_score:
            best_score = score
            best_match = text
    
    return best_match, best_score

stored_embeddings = {}
faqs = {
    "How do I reset my password?": "Go to settings and click Forgot Password.",
    "Where do I find my pay slip?": "Check the HR portal under Documents.",
    "How do I apply for leave?": "Use the Leave Request form in the system."
}

for question in faqs.keys():
    stored_embeddings[question] = get_embedding(question)

print(find_best_match('change password', stored_embeddings))