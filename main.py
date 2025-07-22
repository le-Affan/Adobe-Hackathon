import sys
import json
from util import extract_outline

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_pdf_path> <output_json_path>")
        return

    input_pdf = sys.argv[1]
    output_json = sys.argv[2]

    outline_data = extract_outline(input_pdf)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(outline_data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
