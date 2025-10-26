import streamlit as st
import os
from Ingestion import ingest_pdfs_to_vector_db
from App.Retrieval import answer_question

st.set_page_config(page_title="RAG Chatbot (Local)", layout="wide")

st.sidebar.title("RAG Chatbot (Local)")
st.sidebar.write("Upload PDFs and ask questions directly without FastAPI.")
st.sidebar.markdown("---")
st.sidebar.write("Developed by Amitoj Singh Chawla")

st.markdown("<h1 style='text-align:center;color:#4B8BBE;'>RAG Chatbot (Local)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:grey;'>Ask questions or upload PDFs to get answers</p>", unsafe_allow_html=True)
st.markdown("---")

TEMP_DIR = "../uploaded_pdfs"
os.makedirs(TEMP_DIR, exist_ok=True)

uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        save_path = os.path.join(TEMP_DIR, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success(f"✅ Uploaded: {uploaded_file.name}")

    with st.spinner("Ingesting all PDFs..."):
        try:
            ingest_pdfs_to_vector_db(os.path.abspath(TEMP_DIR))
            st.success("✅ Ingestion complete for all PDFs")
        except Exception as e:
            st.error(f"❌ Ingestion failed: {e}")

st.markdown("---")

question = st.text_input("Ask a question about your documents:")

if question:
    with st.spinner("Getting answer..."):
        try:
            answer = answer_question(question)
            if isinstance(answer, dict) and "answer" in answer:
                answer = answer["answer"]
            st.markdown(
                f"<div style='background-color:#E8EAF6; padding:10px; border-radius:10px; margin:5px 0; width:60%;'>"
                f"<b>Bot:</b> {answer}</div>",
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"❌ Failed to get answer: {e}")
