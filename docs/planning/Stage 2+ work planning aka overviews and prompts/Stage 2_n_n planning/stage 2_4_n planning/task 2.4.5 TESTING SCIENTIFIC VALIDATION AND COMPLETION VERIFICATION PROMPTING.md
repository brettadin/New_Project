# PLAN MODE PROMPT

# PLAN — Task 2.4.5: Testing, Scientific Validation, and Completion Verification

**Stage:** 2.4 — BLS Analysis and Uncertainty  
**Task:** 2.4.5 — Testing, Scientific Validation, and Completion Verification  
**Mode: PLAN ONLY — Inspect, evaluate, and design. Do not implement.**

## 1. Objective

Inspect the actual repository and develop a comprehensive, evidence-based plan for testing, scientifically validating, and verifying completion of Stage 2.4.

Stage 2.4 consists of:

- Task 2.4.1 — BLS Analysis Design and Implementation Planning.
- Task 2.4.2 — BLS Transit Search Implementation.
- Task 2.4.3 — Transit Parameter Uncertainty and Detection Assessment.
- Task 2.4.4 — Application Integration and Analysis Results.

The objective is to determine what evidence is needed to establish that the complete BLS analysis workflow:

1. Correctly processes imported photometric light curves.
2. Identifies candidate periodic transit-like signals.
3. Extracts meaningful transit parameters.
4. Produces uncertainty estimates that are empirically supported.
5. Assesses candidate signals against a specified noise-only null model.
6. Handles aliases, harmonics, and competing candidates responsibly.
7. Presents results correctly through the application.
8. Preserves original scientific measurements.
9. Produces reproducible and traceable analysis results.
10. Meets the requirements and completion criteria established for Stage 2.4.

This is a verification-planning task.

**Do not implement corrections, change scientific algorithms, modify tests, or edit documentation during PLAN.**

## 2. Mandatory Repository and Documentation Inspection

Before developing the plan, inspect the actual repository.

Read and follow:

- `AGENTS.md`.
- The current Stage 2 roadmap.
- The development log.
- Relevant architecture documentation.
- Data-flow documentation.
- Data-model documentation.
- Module responsibility documentation.
- Testing and validation documentation.
- Relevant decision records.
- Project state and continuity documentation.

Inspect the actual implementation and completion evidence for:

- Task 2.4.1 — BLS Analysis Design.
- Task 2.4.2 — BLS Transit Search.
- Task 2.4.3 — Transit Parameter Uncertainty and Detection Assessment.
- Task 2.4.4 — Application Integration and Analysis Results.

Also inspect relevant Stage 2.2 and 2.3 functionality because Stage 2.4 depends on imported datasets, measurements, uncertainties, project integration, and visualization.

### Verify actual repository state

Inspect:

- Current Git branch and working-tree status.
- Existing user modifications.
- Relevant source files.
- Existing test files.
- Test fixtures and synthetic-data generators.
- Scientific validation scripts, if any.
- Documentation and completion records.
- Actual dependency and environment configuration.

Record the exact file paths, classes, functions, and test names relevant to verification.

Do not assume that previous task completion reports accurately describe the current repository.

Do not assume that a test passed simply because a previous report says it did.

If tests are run during PLAN, record the exact command and actual result.

Do not modify the repository through inspection or testing.

## 3. Stage 2.4 Requirements Traceability

Build a traceability assessment connecting the original Stage 2.4 objective to the actual implementation and available evidence.

Evaluate at least these requirements:

1. BLS search implementation.
2. Input validation and data preparation.
3. Search configuration.
4. Candidate identification and parameter extraction.
5. Periodogram and candidate representation.
6. Parameter uncertainty estimation.
7. Empirical uncertainty calibration.
8. Detection assessment against a specified noise-only null.
9. FAP interpretation, if implemented.
10. Aliases, harmonics, and competing candidates.
11. Application integration.
12. Scientific visualization.
13. Reproducibility and traceability.
14. Scientific data integrity.
15. Automated testing.
16. Documentation.

For each requirement, identify:

- Original requirement or approved design reference.
- Actual implementation location.
- Existing tests.
- Existing scientific validation evidence.
- Remaining evidence needed.
- Current assessment.

Use the following classifications:

- Complete and verified.
- Implemented but insufficiently verified.
- Partially complete.
- Incomplete.
- Deferred with documented justification.
- Blocked.

Distinguish code implementation from evidence of correctness.

Do not classify functionality as scientifically validated merely because it executes successfully.

## 4. Review of Existing Test Coverage

Evaluate the existing automated test suite before recommending new tests.

Inspect the actual test structure and identify:

- Tests already covering required behavior.
- Tests that cover only basic execution.
- Tests that use synthetic data.
- Tests that use controlled known parameters.
- Tests that test failure conditions.
- Tests that test integration boundaries.
- Tests that may be redundant.
- Missing test cases.
- Tests that rely on machine-specific files or paths.
- Tests that may be nondeterministic.

Organize the assessment by subsystem.

### BLS tests

Review coverage for:

- Valid inputs.
- Invalid inputs.
- Search configuration.
- Period range.
- Duration configuration.
- Search resolution.
- Candidate extraction.
- Parameter recovery.
- Multiple peaks.
- Competing signals.
- Missing and non-finite measurements.
- Irregular sampling.
- Data gaps.
- Different noise conditions.
- Insufficient observation baselines.
- Failure handling.

### Uncertainty tests

Review coverage for:

- Period uncertainty.
- Epoch uncertainty.
- Duration uncertainty.
- Depth uncertainty.
- Reproducibility.
- Bias.
- Coverage.
- Stability.
- Noise sensitivity.
- Sampling sensitivity.
- Baseline sensitivity.
- Unavailable and unreliable estimates.
- Inconclusive results.
- Failure handling.

### Detection-assessment tests

Review coverage for:

- Noise-only datasets.
- Injected signals.
- False positives.
- False negatives.
- Null-model assumptions.
- FAP, if implemented.
- Simulation reproducibility.
- Sampling preservation.
- Time-correlated noise, if supported.
- Competing candidates.
- Aliases and harmonics.
- Inconclusive results.

