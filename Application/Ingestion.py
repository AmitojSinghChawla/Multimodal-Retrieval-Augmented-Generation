from unstructured.partition.pdf import partition_pdf
from dotenv import load_dotenv
import os
from io import BytesIO

load_dotenv()
directory_path = os.getenv('DATA_PATH')


def create_chunks_from_pdf(source):
    """
    Create document chunks from a PDF.
    `source` can be either:
      - bytes / BytesIO (for API uploads)
      - str path (for local file)
    """
    # Determine input type
    if isinstance(source, (bytes, BytesIO)):
        pdf_stream = BytesIO(source) if isinstance(source, bytes) else source
        elements = partition_pdf(
            file=pdf_stream,
            strategy="hi_res",
            extract_images_in_pdf=True,
            extract_image_block_types=["Image"],
            extract_image_block_to_payload=True,
            chunking_strategy="by_title",
            max_characters=10000,
            combine_text_under_n_chars=2000,
            new_after_n_chars=6000,
        )
    elif isinstance(source, str) and source.lower().endswith(".pdf"):
        elements = partition_pdf(
            filename=source,
            strategy="hi_res",
            extract_images_in_pdf=True,
            extract_image_block_types=["Image"],
            extract_image_block_to_payload=True,
            chunking_strategy="by_title",
            max_characters=10000,
            combine_text_under_n_chars=2000,
            new_after_n_chars=6000,
        )
    else:
        raise ValueError("Unsupported source type. Provide PDF bytes or a valid file path.")

    return elements

#Function to process all PDFs in a directory.
# def process_pdfs_in_directory(directory_path):
#     import os
#     from unstructured.partition.pdf import partition_pdf
#
#     all_elements = []
#
#     for filename in os.listdir(directory_path):
#         if filename.endswith(".pdf"):
#             file_path = os.path.join(directory_path, filename)
#             elements = create_chunks_from_pdf(file_path)
#             all_elements.extend(elements)
#
#     return all_element

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
    images64 = []
    for el in all_elements:
        if "CompositeElement" in str(type(el)):
            for img_el in getattr(el.metadata, "orig_elements", []) or []:
                if "Image" in str(type(img_el)):
                    images64.append(img_el)
    return images64


def ingest_pdfs_to_vector_db(uploaded_files):
    """
    uploaded_files: can be a list of BytesIO objects (from FastAPI)
    or a list of file paths (for local testing)
    """
    from sumarrizer import summarize_texts_tables, summarize_images
    from VectorDB import add_documents_to_vector_db

    all_elements = []

    # Handle both path and BytesIO cases
    for f in uploaded_files:
        elements = create_chunks_from_pdf(f)
        all_elements.extend(elements)

    # Process elements
    tables, texts = table_text_segregation(all_elements)
    text_summaries, table_summaries = summarize_texts_tables(texts, tables)
    images64 = get_images(all_elements)
    img_summaries = summarize_images(images64)

    add_documents_to_vector_db(texts, text_summaries, tables, table_summaries, images64, img_summaries)
    return "Ingestion complete."

