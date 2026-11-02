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

### Expected file format (from documentation, NOT directly verified)

| Property | Expected value | Verification status |
|---|---|---|
| Format | FITS binary table (Q1–Q17 DR25) | Documentation only |
| File naming | kplr<kepid>-<stop_time>_llc.fits | Documentation only |
| Extensions | Primary HDU + light curve table + aperture mask | Documentation only |
| Time column | TIME (BJD, offset by BJDREF) | Documentation only |
| Flux columns | SAP_FLUX, PDCSAP_FLUX | Documentation only |
| Uncertainty columns | SAP_FLUX_ERR, PDCSAP_FLUX_ERR | Documentation only |
| Quality column | SAP_QUALITY (bitmask) | Documentation only |
| Cadence column | CADENCENO | Documentation only |
| Time units | Days | Documentation only |
| Flux units | e⁻/s | Documentation only |

### File inspection status

**NOT INSPECTED.** Multiple attempts to download a Kepler-10b FITS file from MAST failed:
- MAST API v0.1 download/file endpoint: 400 Bad Request
- MAST API v0 download/file endpoint: 400 Bad Request
- MAST Discovery Search API: 500 errors on all endpoints
- Direct archive.stsci.edu URL patterns: 404 errors
- Python not available in environment

The following characteristics are documented but NOT directly verified from an actual file:
- Exact header keywords and BJDREF values
- Whether PDCSAP_FLUX_ERR is populated for all cadences
- Actual quality flag distribution in a Kepler-10b quarter file
- Actual time coverage, cadence, gaps per quarter
- File size (the claim of ~55–60 MB per quarter is from documentation, not verified)
- Whether the file contains enough observations for BLS benchmark

### Time system precision

Kepler time values use Barycentric Julian Date (BJD). The header contains BJDREFI and BJDREFF keywords that together specify the reference offset. Barycentric Kepler Julian Date (BKJD) = BJD − 2454833. Documentation-derived; not verified from actual file.

### SAP vs PDCSAP

- **SAP_FLUX:** Raw simple aperture photometry flux. Best for raw data preservation/provenance.
- **PDCSAP_FLUX:** SAP corrected for instrumental systematics via Co-trending Basis Vectors (CBVs). Pipeline's best estimate of intrinsic variability. Preferred for exoplanet detection.
- **PDCSAP_FLUX is not "relative flux"** — raw values are in electrons/second (e⁻/s). Any normalization to relative flux would be an explicit derived-data operation.

### Quality flag handling

Kepler light curve files contain SAP_QUALITY bitmask. Per Kepler Data Release Notes:
- Most flags are informational, not data-invalidating
- Bit 8 (cosmic ray) indicates corrected data, not unusable
- NaN values indicate missing data
- **Justified bitmask policy needed:** Identify which bits indicate unusable data vs informational flags

### Assessment

| Purpose | Suitability | Basis |
|---|---|---|
| Data import demonstration | Candidate | Simple column structure documented; actual file not inspected |
| Data preservation/provenance | Candidate | Original files preserved separately from derived records |
| BLS period recovery benchmark | Candidate | Published period with high precision; short period gives many transits per quarter |
| Negative control | Not suitable as-is | A random quarter without known planet is not a definitive negative control; need synthetic noise-only data |

### Assumptions

- Quarterly FITS files are downloadable from MAST (unverified - download failed)
- PDCSAP_FLUX_ERR column exists and is populated (documentation-derived, not verified)
- BJDREF header keywords are present (documentation-derived, not verified)

### Limitations

- **Critical evidence gap:** No actual FITS file inspected
- Cannot verify file size, column data types, quality flag distribution, or uncertainty population
- Cannot confirm sufficient observations for BLS benchmark without file inspection
- Cannot verify time coverage per quarter or gap patterns

## Unresolved Questions

| Question | Why unresolved | Revisit condition |
|---|---|---|
| Actual Kepler-10b FITS file structure | MAST download API errors | Successful file download and inspection |
| Whether PDCSAP_FLUX_ERR is populated | Not verified from actual file | File inspection |
| Quality flag distribution | Not verified from actual file | File inspection |
| Sufficient observations per quarter for BLS | Not verified from actual file | File inspection |

## Recommendation

Kepler-10b remains a **candidate** (not confirmed) for representative dataset and BLS benchmark. Actual file inspection required before confirmation. AMATEUR retained as possible secondary import/visualization example (not primary benchmark).

## Related Records

- Related decisions: None yet (dataset selection pending file inspection)
- Related problem records: None
- Related research reviews: REVIEW-001 (BLS method)
