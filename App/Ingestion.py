import os

from langchain_core.runnables import RunnableLambda
from unstructured.partition.pdf import partition_pdf
import dotenv

dotenv.load_dotenv()


# --- PDF processing ---
def create_chunks_from_pdf(file_path):
    """
    Partition a single PDF into structured elements.
    """
    elements = partition_pdf(
        filename=file_path,
        strategy="hi_res",
        extract_images_in_pdf=True,
        extract_image_block_types=["Image"],
        extract_image_block_to_payload=True,
        chunking_strategy="by_title",
        max_characters=10000,
        combine_text_under_n_chars=2000,
        new_after_n_chars=6000,
    )
    return elements


def process_pdfs_in_directory(uploaded_files):
    """
    Process all PDFs in a directory and return all elements.
    """
    all_elements = []

    for filename in os.listdir(uploaded_files):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(uploaded_files, filename)
            elements = create_chunks_from_pdf(file_path)
            all_elements.extend(elements)

    return all_elements


# --- Segregate elements ---
def table_text_segregation(all_elements):
    tables, texts = [], []

    for el in all_elements:
        el_type = str(type(el))
        if "Table" in el_type:
            tables.append(el)
        elif "CompositeElement" in el_type:
            texts.append(el)

    return tables, texts


def get_images(all_elements):
    """
    Extract images from CompositeElements as base64 or objects as needed.
    """
    images64 = []

    for el in all_elements:
        if "CompositeElement" in str(type(el)):
            orig_elements = getattr(el.metadata, "orig_elements", []) or []
            for img_el in orig_elements:
                if "Image" in str(type(img_el)):
                    images64.append(img_el)

    return images64



def ingest(uploaded_files):
    """
    Complete ingestion pipeline for PDFs in a directory.
    """
    try:
        elements = process_pdfs_in_directory(uploaded_files)
        tables, texts = table_text_segregation(elements)
        images64 = get_images(elements)
        return tables, texts, images64

    except Exception as e:
        raise RuntimeError(f"Ingestion pipeline failed: {str(e)}")


def process(tables,texts,images64):
    from App.summarizer import summarize_texts_tables, summarize_images

    table_summaries,text_summaries = summarize_texts_tables(texts,tables)
    image_summaries = summarize_images(images64)
    """
    Process and return the segregated elements.
    """
    return table_summaries, text_summaries, image_summaries

