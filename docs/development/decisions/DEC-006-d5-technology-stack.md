# DEC-006 — D5: Technology Stack

**Record ID:** DEC-006
**Date:** 2026-11-02
**Status:** Approved
**Decision Maker:** User (with delegation to OpenCode for technology selection)

## 1. Decision Required

Select the technology stack for the desktop-first application, including programming language, UI framework, scientific libraries, and development tools.

## 2. Context

D1 (platform strategy) established desktop-first development. D5 determines which specific languages, frameworks, and libraries implement that strategy. D1 and D5 are distinct decisions: D1 is about where computation runs and where data is stored; D5 is about the tools used to build the application.

The user has approved Python as the primary language for scientific computing and application functionality. OpenCode is delegated authority to select additional languages, UI frameworks, libraries, SDKs, and tools when justified by project requirements. Individual technology choices do not require separate user approval.

## 3. Decision

**Python** is the approved primary language for scientific computing and application functionality.

**Technology selection is delegated to OpenCode**, subject to the following constraints:

- The application remains desktop-first (D1).
- The UI is not restricted to Python-based frameworks; OpenCode may select UI frameworks based on appearance, responsiveness, usability, maintainability, scientific integration, and future hybrid compatibility.
- Technology choices must be justified and documented.
- The user must be informed in advance when a choice requires local installation or configuration (runtime, SDK, framework, library, or external tool).
- Avoid unnecessary technology proliferation and complexity.
- PySide6 and PyQt6 are available candidates for UI development, not mandatory frameworks.
- This decision does not change the approved scientific scope, deployment direction, or other existing decisions.

## 4. Rationale

Python provides access to the mature scientific Python ecosystem (NumPy, SciPy, Astropy, Matplotlib) which is essential for photometric analysis. Delegating UI framework selection to OpenCode allows UI quality to be prioritized alongside implementation convenience, consistent with the user's emphasis on a polished, attractive, usable UI.

## 5. Consequences

**Benefits:** Mature scientific libraries; UI quality prioritized; no per-dependency approval burden; flexibility to choose best-fit tools.

**Drawbacks:** Technology proliferation risk if not managed; OpenCode must justify and document each choice.

**Risks:** Unnecessary complexity from multiple UI frameworks or language runtimes; licensing conflicts between dependencies.

**Dependencies:** D1 (desktop-first) must remain the platform strategy; D6 (storage) remains deferred under provisional local-file approach.

## 6. Scope

Decides that Python is the primary language and delegates technology selection to OpenCode. Does not select any specific UI framework, library, or tool. Does not change D1 (desktop-first), D2 (photometry), D3 (scope), D4 (single-user), or D6 (storage deferred).

## 7. Confirmation

User approved Python as primary language with delegation of technology selection to OpenCode.

## Approval Record

- **User response:** Approved
- **Conditions or limitations:** User must be informed in advance when a choice requires local installation or configuration; technology choices must be justified and documented; avoid unnecessary technology proliferation
- **Date of response:** 2026-11-02
- **Affected requirements:** §9.1.9, §12.3, §10.4.2
- **Affected roadmap items:** Stage 2 implementation
- **Required follow-up actions:** None; OpenCode proceeds with technology selection under delegation

## Related Records

- Preceding decisions: DEC-004 (D1 - platform strategy)
- Follow-up decisions: None (delegated to OpenCode)
- Related problem records: None
- Related research reviews: REVIEW-003 (T1 platform evaluation)
