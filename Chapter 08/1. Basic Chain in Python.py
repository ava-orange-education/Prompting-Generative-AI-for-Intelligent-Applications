from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv() 

api_key = os.getenv("OPENAI_API_KEY")


# Step 1: Define the model (Chat-based model)
llm = ChatOpenAI(
    api_key=api_key,
    model="gpt-4o-mini",
    temperature=0.7,          
    )

# Step 2: Create a prompt template
prompt = PromptTemplate.from_template(
    "Explain the importance of {topic} in simple terms."
)

# Step 3: Create an output parser (string)
parser = StrOutputParser()

# Step 4: Build the chain using LCEL (this replaces LLMChain)
chain = prompt | llm | parser

# Step 5: Run the chain
response = chain.invoke({"topic": "machine learning"})
print(response)
