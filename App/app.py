import streamlit as st
import tempfile
import os
import shutil
import atexit
import uuid

from Ingestion_chain import ingestion_chain
from retrieval_chain import answer_question
from VectorDB import initialize_vector_db

# Page configuration
st.set_page_config(
    page_title="QueryDr: A Retrieval-Augmented Generation System for Intelligent Document-Based Question Answering",
    layout="wide",
)

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.temp_dir = os.path.join(
        tempfile.gettempdir(), f"streamlit_rag_session_{st.session_state.session_id}"
    )
    st.session_state.chroma_dir = os.path.join(
        st.session_state.temp_dir, "chroma_store"
    )
    st.session_state.messages = []
    st.session_state.files_uploaded = False
    st.session_state.retriever = None
    st.session_state.retriever = initialize_vector_db(st.session_state.chroma_dir)

    os.makedirs(st.session_state.temp_dir, exist_ok=True)
    os.makedirs(st.session_state.chroma_dir, exist_ok=True)


# Cleanup function
@atexit.register
def cleanup():
    if "session_id" in st.session_state and os.path.exists(st.session_state.temp_dir):
        try:
            shutil.rmtree(st.session_state.temp_dir)
        except Exception:
            pass


# Sidebar
with st.sidebar:
    st.title(
        "🤖 QueryDr: A Retrieval-Augmented Generation System for Intelligent Document-Based Question Answering"
    )
    st.markdown("---")
    st.markdown("### 📋 Instructions")
    st.markdown("""
    1. **Upload PDFs**: Use the file uploader below to upload one or more PDF documents.
    2. **Ask Questions**: Once uploaded, ask questions about your documents in the chat.
    3. **Get Answers**: The chatbot will retrieve relevant information and answer your questions.
    """)
    st.markdown("---")
    st.markdown("**Developed by Amitoj Singh Chawla**")
    st.markdown("---")

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or more PDF files to create your knowledge base",
    )

    if uploaded_files and not st.session_state.files_uploaded:
        if st.button("Process Files", type="primary", use_container_width=True):
            with st.spinner("Processing files..."):
                success_count = 0
                error_count = 0

                for uploaded_file in uploaded_files:
                    try:
                        file_path = os.path.join(
                            st.session_state.temp_dir, uploaded_file.name
                        )
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        ingestion_chain(file_path, st.session_state.retriever)
                        success_count += 1

                    except Exception as e:
                        error_count += 1
                        st.error(f"Error processing {uploaded_file.name}: {str(e)}")

                if success_count > 0:
                    st.success(f"✅ Successfully processed {success_count} file(s)!")
                    st.session_state.files_uploaded = True
                    st.session_state.messages.append(
                        {
                            "role": "system",
                            "content": f"Successfully processed {success_count} PDF file(s). You can now ask questions about your documents.",
                        }
                    )
                    st.rerun()

                if error_count > 0:
                    st.warning(f"⚠️ {error_count} file(s) failed to process.")

    if st.session_state.files_uploaded:
        st.success("✅ Files ready for queries")
        if st.button("Clear All & Reset", use_container_width=True):
            if os.path.exists(st.session_state.temp_dir):
                shutil.rmtree(st.session_state.temp_dir)
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# Main content
st.markdown(
    "<h1 style='text-align: center;'>🤖 QueryDr: A Retrieval-Augmented Generation System for Intelligent Document-Based Question Answering</h1>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Display chat messages
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]

        if role == "system":
            st.markdown(
                f"""<div style='background-color: #FFECB3; padding: 15px; border-radius: 10px; margin: 10px 0;'>
                <p style='margin: 0; color: #333;'><strong>ℹ️ System:</strong> {content}</p>
                </div>""",
                unsafe_allow_html=True,
            )
        elif role == "user":
            st.markdown(
                f"""<div style='background-color: #DCF8C6; padding: 15px; border-radius: 10px; margin: 10px 0; margin-left: 20%;'>
                <p style='margin: 0; color: #333;'><strong>You:</strong> {content}</p>
                </div>""",
                unsafe_allow_html=True,
            )
        elif role == "assistant":
            st.markdown(
                f"""<div style='background-color: #E8EAF6; padding: 15px; border-radius: 10px; margin: 10px 0; margin-right: 20%;'>
                <p style='margin: 0; color: #333;'><strong>🤖 Bot:</strong> {content}</p>
                </div>""",
                unsafe_allow_html=True,
            )

# Chat input
if st.session_state.files_uploaded:
    user_query = st.chat_input("Ask a question about your documents...")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})

        try:
            with st.spinner("Thinking..."):
                answer = answer_question(user_query, st.session_state.retriever)

            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            error_message = f"Sorry, I encountered an error: {str(e)}"
            st.session_state.messages.append(
                {"role": "assistant", "content": error_message}
            )

        st.rerun()
else:
    st.info(
        "👆 Please upload and process PDF files from the sidebar to start chatting."
    )
