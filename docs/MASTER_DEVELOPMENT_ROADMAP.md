# Master Development Roadmap

**Canonical location:** `docs/MASTER_DEVELOPMENT_ROADMAP.md`
**Status:** Authoritative development overview
**Last updated:** 2026-11-02
**Governed by:** `docs/Foundation/` (read-only), `AGENTS.md`

## Purpose

Single authoritative source for overall development planning and progress (§10.3.4). Tracks stages, priorities, dependencies, and status. Distinguishes proposed, approved, ready, in progress, blocked, completed, and deferred work (§12.6.11).

## Approved Initial Decisions

| ID | Decision | Status | Basis |
|---|---|---|---|
| D2 | First scientific capability: photometry and time-series analysis | Approved | §3.4, §2.2 |
| D3 | Initial scope boundary: four categories (included / deferred / architectural consideration now / outside scope) | Approved | §12.5, §10.4.2 |
| D4 | Initial deployment: single-user local, private-by-default projects, permission-aware data model; multi-user deferred | Approved | §8.11, §9.1.2, §9.8.2 |
| D5 | Technology stack: Python 3.13 primary language; PySide6 desktop UI; NumPy/SciPy/Astropy/Matplotlib scientific stack; pytest; venv | Approved (delegated to OpenCode) | §9.1.9, §12.3, §10.4.2 |

## Decisions Requiring Research Before Approval

| ID | Decision | Status | Blocks | Required Research |
|---|---|---|---|---|
| D1 | Initial platform direction | Approved (desktop-first) | No longer blocks Stage 2 | T1: platform evaluation vs §9.1.9 criteria (complete — REVIEW-003) |

## Decisions Deferred

| ID | Decision | Status | Deferred Until | Basis |
|---|---|---|---|---|
| D6 | Data storage model | Provisional local-file approach permitted for the first vertical slice only; subject to documented limitations and preservation of original data; does not constitute approval of a formal storage architecture; formal D6 decision deferred | After first vertical slice | §9.4, §10.4.1, §10.4.2 |
| D7 | External resources for first integration | Deferred | Stage 1 evaluation | §12.4.11 |
| D9 | Application name and acronym | Deferred | After scope approval | §1.1.3–1.1.4 |
| D10 | Project licence and distribution model | Deferred | Before Stage 7 | §4.11, §9.7.1 |

## Decisions Already Resolved by Foundation or AGENTS.md

| ID | Decision | Resolution | Basis |
|---|---|---|---|
| D8 | Documentation structure | Index `docs/Foundation/` as authoritative requirements; no duplicate `requirements/` directory | §11.2.1 (proposed, not mandatory); AGENTS.md |
| D11 | Foundation change governance | Foundation read-only; changes require explicit user authorization + §10 approval boundaries | AGENTS.md; §11.5.2, §11.5.7 |

## Development Stages

| Stage | Objective | Status | Depends On | Produces |
|---|---|---|---|---|
| **0. Documentation & decision baseline** | README index, roadmap, development log, templates, decision records (D2–D4), project identity record, unresolved-questions register, Git init | Approved / Complete | User approval of D2–D4 | `docs/README.md`, roadmap, log, templates, decision records, identity register, unresolved-questions register |
| **1. Targeted research** | T1 platform evaluation vs §9.1.9 criteria; BLS vs Lomb–Scargle comparison; Kepler-10b dataset profile; D1 and BLS operation decision records prepared | Complete (research/documentation only) | Stage 0 complete | Research records (`docs/science/`, `docs/technical/`), D1 decision record (DEC-004, Approved), BLS operation decision record (DEC-005, Approved), .gitignore |
| **2. First useful scientific vertical slice** | Project create/open/save; import one light-curve dataset; preserve original + provenance; table + light-curve visualization; one photometric operation (BLS) with uncertainty; record operation and parameters | In Progress | Stage 1 complete; D1 approval (obtained); BLS operation approval (obtained); S1–S4, S7 research; Kepler-10b file inspection (resolved) | End-to-end reproducible light-curve analysis on real data |
Task 2.1 subtasks: 2.1.1 — Complete; 2.1.2 — Complete; 2.1.3 — Complete; 2.1.4 — Complete; 2.1.5 — Complete; 2.1.6 — Pending
| **3. Reproducibility (user-facing)** | Analysis-record inspection, replay, portable analysis packages, project export/import | Pending | Stages 2 | Reproducible investigations |
| **4. First external integration** | One archive, metadata-first retrieval, caching, licence/auth (D10 must be approved first) | Pending | Stage 3; D10 approval | Retrieval of real archive data |
| **5. Contextual education slice** | Method explanations attached to the capability | Pending | Stage 2 | In-context learning support |
| **6. Review & next-capability decision** | Formal review per §12.7.8; choose spectroscopy vs imaging vs planetary next | Pending | Stages 2–5 | Updated roadmap and next-scope proposal |

## Priorities

**Initial implementation priorities (§12.5):**
1. Foundational: data model, provenance, operation recording, project lifecycle
2. High: first photometric/time-series workflow (single validated operation)
3. Medium: additional formats, visualization enhancements
4. Deferred: spectroscopy, imaging, modelling, orbital analysis, AI-assisted analysis, community features

## Outstanding Research

| ID | Question | Blocks | Priority | Status |
|---|---|---|---|---|
| S1 | Which photometric/time-series methods are scientifically appropriate? | Stage 2 (analytical operation) | Blocking | Complete (REVIEW-001) |
| S2 | Uncertainty, bias, and failure modes of each method? | Stage 2 | Blocking | Complete (REVIEW-001) |
| S3 | Benchmark datasets and published results for validation? | Stage 2 | Blocking | Complete (REVIEW-002; file inspected) |
| S4 | Metadata, units, time systems, coordinate conventions required? | Stage 2 | Blocking | Complete (REVIEW-002; file inspected) |
| S7 | Complete research workflow from discovery to recorded result? | Stage 2 | Blocking | Complete (REVIEW-001, REVIEW-002) |
| T1 | Initial platform vs §9.1.9 criteria? | D1, Stage 2 | Blocking | Complete (REVIEW-003) |
| T2 | Runtime/language strategy for scientific computing? | D5 | Approved | Complete (DEC-006: Python 3.13 + PySide6 + scientific stack) |
| T3–T12 | Other technical questions | Various | Deferred | Open |

## Known Risks and Blockers

| ID | Description | Impact | Mitigation |
|---|---|---|---|
| R1 | D1 platform approved (desktop-first) | Resolved | DEC-004 Approved |
| R2 | BLS operation approved | Resolved | DEC-005 Approved |
| R3 | Kepler-10b FITS file inspected (Q0 quarter) | Resolved | File downloaded from STScI archive; header and light-curve table verified |
| R4 | Storage architecture not finalized (D6 deferred) | Low for first slice | Provisional local-file approach with documented limitations |
| R5 | D5 technology stack approved with delegation | Resolved | DEC-006 Approved; OpenCode selects specific frameworks |

## Consultation Requirements

This roadmap must be consulted (§10.3.4):
- Whenever beginning a new development session
- Before planning or starting new implementation work
- When determining development priorities
- Before recommending the next development task
- Whenever dependencies, blockers, or development direction require reassessment
