# PLAN MODE PROMPT

# PLAN — Task 2.4.3: Transit Parameter Uncertainty and Detection Assessment

**Stage:** 2.4 — BLS Analysis and Uncertainty  
**Task:** 2.4.3 — Transit Parameter Uncertainty and Detection Assessment  
**Mode: PLAN ONLY — Inspect, evaluate, and design. Do not modify the repository.**

## 1. Objective

Develop a detailed, scientifically justified, repository-specific implementation plan for estimating transit parameter uncertainties and assessing the statistical reliability of BLS candidate signals.

Task 2.4.2 implements the BLS search engine and produces structured candidate results. Task 2.4.3 must build on those results without duplicating or unnecessarily changing the existing BLS implementation.

The planning task must establish:

- Which transit parameters can receive meaningful uncertainty estimates.
- Which uncertainty-estimation methods are appropriate.
- How uncertainty estimates will be evaluated and empirically calibrated.
- How candidate signals will be assessed against an explicitly defined noise-only model.
- Whether and how false alarm probability (FAP) should be calculated.
- How aliases, harmonics, and competing candidates affect interpretation.
- How uncertainty and detection results will be represented.
- How unreliable or inconclusive assessments will be handled.
- How the functionality will be tested and scientifically validated.

**Do not implement uncertainty estimation, detection assessment, or FAP during PLAN.**

## 2. Mandatory Repository and Prerequisite Inspection

Inspect the actual repository before developing the plan.

Read and evaluate:

- `AGENTS.md`.
- Current Stage 2 roadmap.
- Development log.
- Completed Task 2.4.1 design.
- Task 2.4.2 implementation and completion report.
- BLS input-preparation implementation.
- BLS search configuration.
- Periodogram and candidate-detection implementation.
- Candidate parameter extraction.
- Structured BLS result classes or data structures.
- Existing measurement uncertainty handling.
- Relevant scientific architecture.
- Data-flow documentation.
- Module responsibilities.
- Testing and validation documentation.
- Existing decision records.
- Current test suite and dependency configuration.

Verify actual implementation status. Do not assume Task 2.4.2 is complete merely because the roadmap says so.

### Prerequisite verification

Determine whether the BLS implementation provides sufficient information for uncertainty and detection assessment.

Inspect:

- Candidate period.
- Candidate epoch.
- Candidate duration.
- Candidate depth.
- BLS power.
- Periodogram data.
- Search configuration.
- Input measurement identity.
- Measurement uncertainties.
- Time metadata.
- Data-preparation information.
- Excluded-observation information.
- Dataset identity and provenance.
- Existing warnings and limitations.

Identify missing information, incomplete interfaces, or implementation defects that could affect scientific reliability.

Do not silently repair Task 2.4.2 functionality or expand this task to include unrelated changes.

## 3. Review and Reconcile the Approved Scientific Design

Review the Task 2.4.1 design and the Task 2.4.2 implementation.

Extract the approved requirements relevant to uncertainty and detection assessment.

Determine:

- Which parameters require uncertainty estimates.
- What uncertainty methods were considered previously.
- Which methods were selected or deferred.
- What input information is available.
- What search information must be retained.
- What assumptions are already documented.
- What scientific limitations are already known.
- What responsibilities were assigned to Task 2.4.3.

Identify any discrepancies between the approved design and actual implementation.

Do not silently replace existing approved decisions.

Clearly distinguish:

1. Verified existing behavior.
2. Approved scientific decisions.
3. New recommendations.
4. Unresolved scientific questions.
5. Implementation prerequisites.

## 4. Transit Parameter Uncertainty Requirements

Evaluate uncertainty estimation for the following parameters:

- Period.
- Transit epoch.
- Transit duration.
- Transit depth.

For each parameter, determine:

- What information is required.
- Which uncertainty methods are suitable.
- Whether the available BLS outputs are sufficient.
- Whether additional calculations are necessary.
- How units and time references will be preserved.
- What limitations affect the estimate.
- How uncertainty will be represented in the result.

Investigate how uncertainty is affected by:

- Measurement noise.
- Measurement uncertainties.
- Observation cadence.
- Number of observations.
- Observation baseline.
- Number of observed transits.
- Transit coverage.
- Missing observations.
- Irregular sampling.
- Data quality.
- Search-grid resolution.
- Competing candidate peaks.

Do not assume all parameters have equivalent uncertainty behavior.

Do not assume a BLS parameter estimate automatically provides a statistically valid uncertainty estimate.

## 5. Evaluate Uncertainty Estimation Methods

Research and compare scientifically appropriate uncertainty-estimation methods.

Potential methods include:

- Bootstrap resampling.
- Monte Carlo simulations.
- Parameter perturbation.
- Local parameter-space exploration.
- Other statistically justified approaches.

For each candidate method, evaluate:

### Statistical validity

- What uncertainty does the method estimate?
- What assumptions does it make?
- Does it preserve the observation sampling?
- Does it incorporate measurement uncertainties?
- Does it account for correlated or time-dependent noise where relevant?
- Does it capture parameter correlations?
- Does it account for the BLS search process itself?

### Practical behavior

- Computational cost.
- Memory requirements.
- Reproducibility.
- Stability with small datasets.
- Sensitivity to noise.
- Sensitivity to missing observations.
- Behavior with weak or ambiguous signals.

### Limitations

Identify cases where a method may underestimate uncertainty, overestimate uncertainty, or produce misleading results.

Recommend a method or combination of methods based on scientific justification and the actual project requirements.

Do not select a method solely because it is easy to implement.

Do not implement or modify anything during PLAN.

## 6. UQ-009 — Empirical Calibration

Explicitly investigate and resolve the planning requirements associated with UQ-009: empirical calibration of BLS uncertainty estimates and tolerances.

Determine how the proposed uncertainty method will be evaluated against synthetic datasets with known input parameters.

Plan experiments using controlled transit signals with known:

- Periods.
- Epochs.
- Durations.
- Depths.
- Noise levels.
- Observation sampling.

Evaluate how to measure:

- Parameter-recovery errors.
- Reported uncertainty ranges.
- Empirical coverage.
- Bias.
- Stability across different noise conditions.
- Sensitivity to sampling and observation baseline.

Consider whether nominal uncertainty intervals actually contain the known input parameters at approximately their intended rates.

Define how calibration should be evaluated across repeated simulations.

Identify the number and diversity of simulations needed to make calibration conclusions meaningful.

Determine how calibration results will influence:

- Uncertainty methods.
- Numerical tolerances.
- Reliability warnings.
- Supported operating conditions.
- Known limitations.

Do not invent calibration success criteria without scientific justification.

If the required coverage levels, tolerances, or simulation requirements remain unresolved, identify the specific decisions that require approval.

The final plan must explain how UQ-009 will be addressed rather than simply marking it complete.

## 7. Detection Assessment Design

Evaluate methods for determining whether a BLS candidate is statistically distinguishable from an explicitly defined noise-only model.

Investigate suitable measures, which may include:

- BLS power.
- Signal-to-noise considerations.
- False alarm probability.
- Noise-only simulations.
- Other statistically justified detection statistics.

For each proposed measure, document:

- What it measures.
- Its assumptions.
- Required inputs.
- Its limitations.
- How it should be interpreted.
- Whether it is suitable for the initial application.

Keep these conclusions distinct:

1. A BLS candidate was detected.
2. The candidate is statistically distinguishable from the specified noise-only model.
3. The candidate represents a confirmed planet.

These are different conclusions.

Do not design a system that collapses them into a single confidence score without scientific justification.

## 8. False Alarm Probability and Null-Model Design

Evaluate whether FAP should be implemented in this task and identify an appropriate method.

If FAP is proposed, define the noise-only null hypothesis explicitly.

Investigate:

- Assumed noise distribution.
- Measurement uncertainty treatment.
- Observation sampling.
- Time-dependent or correlated noise.
- Whether the full BLS search must be repeated for every simulation.
- Search-range dependence.
- Candidate-selection effects.
- Computational requirements.
- Reproducibility requirements.

Consider whether sampling-preserving noise simulations are appropriate.

Evaluate whether shuffling or resampling observations would preserve the relevant properties of the data.

A noise-only dataset must not be treated as valid merely because it contains no known planet. It may still contain astrophysical variability or instrumental systematics.

### Required interpretation

FAP is conditional on the specified noise-only null model.

It is not:

- The probability that the candidate period is correct.
- The probability that the signal is a planet.
- Proof that aliases are absent.
- Proof that instrumental or astrophysical systematics are absent.

If FAP is not appropriate for the initial implementation, explain why and recommend an alternative assessment strategy.

Do not invent a universal FAP threshold or planetary-confidence classification.

## 9. Noise-Only Controls and Negative-Case Design

Develop a scientifically defensible validation strategy.

Evaluate possible controls:

- Synthetic noise-only datasets.
- Synthetic datasets with injected transit signals.
- Sampling-preserving simulations.
- Appropriate shuffling or resampling.
- Other justified control methods.

For each control, identify:

- What it tests.
- Which assumptions it requires.
- Which properties of the original observations it preserves.
- What conclusions it can support.
- What limitations remain.

Ensure that negative controls are suitable for the detection method being evaluated.

A dataset without a known transit is not automatically a noise-only control.

Plan how false detections and missed detections will be evaluated.

## 10. Aliases, Harmonics, and Competing Candidate Assessment

Evaluate how candidate reliability is affected by:

- Period aliases.
- Harmonics.
- Competing periodogram peaks.
- Data gaps.
- Short observation baselines.
- Incomplete transit coverage.
- Stellar variability.
- Instrumental systematics.
- Correlated noise.
- Insufficient observation cadence.

Determine how these factors should affect uncertainty estimates and detection assessment.

Identify whether the existing Task 2.4.2 result structure retains sufficient information for this work.

Plan appropriate warnings and limitations.

Do not assume the highest-power candidate is necessarily the true period.

