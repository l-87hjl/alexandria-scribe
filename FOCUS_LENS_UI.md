# Focus Lens UI — Canonical Specification

This document specifies the **Focus Lens UI** for Stage 2 (Soft Structure), without introducing new data structures, persistence, or ontology.

The Focus Lens is a **pure view transformation** over existing Stage 1 similarity signals.

---

## 1. Purpose

The Focus Lens allows a user to *adjust how they look at fragments*, not to create or assign structure.

It exists to:
- Improve navigability
- Support exploration
- Preserve ambiguity

It must never:
- Create groups
- Name concepts
- Persist state

---

## 2. Architectural Constraints (Non-Negotiable)

- Read-only
- No schema changes
- No persistence of lens state
- No cluster or concept objects
- Operates entirely via query parameters

Deleting all similarity data must leave the UI functional.

---

## 3. Entry Point

The Focus Lens is accessed via the existing route:

```
GET /fragments?focus=<fragment_id>&sim=<threshold>
```

No new endpoints are introduced.

---

## 4. Fragment Detail Layout (Canonical)

### Visual Priority Order

1. Fragment content (primary)
2. Focus Lens control (secondary)
3. Related fragments (tertiary)

Fragment content must visually dominate the page.

---

## 5. Focus Lens Control

### Placement

- Rendered **below fragment content**
- Never above it

### UI Elements

- Label: **"Focus related fragments"**
- Control: similarity sensitivity slider
- Range: implementation-defined

### Language Rules

Allowed terms:
- Focus
- Related
- Similarity

Forbidden terms:
- Concept
- Cluster
- Category
- Topic
- Group

Language is enforcement.

---

## 6. Related Fragments Panel

### Behavior

- Appears only when `focus` is present
- Updates reactively as slider changes
- Displays fragment previews only

### Explicit Omissions

- No similarity scores shown
- No boundaries or containers
- No saved views

---

## 7. Reset Behavior

- A **Reset focus** action must be present
- Reset clears query parameters
- UI returns to fragment-only view

---

## 8. Safety Invariants

The UI is correct if and only if:

- Removing all similarity data disables the lens gracefully
- Users can ignore the lens entirely
- The system remains usable without ever engaging Focus Lens

---

## 9. Canonical Rule

> The Focus Lens may change perception, but must never create obligation.

This document is normative and must be consulted before any UI changes.
