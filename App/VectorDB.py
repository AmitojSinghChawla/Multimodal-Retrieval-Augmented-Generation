import uuid
from langchain_chroma import Chroma
from langchain_core.stores import InMemoryStore
from langchain_core.documents import Document
from langchain_classic.retrievers import MultiVectorRetriever
import torch
from langchain_huggingface import HuggingFaceEmbeddings

# The vectorstore to use to index the child chunks

embedding_model=HuggingFaceEmbeddings(model="BAAI/bge-small-en-v1.5",model_kwargs={"device":"cuda" if torch.cuda.is_available() else "cpu"})
vectorstore = Chroma(collection_name="multi_modal_rag", embedding_function=embedding_model)

# The storage layer for the parent documents
store = InMemoryStore()
id_key = "doc_id"

# The retriever (empty to start)
multi_retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    docstore=store,
    id_key=id_key,
)

def add_documents_to_vector_db(texts, text_summaries, tables, table_summaries, images, img_summaries): # Function to add documents and their summaries to the vector database

    import uuid
    from langchain_core.documents import Document

    # Loops over each text item in the extracted texts and creates a unique ID for each
    doc_ids = [str(uuid.uuid4()) for _ in texts]

    # Create a list of LangChain Document objects for text summaries
    summary_texts = [
        Document(page_content=summary, metadata={id_key: doc_ids[i]})
        for i, summary in enumerate(text_summaries)
        if summary and summary.strip()
    ]

    # Add text summaries to vectorstore
    if summary_texts:
        multi_retriever.vectorstore.add_documents(summary_texts)
    else:
        print("No text summaries to add.")

    # Store original texts in the docstore with their corresponding unique IDs
    multi_retriever.docstore.mset(list(zip(doc_ids, texts)))

    # Add table summaries
    table_ids = [str(uuid.uuid4()) for _ in tables]
    summary_tables = [
        Document(page_content=summary, metadata={id_key: table_ids[i]})
        for i, summary in enumerate(table_summaries)
        if summary and summary.strip()
    ]

    if summary_tables:
        multi_retriever.vectorstore.add_documents(summary_tables)
        multi_retriever.docstore.mset(list(zip(table_ids, tables)))
    else:
        print("No table summaries to add.")

    # Add image summaries
    img_ids = [str(uuid.uuid4()) for _ in images]
    summary_img = [
        Document(page_content=summary, metadata={id_key: img_id})
        for img_id, summary in zip(img_ids, img_summaries)
        if summary and summary.strip()
    ]

    if summary_img:
        multi_retriever.vectorstore.add_documents(summary_img)
        multi_retriever.docstore.mset(list(zip(img_ids, images)))
    else:
        print("No image summaries to add.")

