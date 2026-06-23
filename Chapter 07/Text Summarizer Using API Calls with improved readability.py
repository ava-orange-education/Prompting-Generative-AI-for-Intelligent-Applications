import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

# Load env from config.env in the same folder
load_dotenv(r'.\config.env')

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
)


def chunk_text(text, size=200):
    for i in range(0, len(text), size):
        yield text[i:i+size]

def strip_code_fences(s: str) -> str:
    # Remove ```json ... ``` or ``` ... ``` fences if present
    return re.sub(r"^```(?:json)?\s*|\s*```$", "", s.strip(), flags=re.IGNORECASE)

def safe_json_loads(s: str):
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return None

def summarize_as_json(text: str) -> dict:
    prompt = f"""
Return ONLY a valid JSON object with keys "title" and "bullets".
- "title" is a five word heading.
- "bullets" is a list of three short points.

Text:
{text}
""".strip()

    resp = client.chat.completions.create(
        model="gpt-4o-mini",                  # use your Azure DEPLOYMENT name
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=220
    )

    raw = resp.choices[0].message.content or ""
    raw = strip_code_fences(raw)

    data = safe_json_loads(raw)
    if isinstance(data, dict) and "title" in data and "bullets" in data:
        # Normalize bullets to list of strings
        bullets = data.get("bullets", [])
        if isinstance(bullets, str):
            bullets = [bullets]
        bullets = [str(b).strip() for b in bullets][:3]
        return {"title": str(data.get("title", "Summary")).strip(), "bullets": bullets}

    # Fallback if the model returned plain text
    return {"title": "Summary", "bullets": [raw[:300].strip()]}

def combine_partials(partials: list[dict]) -> str:
    # Turn a list of {"title","bullets"} dicts into one plain string
    blocks = []
    for p in partials:
        title = p.get("title", "Summary")
        bullets = p.get("bullets", [])
        if isinstance(bullets, str):
            bullets = [bullets]
        block = title + "\n- " + "\n- ".join(bullets[:3])
        blocks.append(block)
    return "\n\n".join(blocks)

def summarize_long(text: str) -> dict:
    partials = []
    for chunk in chunk_text(text):
        partials.append(summarize_as_json(chunk))   # dicts

    combined_text = combine_partials(partials)      # string
    final = summarize_as_json(combined_text)        # dict
    return final

if __name__ == "__main__":
    content = input("Paste the text to summarize:\n")
    print("\nSummary:\n")
    print(summarize_long(content))
