# Planning Checklist (Canonical)

This checklist exists to coordinate **planning**, not implementation. Items here may be checked off without code changes if they are design- or documentation-complete.

---

## Stage 1 — Enforcement & Closure

- [ ] Write immutability enforcement tests
- [ ] Write append-only enforcement tests
- [ ] Add CI guard against ontology-like tables
- [ ] Add export-purity test (no DB writes during export)
- [ ] Declare Stage 1 mechanically frozen (tests passing)

---

## UX Closure (Stage 1-safe)

- [x] Disassembler with multi-file + ZIP upload
- [x] Upload progress + elapsed timer
- [x] Post-ingestion confirmation screen
- [x] Export-all as default action
- [ ] Optional: auto-download after ingestion

---

## Documentation

- [x] Stage 1 frozen (theory)
- [ ] Stage 1 frozen (enforced)
- [x] Stage 2 Emergence Charter (design-only)
- [ ] Canonical fragment file format documented
- [ ] Governance: artifact vs annotation vs export

---

## Stage 2 (Design-Only)

- [x] Stage 2 Emergence Charter
- [ ] Stage 2 Readiness Checklist
- [ ] Stage 2 Safety Tests (draft only)
- [ ] UI metaphors exploration (no data structures)

---

## Reassessment

- [ ] Pause implementation
- [ ] Use system on real corpus
- [ ] Identify pressure points before Stage 2
