import os
import requests

def generate_rag_response(question: str, context: str):
    system_prompt = """You are Aura RAG.
Answer ONLY using the provided context.
If the answer isn't available, say "I don't know."
You MUST answer in 1 or 2 short sentences max.
NEVER explain your reasoning. NEVER use phrases like 'The user is asking' or 'Based on the context'.
Your first word MUST be the direct answer."""

    user_prompt = f"""Context:
{context}

Question: {question}"""

    headers = {
        "Authorization": "Bearer dahl_3Y6DwoV1mLW5MQacV1Q8JDiB2vtpNg4x2",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "MiniMaxAI/MiniMax-M2.7",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }
    
    try:
        response = requests.post("https://inference.dahl.global/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        raise Exception("Internal error occurred. Please try again later.") from e