### Application tests

Review coverage for:

- Dataset selection.
- Flux measurement selection.
- Correct uncertainty association.
- BLS configuration and execution.
- Candidate presentation.
- Uncertainty presentation.
- Detection-assessment presentation.
- Visualization.
- Candidate switching.
- Project and dataset switching.
- Partial-result handling.
- Stale-result prevention.
- Error handling.

Identify where existing tests already provide sufficient evidence. Do not recommend duplicating them without a reason.

## 5. Scientific Validation of BLS Candidate Detection

Design a controlled validation strategy for the BLS implementation.

Use synthetic light curves with known input parameters.

Inspect the actual BLS implementation to determine which parameters and operating conditions need validation.

Consider varying:

- Orbital period.
- Transit epoch.
- Transit duration.
- Transit depth.
- Noise level.
- Observation cadence.
- Observation baseline.
- Number of observations.
- Missing observations.
- Irregular sampling.
- Data gaps.
- Competing periodic signals.

For each validation condition, define:

- Input parameters.
- Synthetic-data construction.
- Expected behavior.
- Measured output.
- Comparison method.
- Acceptance or interpretation criteria.
- Relevant limitations.

Evaluate:

- Period recovery.
- Epoch recovery.
- Duration recovery.
- Depth recovery.
- Candidate ranking.
- Sensitivity to noise.
- Sensitivity to sampling.
- Sensitivity to baseline.
- Behavior with missing observations.
- Behavior with competing signals.

Do not invent arbitrary tolerances.

Where the approved design already establishes tolerances, use those.

Where no tolerance exists, identify the missing decision and recommend a scientifically defensible way to establish one.

Distinguish numerical implementation correctness from the broader scientific reliability of the method.

## 6. Empirical Uncertainty Calibration — UQ-009

Treat UQ-009 as a central requirement of this planning task.

Inspect the actual Task 2.4.3 uncertainty methodology and determine what evidence is necessary to evaluate whether its uncertainty estimates are reliable.

Identify the actual method or methods implemented, such as bootstrap, Monte Carlo, perturbation, local parameter-space exploration, or another approved approach.

Do not assume which method was selected without inspecting the code and approved design.

### Calibration dataset design

Plan repeated synthetic simulations with known:

- Period.
- Epoch.
- Duration.
- Depth.
- Noise characteristics.
- Observation cadence.
- Observation baseline.

Include multiple realistic operating conditions.

Determine how many simulations are required for the intended evaluation and justify the proposed sample sizes.

Avoid selecting an arbitrary number of simulations without considering statistical precision and computational cost.

### Calibration measurements

For each parameter, evaluate:

- True input value.
- Recovered estimate.
- Estimated uncertainty.
- Actual estimation error.
- Bias.
- Empirical coverage.
- Stability across repeated simulations.
- Failure or unavailable-estimate frequency.

Where the uncertainty method produces intervals, evaluate whether the nominal coverage corresponds to observed coverage.

For example, a nominal 68% interval should be evaluated against the fraction of repeated known input values actually contained within the intervals.

If the method produces standard errors rather than intervals, define an appropriate calibration assessment.

### Calibration across conditions

Evaluate uncertainty performance under:

- Different noise levels.
- Different transit depths.
- Different transit durations.
- Different observation cadences.
- Different baseline lengths.
- Missing observations.
- Irregular sampling.
- Other relevant conditions identified in Task 2.4.3.

Identify conditions under which uncertainty estimates become biased, unstable, or unreliable.

### Calibration acceptance criteria

Determine whether Task 2.4.3 already defines acceptable calibration criteria.

If it does, use those criteria.

If it does not, identify the unresolved decision and recommend criteria based on:

- Intended uncertainty interpretation.
- Simulation sample size.
- Expected statistical variation.
- Parameter-specific behavior.
- Relevant scientific limitations.

Do not silently invent a universal acceptance threshold.

### UQ-009 resolution assessment

Define the evidence needed to classify UQ-009 as:

- Resolved.
- Partially resolved.
- Unresolved.
- Blocked by a methodological or implementation defect.

Explain what would prevent the uncertainty estimates from being described as reliable.

Do not recommend claiming successful calibration solely because the uncertainty calculations return numerical values.

## 7. Detection Assessment and Noise-Only Validation

Inspect the actual Task 2.4.3 detection-assessment implementation.

Identify:

- Null-model definition.
- Noise distribution.
- Measurement uncertainty handling.
- Observation sampling.
- Time-correlated noise treatment.
- Search period range.
- Candidate-selection procedure.
- Simulation procedure.
- Simulation count.
- Random seed handling.
- FAP calculation, if implemented.
- Computational limitations.

Develop a validation strategy appropriate to the implemented method.

### Noise-only controls

Design controlled datasets without injected transit signals.

Evaluate how frequently the complete search procedure reports apparently significant candidates.

Preserve relevant observation sampling and uncertainty characteristics.

Determine whether the null model accounts for the same search procedure used on real data.

If candidate selection involves searching many periods or durations, assess whether the validation repeats the full search rather than evaluating only a preselected period.

Do not assume that an observation period without a known planet is a pure-noise control.

### Injected-signal controls

Design controlled tests that introduce known transit signals into otherwise appropriate datasets.

Evaluate:

- Detection rate.
- Missed-signal rate.
- False-positive behavior.
- Sensitivity to signal strength.
- Sensitivity to noise.
- Sensitivity to sampling and baseline.
- Candidate-ranking behavior.

### FAP interpretation

Verify that the implementation and presentation preserve the conditional interpretation of FAP.

FAP must not be treated as:

- Probability that a candidate is a planet.
- Probability that the candidate period is correct.
- Proof that aliases are absent.
- Proof that stellar or instrumental systematics are absent.

Identify whether the actual implementation and documentation use appropriate terminology.

### Null-model limitations

Identify the conditions under which the selected null model may not adequately represent real astronomical data.

Document what can and cannot be concluded from the detection assessment.

Do not introduce a different null model or replace the approved methodology during PLAN.

## 8. Aliases, Harmonics, and Competing Candidate Validation

Inspect how the BLS search and detection assessment represent multiple candidate peaks.

