import os
from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found.")
    loader = PyPDFLoader(file_path)
    return loader.load()
