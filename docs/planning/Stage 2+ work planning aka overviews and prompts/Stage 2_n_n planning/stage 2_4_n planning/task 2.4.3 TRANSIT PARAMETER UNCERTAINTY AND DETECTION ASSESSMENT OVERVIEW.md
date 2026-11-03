# Task 2.4.3 — Transit Parameter Uncertainty and Detection Assessment

Stage: 2.4 — BLS Analysis and Uncertainty

Objective: Establish how reliable the transit parameters extracted by the BLS search are, estimate their uncertainties, and assess the statistical significance and reliability of detected transit-like signals.

Task 2.4.2 implements the BLS search engine and produces candidate results. Task 2.4.3 builds on those results by evaluating how much confidence can reasonably be placed in the extracted parameters and whether a candidate signal is distinguishable from noise.

The distinction is important: finding a periodic transit-like signal does not automatically mean that the signal is statistically significant or represents a real planet.

## 1. Review the Existing BLS Implementation

Before implementation, review:

- Completed Task 2.4.1 design.
- Task 2.4.2 BLS implementation.
- BLS result structures.
- Candidate parameter extraction.
- Search configuration and recorded parameters.
- Existing uncertainty fields and their handling.
- Current testing and validation conventions.

Determine what information the BLS implementation already provides and what additional calculations are needed.

The uncertainty implementation should consume existing BLS results rather than duplicate the search algorithm.

Identify any missing information that prevents reliable uncertainty assessment.

## 2. Establish Transit Parameter Uncertainty Requirements

Determine how uncertainty should be estimated for the parameters extracted by BLS.

The primary parameters are:

| Parameter | Description                                             |
| --------- | ------------------------------------------------------- |
| Period    | Estimated repeating interval of the transit-like signal |
| Epoch     | Estimated reference time of transit                     |
| Duration  | Estimated transit duration                              |
| Depth     | Estimated change in flux during transit                 |

The implementation should determine appropriate uncertainty estimates for these parameters.

Consider how uncertainty is affected by:

- Measurement noise.
- Measurement uncertainties.
- Observation cadence.
- Number of observations.
- Observation baseline.
- Transit coverage.
- Missing observations.
- Irregular sampling.
- Data quality.
- Search resolution.

The method must be scientifically justified and documented.

## 3. Evaluate Uncertainty Estimation Methods

Investigate appropriate methods for estimating transit parameter uncertainties.

Potential approaches may include:

- Bootstrap resampling.
- Monte Carlo simulations.
- Parameter perturbation.
- Local parameter-space exploration.
- Other statistically justified methods.

Evaluate their suitability for the application's BLS workflow.

Consider:

- Whether the method preserves the observation sampling.
- Whether measurement uncertainties are incorporated.
- Whether the method captures parameter correlations.
- Computational cost.
- Stability with small datasets.
- Behavior when the signal is weak or ambiguous.

Select methods according to the approved scientific design.

Do not assume that one uncertainty method is automatically appropriate for every dataset.

## 4. Address UQ-009: Empirical Calibration

An existing unresolved research item concerns empirical calibration of BLS uncertainty estimates and tolerances.

This task should explicitly investigate and address that issue.

The goal is to determine whether the uncertainty estimates behave appropriately when the true signal parameters are known.

Use controlled synthetic light curves with known:

- Periods.
- Transit epochs.
- Durations.
- Depths.
- Noise characteristics.

Compare recovered parameter estimates and reported uncertainties against the known input values.

Investigate whether the uncertainty method:

- Produces reasonable uncertainty ranges.
- Covers known parameter values at appropriate rates.
- Behaves consistently across different noise levels.
- Remains reliable under irregular sampling.
- Becomes unreliable under insufficient transit coverage.
- Underestimates or overestimates uncertainty in particular conditions.

Document calibration limitations and any conditions where estimates should not be trusted.

## 5. Implement Detection Assessment

Develop a method for assessing whether a detected BLS signal is statistically distinguishable from a noise-only dataset.

Investigate suitable statistical measures, including:

- BLS power.
- Signal-to-noise considerations.
- False alarm probability (FAP).
- Comparison against noise-only simulations.
- Other justified detection statistics.

The assessment should distinguish between:

1. A BLS candidate being detected.
2. A candidate being statistically distinguishable from the specified noise model.
3. A candidate being confirmed as a planet.

These are not equivalent conclusions.

### False alarm probability

If FAP is implemented, its interpretation must be carefully defined.

FAP is conditional on the specified noise-only null model. It is not the probability that a candidate period is correct, nor does a low FAP eliminate aliases or systematic effects.

Document:

- The null hypothesis.
- The noise model.
- The simulation or statistical procedure.
- The assumptions.
- The limitations.
- The interpretation of the resulting value.

Avoid presenting FAP as a direct probability that a signal is or is not planetary.

## 6. Evaluate Noise-Only Controls and Negative Cases

Develop a validation strategy for distinguishing genuine injected transit signals from noise.

Potential controls include:

