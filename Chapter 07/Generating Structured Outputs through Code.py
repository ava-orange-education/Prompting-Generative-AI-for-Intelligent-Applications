import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv('.\config.env')

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
)

text = input("Paste the text to summarize:\n")

prompt = f"""
Summarize the text below.
Return a JSON object with keys: "title", "bullets", "tone".
- "title" is a five word heading.
- "bullets" is a list of three short points.
- "tone" is one word that best fits the style.

Text:
{text}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.3,
    max_tokens=250
)

raw = response.choices[0].message.content.strip()
print("\nRaw model output:\n", raw)

# Try to parse safely
try:
    data = json.loads(raw)
    print("\nParsed result:")
    print("Title:", data.get("title"))
    print("Points:", *data.get("bullets", []), sep="\n- ")
    print("Tone:", data.get("tone"))
except json.JSONDecodeError:
    print("\nCould not parse JSON. You may refine the prompt or clean the text before parsing.")