Design validation cases involving:

- Known fundamental periods.
- Harmonics.
- Subharmonics.
- Competing periodic signals.
- Sampling-related aliases.
- Data-gap-related artifacts.
- Noise-generated peaks.
- Ambiguous candidate rankings.

Evaluate:

- Whether the expected candidate is recovered.
- Whether competing peaks are retained or represented.
- Whether the candidate-ranking behavior is misleading.
- Whether the application exposes relevant warnings.
- Whether the user can distinguish the strongest peak from a scientifically established period.

Do not assume that the strongest BLS peak is the true planetary period.

Identify limitations that cannot be resolved within the current BLS approach.

## 9. Kepler-10b Real-Data Benchmark

Evaluate whether the existing local Kepler-10b FITS dataset is suitable for optional real-data verification.

Previously inspected dataset:

`C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits`

Known characteristics:

- Kepler long cadence.
- 476 rows.
- Approximately 9.7 days of observation.
- TIME in BKJD/TDB.
- SAP_FLUX and PDCSAP_FLUX.
- Associated uncertainty fields.
- Four non-finite flux values.
- Thirty-seven nonzero quality flags.

Published reference values:

- Period: 0.837491225 days.
- Period uncertainty: 3.03 × 10⁻⁷ days.
- Epoch: 131.574858 BKJD.
- Epoch uncertainty: 0.000282 days.

Verify these details against the actual dataset and existing project documentation where possible.

Plan an optional benchmark that:

- Uses the existing imported dataset.
- Preserves the original FITS file.
- Records the selected flux measurement.
- Records the analysis configuration.
- Accounts for the short observation baseline.
- Accounts for missing observations and quality flags.
- Compares recovered results with the published reference values where scientifically appropriate.
- Documents differences in data preparation and assumptions.

Do not use this dataset as the sole uncertainty-calibration dataset.

Do not invent arbitrary tolerances for agreement with published values.

The standard automated test suite must not depend on this absolute path.

Do not modify, move, rename, or delete the original FITS file.

## 10. Scientific Integrity and Data Preservation

Design a verification strategy for the complete Stage 2.4 workflow.

Verify:

- Original imported measurements remain unchanged.
- SAP_FLUX and PDCSAP_FLUX remain distinct.
- Correct uncertainty fields are used.
- Quality flags remain accessible.
- Nonzero quality flags are not silently removed.
- Missing values are not replaced with zero.
- Units and time references are preserved.
- Analysis preparation is explicit and reproducible.
- Derived representations are distinguishable from original observations.
- Phase folding does not modify source measurements.
- Transit models are distinguishable from measured observations.
- Candidate results remain associated with their correct dataset and configuration.

Inspect existing tests for actual mutation checks.

Identify any gaps that need explicit integrity tests.

Consider whether before-and-after comparisons, immutable data structures, source-file checksums, or other existing mechanisms are appropriate.

Do not introduce new preservation infrastructure unless justified by the approved architecture.

## 11. Reproducibility and Traceability Validation

Evaluate whether the complete workflow retains sufficient information to understand and reproduce an analysis.

Inspect the actual implementation for:

- Dataset identity.
- Selected flux measurement.
- Associated uncertainty measurement.
- BLS search configuration.
- Data-preparation information.
- Uncertainty-estimation method and configuration.
- Detection-assessment method and configuration.
- Null-model assumptions.
- Random seeds.
- Simulation settings.
- Software and method information.
- Warnings and limitations.

Design tests to determine whether:

- Equivalent inputs and configurations produce appropriately reproducible outputs.
- Stochastic methods use random seeds as designed.
- Results can be distinguished when datasets or configurations differ.
- Displayed results correspond to the correct source dataset.
- Project or dataset switching does not misrepresent previously generated results.

Distinguish between reproducibility information exposed by Task 2.4.4 and complete operation-history persistence planned for Task 2.5.

Do not expand this task into permanent storage redesign or full operation-history implementation.

## 12. End-to-End Application Verification

Inspect the actual Task 2.4.4 integration.

Design an end-to-end verification plan covering:

1. Open a project.
2. Select an imported light-curve dataset.
3. Select PDCSAP_FLUX or SAP_FLUX.
4. Verify correct uncertainty association.
5. Configure a BLS search.
6. Execute the search.
7. Inspect candidate parameters.
8. Review uncertainty estimates.
9. Review detection-assessment results.
10. Inspect the periodogram.
11. Inspect the phase-folded light curve, if supported.
12. Switch candidates.
13. Switch datasets or projects.
14. Verify result associations and application state.

Evaluate:

- Correctness.
- Responsiveness.
- Error handling.
- Partial-result behavior.
- State management.
- Scientific presentation.
- Reproducibility.
- Original-data preservation.

Identify which parts can be automated and which require manual verification.

Use portable synthetic datasets and temporary project data for automated tests.

Do not assume a successful UI demonstration proves scientific validity.

## 13. Regression and Environment Verification

Plan regression testing across earlier functionality.

Review relevant tests for:

- Project creation.
- Project opening and closing.
- Project saving.
- Dataset import.
- Dataset persistence.
- Measurement tables.
- Original light-curve visualization.
- Project and dataset switching.

Identify appropriate full-suite and targeted test commands based on the actual repository.

Review environment and dependency requirements.

Do not reinstall or upgrade dependencies during PLAN.

Consider portability limitations, but do not expand the task into an unapproved cross-platform redesign.

## 14. Performance and Computational Feasibility

Evaluate the computational cost of the proposed scientific validation.

Inspect:

- BLS search complexity.
- Uncertainty simulation cost.
- Detection-assessment simulation cost.
- Expected calibration sample sizes.
- Memory use.
- Repeated-search cost.
- Application responsiveness.

Recommend a practical validation sequence that provides meaningful evidence without making the workflow unnecessarily expensive.

Distinguish between:

- Small automated regression tests.
- Medium-scale scientific validation.
- Larger calibration experiments.
- Optional real-data benchmark.
- Manual application verification.

If validation requires long-running experiments, recommend how they should be executed and documented.

Do not weaken scientific validation solely to reduce runtime.

