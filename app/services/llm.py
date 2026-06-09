from google import genai
from app.config import settings

client = genai.Client(api_key=settings.gemini_api_key)

async def generate_answer(question: str, context: list[str]) -> str:
    context_text = "\n\n".join(context)
    prompt = f"""Answer the question based only on the context below.
If the context does not contain the answer, say "I don't have enough information to answer that."

Context:
{context_text}

Question: {question}

Answer:"""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text

# Alias for backward compatibility
ask_gemini = generate_answer
