from Ingestion import process_pdf_input, table_text_segregation, get_images
from summarizer import summarize_texts_tables, summarize_images
from VectorDB import add_documents_to_vector_db


def ingestion_chain(file_path, retriever):
    """
    Complete ingestion pipeline: PDF → extract → summarize → add to vector DB.
    """
    try:
        from ollama_running import ensure_ollama_running
        ensure_ollama_running()

        # Extract elements from PDF
        elements = process_pdf_input(file_path)
        print(f"✅ Extracted {len(elements)} elements from PDF.")

        # Segregate into tables, texts, images
        tables, texts = table_text_segregation(elements)
        images = get_images(elements)
        print(f"📄 Texts: {len(texts)}, 📊 Tables: {len(tables)}, 🖼️ Images: {len(images)}")

        # Summarize
        text_summaries, table_summaries = summarize_texts_tables(texts, tables)
        img_summaries = summarize_images(images)
        print(f"✅ Summarization complete.")

        # Add to vector DB
        add_documents_to_vector_db(
            texts, text_summaries, tables, table_summaries, images, img_summaries,
            retriever=retriever
        )
        print(f"✅ Documents added to vector database.")

        return True

    except Exception as e:
        print(f"❌ Error in ingestion pipeline: {str(e)}")
        raise RuntimeError(f"Ingestion failed: {str(e)}")