Do not assume that a small smoke test establishes calibration.

## 15. Defect Classification and Corrective-Work Boundaries

Establish how identified issues should be classified.

Use these categories:

| Classification | Meaning |
|---|---|
| Critical | Scientific integrity, major correctness, or essential workflow failure |
| Major | Significant functionality or validation failure |
| Moderate | Limited defect or incomplete requirement |
| Minor | Small issue with limited impact |
| Documentation | Inaccurate or incomplete documentation |
| Deferred | Known limitation explicitly outside scope |

For each identified issue, specify:

- Description.
- Affected task or module.
- Reproduction conditions.
- Scientific or application impact.
- Existing evidence.
- Additional evidence needed.
- Recommended correction.
- Whether the correction belongs within approved Stage 2.4 scope.

Identify which issues can be corrected narrowly during the eventual Build phase.

Identify which issues require separate approval because they involve:

- Scientific methodology changes.
- Uncertainty-method replacement.
- New null-model assumptions.
- New detection thresholds.
- Storage redesign.
- Major architecture changes.
- Work outside Stage 2.4.

Do not implement corrections during PLAN.

## 16. Documentation Reconciliation Plan

Inspect the current Stage 2.4 documentation.

Identify documents that must be reconciled against actual implementation and validation evidence.

Consider:

- Stage 2 roadmap.
- Development log.
- BLS design documentation.
- BLS implementation documentation.
- Uncertainty and detection-assessment documentation.
- Architecture documentation.
- Data-flow documentation.
- Module responsibilities.
- Testing and validation documentation.
- Decision records.
- Project state and continuity records.

For each document, identify:

- Current accuracy.
- Required update.
- Evidence that should support the update.
- Whether it should remain unchanged.

The final documentation must distinguish:

- Implemented functionality.
- Tested functionality.
- Scientifically validated functionality.
- Known limitations.
- Deferred functionality.
- Unresolved issues.

Do not edit documentation during PLAN.

Do not modify Foundation documents.

## 17. Stage 2.4 Completion Criteria

Develop an explicit completion checklist tied to the original Stage 2.4 objective and approved task designs.

The checklist must cover:

- BLS search implementation.
- Input validation and preparation.
- Candidate extraction.
- Parameter recovery validation.
- Uncertainty estimation.
- Empirical uncertainty calibration.
- UQ-009 resolution.
- Noise-only null-model validation.
- Injected-signal validation.
- FAP interpretation, if applicable.
- Alias and competing-candidate handling.
- Application integration.
- Scientific visualization.
- Error and partial-result handling.
- Reproducibility.
- Scientific integrity.
- Regression testing.
- Documentation reconciliation.

For every criterion, define:

- Required evidence.
- Verification method.
- Acceptance condition.
- Current status.
- Consequence if not satisfied.

Do not invent universal numerical acceptance thresholds.

Use approved criteria where they exist.

Identify unresolved acceptance criteria that require explicit user approval.

Recommend one final status:

- Complete.
- Conditionally complete.
- Incomplete.
- Blocked.

Explain what evidence is required to justify each possible outcome.

## 18. Proposed Execution Sequence

Develop a practical sequence for the eventual Task 2.4.5 Build work.

Organize it into phases such as:

1. Repository and prerequisite verification.
2. Existing test-suite assessment.
3. BLS synthetic validation.
4. Uncertainty calibration and UQ-009 evaluation.
5. Noise-only and injected-signal validation.
6. Alias and competing-candidate validation.
7. Scientific integrity and reproducibility verification.
8. Application end-to-end verification.
9. Regression and performance testing.
10. Optional Kepler-10b benchmark.
11. Defect correction and retesting.
12. Documentation reconciliation.
13. Final Stage 2.4 completion assessment.

For each phase, specify:

- Objective.
- Relevant modules and tests.
- Required datasets or fixtures.
- Commands or procedures, where known.
- Expected evidence.
- Dependencies.
- Completion criteria.

Identify which phases can be executed independently and which depend on earlier results.

Separate short automated tests from longer scientific validation experiments.

Do not execute this sequence during PLAN except for read-only inspection and narrowly necessary test verification.

## 19. Required PLAN Report

Return a detailed, repository-specific report with the following sections.

### A. Repository and prerequisite status
- Actual status of Tasks 2.4.1–2.4.4.
- Relevant Stage 2.2 and 2.3 dependencies.
- Current working-tree status.
- Any missing prerequisite evidence.

### B. Stage 2.4 requirements traceability
- Original requirements.
- Implementation locations.
- Existing evidence.
- Remaining verification needs.
- Current status.

### C. Existing test coverage
- Test files and test names.
- Covered requirements.
- Coverage gaps.
- Redundant or weak tests.
- Portability concerns.

### D. BLS scientific validation plan
- Synthetic dataset design.
- Parameter-recovery tests.
- Noise and sampling conditions.
- Competing-signal conditions.
- Acceptance criteria.

### E. Uncertainty calibration plan
- Actual uncertainty methodology.
- Calibration design.
- Simulation conditions.
- Sample-size rationale.
- Bias and coverage evaluation.
- Reliability criteria.
- UQ-009 resolution requirements.

### F. Detection-assessment validation plan
- Actual null model.
- Noise-only controls.
- Injected-signal controls.
- FAP evaluation, if applicable.
- False-positive and false-negative evaluation.
- Statistical limitations.

### G. Alias and competing-candidate validation
- Required test conditions.
- Candidate comparison.
- Known limitations.
- Presentation concerns.

### H. Kepler-10b benchmark plan
- Dataset suitability.
- Reference comparisons.
- Limitations.
- Optional verification procedure.

### I. Scientific integrity verification
- Original-data preservation.
- Measurement and uncertainty associations.
- Quality flags.
- Missing values.
- Units and time references.
- Derived-data separation.

### J. Reproducibility and traceability
- Metadata availability.
- Configuration retention.
- Random seeds.
- Repeatability tests.
- Task 2.5 boundary.

### K. Application end-to-end verification
- Workflow tests.
- UI behavior.
- Visualization.
- Error handling.
- Lifecycle behavior.
- Automated versus manual verification.

