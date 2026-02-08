"""
SQLite Fragment Store
---------------------
Append-only, Stage 1 safe persistence.
"""

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("data/fragments.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS fragments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    source TEXT,
    source_type TEXT,
    source_page INTEGER,
    ingestion_batch_id TEXT
);
"""


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    try:
        conn.execute(SCHEMA)
        conn.commit()
    finally:
        conn.close()


def add_fragment(
    content: str,
    source: str | None = None,
    source_type: str | None = None,
    source_page: int | None = None,
    ingestion_batch_id: str | None = None,
) -> int:
    conn = get_connection()
    try:
        cur = conn.execute(
            """
            INSERT INTO fragments (content, created_at, source, source_type, source_page, ingestion_batch_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                content,
                datetime.utcnow().isoformat() + "Z",
                source,
                source_type,
                source_page,
                ingestion_batch_id,
            ),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def list_fragments(limit: int = 25, offset: int = 0):
    conn = get_connection()
    try:
        cur = conn.execute(
            """
            SELECT * FROM fragments
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        )
        return cur.fetchall()
    finally:
        conn.close()


def search_fragments(query: str, limit: int = 25, offset: int = 0):
    q = f"%{query}%"
    conn = get_connection()
    try:
        cur = conn.execute(
            """
            SELECT * FROM fragments
            WHERE content LIKE ?
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            (q, limit, offset),
        )
        return cur.fetchall()
    finally:
        conn.close()
