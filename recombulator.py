"""
Recombulator — Export-only backend logic
---------------------------------------

Generates export artifacts from selected fragments.

Guarantees:
- Read-only access to fragments
- No database writes
- No persistence of outputs
"""

from typing import List
from io import BytesIO
import zipfile
from storage import get_connection


def fetch_fragments_by_ids(ids: List[int]):
    if not ids:
        return []

    placeholders = ",".join("?" for _ in ids)
    query = f"SELECT id, content, created_at, source FROM fragments WHERE id IN ({placeholders}) ORDER BY id"

    conn = get_connection()
    try:
        cur = conn.execute(query, ids)
        return cur.fetchall()
    finally:
        conn.close()


def assemble_markdown(fragments) -> str:
    parts = []
    for f in fragments:
        parts.append(f"---\nFragment #{f['id']}\n\n{f['content']}\n")
    return "\n".join(parts)


def assemble_text(fragments) -> str:
    parts = []
    for f in fragments:
        parts.append(f"[Fragment #{f['id']}]\n{f['content']}\n")
    return "\n".join(parts)


def assemble_zip(fragments) -> BytesIO:
    """
    Create a ZIP archive with one file per fragment.
    Filenames are stable and ordered.
    """
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in fragments:
            filename = f"fragment_{f['id']}.md"
            content = assemble_markdown([f])
            zf.writestr(filename, content)
    buf.seek(0)
    return buf
