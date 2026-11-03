# PLAN MODE PROMPT

# PLAN — Task 2.4.2: BLS Transit Search Implementation

**Stage:** 2.4 — BLS Analysis and Uncertainty  
**Task:** 2.4.2 — BLS Transit Search Implementation  
**Mode: PLAN ONLY — Inspect, evaluate, and design the implementation. Do not modify the repository.**

## 1. Objective

Develop a detailed, repository-specific implementation plan for the application's Box Least Squares (BLS) transit-search functionality.

Task 2.4.1 establishes the scientific and technical design for BLS analysis. Task 2.4.2 will implement the actual search functionality according to that approved design.

The objective of this planning task is to determine exactly how the approved BLS design will be implemented using the existing application architecture, data model, dependencies, and testing conventions.

The planned implementation must allow the application to:

1. Accept an imported astronomical light-curve dataset.
2. Prepare the selected measurements according to the approved design.
3. Execute a BLS period search.
4. Calculate a periodogram.
5. identify relevant candidate peaks.
6. Extract candidate transit parameters.
7. Return structured analysis results.
8. Handle invalid inputs and unsuccessful searches.
9. Preserve original scientific measurements.

**Do not implement any of this functionality during PLAN.**

## 2. Mandatory Repository and Prerequisite Inspection

Inspect the actual repository before developing the plan.

Read and evaluate:

- `AGENTS.md`.
- The current Stage 2 roadmap.
- The development log.
- Completed Task 2.4.1 design and documentation.
- Stage 2.2 light-curve data model.
- Stage 2.2 FITS importer and validation.
- Stage 2.2 project integration and persistence.
- Stage 2.3 measurement table.
- Stage 2.3 scientific light-curve visualization.
- Relevant architecture documentation.
- Data-flow documentation.
- Module-responsibility documentation.
- Testing and validation documentation.
- Existing decision records.
- Current test suite and dependency configuration.

Verify the actual completion status of:

- Stage 2.2.
- Stage 2.3.
- Task 2.4.1.

Do not assume a task is complete merely because its roadmap status says so. Inspect the relevant implementation and documentation.

Identify the actual modules, classes, functions, and interfaces that will be involved.

### Prerequisite verification

Determine whether the existing application provides everything required by the approved BLS design.

Check for:

- Access to imported timestamps.
- Access to SAP_FLUX and PDCSAP_FLUX.
- Correct uncertainty-field associations.
- Time units and references.
- Quality flags.
- Missing and non-finite value representation.
- Dataset identity and provenance.
- Existing error and warning conventions.
- Existing scientific analysis patterns.
- Existing plotting interfaces that may later consume BLS results.

If a prerequisite is missing or differs from the approved design, document it clearly.

Do not silently expand Task 2.4.2 to repair unrelated functionality.

## 3. Review and Reconcile the Approved Task 2.4.1 Design

Read the completed Task 2.4.1 documentation and extract the approved requirements relevant to implementation.

Identify:

- Approved BLS algorithm/library.
- Input-data requirements.
- Data-preparation rules.
- Search configuration.
- Period sampling strategy.
- Duration sampling strategy.
- Candidate identification approach.
- Candidate parameter extraction.
- Result structure.
- Error and warning behavior.
- Architecture and module responsibilities.
- Testing requirements.
- Explicitly deferred decisions.

Create a traceability relationship between the approved design and the planned implementation.

For each major requirement, identify:

1. The approved design requirement.
2. The existing repository functionality that supports it.
3. The proposed implementation location.
4. The planned test coverage.

Do not replace approved decisions with new preferences.

If the approved design contains unresolved questions, identify which ones prevent implementation and which can remain deferred.

Do not make decisions that belong to Task 2.4.3.

## 4. BLS Library and Algorithm Implementation

Inspect the existing dependency configuration and determine whether:

`astropy.timeseries.BoxLeastSquares`

is available and appropriate for the approved design.

The project previously established Astropy as an existing dependency. Do not assume a new package is needed.

Evaluate:

- Existing Astropy version.
- BLS API and input requirements.
- Supported period and duration search configuration.
- Available periodogram outputs.
- Available candidate parameters.
- Model-generation capabilities.
- Weighting or uncertainty support.
- Relevant limitations.
- Compatibility with the project's existing NumPy and Astropy versions.

Determine how the BLS implementation should be isolated from the graphical interface.

Identify the proposed module, class, and function responsibilities.

Do not install packages or modify dependency files.

If Astropy's existing BLS implementation does not support a required approved behavior, explain the limitation and propose a minimal solution for review.

## 5. Input Data and Preparation Implementation Plan

Determine exactly how the BLS implementation will receive data from the existing light-curve model.

The initial detection workflow should use:

- `PDCSAP_FLUX` by default.
- `SAP_FLUX` as an independently selectable alternative.

Preserve the correct uncertainty associations:

| Flux measurement | Associated uncertainty |
|---|---|
| `PDCSAP_FLUX` | `PDCSAP_FLUX_ERR` |
| `SAP_FLUX` | `SAP_FLUX_ERR` |

Plan how the implementation will handle:

- Observation timestamps.
- Flux measurements.
- Associated uncertainties.
- Time units and references.
- Missing values.
- NaN and infinite values.
- Invalid timestamps.
- Nonzero quality flags.
- Insufficient valid observations.
- Irregular sampling.
- Duplicate timestamps, if relevant.

Determine which data-preparation operations are required by the approved design.

Clearly distinguish:

1. Original imported measurements.
2. Temporary analysis inputs.
3. Derived analysis representations.

The implementation must not modify the original dataset.

Do not silently remove observations, substitute missing values with zero, or automatically filter nonzero quality flags.

Do not introduce unapproved normalization, detrending, filtering, or other transformations.

Identify how the implementation will report excluded or unusable observations and the reasons for their exclusion.

If the approved design does not specify a necessary behavior, identify it as an unresolved decision.

## 6. Search Configuration Implementation Plan

Determine how the approved BLS search configuration will be represented and supplied to the algorithm.

Address:

### Period search

- Minimum period.
- Maximum period.
- Period or frequency sampling.
- Search resolution.
- Oversampling.
- Observation-baseline constraints.

### Transit duration

- Minimum duration.
- Maximum duration.
- Duration sampling.
- Constraints relating duration to candidate period.

### Configuration behavior

Identify:

- Default settings.
- Automatically derived settings.
- User-configurable settings.
- Required validation.
- Invalid configuration handling.

Determine whether the existing approved design provides sufficient numerical defaults.

Do not invent new defaults during planning.

Where values are unresolved, explain what decision is required and why.

Plan how the complete search configuration will be retained in the analysis result for reproducibility.

## 7. Periodogram Calculation and Candidate Detection

Develop a concrete implementation plan for calculating the BLS periodogram.

Address:

- Input preparation.
- Search configuration.
- BLS execution.
- Periodogram output.
- Candidate peak identification.
- Multiple candidate peaks.
- Candidate ranking or selection, if approved.
- Invalid or unusable periodograms.
- Search failure reporting.

Determine how the implementation will identify candidate peaks without prematurely assigning scientific confidence.

Consider:

- Harmonics.
- Period aliases.
- Competing peaks.
- Data gaps.
- Short observation baselines.
- Stellar variability.
- Instrumental systematics.

These considerations should be documented as limitations and implementation concerns.

Do not introduce final detection thresholds, false alarm probability calculations, or confidence classifications unless already explicitly approved for this task.

Those scientific assessments belong to Task 2.4.3.

## 8. Candidate Parameter Extraction

Plan how the implementation will extract and represent:

- Period.
- Transit epoch.
- Transit duration.
- Transit depth.
- BLS power.

Determine:

- Which values come directly from the BLS library.
- Which values require additional calculations.
- How units will be represented.
- How timestamps will retain their time reference.
- How multiple candidates will be represented.
- How invalid or incomplete candidate results will be handled.

Identify how the result will retain the relationship between a candidate and its original dataset.

Do not implement uncertainty estimates or imply that extracted parameters are scientifically confirmed.

## 9. Structured Analysis Result Design

Determine the concrete result structure required by the approved Task 2.4.1 design.

