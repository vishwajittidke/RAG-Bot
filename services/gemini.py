import os
import requests

def generate_rag_response(question: str, context: str):
    system_prompt = """You are Aura RAG.
Answer ONLY using the provided context.
If the answer isn't available, say "I don't know."
You MUST answer in 1 or 2 short sentences max.
You MUST output your final answer prefixed with exactly 'ANSWER:'."""

    user_prompt = f"""Context:
{context}

Question: {question}

Format your response exactly like this, with any reasoning placed BEFORE the answer:
[Your reasoning here if needed]
ANSWER: [Your short, direct 1-sentence answer here]"""

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
        if "ANSWER:" in text:
            text = text.split("ANSWER:")[-1].strip()
        return text
    except Exception as e:
        raise Exception("Internal error occurred. Please try again later.") from e
