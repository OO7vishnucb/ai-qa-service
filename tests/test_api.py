import pytest
from fastapi.testclient import TestClient
import os
os.environ["GEMINI_API_KEY"] = "fake"
os.environ["DATABASE_URL"] = "postgresql://fake:fake@localhost/fake"
from app.main import app
from app.services.retrieval import cosine_similarity
client = TestClient(app)
def test_health_check():
    assert client.get("/health").status_code == 200
def test_ingest_missing():
    assert client.post("/ingest", json={}).status_code == 422
def test_query_missing():
    assert client.post("/query", json={}).status_code == 422
def test_cosine():
    assert cosine_similarity([1.0,0.0],[1.0,0.0]) == pytest.approx(1.0)
