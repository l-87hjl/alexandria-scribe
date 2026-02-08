# Stage 1 Emergence — Safety Guarantees

This document defines the **non‑negotiable safety guarantees** that apply during **Stage 1 concept emergence** in Alexandria Scribe.

Stage 1 exists to surface *signals of relatedness* without creating meaning, structure, or ontology.

---

## Core Principle

> **Stage 1 may reveal resemblance, but must not create concepts.**

Anything that risks turning resemblance into structure is explicitly disallowed.

---

## Guaranteed Properties

### 1. No Ontology

- No category tables
- No concept schemas
- No taxonomies
- No hierarchies

Similarity signals do **not** imply membership or classification.

---

### 2. No Concept Naming

- No labels
- No titles
- No user-defined names
- No system-generated names

Fragments are referenced **only by ID**.

---

### 3. Ephemeral Similarity

- Similarity is computed **on demand**
- Similarity is **not persisted**
- No similarity results are stored in the database

Restarting the app resets all similarity signals.

---

### 4. Local Scope Only

- Similarity is computed **only within the current view**
- Pagination enforces a hard boundary on scope
- There is no global similarity graph

This prevents accidental global meaning formation.

---

### 5. Signal Thresholding

- Weak similarities are suppressed
- Default threshold: **0.25 cosine similarity**
- Only the **top 5** related fragments are shown

This prevents noise from appearing meaningful.

---

### 6. Read‑Only Exposure

- Similarity cannot be edited
- Similarity cannot be confirmed
- Similarity cannot be rejected
- Similarity cannot be saved

Users may observe signals but cannot act on them structurally.

---

### 7. Fragment Immutability

- Fragments are append‑only
- Fragment content is immutable
- Similarity signals cannot modify fragments

Meaning does not feed back into storage.

---

## Explicitly Disallowed in Stage 1

The following actions **must not** be implemented during Stage 1:

- Naming clusters
- Persisting similarity graphs
- Promoting similarity to structure
- Creating "concept" records
- Allowing user confirmation of relationships

Any of the above constitutes a **point of no return**.

---

## Transition Criteria to Stage 2

Stage 2 may only be considered when:

- Stage 1 guarantees have held under scale
- Fragment count is large enough to test noise behavior
- Clear governance rules for naming exist
- Safety tests explicitly enforce Stage 1 constraints

Until then, Stage 1 must remain intact.

---

## Summary

> Stage 1 is successful if the system becomes *suggestive but not authoritative*.

If the system ever starts to feel like it "knows what something is," Stage 1 has been violated.
