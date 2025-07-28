# 📘 PDF Outline Extractor

This project extracts a **structured outline** from academic or technical PDFs using visual and numbering-based heading detection. It outputs both a **flat** and a **nested** JSON structure.

---

## 🧠 Approach

Our system extracts meaningful section headings using a **hybrid strategy**:

- ✅ **Font-based heuristics** (font size, boldness)
- ✅ **Number-based regex rules** (e.g., `1.2.3 Introduction`)
- ✅ Cleans and filters out garbage (like one-word or punctuation-only headings)
- ✅ Supports **H1 → H2 → H3** nesting via prefix depth (e.g., `1`, `1.1`, `1.1.1`)
- ✅ Removes empty `subsections: []` for cleaner nested output

---

## 🛠️ Tech Stack

| Tool        | Purpose                          |
|-------------|----------------------------------|
| `pdfplumber`| Extracts text and layout from PDFs |
| `re`        | Regex for number-based headings    |
| `json`      | Structure outputs in JSON format   |
| `Docker`    | Containerized deployment           |

---

## 📂 Folder Structure

```
adobe-hackathon-starter/
├── Dockerfile
├── main.py                  # Generates flat outline.json
├── postprocess.py           # Converts flat → nested_outline.json
├── input/
│   └── sample.pdf
├── output/
│   ├── outline.json         # Flat headings
│   └── nested_outline.json  # Nested headings
└── README.md
```

---

## 🚀 How to Run

### 🔧 1. Build Docker image

```bash
docker build -t adobe-outline .
```

### 📄 2. Run the container

```bash
docker run --rm   -v "$(pwd)/input:/app/input"   -v "$(pwd)/output:/app/output"   adobe-outline
```

> This will generate the flat outline in `/output/outline.json`.

### 🧱 3. Generate Nested Outline

After generating the flat outline, run:

```bash
python postprocess.py
```

> This will create `/output/nested_outline.json`.

---

## 🎯 Example Output

### Flat Outline (`outline.json`)
```json
[
  { "level": "H1", "text": "1. Introduction to NLG", "page": 1 },
  { "level": "H2", "text": "1.1 Text Summarization", "page": 2 },
  ...
]
```

### Nested Outline (`nested_outline.json`)
```json
{
  "title": "UNIT IV: CHAPTER 1",
  "outline": [
    {
      "level": "H1",
      "text": "1. Introduction to NLG",
      "page": 1,
      "subsections": [
        {
          "level": "H2",
          "text": "1.1 Text Summarization",
          "page": 2
        }
      ]
    }
  ]
}
```

---

## ✅ Submission Checklist

- [x] Dockerfile at root
- [x] All dependencies inside the container
- [x] Generates output in expected format
- [x] Clean nested JSON with empty subsections removed

---

## 🌐 Bonus (Optional)

Support for **multilingual headings** (e.g., Japanese, Hindi) can be added with:
- `pytesseract` + `pdf2image` for OCR
- Unicode-compatible regex adjustments

---

## 👨‍💻 Authors

- Sahith Baratam & Team 