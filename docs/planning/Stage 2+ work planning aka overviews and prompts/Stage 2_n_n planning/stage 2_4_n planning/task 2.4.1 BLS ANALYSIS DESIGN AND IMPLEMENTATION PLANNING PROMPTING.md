# PLAN MODE PROMPT

# PLAN — Task 2.4.1: BLS Analysis Design and Implementation Planning

**Stage:** 2.4 — BLS Analysis and Uncertainty  
**Task:** 2.4.1 — BLS Analysis Design and Implementation Planning  
**Mode: PLAN ONLY — repository inspection, scientific evaluation, and design. No implementation.**

## 1. Objective

Establish the scientific, technical, and architectural design for implementing Box Least Squares (BLS) transit analysis in the application.

This task must determine how the application will prepare photometric observations, configure and execute a BLS search, identify candidate transit signals, extract candidate parameters, present results, and prepare for subsequent uncertainty estimation.

The goal is to produce an implementation plan grounded in the actual repository and existing scientific data model.

**Do not implement BLS or modify any project files during this task.**

## 2. Mandatory Repository and Prerequisite Inspection

Inspect the actual repository before making recommendations.

Review:

- `AGENTS.md` and applicable development instructions.
- The current Stage 2 roadmap and development log.
- Stage 2.2 implementation and documentation.
- Stage 2.3.1 approved design.
- Stage 2.3.2 measurement table.
- Stage 2.3.3 scientific light-curve visualization.
- Stage 2.3.4 table/plot integration and completion verification.
- Relevant architecture, data-model, data-flow, module-responsibility, testing, validation, and decision documents.

Verify actual implementation against code and tests. Do not assume that a task is complete merely because documentation marks it complete.

Determine whether the application currently provides:

- Imported light-curve datasets associated with projects.
- Observation timestamps and their time metadata.
- SAP_FLUX and PDCSAP_FLUX as separate measurements.
- SAP_FLUX_ERR and PDCSAP_FLUX_ERR.
- Quality flags.
- Missing and non-finite observation handling.
- Dataset and observation identity.
- Measurement selection.
- Existing scientific plotting interfaces.
- Appropriate analysis-module boundaries.

If prerequisites are incomplete or inconsistent, explain their impact and identify what must be resolved before BLS implementation.

Do not silently design around functionality that does not exist.

## 3. BLS Input Data Design

Determine exactly how the existing data model can supply BLS inputs.

### A. Required inputs

Evaluate the representation and access of:

- Observation times.
- Selected flux measurements.
- Measurement uncertainties, when available.
- Time units.
- Time reference and time scale.
- Relevant quality information.
- Dataset identity and provenance.

The initial detection workflow should use PDCSAP_FLUX as the default measurement, consistent with the existing project direction. SAP_FLUX must remain available for separate analysis.

### B. Data preparation

Investigate and recommend how the application should prepare data for BLS.

Address:

- Missing and non-finite timestamps.
- Missing and non-finite flux values.
- Missing and non-finite uncertainties.
- Nonzero quality flags.
- Irregular observation spacing.
- Insufficient observations.
- Duplicate or invalid timestamps, if applicable.
- Flux baseline and normalization requirements.
- Whether measurement uncertainties should be used as weights.

Distinguish imported measurements from temporary analysis inputs and derived representations.

Any preparation or transformation must be explicit, documented, and reproducible. Original imported measurements must not be modified.

Do not assume that detrending, normalization, or quality filtering is automatically appropriate.

For any proposed exclusion or transformation, explain its scientific justification, consequences, and required configuration or documentation.

### C. Time handling

Inspect the actual time metadata and determine how BLS should receive timestamps.

Address:

- BKJD/TDB compatibility.
- Time units and reference systems.
- Time-scale interpretation.
- Numerical precision.
- Epoch reporting.
- Future compatibility with other time representations.

Do not invent missing metadata or silently convert time systems.

