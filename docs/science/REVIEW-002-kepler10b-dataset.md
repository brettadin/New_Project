# REVIEW-002 — Kepler-10b (KIC 11904151) Dataset Profile

**Record ID:** REVIEW-002
**Date:** 2026-11-02
**Researcher:** AI Development Partner
**Type:** Scientific research

## Research Question

Is Kepler-10b (KIC 11904151) a suitable representative dataset and BLS benchmark for the initial photometric workflow?

## Sources Consulted

| Source | Location | Relevance |
|---|---|---|
| NASA Exoplanet Archive KOI table | exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI | Kepler-10b parameters, period, epoch, duration |
| NASA Exoplanet Archive overview page | exoplanetarchive.ipac.caltech.edu/overview/Kepler-10 | Confirmed planet status, published period |
| MAST Kepler Data Products Overview | exoplanetarchive.ipac.caltech.edu/docs/Kepler_Data_Products_Overview.md | FITS format, file structure, SAP vs PDCSAP |
| MAST notebooks (Kepler light curves) | spacetelescope.github.io/mast_notebooks/ | FITS extensions, column names, time system |
| Kepler Data Release Notes | archive.stsci.edu/kepler/release_notes/ | Quality flag definitions, file format details |

## Findings

### Kepler-10b parameters (verified from NASA Exoplanet Archive)

| Parameter | Value | Source |
|---|---|---|
| KIC ID | 11904151 | Exoplanet Archive KOI table |
| KOI designation | K00072.01 | Exoplanet Archive KOI table |
| Kepler name | Kepler-10 b | Exoplanet Archive KOI table |
| Status | Confirmed planet | Exoplanet Archive |
| Discovery method | Transit | Batalha et al. 2011 |
| Published orbital period | 0.837491225 ± 3.03e-07 days | Exoplanet Archive (q1_q17_dr25) |
| Transit epoch (BKJD) | 131.574858 ± 0.000282 | Exoplanet Archive (q1_q17_dr25) |
| Transit duration | 1.796 hours | Exoplanet Archive KOI table (q1_q17_dr25) |
| Transit depth | 0.000149 relative flux | Exoplanet Archive KOI table (q1_q17_dr25) |
| Planet radius | 1.43 ± 0.08 R⊕ | Exoplanet Archive KOI table |
| Number of quarters | 11 quarters with data | Exoplanet Archive KOI quarters field |
| Number of transits | 1245 (q1_q17_dr25 solution) | Exoplanet Archive KOI table |

### File format (verified from actual file inspection)

| Property | Verified Value | Source |
|---|---|---|
| Format | FITS binary table | Direct file inspection |
| File naming | kplr<kepid>-<stop_time>_llc.fits | Direct file inspection |
| Extensions | Primary HDU + light curve table extension (HDU1); HDU2 not exhaustively characterized | Direct file inspection |
| Time column | TIME (BJD − 2454833), 64-bit float | Direct file inspection |
| Flux columns | SAP_FLUX, PDCSAP_FLUX, 32-bit float | Direct file inspection |
| Uncertainty columns | SAP_FLUX_ERR, PDCSAP_FLUX_ERR, 32-bit float | Direct file inspection |
| Quality column | SAP_QUALITY bitmask, 32-bit int | Direct file inspection |
| Cadence column | CADENCENO, 32-bit int | Direct file inspection |
| Time units | Days | Direct file inspection |
| Flux units | e⁻/s | Direct file inspection |

### File inspection status

**INSPECTED.** A Kepler-10b Quarter 0 long-cadence FITS light-curve file (`kplr011904151-2009131105131_llc.fits`) was downloaded from the STScI archive and inspected at the FITS-header and light-curve-table level. The primary header and HDU1 were examined and verified. HDU2 and other extensions were not exhaustively characterized.

### Verified file characteristics

