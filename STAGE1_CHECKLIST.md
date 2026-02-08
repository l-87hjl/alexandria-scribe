# Stage 1 Checklist — Canonical Status

This document defines what **Stage 1** means in Alexandria-Scribe, what it guarantees, and what kinds of work are still allowed **without advancing stages**.

Stage 1 is now **mechanically enforced** by tests. This checklist clarifies what remains *open by design*.

---

## ✅ Stage 1 — Architecturally Complete (Locked)

These properties are required and enforced:

### Memory & Storage
- Append-only fragment storage
- Fragment immutability
- No deletion or mutation paths

### Semantics
- No ontology tables
- No concept naming
- No persistent clustering
- No hierarchy or taxonomy

### Emergence
- Similarity signals only
- Local scope (page-bounded)
- Ephemeral (not persisted)

### Recombination
- Export-only recombination
- No recombined artifacts stored
- No feedback into ingestion

### Enforcement
- CI tests prevent ontology introduction
- CI tests prevent recombulator writes

---

## 🧭 Stage 1 — Still Allowed (Explicit Extensions)

The following areas are **intentionally open** in Stage 1 and do *not* advance the system to Stage 2.

### 1. UX Polish

Examples:
- Improved fragment browsing
- Selection ergonomics
- Ordering UI inside Recombulator
- Visual clarity

Constraint:
> UX may not introduce persistence or semantics.

---

### 2. Format Expansion

Examples:
- Additional export formats
- Markdown variants
- ZIP layout improvements

Constraint:
> Formats affect outputs only, never memory.

---

### 3. Ingestion Breadth

Examples:
- PDF ingestion
- DOCX ingestion
- Multi-file uploads
- ZIP uploads

Constraint:
> Ingestion may extract text, but must not infer structure or meaning.

---

## 🚫 Explicitly Not Stage 1

The following actions **advance the system beyond Stage 1** and are disallowed:

- Naming concepts
- Persisting clusters
- Saving user groupings
- Ontology-like schemas
- Feedback from exports into memory

---

## Summary

> Stage 1 is complete when **meaning remains human-side only**.

Everything listed as “Still Allowed” improves usability or reach without changing that fact.
