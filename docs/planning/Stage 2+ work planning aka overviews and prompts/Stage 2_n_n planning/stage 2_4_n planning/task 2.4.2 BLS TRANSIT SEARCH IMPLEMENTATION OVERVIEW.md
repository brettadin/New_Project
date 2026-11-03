# Task 2.4.2 — BLS Transit Search Implementation

Stage: 2.4 — BLS Analysis and Uncertainty

Objective: Implement the actual Box Least Squares (BLS) transit-search functionality using the scientific and architectural design established and approved in Task 2.4.1.

Task 2.4.1 establishes how the BLS analysis should work. Task 2.4.2 turns that design into working scientific functionality.

The goal is to allow the application to analyze an imported photometric light curve, search for periodic transit-like signals, and produce structured candidate results that can eventually be evaluated and displayed by later tasks.

## 1. Review the Approved BLS Design

Before implementation, review:

- The completed Task 2.4.1 design.
- The existing light-curve data model and importer from Stage 2.2.
- The measurement table and visualization from Stage 2.3.
- Existing scientific and application architecture.
- Relevant testing and documentation.

Implementation must follow the approved design rather than introduce a separate approach.

Verify that the necessary input fields and interfaces exist. Report any missing prerequisites before proceeding.

## 2. Prepare Light-Curve Data for BLS

Implement the approved process for supplying measurements to the BLS algorithm.

This includes handling:

- Observation timestamps.
- Selected flux measurement.
- Associated measurement uncertainties.
- Time units and references.
- Missing and non-finite values.
- Quality flags.
- Invalid or insufficient observations.

The initial detection workflow should use `PDCSAP_FLUX` by default, while allowing `SAP_FLUX` to be analyzed independently.

Uncertainty fields must remain correctly associated:

| Flux measurement | Associated uncertainty |
| ---------------- | ---------------------- |
| `PDCSAP_FLUX`    | `PDCSAP_FLUX_ERR`      |
| `SAP_FLUX`       | `SAP_FLUX_ERR`         |

Any data preparation must follow the approved Task 2.4.1 design.

Scientific integrity requirements:

- Never modify the original imported measurements.
- Do not silently discard observations.
- Do not automatically remove nonzero quality flags.
- Do not silently substitute missing values with zero.
- Do not introduce unapproved normalization, detrending, or filtering.
- Keep temporary analysis inputs distinguishable from original measurements.

## 3. Implement the BLS Search

Implement the actual Box Least Squares algorithm using the approved library and architecture.

The existing project dependency, `astropy.timeseries.BoxLeastSquares`, should be evaluated and used if confirmed by the approved design.

The implementation should:

1. Receive prepared light-curve measurements.
2. Apply the approved search configuration.
3. Evaluate candidate transit periods and durations.
4. Calculate the BLS periodogram.
5. Identify relevant candidate peaks.
6. Extract the associated transit parameters.
7. Return structured analysis results.

The search should follow the approved configuration for:

- Minimum and maximum period.
- Period sampling and resolution.
- Transit duration range.
- Duration sampling.
- Relevant algorithm settings.

The implementation should not introduce arbitrary search defaults that were not established by the approved design.

## 4. Extract Transit Candidate Parameters

For identified candidate signals, extract the parameters supported by the BLS implementation.

These should include:

| Parameter | Description                                                       |
| --------- | ----------------------------------------------------------------- |
| Period    | Estimated repeating interval of the transit-like signal           |
| Epoch     | Estimated reference time of transit                               |
| Duration  | Estimated duration of the transit                                 |
| Depth     | Estimated change in flux associated with the transit              |
| BLS power | Strength of the candidate signal according to the BLS periodogram |

The implementation should support multiple candidate peaks where established by the approved design.

It should also preserve enough information for subsequent analysis and visualization.

Candidate extraction must not imply that a signal has been confirmed as a planet.

## 5. Produce Structured BLS Results

The implementation should return a structured result rather than only printing values or displaying a plot.

The result should contain the information established in Task 2.4.1, including:

- Search configuration.
- Selected measurement.
- Relevant input metadata.
- Periodogram information.
- Candidate parameters.
- Candidate peak information.
- Warnings and limitations.
- Information needed to reproduce the analysis.

