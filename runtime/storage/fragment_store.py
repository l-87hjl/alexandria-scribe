import sqlite3
from pathlib import Path

DB_PATH = Path("data/fragments.db")

class FragmentStore:
    def __init__(self):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.execute("""CREATE TABLE IF NOT EXISTS fragments (
            fragment_id TEXT PRIMARY KEY,
            raw_text TEXT,
            source_id TEXT,
            timestamp TEXT,
            author_id TEXT,
            signals_json TEXT
        )""")
        self.conn.commit()

    def append(self, fragment):
        self.conn.execute(
            "INSERT INTO fragments VALUES (?, ?, ?, ?, ?, ?)",
            (
                fragment["fragment_id"],
                fragment["raw_text"],
                fragment["source_id"],
                fragment["timestamp"],
                fragment.get("author_id"),
                "{}",
            ),
        )
        self.conn.commit()
