import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_rag_response(question: str, context: str):
    prompt = f"""You are Aura RAG.
Answer ONLY using the provided context.
If the answer isn't available, say you don't know.

Context:
{context}

Question: {question}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text.strip()