## 4. BLS Algorithm and Library Evaluation

Evaluate the existing installed scientific libraries, particularly:

`astropy.timeseries.BoxLeastSquares`

Determine:

- Whether it supports the required initial workflow.
- What inputs it requires.
- How period and duration searches are configured.
- How measurement uncertainties are supplied.
- What statistics and candidate parameters it returns.
- What limitations apply to its outputs.
- Whether its existing capabilities are sufficient for the initial implementation.

Do not add dependencies during planning.

Do not recommend a new library without explaining why the existing stack is insufficient.

## 5. Search Configuration Design

Establish a scientifically reasonable approach for configuring the search.

### A. Period range

Determine how the application should establish:

- Minimum period.
- Maximum period.
- Period sampling or frequency sampling.
- Search resolution.
- Oversampling requirements.
- Constraints imposed by observation baseline and cadence.

Avoid arbitrarily narrow ranges that could exclude real signals.

### B. Transit duration

Determine:

- Minimum duration.
- Maximum duration.
- Duration sampling.
- Relationship between duration and candidate period.
- Appropriate constraints for the available observations.

### C. Configuration ownership

Determine which settings should be:

- Automatically derived from the dataset.
- Set to sensible defaults.
- User-configurable.
- Required inputs.
- Recorded for reproducibility.

Explain the tradeoffs between usability, computational cost, and scientific reliability.

## 6. Candidate Detection and Parameter Extraction

Design the process for identifying and representing candidate transit signals.

Address:

1. BLS periodogram calculation.
2. Candidate peak identification.
3. Strongest candidate selection.
4. Candidate period.
5. Transit epoch.
6. Transit duration.
7. Transit depth.
8. BLS power or equivalent detection statistic.
9. Multiple candidate peaks.
10. Potential harmonics and aliases.

Determine whether the initial design should retain multiple candidate peaks rather than only the strongest one.

Explain how the application should communicate competing candidates and avoid presenting the highest peak as unquestionably correct.

Clearly distinguish a transit-like signal from a confirmed planetary detection.

## 7. Analysis Results and Visualization Design

Establish the minimum results needed for the initial BLS workflow.

### A. Periodogram

Determine how the periodogram should present:

- Period or frequency.
- BLS power.
- Candidate peaks.
- Selected candidate.
- Search configuration context.

### B. Phase-folded light curve

Determine how the application should display:

- Phase-folded observations.
- Selected flux measurement.
- Candidate transit model.
- Measurement uncertainties, when available.
- Relevant labels and units.

### C. Candidate parameter presentation

Determine how to present:

- Period.
- Epoch.
- Duration.
- Depth.
- BLS power.
- Units.
- Warnings and limitations.

Inspect the existing plotting architecture and recommend the smallest appropriate integration approach.

Do not implement the visualizations during this task.

## 8. Analysis Result Structure and Reproducibility

Design the information that must eventually accompany a BLS analysis result.

Consider:

- Project identity.
- Dataset identity.
- Selected flux measurement.
- Associated uncertainty measurement.
- Search configuration.
- Data-preparation steps.
- Algorithm and software version information, where available.
- Candidate parameters.
- Periodogram information or the ability to regenerate it.
- Warnings and limitations.
- Relevant input metadata.

The result design should support future Stage 2.5 operation recording.

However, do not implement the operation-history system or redesign permanent storage.

Review the existing deferred storage decision and respect its limitations.

## 9. Scientific Limitations and Benchmark Considerations

Evaluate how the following factors affect the proposed BLS implementation:

- Short observation baselines.
- Gaps in observations.
- Irregular sampling.
- Stellar variability.
- Instrumental systematics.
- Measurement noise.
- Transit duration assumptions.
- Multiple periodogram peaks.
- Period aliases and harmonics.
- Insufficient observed transits.
- Missing or unreliable measurement uncertainties.

Consider the available Kepler-10b dataset as a practical initial benchmark.

Known context:

