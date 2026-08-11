import os
import requests

def generate_rag_response(question: str, context: str):
    system_prompt = "You are a concise AI. Answer strictly using the context. If unknown, say 'I don't know.' DO NOT explain your reasoning. DO NOT think out loud. Output ONLY the final answer."

    user_prompt = f"Context:\n{context}\n\nQuestion: {question}"

    headers = {
        "Authorization": "Bearer dahl_3Y6DwoV1mLW5MQacV1Q8JDiB2vtpNg4x2",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "MiniMaxAI/MiniMax-M2.7",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Context:\nVishwajit is in Bengaluru.\n\nQuestion: Where is Vishwajit?"},
            {"role": "assistant", "content": "Vishwajit is in Bengaluru."},
            {"role": "user", "content": user_prompt}
        ]
    }
    
    try:
        response = requests.post("https://inference.dahl.global/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        raise Exception("Internal error occurred. Please try again later.") from e