Inspect existing project conventions for dataclasses, validation, result objects, and error handling.

Plan a result representation that can retain, where applicable:

- Dataset identity.
- Selected flux measurement.
- Associated uncertainty measurement.
- Time metadata.
- Search configuration.
- Data-preparation information.
- Periodogram values.
- Candidate peaks.
- Extracted candidate parameters.
- Warnings.
- Errors or failure information.
- Algorithm and software version information.

The result should be suitable for future consumption by:

- Task 2.4.3 — Transit Parameter Uncertainty and Detection Assessment.
- Task 2.4.4 — Application Integration and Analysis Results.
- Stage 2.5 — Analysis-operation recording.

Determine how the result will remain independent of the graphical interface.

Do not implement permanent persistence or the complete operation-history system.

## 10. Error Handling and Failure States

Plan explicit behavior for:

- Missing datasets.
- Missing required columns.
- Missing selected flux measurements.
- Missing uncertainty fields.
- Insufficient valid observations.
- Invalid timestamps.
- Non-finite values.
- Invalid search configurations.
- Invalid period or duration ranges.
- Insufficient observation baseline.
- BLS library errors.
- Empty or unusable periodograms.
- Candidate extraction failures.

Distinguish between:

- Input validation errors.
- Warnings.
- Search failures.
- Valid searches that produce no useful candidate.

Identify how these outcomes will be represented and communicated to later application-integration work.

Avoid designs that silently return misleading or incomplete results.

## 11. Architecture and File-Level Implementation Plan

Map the proposed implementation onto the actual repository.

Identify:

- New modules likely required.
- Existing modules likely to be modified.
- Existing modules that should remain unchanged.
- Proposed classes and functions.
- Input and output interfaces.
- Error-handling boundaries.
- Dependencies between modules.
- Integration points for later tasks.

Prefer existing architectural conventions.

Keep the scientific BLS implementation independent of the GUI.

Do not introduce a general-purpose analysis framework or unnecessary abstraction.

Do not introduce new dependencies without identifying the need and obtaining approval.

Provide a file-by-file implementation plan explaining what each change would accomplish.

## 12. Testing and Validation Plan

Develop a concrete testing plan for the future implementation.

Use portable synthetic light-curve fixtures and temporary data.

The standard test suite must not depend on the permanent Kepler-10b FITS file or any absolute local path.

### Synthetic signals

Plan tests using known:

- Periods.
- Transit epochs.
- Durations.
- Depths.
- Noise levels.

### Required scenarios

Include:

- Clean periodic transit signals.
- Noisy transit signals.
- Different periods.
- Different durations and depths.
- Missing observations.
- Non-finite measurements.
- Irregular sampling.
- Noise-only controls.
- Insufficient observations.
- Invalid search configurations.
- Multiple candidate peaks.
- Invalid or unusable periodograms.

Define how recovered parameters will be compared with known synthetic inputs.

Identify which tests belong to core algorithm behavior and which belong to input preparation or result validation.

### Scientific validation

Plan optional use of the user's existing Kepler-10b dataset:

`C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits`

Known context:

- Kepler long-cadence observations.
- 476 rows.
- Approximately 9.7-day observation span.
- Published period approximately 0.837491225 days.
- Published epoch approximately 131.574858 BKJD.
- TIME uses BKJD/TDB.
- Approximately four non-finite flux values.
- Approximately 37 nonzero quality flags.

The short observation baseline must be considered when interpreting search results.

The original FITS file must remain unchanged.

Do not make routine automated tests depend on this file.

## 13. Performance and Resource Considerations

Evaluate expected computational cost.

Consider:

- Number of observations.
- Period-grid size.
- Duration-grid size.
- Memory requirements.
- Repeated analysis.
- Avoiding unnecessary data copies.
- Responsiveness of future GUI integration.

Identify reasonable implementation safeguards without prematurely designing a general-purpose optimization system.

Do not introduce unapproved downsampling or reduction of scientific measurements.

## 14. Documentation Plan

Follow `AGENTS.md` and identify documentation that will need updating during the later Build phase.

Review the need for updates to:

