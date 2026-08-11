import os
import asyncio
from pathlib import Path
import shutil

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

from services.loader import load_pdf
from services.splitter import split_documents
from services.vector_store import add_to_vector_store
from services.rag import retrieve_context
from services.gemini import generate_rag_response

# ------------------------
# Load Environment
# ------------------------

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# ------------------------
# FastAPI
# ------------------------

app = FastAPI(title="Aura RAG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ------------------------
# Request Model
# ------------------------

class Query(BaseModel):
    question: str

# ------------------------
# Frontend
# ------------------------

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

# ------------------------
# Endpoints
# ------------------------

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        docs = load_pdf(file_path)
        chunks = split_documents(docs)
        add_to_vector_store(chunks)
        return {"success": True, "message": f"Document '{file.filename}' uploaded and indexed successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat(q: Query):
    try:
        await asyncio.sleep(1)
        
        context = retrieve_context(q.question)
        response_text = generate_rag_response(q.question, context)
        
        if not response_text:
            response_text = "Gemini returned an empty response."

        return {
            "success": True,
            "sender": "bot",
            "text": response_text
        }
    except Exception as e:
        return {
            "success": False,
            "sender": "bot",
            "text": f"Error: {str(e)}"
        }

# ------------------------
# Run
# ------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )