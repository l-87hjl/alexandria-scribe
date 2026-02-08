# Stage 2 Readiness, Safety, and UI Exploration

This document prepares the system for **Stage 2 (Soft Structure)** without implementing it.

It contains three parts:

1. A **Phase Readiness Checklist** — what must be true before Stage 2 is allowed to exist
2. A **Stage 2 Safety Test Charter** — what must never break once Stage 2 exists
3. A set of **UI metaphors for soft clusters** that do not require new data structures

This document is intentionally *pre-executable*.

---

## I. Phase Readiness Checklist — Before Stage 2 Is Allowed

Stage 2 must **not** be implemented unless *all* of the following are true.

### A. Architectural Preconditions

- Stage 1 emergence is complete and stable
  - Embeddings are deterministic
  - Similarity signals are reproducible
- Fragment immutability is enforced
- Append-only guarantees are in place
- Anti-ontology rules are documented and visible

If any of these regress, Stage 2 is **blocked**.

---

### B. System Integrity Preconditions

- Deleting all Stage 1 outputs (embeddings + signals):
  - Does not affect ingestion
  - Does not affect fragment browsing
  - Does not affect search

- Fragment access does not depend on:
  - Concepts
  - Clusters
  - Derived structures of any kind

Fragments must remain the **only authoritative records**.

---

### C. Human Factors Preconditions

- Users are not required to:
  - Name anything
  - Classify anything
  - Choose a category to proceed

- UI language does not imply meaning or correctness
- All structure is presented as *assistive*, not *defining*

If users feel they are "doing it wrong," Stage 2 is premature.

---

## II. Stage 2 Safety Tests (Charter Only)

These tests define **what must always remain true** once soft clustering exists.
They are written as *claims*, not code.

---

### Safety Test 1 — Cluster Deletion Test

> Deleting all clusters must leave the system fully usable.

Expected behavior:
- All fragments remain accessible
- Search continues to work
- Similarity exploration continues to work
- No errors surface in UI or runtime

If this test fails, clusters have become structural.

---

### Safety Test 2 — Fragment Sovereignty Test

> A fragment must never require cluster membership.

Expected behavior:
- Fragments may appear in zero, one, or many clusters
- No fragment is orphaned by cluster removal
- No ingestion path references clusters

---

### Safety Test 3 — Naming Independence Test

> The system must function with all cluster labels removed.

Expected behavior:
- Navigation still works
- UI does not collapse
- No storage keys reference names

Names, if present, are annotations only.

---

### Safety Test 4 — Navigation Optionality Test

> Clusters must not become the primary navigation surface.

Expected behavior:
- Users can ignore clusters entirely
- Fragment-first navigation remains complete

If users *must* go through clusters, the point of no return has been crossed.

---

## III. UI Metaphors for Soft Clusters (No New Data Structures)

The following UI metaphors allow **soft structure exploration** without introducing
clusters as stored objects.

---

### 1. “Highlight Clouds”

- When viewing a fragment, related fragments are *highlighted*, not grouped
- Highlights fade with distance
- No boundaries, no containers

Effect:
- Suggests proximity without asserting membership

---

### 2. “Focus Lenses”

- User temporarily adjusts a similarity threshold
- UI re-renders fragments that come into focus
- Resetting the lens returns to baseline view

Effect:
- Structure feels adjustable and provisional

---

### 3. “Transient Piles”

- UI allows temporary piles during a session
- Piles disappear on refresh
- No persistence, no identity

Effect:
- Encourages exploration without commitment

---

### 4. “Heat Fields”

- Density of related fragments shown via intensity
- No edges, no groups
- Only gradients

Effect:
- Communicates recurrence without grouping

---

## IV. Final Readiness Rule

> **Stage 2 may only exist if it can be removed without regret.**

If implementing soft structure creates fear of deletion, it has been implemented too deeply.

This document defines readiness, not momentum.
