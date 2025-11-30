import os
from unstructured.partition.pdf import partition_pdf


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


def process_pdfs_in_directory(directory_path):
    """
    Process all PDFs in a directory and return all elements.
    """
    all_elements = []
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)
            elements = create_chunks_from_pdf(file_path)
            all_elements.extend(elements)
    return all_elements


def process_pdf_input(input_path):
    """
    Process either a single PDF file or all PDFs in a directory.
    """
    all_elements = []

    if os.path.isfile(input_path):
        if input_path.lower().endswith(".pdf"):
            elements = create_chunks_from_pdf(input_path)
            all_elements.extend(elements)
        else:
            raise ValueError(f"File {input_path} is not a PDF")
    elif os.path.isdir(input_path):
        all_elements = process_pdfs_in_directory(input_path)
    else:
        raise ValueError(f"Path {input_path} is neither a file nor a directory")

    return all_elements


def table_text_segregation(all_elements):
    """
    Segregate elements into tables and texts.
    """
    tables = []
    texts = []

    for el in all_elements:
        el_type = str(type(el))
        if "Table" in el_type:
            tables.append(el)
        elif "CompositeElement" in el_type:
            texts.append(el)

    return tables, texts


def get_images(chunks):
    """
    Extract images from CompositeElements.
    """
    images_b64 = []
    for chunk in chunks:
        if "CompositeElement" in str(type(chunk)):
            chunk_els = chunk.metadata.orig_elements
            for el in chunk_els:
                if "Image" in str(type(el)):
                    images_b64.append(el.metadata.image_base64)
    return images_b64