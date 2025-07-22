import fitz  # PyMuPDF
from collections import Counter

EXCLUDE_KEYWORDS = ["table of contents", "acknowledgements", "overview", "revision history", "contents"]

def is_bold(font_name):
    return "Bold" in font_name or "bold" in font_name

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)

    font_stats = []

    headings = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if not text or len(text) < 3:
                        continue

                    font_size = span["size"]
                    font_name = span["font"]
                    is_bold_text = is_bold(font_name)

                    # Store stats to find top font sizes later
                    font_stats.append((round(font_size, 1), is_bold_text))

    # Find most common font sizes
    size_counts = Counter(size for size, bold in font_stats)
    top_sizes = [size for size, _ in size_counts.most_common()]

    if len(top_sizes) < 2:
        return {"title": doc.metadata.get("title", ""), "outline": []}

    h1_size = top_sizes[0]
    h2_size = top_sizes[1] if len(top_sizes) > 1 else None
    h3_size = top_sizes[2] if len(top_sizes) > 2 else None

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if not text or len(text) < 3:
                        continue

                    font_size = round(span["size"], 1)
                    font_name = span["font"]
                    is_bold_text = is_bold(font_name)

                    level = None
                    if font_size == h1_size and is_bold_text:
                        level = "H1"
                    elif font_size == h2_size:
                        level = "H2"
                    elif font_size == h3_size:
                        level = "H3"

                    if level and not any(x in text.lower() for x in EXCLUDE_KEYWORDS):
                        headings.append({
                            "level": level,
                            "text": text,
                            "page": page_num + 1
                        })

    return {
        "title": doc.metadata.get("title", ""),
        "outline": headings
    }
