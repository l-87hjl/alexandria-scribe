# Disassembler UI — Web-Accessible Ingestion & Decomposition Workspace

The Disassembler is a **web-accessible upload and decomposition interface**.

It exists to **intake external artifacts (PDFs, documents, text bundles)**, break them into fragments, and prepare them for preservation — without interpretation, ontology, or structure.

This document is **design-only**. No implementation is implied.

---

## I. Purpose

> **The Disassembler turns external artifacts into preservable fragments.**

It is the inverse of the Recombulator:
- Disassembler → *many → fragments*
- Recombulator → *fragments → many*

The Disassembler is about **faithful intake**, not meaning.

---

## II. Web Accessibility Model

### Web Page

The Disassembler is exposed as a dedicated web page:

```
GET /disassembler
```

Entering the Disassembler is always an **explicit user action**.

---

### Upload Capabilities (Primary)

Supported uploads (conceptually):
- PDF files
- Word documents
- Markdown files
- Plain text files
- ZIP archives containing documents

Uploads are:
- Temporary until ingestion is confirmed
- Never automatically preserved

---

### Download Capabilities (Optional, Explicit)

The Disassembler supports **pre-ingestion downloads** for inspection and reuse.

#### Single-file downloads
- Normalized text (`.txt`)
- Fragment preview (`.json`)

#### Multi-file downloads (Recommended)

```
disassembly-preview.zip
├── fragments.json
├── source.txt
├── metadata.json
```

This allows:
- Review before ingestion
- External tooling
- Re-ingestion or recombination elsewhere

Downloading does **not** ingest anything.

---

## III. Disassembly Surface (UI Regions)

### 1. Upload Panel

- Drag-and-drop upload
- File list
- Remove / replace files

No processing occurs until explicitly requested.

---

### 2. Disassembly Controls

Controls may include:
- Chunk size (soft)
- Preserve paragraph boundaries (toggle)
- Preserve headings (toggle)

All controls affect **fragmentation only**, not meaning.

---

### 3. Fragment Preview Panel

- Shows proposed fragments
- Read-only
- Scrollable

Fragments at this stage:
- Have no IDs
- Are not yet artifacts

---

## IV. Ingestion Boundary (Critical)

Fragments become artifacts **only** when the user explicitly confirms ingestion.

### Canonical Action

> **Ingest fragments**

This action:
- Writes fragments to the fragment store
- Assigns fragment IDs
- Records provenance (source file, page, section)

No partial ingestion.

---

## V. Safety Rules

The Disassembler is correct if:

- Closing the page ingests nothing
- Downloading previews ingests nothing
- No interpretation is required to proceed
- Fragmentation is non-judgmental

---

## VI. Relationship to Other UIs

| UI | Role |
|---|---|
| `/disassembler` | Intake & decomposition |
| `/fragments` | Exploration |
| `/recombulator` | Composition & export |

These UIs are intentionally separate.

---

## VII. Canonical Rule

> **Nothing becomes memory until a human explicitly commits it.**

The Disassembler exists to make that commitment informed and reversible.
