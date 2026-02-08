# Recombulator UI — Export Workspace Specification

The Recombulator is a **web-accessible, temporary export workspace**.

It allows users to **assemble, weight, order, and export fragments** without creating structure, concepts, or persistent groupings inside the system.

This document is **design-only**. No implementation is implied.

---

## I. Purpose

> **The Recombulator exists to help humans compose outputs, not to help the system remember.**

It is explicitly oriented toward:
- Writing
- Reporting
- Publishing (e.g. Substack)

It is not a memory surface.

---

## II. Access Model (Web + Files)

### Web Accessibility

The Recombulator is exposed as a **web page**:

```
GET /recombulator
```

It is separate from `/fragments` and `/ingest`.

Entering the Recombulator is always an **explicit user action**.

---

### Upload / Download Orientation

The Recombulator supports **export-only file operations**:

#### Downloads (Primary)

- Single-file exports:
  - Markdown (`.md`)
  - Plain text (`.txt`)
  - JSON (`.json`)

- Multi-file exports:
  - ZIP archive containing:
    - `core.md`
    - `optional.md`
    - `sources.json`

No download action writes back to the system.

---

#### Uploads (Optional, Explicit)

Uploads into the Recombulator:
- Are treated as **external reference material**
- Do not automatically enter ingestion
- May be disassembled and re-ingested only via `/ingest`

The Recombulator itself does **not** preserve uploads.

---

## III. Data Model (Intentional Absence)

The Recombulator introduces:
- No tables
- No IDs
- No persistence
- No schema

All state is:
- Session-bound
- Disposable
- Reconstructable from fragments

Closing the page discards everything.

---

## IV. Core UI Regions

### 1. Source Fragments (Read-Only)

- Fragment list
- Search
- Optional similarity context
- Action: **Add to recombulator**

This does not imply grouping.

---

### 2. Assembly Surface (Central)

Fragments may be:
- Ordered
- Temporarily labeled:
  - `core`
  - `optional`

These labels are:
- UI-only
- Session-only
- Never persisted

---

### 3. Export Panel

Controls:
- Output format
- Optional free-text purpose ("Draft Substack article", etc.)

Actions:
- **Generate export**
- **Download**

---

## V. Export Semantics

Exports are:
- Derived
- Non-authoritative
- Disposable

They may be:
- Downloaded
- Copied
- Published externally

They do not affect the archive.

---

## VI. Explicit Bridge Back to Preservation

The only allowed reverse flow is:

> **Save as new fragment**

This action:
- Is explicit
- Requires confirmation
- Labels the fragment as `derived`
- Records source fragments

There is no automatic saving.

---

## VII. Safety Rules

The Recombulator is correct if:

- Closing it changes nothing
- Deleting all exports changes nothing
- Users can ignore it entirely

If using the Recombulator makes users anxious about losing data, it has failed.

---

## VIII. Canonical Rule

> **The Recombulator composes meaning without committing it.**

This document defines the maximum safe envelope for recombination.
