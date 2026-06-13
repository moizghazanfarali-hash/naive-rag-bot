import os
import shutil
import logging
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.config import settings
from app.retrieve import retrieve_context
from app.llm import get_llm
from app.database import get_vector_store

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="Production Naive RAG API", version="1.0")

# CORS setup for Frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.get("/health")
def health_check():
    return {"status": "healthy", "model": settings.GROQ_MODEL_NAME}


# ================= INGESTION ROUTE =================
@app.post("/api/ingest")
async def ingest_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Received file for ingestion: {file.filename}")
        
        # 1. Temporarily file ko 'data/' folder me save karna
        DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
        os.makedirs(DATA_DIR, exist_ok=True)
        
        file_path = os.path.join(DATA_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 2. File type check karke sahi loader select karna (.txt ya .pdf)
        if file.filename.endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")
        elif file.filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            os.remove(file_path) # Unsupported file delete karna
            raise HTTPException(status_code=400, detail="Only .txt and .pdf files are supported.")
            
        documents = loader.load()
        
        # 3. Text ko chunks me split karna
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=60)
        chunks = text_splitter.split_documents(documents)
        
        if not chunks:
            raise HTTPException(status_code=400, detail="File is empty or could not be parsed.")
            
        # 4. ChromaDB me store karna (Jina Embeddings automatically use hongi)
        vector_store = get_vector_store()
        vector_store.add_documents(chunks)
        
        logger.info(f"Successfully indexed {len(chunks)} chunks from {file.filename}")
        
        return {
            "success": True,
            "message": f"File '{file.filename}' uploaded and indexed successfully into ChromaDB!",
            "chunks_created": len(chunks)
        }
        
    except Exception as e:
        logger.error(f"Error during file ingestion endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


# ================= CHAT/QUERY ROUTE =================
@app.post("/api/chat")
async def chat_with_rag(payload: QueryRequest):
    try:
        user_question = payload.question
        if not user_question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty.")

        context = retrieve_context(user_question, k=3)
        
        if not context:
            logger.warning("No relevant context found in database.")
            context = "No specific context found in database. Answer using general knowledge."

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Answer the user's question using ONLY the provided context below. If you don't know the answer or if it's not in the context, say that you don't know based on the documents.\n\nContext:\n{context}"),
            ("user", "{question}")
        ])

        llm = get_llm()
        chain = prompt_template | llm
        
        logger.info("Sending prompt to Groq API...")
        response = chain.invoke({"context": context, "question": user_question})
        
        return {
            "answer": response.content,
            "success": True
        }

    except Exception as e:
        logger.error(f"Error in /api/chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")