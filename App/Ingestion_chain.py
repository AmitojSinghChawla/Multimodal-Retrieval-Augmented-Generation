from App.Ingestion import ingest,process
from App.VectorDB import add_documents_to_vector_db


def ingestion_chain(uploaded_files):
    """
    Complete ingestion chain: ingest files, process them, and add to vector DB.
    """
    try:
        # Ingest files to get segregated elements
        tables, texts, images64 = ingest(uploaded_files)

        # Process elements to get summaries
        table_summaries, text_summaries, img_summaries = process(tables, texts, images64)

        # Add documents and their summaries to the vector database
        add_documents_to_vector_db(texts, text_summaries, tables, table_summaries, images64, img_summaries)

        return f"Successfully ingested {len(texts)} texts, {len(tables)} tables, and {len(images64)} images."

    except Exception as e:
        raise RuntimeError(f"Ingestion chain failed: {str(e)}")