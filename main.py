import json
import os
from util import extract_text_blocks, classify_headings


def get_pdf_title(pdf_path):
    """
    Attempts to extract the PDF title from metadata or filename.
    """
    import fitz
    doc = fitz.open(pdf_path)
    metadata_title = doc.metadata.get("title")
    if metadata_title and metadata_title.strip():
        return metadata_title.strip()
    return os.path.splitext(os.path.basename(pdf_path))[0]


def build_outline(pdf_path):
    blocks = extract_text_blocks(pdf_path)
    headings = classify_headings(blocks)

    outline = {
        "title": get_pdf_title(pdf_path),
        "headings": headings
    }

    return outline


if __name__ == "__main__":
    pdf_file = "sample.pdf"  # Replace with your input file
    output_file = "outline.json"

    if not os.path.exists(pdf_file):
        print(f"Error: '{pdf_file}' not found.")
    else:
        print(f"Processing '{pdf_file}'...")
        outline = build_outline(pdf_file)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(outline, f, indent=4, ensure_ascii=False)

        print(f"Outline written to '{output_file}'")
