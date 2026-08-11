import os
from langchain_chroma import Chroma
from services.embeddings import get_embeddings

CHROMA_PATH = "chroma_db"

def get_vector_store():
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embeddings()
    )

def add_to_vector_store(chunks):
    vector_store = get_vector_store()
    try:
        vector_store.delete_collection()
    except Exception:
        pass
    
    # Re-initialize after deletion
    vector_store = get_vector_store()
    vector_store.add_documents(chunks)
    return vector_store