Do not treat a low FAP as proof that aliases or systematics are absent.

## 11. Uncertainty and Detection Result Representation

Inspect the existing BLS result structures and determine the smallest appropriate extension.

Plan how results should distinguish:

### Original BLS results

- Period.
- Epoch.
- Duration.
- Depth.
- BLS power.
- Periodogram.
- Search configuration.

### Additional uncertainty results

- Parameter uncertainty estimates.
- Uncertainty method.
- Assumptions.
- Calibration information.
- Reliability limitations.

### Detection-assessment results

- Detection statistics.
- FAP, if implemented.
- Null-model definition.
- Noise-model assumptions.
- Assessment outcome.
- Warnings and limitations.

Determine how the new results will retain their relationship to:

- Original BLS candidate.
- Dataset identity.
- Selected flux measurement.
- Associated uncertainty measurement.
- Search configuration.
- Data-preparation history.

The result structure must support future application integration and reproducibility.

Avoid overwriting original BLS outputs with uncertainty-adjusted or interpreted values.

Do not implement GUI presentation or permanent persistence.

## 12. Unreliable and Inconclusive Assessments

Plan how the system should handle cases where a reliable uncertainty estimate or detection assessment cannot be produced.

Consider:

- Weak signals.
- Insufficient observations.
- Insufficient transit coverage.
- Very short observation baselines.
- Poor measurement precision.
- Ambiguous candidate peaks.
- Strong aliases.
- Inadequate noise models.
- Unstable uncertainty estimates.
- Failed calibration checks.
- Incomplete parameter information.

Define the distinction between:

- Assessment completed with usable results.
- Assessment completed with important limitations.
- Assessment inconclusive.
- Assessment could not be performed.

Do not manufacture uncertainty values or confidence classifications when the available data do not support them.

## 13. Architecture and File-Level Implementation Plan

Map the proposed implementation onto the actual repository.

Identify:

- New modules that may be required.
- Existing modules likely to be modified.
- Existing modules that should remain unchanged.
- Proposed classes and functions.
- Inputs and outputs.
- Interfaces with Task 2.4.2 BLS results.
- Dependencies between uncertainty and detection-assessment components.
- Error-handling boundaries.
- Integration points for Task 2.4.4.

Prefer existing project conventions.

Keep scientific calculations independent of the graphical interface.

Do not redesign the BLS engine.

Do not introduce a general-purpose statistical framework or unnecessary abstractions.

Do not introduce dependencies without identifying the need and obtaining approval.

Provide a file-by-file implementation plan.

## 14. Testing and Scientific Validation Plan

Develop a detailed plan for testing both uncertainty estimation and detection assessment.

Use portable synthetic datasets and temporary files.

The standard test suite must not depend on the permanent Kepler-10b FITS file or an absolute local path.

### Parameter uncertainty tests

Include:

- Known transit parameter recovery.
- Uncertainty estimates for period.
- Uncertainty estimates for epoch.
- Uncertainty estimates for duration.
- Uncertainty estimates for depth.
- Different noise levels.
- Different observation baselines.
- Different transit coverage.
- Irregular sampling.
- Missing observations.
- Measurement uncertainty variations.
- Competing candidate peaks.

### Calibration tests

Plan repeated synthetic experiments to evaluate:

- Parameter bias.
- Uncertainty coverage.
- Calibration stability.
- Sensitivity to noise.
- Sensitivity to sampling.
- Conditions where uncertainty estimates fail.

### Detection assessment tests

Include:

- Noise-only datasets.
- Injected transit signals.
- Different signal strengths.
- Different noise conditions.
- Sampling-preserving controls.
- Aliases and harmonics.
- Competing peaks.
- Correlated or time-dependent noise, where supported.

Define how false-positive and false-negative behavior will be evaluated.

### Reproducibility

Determine how random seeds, simulation configuration, noise assumptions, and software versions will be retained.

Do not weaken existing tests or use arbitrary tolerances.

If a scientifically defensible tolerance cannot yet be established, identify it as an unresolved decision.

## 15. Kepler-10b Optional Benchmark

The existing local dataset is:

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

Plan how this dataset could be used as an optional real-data benchmark.

Account for:

- Short observation baseline.
- Number of observed transits.
- Transit coverage.
- Measurement uncertainties.
- Quality flags.
- Missing observations.
- Noise and systematics.

Do not assume this dataset alone can empirically calibrate uncertainty estimates or establish general detection reliability.

The original FITS file must remain unchanged.

Do not make standard automated tests depend on this file.

## 16. Performance and Resource Considerations

Evaluate computational requirements for:

- Bootstrap or Monte Carlo simulations.
- Repeated BLS searches, if required.
- Noise-only simulations.
- Parameter-space exploration.
- Calibration experiments.

Consider:

- Number of simulations.
- Period-grid size.
- Duration-grid size.
- Observation count.
- Memory usage.
- Runtime.
- Reproducibility.
- Future GUI responsiveness.

Identify reasonable safeguards and practical limits.

