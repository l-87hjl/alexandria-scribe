# Recombulator — Design & Execution Spec (Stage 1 Safe)

The Recombulator is an **export-only workspace** for assembling fragments into artifacts **without writing anything back** into system memory.

This file is normative.

---

## Purpose

- Assemble selected fragments into:
  - Markdown documents
  - Plain-text reports
  - ZIP bundles
- Enable downstream use (Substack, editors, AI tools)
- Preserve fragment immutability

> **Recombination produces exports, not memory.**

---

## Non-Negotiable Constraints

- ❌ No fragment mutation
- ❌ No concept creation
- ❌ No persistence of recombined artifacts
- ❌ No feedback into ingestion

Exports are disposable artifacts.

---

## Core Capabilities (Stage 1)

### 1. Selection
- User selects fragments by ID
- Order is explicit and user-controlled

### 2. Assembly
- Concatenate fragment contents
- Optional separators (e.g. `---`)
- Optional headings (manual only)

### 3. Export
- Download as:
  - `.md`
  - `.txt`
- Optional ZIP for multi-file output

---

## Explicitly Deferred

- Named bundles
- Persistent collections
- Concept-aware assembly
- Templates beyond plain Markdown

---

## Safety Summary

> The Recombulator must feel powerful but forgetful.

If anything created here becomes addressable later, the design has failed.
