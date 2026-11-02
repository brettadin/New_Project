# DEC-001 — First Scientific Capability: Photometry and Time-Series Analysis

**Record ID:** DEC-001
**Date:** 2026-11-02
**Status:** Approved
**Decision Maker:** User

## 1. Decision Required

Select the first scientific capability for the application's initial implementation.

## 2. Context

The Foundation defines multiple scientific capability areas (Section 3): spectroscopy, photometry/time-series, astronomical imaging, and others. The initial implementation must begin with a single, scientifically defensible capability that serves as a vertical slice exercising data → analysis → reproducible record (§12.5.1, §12.5.5). The choice determines all downstream research and architecture.

## 3. Options

- **Option A: Photometry and time-series analysis.** Explicitly cross-disciplinary (stellar variability, exoplanet transits, eclipses, periodic phenomena — §3.4). Serves two initial priority disciplines (exoplanet science §2.2.2, stellar astronomy §2.2.4) with one shared capability (§2.2.6). Well-established methods, tractable 1-D data, accessible public data, and well-characterized reference objects exist for validation (§3.4.13). Lower scientific risk for a first capability.
- **Option B: Spectroscopy and spectral analysis.** Equally cross-disciplinary and central to the long-term vision (§3.3), but requires heavier calibration, continuum handling, and reference line data. Higher scientific risk for a first capability.
- **Option C: Astronomical imaging and image analysis.** Foundational for observational astronomy (§3.5), but is a large subsystem (calibration, WCS, source detection, image measurement) that would delay a complete workflow.

## 4. Recommendation

Option A: Photometry and time-series analysis. Justification: cross-disciplinary reach, tractable data, established methods, accessible validation data, and it forces the hard foundational work (data model, provenance, units, records) to be done properly because those are exactly what a light-curve analysis needs (§3.4, §5.5).

## 5. Consequences

**Benefits:** One capability serves two priority disciplines; reduces scientific and technical risk for the first stage; establishes shared analysis services usable by later capabilities (§1.3.5, §6.3).
**Drawbacks:** Defers spectroscopy and imaging; spectroscopy and imaging remain as natural next expansions.
**Risks:** Scope pressure from the broad Foundation vision; must resist building Layer D/E before Layer B is sound.
**Dependencies:** Requires data model, provenance, units/time/coordinate handling, and operation recording from Stage 3 (§5.5).

## 6. Scope

Defines the initial scientific capability as photometry/time-series, framed as exoplanet transits and stellar variability (§2.2). The first implementation will use one small, scientifically defensible analytical workflow, not the complete §3.4 capability. All other capability areas (spectroscopy, imaging, modelling, etc.) are deferred to later stages.

## 7. Confirmation

User approved photometry and time-series analysis as the initial scientific capability.

## Approval Record

- **User response:** Approved
- **Conditions or limitations:** First implementation uses one small analytical workflow only; not the complete photometry capability
- **Date of response:** 2026-11-02
- **Affected requirements:** §3.4, §2.2, §12.5, §5.5
- **Affected roadmap items:** Stage 2 (First useful scientific vertical slice)
- **Required follow-up actions:** Complete S1–S4 and S7 research before Stage 2 analytical operation (§12.2)

## Related Records

- Preceding decisions: None
- Follow-up decisions: D3 (scope boundary), D4 (deployment model)
- Related problem records: None
- Related research reviews: None
