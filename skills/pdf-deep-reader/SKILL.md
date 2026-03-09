---
name: pdf-deep-reader
description: Deep analysis of PDF documents including text extraction, structure analysis, table extraction, and content summarization.
---

# PDF Deep Reader Skill

## Capabilities

- Extract text from PDFs (simple and complex layouts)
- Analyze PDF structure (sections, headings, pages)
- Extract tables from PDFs
- Identify and extract images
- Summarize document content
- Search for specific information
- Handle scanned PDFs with OCR (if available)

## Tools Used

- `pymupdf` (fitz) - Fast PDF text extraction
- `pdfplumber` - Table extraction
- `PyPDF2` - PDF metadata
- `pytesseract` - OCR for scanned PDFs (optional)

## Installation

```bash
pip install pymupdf pdfplumber PyPDF2 pytesseract
```

## Usage

When the user asks to analyze a PDF:

1. Load the PDF file
2. Extract metadata (pages, author, title)
3. Extract text content
4. Analyze structure (headings, sections)
5. Extract tables if present
6. Provide summary or answer specific questions

## Example Commands

```python
import fitz  # pymupdf
import pdfplumber

# Open PDF
doc = fitz.open('document.pdf')

# Get page count
print(f"Pages: {len(doc)}")

# Extract text from page
page = doc[0]
text = page.get_text()

# Extract tables
with pdfplumber.open('document.pdf') as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            print(table)

# Search for text
for page in doc:
    if "keyword" in page.get_text().lower():
        print(f"Found on page {page.number + 1}")
```

## Notes

- Use pymupdf for fast text extraction
- Use pdfplumber for accurate table extraction
- Handle multi-column layouts carefully
- OCR requires tesseract-ocr installed
