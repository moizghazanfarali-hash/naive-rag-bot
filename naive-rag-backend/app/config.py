import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GROQ_API_KEY: str
    JINA_API_KEY: str
    
    # Chroma DB Settings
    CHROMA_PERSIST_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
    
    # Model Configurations (Updated to supported models)
    GROQ_MODEL_NAME: str = "llama-3.1-8b-instant"  # Yeh boht fast aur updated model hai
    JINA_EMBEDDING_MODEL: str = "jina-embeddings-v2-base-en"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Global settings instance
settings = Settings()