import fitz  # PyMuPDF
import re


def extract_text_blocks(pdf_path):
    """
    Extracts blocks of text along with font information from a PDF.
    """
    doc = fitz.open(pdf_path)
    blocks = []

    for page_num, page in enumerate(doc):
        for block in page.get_text("dict")["blocks"]:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                line_text = ""
                sizes = []
                fonts = []

                for span in line["spans"]:
                    line_text += span["text"]
                    sizes.append(span["size"])
                    fonts.append(span["font"])

                if line_text.strip():  # Ignore empty lines
                    blocks.append({
                        "page": page_num + 1,
                        "text": line_text.strip(),
                        "font_sizes": sizes,
                        "fonts": fonts,
                        "bbox": line["bbox"],
                    })

    return blocks


def score_line(block):
    """
    Assigns a score to a text block to estimate its importance.
    Higher score = higher-level heading.
    """
    text = block["text"]
    avg_size = sum(block["font_sizes"]) / len(block["font_sizes"])
    font_names = " ".join(block["fonts"]).lower()
    bbox = block["bbox"]
    indent = bbox[0]
    length = len(text)

    score = 0

    # Font size importance
    score += avg_size * 1.5

    # Bold fonts
    if "bold" in font_names or "bd" in font_names:
        score += 5

    # Capitalization
    if text.isupper():
        score += 4
    elif text.istitle():
        score += 2

    # Shorter lines = more likely headings
    if length < 40:
        score += 2
    elif length < 80:
        score += 1

    # Less indentation = more likely to be heading
    if indent < 50:
        score += 2

    return score


def classify_headings(blocks):
    """
    Classifies blocks into headings (H1, H2, H3) based on relative scores.
    """
    for block in blocks:
        block["score"] = score_line(block)

    # Sort by score descending
    sorted_blocks = sorted(blocks, key=lambda x: x["score"], reverse=True)

    # Compute thresholds using top N percentile buckets
    scores = [b["score"] for b in sorted_blocks]
    h1_cutoff = scores[int(len(scores) * 0.05)] if len(scores) > 20 else max(scores)
    h2_cutoff = scores[int(len(scores) * 0.15)] if len(scores) > 20 else max(scores) * 0.75
    h3_cutoff = scores[int(len(scores) * 0.30)] if len(scores) > 20 else max(scores) * 0.6

    output = []
    for block in sorted_blocks:
        heading_type = None
        if block["score"] >= h1_cutoff:
            heading_type = "H1"
        elif block["score"] >= h2_cutoff:
            heading_type = "H2"
        elif block["score"] >= h3_cutoff:
            heading_type = "H3"

        if heading_type:
            output.append({
                "text": block["text"],
                "page": block["page"],
                "type": heading_type
            })

    return output