- Stage roadmap.
- Development log.
- Architecture documentation.
- Data-flow documentation.
- Module responsibilities.
- Data-model documentation, if necessary.
- Testing and validation documentation.
- Project state and continuity records.
- Decision records, where appropriate.

Identify the specific changes each document will need.

Do not modify documentation during PLAN.

Do not modify Foundation documents.

## 15. Explicit Task Boundaries

The implementation plan must keep Task 2.4.2 within its assigned scope.

### Included in Task 2.4.2

- BLS input preparation.
- BLS search configuration implementation.
- BLS periodogram calculation.
- Candidate peak identification.
- Candidate parameter extraction.
- Structured BLS results.
- Error and warning handling.
- Core algorithm tests.
- Necessary documentation updates.

### Excluded from Task 2.4.2

- Transit parameter uncertainty estimation.
- Empirical uncertainty calibration.
- False alarm probability implementation.
- Detection significance assessment.
- Final candidate confidence assessment.
- Application GUI integration.
- Periodogram and phase-folded plot integration.
- Transit fitting.
- Automatic detrending.
- Automatic normalization.
- Automatic quality filtering.
- Archive integration.
- Permanent storage redesign.
- Complete operation-history recording.
- Unrelated refactoring.

Task 2.4.3 owns uncertainty and detection assessment.

Task 2.4.4 owns application integration and presentation.

Task 2.4.5 owns final testing, scientific validation, and completion verification.

Do not move responsibilities between tasks without explicit approval.

## 16. Required PLAN Report

Return a detailed report with the following sections.

### A. Repository and prerequisite verification
- Actual repository state.
- Verified Stage 2.2 status.
- Verified Stage 2.3 status.
- Verified Task 2.4.1 status.
- Relevant existing modules and interfaces.
- Missing prerequisites.

### B. Approved design reconciliation
- Requirements from Task 2.4.1.
- Existing implementation support.
- Unresolved decisions.
- Any discrepancies.

### C. BLS library evaluation
- Astropy version.
- `BoxLeastSquares` capabilities.
- Input requirements.
- Relevant limitations.
- Dependency assessment.

### D. Input preparation
- Data access.
- Flux and uncertainty selection.
- Timestamp handling.
- Missing and non-finite values.
- Quality flags.
- Temporary analysis inputs.
- Scientific integrity safeguards.

### E. Search configuration
- Period range.
- Period sampling.
- Duration range.
- Duration sampling.
- Defaults and validation.
- Unresolved numerical settings.

### F. Periodogram and candidate detection
- Algorithm workflow.
- Periodogram output.
- Candidate peak identification.
- Multiple candidates.
- Alias and harmonic considerations.
- Failure behavior.

### G. Candidate parameter extraction
- Period.
- Epoch.
- Duration.
- Depth.
- BLS power.
- Units and time references.
- Candidate representation.

### H. Structured result design
- Proposed result fields.
- Data relationships.
- Reproducibility.
- Compatibility with Tasks 2.4.3, 2.4.4, and Stage 2.5.

### I. Error and warning handling
- Validation.
- Search failures.
- Empty results.
- Invalid inputs.
- Warning representation.

### J. Architecture and file-level changes
- Proposed files.
- Existing files to modify.
- New modules.
- Classes and functions.
- Interfaces and dependencies.

### K. Testing and scientific validation
- Synthetic fixtures.
- Known-signal recovery.
- Noise-only controls.
- Missing and irregular data.
- Invalid inputs.
- Kepler-10b optional benchmark.
- Scientific integrity tests.

### L. Performance considerations
- Computational complexity.
- Memory.
- Responsiveness.
- Potential safeguards.

### M. Documentation updates
- Exact documents.
- Proposed updates.
- Documents that should remain unchanged.

### N. Risks and unresolved decisions
- Scientific risks.
- Technical risks.
- Missing prerequisites.
- Decisions requiring user approval.

### O. Proposed Build breakdown
Provide a logical, ordered implementation sequence.

For each implementation step, identify:
- Objective.
- Files involved.
- Dependencies.
- Tests.
- Expected outcome.

Keep the breakdown within Task 2.4.2.

