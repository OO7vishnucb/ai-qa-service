# services/llm.py
from google import genai
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def ask_gemini(question: str, context_chunks: list[str]) -> str:
    if not context_chunks:
        return "I couldn't find any relevant information in the knowledge base."

    context = "\n\n---\n\n".join(context_chunks)

    prompt = f"""You are a helpful assistant. Answer the user's question using ONLY the context provided below.
If the answer is not contained in the context, say "I don't have enough information to answer that."

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:"""

    response = client.models.generate_content(
    model="models/gemini-2.5-flash-lite",
        contents=prompt,
    )
    return response.text