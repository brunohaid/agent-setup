---
name: pdf
description: Extract text and tables from PDF files. Use for reading PDF content, extracting tables, or analyzing PDF documents.
---

# PDF Skill

## Quick Start

Use `pdftotext` for simple text extraction (fast, no Python deps):

```bash
pdftotext "file.pdf" -  # outputs to stdout
pdftotext -layout "file.pdf" -  # preserve layout
pdftotext -f 1 -l 5 "file.pdf" -  # pages 1-5 only
```

## Installation

Core tools (`pdftotext`, `pdftoppm`, `pdfimages`) all come from **poppler**:
```bash
brew install poppler       # macOS
apt install poppler-utils  # Linux
```

Optional — for tables, bounding boxes, or precise layout control:
```bash
pip install pdfplumber
```

Optional — for OCR of scanned/image-based PDFs:
```bash
brew install tesseract ocrmypdf   # macOS
apt install tesseract-ocr ocrmypdf  # Linux
# Usage: ocrmypdf --force-ocr --deskew input.pdf output.pdf && pdftotext output.pdf -
```

### Extract text
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    for page in pdf.pages:
        print(page.extract_text())
```

### Extract tables
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    for page in pdf.pages:
        for table in page.extract_tables():
            for row in table:
                print(row)
```

### Extract text from region
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    page = pdf.pages[0]
    # Crop to region (x0, top, x1, bottom)
    cropped = page.crop((0, 0, 300, 200))
    print(cropped.extract_text())
```

## Diagrams and Figures

Use `pdftoppm` to render PDF pages (including vector diagrams, schematics, block diagrams) to PNG, then view with the `read` tool:

```bash
pdftoppm -png -r 200 -f 11 -l 11 "file.pdf" /tmp/page    # render page 11 at 200 DPI
# output: /tmp/page-11.png (or /tmp/page-0011.png depending on page count)
```

Use `-r 300` for fine-detail schematics. Comes with poppler (same as pdftotext).

To extract only embedded raster images (photos, logos — not vector diagrams):
```bash
pdfimages -png -f 1 -l 5 "file.pdf" /tmp/img    # extract images from pages 1-5
```

## When to use which

| Task | Tool |
|------|------|
| Read text | pdftotext |
| Preserve columns/layout | pdftotext -layout |
| Extract tables | pdfplumber |
| Get text coordinates | pdfplumber |
| Encrypted PDFs | pdfplumber |
| View diagrams/schematics | pdftoppm → read |
| Extract embedded images | pdfimages |
