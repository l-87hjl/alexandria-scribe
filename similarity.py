"""
Stage 1 Concept Emergence — Similarity Signals Only
--------------------------------------------------

Safety constraints:
- No concept naming
- No clustering persistence
- No ontology
- Similarity is local to the current view
- Weak signals are suppressed
"""

from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DEFAULT_SIMILARITY_THRESHOLD = 0.25
DEFAULT_TOP_K = 5


def compute_similarity(
    fragments: List[Tuple[int, str]],
    threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
    top_k: int = DEFAULT_TOP_K,
):
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
            if score >= threshold:
                scores.append((other_id, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        results[fid] = scores[:top_k]

    return results
