# Project 1: Intelligent Resume Analyzer with RAG

**Difficulty:** Beginner

## What This Project Does

This application compares a candidate's resume with a job description and generates a structured evaluation report. It uses semantic search and Retrieval Augmented Generation (RAG) to understand meaning, not just keywords.

The final output includes:
- A match summary
- Strength areas
- Skill gaps
- Improvement suggestions

## What You Will Need

Before running this project, make sure you have the following installed on your computer.

### 1. Python

You need Python 3.9 or higher. Check your version by running:

```
python --version
```

If you do not have Python, download it from https://www.python.org/downloads/

### 2. OpenAI API Key

This project uses the OpenAI API for embeddings and text generation. You will need an API key.

- Go to https://platform.openai.com/api-keys
- Create a new key
- Copy it and keep it safe

You will store this key in a file called `.env` (explained below).

### 3. Required Python Packages

Install all required packages by running this command in your terminal:

```
pip install openai chromadb streamlit python-dotenv PyPDF2
```

Here is what each package does:

| Package        | Purpose                                      |
|----------------|----------------------------------------------|
| openai         | Connects to the OpenAI API for embeddings and text generation |
| chromadb       | Vector database to store and search resume chunks |
| streamlit      | Creates the web interface for uploading and viewing results |
| python-dotenv  | Loads your API key securely from a .env file  |
| PyPDF2         | Reads text from uploaded PDF resumes          |

**Note for Windows users:** ChromaDB may require `onnxruntime`. If you see an error, run:

```
pip install onnxruntime
```

## How to Set Up

### Step 1: Create the .env file

In the same folder as the project files, create a file called `.env` and add your API key:

```
OPENAI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual key. Do not add quotes around it.

**Important:** Never share this file or upload it to GitHub. The `.gitignore` file in this project already excludes it.

### Step 2: Check the project files

Your project folder should look like this:

```
project1/
    app.py
    resume_analyzer.py
    .env
    .gitignore
    README.md
    sample_resume.txt
```

## How to Run

Open your terminal, navigate to the project folder, and run:

```
streamlit run app.py
```

This will open the application in your web browser (usually at http://localhost:8501).

### Using the App

1. Upload a resume (PDF or TXT format)
2. Paste the job description in the text area
3. Click "Analyze Resume"
4. Wait a few seconds for the evaluation report to appear

## Project Structure

| File                 | What It Does                                           |
|----------------------|--------------------------------------------------------|
| `app.py`             | The Streamlit interface (upload, input, display)       |
| `resume_analyzer.py` | The core logic (chunking, embedding, retrieval, RAG)   |
| `sample_resume.txt`  | A sample resume you can use to test the app            |
| `.env`               | Stores your API key (you create this yourself)         |
| `.gitignore`         | Prevents sensitive files from being uploaded to GitHub  |

## Troubleshooting

**"ModuleNotFoundError"** - Run the pip install command again. Make sure you are using the correct Python environment.

**"AuthenticationError"** - Check that your `.env` file has the correct API key and that it has not expired.

**"The app does not open in the browser"** - Try opening http://localhost:8501 manually in your browser.

**"Empty results or errors with PDF"** - Make sure the PDF contains selectable text, not just scanned images. Scanned PDFs need OCR, which is not covered in this project.

## Reference Chapters

If you get stuck, revisit these chapters from the book:

- Chapter 6: Master Prompt Engineering to Make AI Work for You
- Chapter 7: Build Your First AI App by Turning Ideas into Code
- Chapter 9: Design Beautiful AI Apps with Professional User Interfaces
- Chapter 10: Teach AI to Understand Meaning with Semantic Search
- Chapter 11: Build AI Memory with Knowledge Bases and Vector Databases
- Chapter 12: Create AI with Memory Using RAG Systems That Remember

## Extra Challenges

Once the basic version is working, try these improvements:

- Add a match score percentage based on similarity scores
- Introduce role-based prompting such as "You are a senior HR recruiter"
- Allow multiple resumes and rank candidates automatically
- Deploy the app on AWS, Azure, or GCP
- Add a responsible AI disclaimer to avoid overreliance on automated hiring decisions
