import os
import requests

def generate_rag_response(question: str, context: str):
    prompt = f"""You are Aura RAG.
Answer ONLY using the provided context.
If the answer isn't available, say you don't know strictly if the question is not related to the context provided or if the information is not present in the context provided - Do not answer or guess anything - Answer must be factual and based on context provided - No additional information.

Context:
{context}

Question: {question}
"""
    headers = {
        "Authorization": "Bearer dahl_3Y6DwoV1mLW5MQacV1Q8JDiB2vtpNg4x2",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "MiniMaxAI/MiniMax-M2.7",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        response = requests.post("https://inference.dahl.global/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error contacting fallback model: {str(e)}"
