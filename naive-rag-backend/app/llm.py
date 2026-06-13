import logging
from langchain_groq import ChatGroq
from app.config import settings

logger = logging.getLogger("uvicorn.error")

def get_llm():
    """
    Returns the initialized Groq LLM instance.
    """
    try:
        if not settings.GROQ_API_KEY:
            raise ValueError("Groq API Key is missing in configuration.")
            
        llm = ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            model_name=settings.GROQ_MODEL_NAME,
            temperature=0.2, # Low temperature for factual RAG responses
        )
        logger.info(f"Groq LLM ({settings.GROQ_MODEL_NAME}) initialized successfully.")
        return llm
        
    except Exception as e:
        logger.error(f"Error initializing Groq LLM: {str(e)}")
        raise e