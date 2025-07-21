import fitz  # PyMuPDF
from collections import defaultdict

def extract_headings_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    headings = []

    font_size_map = defaultdict(list)

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" not in b:
                continue
            for line in b["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue

                    font_size = round(span["size"], 2)
                    font_name = span.get("font", "")
                    is_bold = "Bold" in font_name or "bold" in font_name.lower()

                    font_size_map[font_size].append((text, is_bold, page_num))

    # Sort font sizes descending (larger = higher level heading)
    sorted_font_sizes = sorted(font_size_map.keys(), reverse=True)

    # Assign heading levels
    heading_levels = {}
    for idx, size in enumerate(sorted_font_sizes[:3]):  # h1, h2, h3
        heading_levels[size] = f"h{idx + 1}"

    # Build the final result
    for size in heading_levels:
        for text, is_bold, page_num in font_size_map[size]:
            headings.append({
                "text": text,
                "level": heading_levels[size],
                "page": page_num
            })

    return headings
