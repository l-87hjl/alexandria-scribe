"""
DOCX Ingestion — Stage 1 Safe
----------------------------

Rules:
- Extract visible text only
- No heading or style semantics
- Conservative paragraph-level fragmentation
"""

from docx import Document


def extract_docx_fragments(docx_bytes: bytes, filename: str):
    doc = Document(docx_bytes)
    fragments = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        fragments.append({
            "content": text,
            "source": filename,
        })

    return fragments
