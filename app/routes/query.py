# routes/query.py
# Handles POST /query — answers a question using the stored knowledge base.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.database import get_db
from app.services.embeddings import get_query_embedding
from app.services.retrieval import retrieve_similar_documents
from app.services.llm import ask_gemini

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list[str]  # the retrieved context chunks, so the caller can see what was used


@router.post("/query", response_model=QueryResponse)
def query_knowledge_base(request: QueryRequest, db: Session = Depends(get_db)):
    """
    Full RAG pipeline:
    1. Embed the user's question.
    2. Find the top-3 most similar documents in PostgreSQL.
    3. Send question + those documents to Gemini.
    4. Return Gemini's answer alongside the source chunks.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # Step 1: embed the question
    query_embedding = get_query_embedding(request.question)

    # Step 2: retrieve relevant context from the database
    context_chunks = retrieve_similar_documents(query_embedding, db, top_k=3)

    # Step 3: ask Gemini
    answer = ask_gemini(request.question, context_chunks)

    return QueryResponse(
        question=request.question,
        answer=answer,
        sources=context_chunks,
    )
