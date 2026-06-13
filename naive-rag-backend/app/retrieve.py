import logging
from app.database import get_vector_store

logger = logging.getLogger("uvicorn.error")

def retrieve_context(query: str, k: int = 3):
    """
    Takes a user query, searches ChromaDB, and returns the top 'k' relevant document chunks.
    """
    try:
        vector_store = get_vector_store()
        
        # Similarity search matching the query vector with stored vectors
        logger.info(f"Retrieving top {k} relevant chunks for query: '{query}'")
        docs = vector_store.similarity_search(query, k=k)
        
        # Saare matching chunks ko aik single text string me combine karna
        context = "\n\n".join([doc.page_content for doc in docs])
        return context
        
    except Exception as e:
        logger.error(f"Error during retrieval: {str(e)}")
        return ""