- Synthetic noise-only datasets.
- Synthetic datasets with injected transit signals.
- Sampling-preserving simulations.
- Appropriate shuffling or resampling methods.

Controls should account for the observation cadence and uncertainty characteristics.

A dataset from a period without a known transit is not automatically a valid noise-only control. Other astrophysical signals and instrumental systematics may still be present.

Document why each control is appropriate and what it can establish.

## 7. Evaluate Aliases and Competing Signals

Detection assessment must account for the possibility that a strong BLS candidate is not the true underlying period.

Investigate:

- Harmonics.
- Period aliases.
- Competing periodogram peaks.
- Data gaps.
- Short observation baselines.
- Stellar variability.
- Instrumental systematics.
- Incomplete transit coverage.

Determine how these limitations should influence the assessment and warnings associated with a candidate.

Do not treat the strongest BLS peak as automatically correct.

## 8. Represent Uncertainty and Detection Results

Extend the existing BLS result structures according to the approved design.

The resulting analysis should be able to represent:

- Original BLS candidate parameters.
- Estimated parameter uncertainties.
- Uncertainty estimation method.
- Relevant calibration information.
- Detection statistics.
- False alarm probability, if implemented.
- Null-model assumptions.
- Warnings and limitations.
- Assessment status.

Keep the original BLS outputs distinguishable from the additional uncertainty and detection-assessment results.

This is important for reproducibility and for allowing later tasks to inspect how the conclusions were obtained.

## 9. Handle Unreliable or Inconclusive Results

Not every BLS candidate will support a meaningful uncertainty estimate or detection assessment.

Handle cases such as:

- Weak transit-like signals.
- Insufficient observations.
- Insufficient transit coverage.
- Very short observation baselines.
- Poor measurement precision.
- Ambiguous candidate peaks.
- Strong aliases.
- Inadequate noise models.
- Unstable uncertainty estimates.
- Failed calibration checks.

The implementation should be able to report when an assessment is inconclusive or unreliable.

Do not manufacture uncertainty values or confidence classifications when the available information does not support them.

## 10. Testing and Scientific Validation

Develop tests using synthetic light curves with known underlying parameters.

Test:

- Recovery of known transit parameters.
- Uncertainty estimation.
- Uncertainty calibration.
- Noise-only controls.
- Injected signals at different strengths.
- Different noise levels.
- Irregular sampling.
- Missing observations.
- Multiple candidate peaks.
- Aliases and harmonics.
- Insufficient transit coverage.
- Invalid or inadequate noise models.

Evaluate whether reported uncertainties are consistent with observed parameter-recovery errors.

Test detection assessment against both injected signals and noise-only controls.

The standard test suite must remain independent of the permanent Kepler-10b FITS file.

### Kepler-10b optional benchmark

The existing dataset remains available:

`C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits`

Known context:

- 476 observations.
- Approximately 9.7-day observation span.
- Published period approximately 0.837491225 days.
- Published epoch approximately 131.574858 BKJD.
- Approximately four non-finite flux values.
- Approximately 37 nonzero quality flags.

The short observation baseline and limited transit coverage must be considered when evaluating uncertainty and detection reliability.

The original FITS file must remain unchanged.

## 11. Documentation and Scientific Reproducibility

Update the relevant project documentation as uncertainty and detection-assessment functionality is designed and implemented.

Document:

- Selected uncertainty methods.
- Statistical assumptions.
- Calibration procedures.
- Detection statistics.
- Null-model assumptions.
- FAP interpretation, if applicable.
- Known limitations.
- Conditions where results are unreliable.
- Testing and validation evidence.

Ensure that analysis results retain sufficient information for reproducibility.

Follow `AGENTS.md` documentation-maintenance requirements.

Do not modify Foundation documents.

## 12. Explicitly Outside This Task

Task 2.4.3 does not include:

- Reimplementing the BLS search engine.
- Changing the approved BLS search algorithm.
- Building the complete analysis interface.
- Integrating periodogram and phase-folded plots into the GUI.
- Full transit fitting.
- Detailed physical parameter estimation.
- Atmospheric characterization.
- Radial-velocity analysis.
- Archive integration.
- Permanent storage redesign.
- Complete operation-history recording.
- Unrelated application refactoring.

Task 2.4.2 owns the BLS search engine.

Task 2.4.4 owns application integration and presentation.

Task 2.4.5 owns final integrated testing, scientific validation, and completion verification.

## Expected Outcome

At the completion of Task 2.4.3, the application should be able to take BLS candidate results and:

1. Estimate uncertainties for supported transit parameters.
2. Evaluate how reliable those uncertainty estimates are.
3. Assess candidate signals against an explicitly defined noise-only model.
4. Calculate and interpret appropriate detection statistics.
5. Identify conditions where an assessment is unreliable or inconclusive.
6. Preserve the assumptions, methods, and results needed for reproducibility.
7. Distinguish candidate detection from statistical significance and planetary confirmation.

The next task is 2.4.4 — Application Integration and Analysis Results. It will bring the BLS search and uncertainty-assessment capabilities into the application's interface and present their results in a coherent workflow.