# testset_ingestion.py

import os
from langchain_core.documents import Document

# Ingestion + Summarization imports
from App.Ingestion import (
    process_pdf_input,
    table_text_segregation,
    get_images
)
from App.summarizer import (
    summarize_texts_tables,
    summarize_images
)

# RAGAS imports
from ragas.testset import TestsetGenerator
from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI
from ragas.embeddings import OpenAIEmbeddings
import openai


# -----------------------------
# 1. Convert Summaries → LC Docs
# -----------------------------
def summaries_to_docs(text_summaries, table_summaries, img_summaries):
    """Convert all summary types into LangChain Document objects."""
    docs = []

    for s in text_summaries:
        docs.append(Document(page_content=s, metadata={"type": "text"}))

    for s in table_summaries:
        docs.append(Document(page_content=s, metadata={"type": "table"}))

    for s in img_summaries:
        docs.append(Document(page_content=s, metadata={"type": "image"}))

    return docs


# ------------------------------------
# 2. Ingestion Pipeline (For Testset)
# ------------------------------------
def ingestion_chain_for_testset_generation(file_path):
    """
    PDF → Extract elements → Summaries → Convert to LC Docs
    This function does NOT push anything to vector DB.
    Only produces RAGAS-ready documents.
    """
    # Extract raw elements
    elements = process_pdf_input(file_path)

    # Separate modalities
    tables, texts = table_text_segregation(elements)
    images = get_images(elements)

    # Summaries
    table_summaries, text_summaries = summarize_texts_tables(texts, tables)
    img_summaries = summarize_images(images)

    # Convert into LangChain documents
    return summaries_to_docs(text_summaries, table_summaries, img_summaries)


# -----------------------------
# 3. RAGAS Testset Generation
# -----------------------------
def generate_testset(input_pdf_path, output_csv="testset.csv", testset_size=20):
    """End-to-end pipeline: summaries → docs → ragas testset → CSV."""

    # Load summaries as LC documents
    docs = ingestion_chain_for_testset_generation(input_pdf_path)

    # Init LLM + Embeddings for RAGAS
    generator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o-mini"))
    openai_client = openai.OpenAI()
    generator_embeddings = OpenAIEmbeddings(client=openai_client)

    # Generate testset
    generator = TestsetGenerator(
        llm=generator_llm,
        embedding_model=generator_embeddings
    )
    dataset = generator.generate_with_langchain_docs(docs, testset_size=testset_size)

    # Export to CSV
    df = dataset.to_pandas()
    df.to_csv(output_csv, index=False)

    print(f"✅ Testset generated: {output_csv}")
    return df


# -----------------------------
# 4. Entry point
# -----------------------------
if __name__ == "__main__":
    data_path = r"D:\Projects\Multimodal-Retrieval-Augmented-Generation\uploaded_pdfs\NIPS-2017-attention-is-all-you-need-Paper.pdf"

    generate_testset(
        input_pdf_path=data_path,
        output_csv="testset.csv",
        testset_size=20
    )
