"""
Phase A Guardrail Tests

These tests enforce core preservation guarantees:
- Fragments are immutable once written
- Storage is append-only
- No concept labels or ontology structures are introduced

These tests are intentionally conservative and should fail loudly
if future changes violate preservation constraints.
"""

import sqlite3
import pytest

DB_PATH = "fragments.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def test_fragments_are_append_only():
    """Ensure fragments table does not allow UPDATE or DELETE."""
    conn = get_connection()
    cur = conn.cursor()

    # Attempt to delete from fragments table
    with pytest.raises(sqlite3.OperationalError):
        cur.execute("DELETE FROM fragments")

    # Attempt to update fragments table
    with pytest.raises(sqlite3.OperationalError):
        cur.execute("UPDATE fragments SET content = 'mutated'")

    conn.close()


def test_fragment_immutability_by_id():
    """Ensure an existing fragment cannot be mutated by ID."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, content FROM fragments LIMIT 1")
    row = cur.fetchone()

    if row is None:
        pytest.skip("No fragments present yet")

    fragment_id, original_content = row

    with pytest.raises(sqlite3.OperationalError):
        cur.execute(
            "UPDATE fragments SET content = 'tampered' WHERE id = ?",
            (fragment_id,),
        )

    conn.close()


def test_no_concept_labels_table_exists():
    """Ensure no ontology or concept-label tables exist yet."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%concept%'"
    )
    rows = cur.fetchall()

    assert rows == [], "Concept or ontology tables must not exist at this stage"

    conn.close()
