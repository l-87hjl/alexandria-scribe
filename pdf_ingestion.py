"""
PDF Ingestion — Stage 1 Safe
---------------------------

Rules:
- One or more fragments per page
- No semantic interpretation
- Conservative text extraction
"""

from io import BytesIO
from PyPDF2 import PdfReader


def extract_pdf_fragments(pdf_bytes: bytes, filename: str):
    """
    Accept raw PDF bytes, wrap in BytesIO for PyPDF2 compatibility.
    """
    stream = BytesIO(pdf_bytes)
    reader = PdfReader(stream)

    fragments = []
    for idx, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""

        text = text.strip()
        if not text:
            continue

        fragments.append({
            "content": text,
            "source": filename,
            "source_page": idx,
        })

    return fragments
