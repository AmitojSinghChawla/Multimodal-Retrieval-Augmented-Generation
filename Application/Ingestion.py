from unstructured.partition.pdf import partition_pdf
from dotenv import load_dotenv
load_dotenv()
import os


directory_path = os.getenv('DATA_PATH')

pdf_path = "D:/Projects/RetrivalAugmentedGeneration/NIPS-2017-attention-is-all-you-need-Paper.pdf"

def create_chunks_from_pdf(pdf_path):
    elements = partition_pdf(
        filename=pdf_path,                  # mandatory
        strategy="hi_res",                                     # mandatory to use ``hi_res`` strategy
        extract_images_in_pdf=True,                            # mandatory to set as ``True``
        extract_image_block_types=["Image"],          # optional
        extract_image_block_to_payload=True,                  # optional
        # extract_image_block_output_dir="D:/Projects/Rag/extracted_images",# optional - only works when ``extract_image_block_to_payload=False``
        chunking_strategy="by_title",
        max_characters=10000,
        combine_text_under_n_chars=2000,
        new_after_n_chars=6000,

        )
    return elements


def process_pdfs_in_directory(directory_path):
    import os
    from unstructured.partition.pdf import partition_pdf

    all_elements = []

    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)
            elements = create_chunks_from_pdf(file_path)
            all_elements.extend(elements)

    return all_elements

def table_text_segregation(all_elements):
    tables = []
    texts = []

    for el in all_elements:
        if str(type(el)) == "<class 'unstructured.documents.elements.Table'>":
            tables.append(el)
        if str(type(el)) == "<class 'unstructured.documents.elements.CompositeElement'>":
            texts.append(el)

    return tables, texts

def get_images(all_elements):
    images64 = []
    for el in all_elements:
        if str(type(el)) == "<class 'unstructured.documents.elements.CompositeElement'>":
            for img_el in el.metadata.orig_elements or []:
                if 'Image' in str(type(img_el)):
                    images64.append(img_el)
    return images64

