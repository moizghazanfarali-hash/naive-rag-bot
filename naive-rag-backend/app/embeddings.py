import logging
from langchain_community.embeddings import JinaEmbeddings
from app.config import settings

logger = logging.getLogger("uvicorn.error")

def get_embedding_model():
    """
    Returns the initialized Jina AI embedding model.
    """
    try:
        if not settings.JINA_API_KEY:
            raise ValueError("Jina API Key is missing in configuration.")
            
        embeddings = JinaEmbeddings(
            jina_api_key=settings.JINA_API_KEY,
            model_name=settings.JINA_EMBEDDING_MODEL
        )
        logger.info("Jina Embeddings model initialized successfully.")
        return embeddings
        
    except Exception as e:
        logger.error(f"Error initializing Jina Embeddings: {str(e)}")
        raise e