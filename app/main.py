from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.database import init_db
from app.routes import ingest, query

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="AI Q&A Service",
    description="A RAG-based question answering API powered by Gemini and PostgreSQL.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(ingest.router)
app.include_router(query.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}