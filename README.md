# Alexandria Scribe

A **preservation-first system** for ingesting, exploring, and recombining ideas without premature structure or ontology.

This repository contains:
- Architectural canon and governance documents
- UI specifications for all major system surfaces
- A live documentation/demo site via GitHub Pages
- A running backend application deployed on Render

---

## 🌐 Live Documentation & Demo Site (GitHub Pages)

**Canonical live link:**

```
https://l-87hjl.github.io/alexandria-scribe/
```

This site is served from the `/docs` directory and provides:
- The system landing page
- Conceptual UI overviews
- Design-only demonstrations of system surfaces

> If you are looking for “the web page”, this is it.

---

## ⚙️ Live Application (Render)

The actual running application is deployed on **Render**.

- The service is **not on the free tier**.
- There is **no cold-start / spin-up delay**.
- Requests should respond immediately under normal conditions.

This is important for debugging:

> If a page appears slow or unresponsive, it should be treated as a **real application issue**, not a hosting spin-up artifact.

(The common 30–60 second cold-start behavior associated with free tiers does **not** apply here.)

---

## 🧭 System Surfaces (Conceptual URLs)

These are the three major UI surfaces defined by the architecture. They are **real routes** in the deployed application.

| Surface | Purpose | Route |
|------|--------|-------|
| Disassembler | Intake & decomposition | `/disassembler` |
| Fragment Browser | Exploration & Focus Lens | `/fragments` |
| Recombulator | Composition & export | `/recombulator` |

---

## 🗂 Repository Layout (What Lives Where)

```
/               → runtime code (Flask app)
/docs           → GitHub Pages site (landing page, demos)
/templates      → HTML templates for the live app
```

GitHub Pages is intentionally mapped to `/docs` so the repository root remains free for the real application.

---

## 📜 Key Design & Governance Documents

If you want to understand *how the system is supposed to work*, start here:

- `ARCHITECTURAL_CANON.md` — non-negotiable architectural rules
- `STAGE2_EMERGENCE_CHARTER.md` — limits on emergence beyond similarity
- `GOVERNANCE_ARTIFACTS_AND_EXPORTS.md` — artifacts vs annotations vs exports
- `DISASSEMBLER_UI.md` — web-accessible intake design
- `FOCUS_LENS_UI.md` — exploration UI contract
- `RECOMBULATOR_UI.md` — export-only recombination workspace

These documents are normative.

---

## 🧠 How to Think About This System

- Nothing is preserved unless you explicitly ingest it
- Exploration never creates structure
- Recombination produces exports, not memory
- Meaning is optional and always revisable

---

## 🔗 Quick Reference (Save This)

- **Docs / landing page:** https://l-87hjl.github.io/alexandria-scribe/
- **Source repo:** https://github.com/l-87hjl/alexandria-scribe
- **Landing page source:** `docs/index.html`

If you ever forget where things live, start with the docs link above.
