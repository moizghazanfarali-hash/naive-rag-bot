import os
import sys
import logging

# Task ko smooth chalane ke liye project root ko path me add karna
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.database import get_vector_store
from langchain_community.document_loaders import PyPDFLoader

# Setup temporary logging for standalone script execution
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ingest")
logger.info("Loading documents...")
txt_loader = DirectoryLoader(DATA_DIR, glob="*.txt", loader_cls=TextLoader)
txt_docs = txt_loader.load()
    
    # PDF files load karne ke liye
pdf_loader = DirectoryLoader(DATA_DIR, glob="*.pdf", loader_cls=PyPDFLoader)
pdf_docs = pdf_loader.load()
    
    # Dono ko combine karna
documents = txt_docs + pdf_docs
logger.info(f"Loaded {len(documents)} total documents from raw storage.")

def run_ingestion():
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    
    if not os.path.exists(DATA_DIR) or not os.listdir(DATA_DIR):
        logger.warning(f"Data directory '{DATA_DIR}' is empty or does not exist. Please add some .txt files.")
        return

    logger.info("Starting document ingestion pipeline...")
    
    # 1. Load Documents
    loader = DirectoryLoader(DATA_DIR, glob="*.txt", loader_cls=TextLoader)
    documents = loader.load()
    logger.info(f"Loaded {len(documents)} documents from raw storage.")

    # 2. Split Text into Chunks (Naive RAG standard settings)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=60
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Split documents into {len(chunks)} distinct chunks.")

    # 3. Embed and Store into ChromaDB
    vector_store = get_vector_store()
    logger.info("Generating Jina Embeddings and saving chunks to ChromaDB...")
    vector_store.add_documents(chunks)
    
    logger.info("🚀 Ingestion successfully completed! Your data is indexed.")

if __name__ == "__main__":
    run_ingestion()