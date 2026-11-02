# REVIEW-001 — Box Least Squares (BLS) Periodogram Method

**Record ID:** REVIEW-001
**Date:** 2026-11-02
**Researcher:** AI Development Partner
**Type:** Scientific research

## Research Question

Which photometric/time-series analytical operation is most suitable as the initial capability for the first vertical slice, and what are its scientific principles, equations, required inputs, uncertainty handling, limitations, failure modes, and validation requirements?

## Sources Consulted

| Source | Location | Relevance |
|---|---|---|
| Astropy BLS Periodogram documentation | docs.astropy.org/en/stable/timeseries/bls.html | Mathematical model, usage, limitations, implementation |
| NASA Exoplanet Archive Periodogram Algorithms | exoplanetarchive.ipac.caltech.edu/docs/pgram/pgram_algo.html | Official archive description of L-S vs BLS suitability |
| Astropy Lomb-Scargle documentation | docs.astropy.org/en/stable/timeseries/lombscargle.html | L-S mathematical model and uncertainty handling |
| VanderPlas 2018 | ApJS 236:16, Understanding the Lomb-Scargle Periodogram | L-S statistical properties, caveats |
| Kovacs, Zucker, & Mazeh 2002 | A&A 391:369 (arXiv:astro-ph/0206099) | Original BLS paper |
| Foundation §3.4 | docs/Foundation/3.4_Photometry, Transits and Time-Series Analysis.md | Photometric capability requirements |
| Foundation §5.4 | docs/Foundation/5.4_Scientific Interpretation and Uncertainty.md | Scientific interpretation and uncertainty requirements |
| Foundation §5.6 | docs/Foundation/5.6_Validation, Error Detection and Quality Control.md | Validation requirements |

## Findings

### Lomb–Scargle vs Box Least Squares comparison

**Verified facts:**

1. **Lomb–Scargle (L-S)** is optimized for sinusoidal-shaped periodic signals. Applications include radial velocity data and searches for pulsating variable stars. **L-S is not optimal for detecting signals from transiting exoplanets**, where the shape of the periodic light curve is not sinusoidal. (Source: NASA Exoplanet Archive Periodogram Algorithms, official archive documentation)

2. **Box Least Squares (BLS)** is optimized for "box" or transit-shaped periodic signals. Applications include searches for transiting exoplanets or detached eclipsing binaries. **BLS is not optimal for detecting signals from pulsating variables or radial velocity exoplanets**, where the shape of the time-series data variations is sinusoidal. (Source: NASA Exoplanet Archive Periodogram Algorithms, official archive documentation)

3. **L-S mathematical model:** At each frequency f, fits y(t; f, θ) = θ₀ + Σ[θ₂ₙ₋₁·sin(2πnft) + θ₂ₙ·cos(2πnft)]. Standard normalization: P_standard(f) = (χ²_ref − χ²(f)) / χ²_ref, dimensionless, 0 ≤ P ≤ 1. (Source: Astropy L-S documentation)

4. **BLS mathematical model:** Models transit as periodic upside-down top hat with four parameters: period, duration, depth, reference time. Log-likelihood: log ℒ(P, τ, t₀) = −½Σ_in[(yₙ−y_in)²/σₙ²] −½Σ_out[(yₙ−y_out)²/σₙ²] + constant. (Source: Astropy BLS documentation)

5. **BLS period grid sensitivity:** BLS performance is more sensitive to period grid sampling than L-S. Coarse grids can miss the correct period. (Source: Astropy BLS documentation)

6. **L-S uncertainty handling:** False alarm probability (FAP) via Baluev (analytical upper bound), bootstrap (computationally expensive), Davies, or naive approximations. FAP is P(data \| noise-only), NOT P(noise-only \| data). Highest peak is not guaranteed correct, especially with aliasing. (Source: Astropy L-S documentation; VanderPlas 2018)

7. **BLS uncertainty handling:** Chi-squared likelihood with per-point uncertainties; compute_stats method for candidate vetting. Periodogram power distribution described by normal (Gaussian) distribution; p-values computed from mean and standard deviation. (Source: Astropy BLS documentation; NASA Exoplanet Archive)

### Scientific validity for first vertical slice

**BLS is recommended as the initial operation** because:
- Serves exoplanet science (§2.2.2), one of the four initial priority disciplines
- Designed for transit-shaped signals, which are non-sinusoidal
- Well-established method (Kovacs et al. 2002)
- Available in Astropy (maintained scientific library)
- Uncertainty handling via per-point chi-squared weighting
- Clear validation path against published exoplanet periods

**Lomb–Scargle is documented as a future capability** (not excluded) for approximately sinusoidal periodic signals including stellar variability (§2.2.4).

### Limitations and failure modes

1. **Aliasing:** Observing window creates aliases at f_alias = f_true + n·f_window
2. **Period grid sensitivity:** BLS more sensitive than L-S to grid coarseness; coarse grids can miss the correct period
3. **Non-sinusoidal signals:** Additional peaks from higher frequency components (relevant to L-S, not BLS)
4. **Observation errors:** Leakage of power from true peaks
5. **Duration binning:** BLS duration parameter affects results
6. **FAP interpretation:** FAP conditioned on null hypothesis; does not establish periodic signal correctness

### Validation requirements

- Compare BLS-recovered period against published period (Kepler-10b: 0.837491225 ± 3.03e-07 days)
- Software correctness separate from scientific validation (§12.2.7)
- Negative controls: noise-only data, shuffled flux values
- Positive controls: injected synthetic transit signals
- Document limitations where benchmarks unavailable (§12.2.7)

## Assumptions

- BLS implementation in Astropy is scientifically sound (unverified - depends on library quality)
- Kepler-10b published period is reliable reference (verified - from NASA Exoplanet Archive)
- Per-point uncertainties in Kepler PDCSAP_FLUX_ERR are usable (verified - from actual file inspection)

## Limitations

- Quarter 0 baseline (~9.7 days) is shorter than regular quarters (~90 days); limits period precision and broader period search
- BLS not yet implemented or tested
- Validation tolerances not yet established (empirical calibration required during Stage 2)

## Unresolved Questions

| Question | Why unresolved | Revisit condition |
|---|---|---|
| BLS implementation details for the application | Not yet implemented | Stage 2 implementation |
| Validation acceptance tolerances | Requires implementation testing against actual data | Stage 2 validation activity (not an entry blocker) |

## Recommendation

BLS transit-period detection as the initial photometric operation, serving exoplanet science. Lomb–Scargle documented as future capability for stellar variability. Kepler-10b Q0 as candidate representative dataset and benchmark (file inspected; suitable for targeted period-recovery testing).

## Related Records

- Related decisions: DEC-001 (D2 - photometry capability), DEC-005 (BLS operation selection)
- Related problem records: None
- Related research reviews: None
