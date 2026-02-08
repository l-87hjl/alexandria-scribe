"""
Stage 1 Concept Emergence — Similarity Signals Only

UPDATED:
- Uses real offline deterministic embeddings
- Still no concepts, labels, or hierarchies
"""

import sqlite3
import json
from typing import List, Tuple
from concept_emergence.embeddings_offline import embed

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
    return [
        {"fragment_id": fid, "embedding": embed(content)}
        for fid, content in fragments
    ]


def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return dot / (na * nb) if na and nb else 0.0


def generate_similarity_signals(embeddings, threshold=0.75):
    signals = []
    for i in range(len(embeddings)):
        for j in range(i + 1, len(embeddings)):
            sim = cosine_similarity(
                embeddings[i]["embedding"], embeddings[j]["embedding"]
            )
            if sim >= threshold:
                signals.append({
                    "a": embeddings[i]["fragment_id"],
                    "b": embeddings[j]["fragment_id"],
                    "similarity": round(sim, 4),
                })
    return signals


def run_stage1(output_path="logs/concept_stage1.json", threshold=0.75):
    embeddings = generate_embeddings()
    signals = generate_similarity_signals(embeddings, threshold)

    output = {
        "stage": 1,
        "embedding_model": "offline_hash_v1",
        "threshold": threshold,
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