The result structure should be suitable for later use by:

- Task 2.4.3: uncertainty and detection assessment.
- Task 2.4.4: application integration and analysis results.
- Stage 2.5: analysis-operation recording.

Permanent persistence and complete operation-history functionality are not part of this task.

## 6. Handle Invalid Inputs and Search Failures

The implementation must handle unsuccessful searches and invalid inputs explicitly.

Examples include:

- Missing required measurements.
- Insufficient valid observations.
- Invalid timestamps.
- Non-finite flux values.
- Invalid search ranges.
- Incompatible period and duration settings.
- Insufficient observation baseline.
- Search results that cannot produce meaningful candidates.

Errors and warnings should be distinguishable.

The application should not silently return misleading results when the search cannot be performed reliably.

## 7. Establish the Initial Testing Framework

Implement tests for the BLS functionality using controlled, portable datasets.

Synthetic light curves should include known transit parameters so the algorithm's behavior can be evaluated.

Test scenarios should include:

- A clean periodic transit signal.
- A transit signal with added noise.
- Different transit periods.
- Different transit depths and durations.
- Missing observations.
- Irregular sampling.
- Non-finite measurements.
- Noise-only datasets.
- Insufficient observations.
- Invalid search configurations.

Tests should verify that recovered candidate parameters are within the tolerances established by the approved design.

The noise-only controls should use appropriate sampling and uncertainty assumptions. They should not be treated as proof that a real signal is absent.

The standard test suite must use fixtures and temporary data. It must not depend on the permanent Kepler-10b FITS file or an absolute local path.

## 8. Maintain Scientific Integrity

Throughout implementation:

- Preserve original measurements.
- Keep SAP and PDCSAP separate.
- Associate the correct uncertainty fields.
- Preserve time references and units.
- Preserve quality information.
- Make data preparation reproducible.
- Distinguish candidate detection from planetary confirmation.
- Keep warnings and limitations accessible.
- Avoid unapproved scientific transformations.

The implementation must not silently imply that BLS power alone establishes a planetary detection.

## 9. Documentation and Project Tracking

Update the appropriate project documentation as functionality and interfaces are implemented.

This may include:

- Stage roadmap.
- Development log.
- Architecture documentation.
- Data-flow documentation.
- Module responsibilities.
- Testing and validation documentation.
- Project state and continuity records.
- Decision records, if new decisions are genuinely required.

Follow the documentation-maintenance requirements in `AGENTS.md`.

Document what was actually implemented and tested. Do not describe planned uncertainty calculations or application integration as completed.

Do not modify Foundation documents.

## 10. Explicitly Outside This Task

Task 2.4.2 does not include:

- Transit parameter uncertainty estimation.
- Empirical uncertainty calibration.
- False alarm probability implementation.
- Detection significance assessment.
- Final candidate confidence assessment.
- BLS interface integration.
- Periodogram or phase-folded visualization integration.
- Transit fitting.
- Detrending or automatic normalization.
- Automatic quality filtering.
- Archive integration.
- Permanent storage redesign.
- Complete operation-history recording.
- Unrelated application refactoring.

These responsibilities remain with their designated later tasks.

## Expected Outcome

At the completion of Task 2.4.2, the application should have a working, testable BLS analysis capability that can:

1. Accept an imported light-curve dataset.
2. Prepare the selected measurements according to the approved design.
3. Search for periodic transit-like signals.
4. Calculate a BLS periodogram.
5. Extract candidate transit parameters.
6. Return structured and reproducible analysis results.
7. Handle invalid inputs and unsuccessful searches.
8. Preserve the original scientific measurements.

The implementation should be independent of the graphical interface, allowing later integration.

The next task is 2.4.3 — Transit Parameter Uncertainty and Detection Assessment. That task will address how reliable the extracted parameters are, how their uncertainties should be estimated, and how candidate detections should be evaluated.

Task boundary: 2.4.2 builds the BLS search engine. It does not establish the final scientific confidence or uncertainty of a candidate, and it does not yet integrate the results into the application interface.