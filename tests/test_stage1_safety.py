import sqlite3
import tempfile
import os
import shutil
from app import app
from storage import init_db, get_connection


def snapshot_fragment_count():
    conn = get_connection()
    try:
        cur = conn.execute("SELECT COUNT(*) FROM fragments")
        return cur.fetchone()[0]
    finally:
        conn.close()


def list_tables():
    conn = get_connection()
    try:
        cur = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        return [r[0] for r in cur.fetchall()]
    finally:
        conn.close()


def test_recombulator_does_not_modify_database():
    client = app.test_client()

    before_count = snapshot_fragment_count()

    response = client.post(
        "/recombulator",
        data={"fragment_ids": [], "format": "md"},
    )

    after_count = snapshot_fragment_count()

    assert before_count == after_count


def test_only_fragment_table_exists():
    tables = list_tables()
    assert tables == ["fragments"]


def test_zip_ingestion_skips_unsupported_files():
    client = app.test_client()

    tmpdir = tempfile.mkdtemp()
    try:
        zip_path = os.path.join(tmpdir, "test.zip")
        with open(zip_path, "wb") as f:
            import zipfile
            with zipfile.ZipFile(f, "w") as zf:
                zf.writestr("a.txt", "hello")
                zf.writestr("b.pdf", "%PDF-1.4 fake")

        before = snapshot_fragment_count()

        with open(zip_path, "rb") as zf:
            client.post(
                "/disassembler",
                data={"files": [zf]},
                content_type="multipart/form-data",
            )

        after = snapshot_fragment_count()

        # Only the text file should ingest
        assert after == before + 1
    finally:
        shutil.rmtree(tmpdir)
