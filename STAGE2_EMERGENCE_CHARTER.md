# Stage 2 Emergence Charter — Soft Structure Without Meaning

This document defines **Stage 2 of concept emergence**.

It is intentionally **charter-only**: no implementation, no schema, no UI commitments.
Its purpose is to define *what is allowed*, *what is forbidden*, and *where the new points of no return lie*.

Stage 2 exists to increase **navigability and compression** while preserving the system’s core property:

> **The system remembers faithfully before it understands.**

---

## I. Minimum Architecture for First Implementation (Baseline)

Before Stage 2, the **minimum viable architecture** for a preservation-first system is:

### Required (Must Exist)

1. **Fragment store**
   - Append-only
   - Immutable fragments

2. **Provenance model**
   - Fragment origin preserved
   - Time-order preserved

3. **Anti-ontology constraints**
   - No required categories
   - No schema-level meaning

4. **Stage 1 emergence**
   - Embeddings
   - Similarity signals
   - Logged only

5. **Read-only exploration UI**
   - Fragment browsing
   - Optional similarity-based relatedness

If these are present, the system is *architecturally complete at Stage 1*.

Everything beyond this point is **phase-based expansion**, not core definition.

---

## II. What Stage 2 Is (Allowed Meaning)

Stage 2 introduces **soft clustering**.

Soft clustering is defined as:

- A *temporary grouping* of fragments
- Derived entirely from Stage 1 signals
- Non-authoritative
- Discardable without data loss

### Properties of Soft Clusters

Soft clusters:

- Have **no names**
- Have **no required membership**
- May overlap freely
- May dissolve or reform
- Are computed, not asserted

A cluster answers only one question:

> “These fragments tend to co-occur or resemble one another.”

It does **not** answer:
- What they *are*
- What they *mean*
- What they *should be called*

---

## III. What Stage 2 Is Not (Explicitly Forbidden)

Stage 2 must not introduce:

- Named concepts
- Hierarchical trees
- Parent/child relationships
- Stable cluster IDs used as keys
- UI flows that require choosing a cluster

Clusters must never become:

- Storage primitives
- Authorization boundaries
- Required metadata

> If a fragment must belong to a cluster, the line has been crossed.

---

## IV. New Points of No Return (Stage 2)

Stage 2 introduces **new dangers** distinct from Stage 1.

The system crosses a new point of no return if:

1. **Clusters are given stable names**
2. **Clusters are stored as authoritative records**
3. **Clusters become the primary navigation surface**
4. **Users are required to assign fragments to clusters**
5. **Deleting all clusters degrades fragment access or ingestion**

These transitions are dangerous because they:

- Shift meaning from emergent to structural
- Encourage users to optimize for clusters
- Freeze interpretation prematurely

> **Rule:** Clusters may assist navigation, never define it.

---

## V. Phase-Based Roadmap (Explicit)

### Phase 1 — Preservation (Complete)
- Fragment ingestion
- Immutability
- Provenance

### Phase 2 — Signal Emergence (Complete)
- Embeddings
- Similarity

### Phase 3 — Soft Structure (Defined Here)
- Soft clustering
- Overlapping groups
- No naming

### Phase 4 — Human Interpretation (Future, Optional)
- Naming (revisable)
- Synthesis
- Export

Only Phases 1–3 are required for a *complete preservation system*.

---

## VI. Canonical Safety Test (Stage 2)

Stage 2 remains safe if and only if the following is true:

> **Deleting all clusters leaves the system fully usable, searchable, and intact.**

If this condition fails, Stage 2 has exceeded its mandate.

---

## VII. Final Rule

> **Stage 2 may increase structure, but must not increase obligation.**

This charter defines the maximum safe envelope for emergence beyond similarity.