Do not sacrifice scientific validity for speed without documenting the trade-off.

Do not introduce unnecessary optimization infrastructure.

## 17. Documentation Plan

Follow the documentation-maintenance requirements in `AGENTS.md`.

Identify documentation that will need updates during the later Build phase.

Review the need for updates to:

- Stage roadmap.
- Development log.
- Architecture documentation.
- Data-flow documentation.
- Module responsibilities.
- Data-model or result-structure documentation.
- Testing and validation documentation.
- Scientific methodology and assumptions.
- Decision records.
- Project state and continuity records.

Ensure the plan includes documentation of:

- Uncertainty methods.
- Statistical assumptions.
- Calibration procedures.
- Null-model definitions.
- FAP interpretation, if applicable.
- Detection-assessment limitations.
- Reproducibility requirements.
- Conditions where results are unreliable.

Do not modify documentation during PLAN.

Do not modify Foundation documents.

## 18. Explicit Task Boundaries

### Included in Task 2.4.3

- Transit parameter uncertainty design and implementation planning.
- Evaluation of uncertainty-estimation methods.
- Empirical calibration planning for UQ-009.
- Detection-assessment design.
- Null-model design.
- FAP evaluation and implementation planning, if scientifically justified.
- Noise-only controls.
- Alias and competing-candidate assessment.
- Structured uncertainty and detection results.
- Scientific testing and calibration planning.
- Necessary documentation updates during Build.

### Excluded from Task 2.4.3

- Reimplementing the BLS search engine.
- Changing the approved BLS algorithm.
- Reworking BLS input preparation without an approved prerequisite correction.
- Building the complete analysis interface.
- GUI visualization integration.
- Full transit fitting.
- Detailed physical parameter estimation.
- Atmospheric characterization.
- Radial-velocity analysis.
- Archive integration.
- Permanent storage redesign.
- Complete operation-history recording.
- Unrelated refactoring.

Task 2.4.2 owns the BLS search engine.

Task 2.4.4 owns application integration and analysis-result presentation.

Task 2.4.5 owns final integrated testing, scientific validation, and completion verification.

Do not move responsibilities between tasks without explicit user approval.

## 19. Required PLAN Report

Return a detailed report with the following sections.

### A. Repository and prerequisite verification
- Actual repository state.
- Verified Task 2.4.1 status.
- Verified Task 2.4.2 status.
- Existing BLS result structures.
- Available input information.
- Missing prerequisites.

### B. Approved design reconciliation
- Existing approved requirements.
- Existing implementation behavior.
- Discrepancies.
- Unresolved decisions.

### C. Parameter uncertainty requirements
- Period.
- Epoch.
- Duration.
- Depth.
- Available input information.
- Known limitations.

### D. Uncertainty-method evaluation
For each candidate method:
- Scientific suitability.
- Assumptions.
- Advantages.
- Limitations.
- Computational requirements.
- Recommendation.

### E. UQ-009 calibration plan
- Synthetic experiment design.
- Known parameter inputs.
- Repeated simulations.
- Coverage evaluation.
- Bias and stability.
- Proposed calibration criteria.
- Unresolved decisions.

### F. Detection-assessment design
- Proposed statistics.
- Noise-only null model.
- Detection interpretation.
- Limitations.

### G. FAP assessment
- Whether FAP is appropriate.
- Proposed method, if applicable.
- Null-model assumptions.
- Search procedure.
- Interpretation.
- Limitations.

### H. Negative controls
- Noise-only controls.
- Injected signals.
- Sampling preservation.
- False-positive and false-negative evaluation.

### I. Aliases and competing candidates
- Period aliases.
- Harmonics.
- Competing peaks.
- Data gaps.
- Stellar and instrumental effects.
- Proposed handling.

### J. Result representation
- Proposed uncertainty fields.
- Detection-assessment fields.
- Calibration metadata.
- Dataset and candidate relationships.
- Reproducibility.

### K. Unreliable and inconclusive results
- Conditions.
- Assessment statuses.
- Warnings.
- Failure behavior.

### L. Architecture and file-level changes
- Proposed modules.
- Existing files to modify.
- New classes and functions.
- Interfaces.
- Dependencies.

### M. Testing and scientific validation
- Parameter uncertainty tests.
- Calibration experiments.
- Detection tests.
- Negative controls.
- Kepler-10b optional benchmark.
- Reproducibility.

### N. Performance considerations
- Computational cost.
- Simulation requirements.
- Memory.
- Practical safeguards.

### O. Documentation updates
- Exact documents.
- Proposed changes.
- Documents intentionally unchanged.

### P. Risks and unresolved decisions
- Scientific risks.
- Technical risks.
- Missing prerequisites.
- Decisions requiring user approval.

### Q. Proposed Build breakdown
Provide an ordered implementation sequence.

For each step, identify:
- Objective.
- Files involved.
- Dependencies.
- Tests.
- Expected outcome.

Keep the breakdown within Task 2.4.3.

### R. Readiness assessment
State whether Task 2.4.3 is ready for Build.

