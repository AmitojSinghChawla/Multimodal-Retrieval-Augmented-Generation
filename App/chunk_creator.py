# chunk_exporter.py
import json
import uuid


def export_text_chunks(texts, source_pdf, output_file="chunks.jsonl"):
    with open(output_file, "a", encoding="utf-8") as f:
        for text in texts:
            raw_text = text.text if hasattr(text, "text") else str(text)

            record = {
                "chunk_id": str(uuid.uuid4()),
                "modality": "text",
                "source_pdf": source_pdf,
                "page_number": None,
                "raw_text": raw_text,
                "image_b64": None,
                "gold_questions": [],
            }
            f.write(json.dumps(record) + "\n")


def export_image_chunks(images_b64, source_pdf, output_file="chunks.jsonl"):
    with open(output_file, "a", encoding="utf-8") as f:
        for img in images_b64:
            record = {
                "chunk_id": str(uuid.uuid4()),
                "modality": "image",
                "source_pdf": source_pdf,
                "page_number": None,
                "raw_text": None,
                "image_b64": img,
                "gold_questions": [],
            }
            f.write(json.dumps(record) + "\n")
