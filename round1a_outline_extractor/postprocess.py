import json
import re
from pathlib import Path

def get_number_prefix(text):
    match = re.match(r"^(\d+(?:\.\d+)*)(?:\s|:|\.)", text)
    return match.group(1) if match else None

def level_to_heading(level):
    return f"H{level}"

def clean_subsections(outline):
    for node in outline:
        if "subsections" in node:
            if node["subsections"]:
                clean_subsections(node["subsections"])
            else:
                del node["subsections"]
    return outline

def build_nested_outline(sections, title="Untitled"):
    root = {
        "title": title,
        "outline": []
    }
    stack = []

    for sec in sections:
        prefix = get_number_prefix(sec["text"])
        level = prefix.count(".") + 1 if prefix else 1

        text_without_prefix = re.sub(r"^(\d+(?:\.\d+)*)(?:\s|:|\.)\s*", "", sec["text"])

        if not text_without_prefix or len(text_without_prefix.strip()) < 5:
            continue
        if re.search(r'^\d+$', text_without_prefix.strip()):
            continue
        if re.match(r'^\d+(\.\d+)*$', text_without_prefix.strip()):
            continue

        node = {
            "level": level_to_heading(level),
            "text": text_without_prefix.strip(),
            "page": sec.get("page"),
            "subsections": []
        }

        while len(stack) >= level:
            stack.pop()

        if not stack:
            root["outline"].append(node)
        else:
            stack[-1]["subsections"].append(node)

        stack.append(node)

    root["outline"] = clean_subsections(root["outline"])
    return root

def main():
    input_path = Path("../output/outline.json")
    output_path = Path("../output/nested_outline.json")

    with open(input_path, "r", encoding="utf-8") as f:
        flat_data = json.load(f)

    nested = build_nested_outline(flat_data["outline"], title=flat_data.get("title", "Untitled"))

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(nested, f, indent=2, ensure_ascii=False)

    print(f"✅ Nested outline saved to {output_path.resolve()}")

if __name__ == "__main__":
    main()