Identify all blockers and decisions requiring user approval.

## 20. PLAN Restrictions

During this task:

- Do not create or modify source files.
- Do not implement uncertainty calculations.
- Do not implement FAP.
- Do not implement detection assessment.
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

Clearly distinguish verified facts, approved decisions, recommendations, assumptions, and unresolved scientific questions.

**Stop after presenting the PLAN report. Wait for explicit user approval before making any changes.**


# BUILD MODE PROMPT

# BUILD — Task 2.4.3: Transit Parameter Uncertainty and Detection Assessment

**Stage:** 2.4 — BLS Analysis and Uncertainty  
**Task:** 2.4.3 — Transit Parameter Uncertainty and Detection Assessment  
**Mode: BUILD — Implement the approved uncertainty and detection-assessment functionality only.**

## 1. Objective

Implement scientifically justified transit parameter uncertainty estimation and detection assessment using the existing BLS search results from Task 2.4.2.

The implementation must follow:

1. The approved Task 2.4.1 scientific and technical design.
2. The completed Task 2.4.2 BLS implementation.
3. The reviewed and approved Task 2.4.3 PLAN report.
4. The existing repository architecture and data interfaces.
5. The project's Foundation requirements and `AGENTS.md` governance.

The objective is to extend the existing BLS analysis capability so that candidate results can be evaluated for:

- Parameter uncertainty.
- Uncertainty reliability.
- Empirical calibration.
- Statistical distinguishability from an explicitly defined noise-only model.
- Detection-assessment limitations.
- Conditions where results are unreliable or inconclusive.

**This task does not reimplement BLS or integrate the complete analysis workflow into the GUI.**

## 2. Mandatory Pre-Build Verification

Before making changes:

1. Read `AGENTS.md`.
2. Read the approved Task 2.4.1 design.
3. Read the completed Task 2.4.2 implementation report.
4. Read the approved Task 2.4.3 PLAN report.
5. Inspect the current repository state.
6. Verify that the BLS result structures provide the information required by the approved design.
7. Review existing uncertainty and measurement-error handling.
8. Review the current roadmap and development log.
9. Identify the exact source, test, and documentation files affected.
10. Inspect the Git working tree and preserve all existing user changes.

Reconcile the approved PLAN with the actual repository.

If a prerequisite is missing or differs materially from the approved PLAN, stop and report the discrepancy.

If an unresolved scientific decision requires approval, do not invent an answer.

Do not silently change the approved uncertainty method, null model, calibration criteria, or statistical interpretation.

## 3. Implement Transit Parameter Uncertainty Estimation

Implement the uncertainty-estimation methods selected in the approved PLAN.

The primary parameters are:

- Period.
- Transit epoch.
- Transit duration.
- Transit depth.

For each supported parameter, implement the approved method of estimating uncertainty.

The implementation must:

- Use the existing BLS candidate results.
- Preserve the original BLS parameter estimates.
- Keep uncertainty estimates separate from the original parameter values.
- Preserve appropriate units.
- Preserve timestamp references and time scales.
- Record the uncertainty-estimation method.
- Retain relevant assumptions and limitations.
- Handle cases where an uncertainty estimate cannot be produced.

### Scientific requirements

Do not assume that BLS parameter estimates automatically provide valid uncertainty estimates.

Do not assign uncertainty values based solely on arbitrary tolerances.

Do not treat all parameters as having identical uncertainty behavior.

Account for relevant factors established by the approved design, including:

- Measurement noise.
- Measurement uncertainties.
- Observation cadence.
- Observation baseline.
- Number of observed transits.
- Transit coverage.
- Missing observations.
- Irregular sampling.
- Search-grid resolution.
- Competing candidate peaks.

If the approved method does not support a reliable estimate for a particular parameter or dataset, report that limitation explicitly rather than manufacturing a value.

## 4. Implement the Approved Uncertainty Methods

Implement only the methods selected in the approved PLAN.

Potential methods may include:

- Bootstrap resampling.
- Monte Carlo simulations.
- Parameter perturbation.
- Local parameter-space exploration.
- Other statistically justified methods.

For each implemented method, ensure that:

1. Its required inputs are validated.
2. Its assumptions are documented.
3. Its random behavior is reproducible where applicable.
4. Its relationship to the original BLS candidate is preserved.
5. Its output can be interpreted independently of the original BLS estimate.
6. Its limitations are represented in the result.

Where simulation or resampling is used, preserve the relevant observation sampling and uncertainty characteristics according to the approved design.

Do not introduce additional methods simply because they are convenient to implement.

Do not replace an approved method without explicit authorization.

## 5. Implement UQ-009 Empirical Calibration

Address the previously unresolved UQ-009 requirement concerning empirical calibration of BLS uncertainty estimates and tolerances.

Implement the approved calibration strategy using controlled synthetic light curves with known input parameters.

### Synthetic experiment inputs

Use known:

- Periods.
- Transit epochs.
- Transit durations.
- Transit depths.
- Noise characteristics.
- Observation sampling.

### Calibration evaluation

