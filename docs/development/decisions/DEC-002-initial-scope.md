# DEC-002 — Initial Scope Boundary (Four Categories)

**Record ID:** DEC-002
**Date:** 2026-11-02
**Status:** Approved
**Decision Maker:** User

## 1. Decision Required

Establish the initial scope boundary for the application's first implementation, organized into four categories.

## 2. Context

§12.5 requires that initial scope be researched, not chosen for ease, and that it be a genuine working foundation, not disconnected demonstrations or placeholders (§12.5.1). §12.5.4 establishes priority categories: Foundational / High / Medium / Low / Deferred / Future possibility / Rejected. The scope boundary must be documented in the Master Development Roadmap (§12.5.8). Long-term Foundation capabilities must not be classified as permanently excluded merely because they are deferred (§12.2.7, §12.7).

## 3. Options

- **Option A: Four-category scope boundary.** Classify all capabilities into: (1) Included in initial implementation, (2) Deferred to later stages, (3) Architectural consideration now without immediate implementation, (4) Outside intended scope only where supported by the Foundation.
- **Option B: Single exclusions list.** List what is out of scope, risking misclassification of deferred capabilities as permanently excluded.
- **Option C: No explicit scope boundary.** Allow scope to expand organically, violating §12.5.1 and §12.5.5.

## 4. Recommendation

Option A: Four-category scope boundary. This preserves the distinction between "deferred" and "rejected," avoiding the error of treating long-term Foundation capabilities as permanently excluded merely because they are not part of the first implementation (§12.5.7, §13.2).

## 5. Consequences

**Benefits:** Clear scope boundary; prevents scope creep; preserves future expansion options; satisfies §12.5 documentation requirement.
**Drawbacks:** Requires discipline to say "not now" to Foundation capabilities that are scientifically valid but not initial priority.
**Dependencies:** D2 (photometry first) determines what is included; D4 (single-user) determines what deployment features are included.

## 6. Scope

**Category 1 — Included in initial implementation:**
- Single-user local application
- Project create/open/save lifecycle
- Import of one light-curve format (CSV or FITS table, whichever the sample data uses)
- Original-file preservation and provenance recording (§5.5.1, §5.5.2, §4.4.1)
- Table view and interactive light-curve visualization (§3.4.1, §3.4.2)
- One photometric/time-series analytical operation (e.g., detrending or periodogram) with uncertainty reporting (§3.4.8, §3.4.10, §3.4.12)
- Operation recording: inputs, methods, parameters, execution order (§5.5.3, §5.5.4)
- Privacy-by-default projects (§8.11.2)
- Basic error handling

**Category 2 — Deferred to later stages:**
- Additional formats (VOTable, HDF5, ECSV, etc.) — §4.4.2 lists formats as examples, not simultaneous requirements
- Full photometry suite (transit fitting, phase curves, secondary eclipses) — §3.4.6, §3.4.7
- External archive integration — Stage 7
- User-facing replay/export packages — §5.5.14
- Contextual education slice — §7.4

**Category 3 — Architectural consideration now, without immediate implementation:**
- Permission-aware data model (roles in schema) — §8.11.3
- Platform-independent architecture preserving second platform option — §9.1.2
- Portable project format concept — §9.7
- Analysis record model designed for later replay — §5.5

**Category 4 — Outside intended initial scope (Foundation-supported):**
- AI-assisted scientific analysis — §5.7 explicitly "speculative future possibility, not an initial requirement"
- Community and collaboration features — §8 is supporting, not initial core
- Multi-user accounts and authentication — §9.8.2 "where applicable"; deferred per D4

## 7. Confirmation

User approved the initial scope boundary in four categories.

## Approval Record

- **User response:** Approved
- **Conditions or limitations:** Long-term Foundation capabilities deferred, not permanently excluded (§12.5.7, §13.2)
- **Date of response:** 2026-11-02
- **Affected requirements:** §12.5, §10.4.2, §8.11, §5.7, §9.8.2
- **Affected roadmap items:** Stage 0 through Stage 2
- **Required follow-up actions:** Record scope in roadmap; review at Stage 6 formal review (§12.7.8)

## Related Records

- Preceding decisions: DEC-001 (D2)
- Follow-up decisions: None at this stage
- Related problem records: None
- Related research reviews: None
