import streamlit as st
import requests
import io

# Backend endpoint
FASTAPI_URL = "http://127.0.0.1:8000"

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

# Chat input
prompt = st.chat_input(
    placeholder="Type your message or upload PDF files",
    accept_file="multiple",
    file_type="pdf"
)

# --- Chat messages ---
if prompt is not None:
    # USER TEXT MESSAGE
    if getattr(prompt, "text", ""):
        user_msg = prompt.text
        with chat_container:
            st.markdown(
                f"<div style='background-color:#DCF8C6; padding:10px; border-radius:10px; margin:5px 0; width:60%;'>"
                f"<b>You:</b> {user_msg}</div>",
                unsafe_allow_html=True
            )

        # --- Send text query to FastAPI ---
        with st.spinner("Thinking..."):
            response = requests.post(f"{FASTAPI_URL}/ask", json={"query": user_msg})

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer received.")
            with chat_container:
                st.markdown(
                    f"<div style='background-color:#E8EAF6; padding:10px; border-radius:10px; margin:5px 0; width:60%;'>"
                    f"<b>Bot:</b> {answer}</div>",
                    unsafe_allow_html=True
                )
        else:
            with chat_container:
                st.markdown(
                    f"<div style='background-color:#FFCDD2; padding:10px; border-radius:10px; margin:5px 0; width:60%;'>"
                    f"<b>Error:</b> {response.text}</div>",
                    unsafe_allow_html=True
                )

    # USER FILE UPLOAD
    for uploaded_file in getattr(prompt, "files", []):
        with chat_container:
            st.markdown(
                f"<div style='background-color:#FFECB3; padding:10px; border-radius:10px; margin:5px 0; width:60%;'>"
                f"<b>Uploaded file:</b> {uploaded_file.name}</div>",
                unsafe_allow_html=True
            )

        # --- Send file(s) to FastAPI ---
        with st.spinner(f"Ingesting {uploaded_file.name}..."):
            files = [("files", (uploaded_file.name, uploaded_file.read(), "application/pdf"))]
            response = requests.post(f"{FASTAPI_URL}/ingest", files=files)

        if response.status_code == 200:
            with chat_container:
                st.markdown(
                    f"<div style='background-color:#C8E6C9; padding:10px; border-radius:10px; margin:5px 0; width:60%;'>"
                    f"✅ File {uploaded_file.name} ingested successfully.</div>",
                    unsafe_allow_html=True
                )
        else:
            with chat_container:
                st.markdown(
                    f"<div style='background-color:#FFCDD2; padding:10px; border-radius:10px; margin:5px 0; width:60%;'>"
                    f"❌ Error ingesting {uploaded_file.name}: {response.text}</div>",
                    unsafe_allow_html=True
                )
