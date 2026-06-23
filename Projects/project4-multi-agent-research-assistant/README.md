# Project 4: Multi-Agent Research Assistant

**Difficulty:** Advanced

## What This Project Does

This application takes a research topic as input and produces a structured research report by orchestrating three AI agents that work in sequence:

1. **Research Agent** - Gathers broad information and identifies key subtopics
2. **Analysis Agent** - Evaluates the research, finds patterns, pros and cons, risks and opportunities
3. **Report Writer Agent** - Converts the analysis into a professional, structured report

The final output includes an executive summary, key findings, detailed analysis, and a conclusion. You can see the output of each agent step by step, so you understand how information flows through the chain.

This project is fundamentally different from Projects 1 to 3. There is no vector database or retrieval involved. The focus here is on **agent orchestration and sequential chaining**, where each agent has a specific role and passes its output to the next.

## What You Will Need

### 1. Python

Python 3.9 or higher. Check your version:

```
python --version
```

### 2. OpenAI API Key

- Go to https://platform.openai.com/api-keys
- Create a new key and copy it

**Note:** This project makes 3 sequential API calls per report (one per agent), so it uses more tokens than the earlier projects. A typical report costs approximately 3,000 to 5,000 tokens total.

### 3. Required Python Packages

```
pip install -r requirements.txt
```

| Package        | Purpose                                           |
|----------------|---------------------------------------------------|
| openai         | Powers each AI agent through the OpenAI API       |
| streamlit      | Web interface for topic input and report display   |
| python-dotenv  | Loads your API key securely from a .env file      |

## How to Set Up

### Step 1: Create the .env file

In the project folder, create a file called `.env`:

```
OPENAI_API_KEY=your_api_key_here
```

### Step 2: Check the project files

```
project4/
    app.py
    research_agents.py
    .env
    .gitignore
    requirements.txt
    README.md
```

## How to Run

```
streamlit run app.py
```

### Using the App

1. Enter a research topic (for example: "The future of remote work" or "Impact of AI on healthcare")
2. Click "Generate Research Report"
3. Watch each agent complete its task step by step
4. Read the final structured report
5. Expand each agent's section to see their individual outputs

### Example Topics to Try

- "The impact of electric vehicles on the global auto industry"
- "Advantages and risks of adopting AI in education"
- "The rise of remote work and its effect on company culture"
- "How blockchain technology is changing supply chain management"

## Project Structure

| File                  | What It Does                                              |
|-----------------------|-----------------------------------------------------------|
| `app.py`              | Streamlit interface (topic input, step display, report)    |
| `research_agents.py`  | Core logic (3 agents, sequential chaining, validation)     |
| `.env`                | Stores your API key (you create this yourself)             |
| `.gitignore`          | Prevents sensitive files from being pushed to GitHub       |
| `requirements.txt`    | Python packages needed to run the project                  |

## How the Agent Chain Works

```
User enters topic
       |
       v
 Research Agent
 (gathers information, identifies subtopics)
       |
       v
 Analysis Agent
 (evaluates research, finds patterns and risks)
       |
       v
 Report Writer Agent
 (structures everything into a professional report)
       |
       v
 Final Report displayed to user
```

Each agent receives the output of the previous agent as part of its input. No agent sees the full picture alone. Together, they produce a result that is more structured and thorough than a single prompt could achieve.

## Troubleshooting

**"AuthenticationError"** - Check your `.env` file has the correct API key.

**"The report seems thin or generic"** - Try a more specific topic. "AI" is too broad. "How AI is being used in radiology to detect cancer" gives much better results.

**"Takes too long"** - The system makes 3 API calls in sequence. Each takes a few seconds. Total time is typically 15 to 30 seconds.

**"One agent produced weak output"** - The validation checks will flag this. Try regenerating, or refine your topic to be more specific.

## Reference Chapters

- Chapter 6: Master Prompt Engineering to Make AI Work for You
- Chapter 7: Build Your First AI App by Turning Ideas into Code
- Chapter 8: Create Smart Workflows by Chaining AI Actions Together
- Chapter 9: Design Beautiful AI Apps with Professional User Interfaces
- Chapter 13: Use Design Thinking to Build Reasoning AI Agents
- Chapter 14: Orchestrate AI Teams with Collaborative Multi-Agent Systems
- Chapter 18: Build Responsible AI with Ethics and Safety Best Practices

## Extra Challenges

- Introduce a fact-verification agent to cross-check claims
- Add an iteration loop where the Analysis Agent can request more research
- Allow users to download the final report as PDF
- Compare sequential chaining versus autonomous agent approach
- Deploy and measure token usage per agent
