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

previous_questions = [
    "My password is not working",
    "Cannot access my salary information",
    "Need to request time off for next week",
    "How to change payment account details",
    "System is running very slow",
    "When will I receive my bonus payment?"
]

previous_embeddings = {}
for question in previous_questions:
    previous_embeddings[question] = get_embedding(question)

def detect_similar_question(new_question, similarity_threshold=0.6):
    new_embedding = get_embedding(new_question)
    similar_found = []
    
    for question, embedding in previous_embeddings.items():
        score = cosine_similarity(new_embedding, embedding)
        if score >= similarity_threshold:
            similar_found.append((question, score))
    
    if similar_found:
        result = "Similar questions found:\n"
        for question, score in similar_found:
            result += f"  - '{question}' (similarity: {score:.2f})\n"
        return result
    else:
        return "This appears to be a new unique question."


print(detect_similar_question("I forgot my password and need help"))
print()
print(detect_similar_question("Where is my monthly payslip?"))
print()
print(detect_similar_question("What is the office wifi password?"))
print()
print(detect_similar_question("My login credentials are not working"))
