# services/retrieval.py
# Loads all documents from PostgreSQL and finds the most similar ones
# using cosine similarity calculated in Python — no pgvector needed.

import json
import math
from sqlalchemy.orm import Session
from app.db.models import Document


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """
    Calculates how similar two vectors are.
    Returns a value between -1 and 1 — higher means more similar.
    """
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def retrieve_similar_documents(query_embedding: list[float], db: Session, top_k: int = 3) -> list[str]:
    """
    Fetches all documents from the database, computes cosine similarity
    between each one and the query, and returns the top_k most relevant.
    """
    documents = db.query(Document).all()

    if not documents:
        return []

    # Score each document
    scored = []
    for doc in documents:
        doc_embedding = json.loads(doc.embedding)
        score = cosine_similarity(query_embedding, doc_embedding)
        scored.append((score, doc.content))

    # Sort by score descending and return top_k
    scored.sort(key=lambda x: x[0], reverse=True)
    return [content for _, content in scored[:top_k]]