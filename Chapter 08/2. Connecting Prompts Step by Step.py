import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=api_key,
    temperature=0.6
)

parser = StrOutputParser()

# Step 1: Summarise text
summary_prompt = PromptTemplate.from_template(
    "Summarise the following text in one short paragraph:\n\n{text}"
)
summary_chain = summary_prompt | llm | parser

# Step 2: Extract keywords from summary
keyword_prompt = PromptTemplate.from_template(
    "List five keywords from the following summary:\n\n{summary}"
)
keyword_chain = keyword_prompt | llm | parser

# Combine chains (SequentialChain replacement)
overall_chain = summary_chain | keyword_chain

# Run workflow
text = """
Machine learning helps systems learn automatically from data
without being explicitly programmed. It powers recommendation
systems, speech recognition, and self-driving cars.
"""

result = overall_chain.invoke({"text": text})
print(result)
