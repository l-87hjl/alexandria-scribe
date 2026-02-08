"""
Stage 1 Concept Emergence — Similarity Signals Only
--------------------------------------------------

This module computes lightweight similarity signals between fragments.

Constraints:
- No concept naming
- No clustering persistence
- No ontology
- Signals are ephemeral and computed on demand
"""

from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity(fragments: List[Tuple[int, str]], top_k: int = 5):
    """
    Given a list of (id, content), return similarity scores per fragment.

    Returns:
        dict[id] -> list of (other_id, score)
    """
    ids = [f[0] for f in fragments]
    texts = [f[1] for f in fragments]

    if len(texts) < 2:
        return {}

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform(texts)
    sim_matrix = cosine_similarity(tfidf)

    results = {}
    for i, fid in enumerate(ids):
        scores = []
        for j, other_id in enumerate(ids):
            if i == j:
                continue
            score = float(sim_matrix[i, j])
            if score > 0:
                scores.append((other_id, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        results[fid] = scores[:top_k]

    return results
