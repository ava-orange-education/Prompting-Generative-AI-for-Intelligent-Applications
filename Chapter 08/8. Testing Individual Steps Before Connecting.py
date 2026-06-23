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

# ---------------------------------------
# STEP 1: Summarize
# ---------------------------------------
step1_prompt = PromptTemplate.from_template(
    "Summarize this in one sentence: {text}"
)

step1_chain = step1_prompt | llm | parser

step1_result = step1_chain.invoke({"text": "Long article text here..."})
print("Step 1:", step1_result)

# ---------------------------------------
# STEP 2: Extract topic from summary
# ---------------------------------------
step2_prompt = PromptTemplate.from_template(
    "What is the main topic of this summary? {summary}"
) 

step2_chain = step2_prompt | llm | parser

step2_result = step2_chain.invoke({"summary": "Sample summary here..."})
print("Step 2:", step2_result)

# ---------------------------------------
# COMBINE 
# ---------------------------------------

# A combined pipeline: output of step1 -> input of step2
full_chain = step1_chain | step2_chain

final_result = full_chain.invoke({"text": "Long article text here..."})
print("Final:", final_result)
