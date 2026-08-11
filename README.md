# Coursework Copilot

Coursework Copilot is a RAG-first study assistant for coursework materials such as PDFs, notes, and slides.

This Phase 1 version is now **local-first**:

- embeddings come from **Ollama**
- answer generation comes from **Ollama**
- vector storage uses **Chroma**
- backend uses **FastAPI**
- frontend uses **Next.js**

No paid API key is required for Phase 1.

## Current Status

The project now has:

- **Phase 1**: upload, indexing, retrieval, grounded Q&A with citations
- **Phase 2**: summary, explain simply, quiz, compare topics, revision checklist
- **Phase 3**: lightweight task routing that chooses the right study workflow from one free-form request

Phase 1 is considered truly complete only when you can:

1. start Ollama
2. pull the required local models
3. run the backend
4. run the frontend
5. upload a real PDF or note file
6. ask a question and get a relevant answer with citations

## What Phase 1 Does

Phase 1 is the core RAG pipeline.

1. user uploads a file
2. backend extracts the text
3. backend splits the text into chunks
4. backend sends chunks to Ollama for embeddings
5. backend stores chunk vectors in Chroma
6. user asks a question
7. backend embeds the question with the same Ollama embedding model
8. backend retrieves the most relevant chunks
9. backend sends those chunks to an Ollama chat model
10. app returns the answer and citations

## What Phase 2 Adds

Phase 2 reuses the same retrieval pipeline for more study workflows.

- `summarize`: produce structured study notes for a topic
- `explain simply`: rewrite a concept in beginner-friendly language
- `quiz`: generate short-answer practice questions with answer keys
- `compare`: compare two topics with similarities, differences, and confusion points
- `checklist`: generate a revision checklist grouped by what to review

The important idea is that Phase 2 does **not** build a new AI system. It reuses the
same RAG foundation from Phase 1 and changes the task prompt.

## What Phase 3 Adds

Phase 3 adds a simple routing layer.

- user writes one free-form request
- backend chooses the most suitable workflow
- backend runs the selected Phase 2 study tool
- UI shows which workflow was used and why

Examples:

- `Compare stack and queue`
- `Explain dynamic programming simply`
- `Give me a revision checklist for binary trees`
- `Create a quiz on gradient descent`

This is intentionally **not** a full agent framework. It is a small routing step that
teaches workflow selection before adding LangGraph or more complex orchestration.

## Phase 1 Tech Stack

### Backend

- `Python 3.11`
- `FastAPI`
- `pypdf`
- `httpx`
- `Chroma`
- `Ollama`

### Frontend

- `Next.js`
- `TypeScript`

### Important note about PyTorch

PyTorch is **not required for Phase 1 anymore**.

You can still add PyTorch later in a future phase when you build:

- a reranker
- a topic classifier
- another trained ML component

## What You Need To Install First

Install these before trying to run the project:

1. `Git`
2. `Python 3.11`
3. `Node.js 20+`
4. `npm`
5. `Ollama`

## Your Current Machine Status

Checked on **July 29, 2026**:

- `Git` is installed
- `Node.js` is installed
- `npm` is installed
- `Ollama` is installed
- `Python 3.13.3` is installed

### Important Python warning

Use **Python 3.11** for this project.

Even though some parts may run on newer versions, `3.11` is the safer beginner setup for this stack.

## Ollama Models To Use

For this project, use:

- chat model: `qwen3:4b`
- embedding model: `embeddinggemma`

Pull them first:

```powershell
ollama pull qwen3:4b
ollama pull embeddinggemma
```

Confirm they exist:

```powershell
ollama list
```

## Beginner Startup Guide

This guide assumes:

- you are on **Windows**
- you are using **PowerShell**
- your project folder is:

```text
C:\Users\User\Desktop\personal\ai learning
```

Follow the steps exactly in order.

## Step 1: Install Python 3.11

If Python 3.11 is not installed yet:

1. download Python 3.11 from the official Python site
2. install it
3. check the box that adds Python to PATH

Then run:

```powershell
py -0p
```

You should see Python `3.11` listed.

## Step 2: Open the Project Folder

```powershell
cd "C:\Users\User\Desktop\personal\ai learning"
```

## Step 3: Create a Virtual Environment

```powershell
py -3.11 -m venv .venv
```

This creates an isolated Python environment for the project.

## Step 4: Activate the Virtual Environment

```powershell
.venv\Scripts\Activate.ps1
```

If activation works, your prompt should start with:

```text
(.venv)
```

## Step 5: Upgrade pip

```powershell
python -m pip install --upgrade pip
```

## Step 6: Install Backend Dependencies

```powershell
pip install -r backend/requirements.txt
```

This installs:

- FastAPI
- Chroma
- PDF parsing libraries
- HTTP client dependencies for talking to Ollama

## Step 7: Install Frontend Dependencies

```powershell
cd frontend
npm install
cd ..
```

## Step 8: Create the Backend Environment File

```powershell
Copy-Item .env.example backend/.env
```

This creates the backend config file.

## Step 9: Review the Backend Environment File

Open:

[backend/.env](<C:\Users\User\Desktop\personal\ai learning\backend\.env>)

You should see something like:

```text
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_CHAT_MODEL=qwen3:4b
OLLAMA_EMBED_MODEL=embeddinggemma
OLLAMA_TIMEOUT_SECONDS=120
FRONTEND_ORIGIN=http://localhost:3000
CHROMA_COLLECTION=coursework_chunks
```