### P. Readiness assessment
State whether Task 2.4.2 is ready for Build.

Identify any blockers or decisions requiring user approval.

## 17. PLAN Restrictions

During this task:

- Do not create or modify source files.
- Do not implement BLS.
- Do not modify tests.
- Do not modify documentation.
- Do not install or update dependencies.
- Do not modify project data.
- Do not modify the original Kepler FITS file.
- Do not modify Foundation documents.
- Do not commit or push.
- Do not reset, clean, or alter Git history.
- Do not discard or overwrite user changes.

You may inspect existing code, documentation, configuration, and tests to develop the plan.

Do not claim functionality exists without verifying it in the repository.

Clearly distinguish verified facts, approved decisions, recommendations, assumptions, and unresolved questions.

**Stop after presenting the PLAN report. Wait for explicit user approval before making any changes.**


# BUILD MODE PROMPT

# BUILD — Task 2.4.2: BLS Transit Search Implementation

**Stage:** 2.4 — BLS Analysis and Uncertainty  
**Task:** 2.4.2 — BLS Transit Search Implementation  
**Mode: BUILD — Implement the approved BLS transit-search functionality only.**

## 1. Objective

Implement the application's initial Box Least Squares (BLS) transit-search capability according to:

1. The approved Task 2.4.1 scientific and technical design.
2. The reviewed and approved Task 2.4.2 PLAN report.
3. The actual existing repository architecture and interfaces.
4. The project's Foundation requirements and `AGENTS.md` governance.

The implementation should allow the application to accept an imported photometric light-curve dataset, prepare its measurements according to the approved design, execute a BLS period search, identify candidate transit-like signals, extract candidate parameters, and return structured analysis results.

**This task implements the BLS search engine. It does not implement uncertainty estimation, detection significance assessment, or GUI integration.**

## 2. Mandatory Pre-Build Verification

Before modifying anything:

1. Read `AGENTS.md`.
2. Read the approved Task 2.4.1 design.
3. Read the approved Task 2.4.2 PLAN report.
4. Inspect the current repository state.
5. Verify that the prerequisites identified in the PLAN are present.
6. Review the relevant Stage 2.2 and Stage 2.3 implementations.
7. Review the current roadmap and development log.
8. Identify the exact files and documentation affected by the approved implementation plan.
9. Inspect the Git working tree and preserve existing user changes.

Reconcile the approved PLAN with the actual repository.

If the repository differs materially from the approved PLAN, stop and report the discrepancy.

If an unresolved decision requires user approval, do not invent a solution. Stop and request clarification.

Do not silently change the approved scientific design, architecture, or implementation scope.

## 3. Implement BLS Input Preparation

Implement the approved method of obtaining and preparing light-curve measurements for BLS.

The implementation must use the existing Stage 2.2 data model and interfaces wherever possible.

Support the approved initial measurement choices:

- `PDCSAP_FLUX` as the default detection measurement.
- `SAP_FLUX` as an independently selectable alternative.

Maintain the correct uncertainty associations:

| Flux measurement | Associated uncertainty |
|---|---|
| `PDCSAP_FLUX` | `PDCSAP_FLUX_ERR` |
| `SAP_FLUX` | `SAP_FLUX_ERR` |

Handle the input information required by the approved design:

- Observation timestamps.
- Flux measurements.
- Associated uncertainties, when available.
- Time units.
- Time reference and time scale.
- Quality flags.
- Missing and non-finite values.
- Dataset identity and provenance.

### Scientific data preservation

The implementation must:

- Leave original imported measurements unchanged.
- Keep temporary analysis inputs separate from original data.
- Preserve SAP and PDCSAP as distinct measurements.
- Never silently substitute missing values with zero.
- Never automatically remove nonzero quality flags.
- Never silently discard observations without documenting the reason.
- Preserve the relationship between analysis inputs and their original observations.

Any excluded observations must be accounted for according to the approved design.

Do not introduce unapproved normalization, detrending, filtering, or other scientific transformations.

Do not modify the Stage 2.2 importer or data model unless the approved PLAN explicitly authorizes a necessary, narrowly scoped change.