| Attribute | Value | Source |
|---|---|---|
| Target | KIC 11904151 (Kepler-10b) | Primary header OBJECT + KEPLERID |
| Quarter | Q0 | Primary header QUARTER |
| Cadence | Long cadence | Primary header OBSMODE |
| Observations | 476 cadences | LIGHTCURVE extension NAXIS2 |
| Time span | ~9.7 days (BJD − 2454833: ~120.54 to ~130.25) | LIGHTCURVE header TSTART/TSTOP |
| Time system | BJD, BJDREFI=2454833, TIMESYS=TDB | LIGHTCURVE header |
| SAP_FLUX range | ~532,355 to ~532,944 e⁻/s | Direct data inspection |
| PDCSAP_FLUX_ERR | ~20.6 e⁻/s (sampled, non-zero) | Direct data inspection |
| SAP_QUALITY | Mostly zero (clean cadences), some non-zero flags present | Direct data inspection |
| File size | 77,760 bytes | Direct file inspection |

**Note:** This is Quarter 0 (~10 days), a short commissioning quarter. Multiple additional quarterly files exist in the same archive directory for extended baseline if needed.

### Time system precision

Kepler time values use Barycentric Julian Date (BJD). The header contains BJDREFI (=2454833) and BJDREFF (=0.00000000) keywords. Barycentric Kepler Julian Date (BKJD) = BJD − 2454833. Verified from actual file header.

### SAP vs PDCSAP

- **SAP_FLUX:** Raw simple aperture photometry flux. Best for raw data preservation/provenance.
- **PDCSAP_FLUX:** SAP corrected for instrumental systematics via Co-trending Basis Vectors (CBVs). Pipeline's best estimate of intrinsic variability. Preferred for exoplanet detection.
- **PDCSAP_FLUX is not "relative flux"** — raw values are in electrons/second (e⁻/s). Any normalization to relative flux would be an explicit derived-data operation.

### Quality flag handling

Kepler light curve files contain SAP_QUALITY bitmask. Per Kepler Data Release Notes:
- Most flags are informational, not data-invalidating
- Bit position 8 corresponds to numeric value 256 (2^8, if 0-indexed); do not confuse bit position with numeric mask value
- Nonzero quality flags do not automatically mean the cadence must be discarded; distinguish informational flags from potentially invalidating flags
- NaN values indicate missing data
- **Justified bitmask policy needed:** Document which bits indicate unusable data vs informational flags; preserve original quality values; record the filtering policy in derived-data provenance

### Assessment

| Purpose | Suitability | Basis |
|---|---|---|
| Data import demonstration | Suitable | Verified from actual file inspection; well-defined columns and headers |
| Data preservation/provenance | Suitable | Original file preserved separately; header metadata available |
| BLS period recovery benchmark | Candidate | Published period with high precision; short period (~0.84 days) gives ~11-12 expected transits in Q0's ~9.7-day baseline |
| Negative control | Not suitable as-is | A random quarter without known planet is not a definitive negative control; need synthetic noise-only data |

**Caveat:** This is Quarter 0 (~10 days), a short commissioning quarter. Suitable for targeted period-recovery testing around the known period, but not sufficient for blind transit discovery. Multiple additional quarterly files exist in the same archive directory for extended baseline if needed.

### Assumptions

- None remaining: all format, column, and header characteristics verified from actual file inspection

### Limitations

- Quarter 0 baseline (~9.7 days) is shorter than regular quarters (~90 days); limits period precision and broader period search capability
- HDU2 and other extensions not exhaustively characterized
- Targeted BLS recovery has not yet been demonstrated; requires implementation and testing against actual data

## Unresolved Questions

| Question | Why unresolved | Revisit condition |
|---|---|---|
| None remaining for dataset inspection | File obtained and inspected; all key characteristics verified | N/A |

## Recommendation

Kepler-10b Q0 remains a **candidate** representative dataset and BLS benchmark. File inspection completed successfully; dataset is suitable for targeted period-recovery testing around the known published period (0.837491225 days). AMATEUR retained as possible secondary import/visualization example (not primary benchmark).

## Related Records

- Related decisions: None yet (dataset selection pending file inspection)
- Related problem records: None
- Related research reviews: REVIEW-001 (BLS method)