### L. Regression, environment, and performance
- Existing functionality at risk.
- Test commands.
- Environment constraints.
- Computational cost.
- Validation execution strategy.

### M. Defect classification and correction plan
- Known issues.
- Severity.
- Evidence.
- Recommended corrections.
- Approval requirements.

### N. Documentation reconciliation
- Documents to update.
- Documents intentionally unchanged.
- Required evidence.
- Documentation gaps.

### O. Stage 2.4 completion checklist
- Every criterion.
- Evidence required.
- Acceptance condition.
- Current status.

### P. Proposed execution sequence
- Ordered phases.
- Dependencies.
- Tests and experiments.
- Completion criteria.

### Q. Unresolved decisions and assumptions
- Missing acceptance criteria.
- Unresolved UQ-009 requirements.
- Statistical assumptions.
- Any decisions requiring user approval.

### R. Overall readiness recommendation
State whether Task 2.4.5 is:

- Ready for Build.
- Conditionally ready for Build.
- Blocked.

Explain the recommendation and identify any prerequisite corrections or user decisions needed first.

Clearly distinguish:

- Verified repository facts.
- Existing test evidence.
- Scientific validation evidence.
- Recommendations.
- Assumptions.
- Unresolved decisions.
- Known limitations.

## 20. PLAN Restrictions

This is a planning task only.

Do not:

- Modify source code.
- Modify tests.
- Modify documentation.
- Add dependencies.
- Implement scientific validation scripts.
- Change BLS algorithms.
- Change uncertainty methods.
- Change detection-assessment methods.
- Change statistical thresholds.
- Modify research datasets.
- Modify the original Kepler-10b FITS file.
- Modify Foundation documents.
- Commit or push.
- Reset, clean, or alter Git history.
- Discard or overwrite user changes.

You may inspect repository files, review existing test results, execute read-only inspection commands, and run existing tests only when necessary to verify current state.

Do not begin the Task 2.4.5 implementation.

**Stop after delivering the complete PLAN report. Wait for explicit user review and approval before any Build work.**


# BUILD MODE PROMPT

# BUILD — Task 2.4.5: Testing, Scientific Validation, and Completion Verification

**Stage:** 2.4 — BLS Analysis and Uncertainty  
**Task:** 2.4.5 — Testing, Scientific Validation, and Completion Verification  
**Mode: BUILD — Implement the approved verification plan, perform validation, and assess Stage 2.4 completion.**

## 1. Objective

Execute the approved Task 2.4.5 PLAN and determine whether the complete Stage 2.4 workflow is implemented, tested, scientifically validated, reproducible, documented, and ready to be marked complete.

Stage 2.4 includes:

- Task 2.4.1 — BLS Analysis Design and Implementation Planning.
- Task 2.4.2 — BLS Transit Search Implementation.
- Task 2.4.3 — Transit Parameter Uncertainty and Detection Assessment.
- Task 2.4.4 — Application Integration and Analysis Results.
- Task 2.4.5 — Testing, Scientific Validation, and Completion Verification.

This task is not merely a test-suite execution.

It must establish whether the scientific methods and application behavior meet their approved requirements, with particular attention to:

1. BLS parameter recovery.
2. Empirical uncertainty calibration and UQ-009.
3. Noise-only null-model validation.
4. Injected-signal detection behavior.
5. Aliases, harmonics, and competing candidates.
6. Scientific data integrity.
7. Reproducibility.
8. End-to-end application behavior.
9. Documentation accuracy.

Follow the approved PLAN report. Do not silently change its scientific methodology, acceptance criteria, or scope.

## 2. Mandatory Pre-Build Verification

Before modifying anything:

1. Read `AGENTS.md` and follow its requirements.
2. Read the approved Task 2.4.5 PLAN report.
3. Inspect the current roadmap and development log.
4. Inspect relevant architecture, data-flow, data-model, module-responsibility, testing, decision, and project-state documentation.
5. Inspect the actual implementations of Tasks 2.4.1–2.4.4.
6. Inspect relevant Stage 2.2 and 2.3 functionality.
7. Check the current Git branch and working-tree status.
8. Identify existing user modifications and uncommitted work.
9. Verify the current test and dependency environment.

Compare the actual repository against the approved PLAN.

**Stop and report before implementation if:**

- The repository has materially changed since PLAN.
- A required prerequisite is missing or incomplete.
- The approved PLAN conflicts with the actual implementation.
- A required scientific decision remains unresolved.
- The planned validation cannot be performed without changing the approved methodology.
- A proposed correction would exceed the approved scope.

Do not overwrite or discard user work.

Do not assume previous task reports accurately represent the current code.

## 3. Execute the Approved Verification Plan

Follow the phases and dependencies established in the approved PLAN report.

Maintain a clear distinction between:

- Automated software testing.
- Scientific validation.
- Empirical calibration.
- Manual application verification.
- Optional real-data benchmarking.

For each phase, record:

- Objective.
- Files and modules inspected or changed.
- Test commands or experiment procedures.
- Inputs and configurations.
- Actual results.
- Evidence collected.
- Acceptance criteria.
- Pass, fail, inconclusive, or not performed status.
- Limitations and follow-up work.

Do not claim a phase passed without its required evidence.

## 4. BLS Parameter-Recovery Validation

Execute the approved synthetic-data validation plan.

Use controlled datasets with known:

- Period.
- Transit epoch.
- Transit duration.
- Transit depth.
- Noise characteristics.
- Observation cadence.
- Observation baseline.

Include the conditions required by the approved PLAN, such as:

- Different noise levels.
- Different transit depths and durations.
- Different sampling patterns.
- Missing observations.
- Irregular sampling.
- Data gaps.
- Competing periodic signals.
- Short observation baselines.

Evaluate the actual BLS outputs against the known input parameters.

Assess:

- Period recovery.
- Epoch recovery.
- Duration recovery.
- Depth recovery.
- Candidate ranking.
- Sensitivity to noise and sampling.
- Behavior when the input is poorly constrained.
- Behavior when multiple candidates compete.

Use acceptance criteria established in the approved design or PLAN.

