from google import genai
from app.config import settings

client = genai.Client(api_key=settings.gemini_api_key)

def get_embedding(text: str) -> list[float]:
    result = client.models.embed_content(
        model="models/gemini-embedding-001",
        contents=text,
    )
    return result.embeddings[0].values

# Alias so both ingest.py and query.py work
async def get_query_embedding(text: str) -> list[float]:
    return get_embedding(text)
