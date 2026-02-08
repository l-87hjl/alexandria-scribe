import io
import zipfile
from app import app
from storage import get_connection


def count_fragments():
    conn = get_connection()
    try:
        return conn.execute("SELECT COUNT(*) FROM fragments").fetchone()[0]
    finally:
        conn.close()


def test_pdf_ingestion_creates_multiple_fragments():
    client = app.test_client()

    # Minimal fake PDF structure using PyPDF2 expectations
    from PyPDF2 import PdfWriter
    buf = io.BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    writer.add_blank_page(width=72, height=72)
    writer.write(buf)
    buf.seek(0)

    before = count_fragments()

    client.post(
        "/disassembler",
        data={"files": [(buf, "test.pdf")]},
        content_type="multipart/form-data",
    )

    after = count_fragments()

    # At least one fragment per page expected
    assert after >= before + 2


def test_pdf_ingestion_does_not_create_tables():
    conn = get_connection()
    try:
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        assert [t[0] for t in tables] == ["fragments"]
    finally:
        conn.close()
