# 🧠 KnowledgeGPT — RAG Chatbot with Conversational Memory

An AI-powered chatbot that answers questions from your own documents (PDF, TXT) 
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
5. Retrieved context + conversation history is passed to Gemini to generate a grounded, accurate answer

## ✨ Features
- Multi-source input: PDF, TXT, or web URL
- Context-aware answers grounded in your documents, not generic LLM output
- Remembers previous questions in the same session for natural follow-up conversations

## 🖥️ Run Locally
​```bash
git clone <your-repo-url>
cd KnowledgeGPT
pip install -r requirements.txt
streamlit run app.py
​``
