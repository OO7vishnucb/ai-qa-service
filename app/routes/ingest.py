# routes/ingest.py
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.database import get_db
from app.db.models import Document
from app.services.embeddings import get_embedding

router = APIRouter()


class IngestRequest(BaseModel):
    text: str


class IngestResponse(BaseModel):
    id: int
    message: str


@router.post("/ingest", response_model=IngestResponse)
def ingest_document(request: IngestRequest, db: Session = Depends(get_db)):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    embedding = get_embedding(request.text)

    # Store embedding as JSON string since we're not using pgvector
    doc = Document(content=request.text, embedding=json.dumps(embedding))
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return IngestResponse(id=doc.id, message="Document ingested successfully.")