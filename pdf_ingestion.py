"""
PDF Ingestion — Stage 1 Safe
---------------------------

Rules:
- Extract raw text only
- No structure inference
- No section detection
- Multiple fragments per page allowed
- Page numbers preserved as provenance
"""

from typing import List
from PyPDF2 import PdfReader


def extract_pdf_fragments(pdf_bytes: bytes, filename: str) -> List[dict]:
    reader = PdfReader(pdf_bytes)
    fragments = []

    for page_index, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception:
            continue

        # Conservative splitting: blank lines
        blocks = [b.strip() for b in text.split("\n\n") if b.strip()]

        for block in blocks:
            fragments.append({
                "content": block,
                "source": filename,
                "source_page": page_index,
            })

    return fragments
