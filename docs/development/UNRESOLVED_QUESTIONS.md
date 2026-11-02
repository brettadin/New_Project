# Unresolved-Questions Register

**Location:** `docs/development/UNRESOLVED_QUESTIONS.md`
**Governed by:** §13.1
**Last updated:** 2026-11-02

## Purpose

Records unanswered questions, incomplete requirements, and decisions requiring further investigation. Questions remain visible and traceable without being treated as established requirements (§13.1).

## Classification

Per §13.1.2:
- **Blocking:** Must be resolved before a particular development task or consequential decision can proceed.
- **Important:** Requires investigation or a decision before a relevant development stage.
- **Deferred:** Can remain unresolved until a later stage without preventing current work.
- **Future consideration:** Relevant to possible future capabilities or application direction.
- **Exploratory:** An interesting question or opportunity with no established development commitment.

## Register

| ID | Question | Classification | Affected Decision/Capability | Revisit Condition | Status |
|---|---|---|---|---|---|
| UQ-001 | Which initial platform best satisfies local data access, offline use, computation, and future hybrid deployment? | Blocking | D1 (platform), Stage 2 | T1 research complete (REVIEW-003); DEC-004 Approved (desktop-first) | Resolved (D1 Approved) |
| UQ-002 | What runtime/language strategy supports required scientific computing without duplicating mature libraries? | Deferred | D5 (stack) | After D1 approval | Open |
| UQ-003 | What data model represents objects, observations, datasets, derived products, operations, and relationships without premature complexity? | Important | D6 (storage), Stage 3 | Stage 1 research complete; provisional local-file approach approved | Open (D6 formal deferred) |
| UQ-004 | Which external archives/APIs are feasible, licensed, and stable enough for Stage 7 integration? | Deferred | D7 (external resources) | Stage 1 evaluation | Open |
| UQ-005 | What is the project licence and distribution model? | Important | D10 (licence) | Before Stage 7 | Open |
| UQ-006 | How should authentication and credentials be handled if/when external accounts are required? | Deferred | Multi-user / external integrations | After single-user foundation | Open |
| UQ-007 | Which photometric operation should be the initial workflow? | Blocking | BLS operation (DEC-005), Stage 2 | REVIEW-001 complete; DEC-005 Approved (BLS initial, Lomb–Scargle future) | Resolved (BLS Approved) |
| UQ-008 | Can a Kepler-10b FITS light-curve file be obtained and inspected? | Blocking | Representative dataset (REVIEW-002), Stage 2 import/validation | MAST download API errors; file not inspected | Open (evidence gap) |
| UQ-009 | What validation tolerances and acceptance criteria apply to BLS period recovery? | Important | Stage 2 acceptance criteria | Method and benchmark dataset must be established first | Open |

## Linkage

This register is linked to `docs/MASTER_DEVELOPMENT_ROADMAP.md` per §13.1.5. Blocking questions (e.g., UQ-008) prevent progression to dependent stages. UQ-001 and UQ-007 are resolved; UQ-008 remains the primary blocker for Stage 2.