- Published orbital period: approximately 0.837491225 days.
- Available local dataset: Kepler Q0 long-cadence observations.
- Observation span: approximately 9.7 days.
- The dataset contains missing/non-finite measurements and nonzero quality flags.

Assess what this dataset can reasonably validate and what limitations its short observation baseline imposes.

Do not assume successful recovery of one benchmark establishes general BLS reliability.

## 10. Architecture and Module Responsibilities

Inspect the existing application architecture.

Recommend:

- Where BLS algorithm functionality should reside.
- How input data should be supplied.
- How analysis configuration should be represented.
- How candidate results should be represented.
- How errors and warnings should be communicated.
- How plotting interfaces should consume results.
- How future uncertainty calculations can use the BLS outputs.
- How the analysis remains independent of the graphical interface.

Prefer existing architectural patterns.

Identify the actual modules and files likely to require changes in subsequent implementation tasks.

Do not create abstractions or introduce dependencies without justification.

## 11. Testing and Validation Strategy

Design the testing strategy for the implementation.

### A. Synthetic datasets

Plan controlled datasets with known:

- Transit periods.
- Transit epochs.
- Transit durations.
- Transit depths.
- Noise levels.

Include:

- Clean synthetic transit signals.
- Noisy transit signals.
- Missing observations.
- Irregular sampling.
- Noise-only controls.
- Cases with insufficient observations.

Explain how recovered values will be compared with known values.

### B. Astronomical benchmarks

Determine how published detections and non-detections can be used for validation.

Evaluate the suitability and limitations of the available Kepler-10b dataset.

### C. Scientific integrity

Plan tests that verify:

- Original imported measurements remain unchanged.
- SAP_FLUX and PDCSAP_FLUX remain separate.
- Correct uncertainties are associated with each measurement.
- Missing values are not replaced with zero.
- Quality flags are not silently filtered.
- Time metadata is interpreted correctly.
- Analysis results are reproducible from their inputs and configuration.

### D. Test portability

Routine tests must use controlled fixtures and temporary datasets.

The standard test suite must not depend on the user's permanent Kepler FITS file or absolute local paths.

## 12. Relationship to Subsequent Stage 2.4 Tasks

The current proposed Stage 2.4 breakdown is:

- 2.4.1 — BLS Analysis Design and Implementation Planning.
- 2.4.2 — BLS Transit Search Implementation.
- 2.4.3 — Transit Parameter Uncertainty and Detection Assessment.
- 2.4.4 — Application Integration and Analysis Results.
- 2.4.5 — Testing, Scientific Validation, and Completion Verification.

Review whether this breakdown is practical and whether any responsibilities overlap.

Specifically establish:

- What must be implemented in 2.4.2.
- What uncertainty and detection-assessment work belongs in 2.4.3.
- What application integration belongs in 2.4.4.
- What final verification belongs in 2.4.5.

Do not change the roadmap or formally adopt a revised breakdown during planning without user approval.

## 13. Documentation Plan

Follow the repository's `AGENTS.md` requirements.

Identify the existing documents that will need updates during subsequent implementation.

Consider:

- Stage roadmap.
- Development log.
- Architecture documentation.
- Data-flow documentation.
- Module responsibilities.
- Data-model documentation, if necessary.
- Testing and validation documentation.
- Project state and continuity records.
- Decision records, where a genuine new decision is required.

Do not modify documentation during this planning task.

Do not modify Foundation documents.

## 14. Required PLAN Report

Provide a structured report with these sections:

**A. Repository and prerequisite status**
- Actual implementation state.
- Relevant modules and documents inspected.
- Verified facts versus documentation claims.
- Missing prerequisites.

**B. Existing data-model capabilities**
- Available BLS inputs.
- Measurement and uncertainty representation.
- Time metadata.
- Missing-value and quality handling.

**C. Data-preparation design**
- Proposed input preparation.
- Exclusions and transformations.
- Scientific justification.
- Original-data preservation.

