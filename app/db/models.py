# db/models.py
# Stores embeddings as plain JSON text — no pgvector needed.

from sqlalchemy import Column, Integer, Text, DateTime, func
from app.db.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    embedding = Column(Text, nullable=False)  # stored as JSON string e.g. "[0.1, 0.2, ...]"
    created_at = Column(DateTime(timezone=True), server_default=func.now())