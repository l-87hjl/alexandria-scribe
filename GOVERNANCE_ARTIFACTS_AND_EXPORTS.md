# Governance: Artifacts, Annotations, and Exports

This document defines **what kinds of things may exist in the system**, how they differ, and how information is allowed to flow between them.

It formalizes two decisions:

- **2B** — Synthesis outputs are exports by default
- **3B** — UI-created text may re-enter ingestion only via explicit, labeled action

This file is normative.

---

## I. Core Principle

> **Preservation is opt-in. Interpretation is provisional.**

Nothing enters long-term memory unless a human explicitly chooses to preserve it.

---

## II. Formal Definitions

### 1. Artifact (Preserved Memory)

**Definition:**
An artifact is any piece of information that has been **explicitly ingested** into the system and is subject to preservation guarantees.

**Properties:**
- Append-only
- Immutable
- Has a unique fragment ID
- Has provenance (source, time, authorship)
- Survives restarts and UI changes

**Examples:**
- Raw notes
- Disassembled PDF fragments
- Manually saved reflections
- Explicitly saved synthesis outputs

Artifacts are the **only authoritative records** in the system.

---

### 2. Annotation (Non-Preserved, Contextual)

**Definition:**
An annotation is **contextual text or structure** created during exploration that does *not* enter preservation by default.

**Properties:**
- Ephemeral
- Session-bound or view-bound
- No fragment ID
- May disappear without loss

**Examples:**
- Temporary UI notes
- Highlighting
- Focus Lens interactions
- Draft groupings or piles

Annotations assist thinking but do not constitute memory.

---

### 3. Export (Derived Output)

**Definition:**
An export is a **derived product** generated from one or more artifacts, intended for use *outside* the system unless explicitly re-ingested.

**Properties:**
- Derived, not primary
- Has no preservation guarantees by default
- May be copied, downloaded, or published externally

**Examples:**
- Reports
- Syntheses
- Outlines
- Articles (e.g., Substack drafts)

Exports do not affect the system unless a human chooses to ingest them.

---

## III. Default Flow Rules

### Canonical Flow

```
Artifacts  →  Exploration / UI  →  Exports
```

There is **no automatic reverse flow**.

---

### Explicit Reverse Flow (Allowed)

```
Exports / UI Text  →  (Explicit Save)  →  Artifacts
```

This reverse flow is allowed **only** under strict conditions.

---

## IV. Rules for Re-ingesting Exports or UI-Created Text

Re-ingestion is allowed if and only if:

1. The user performs an **explicit action**
2. The text is **clearly labeled as derived**
3. Provenance is recorded (what it came from)
4. Authorship is explicit (human / system)
5. The system does not do this automatically

There must be **no background saving**.

---

## V. Canonical UI Language — “Save as Fragment”

The following wording is normative.

### Button Label

> **Save as new fragment**

---

### Confirmation Copy (Required)

> This will save this text as a new fragment in your archive.
> 
> It will be preserved and treated like any other ingested material.
> 
> Source fragments will be recorded.

**Actions:**
- `Save fragment`
- `Cancel`

---

### Metadata Applied Automatically

When saved:
- `origin: derived`
- `source_fragments: [ids...]`
- `authorship: human` or `authorship: system`
- `note: user-confirmed preservation`

No editing of existing fragments is permitted.

---

## VI. Practical Workflow (Your Use Case)

This governance explicitly supports the following workflow:

1. Disassemble PDFs into fragments
2. Preserve all raw material as artifacts
3. Use Focus Lens and similarity to explore
4. Generate **exports** (reports, syntheses)
5. Optionally re-ingest selected exports or sections
6. Recombine preserved fragments around a theme (e.g. *covenant*)
7. Feed selected fragments into an article writer (e.g. Substack)

At every step:
- Core material remains separate
- Tangential material stays optional
- Nothing is forced into structure

---

## VII. Canonical Safety Tests (Governance-Level)

The system is governed correctly if:

- Deleting all exports has no effect
- Deleting all annotations has no effect
- Deleting all derived fragments leaves raw fragments intact
- No export enters preservation without explicit consent

---

## VIII. Final Rule

> **The system preserves what you choose to remember, not what it happens to generate.**

This document governs all future ingestion and synthesis behavior.
