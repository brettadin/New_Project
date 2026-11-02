# DEC-004 — D1: Initial Platform Strategy

**Record ID:** DEC-004
**Date:** 2026-11-02
**Status:** Approved
**Decision Maker:** User

## 1. Decision Required

Select the initial platform strategy for the application. Options: desktop-first, browser-first, or local-first web.

## 2. Context

Foundation §9.1.1 establishes hybrid web-and-desktop as the preferred long-term direction. §9.1.2 requires beginning with one primary platform and preserving the ability to introduce the second platform without substantial architectural restructuring. §9.1.9 establishes ten selection criteria for the initial platform.

D1 (platform strategy) is distinct from D5 (technology stack). D1 determines where computation runs and where data is stored; D5 determines specific languages, frameworks, and libraries. D5 remains deferred.

## 3. Options

- **Option A: Desktop-first.** Local application with computation and data storage on the user's machine. Full local file system access, native scientific computing performance, offline operation by default.
- **Option B: Browser-first.** Web application with computation and data storage in the browser or on remote servers. Zero installation, but constrained by browser sandbox and JavaScript execution limits.
- **Option C: Local-first web.** Web application with local file access via browser storage APIs and File System Access API. Data stays on device, but browser storage APIs have incomplete cross-browser support.

## 4. Recommendation

Option A: Desktop-first. Best satisfies §9.1.9 criteria for scientific computing performance, local system access, offline functionality, and future hybrid compatibility. Scientific logic can be exposed via API to a future web platform (§9.1.2).

**User decision: Approved.** Desktop-first is the initial platform strategy. D5 technology stack (specific frameworks, libraries) remains separate and deferred.

## 5. Consequences

**Benefits:** Full local file access, native scientific computing, offline by default, no hosting costs, scientific logic portable to future web platform.
**Drawbacks:** Requires local installation; packaging and dependency management; platform-specific build considerations.
**Risks:** No implementation testing performed; framework integration patterns not empirically evaluated; cross-platform compatibility not tested.
**Dependencies:** D5 (technology stack) deferred until after D1 approval.

## 6. Scope

Decides platform strategy only. Does not select technology stack, frameworks, or libraries (D5 deferred). Preserves ability to introduce second platform later (§9.1.2).

## 7. Confirmation

User approved desktop-first as the initial platform strategy.

## Approval Record

- **User response:** Approved
- **Conditions or limitations:** D5 technology stack remains separate and deferred; no specific framework (Electron, Tauri, Wails, Python GUI, or other) selected as part of this decision
- **Date of response:** 2026-11-02
- **Affected requirements:** §9.1, §9.1.9, §10.4.2
- **Affected roadmap items:** Stage 2 (no longer blocked by D1; now unblocked subject to other gates)
- **Required follow-up actions:** None; D5 remains deferred

## Related Records

- Preceding decisions: DEC-001 (D2 - photometry capability), DEC-003 (D4 - deployment model)
- Follow-up decisions: D5 (technology stack, deferred)
- Related problem records: None
- Related research reviews: REVIEW-003 (T1 platform evaluation)
