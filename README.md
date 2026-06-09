# AI Q&A Service

A RAG (Retrieval-Augmented Generation) API built with FastAPI, Google Gemini, and PostgreSQL + pgvector.

## How it works

1. **Ingest** — POST text documents to `/ingest`. The service converts them to embeddings and stores them in PostgreSQL.
2. **Query** — POST a question to `/query`. The service finds the most relevant stored documents and asks Gemini to answer based on them.

---

## Prerequisites

- Python 3.10+
- PostgreSQL 15+ with the [pgvector](https://github.com/pgvector/pgvector) extension
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

---

## Local Setup

### 1. Clone and install dependencies

```bash
git clone <your-repo-url>
cd my_ai_service
pip install -r requirements.txt
```

### 2. Set up PostgreSQL with pgvector

Install pgvector ([instructions](https://github.com/pgvector/pgvector#installation)), then create the database:

```sql
CREATE DATABASE ai_service;
```

The app enables the `vector` extension automatically on startup.

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

```
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/ai_service
```

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

The API is now running at `http://localhost:8000`.
Visit `http://localhost:8000/docs` for the interactive Swagger UI.

---

## API Reference

### `POST /ingest`

Add a document to the knowledge base.

**Request body:**
```json
{ "text": "FastAPI is a modern Python web framework for building APIs." }
```

**Response:**
```json
{ "id": 1, "message": "Document ingested successfully." }
```

---

### `POST /query`

Ask a question answered from the knowledge base.

**Request body:**
```json
{ "question": "What is FastAPI?" }
```

**Response:**
```json
{
  "question": "What is FastAPI?",
  "answer": "FastAPI is a modern Python web framework for building APIs.",
  "sources": ["FastAPI is a modern Python web framework for building APIs."]
}
```

---

### `GET /health`

Returns `{ "status": "ok" }` if the service is running.

---

## Deployment

### Deploy to Render (free tier)

1. Push your code to a GitHub repository.
2. Go to [render.com](https://render.com) and create a new **Web Service**.
3. Connect your GitHub repo.
4. Set the **Start Command** to: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
5. Add environment variables (`GEMINI_API_KEY`, `DATABASE_URL`) under the Environment tab.
6. For the database, create a **PostgreSQL** instance on Render and enable pgvector via the console:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

---

## Project Structure

```
my_ai_service/
├── app/
│   ├── main.py              # FastAPI app + startup
│   ├── config.py            # Loads environment variables
│   ├── routes/
│   │   ├── ingest.py        # POST /ingest
│   │   └── query.py         # POST /query
│   ├── services/
│   │   ├── embeddings.py    # Gemini embedding generation
│   │   ├── retrieval.py     # pgvector similarity search
│   │   └── llm.py           # Gemini Q&A
│   └── db/
│       ├── database.py      # SQLAlchemy engine + session
│       └── models.py        # Document table definition
├── .env.example
├── requirements.txt
└── README.md
```
