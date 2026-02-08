"""
SQLite Fragment Store
---------------------
Core, append-only persistence layer for fragments.

Design constraints:
- Append-only (no UPDATE / DELETE for fragments)
- Immutable fragments
- Simple schema, no ontology
- SQLite file lives with the app
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List

DB_PATH = Path("data/fragments.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS fragments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    source TEXT
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


def add_fragment(content: str, source: str | None = None) -> int:
    """Insert a new fragment. Returns fragment ID."""
    conn = get_connection()
    try:
        cur = conn.execute(
            "INSERT INTO fragments (content, created_at, source) VALUES (?, ?, ?)",
            (content, datetime.utcnow().isoformat() + "Z", source),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def list_fragments(limit: int = 100):
    conn = get_connection()
    try:
        cur = conn.execute(
            "SELECT id, content, created_at, source FROM fragments ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        return cur.fetchall()
    finally:
        conn.close()


def search_fragments(query: str, limit: int = 100) -> List[sqlite3.Row]:
    """
    Read-only substring search over fragment content.
    No semantics, no ranking beyond recency.
    """
    q = f"%{query}%"
    conn = get_connection()
    try:
        cur = conn.execute(
            """
            SELECT id, content, created_at, source
            FROM fragments
            WHERE content LIKE ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (q, limit),
        )
        return cur.fetchall()
    finally:
        conn.close()
