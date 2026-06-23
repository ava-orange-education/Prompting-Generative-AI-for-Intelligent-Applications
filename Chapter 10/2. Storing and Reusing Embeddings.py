from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

faq_embeddings = {}
faqs = {
    "How do I reset my password?": "Go to settings and click Forgot Password.",
    "Where do I find my pay slip?": "Check the HR portal under Documents.",
    "How do I apply for leave?": "Use the Leave Request form in the system."
}
client = OpenAI(api_key=api_key)

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

for question in faqs.keys():
    faq_embeddings[question] = get_embedding(question)

print(faq_embeddings)