**D. BLS library evaluation**
- Existing Astropy capabilities.
- Suitability.
- Limitations.
- Any unresolved technical questions.

**E. Search configuration**
- Period range.
- Duration range.
- Sampling and resolution.
- Defaults and user-configurable parameters.

**F. Candidate detection and extraction**
- Periodogram strategy.
- Candidate identification.
- Parameter extraction.
- Multiple peaks, aliases, and harmonics.

**G. Results and visualization**
- Required result outputs.
- Periodogram design.
- Phase-folded plot design.
- Candidate parameter presentation.

**H. Reproducibility and result structure**
- Required inputs and metadata.
- Search configuration.
- Result representation.
- Future Stage 2.5 compatibility.

**I. Scientific limitations**
- Data-quality constraints.
- Kepler-10b benchmark suitability.
- Known scientific risks.

**J. Architecture and module design**
- Proposed module boundaries.
- Interfaces.
- Existing components to reuse.
- Expected files affected.

**K. Testing and validation plan**
- Synthetic data.
- Negative controls.
- Astronomical benchmarks.
- Integrity tests.
- Portable fixtures.

**L. Documentation plan**
- Exact existing documents likely to change during implementation.
- Purpose of each update.

**M. Stage 2.4 task breakdown**
- Responsibilities of 2.4.2 through 2.4.5.
- Dependencies.
- Potential overlap or missing work.

**N. Risks and unresolved decisions**
- Scientific uncertainties.
- Technical risks.
- Decisions requiring user approval.

**O. Implementation sequence**
- Ordered implementation recommendations.
- Expected verification points.
- Dependencies between steps.

**P. Readiness recommendation**
- Whether the design is ready for review and approval.
- Whether any prerequisites or decisions remain unresolved.
- Explicit confirmation that no implementation has occurred.

## 15. PLAN Restrictions

During this task:

- Do not modify source code.
- Do not modify tests.
- Do not modify documentation.
- Do not create or delete files.
- Do not install or update dependencies.
- Do not modify project data.
- Do not modify the original Kepler FITS file.
- Do not implement BLS or run analysis-development scripts.
- Do not commit, push, reset, clean, or alter Git history.
- Do not modify Foundation documents.
- Do not make unapproved architecture or scientific decisions.

Read-only repository inspection and appropriate existing test execution may be used to verify current functionality, provided they do not modify project files or data. If a command could modify files, explain the limitation and do not run it.

Clearly distinguish verified facts, recommendations, assumptions, and unresolved decisions.

**Stop after presenting the PLAN report. Wait for user review and explicit approval before implementation.**


# BUILD MODE PROMPT

# BUILD — Task 2.4.1: BLS Analysis Design and Implementation Planning

**Stage:** 2.4 — BLS Analysis and Uncertainty  
**Task:** 2.4.1 — BLS Analysis Design and Implementation Planning  
**Mode: BUILD — Complete the approved design and documentation work only.**

## 1. Objective

Complete Task 2.4.1 by establishing and documenting the approved scientific, technical, and architectural design for the application's initial Box Least Squares (BLS) transit-analysis capability.

This task converts the reviewed PLAN into an actionable design that subsequent Stage 2.4 tasks can implement.

The work includes:

- Finalizing the BLS input-data requirements.
- Establishing the data-preparation approach.
- Defining the BLS search configuration.
- Establishing the candidate-detection and parameter-extraction approach.
- Defining required analysis outputs.
- Establishing result and reproducibility requirements.
- Defining architecture and module responsibilities.
- Establishing testing and validation requirements.
- Clarifying the boundaries between Tasks 2.4.2–2.4.5.
- Updating the appropriate project documentation.

**This task does not implement the BLS algorithm, uncertainty calculations, or analysis interface.**

## 2. Mandatory Pre-Build Verification

Before making changes:

