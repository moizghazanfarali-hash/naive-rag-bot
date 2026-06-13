import logging
import chromadb
from langchain_community.vectorstores import Chroma
from app.config import settings
from app.embeddings import get_embedding_model

logger = logging.getLogger("uvicorn.error")

def get_vector_store():
    """
    Initializes and returns the Chroma Vector Store instance.
    """
    try:
        embedding_model = get_embedding_model()
        
        # Ensure persistent directory exists and initialize Chroma
        vector_store = Chroma(
            persist_directory=settings.CHROMA_PERSIST_DIR,
            embedding_function=embedding_model,
            collection_name="naive_rag_collection"
        )
        logger.info(f"ChromaDB connected successfully at: {settings.CHROMA_PERSIST_DIR}")
        return vector_store
        
    except Exception as e:
        logger.error(f"Error connecting to ChromaDB: {str(e)}")
        raise e