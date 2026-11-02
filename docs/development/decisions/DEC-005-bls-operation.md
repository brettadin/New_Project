# DEC-005 — Initial Photometric Operation: BLS Transit-Period Detection

**Record ID:** DEC-005
**Date:** 2026-11-02
**Status:** Pending
**Decision Maker:** User

## 1. Decision Required

Select the initial photometric/time-series analytical operation for the first vertical slice.

## 2. Context

DEC-001 (D2) approved photometry and time-series analysis as the initial scientific capability, framed as exoplanet transits and stellar variability. The first implementation uses one small, scientifically defensible analytical workflow, not the complete §3.4 capability.

Two candidate operations were compared: Lomb–Scargle periodogram (sinusoidal periodic signals) and Box Least Squares (BLS) (transit-shaped periodic signals). NASA Exoplanet Archive documentation explicitly states L-S "is not optimal for detecting signals from transiting exoplanets" and BLS "is not optimal for detecting signals from pulsating variables."

## 3. Options

- **Option A: BLS transit-period detection.** Optimized for box-shaped transit signals. Parameters: period, duration, depth, reference time. Serves exoplanet science (§2.2.2). More sensitive to period grid sampling than L-S.
- **Option B: Lomb–Scargle periodogram.** Optimized for sinusoidal periodic signals. Parameters: frequency, power. Serves stellar variability (§2.2.4). Not optimal for transit-shaped signals.

## 4. Recommendation

Option A: BLS transit-period detection as the initial photometric operation. Recommended because:
- BLS is designed for transit-shaped (non-sinusoidal) signals, matching exoplanet transit light curves
- Serves exoplanet science, an initial priority discipline (§2.2.2)
- Well-established method (Kovacs et al. 2002) with Astropy implementation
- Clear validation path against published exoplanet periods (e.g., Kepler-10b: 0.837491225 days)

**Lomb–Scargle is documented as a future capability**, not excluded or abandoned, for approximately sinusoidal periodic signals including stellar variability (§2.2.4).

## 5. Consequences

**Benefits:** Optimal method for transit detection; serves exoplanet priority discipline; well-established with published reference; clear validation benchmark.
**Drawbacks:** Defers stellar variability workflow to later stage; period grid more sensitive than L-S; requires careful duration parameter selection.
**Risks:** Kepler-10b FITS file not yet inspected (evidence gap); validation tolerances not yet established.
**Dependencies:** Requires representative dataset (Kepler-10b candidate pending file inspection); D1 platform approval before Stage 2 implementation.

## 6. Scope

Selects BLS as the initial photometric operation for the first vertical slice. Lomb–Scargle remains a future capability for stellar variability. Does not implement transit fitting, phase curves, or secondary eclipses (deferred per DEC-002).

## 7. Confirmation

User approval requested for BLS as initial photometric operation, with Lomb–Scargle documented as future capability.

## Approval Record

- **User response:** Pending (awaiting user decision)
- **Conditions or limitations:** Lomb–Scargle must remain part of long-term application as future capability for approximately sinusoidal periodic signals, including stellar variability
- **Date of response:** Not yet provided
- **Affected requirements:** §3.4, §3.4.8, §12.5, §5.4, §5.6
- **Affected roadmap items:** Stage 2 analytical operation
- **Required follow-up actions:** Authorize Foundation §3.4.8 addition documenting Lomb–Scargle as future capability

## Related Records

- Preceding decisions: DEC-001 (D2 - photometry capability)
- Follow-up decisions: None at this stage
- Related problem records: None
- Related research reviews: REVIEW-001 (BLS method research)