1. Read the approved Task 2.4.1 PLAN report.
2. Review the actual repository state.
3. Verify the prerequisite functionality identified in the PLAN.
4. Review the current Stage 2 roadmap and development log.
5. Review relevant architecture, data-model, data-flow, testing, and decision documents.
6. Identify the exact documentation and other files authorized for modification.
7. Check the current Git working-tree state.

The approved PLAN is the authority for this task.

If the actual repository differs materially from the approved PLAN, stop and report the discrepancy.

Do not silently change approved scientific or architectural decisions.

If the PLAN identifies unresolved decisions requiring user approval, do not invent answers. Document them as unresolved and request approval where necessary.

Preserve all existing user changes.

## 3. Finalize the BLS Scientific Input Design

Document how BLS will receive data from the existing light-curve model.

Establish the required inputs:

- Observation timestamps.
- Selected flux measurement.
- Measurement uncertainties, when available.
- Time units.
- Time reference and time scale.
- Relevant quality information.
- Dataset identity and provenance.

Preserve the initial detection-workflow direction:

- PDCSAP_FLUX is the default detection measurement.
- SAP_FLUX remains available for separate analysis.
- Their associated uncertainty fields remain distinct.

Document the actual existing data-model interfaces and identify any implementation prerequisites.

Do not modify the existing scientific data model as part of this task.

## 4. Finalize the Data-Preparation Design

Document how imported measurements will be prepared for BLS.

Address:

- Missing and non-finite timestamps.
- Missing and non-finite flux measurements.
- Missing and non-finite uncertainties.
- Nonzero quality flags.
- Irregular observation spacing.
- Insufficient observations.
- Duplicate or invalid timestamps, where relevant.
- Flux baseline and normalization requirements.
- Measurement uncertainty handling.

Clearly distinguish:

1. Original imported measurements.
2. Temporary analysis inputs.
3. Derived analysis representations.

Any approved preparation or transformation must be explicit, reproducible, and documented.

Original imported measurements must remain unchanged.

Do not introduce automatic detrending, normalization, or quality filtering unless the approved PLAN explicitly establishes and justifies the behavior.

Unresolved scientific choices must remain identified as unresolved rather than being silently decided.

## 5. Finalize the BLS Algorithm and Library Design

Document the approved BLS implementation approach.

Evaluate the existing:

`astropy.timeseries.BoxLeastSquares`

Record:

- Why the selected implementation is appropriate.
- Required inputs.
- Search configuration capabilities.
- Available candidate parameters.
- Relevant outputs.
- Known limitations.
- Any implementation constraints.

Confirm whether the existing dependencies are sufficient.

Do not install dependencies or implement algorithm functionality.

## 6. Finalize Search Configuration

Document the approved search-configuration strategy.

Address:

### Period search

- Minimum period.
- Maximum period.
- Period or frequency sampling.
- Search resolution.
- Oversampling requirements.
- Constraints imposed by observation baseline and cadence.

### Transit duration

- Minimum duration.
- Maximum duration.
- Duration sampling.
- Relationship between duration and candidate period.

### Configuration ownership

Identify which settings are:

- Automatically derived.
- Defaulted by the application.
- User-configurable.
- Required.
- Recorded for reproducibility.

Record the scientific reasoning behind the selected defaults and identify unresolved choices.

Do not invent numerical defaults where the approved PLAN does not establish a defensible basis.

## 7. Finalize Candidate Detection and Extraction Design

Document how the BLS workflow will:

1. Calculate the periodogram.
2. Identify candidate peaks.
3. Select candidate signals.
4. Extract candidate period.
5. Extract transit epoch.
6. Extract transit duration.
7. Extract transit depth.
8. Retain BLS power or equivalent detection statistics.
9. Represent multiple candidate peaks where appropriate.

Document how the design addresses:

- Period aliases.
- Harmonics.
- Competing candidate peaks.
- Insufficient observations.
- Potential false detections.

Explicitly distinguish a transit-like signal from a confirmed planetary detection.

