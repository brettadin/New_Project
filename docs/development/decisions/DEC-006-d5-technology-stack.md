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

**Python 3.13** is the approved primary language for scientific computing and application functionality.

**Selected technology stack:**

| Component | Selection | Rationale |
|---|---|---|
| Language | Python 3.13 | Approved by user (DEC-006); already installed (3.13.7); mature scientific ecosystem |
| Desktop UI | PySide6 | Qt6-based; LGPL/GPL dual licensing; Qt Company-backed; direct Python integration with Matplotlib QtAgg backend |
| Scientific computing | NumPy, SciPy | Standard numerical/scientific libraries |
| FITS handling | astropy.fits | Standard FITS library; handles primary header and binary table extensions |
| BLS implementation | astropy.timeseries.BoxLeastSquares | Well-established (Kovacs et al. 2002); documented API; uncertainty handling |
| Plotting/visualization | Matplotlib (QtAgg backend) | Standard scientific plotting; native Qt6 integration for light-curve visualization |
| Testing | pytest | Standard Python testing framework |
| Environment isolation | Python venv | Built-in; no extra installation required |

**Technology selection was delegated to OpenCode under DEC-006.** This selection is made under that delegation authority. No separate user approval is required for individual technology choices.

## 4. Rationale

Python provides access to the mature scientific Python ecosystem (NumPy, SciPy, Astropy, Matplotlib) which is essential for photometric analysis. PySide6 provides a Qt6-based desktop UI with direct integration to Matplotlib's QtAgg backend, enabling polished, responsive desktop visualization of light curves and periodograms without IPC complexity or a separate frontend codebase.

## 5. Consequences

**Benefits:** Mature scientific libraries; UI quality prioritized; single language stack; no per-dependency approval burden; direct Matplotlib integration via QtAgg backend.

**Drawbacks:** PySide6 packaging can add distribution complexity; Qt licensing (LGPL/GPL) has distribution implications.

**Risks:** PyQt6 was considered but rejected due to GPLv3 licensing restrictions for distribution; PySide6's LGPL/GPL dual licensing provides more flexibility. Technology proliferation risk if not managed; OpenCode must justify and document each choice.

**Dependencies:** D1 (desktop-first) must remain the platform strategy; D6 (storage) remains deferred under provisional local-file approach.

## 6. Scope

Decides that Python 3.13 is the primary language and PySide6 is the selected desktop UI framework, with NumPy, SciPy, Astropy, Matplotlib (QtAgg backend), pytest, and venv as supporting components. Does not select PyInstaller at this stage (packaging is a later concern). Does not change D1 (desktop-first), D2 (photometry), D3 (scope), D4 (single-user), or D6 (storage deferred).

## 7. Confirmation

User approved Python as primary language with delegation of technology selection to OpenCode. OpenCode has selected PySide6 as the desktop UI framework under that delegation authority.

## Approval Record

- **User response:** Approved (DEC-006, Python as primary language with delegation)
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
