import os
import requests
import re

def generate_rag_response(question: str, context: str):
    system_prompt = "You are a concise AI. Answer strictly using the context. If unknown, say 'I don't know.' DO NOT explain your reasoning. Output ONLY the final answer in 1 or 2 sentences max."

    user_prompt = f"Context:\n{context}\n\nQuestion: {question}"

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
        text = response.json()["choices"][0]["message"]["content"].strip()
        
        # Physically remove any <think> reasoning blocks
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
        
        return text
    except Exception as e:
        raise Exception("Internal error occurred. Please try again later.") from e