Do not implement candidate detection.

## 8. Finalize Results and Visualization Requirements

Document the required outputs for the initial BLS workflow.

### Periodogram

Define the required information:

- Period or frequency.
- BLS power.
- Candidate peak locations.
- Selected candidate.
- Relevant search configuration.

### Phase-folded light curve

Define:

- Folded observations.
- Selected flux measurement.
- Candidate transit model.
- Measurement uncertainties, when available.
- Appropriate units and labels.

### Candidate parameters

Define how the application will represent:

- Period.
- Epoch.
- Duration.
- Depth.
- BLS power.
- Relevant warnings and limitations.

Identify which existing plotting components and interfaces should be reused.

Do not implement the visualizations or modify existing plotting functionality.

## 9. Finalize Analysis Result and Reproducibility Requirements

Document the information that must accompany an analysis result.

Include, where available:

- Project identity.
- Dataset identity.
- Selected flux measurement.
- Associated uncertainty measurement.
- Search configuration.
- Data-preparation steps.
- Algorithm and software version information.
- Candidate parameters.
- Periodogram information or the ability to regenerate it.
- Warnings and limitations.

Ensure the proposed result structure can support future Stage 2.5 operation recording.

Respect the existing deferred storage decision.

Do not implement persistence changes or the complete operation-history system.

## 10. Finalize Architecture and Module Responsibilities

Document the approved architectural design.

Identify:

- Where BLS algorithm functionality will reside.
- How input data will be supplied.
- How search configuration will be represented.
- How results will be represented.
- How errors and warnings will be communicated.
- How visualization will consume analysis results.
- How uncertainty calculations will eventually consume BLS outputs.
- How the analysis will remain independent of the graphical interface.

Identify actual repository modules and likely files affected by subsequent implementation.

Prefer existing architectural patterns.

Do not introduce unnecessary abstractions, dependencies, or storage changes.

## 11. Finalize Testing and Scientific Validation Requirements

Document the testing strategy for subsequent implementation.

Include controlled synthetic datasets with known:

- Transit periods.
- Transit epochs.
- Transit durations.
- Transit depths.
- Noise levels.

Include test scenarios involving:

- Clean transit signals.
- Noisy transit signals.
- Missing observations.
- Irregular sampling.
- Noise-only controls.
- Insufficient observations.

Document how recovered values will be evaluated.

Establish how the available Kepler-10b dataset will be used as an optional benchmark.

Its published orbital period is approximately 0.837491225 days, and the available Q0 observation span is approximately 9.7 days. Document the implications of this limited observation baseline.

Routine tests must use portable fixtures and temporary data. The standard test suite must not depend on the user's permanent FITS file or absolute local paths.

Do not create or implement the test suite during this task.

## 12. Finalize Stage 2.4 Task Boundaries

Document the responsibilities and dependencies of the proposed subsequent tasks:

### Task 2.4.2 — BLS Transit Search Implementation

Responsible for implementing the approved BLS search, periodogram calculation, candidate extraction, and core analysis functionality.

### Task 2.4.3 — Transit Parameter Uncertainty and Detection Assessment

Responsible for scientifically justified parameter uncertainty estimation, detection assessment, calibration, and interpretation.

### Task 2.4.4 — Application Integration and Analysis Results

Responsible for integrating BLS into the application and presenting analysis configuration and results.

### Task 2.4.5 — Testing, Scientific Validation, and Completion Verification

Responsible for final integrated testing, synthetic and astronomical validation, scientific integrity verification, documentation reconciliation, and Stage 2.4 completion assessment.

Review these boundaries against the approved PLAN.

Do not formally change the roadmap or expand the task breakdown without user approval.

## 13. Documentation Maintenance

Follow the documentation-maintenance requirements in `AGENTS.md`.

Update the appropriate existing documentation based on the approved PLAN and actual repository structure.

Review the need for updates to:

