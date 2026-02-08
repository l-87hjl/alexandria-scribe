"""
CSV Ingestion — Stage 1 Safe
---------------------------

Rules:
- Each non-header row becomes one fragment
- No column semantics inferred
- Header preserved as provenance text
"""

import csv
import io


def extract_csv_fragments(csv_bytes: bytes, filename: str):
    text = csv_bytes.decode("utf-8", errors="ignore")
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)

    if not rows:
        return []

    header = rows[0]
    fragments = []

    for i, row in enumerate(rows[1:], start=2):
        content = ", ".join(row).strip()
        if not content:
            continue
        fragments.append({
            "content": content,
            "source": filename,
            "source_type": "csv",
            "source_page": i,
            "header": ", ".join(header),
        })

    return fragments
