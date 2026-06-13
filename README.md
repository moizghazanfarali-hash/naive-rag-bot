# 🤖 Naive RAG Bot

This is an AI-powered Chatbot that can read your documents and answer questions based on them. It has a beautiful user interface (Frontend) and a smart AI brain (Backend).

---

## 📁 What's Inside?

*   **`naive-rag-frontend/`**: The visual website where users type and chat with the AI.
*   **`naive-rag-backend/`**: The AI brain that connects to the database and processes your files.

---

## 🚀 How to Run the Project (Quick Setup)

### Step 1: Set up the AI Brain (Backend)
1. Open your terminal and go to the backend folder:
```bash
   cd naive-rag-backend
Create a .env file in this folder and add your OpenAI Key:

Plaintext
   OPENAI_API_KEY=your_actual_api_key_here
Install the required tools and start the backend server:

Bash
   pip install -r requirements.txt
   uvicorn app.main:app --reload
Step 2: Set up the Website (Frontend)
Open a new terminal and go to the frontend folder:

Bash
   cd naive-rag-frontend
Install the website design files and start the website:

Bash
   npm install
   npm run dev
Open the link shown in your terminal (usually http://localhost:5173) in your browser to start chatting!

🐳 Docker Support
Both frontend and backend include a Dockerfile, making it easy to package and run this application inside containers anywhere!
