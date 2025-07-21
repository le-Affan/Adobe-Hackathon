from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

def extract_headings_from_pdf(pdf_path):
    headings = []
    max_font_sizes = {"H1": 0, "H2": 0, "H3": 0}
    font_size_thresholds = []

    # First pass: collect all font sizes
    font_sizes = set()
    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    for character in text_line:
                        if isinstance(character, LTChar):
                            font_sizes.add(round(character.size, 1))

    # Sort and define thresholds
    font_sizes = sorted(font_sizes, reverse=True)
    if len(font_sizes) >= 3:
        font_size_thresholds = font_sizes[:3]
    else:
        font_size_thresholds = font_sizes + [0] * (3 - len(font_sizes))

    def get_heading_level(font_size):
        if round(font_size, 1) == font_size_thresholds[0]:
            return "H1"
        elif round(font_size, 1) == font_size_thresholds[1]:
            return "H2"
        elif round(font_size, 1) == font_size_thresholds[2]:
            return "H3"
        else:
            return None

    for page_number, page_layout in enumerate(extract_pages(pdf_path), start=1):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    line_text = text_line.get_text().strip()
                    if not line_text:
                        continue
                    font_size = 0
                    for character in text_line:
                        if isinstance(character, LTChar):
                            font_size = max(font_size, round(character.size, 1))
                    heading_level = get_heading_level(font_size)
                    if heading_level:
                        headings.append({
                            "level": heading_level,
                            "text": line_text,
                            "page": page_number
                        })

    # Format final result
    title_parts = [h["text"] for h in headings if h["level"] == "H1" and h["page"] == 1]
    title = "  ".join(title_parts)

    return {
        "title": title,
        "outline": headings
    }
