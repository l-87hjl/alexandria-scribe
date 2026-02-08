# Disassembler Ingestion — Multi‑File & ZIP Support (Stage 1 Safe)

This document defines the **canonical ingestion behavior** for the Disassembler.

It extends the existing Disassembler to support **multiple files and ZIP archives** while preserving all Stage 1 safety guarantees.

This document is normative.

---

## Core Principle

> **Ingestion captures raw material; it does not decide meaning.**

All ingestion paths must preserve ambiguity, provenance, and reversibility.

---

## Supported Upload Types

### Direct File Uploads (Multiple Allowed)

The Disassembler must accept **multiple files in a single upload**.

Supported formats:

- `.txt`
- `.md`
- `.csv`
- `.docx`
- `.pdf`

Each file is processed independently.

---

### ZIP Uploads

The Disassembler must also accept **ZIP archives**.

ZIP ingestion rules:

1. ZIP is unpacked server‑side
2. Nested directories are flattened (path preserved as metadata)
3. Each contained file is treated as an independent upload
4. Unsupported file types are skipped (logged, not failed)

> ZIP ingestion is equivalent to uploading all contained files at once.

---

## Ingestion Pipeline (All Formats)

All files — whether direct or from ZIP — pass through the same pipeline:

```
file → raw text extraction → conservative chunking → fragments
```

At no point may ingestion introduce:
- Concept labels
- Categories
- Ontology
- Hierarchy

---

## Format‑Specific Notes

### Plain Text (`.txt`, `.md`)

- Ingested verbatim
- Chunked only by size / line breaks

---

### CSV

Default behavior:

- Each row → one fragment
- Header row preserved as provenance metadata

No semantic interpretation of columns is allowed.

---

### DOCX

- Extract visible text only
- Ignore styling, headings, tables as structure
- Preserve document filename as provenance

DOCX structure must **not** become ontology.

---

### PDF

- Extract raw text in reading order
- Page numbers preserved as provenance metadata
- No section inference

#### Generated TOCs (Kiwi‑style PDFs)

Some PDFs append auto‑generated Tables of Contents.

Stage 1 handling:

- TOC text is ingested **by default**
- Parser may annotate fragments with:
  - `parser_note: generated_toc_detected`
- No automatic removal or suppression

Rationale:
- Removal is semantic judgment
- Preservation allows later reinterpretation

---

## Provenance Metadata (Required)

Each fragment created via ingestion must record:

- `source_filename`
- `source_type` (txt, pdf, docx, csv)
- `source_page` (if applicable)
- `ingestion_batch_id`
- Optional `parser_notes`

Provenance is informational only.

---

## Explicitly Disallowed

During ingestion, the system must NOT:

- Merge fragments
- Deduplicate content
- Assign topics
- Collapse repeated text
- Infer structure

All such actions are deferred to later stages.

---

## Safety Guarantees

- Ingestion is append‑only
- Files cannot modify existing fragments
- ZIP unpacking cannot escape sandbox
- Failed files do not block successful ones

---

## Summary

> The Disassembler accepts **messy reality** and preserves it intact.

If ingestion ever feels "helpful," it has gone too far.