Do not invent arbitrary tolerances to make results pass.

If an acceptance criterion is missing, report the gap and request approval before using a new criterion.

Do not interpret a successful synthetic test as proof that all real astronomical datasets will behave similarly.

## 5. Empirical Uncertainty Calibration — UQ-009

Treat UQ-009 as a required scientific-validation objective.

Inspect and validate the uncertainty methods actually implemented in Task 2.4.3.

Do not assume a method was implemented merely because it appeared in the design.

Execute the approved repeated-simulation calibration plan.

### Calibration procedure

For each required synthetic condition:

1. Generate or obtain a dataset with known input parameters.
2. Run the actual BLS workflow.
3. Execute the implemented uncertainty method.
4. Record the true parameter values.
5. Record recovered parameter estimates.
6. Record estimated uncertainties or intervals.
7. Compare estimates against the known values.
8. Repeat according to the approved simulation design.
9. Aggregate the calibration results.
10. Compare observed behavior against the approved acceptance criteria.

Evaluate the parameters supported by the implementation:

- Period.
- Epoch.
- Duration.
- Depth.

Assess:

- Estimation bias.
- Actual estimation error.
- Uncertainty magnitude.
- Empirical interval coverage, where intervals are produced.
- Stability across repeated simulations.
- Failure and unavailable-estimate frequency.
- Sensitivity to noise.
- Sensitivity to cadence and sampling.
- Sensitivity to observation baseline.
- Sensitivity to transit depth and duration.

For interval-based uncertainty, compare nominal coverage with observed coverage.

For example, a nominal 68% interval should be evaluated against the fraction of repeated known input values actually contained within the intervals.

For methods that produce standard errors or another uncertainty representation, use the calibration assessment approved in the PLAN.

### Calibration reporting

Report results separately for each parameter and relevant simulation condition.

Include:

- Number of simulations.
- Input conditions.
- Random seeds or seed policy.
- Recovered estimates.
- Bias.
- Empirical coverage, where applicable.
- Uncertainty behavior.
- Failed or inconclusive simulations.
- Computational limitations.
- Conditions where the method is unreliable.

Do not report a single aggregate calibration result if it conceals substantial differences between parameters or operating conditions.

### UQ-009 outcome

Classify UQ-009 as:

- Resolved.
- Partially resolved.
- Unresolved.
- Blocked.

Justify the classification with actual evidence.

Do not claim uncertainty estimates are reliable merely because they produce numerical outputs.

If calibration fails, identify:

- Which estimates are affected.
- The conditions under which they fail.
- The scientific consequences.
- Whether a narrow correction is within the approved plan.
- What additional work or user decision is required.

Do not replace the uncertainty methodology or change scientific assumptions without approval.

## 6. Detection Assessment and Noise-Only Validation

Execute the approved Task 2.4.3 detection-assessment validation plan.

Inspect the actual implementation and verify that experiments reflect its real null-model assumptions.

Evaluate:

- Null-model definition.
- Noise distribution.
- Measurement uncertainties.
- Observation sampling.
- Time-correlated noise treatment, if supported.
- Search period range.
- Candidate-selection procedure.
- Simulation procedure.
- Simulation count.
- Random seed handling.
- FAP calculation, if implemented.

### Noise-only controls

Run the approved noise-only experiments.

Preserve the relevant sampling and uncertainty characteristics.

Evaluate how frequently the complete search procedure reports apparently significant candidates when no transit signal is injected.

If the real search evaluates multiple periods or durations, ensure the validation follows the complete approved search and candidate-selection procedure.

Do not substitute a test at one preselected period for validation of a full period search unless the approved methodology explicitly calls for it.

### Injected-signal controls

Run the approved injected-signal experiments.

Evaluate:

- Detection rate.
- False-positive behavior.
- False-negative behavior.
- Sensitivity to signal strength.
- Sensitivity to noise.
- Sensitivity to observation cadence.
- Sensitivity to baseline.
- Candidate-ranking behavior.

Record the conditions under which signals are detected, missed, or confused with competing candidates.

### FAP interpretation

Verify that code, tests, results, and documentation preserve the correct conditional interpretation of FAP.

FAP is conditional on the specified noise-only null model.

It is not:

- Probability that a candidate is a planet.
- Probability that the candidate period is correct.
- Proof that aliases are absent.
- Proof that stellar or instrumental systematics are absent.

Correct misleading terminology only when the correction is within the approved plan and does not change the scientific method.

If the null model is inadequate or the evidence is insufficient, report the limitation instead of presenting unsupported significance claims.

## 7. Aliases, Harmonics, and Competing Candidates

Execute the approved tests involving:

- Fundamental periods.
- Harmonics.
- Subharmonics.
- Competing transit signals.
- Sampling-related aliases.
- Data-gap-related artifacts.
- Noise-generated peaks.
- Ambiguous candidate rankings.

Verify that:

- Expected candidate behavior is understood.
- Competing peaks are represented appropriately.
- Candidate ranking is not misleading.
- Relevant warnings and limitations are exposed.
- The application does not imply that the strongest BLS peak is automatically the true planetary period.

Document limitations that cannot be resolved within the approved BLS approach.

Do not expand this task into a new multi-planet detection or transit-fitting methodology.

## 8. Optional Kepler-10b Real-Data Benchmark

If approved in the PLAN and the local file is available, perform the optional benchmark using:

`C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits`

Previously recorded dataset characteristics:

- Kepler long cadence.
- 476 observations.
- Approximately 9.7 days of observation.
- TIME in BKJD/TDB.
- SAP_FLUX and PDCSAP_FLUX.
- Associated uncertainty fields.
- Four non-finite flux values.
- Thirty-seven nonzero quality flags.

Published reference values:

- Period: 0.837491225 days.
- Period uncertainty: 3.03 × 10⁻⁷ days.
- Epoch: 131.574858 BKJD.
- Epoch uncertainty: 0.000282 days.

Verify these values and dataset characteristics against available evidence.

Record:

- Dataset identity.
- Selected flux measurement.
- Associated uncertainty field.
- Analysis configuration.
- Data-preparation choices.
- Quality-flag treatment.
- Recovered candidates.
- Comparison with published values.
- Limitations caused by the short baseline and sampling.

