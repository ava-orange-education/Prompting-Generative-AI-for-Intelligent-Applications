# Project 5: Enterprise AI Copilot for Internal Knowledge Base

**Difficulty:** Advanced

## What This Project Does

This is the most comprehensive project in the book. It brings together nearly every concept you have learned into a single enterprise-level application.

The Enterprise AI Copilot acts as an internal knowledge assistant for a company. Employees can ask questions in natural language, and the system retrieves answers from company documents using semantic search and RAG.

What makes this project different from all earlier ones:

- **Conversation memory** - The system remembers previous questions in the session so employees can ask follow-up questions naturally
- **Department-based metadata filtering** - Employees can search within specific departments (HR, Engineering, Finance, etc.)
- **Responsible AI safeguards** - The system refuses to speculate, adds disclaimers, and avoids generating restricted content
- **Structured for deployment** - The code is organized in a way that can be deployed to AWS, Azure, or GCP
- **Query logging** - Every question and response is logged for monitoring and improvement

## What You Will Need

### 1. Python

Python 3.9 or higher.

```
python --version
```

### 2. OpenAI API Key

- Go to https://platform.openai.com/api-keys
- Create a new key and copy it

### 3. Required Python Packages

```
pip install -r requirements.txt
```

| Package        | Purpose                                                    |
|----------------|------------------------------------------------------------|
| openai         | Embeddings and text generation via OpenAI API              |
| chromadb       | Vector database with metadata filtering                    |
| streamlit      | Web interface for the copilot                              |
| python-dotenv  | Loads your API key securely from a .env file               |
| PyPDF2         | Reads text from uploaded PDF documents                     |

## How to Set Up

### Step 1: Create the .env file

```
OPENAI_API_KEY=your_api_key_here
```

### Step 2: Check the project files

```
project5/
    app.py
    copilot_engine.py
    responsible_ai.py
    company_documents/
        hr_onboarding_guide.txt
        engineering_release_process.txt
        finance_expense_policy.txt
        it_security_guidelines.txt
    .env
    .gitignore
    requirements.txt
    README.md
```

The `company_documents/` folder contains four sample internal documents from different departments. Each document is tagged with department metadata during ingestion.

## How to Run

```
streamlit run app.py
```

### Using the App

1. Click "Load and Index Documents" to process the sample company documents
2. Optionally select a department filter (HR, Engineering, Finance, IT, or All)
3. Type a question in the chat input at the bottom
4. The copilot responds with a grounded answer, source citations, and a responsible AI disclaimer
5. Ask follow-up questions naturally. The system remembers the conversation context.

### Example Conversations to Try

**Single question:**
- "What is the process for submitting expenses?"
- "How do I set up my development environment?"

**Follow-up conversation:**
- "What are the security requirements for passwords?"
- Then: "What about two-factor authentication?" (the system remembers the security context)
- Then: "Are there any exceptions to these rules?"

**Department-filtered search:**
- Select "HR" and ask: "What happens during the first week of onboarding?"
- Select "Engineering" and ask: "How are releases approved?"

**Responsible AI in action:**
- Ask: "What is the CEO's personal phone number?" (the system will decline)
- Ask: "Can you guess what next quarter's revenue will be?" (the system will refuse to speculate)

## Project Structure

| File / Folder              | What It Does                                                 |
|----------------------------|--------------------------------------------------------------|
| `app.py`                   | Streamlit chat interface with memory and filters              |
| `copilot_engine.py`        | Core logic (ingest, chunk, embed, retrieve, RAG with memory)  |
| `responsible_ai.py`        | Safety checks, disclaimers, and content filtering             |
| `company_documents/`       | Sample internal documents from 4 departments                  |
| `.env`                     | Stores your API key (you create this yourself)                |
| `.gitignore`               | Prevents sensitive files from being pushed to GitHub          |
| `requirements.txt`         | Python packages needed to run the project                     |

## System Architecture

```
Employee asks a question
        |
        v
  Responsible AI Check (block unsafe queries)
        |
        v
  Conversation Memory (include previous context)
        |
        v
  Metadata Filter (optional department filter)
        |
        v
  Semantic Retrieval (ChromaDB)
        |
        v
  RAG Prompt (grounded answer with citations)
        |
        v
  Responsible AI Disclaimer (added to response)
        |
        v
  Response displayed + logged
```

## Troubleshooting

**"No documents indexed"** - Click "Load and Index Documents" in the sidebar first.

**"Follow-up answers ignore context"** - Make sure you are in the same session. Refreshing the page clears conversation memory.

**"Answers seem too cautious"** - This is intentional. The responsible AI layer prevents speculation. If you want more flexible answers, you can adjust the safety settings in `responsible_ai.py`.

**"Department filter returns no results"** - The sample documents cover HR, Engineering, Finance, and IT. Questions outside these topics will not find matches.

## Reference Chapters

- Chapter 6: Master Prompt Engineering to Make AI Work for You
- Chapter 7: Build Your First AI App by Turning Ideas into Code
- Chapter 8: Create Smart Workflows by Chaining AI Actions Together
- Chapter 9: Design Beautiful AI Apps with Professional User Interfaces
- Chapter 10: Teach AI to Understand Meaning with Semantic Search
- Chapter 11: Build AI Memory with Knowledge Bases and Vector Databases
- Chapter 12: Create AI with Memory Using RAG Systems That Remember
- Chapter 13: Use Design Thinking to Build Reasoning AI Agents
- Chapter 14: Orchestrate AI Teams with Collaborative Multi-Agent Systems
- Chapter 16: Launch AI Apps on AWS, Azure, and GCP
- Chapter 18: Build Responsible AI with Ethics and Safety Best Practices

## Extra Challenges

- Add role-based access control simulation
- Introduce an analytics dashboard for query trends
- Compare performance with and without metadata filtering
- Add a feedback system for answer quality improvement
- Implement logging and monitoring for production readiness
- Deploy to AWS, Azure, or GCP using the patterns from Chapter 16
