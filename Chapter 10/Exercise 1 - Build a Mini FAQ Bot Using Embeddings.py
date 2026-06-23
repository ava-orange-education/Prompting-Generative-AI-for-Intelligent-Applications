import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
SIMILARITY_THRESHOLD = 0.6

faqs = {
    "How do I reset my password?": "Go to the login page and click Forgot Password. Follow the instructions sent to your email.",
    "Where can I find my pay slip?": "Log in to the HR portal and navigate to Documents. Your pay slips are available under Salary.",
    "How do I apply for leave?": "Use the Leave Management section in the employee portal. Fill out the request form and submit it to your manager.",
    "How do I update my bank details?": "Go to Settings, select Payment Information, and update your bank account number. Save the changes."
}

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

def answer_user_query(query):
    user_embedding = get_embedding(query)
    best_question = None
    best_score = -1
    
    for question, embedding in faq_embeddings.items():
        score = cosine_similarity(user_embedding, embedding)
        if score > best_score:
            best_score = score
            best_question = question
    
    if best_score >= SIMILARITY_THRESHOLD:
        return f"Answer: {faqs[best_question]} (match score {best_score:.2f})"
    else:
        return (
            "I am not fully sure what you mean. "
            "Do you want help with password, bank details, holidays, or leave?"
        )


faq_embeddings = {}
for question in faqs.keys():
    faq_embeddings[question] = get_embedding(question)

print("Embeddings generated for all FAQ questions.")

print(answer_user_query("I forgot my login password"))
print()
print(answer_user_query("Where do I see my salary slip?"))
print()
print(answer_user_query("I want to take a day off"))
print()
print(answer_user_query("Issue in system"))