Implement the approved methods for evaluating:

- Parameter-recovery errors.
- Reported uncertainty ranges.
- Empirical uncertainty coverage.
- Parameter bias.
- Calibration stability.
- Sensitivity to different noise levels.
- Sensitivity to observation cadence.
- Sensitivity to observation baseline.
- Sensitivity to incomplete transit coverage.

Where nominal uncertainty intervals are produced, evaluate whether they contain the known input parameters at approximately their intended coverage rates.

Use repeated simulations as required by the approved design.

### Calibration safeguards

- Do not claim calibration success based on a small number of favorable examples.
- Do not use arbitrary tolerances.
- Do not treat successful recovery of one synthetic signal as evidence of general reliability.
- Do not hide conditions where uncertainty estimates become unreliable.
- Do not claim empirical calibration beyond the conditions actually tested.

If the approved PLAN does not establish a scientifically defensible calibration criterion, stop and request approval rather than inventing one.

Record the calibration configuration, assumptions, and results sufficiently for reproducibility.

UQ-009 must not be marked resolved merely because a calibration function or test exists. Its completion must be supported by the approved calibration methodology and actual evidence.

## 6. Implement Detection Assessment

Implement the detection-assessment approach approved in the PLAN.

The purpose is to evaluate whether a BLS candidate is statistically distinguishable from the specified noise-only model.

Use the approved detection statistics and methods.

Potential components include:

- BLS power.
- Signal-to-noise measures.
- Noise-only simulations.
- False alarm probability.
- Other statistically justified measures.

For every implemented statistic, document:

- What it measures.
- Its required inputs.
- Its assumptions.
- Its limitations.
- How it should be interpreted.

Keep the following conclusions distinct:

1. A BLS candidate was detected.
2. The candidate is statistically distinguishable from the specified noise-only model.
3. The candidate represents a confirmed planet.

The implementation must not collapse these conclusions into one unsupported confidence value.

Do not introduce arbitrary detection thresholds or planetary-confidence classifications.

## 7. Implement the Approved Noise-Only Null Model

If the approved PLAN selects FAP or another noise-based detection statistic, implement the specified null model.

Document and preserve:

- Null hypothesis.
- Noise distribution or model.
- Measurement uncertainty treatment.
- Observation sampling.
- Relevant temporal or correlated-noise assumptions.
- Search configuration.
- Simulation procedure.
- Number of simulations.
- Random seed or reproducibility information.
- Relevant software versions.

If simulations are used, implement the approved simulation process.

Where required by the approved methodology, repeat the full BLS search for simulated datasets so that the statistical assessment accounts for the search procedure.

Do not substitute an easier statistical calculation without approval.

### False alarm probability interpretation

If FAP is implemented, ensure its meaning is explicit.

FAP is conditional on the specified noise-only null model.

It is not:

- The probability that the candidate period is correct.
- The probability that the candidate is a planet.
- Proof that aliases are absent.
- Proof that instrumental or astrophysical systematics are absent.

Do not describe a low FAP as planetary confirmation.

If the approved PLAN determines FAP is inappropriate for the initial implementation, implement the approved alternative and document why FAP was deferred.

## 8. Implement Noise-Only Controls and Negative Cases

Implement the control-generation or evaluation methods established by the approved design.

Potential controls include:

- Synthetic noise-only datasets.
- Synthetic datasets with injected transit signals.
- Sampling-preserving simulations.
- Approved shuffling or resampling methods.

Ensure that controls preserve the relevant properties required by the selected statistical method.

Do not assume that a dataset without a known transit is automatically a valid noise-only control.

Where appropriate, evaluate:

- False-positive behavior.
- False-negative behavior.
- Detection sensitivity.
- Dependence on noise level.
- Dependence on sampling.
- Dependence on observation baseline.

Document what each control can and cannot establish.

## 9. Implement Alias and Competing-Candidate Assessment

Implement the approved methods for accounting for aliases and competing candidates.

Use information retained by the BLS implementation, including periodogram and candidate information where available.

Address:

- Period aliases.
- Harmonics.
- Competing peaks.
- Data gaps.
- Short observation baselines.
- Incomplete transit coverage.
- Stellar variability.
- Instrumental systematics.
- Correlated noise.

The assessment should retain relevant warnings and limitations.

Do not automatically select the strongest peak as the correct physical period.

Do not claim that a low FAP eliminates aliases or systematic effects.

If the existing BLS results do not retain enough information to support an approved assessment, report the prerequisite defect rather than silently redesigning Task 2.4.2.

## 10. Extend Structured Analysis Results

Extend the existing BLS result structures using the approved design.

Preserve the original BLS outputs and add separate uncertainty and detection-assessment information.

### Original BLS results

Retain:

- Period.
- Epoch.
- Duration.
- Depth.
- BLS power.
- Periodogram.
- Search configuration.

### Uncertainty results

Represent the approved information, including where applicable:

- Parameter uncertainty estimates.
- Uncertainty method.
- Method configuration.
- Assumptions.
- Calibration information.
- Reliability limitations.
- Failure or inconclusive status.

