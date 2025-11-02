import os
import sys
# from App.ollama_running import ensure_ollama_running
#
import streamlit as st


# Add parent directory to Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# # Ensure Ollama is running
# ensure_ollama_running()


import shutil
import tempfile

# Create a temp directory for file uploads
TEMP_DIR = os.path.join(tempfile.gettempdir(), "streamlit_ingestion_temp")
os.makedirs(TEMP_DIR, exist_ok=True)



from App.retrieval_chain import answer_question
from App.Ingestion_chain import ingestion_chain

# Page config
st.set_page_config(
    page_title="RAG Chatbot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar ---
st.sidebar.title("RAG Chatbot")
st.sidebar.write("""
Welcome to the **Retrieval Augmented Generation** app.
- Type your query or upload PDF files.
- Explore and interact with documents intelligently.
""")
st.sidebar.markdown("---")
st.sidebar.write("Developed by Amitoj Singh Chawla")

# --- Header ---
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>RAG Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>Ask questions or upload PDFs to get answers</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Chat container ---
st.write("### Chat")
chat_container = st.container()

# --- Chat Input and File Upload ---
col1, col2 = st.columns([5, 1])

with col1:
    user_msg = st.chat_input("Type your message...")

with col2:
    uploaded_files = st.file_uploader(
        "",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )


# --- Handle File Uploads ---
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(TEMP_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        with chat_container:
            st.markdown(
                f"<div style='background-color:#FFECB3; padding:10px; border-radius:10px; margin:5px 0; width:60%;'>"
                f"<b>Uploaded file:</b> {uploaded_file.name}</div>",
                unsafe_allow_html=True
            )

        with st.spinner(f"Ingesting {uploaded_file.name}..."):
            try:
                response = ingestion_chain(file_path)
                color = "#C8E6C9" if "Successfully" in response else "#FFCDD2"
                with chat_container:
                    st.markdown(
                        f"<div style='background-color:{color}; padding:10px; border-radius:10px; margin:5px 0; width:60%;'>"
                        f"{response}</div>",
                        unsafe_allow_html=True
                    )
            except Exception as e:
                with chat_container:
                    st.markdown(
                        f"<div style='background-color:#FFCDD2; padding:10px; border-radius:10px; margin:5px 0; width:60%;'>"
                        f"❌ Unexpected error: {str(e)}</div>",
                        unsafe_allow_html=True
                    )
if user_msg:
    with chat_container:
        st.markdown(
            f"<div style='background-color:#DCF8C6; padding:10px; border-radius:10px; margin:5px 0; width:60%;'>"
            f"<b>You:</b> {user_msg}</div>",
            unsafe_allow_html=True
        )

    with st.spinner("Thinking..."):
        answer = answer_question(user_msg)

    if isinstance(answer, dict) and "answer" in answer:
        answer = answer["answer"]

    with chat_container:
        st.markdown(
            f"<div style='background-color:#E8EAF6; padding:10px; border-radius:10px; margin:5px 0; width:60%;'>"
            f"<b>Bot:</b> {answer}</div>",
            unsafe_allow_html=True
        )

import atexit

@atexit.register
def cleanup_temp_dir():
    """Remove temporary ingestion directory on app shutdown."""
    try:
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR, ignore_errors=True)
            print(f"[INFO] Cleaned up temp directory: {TEMP_DIR}")
    except Exception as e:
        print(f"[WARN] Failed to delete temp directory: {e}")
