"""
Offline Embedding Model (Stage 1)

Implements a lightweight, fully-offline embedding mechanism with **no external
network or model dependencies**.

Design goals:
- Deterministic
- Replaceable later with a real local model (e.g. sentence-transformers)
- Safe for Stage 1 (signals only, no concepts)
"""

import hashlib
from typing import List

EMBEDDING_DIM = 8


def embed(text: str) -> List[float]:
    """Create a deterministic vector from text using hashing.

    This is NOT semantic understanding — only a stable signal generator.
    """
    h = hashlib.sha256(text.encode("utf-8")).digest()
    # Convert first bytes into a small numeric vector
    return [h[i] / 255.0 for i in range(EMBEDDING_DIM)]
