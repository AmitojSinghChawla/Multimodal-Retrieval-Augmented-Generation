import uuid
from langchain_chroma import Chroma
from langchain_core.stores import InMemoryStore
from langchain_core.documents import Document
from langchain_classic.retrievers import MultiVectorRetriever
from langchain_huggingface import HuggingFaceEmbeddings


def initialize_vector_db(persist_directory="./chroma_store"):
    """
    Initialize the vector database and multi-vector retriever.
    """
    embedding_model = HuggingFaceEmbeddings(
        model="BAAI/bge-small-en-v1.5",
        model_kwargs={"device": "cpu"}
    )

    vectorstore = Chroma(
        collection_name="multi_modal_rag",
        embedding_function=embedding_model,
        persist_directory=persist_directory
    )

    store = InMemoryStore()
    id_key = "doc_id"

    multi_retriever = MultiVectorRetriever(
        vectorstore=vectorstore,
        docstore=store,
        id_key=id_key,
    )

    return multi_retriever


def add_documents_to_vector_db(
        texts, text_summaries, tables, table_summaries, images, img_summaries,
        retriever, id_key="doc_id"
):
    """
    Adds original documents and their summaries to the multi-vector retriever.
    """

    # --- SAFETY WRAPPER (fixes .strip() crash) ---
    def _safe_string(x):
        if isinstance(x, str):
            return x
        if hasattr(x, "content"):   # AIMessage or LC Message
            return x.content
        return str(x)

    def process_and_add(elements, summaries, label):
        docs, pairs = [], []
        for elem, summary in zip(elements, summaries):

            summary = _safe_string(summary)  # <-- REQUIRED FIX

            if summary and summary.strip():
                uid = str(uuid.uuid4())
                docs.append(Document(page_content=summary.strip(), metadata={id_key: uid}))
                pairs.append((uid, elem))

        if docs:
            retriever.vectorstore.add_documents(docs)
            retriever.docstore.mset(pairs)
            print(f"✅ Added {len(docs)} {label} summaries.")
        else:
            print(f"⚠️ No {label} summaries to add.")

    process_and_add(texts, text_summaries, "text")
    process_and_add(tables, table_summaries, "table")
    process_and_add(images, img_summaries, "image")


def retrieve_documents(retriever, question, k=3):
    """
    Retrieve documents from vector database.
    """
    docs = retriever.invoke(question, kw_args={"k": k})
    return docs


def delete_vector_db(persist_directory):
    """
    Delete the vector database directory.
    """
    import shutil
    import os
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)
        print(f"🗑️ Deleted vector database at {persist_directory}")