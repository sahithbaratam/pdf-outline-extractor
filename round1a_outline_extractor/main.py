import json
import re
from pathlib import Path
import pdfplumber

def is_heading(line):
    """
    Heuristic: A heading is usually short, or starts with numbering.
    """
    line = line.strip()
    if not line:
        return False
    # Matches lines like "1.", "1.1", "2.3.4 Something"
    if re.match(r"^\d+(\.\d+)*[\s:.\-]", line):
        return True
    # Short capitalized phrases
    if len(line) <= 80 and line[0].isupper():
        return True
    return False

def extract_headings(pdf_path):
    headings = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if not text:
                continue
            for line in text.split("\n"):
                line = line.strip()
                if is_heading(line):
                    headings.append({
                        "text": line,
                        "level": None,  # Level will be handled in postprocess
                        "page": page_num
                    })
    return headings

def main():
    input_pdf = Path("../input/sample.pdf")
    output_path = Path("../output/outline.json")

    if not input_pdf.exists():
        print(f"❌ PDF not found at {input_pdf}")
        return

    headings = extract_headings(input_pdf)
    result = {
        "title": "UNIT IV: CHAPTER 1",
        "outline": headings
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"✅ Flat outline saved to {output_path.resolve()}")

if __name__ == "__main__":
    main()
