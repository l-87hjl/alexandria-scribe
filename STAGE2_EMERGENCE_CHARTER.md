# Stage 2 Emergence Charter

**Status:** Design-only (no implementation)

This document defines the **conditions, permissions, and limits** of *Stage 2 Emergence* in Alexandria-Scribe.

Stage 2 exists to allow **soft structure to appear** *without collapsing ambiguity* or prematurely committing to ontology.

This charter is normative.

---

## Purpose of Stage 2

Stage 1 proved that fragments can exist, interact, and be recombined **without meaning being imposed by the system**.

Stage 2 explores a narrow, careful expansion:

> **From resemblance → to provisional grouping**

But *not* to naming, taxonomy, or authority.

---

## Core Principle

> **Stage 2 may surface patterns, but must not decide what they are.**

Meaning remains:
- Human-interpreted
- Reversible
- Contestable

---

## Preconditions (Must Be True Before Stage 2)

Stage 2 may not begin unless all of the following are satisfied:

1. **Stage 1 is frozen** (see `STAGE1_FROZEN.md`)
2. **Safety tests are passing**
3. **No ontology tables exist**
4. **Fragments are immutable**
5. **Similarity remains non-persistent by default**

If any precondition fails, Stage 2 is invalid.

---

## What Stage 2 Allows (Strictly Limited)

### 1. Soft Clustering (Ephemeral)

The system may:
- Group fragments based on similarity signals
- Present groupings as *views*, not objects
- Recompute clusters dynamically

Constraints:
- Clusters are **not stored**
- Clusters have **no IDs**
- Clusters cannot be referenced later

---

### 2. Provisional Group Labels (Human-Only)

Humans may:
- Temporarily label a view
- Use labels as **personal annotations**

Constraints:
- Labels are not stored as system concepts
- Labels are not reused automatically
- Labels never affect similarity computation

---

### 3. Perspective-Based Exploration

Stage 2 may introduce UI metaphors such as:
- Lenses
- Focus views
- Overlays

These metaphors:
- Reorder perception
- Do not alter memory
- Do not create structure

---

## Explicitly Disallowed in Stage 2

The following actions are forbidden and constitute a **point of no return**:

- Persisting clusters
- Naming concepts as first-class objects
- Creating concept tables
- Establishing parent/child relationships
- Using clusters to affect ingestion
- Allowing clusters to feed back into similarity

If any of these occur, Stage 2 has failed.

---

## Data Model Constraints

During Stage 2:

- The `fragments` table **must remain unchanged**
- No new tables representing meaning may be added
- Any new tables must be:
  - UI-only
  - Session-scoped
  - Explicitly discardable

---

## Tests Required Before Implementation

Before *any* Stage 2 code is written, the following must exist:

- Tests proving clusters are not persisted
- Tests proving labels do not affect similarity
- Tests proving fragment immutability still holds

No tests → no Stage 2.

---

## Human Authority Clause

Stage 2 explicitly affirms:

> The system does not know what something *is*.

It may only:
- Suggest
- Surface
- Invite

Interpretation remains human.

---

## Exit Criteria (Transition to Stage 3)

Stage 2 may only advance when:

- Clear rules for naming are defined
- Governance for concept persistence exists
- Multiple users validate emergence behavior
- Reversibility has been demonstrated under scale

---

## Summary

> Stage 2 is a controlled experiment in *noticing without declaring*.

If the system ever feels confident about meaning, Stage 2 has gone too far.