- Stage roadmap.
- Development log.
- Architecture documentation.
- Data-flow documentation.
- Module responsibilities.
- Data-model documentation, if necessary.
- Testing and validation documentation.
- Project state and continuity records.
- Decision records, where a genuine new decision is required.

Documentation must distinguish:

- Verified existing functionality.
- Approved design decisions.
- Proposed implementation details.
- Unresolved decisions.
- Deferred functionality.

Update Task 2.4.1 status only when its design and documentation deliverables are actually complete.

Do not mark Tasks 2.4.2–2.4.5 complete.

Do not modify Foundation documents.

Do not create duplicate documentation where an existing document is appropriate.

## 14. Explicit Scope Exclusions

Do not:

- Implement BLS.
- Calculate BLS periodograms.
- Implement candidate detection.
- Implement transit parameter uncertainty.
- Implement false alarm probability.
- Implement detection calibration.
- Build the BLS interface.
- Modify the existing table or light-curve plot.
- Implement transit fitting.
- Implement atmospheric characterization.
- Implement archive integration.
- Redesign permanent storage.
- Implement complete operation-history recording.
- Perform unrelated refactoring.
- Introduce unapproved dependencies.

If a prerequisite defect or necessary scope expansion is discovered, stop and report it rather than silently expanding the task.

## 15. Final Verification

After completing the design and documentation updates:

1. Compare the resulting documentation against the approved PLAN.
2. Verify that all required scientific and architectural decisions are documented.
3. Check that unresolved decisions are clearly identified.
4. Verify that subsequent task boundaries are consistent.
5. Ensure documentation does not describe planned functionality as implemented.
6. Check that no Foundation documents were modified.
7. Review the working-tree diff to identify every change.
8. Confirm no source-code or scientific-data modifications occurred.

Do not claim that implementation functionality was tested when this task only establishes its design.

## 16. Required Final Report

Provide a report with the following sections:

### A. Task completion summary
- What design work was completed.
- Whether Task 2.4.1 completion criteria were met.

### B. Scientific design
- Input requirements.
- Data-preparation decisions.
- Search configuration.
- Candidate detection and extraction.
- Results and visualization requirements.

### C. Architecture
- Approved module responsibilities.
- Interfaces and data flow.
- Future implementation boundaries.

### D. Reproducibility
- Required analysis metadata.
- Result representation.
- Compatibility with Stage 2.5.

### E. Testing and validation design
- Synthetic-data strategy.
- Negative controls.
- Kepler-10b benchmark considerations.
- Scientific integrity requirements.

### F. Files changed
For every changed file, explain:
- What changed.
- Why it changed.
- Which approved PLAN requirement it addresses.

Separate documentation changes from any other changes.

### G. Decisions and unresolved questions
List:
- Decisions finalized within the approved scope.
- Decisions intentionally deferred.
- Decisions requiring additional user approval.

### H. Documentation reconciliation
Identify:
- Documents updated.
- Documents inspected but intentionally unchanged.
- Remaining documentation gaps.

### I. Scope verification
Explicitly confirm whether:
- BLS algorithm code was left unimplemented.
- Uncertainty calculations were left unimplemented.
- Existing scientific data was unchanged.
- Existing plotting and table functionality was unchanged.
- No unapproved dependencies were added.
- No Foundation documents were modified.

### J. Task status and handoff
Recommend whether Task 2.4.1 is complete.

If complete, provide a concise handoff for Task 2.4.2, identifying the approved design, relevant modules, required interfaces, and implementation constraints.

Do not begin Task 2.4.2.

## 17. Git and User-Work Protections

- Do not commit.
- Do not push.
- Do not reset, clean, or alter Git history.
- Do not discard or overwrite user changes.
- Do not modify the original research FITS file.
- Do not modify Foundation documents.
- Do not perform destructive cleanup.

Leave all changes in the working tree for user review.

**Stop after presenting the final report. Wait for separate user approval before beginning Task 2.4.2.**