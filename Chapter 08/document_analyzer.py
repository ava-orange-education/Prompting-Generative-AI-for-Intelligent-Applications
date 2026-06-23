from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Model
llm = ChatOpenAI(
    api_key=api_key,
    model="gpt-4o-mini",
    temperature=0
)


parser = StrOutputParser()

# -------------------------------
# STEP 1 — SUMMARY CHAIN
# -------------------------------
summary_template = """
Summarize the following document in exactly three clear bullet points:

Document:
{document}

Summary:
"""

summary_prompt = PromptTemplate.from_template(summary_template)
summary_chain = summary_prompt | llm | parser

# -------------------------------
# STEP 2 — TOPIC IDENTIFICATION
# -------------------------------
topic_template = """
Based on this summary, identify the main topic in one clear sentence:

Summary:
{summary}

Main Topic:
"""

topic_prompt = PromptTemplate.from_template(topic_template)
topic_chain = topic_prompt | llm | parser

# -------------------------------
# STEP 3 — FOLLOW-UP QUESTIONS
# -------------------------------
questions_template = """
Based on this topic, suggest three thoughtful follow-up questions that would help someone understand it better:

Topic:
{topic}

Questions:
"""

questions_prompt = PromptTemplate.from_template(questions_template)
questions_chain = questions_prompt | llm | parser

# -------------------------------
# COMBINE THE PIPELINE
# -------------------------------
full_chain = (
    summary_chain
    | (lambda summary: {"summary": summary})
    | topic_chain
    | (lambda topic: {"topic": topic})
    | questions_chain
)

# -------------------------------
# RUN THE PIPELINE
# -------------------------------
sample_doc = """
Artificial intelligence is transforming industries worldwide. Companies use AI 
for automation, data analysis, and customer service. Machine learning models 
can now predict trends, detect fraud, and personalize user experiences. However, 
ethical concerns around bias and privacy remain important challenges that 
organizations must address.
"""

result = full_chain.invoke({"document": sample_doc})

print("\n=== DOCUMENT ANALYSIS ===\n")
print("Summary:\n", result.split("Main Topic:")[0].strip())
print("\nMain Topic:\n", result.split("Questions:")[0].split("Main Topic:")[-1].strip())
print("\nFollow-up Questions:\n", result.split("Questions:")[-1].strip())
