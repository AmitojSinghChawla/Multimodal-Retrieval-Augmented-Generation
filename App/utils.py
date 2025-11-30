import os
import tempfile
import shutil


def create_temp_directory(session_id):
    """
    Create a temporary directory for the session.
    """
    temp_dir = os.path.join(tempfile.gettempdir(), f"streamlit_rag_session_{session_id}")
    chroma_dir = os.path.join(temp_dir, "chroma_store")

    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(chroma_dir, exist_ok=True)

    return temp_dir, chroma_dir


def cleanup_temp_directory(temp_dir):
    """
    Delete the temporary directory.
    """
    if os.path.exists(temp_dir):
        try:
            shutil.rmtree(temp_dir)
            print(f"🗑️ Cleaned up temporary directory: {temp_dir}")
        except Exception as e:
            print(f"⚠️ Could not clean up {temp_dir}: {str(e)}")