Do not invent arbitrary tolerances for agreement.

Do not use this single dataset as the sole uncertainty-calibration evidence.

The benchmark is optional and must not become a dependency of the standard test suite.

**Never modify, move, rename, or delete the original FITS file.**

If the file is unavailable, report the benchmark as not performed. Do not ask the user to redownload or relocate it.

## 9. Scientific Integrity Verification

Verify that the complete Stage 2.4 workflow preserves the scientific integrity requirements established in earlier stages.

Check that:

- Original imported measurements remain unchanged.
- SAP_FLUX and PDCSAP_FLUX remain separate.
- Correct uncertainty fields are used.
- Quality flags remain accessible.
- Nonzero quality flags are not silently removed.
- Missing values are not replaced with zero.
- Units and time references are preserved.
- Analysis preparation is explicit and reproducible.
- Derived representations remain distinguishable from original measurements.
- Phase folding does not modify source measurements.
- Transit models are distinguishable from observed measurements.
- Candidate results remain associated with the correct dataset and configuration.

Execute existing integrity tests and add narrowly scoped tests where the approved PLAN identifies gaps.

Do not introduce new preservation infrastructure or modify earlier-stage architecture unless approved.

## 10. Reproducibility and Traceability Verification

Verify that results retain the information necessary to understand and reproduce the analysis.

Inspect and test the actual handling of:

- Dataset identity.
- Selected flux measurement.
- Associated uncertainty field.
- BLS search configuration.
- Data-preparation information.
- Uncertainty method and configuration.
- Detection-assessment method and configuration.
- Null-model assumptions.
- Random seeds.
- Simulation settings.
- Software and method information.
- Warnings and limitations.

Test repeatability and result association according to the approved PLAN.

Verify that changing datasets or configurations cannot cause old results to be presented as belonging to a different analysis.

Respect the boundary between Task 2.4 and Task 2.5.

Do not implement the complete operation-history system or redesign persistence.

## 11. End-to-End Application Verification

Execute the approved application verification plan.

Verify the workflow:

1. Open a project.
2. Select an imported light-curve dataset.
3. Select PDCSAP_FLUX or SAP_FLUX.
4. Verify the associated uncertainty measurement.
5. Configure a BLS search.
6. Execute the search.
7. Inspect candidate parameters.
8. Review uncertainty results.
9. Review detection-assessment results.
10. Inspect the periodogram.
11. Inspect the phase-folded light curve, if implemented.
12. Switch candidates.
13. Switch datasets or projects.
14. Verify all displayed results remain associated with the correct analysis.

Test:

- Empty states.
- Invalid inputs.
- Search failures.
- Uncertainty failures.
- Detection-assessment failures.
- Partial results.
- Project and dataset switching.
- Stale-result prevention.
- Responsiveness.
- Scientific presentation.

A failure in uncertainty or detection assessment must not silently misrepresent or discard an otherwise valid BLS result if the approved design supports partial results.

Clearly distinguish manual verification from automated tests.

Do not claim manual verification was completed unless the application was actually launched and the relevant behavior was inspected.

## 12. Regression and Full Test Suite

Run the targeted tests identified in the approved PLAN.

Run the complete project test suite.

Include relevant regression coverage for:

- Project lifecycle.
- Dataset import and persistence.
- Measurement tables.
- Light-curve visualization.
- Dataset and project switching.
- BLS search.
- Uncertainty estimation.
- Detection assessment.
- Application integration.

Record exact commands, environment details, test counts, failures, skipped tests, and warnings.

Do not report only that "tests passed."

If a test fails:

1. Determine whether the failure is new or pre-existing.
2. Identify the affected functionality.
3. Assess scientific and application impact.
4. Determine whether a correction is within approved scope.
5. Preserve the failure evidence.
6. Retest after any approved correction.

Do not weaken, remove, skip, or rewrite tests simply to obtain a passing suite.

Do not make standard tests dependent on the user's absolute Kepler-10b FITS path.

Use portable synthetic fixtures and temporary directories.

## 13. Performance and Computational Feasibility

Execute the performance checks approved in the PLAN.

Evaluate relevant costs for:

- BLS search.
- Uncertainty simulations.
- Detection-assessment simulations.
- Calibration experiments.
- Repeated full-search procedures.
- Memory usage.
- Application responsiveness.

Record actual runtimes and relevant environment information.

If an experiment is too expensive to complete:

- Report what was executed.
- Report what remains.
- Explain the computational limitation.
- Identify whether the missing evidence affects completion.
- Recommend a practical next step.

Do not silently reduce simulation counts or weaken scientific validation.

Any change to an approved simulation design or sample size requires justification and approval where it changes the intended evidence or acceptance criteria.

## 14. Defect Correction Boundaries

Correct defects only when all of the following apply:

- The defect is demonstrated by inspection or testing.
- The correction is necessary for the approved Task 2.4.5 verification objective.
- The correction is within the approved PLAN.
- The correction does not alter an unapproved scientific assumption or methodology.
- The correction does not expand architecture or project scope.

Examples of potentially in-scope corrections include:

- A narrow defect in a Stage 2.4 test.
- A missing test for an already-approved requirement.
- Incorrect result association in the Stage 2.4 UI.
- Misleading presentation of an existing result.
- A documentation statement contradicted by verified implementation.

Stop and request approval before:

- Replacing a scientific method.
- Changing the null model.
- Changing detection thresholds.
- Changing uncertainty methodology.
- Introducing new scientific assumptions.
- Redesigning persistence.
- Changing earlier-stage architecture substantially.
- Adding unapproved dependencies.
- Expanding beyond Stage 2.4.

Do not conceal defects by changing acceptance criteria.

Do not make unrelated refactoring changes.

## 15. Documentation Maintenance

Follow the documentation-maintenance requirements in `AGENTS.md`.

Update documentation during implementation where functionality, testing, validation, architecture, interfaces, or project status changes.

Reconcile relevant documents, including:

- Stage 2 roadmap.
- Development log.
- BLS design and implementation documentation.
- Uncertainty and detection-assessment documentation.
- Architecture documentation.
- Data-flow documentation.
- Module responsibilities.
- Testing and validation documentation.
- Relevant decision records.
- Project state and continuity records.

Document actual evidence, not intended behavior.

Clearly distinguish:

- Implemented.
- Automated-tested.
- Scientifically validated.
- Manually verified.
- Optional benchmark completed or not performed.
- Known limitations.
- Deferred functionality.
- Unresolved issues.

Record UQ-009's actual outcome.

Do not mark a requirement complete merely because the relevant documentation was updated.

Do not modify Foundation documents.

## 16. Stage 2.4 Completion Assessment

After the approved validation work and any in-scope corrections, evaluate every Stage 2.4 requirement.

At minimum, assess:

1. BLS search implementation.
2. Input validation and preparation.
3. Candidate extraction.
4. Parameter-recovery validation.
5. Uncertainty estimation.
6. Empirical uncertainty calibration.
7. UQ-009 resolution.
8. Noise-only null-model validation.
9. Injected-signal validation.
10. FAP interpretation, if applicable.
11. Alias and competing-candidate handling.
12. Application integration.
13. Scientific visualization.
14. Error and partial-result handling.
15. Reproducibility.
16. Scientific integrity.
17. Automated testing.
18. Documentation reconciliation.

For each requirement, assign one status:

- Complete and verified.
- Implemented but insufficiently verified.
- Partially complete.
- Incomplete.
- Deferred with documented justification.
- Blocked.

Provide the evidence supporting each status.

Then recommend one overall Stage 2.4 status:

- **Complete** — All required functionality and evidence meet approved criteria.
- **Conditionally complete** — Core requirements are met, but clearly documented non-blocking limitations or deferred items remain under approved criteria.
- **Incomplete** — One or more required objectives have not been satisfied.
- **Blocked** — A prerequisite, unresolved decision, or critical defect prevents reliable completion.

Do not mark Stage 2.4 complete solely because the test suite passes.

Do not mark UQ-009 resolved without empirical calibration evidence.

Do not classify an optional Kepler benchmark as a blocker unless the approved PLAN explicitly made it mandatory.

If completion is not justified, identify the specific work and evidence required before completion can be reconsidered.

## 17. Final Documentation and Change Review

Before finishing:

1. Review every changed source file.
2. Review every changed test.
3. Review every changed document.
4. Inspect the complete Git diff.
5. Check for accidental data or generated-file changes.
6. Confirm that no user modifications were overwritten.
7. Confirm that no original research data was modified.
8. Confirm that no Foundation documents were changed.
9. Confirm that the full test suite was executed after the final code correction.
10. Confirm that documentation matches the final implementation and evidence.

Report files that were:

- Changed.
- Added.
- Intentionally left unchanged.
- Identified as needing later work.

Explain why relevant documents were not changed when no update was necessary.

## 18. Required Final Report

Provide a detailed completion report with the following sections.

### A. Overall Stage 2.4 assessment
- Recommended status.
- Summary and justification.
- Whether Stage 2.4 is ready to close.

### B. Task-by-task verification
- Tasks 2.4.1–2.4.5.
- Actual implementation status.
- Verification evidence.
- Remaining limitations.

### C. Automated testing
- Exact commands.
- Environment.
- Test counts.
- Passes, failures, skips, and warnings.
- Regression results.

### D. BLS scientific validation
- Synthetic datasets.
- Parameter-recovery results.
- Noise and sampling conditions.
- Competing candidates.
- Acceptance criteria and limitations.

### E. Uncertainty calibration and UQ-009
- Actual method evaluated.
- Simulation conditions and sample sizes.
- Period, epoch, duration, and depth results.
- Bias and coverage.
- Stability and failure conditions.
- UQ-009 classification and evidence.

### F. Detection-assessment validation
- Null-model assumptions.
- Noise-only results.
- Injected-signal results.
- False-positive and false-negative behavior.
- FAP interpretation.
- Limitations.

### G. Aliases and competing candidates
- Tests performed.
- Results.
- Known limitations.

### H. Kepler-10b benchmark
- Performed or not performed.
- Dataset and configuration.
- Results and comparison.
- Limitations.
- Confirmation that the original file was not modified.

### I. Scientific integrity
- Original-data preservation.
- Measurement and uncertainty associations.
- Quality flags.
- Missing values.
- Units and time references.
- Derived-data separation.

### J. Reproducibility and traceability
- Metadata and configuration.
- Random seed handling.
- Repeatability.
- Dataset/result association.
- Task 2.5 boundary.

### K. Application verification
- End-to-end workflow.
- UI behavior.
- Visualization.
- Error and partial-result handling.
- Lifecycle behavior.
- Manual versus automated verification.

### L. Performance and environment
- Runtime observations.
- Computational limitations.
- Environment details.
- Remaining performance concerns.

### M. Defects and corrective work
- Defects found.
- Severity.
- Corrections made.
- Tests added or changed.
- Outstanding work.
- Items requiring separate approval.

### N. Documentation reconciliation
- Files changed.
- Files intentionally unchanged.
- Evidence reflected in documentation.
- Remaining documentation gaps.

### O. Final completion checklist and handoff
- Each Stage 2.4 criterion and its status.
- UQ-009 outcome.
- Outstanding limitations.
- Required next steps.
- Whether Stage 2.4 can be marked complete.
- Readiness for subsequent Stage 2.5 work.

## 19. Final Restrictions

Do not:

- Commit or push changes.
- Reset, clean, or alter Git history.
- Discard or overwrite user changes.
- Modify, move, rename, or delete the original Kepler-10b FITS file.
- Modify Foundation documents.
- Redesign the storage architecture.
- Implement the Stage 2.5 operation-history system.
- Add unrelated functionality.
- Perform unrelated refactoring.
- Introduce unapproved dependencies.
- Change approved scientific methods or assumptions without approval.
- Claim scientific validation without supporting evidence.
- Claim manual verification without actually performing it.

Preserve all existing user work.

**Stop after delivering the complete final report. Do not commit, push, or begin Stage 2.5. Wait for the user's review and explicit approval before proceeding.**