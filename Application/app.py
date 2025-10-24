import streamlit as st

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
    # User message
    if getattr(prompt, "text", ""):
        with chat_container:
            st.markdown(
                f"<div style='background-color:#DCF8C6; padding:10px; border-radius:10px; margin:5px 0; width:60%;'>"
                f"<b>You:</b> {prompt.text}</div>",
                unsafe_allow_html=True
            )

    # Uploaded files
    for uploaded_file in getattr(prompt, "files", []):
        with chat_container:
            st.markdown(
                f"<div style='background-color:#FFECB3; padding:10px; border-radius:10px; margin:5px 0; width:60%;'>"
                f"<b>Uploaded file:</b> {uploaded_file.name}</div>",
                unsafe_allow_html=True
            )

    # Assistant response placeholder
    with chat_container:
        response_placeholder = st.empty()