### Detection-assessment results

Represent the approved information, including where applicable:

- Detection statistics.
- FAP.
- Null-model definition.
- Noise-model assumptions.
- Simulation configuration.
- Assessment outcome.
- Warnings and limitations.

Preserve relationships to:

- Original BLS candidate.
- Dataset identity.
- Selected flux measurement.
- Associated uncertainty measurement.
- Search configuration.
- Data-preparation information.

Avoid overwriting original BLS values with interpreted or adjusted values.

Ensure the result structure remains independent of the GUI.

Do not implement permanent persistence or complete operation-history recording.

## 11. Implement Unreliable and Inconclusive Assessment Handling

Implement explicit handling for conditions where meaningful uncertainty or detection assessment cannot be produced.

Include the conditions identified in the approved PLAN, such as:

- Weak signals.
- Insufficient observations.
- Insufficient transit coverage.
- Short observation baselines.
- Poor measurement precision.
- Ambiguous candidate peaks.
- Strong aliases.
- Inadequate noise models.
- Unstable uncertainty estimates.
- Failed calibration checks.
- Incomplete candidate information.

Distinguish between:

1. Assessment completed with usable results.
2. Assessment completed with important limitations.
3. Assessment inconclusive.
4. Assessment could not be performed.

Do not substitute fabricated uncertainty or confidence values when an assessment fails.

Warnings and failure information must remain accessible to later application-integration work.

## 12. Implement Testing and Scientific Validation

Implement tests according to the approved PLAN.

Use portable synthetic datasets and temporary files.

The standard test suite must not depend on the permanent Kepler-10b FITS file or an absolute local path.

### Parameter uncertainty tests

Include appropriate tests for:

- Period uncertainty.
- Epoch uncertainty.
- Duration uncertainty.
- Depth uncertainty.
- Known-parameter recovery.
- Different noise levels.
- Different observation baselines.
- Different transit coverage.
- Irregular sampling.
- Missing observations.
- Different measurement uncertainties.
- Competing candidate peaks.

### Calibration tests

Verify:

- Repeated simulation behavior.
- Parameter bias.
- Uncertainty coverage.
- Calibration stability.
- Sensitivity to noise.
- Sensitivity to observation sampling.
- Conditions where estimates become unreliable.

### Detection-assessment tests

Include:

- Noise-only datasets.
- Injected transit signals.
- Different signal strengths.
- Different noise conditions.
- Sampling-preserving controls.
- Aliases and harmonics.
- Competing candidate peaks.
- Correlated or time-dependent noise where supported.

Evaluate false-positive and false-negative behavior according to the approved design.

### Reproducibility tests

Verify that applicable simulation settings, random seeds, noise assumptions, and method configurations are retained.

### Test quality

- Tests must verify meaningful statistical behavior.
- Do not weaken existing tests.
- Do not invent arbitrary tolerances.
- Do not claim empirical calibration without supporting evidence.
- Do not treat a passing unit test as proof of scientific validity.

If the approved PLAN leaves an essential test criterion unresolved, request approval rather than silently selecting a value.

## 13. Kepler-10b Optional Verification

The available local research dataset is:

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

Account for:

- Limited observation baseline.
- Number of observed transits.
- Transit coverage.
- Measurement uncertainties.
- Quality flags.
- Missing observations.
- Noise and systematics.

Do not assume that this dataset alone can establish general uncertainty calibration or detection reliability.

Do not treat a failure to recover the published signal as automatic proof of an implementation defect.

Do not make standard automated tests depend on this file.

## 14. Performance and Resource Considerations

Implement reasonable computational safeguards consistent with the approved design.

Consider:

- Number of simulations.
- Repeated BLS searches.
- Period-grid size.
- Duration-grid size.
- Observation count.
- Memory use.
- Runtime.
- Random-seed reproducibility.
- Avoiding unnecessary data copies.

Do not compromise scientific validity for speed without documenting the trade-off.

Do not introduce unnecessary optimization infrastructure or unapproved downsampling.

## 15. Documentation Maintenance

Follow the documentation-maintenance requirements in `AGENTS.md`.

Update the appropriate existing documentation as implementation changes scientific functionality, interfaces, architecture, testing, and project progress.

Review and update where appropriate:

- Stage roadmap.
- Development log.
- Architecture documentation.
- Data-flow documentation.
- Module responsibilities.
- Data-model and result-structure documentation.
- Testing and validation documentation.
- Scientific methodology and assumptions.
- Decision records, where genuinely required.
- Project state and continuity records.

Documentation must accurately describe:

- Implemented uncertainty methods.
- Statistical assumptions.
- Calibration methodology.
- Actual calibration evidence.
- Noise-only null model.
- Detection statistics.
- FAP interpretation, if implemented.
- Reproducibility requirements.
- Known limitations.
- Conditions where assessments are unreliable.

Clearly distinguish planned functionality from implemented and tested functionality.

Update UQ-009 status only when its actual completion criteria and evidence support doing so.

