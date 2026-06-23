# Project 2: AI-Powered Customer Support Assistant

**Difficulty:** Beginner

## What This Project Does

This application acts as a smart customer support bot. It understands user questions using semantic search, retrieves the best answer from a knowledge base of FAQ documents, and generates a clear, polite response using RAG.

The key feature that makes this different from Project 1 is **confidence logic**. If the system is not confident about its answer (low similarity score), it tells the user that a human agent may need to help.

The output includes:
- A clear, customer-friendly answer
- A confidence indicator (High, Medium, or Low)
- An escalation notice when confidence is low

## What You Will Need

### 1. Python

You need Python 3.9 or higher. Check your version:

```
python --version
```

### 2. OpenAI API Key

- Go to https://platform.openai.com/api-keys
- Create a new key and copy it

### 3. Required Python Packages

Install everything with one command:

```
pip install -r requirements.txt
```

| Package        | Purpose                                              |
|----------------|------------------------------------------------------|
| openai         | Embeddings and text generation via OpenAI API        |
| chromadb       | Vector database for storing and searching FAQ chunks |
| streamlit      | Web interface for the support assistant              |
| python-dotenv  | Loads your API key securely from a .env file         |

**Note for Windows users:** If you see an error related to ChromaDB, run:

```
pip install onnxruntime
```

## How to Set Up

### Step 1: Create the .env file

In the project folder, create a file called `.env` and add your API key:

```
OPENAI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual key. Do not add quotes.

**Important:** Never share this file or push it to GitHub.

### Step 2: Check the project files

Your project folder should look like this:

```
project2/
    app.py
    support_assistant.py
    knowledge_base/
        general_faq.txt
        billing_faq.txt
        technical_faq.txt
    .env
    .gitignore
    requirements.txt
    README.md
```

The `knowledge_base/` folder contains sample FAQ documents. You can edit these or add your own.

## How to Run

Open your terminal, navigate to the project folder, and run:

```
streamlit run app.py
```

This opens the app in your browser (usually at http://localhost:8501).

### Using the App

1. The app automatically loads FAQ documents from the `knowledge_base/` folder on first run
2. Type a customer question in the input box
3. Click "Get Answer"
4. The system shows an answer with a confidence level
5. If confidence is low, an escalation notice appears

## Project Structure

| File / Folder            | What It Does                                              |
|--------------------------|-----------------------------------------------------------|
| `app.py`                 | Streamlit interface (input, display, confidence badges)    |
| `support_assistant.py`   | Core logic (load docs, chunk, embed, retrieve, RAG, confidence) |
| `knowledge_base/`        | Folder with sample FAQ text files                         |
| `general_faq.txt`        | General company questions (hours, contact, returns)       |
| `billing_faq.txt`        | Billing and payment related questions                     |
| `technical_faq.txt`      | Technical support and troubleshooting questions            |
| `.env`                   | Stores your API key (you create this yourself)            |
| `.gitignore`             | Prevents sensitive files from being pushed to GitHub      |
| `requirements.txt`       | Python packages needed to run the project                 |

## Troubleshooting

**"ModuleNotFoundError"** - Run `pip install -r requirements.txt` again.

**"AuthenticationError"** - Check your `.env` file has the correct API key.

**"No documents found"** - Make sure the `knowledge_base/` folder has at least one `.txt` file with content.

**"Low confidence on every question"** - The sample FAQ files may not cover your question. Try asking something related to the content in those files, like "How do I return a product?" or "What payment methods do you accept?"

## Reference Chapters

- Chapter 6: Master Prompt Engineering to Make AI Work for You
- Chapter 7: Build Your First AI App by Turning Ideas into Code
- Chapter 8: Create Smart Workflows by Chaining AI Actions Together
- Chapter 9: Design Beautiful AI Apps with Professional User Interfaces
- Chapter 10: Teach AI to Understand Meaning with Semantic Search
- Chapter 11: Build AI Memory with Knowledge Bases and Vector Databases
- Chapter 12: Create AI with Memory Using RAG Systems That Remember
- Chapter 18: Build Responsible AI with Ethics and Safety Best Practices

## Extra Challenges

Once the basic version works, try these improvements:

- Add metadata filtering such as product category or department
- Introduce short-term conversation memory to handle follow-up questions
- Track unanswered questions and log them for improvement
- Add analytics such as most frequently asked topics
- Deploy the assistant to cloud and test scalability
