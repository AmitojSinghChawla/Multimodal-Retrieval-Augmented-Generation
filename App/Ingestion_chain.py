<<<<<<< HEAD
def ingestion_chain(file_path, retriever):
    from Ingestion import process_pdf_input, table_text_segregation, get_images
    from summarizer import summarize_texts_tables, summarize_images
    from VectorDB import add_documents_to_vector_db
=======
from Ingestion import process_pdf_input, table_text_segregation, get_images
from summarizer import summarize_texts_tables, summarize_images
from VectorDB import add_documents_to_vector_db


def ingestion_chain(file_path, retriever):
>>>>>>> 196e6167f54456da83b27d8dcf9ad4415b4e71d9
    """
    Complete ingestion pipeline: PDF → extract → summarize → add to vector DB.
    """
    try:
<<<<<<< HEAD

        from App.ollama_running import ensure_ollama_running
        ensure_ollama_running()


=======
>>>>>>> 196e6167f54456da83b27d8dcf9ad4415b4e71d9
        # Extract elements from PDF
        elements = process_pdf_input(file_path)
        print(f"✅ Extracted {len(elements)} elements from PDF.")

        # Segregate into tables, texts, images
        tables, texts = table_text_segregation(elements)
        images = get_images(elements)
        print(f"📄 Texts: {len(texts)}, 📊 Tables: {len(tables)}, 🖼️ Images: {len(images)}")

        # Summarize
        table_summaries, text_summaries = summarize_texts_tables(texts, tables)
        img_summaries = summarize_images(images)
        print(f"✅ Summarization complete.")

<<<<<<< HEAD

=======
>>>>>>> 196e6167f54456da83b27d8dcf9ad4415b4e71d9
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