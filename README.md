# 🤖 RAG Chatbot with Conversational Memory

An AI-powered chatbot that answers questions from uploaded documents (PDF, TXT) 
or any webpage URL, using Retrieval-Augmented Generation (RAG) with conversational memory.

## 🔧 Tech Stack
- **Frontend/UI:** Streamlit
- **LLM:** Google Gemini
- **Framework:** LangChain
- **Vector Database:** ChromaDB
- **Memory:** LangChain Conversational Memory

## 🚀 How It Works
1. User uploads a document or enters a webpage URL
2. Content is loaded and split into chunks
3. Chunks are embedded and stored in ChromaDB as vectors
4. On each query, the most relevant chunks are retrieved via similarity search
5. Retrieved context + conversation history is passed to Gemini to generate a grounded answer

## ✨ Features
- Multi-source input: PDF, TXT, or web URL
- Context-aware answers (not generic LLM hallucination — grounded in your docs)
- Remembers previous questions in the same session for natural follow-ups

## 🖥️ Run Locally
​```bash
git clone <your-repo-url>
cd Intelligent-Chatbot-using-RAG
pip install -r requirements.txt
streamlit run app.py
​```

## 📌 My Contribution
Built as part of a group project. Worked on document loading and UI and gained hands-on understanding of 
the full RAG pipeline — from embedding generation to context-aware response generation.
