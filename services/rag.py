from services.vector_store import get_vector_store

def retrieve_context(query: str, k: int = 5):
    vector_store = get_vector_store()
    results = vector_store.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in results])
