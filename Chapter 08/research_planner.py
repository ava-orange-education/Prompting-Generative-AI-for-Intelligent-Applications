import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

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

# --------------------------------------------------------------------
# Research Hours Logic 
# --------------------------------------------------------------------
def estimate_research_hours(complexity):
    hours_map = {
        'simple': 5,
        'moderate': 15,
        'complex': 30
    }
    return hours_map.get(complexity.lower(), 10)

# --------------------------------------------------------------------
# Prompt and LCEL chain 
# --------------------------------------------------------------------
questions_template = """
Generate three clear research questions about the following topic. 
Label each as 'simple', 'moderate', or 'complex' based on depth needed.

Topic: {topic}

Format as:
1. [Question] - [complexity level]
2. [Question] - [complexity level]
3. [Question] - [complexity level]
"""

questions_prompt = PromptTemplate.from_template(questions_template)

questions_chain = questions_prompt | llm | parser

# --------------------------------------------------------------------
# Processing logic
# --------------------------------------------------------------------
def process_research_plan(inputs):
    topic = inputs["topic"]
    
    # NEW: modern invoke
    questions_result = questions_chain.invoke({"topic": topic})
    
    lines = questions_result.strip().split("\n")
    total_hours = 0
    plan_details = []

    for line in lines:
        if "-" in line:
            # Split only on last hyphen to avoid parsing issues
            question_part, complexity_part = line.rsplit("-", 1)
            complexity = complexity_part.strip().lower().split()[0]
            hours = estimate_research_hours(complexity)
            total_hours += hours
            plan_details.append(f"{question_part.strip()} → {hours} hours")

    return {
        "questions": questions_result,
        "plan": "\n".join(plan_details),
        "total_hours": total_hours
    }

# --------------------------------------------------------------------
# Run the flow
# --------------------------------------------------------------------
topic = input("Enter your research topic: ")

result = process_research_plan({"topic": topic})

print("\n=== RESEARCH PLAN ===\n")
print("Research Questions:")
print(result["questions"])

print("\nTime Breakdown:")
print(result["plan"])

print(f"\nTotal Estimated Hours: {result['total_hours']}")
