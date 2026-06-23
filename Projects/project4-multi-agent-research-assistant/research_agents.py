# research_agents.py
# Core logic: three AI agents with sequential chaining
# Research Agent -> Analysis Agent -> Report Writer Agent

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Constants ---
GENERATION_MODEL = "gpt-4o-mini"
MIN_OUTPUT_WORDS = 80   # Minimum words to consider an agent output valid


def get_openai_client():
    """
    Create and return the OpenAI client on demand.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found. "
            "Please add it to your .env file."
        )
    return OpenAI(api_key=api_key)


def validate_output(output, agent_name):
    """
    Check if an agent's output meets the minimum quality threshold.
    Returns True if valid, raises ValueError if too short.
    """
    word_count = len(output.split())
    if word_count < MIN_OUTPUT_WORDS:
        raise ValueError(
            f"{agent_name} produced a response with only {word_count} words. "
            f"Minimum required is {MIN_OUTPUT_WORDS}. "
            "Try a more specific or detailed topic."
        )
    return True


def run_research_agent(topic):
    """
    Agent 1: Research Agent
    Gathers broad information about the topic and identifies key subtopics.

    Input: research topic (string)
    Output: research findings (string)
    """
    system_prompt = (
        "You are a professional researcher. Your job is to gather "
        "comprehensive information about a given topic. You identify "
        "key subtopics, important facts, recent developments, and "
        "relevant data points. You write in a clear, factual style "
        "without personal opinions."
    )

    user_prompt = f"""Research the following topic thoroughly:

Topic: {topic}

Provide your research output with the following structure:
1. Overview: A brief introduction to the topic
2. Key Subtopics: List and describe the most important areas within this topic
3. Important Facts and Data: Include specific facts, statistics, or developments
4. Current Trends: What is happening right now in this space
5. Notable Examples: Real-world examples or case studies if applicable

Be thorough and factual. Your output will be used by an analysis agent in the next step."""

    response = get_openai_client().chat.completions.create(
        model=GENERATION_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.4,
        max_tokens=1200
    )

    output = response.choices[0].message.content
    usage = response.usage.total_tokens

    validate_output(output, "Research Agent")

    return output, usage


def run_analysis_agent(topic, research_output):
    """
    Agent 2: Analysis Agent
    Evaluates the research and identifies patterns, pros and cons,
    risks, and opportunities.

    Input: topic + research output from Agent 1
    Output: analysis findings (string)
    """
    system_prompt = (
        "You are a strategic analyst. Your job is to evaluate research "
        "findings and extract meaningful insights. You identify patterns, "
        "weigh pros and cons, assess risks and opportunities, and form "
        "balanced conclusions. You write in a structured, analytical style."
    )

    user_prompt = f"""Analyze the following research findings on the topic: {topic}

Research Findings:
{research_output}

Provide your analysis with the following structure:
1. Key Patterns: What recurring themes or patterns do you see in the research?
2. Strengths and Opportunities: What are the positive aspects and potential opportunities?
3. Risks and Challenges: What are the potential downsides, risks, or challenges?
4. Gaps in Information: Is anything important missing from the research?
5. Strategic Insights: What are the most important takeaways for someone making decisions about this topic?

Be balanced and thoughtful. Your output will be used by a report writer agent in the next step."""

    response = get_openai_client().chat.completions.create(
        model=GENERATION_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=1200
    )

    output = response.choices[0].message.content
    usage = response.usage.total_tokens

    validate_output(output, "Analysis Agent")

    return output, usage


def run_report_writer_agent(topic, research_output, analysis_output):
    """
    Agent 3: Report Writer Agent
    Converts the research and analysis into a structured, professional report.

    Input: topic + research output from Agent 1 + analysis output from Agent 2
    Output: final structured report (string)
    """
    system_prompt = (
        "You are a professional business report writer. Your job is to "
        "take research findings and strategic analysis and combine them "
        "into a clear, well-structured report. You write with clarity, "
        "use professional formatting, and ensure the report is easy to "
        "read for a business audience."
    )

    user_prompt = f"""Write a professional research report on the topic: {topic}

Use the following research and analysis as your source material. Do not add information that is not present in these sources.

Research Findings:
{research_output}

Strategic Analysis:
{analysis_output}

Structure the report with the following sections:
1. Executive Summary: A brief overview of the topic and key conclusions (3 to 4 sentences)
2. Key Findings: The most important facts and discoveries from the research
3. Analysis: Insights, patterns, opportunities, and risks identified during analysis
4. Recommendations: Practical suggestions based on the findings and analysis
5. Conclusion: A closing summary that ties everything together

Write in a professional, clear, and accessible tone. Use headings for each section."""

    response = get_openai_client().chat.completions.create(
        model=GENERATION_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=1500
    )

    output = response.choices[0].message.content
    usage = response.usage.total_tokens

    validate_output(output, "Report Writer Agent")

    return output, usage


def run_full_pipeline(topic):
    """
    Full pipeline: run all three agents in sequence.
    Output from each agent feeds into the next.

    Returns a dictionary with:
        - research_output: Agent 1 result
        - analysis_output: Agent 2 result
        - report_output: Agent 3 result (final report)
        - token_usage: dict with per-agent and total token counts
        - status: 'success' or 'error'
        - error_message: error details if status is 'error'
    """
    result = {
        "research_output": "",
        "analysis_output": "",
        "report_output": "",
        "token_usage": {
            "research_agent": 0,
            "analysis_agent": 0,
            "report_writer_agent": 0,
            "total": 0
        },
        "status": "success",
        "error_message": ""
    }

    try:
        # Agent 1: Research
        research_output, research_tokens = run_research_agent(topic)
        result["research_output"] = research_output
        result["token_usage"]["research_agent"] = research_tokens

        # Agent 2: Analysis (receives Agent 1 output)
        analysis_output, analysis_tokens = run_analysis_agent(
            topic, research_output
        )
        result["analysis_output"] = analysis_output
        result["token_usage"]["analysis_agent"] = analysis_tokens

        # Agent 3: Report Writer (receives Agent 1 + Agent 2 output)
        report_output, report_tokens = run_report_writer_agent(
            topic, research_output, analysis_output
        )
        result["report_output"] = report_output
        result["token_usage"]["report_writer_agent"] = report_tokens

        # Total tokens
        result["token_usage"]["total"] = (
            research_tokens + analysis_tokens + report_tokens
        )

    except ValueError as e:
        result["status"] = "error"
        result["error_message"] = str(e)
    except Exception as e:
        result["status"] = "error"
        result["error_message"] = (
            f"An unexpected error occurred: {str(e)}. "
            "Please check your API key and internet connection."
        )

    return result