Do not mark Task 2.4.3 complete if required calibration or detection-assessment work remains incomplete.

Do not mark Tasks 2.4.4 or 2.4.5 complete.

Do not modify Foundation documents.

Do not create duplicate documentation where an existing document is appropriate.

## 16. Explicit Scope Exclusions

Do not:

- Reimplement the BLS search engine.
- Replace or change the approved BLS algorithm.
- Redesign BLS input preparation.
- Implement the complete analysis interface.
- Integrate periodogram visualization into the GUI.
- Integrate phase-folded visualization into the GUI.
- Implement full transit fitting.
- Perform detailed physical parameter estimation.
- Implement atmospheric characterization.
- Implement radial-velocity analysis.
- Integrate external archives.
- Redesign permanent storage.
- Implement complete operation-history recording.
- Perform unrelated refactoring.

These responsibilities remain with their designated tasks.

If an implementation requirement crosses these boundaries, stop and report it.

## 17. Final Verification

After implementation:

1. Run targeted uncertainty tests.
2. Run calibration tests.
3. Run detection-assessment tests.
4. Run relevant regression tests.
5. Run the full test suite.
6. Record the exact commands and results.
7. Investigate failures rather than suppressing them.
8. Review the working-tree diff.
9. Verify that original BLS results remain distinguishable from uncertainty and assessment results.
10. Verify that statistical assumptions and simulation settings are retained.
11. Verify that original scientific measurements remain unchanged.
12. Compare implementation against the approved PLAN.
13. Reconcile documentation against actual code and test evidence.
14. Identify remaining limitations and incomplete requirements.

Do not claim scientific calibration or validation beyond what the actual experiments establish.

Do not claim tests passed unless they were actually executed successfully.

## 18. Required Final Report

Provide a report with the following sections.

### A. Implementation summary
- Functionality implemented.
- Overall completion status.
- Relationship to the approved design and PLAN.

### B. Parameter uncertainty implementation
- Parameters supported.
- Methods used.
- Assumptions.
- Units and time references.
- Limitations.

### C. UQ-009 calibration
- Calibration methodology.
- Synthetic experiment configuration.
- Number and diversity of simulations.
- Parameter-recovery results.
- Coverage results.
- Bias and stability.
- Calibration conclusions.
- Remaining limitations.

### D. Detection assessment
- Statistics implemented.
- Noise-only null model.
- FAP implementation, if applicable.
- Assumptions.
- Interpretation.
- Limitations.

### E. Negative controls and candidate reliability
- Controls implemented.
- Injected-signal results.
- Noise-only results.
- False-positive and false-negative behavior.
- Alias and competing-candidate handling.

### F. Structured results
- New result fields.
- Original BLS result preservation.
- Reproducibility information.
- Compatibility with Task 2.4.4.

### G. Error and inconclusive handling
- Supported assessment states.
- Warning behavior.
- Failure conditions.
- Known limitations.

### H. Files changed
For every changed file, explain:
- What changed.
- Why it changed.
- Which approved PLAN requirement it addresses.

Separate source-code, test, and documentation changes.

### I. Test and validation results
Include:
- Exact commands executed.
- Targeted test results.
- Calibration test results.
- Detection-assessment test results.
- Regression test results.
- Full suite results.
- Failures or skipped tests.
- Limitations of the evidence.

### J. Scientific integrity verification
Explicitly report whether:
- Original BLS outputs remain preserved.
- Uncertainty results are separate.
- Detection results are separate.
- Statistical assumptions are retained.
- Original measurements remain unchanged.
- SAP and PDCSAP remain separate.
- Uncertainty associations remain correct.
- Time metadata is preserved.
- No unapproved transformations were introduced.

### K. Documentation reconciliation
Identify:
- Documents updated.
- Documents inspected but intentionally unchanged.
- Remaining documentation gaps.

### L. Scope verification
Explicitly confirm whether:
- Uncertainty estimation was implemented.
- UQ-009 was addressed with actual calibration evidence.
- Detection assessment was implemented.
- The noise-only null model was documented.
- FAP was implemented or appropriately deferred.
- BLS search functionality was left intact.
- GUI integration was left to Task 2.4.4.
- Final integrated validation was left to Task 2.4.5.
- No unapproved dependencies were added.
- No Foundation documents were modified.

### M. Remaining issues and handoff
List:
- Incomplete requirements.
- Known scientific limitations.
- Unresolved decisions.
- Any remaining UQ-009 work.
- Information needed by Task 2.4.4.
- Recommended next steps.

Recommend whether Task 2.4.3 is complete.

Do not begin Task 2.4.4.

## 19. Git and User-Work Protections

- Do not commit.
- Do not push.
- Do not reset, clean, or alter Git history.
- Do not discard or overwrite user changes.
- Do not modify the original research FITS file.
- Do not modify Foundation documents.
- Do not perform destructive cleanup.

Leave all changes in the working tree for user review.

**Stop after presenting the final report. Wait for separate user approval before beginning Task 2.4.4.**