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

If `pdftotext` is missing:
```bash
brew install poppler  # macOS
apt install poppler-utils  # Linux
```

## Advanced: pdfplumber

For tables, bounding boxes, or precise layout control, use pdfplumber:

```bash
pip install pdfplumber
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

## When to use which

| Task | Tool |
|------|------|
| Read text | pdftotext |
| Preserve columns/layout | pdftotext -layout |
| Extract tables | pdfplumber |
| Get text coordinates | pdfplumber |
| Encrypted PDFs | pdfplumber |
