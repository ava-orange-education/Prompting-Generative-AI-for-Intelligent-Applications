# Project 3: Multi-Document Insight Engine

**Difficulty:** Intermediate

## What This Project Does

This application lets users upload multiple documents and ask natural language questions that span across all of them. Unlike the earlier projects that work with a single document, this system:

- Tracks which document each answer comes from (source citation)
- Supports cross-document comparison queries
- Uses metadata filtering so users can search within specific documents or across all of them
- Displays similarity scores for transparency

This is how enterprise document intelligence systems work in real companies.

## What You Will Need

### 1. Python

Python 3.9 or higher. Check your version:

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

| Package        | Purpose                                                    |
|----------------|------------------------------------------------------------|
| openai         | Embeddings and text generation via OpenAI API              |
| chromadb       | Vector database with metadata filtering support            |
| streamlit      | Web interface for uploading documents and asking questions  |
| python-dotenv  | Loads your API key securely from a .env file               |
| PyPDF2         | Reads text from uploaded PDF documents                     |

**Note for Windows users:** If you see an error related to ChromaDB, run:

```
pip install onnxruntime
```

## How to Set Up

### Step 1: Create the .env file

In the project folder, create a file called `.env`:

```
OPENAI_API_KEY=your_api_key_here
```

### Step 2: Check the project files

```
project3/
    app.py
    document_engine.py
    sample_documents/
        company_leave_policy.txt
        remote_work_policy.txt
        employee_code_of_conduct.txt
    .env
    .gitignore
    requirements.txt
    README.md
```

The `sample_documents/` folder contains three sample policy documents you can use to test the app. You can also upload your own PDF or TXT files through the interface.

## How to Run

```
streamlit run app.py
```

### Using the App

1. Upload one or more documents (PDF or TXT) using the file uploader
2. Wait for the system to process and index them
3. Optionally select a specific document to search within, or leave it on "All Documents"
4. Type a question in the input box
5. Click "Search and Answer"
6. The system shows a grounded answer with source citations and similarity scores

### Try These Example Questions

With the sample documents loaded:

- "What is the leave policy for new employees?"
- "Can employees work remotely on Fridays?"
- "Compare the remote work policy with the code of conduct regarding professional behavior"
- "Which documents mention disciplinary action?"

## Project Structure

| File / Folder               | What It Does                                                |
|-----------------------------|-------------------------------------------------------------|
| `app.py`                    | Streamlit interface (upload, filter, question, display)      |
| `document_engine.py`        | Core logic (chunk, embed, store, retrieve, compare, RAG)     |
| `sample_documents/`         | Sample policy documents for testing                          |
| `.env`                      | Stores your API key (you create this yourself)               |
| `.gitignore`                | Prevents sensitive files from being pushed to GitHub         |
| `requirements.txt`          | Python packages needed to run the project                    |

## What Makes This Different from Projects 1 and 2

| Feature                    | Project 1 & 2            | Project 3                    |
|----------------------------|--------------------------|------------------------------|
| Number of documents        | Single document          | Multiple documents           |
| Source tracking             | Not included             | Each chunk tagged with source |
| Metadata filtering          | Not included             | Filter by document name       |
| Cross-document comparison   | Not applicable           | Compare across sources        |
| Similarity score display    | Not included             | Shown to user                 |

## Troubleshooting

**"No documents processed yet"** - Upload at least one document and wait for the success message before asking questions.

**"Empty or unreadable PDF"** - Make sure the PDF has selectable text, not scanned images.

**"Comparison results seem incomplete"** - Cross-document comparison works best when at least two documents cover overlapping topics.

## Reference Chapters

- Chapter 6: Master Prompt Engineering to Make AI Work for You
- Chapter 7: Build Your First AI App by Turning Ideas into Code
- Chapter 9: Design Beautiful AI Apps with Professional User Interfaces
- Chapter 10: Teach AI to Understand Meaning with Semantic Search
- Chapter 11: Build AI Memory with Knowledge Bases and Vector Databases
- Chapter 12: Create AI with Memory Using RAG Systems That Remember
- Chapter 18: Build Responsible AI with Ethics and Safety Best Practices

## Extra Challenges

- Add an option to compare answers from two different models
- Implement adjustable chunk size through the UI
- Introduce conversation memory so users can ask follow-up questions
- Deploy and measure response time and retrieval latency
