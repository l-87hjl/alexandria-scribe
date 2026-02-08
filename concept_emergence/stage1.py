"""
Stage 1 Concept Emergence — Similarity Signals Only

This module implements the *first executable step* toward concept emergence.

Constraints (ENFORCED BY DESIGN):
- No named concepts
- No hierarchies
- No labels exposed to UI
- Read-only with respect to fragments

Outputs:
- Embeddings stored separately
- Similarity signals (pairwise / graph-ready)
- Logged only; no mutation of fragment content
"""

import sqlite3
import json
from typing import List, Tuple

# Placeholder embedding function — replace with offline model later

def embed(text: str) -> List[float]:
    """Deterministic placeholder embedding.
    Replace with offline embedding model when ready.
    """
    return [float(len(text))]


DB_PATH = "fragments.db"


def load_fragments() -> List[Tuple[int, str]]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, content FROM fragments")
    rows = cur.fetchall()
    conn.close()
    return rows


def generate_embeddings():
    fragments = load_fragments()
    embeddings = []

    for fragment_id, content in fragments:
        vector = embed(content)
        embeddings.append({
            "fragment_id": fragment_id,
            "embedding": vector,
        })

    return embeddings


def compute_similarity(a: List[float], b: List[float]) -> float:
    # Minimal similarity heuristic (placeholder)
    return 1.0 / (1.0 + abs(a[0] - b[0]))


def generate_similarity_signals(embeddings):
    signals = []
    for i in range(len(embeddings)):
        for j in range(i + 1, len(embeddings)):
            sim = compute_similarity(
                embeddings[i]["embedding"], embeddings[j]["embedding"]
            )
            signals.append({
                "a": embeddings[i]["fragment_id"],
                "b": embeddings[j]["fragment_id"],
                "similarity": sim,
            })
    return signals


def run_stage1(output_path="logs/concept_stage1.json"):
    embeddings = generate_embeddings()
    signals = generate_similarity_signals(embeddings)

    output = {
        "stage": 1,
        "embeddings": embeddings,
        "signals": signals,
        "constraints": {
            "named_concepts": False,
            "hierarchies": False,
            "ui_exposure": False,
        },
    }

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    return output


if __name__ == "__main__":
    run_stage1()
