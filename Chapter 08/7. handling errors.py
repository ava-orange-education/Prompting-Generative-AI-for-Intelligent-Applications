import os
import logging
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Step 1: Define the model (ChatOpenAI instead of OpenAI)
llm = ChatOpenAI(
    api_key=api_key,
    model="gpt-4o-mini",
    temperature=0,  # deterministic
    # api_key is read from OPENAI_API_KEY in env, no need to pass explicitly
)

# Step 2: Create a prompt template
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Write three benefits of {topic}."
)

# Step 3: Output parser to get plain text
parser = StrOutputParser()

# Step 4: LCEL chain (replaces LLMChain)
chain = prompt | llm | parser

# Step 5: Run inside try/except
try:
    result = chain.invoke({"topic": "exercise"})
    print(result)
except Exception as e:
    logger.error(f"Chain failed: {e}")
    print("Sorry, something went wrong. Please try again.")