If an unexpected prerequisite defect is discovered, stop and report it rather than expanding the task.

## 4. Implement BLS Search Configuration

Implement the search configuration established in the approved design.

This includes the approved settings for:

- Minimum period.
- Maximum period.
- Period sampling or frequency grid.
- Search resolution.
- Transit duration range.
- Duration sampling.
- Other required BLS parameters.

Implement the approved distinction between:

- Application defaults.
- Automatically derived settings.
- User-configurable settings.
- Required settings.

Validate configurations before executing the search.

Handle invalid or incompatible configurations explicitly.

Preserve the complete configuration used for each analysis so that the search can be reproduced.

Do not introduce arbitrary numerical defaults or change approved values without authorization.

Do not add GUI configuration controls; application integration belongs to Task 2.4.4.

## 5. Implement the BLS Search Engine

Implement the actual BLS search using the library and architecture selected in the approved design.

Evaluate and use the existing:

`astropy.timeseries.BoxLeastSquares`

if that is the approved implementation.

Use the existing dependency configuration. Do not install unnecessary packages or replace the approved library without authorization.

The search implementation should:

1. Receive validated analysis inputs.
2. Receive the approved search configuration.
3. Execute the BLS calculation.
4. Generate the periodogram.
5. Identify candidate peaks according to the approved design.
6. Extract candidate parameters.
7. Return structured results.

Keep the scientific algorithm independent of the graphical interface.

Use the existing project architecture and coding conventions.

Do not build a general-purpose analysis framework.

## 6. Implement Periodogram and Candidate Detection

Implement the approved periodogram calculation and candidate-identification approach.

The implementation should support the approved representation of:

- Period or frequency values.
- BLS power values.
- Candidate peak locations.
- Candidate ranking or selection, where approved.
- Multiple candidate peaks, where required.

Handle empty, invalid, or unusable periodograms explicitly.

Candidate identification must not silently imply that the strongest BLS peak represents a confirmed planetary detection.

Preserve information needed for later evaluation of:

- Period aliases.
- Harmonics.
- Competing peaks.
- Data gaps.
- Short observation baselines.
- Stellar variability.
- Instrumental systematics.

Do not implement false alarm probability, final detection thresholds, or scientific confidence classifications unless the approved design explicitly assigns a narrowly scoped requirement to this task.

Detection assessment belongs to Task 2.4.3.

## 7. Implement Candidate Parameter Extraction

Extract the candidate parameters established by the approved design:

- Period.
- Transit epoch.
- Transit duration.
- Transit depth.
- BLS power.

Use the appropriate BLS outputs and any additional calculations explicitly approved in the design.

Preserve:

- Appropriate units.
- Timestamp reference and scale.
- Relationship to the source dataset.
- Candidate identity.
- Relevant warnings or limitations.

Support multiple candidate results if required by the approved design.

Handle incomplete or invalid candidate results explicitly.

Do not implement uncertainty estimates or present extracted values as confirmed planetary parameters.

## 8. Implement Structured Analysis Results

Implement the approved result representation.

Follow existing repository conventions for data classes, validation, and result objects.

The result should retain the information established in Task 2.4.1 and Task 2.4.2 planning, including where applicable:

- Dataset identity.
- Selected flux measurement.
- Associated uncertainty measurement.
- Time metadata.
- Search configuration.
- Data-preparation information.
- Periodogram values.
- Candidate peaks.
- Extracted candidate parameters.
- Warnings and limitations.
- Error or failure information.
- Algorithm and software version information.

Ensure the result is independent of the GUI.

Design it so that subsequent tasks can consume it without requiring the BLS algorithm to be rewritten:

- Task 2.4.3: uncertainty and detection assessment.
- Task 2.4.4: application integration and analysis results.
- Stage 2.5: analysis-operation recording.

Do not implement permanent persistence or the complete operation-history system.

Do not introduce unnecessary result fields or abstractions beyond the approved design.

## 9. Implement Error Handling and Validation

Implement the approved error and warning behavior.

Account for:

- Missing datasets.
- Missing required columns.
- Missing selected flux measurements.
- Missing uncertainty fields.
- Insufficient valid observations.
- Invalid timestamps.
- Non-finite measurements.
- Invalid search configurations.
- Incompatible period and duration settings.
- Insufficient observation baseline.
- BLS library errors.
- Empty or unusable periodograms.
- Candidate extraction failures.

Distinguish between:

1. Input validation errors.
2. Warnings that permit analysis to continue.
3. Search execution failures.
4. Valid searches that produce no useful candidate.

Avoid silent failures and misleading results.

Follow existing application error-handling conventions.

Do not add GUI-specific error dialogs; that belongs to Task 2.4.4.

## 10. Implement Core BLS Tests

Implement tests according to the approved PLAN.

Use portable synthetic light-curve fixtures and temporary data.

The standard test suite must not depend on the permanent Kepler-10b FITS file or any absolute local path.

### Known-signal tests

Create or use controlled signals with known:

- Periods.
- Transit epochs.
- Transit durations.
- Transit depths.
- Noise levels.

Verify that the implementation can recover the expected signal within the approved tolerances.

### Required scenarios

Include appropriate tests for:

- Clean periodic transit signals.
- Noisy transit signals.
- Different transit periods.
- Different transit durations and depths.
- Missing observations.
- Non-finite measurements.
- Irregular sampling.
- Noise-only controls.
- Insufficient observations.
- Invalid search configurations.
- Multiple candidate peaks.
- Empty or unusable periodograms.
- Error and warning behavior.

### Input preparation tests

Verify:

- Correct selection of PDCSAP_FLUX.
- Independent selection of SAP_FLUX.
- Correct uncertainty-field associations.
- Correct timestamp handling.
- Correct handling of missing and non-finite values.
- Preservation of quality information.
- No mutation of original measurements.

### Result tests

Verify:

- Candidate parameters.
- Periodogram representation.
- Search configuration retention.
- Dataset association.
- Units and time metadata.
- Warnings and errors.
- Result usability by later analysis components.

### Test quality

Tests must verify meaningful behavior rather than merely checking that functions execute.

Do not weaken, delete, or rewrite existing tests simply to obtain a passing suite.

Do not use arbitrary tolerances without scientific or technical justification.

If an expected recovery tolerance is not established in the approved design, identify the issue and request approval rather than inventing a threshold.

## 11. Kepler-10b Optional Verification

The available research dataset is:

`C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits`

Known context:

- Kepler long-cadence observations.
- 476 rows.
- Approximately 9.7-day observation span.
- TIME in BKJD/TDB.
- Published period approximately 0.837491225 days.
- Published epoch approximately 131.574858 BKJD.
- Approximately four non-finite flux values.
- Approximately 37 nonzero quality flags.

If the approved PLAN includes optional real-data verification, use the dataset without modifying the original file.

Account for the limited observation baseline when interpreting results.

Do not treat failure to recover a published signal from this short dataset as automatic proof of an implementation defect. Investigate the search configuration, data preparation, sampling, and limitations.

Do not make standard automated tests depend on this file.

## 12. Performance and Resource Considerations

Implement reasonable safeguards consistent with the approved design.

Consider:

- Period-grid size.
- Duration-grid size.
- Number of observations.
- Memory use.
- Repeated data preparation.
- Avoiding unnecessary copies.
- Computational cost.

Do not introduce unapproved downsampling or reduce scientific measurements for convenience.

Do not overengineer performance infrastructure before evidence requires it.

## 13. Documentation Maintenance

Follow the documentation-maintenance requirements in `AGENTS.md`.

Update the appropriate existing documents as implementation changes functionality, interfaces, architecture, testing, and project progress.

Review and update where appropriate:

- Stage roadmap.
- Development log.
- Architecture documentation.
- Data-flow documentation.
- Module responsibilities.
- Data-model documentation, if affected.
- Testing and validation documentation.
- Project state and continuity records.
- Decision records, if a genuine new decision is required.

Documentation must accurately distinguish:

- Existing functionality.
- Newly implemented functionality.
- Tested behavior.
- Known limitations.
- Deferred functionality.
- Unresolved decisions.

Update Task 2.4.2 status only according to its actual completion state.

