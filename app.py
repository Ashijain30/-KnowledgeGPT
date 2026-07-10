import os
import streamlit as st
from dotenv import load_dotenv

# Fix SQLite
__import__("pysqlite3")
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

# Load env
load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    st.error("🚨 GOOGLE_API_KEY not found")
    st.stop()

# LangChain
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="KnowledgeGPT",
    page_icon="🧠",
    layout="centered"
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
.big-title {
    font-size: 40px;
    font-weight: 700;
    text-align: center;
}
.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 30px;
}
.chat-box {
    background-color: #f5f5f5;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown('<div class="big-title">🧠 KnowledgeGPT</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask anything from PDFs or Websites</div>', unsafe_allow_html=True)

# ------------------ SESSION ------------------
if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------ MODELS ------------------
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# ------------------ FUNCTIONS ------------------
def load_and_index(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(splits, embeddings)
    return vectorstore.as_retriever()

def build_chain(retriever):
    prompt = ChatPromptTemplate.from_template("""
    Answer ONLY using the context below:
    {context}

    Question: {input}
    """)

    doc_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, doc_chain)

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.header("📂 Add Knowledge")

    option = st.radio("Choose source:", ["PDF", "Website"])

    if option == "PDF":
        file = st.file_uploader("Upload PDF", type=["pdf"])
        if file:
            with open("temp.pdf", "wb") as f:
                f.write(file.read())

            with st.spinner("Reading PDF..."):
                loader = PyPDFLoader("temp.pdf")
                docs = loader.load()
                st.session_state.retriever = load_and_index(docs)

            st.success("✅ PDF Ready!")

    elif option == "Website":
        url = st.text_input("Enter URL")
        if st.button("Load Website"):
            with st.spinner("Fetching content..."):
                loader = WebBaseLoader(url)
                docs = loader.load()
                st.session_state.retriever = load_and_index(docs)

            st.success("✅ Website Ready!")

# ------------------ CHAT ------------------
st.divider()

user_input = st.chat_input("Ask something...")

if user_input:
    if not st.session_state.retriever:
        st.warning("⚠️ Please upload a PDF or URL first")
    else:
        chain = build_chain(st.session_state.retriever)

        with st.spinner("Thinking..."):
            response = chain.invoke({"input": user_input})
            answer = response["answer"]

        st.session_state.messages.append(("user", user_input))
        st.session_state.messages.append(("bot", answer))

# ------------------ DISPLAY CHAT ------------------
for role, msg in st.session_state.messages:
    if role == "user":
        st.chat_message("user").write(msg)
    else:
        st.chat_message("assistant").write(msg)