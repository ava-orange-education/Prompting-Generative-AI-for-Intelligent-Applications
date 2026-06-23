from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
import logging

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Step 1: Model
llm = ChatOpenAI(
    api_key=api_key,
    model="gpt-4o-mini",
    temperature=0.5
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Step 2: Prompt
prompt = PromptTemplate.from_template(
    "Write three benefits of {topic}."
)

# Step 3: Parser
parser = StrOutputParser()

# Step 4: LCEL chain 
chain = prompt | llm | parser

# Step 5: Run the chain
logger.info("Starting chain execution")
result = chain.invoke({"topic": "exercise"})
logger.info(f"Result: {result}")