Do not mark Task 2.4.3, 2.4.4, or 2.4.5 complete.

Do not modify Foundation documents.

Do not create duplicate documentation where an existing document is appropriate.

## 14. Explicit Scope Exclusions

Do not implement:

- Transit parameter uncertainty estimation.
- Empirical uncertainty calibration.
- False alarm probability.
- Detection significance assessment.
- Final candidate confidence classification.
- GUI integration.
- Periodogram visualization integration.
- Phase-folded plot integration.
- Transit fitting.
- Atmospheric characterization.
- Automatic detrending.
- Automatic normalization.
- Automatic quality filtering.
- Archive integration.
- Permanent storage redesign.
- Complete operation-history recording.
- Unrelated refactoring.

These responsibilities remain with their designated later tasks.

If an implementation requirement crosses these boundaries, stop and report it.

## 15. Final Verification

After implementation:

1. Run the targeted BLS tests.
2. Run relevant regression tests.
3. Run the full test suite.
4. Record actual commands and results.
5. Investigate failures rather than suppressing them.
6. Review the working-tree diff.
7. Verify that original scientific measurements remain unchanged.
8. Verify SAP/PDCSAP separation and uncertainty associations.
9. Verify that result structures retain the required metadata.
10. Compare the implementation against the approved PLAN.
11. Reconcile documentation against actual code and test results.
12. Identify remaining limitations and incomplete requirements.

Do not claim tests passed unless they were actually executed successfully.

Do not claim scientific validation beyond what the tests and available evidence support.

## 16. Required Final Report

Provide a report with the following sections.

### A. Implementation summary
- Functionality implemented.
- Overall completion status.
- Relationship to the approved design.

### B. Input preparation
- Data access.
- Measurement selection.
- Uncertainty associations.
- Timestamp handling.
- Missing and non-finite values.
- Quality flags.
- Scientific integrity safeguards.

### C. BLS implementation
- Library used.
- Search configuration.
- Periodogram calculation.
- Candidate identification.
- Parameter extraction.

### D. Structured results
- Result fields.
- Dataset association.
- Units and time references.
- Reproducibility information.
- Compatibility with later tasks.

### E. Error and warning handling
- Validation behavior.
- Failure cases.
- Empty-result behavior.
- Known limitations.

### F. Files changed
For every changed file, explain:
- What changed.
- Why it changed.
- Which approved requirement it addresses.

Separate source-code, test, and documentation changes.

### G. Test results
Include:
- Exact commands executed.
- Targeted test results.
- Regression test results.
- Full suite results.
- Any failures or skipped tests.
- Explanation of unresolved test limitations.

### H. Scientific integrity verification
Explicitly report whether:
- Original measurements remain unchanged.
- SAP and PDCSAP remain separate.
- Uncertainty associations are correct.
- Missing values remain distinguishable from zero.
- Quality flags remain accessible.
- Time metadata is preserved.
- No unapproved transformations were introduced.

### I. Documentation reconciliation
Identify:
- Documents updated.
- Documents inspected but intentionally unchanged.
- Remaining documentation gaps.

### J. Scope verification
Explicitly confirm whether:
- BLS search functionality was implemented.
- Uncertainty calculations were left to Task 2.4.3.
- Detection assessment was left to Task 2.4.3.
- GUI integration was left to Task 2.4.4.
- Final scientific validation was left to Task 2.4.5.
- No unapproved dependencies were added.
- No Foundation documents were modified.

### K. Remaining issues and handoff
List:
- Incomplete requirements.
- Known limitations.
- Unresolved decisions.
- Prerequisites for Task 2.4.3.
- Information Task 2.4.4 will need.
- Recommended next steps.

Recommend whether Task 2.4.2 is complete.

Do not begin Task 2.4.3.

## 17. Git and User-Work Protections

- Do not commit.
- Do not push.
- Do not reset, clean, or alter Git history.
- Do not discard or overwrite user changes.
- Do not modify the original research FITS file.
- Do not modify Foundation documents.
- Do not perform destructive cleanup.

Leave all changes in the working tree for user review.

**Stop after presenting the final report. Wait for separate user approval before beginning Task 2.4.3.**