For most users, you do not need to change anything.

## Step 10: Make Sure Ollama Is Running

Test Ollama:

```powershell
ollama --version
ollama list
```

Then test generation:

```powershell
ollama run qwen3:4b
```

Ask:

```text
Explain gradient descent simply.
```

Exit with:

```text
/bye
```

## Step 11: Start the Backend

Open a PowerShell window in the project folder, activate `.venv` if needed, then run:

```powershell
cd backend
uvicorn app.main:app --reload
```

If successful, the backend runs at:

[http://localhost:8000](http://localhost:8000)

Health check:

[http://localhost:8000/health](http://localhost:8000/health)

Expected response:

```json
{"status":"ok"}
```

## Step 12: Start the Frontend

Open a **second** PowerShell window.

Run:

```powershell
cd "C:\Users\User\Desktop\personal\ai learning"
cd frontend
npm run dev
```

The frontend should be at:

[http://localhost:3000](http://localhost:3000)

## Step 13: Test the Full App

1. open [http://localhost:3000](http://localhost:3000)
2. upload a small `pdf`, `txt`, or `md` file
3. wait for indexing to finish
4. ask a question about the uploaded material
5. check the answer and citations

### Good first test file

Use a small lecture note or a short PDF first.

Do not start with a giant textbook.

## What Is Happening Behind the Scenes

### When you upload a file

1. the frontend sends the file to the FastAPI backend
2. the backend saves the file in `data/raw/`
3. the backend extracts text from the file
4. the backend splits the text into chunks
5. the backend sends the chunk text to Ollama `/api/embed`
6. Ollama returns vector embeddings
7. the backend stores vectors and metadata in Chroma

### When you ask a question

1. the frontend sends the question to the backend
2. the backend sends the question to Ollama `/api/embed`
3. the backend finds similar chunks in Chroma
4. the backend builds a grounded prompt from those chunks
5. the backend sends that prompt to Ollama `/api/chat`
6. Ollama returns an answer
7. the backend returns the answer and citations to the frontend

That is the full local RAG flow.

## Files To Learn First

Study these files in order:

1. [backend/app/main.py](\backend\app\main.py)
2. [backend/app/api/routes/documents.py](\backend\app\api\routes\documents.py)
3. [backend/app/rag/parsers.py](\backend\app\rag\parsers.py)
4. [backend/app/rag/chunking.py](\backend\app\rag\chunking.py)
5. [backend/app/rag/embeddings.py](\backend\app\rag\embeddings.py)
6. [backend/app/rag/vector_store.py](\backend\app\rag\vector_store.py)
7. [backend/app/rag/retrieval.py](\backend\app\rag\retrieval.py)
8. [backend/app/services/llm.py](\backend\app\services\llm.py)
9. [backend/app/services/study_workflows.py](\backend\app\services\study_workflows.py)
10. [frontend/src/app/page.tsx](\frontend\src\app\page.tsx)

## Common Problems

### Problem: `py -3.11` does not work

Cause:

- Python 3.11 is not installed
- or the Python launcher cannot find it

Fix:

- install Python 3.11
- reopen PowerShell
- run `py -0p`

### Problem: PowerShell blocks `.ps1` activation

If you see:

```text
running scripts is disabled on this system
```

Run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then close and reopen PowerShell.

### Problem: `model '...' not found`

Cause:

- the Ollama model has not been downloaded yet

Fix:

```powershell
ollama pull qwen3:4b
ollama pull embeddinggemma
```

### Problem: backend cannot connect to Ollama

Cause:

- Ollama is not running
- or `OLLAMA_BASE_URL` is wrong

Fix:

1. run `ollama --version`
2. run `ollama list`
3. confirm `backend/.env` uses `http://localhost:11434`

### Problem: first indexing call is slow

This is normal.

The first request may need to load the model into memory.

### Problem: frontend cannot talk to backend

Cause:

- backend is not running
- frontend is not running
- ports are wrong

Fix:

- confirm backend health at [http://localhost:8000/health](http://localhost:8000/health)
- confirm frontend is running at [http://localhost:3000](http://localhost:3000)

## How To Know Phase 1 Is Really Done

Phase 1 is truly done when:

1. upload works
2. indexing works
3. question answering works
4. the answer is relevant
5. the citations point to sensible chunks or pages

Until then, treat Phase 1 as implemented but not fully verified.

## How To Know Phase 2 Is Really Done

Phase 2 is working well when:

1. all study modes return responses without crashing
2. summaries are structured and grounded in retrieved material
3. quizzes use the uploaded material instead of generic model knowledge
4. comparisons discuss both requested topics clearly
5. checklists are actionable for revision

## How To Know Phase 3 Is Really Done

Phase 3 is working when:

1. the auto-route mode chooses the correct workflow most of the time
2. compare-style requests are routed to compare
3. summary-style requests are routed to summarize
4. the UI clearly shows which workflow was selected
5. the fallback for unclear requests still works as grounded Q&A

## What Comes After Phase 3

After this, the next steps are:

1. improve routing quality and prompt quality
2. add one multimodal feature
3. add one PyTorch-trained component

## Official References

- [Ollama API introduction](https://docs.ollama.com/api/introduction)
- [Ollama chat API](https://docs.ollama.com/api/chat)
- [Ollama embed API](https://docs.ollama.com/api/embed)
- [Ollama embeddings guide](https://docs.ollama.com/capabilities/embeddings)
