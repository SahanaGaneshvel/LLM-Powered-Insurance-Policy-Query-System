# LLM-Powered Insurance Policy Query System

This project is an end-to-end, modular system for querying insurance policy documents using LLMs (Large Language Models) and semantic search. It supports PDF/DOCX ingestion, semantic clause retrieval, LLM-based reasoning, and a feedback loop for policy improvement.

---

## Feature Overview

- **Index Documents:**
  - Scans your `/data/policies/` folder for `.pdf` and `.docx` files, extracts and cleans their text, chunks them, generates embeddings, and stores them in a vector database (FAISS) with metadata.
  - Use this after adding, removing, or updating policy documents.

- **Query Policies:**
  - Enter a natural language insurance query (e.g., “46-year-old male, knee surgery in Pune, 3-month-old insurance policy”).
  - The system parses your query, retrieves the most relevant policy clauses, and uses an LLM to generate a structured decision (approved/rejected, amount, justification, references).

- **Weekly Report:**
  - Shows analytics and feedback based on all queries and decisions made.
  - Summarizes the most common reasons for claim rejection and other stats to help improve your policies and system.

---

## Features
- **Document Preprocessing:** Extracts, cleans, and chunks policy documents from `/data/policies/`.
- **Embedding & Indexing:** Embeds chunks and stores them in a persistent FAISS vector database with metadata.
- **Semantic Query Processing:** Parses user queries for structured information (age, procedure, duration, etc.).
- **Clause Retrieval:** Finds top-k relevant clauses using vector search.
- **LLM Reasoning:** Uses Groq's Llama API to generate structured decisions and explanations.
- **Clause Reference Tracing:** Every clause in the output includes document name and page number.
- **Feedback Loop:** Logs all queries and decisions, and generates weekly reports on common failure reasons.
- **Streamlit UI:** Simple web interface for indexing, querying, and viewing reports.

---

## Setup

### 1. Clone the Repository
```
git clone <your-repo-url>
cd LLM-Powered Insurance Policy Query System
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Add Your Groq API Key
Create a `.env` file in the main directory:
```
GROQ_API_KEY=your_actual_groq_api_key_here
```

### 4. Add Policy Documents
Place your `.pdf` and `.docx` policy files in the `data/policies/` directory.

---

## Usage

### 1. Start the FastAPI Backend
```
uvicorn main:app --reload
```

### 2. (Optional) Start the Streamlit UI
```
streamlit run streamlit_app.py
```

- The UI will let you index documents, submit queries, and view weekly reports.
- You can also use the API directly:
  - `POST /index` — Index all policy documents
  - `POST /query` — Query policies (JSON: `{ "query": "...", "top_k": 5 }`)
  - `GET /report` — Get weekly summary report

---

## Architecture

```
/data/policies/         # Policy documents (.pdf, .docx)
preprocessing/          # Extraction, cleaning, chunking
embedding/              # Embedding and FAISS index logic
query/                  # Query parsing and clause retrieval
llm/                    # LLM (Groq Llama) integration
feedback/               # Logging and reporting
main.py                 # FastAPI entry point
streamlit_app.py        # Streamlit UI
```

---

## Notes
- The vector database (FAISS) is persistent across sessions.
- All logs are stored in `query_log.jsonl` for feedback and reporting.
- Make sure your `.env` file is **not** committed to version control.

---

## License
MIT 