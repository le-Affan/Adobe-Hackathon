import sys
import os
import json
from util import extract_headings_from_pdf


def extract_headings(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' does not exist.")
        return

    try:
        result = extract_headings_from_pdf(pdf_path)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"An error occurred while processing the PDF: {e}")


if __name__ == "__main__":
    pdf_path = "input/file02.pdf"  # or whatever your file name is
    extract_headings(pdf_path)
    # if len(sys.argv) != 2:
    #     print("Usage: python main.py <pdf_file_path>")
    # else:
    #     extract_headings(sys.argv[1])
