from .Ingestion import process_pdfs_in_directory, table_text_segregation, get_images
import os
from summarizer import summarize_texts_tables, summarize_images
from .VectorDB import add_documents_to_vector_db
from .Retrieval import answer_question


if __name__ == "__main__":
    # Example usage
    uploaded_files =os.getenv("DATA_PATH") # Directory containing uploaded PDFs
    elements = process_pdfs_in_directory(uploaded_files)
    tables, texts = table_text_segregation(elements)
    images64 = get_images(elements)

    print(f"Processed {len(elements)} elements.")
    print(f"Found {len(tables)} tables, {len(texts)} text blocks, and {len(images64)} images.")

    # Summarize texts and tables
    text_summaries, table_summaries = summarize_texts_tables(texts, tables)
    print("Text and table summarization complete.")

    # Summarize images
    img_summaries = summarize_images(images64)
    print("Image summarization complete.")

    # Add documents and their summaries to the vector database
    add_documents_to_vector_db(texts, text_summaries, tables, table_summaries, images64, img_summaries)
    print("Documents and summaries added to vector database.")

    # Done
    print("Ingestion and summarization process completed successfully.")

    print("Answering question...")

    # Example question
    question = "What is the main topic of the documents?"
    answer = answer_question(question)
    print(f"Q: {question}\nA: {answer}")
