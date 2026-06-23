import os
from openai import OpenAI, APIError
from dotenv import load_dotenv

load_dotenv('.\config.env')

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
)

try:
    response = client.chat.completions.create(
        model="gpt-4o-err",
        messages=[{"role": "user", "content": "Write a haiku about patience."}],
        timeout=10  # sets a 10-second limit for the response
    )
    print(response.choices[0].message.content)
    
except APIError as e:
    print("The API encountered an issue:", e)
    
except TimeoutError:
    print("The request took too long. Please try again later.")
    
except Exception as e:
    print("An unexpected error occurred:", e)
