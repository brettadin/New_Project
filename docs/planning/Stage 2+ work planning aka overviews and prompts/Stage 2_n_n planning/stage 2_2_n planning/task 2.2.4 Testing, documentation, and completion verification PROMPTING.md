# PLAN MODE PROMPT

# Subtask 2.2.4 — Testing, Documentation, and Completion Verification
## PLAN Prompt

**Mode: PLAN ONLY. Inspect, test where appropriate, analyze, and report. Do not modify files or implement anything.**

You are working on the New_Project astronomy research application.

Repository:
`C:\Code\New_Project`

GitHub:
`https://github.com/brettadin/New_Project`

The application is a local-first astronomy research application built with Python 3.13 and PySide6.

Your task is to investigate and prepare a final verification plan for **Stage 2, Subtask 2.2.4 — Testing, Documentation, and Completion Verification**.

This is the final verification subtask for Stage 2.2 — Light-Curve Import.

The goal is to establish whether the combined work from Subtasks 2.2.1, 2.2.2, and 2.2.3 satisfies its requirements, preserves scientific integrity, has sufficient automated test coverage, and is accurately documented.

Do not assume the earlier subtasks are complete merely because previous reports said they were. Inspect the current repository and verify the actual implementation.

Your responsibility is to assess the current state, identify gaps, and propose a focused verification and documentation plan.

---

## 1. Mandatory governance and context review

Before beginning, read and follow:

- `AGENTS.md`
- Applicable Foundation requirements referenced by `AGENTS.md`
- Current development roadmap
- Current development log
- Relevant architecture documentation
- Data-model documentation
- Data-flow documentation
- Module responsibility documentation
- Relevant decision records
- Testing and validation documentation
- Project state and continuity documentation

Pay particular attention to:

- Scientific integrity and data preservation.
- Data provenance and traceability.
- Reproducibility.
- Project lifecycle and persistence.
- Local storage and data integrity.
- Testing and QA requirements.
- Documentation maintenance.
- Completion criteria and status definitions.
- Approval requirements for architectural changes.

Foundation is authoritative and read-only. Do not modify Foundation requirements or documents.

Follow the actual repository documentation structure. Do not assume every document named in previous discussions exists.

## 2. Inspect the current repository and working state

Before assessing completion:

1. Inspect the current Git branch and working-tree status.
2. Identify committed and uncommitted changes.
3. Inspect the current repository structure.
4. Identify all relevant implementation and test files.
5. Review the latest development log and roadmap.
6. Identify any changes made since the earlier subtask completion reports.

Do not overwrite, discard, or modify existing user work.

Distinguish between:
- Current verified repository state.
- Historical completion reports.
- Uncommitted work.
- Assumptions or information that cannot currently be verified.

Do not assume the GitHub remote reflects the current local working tree.

## 3. Verify Subtask 2.2.1 — FITS Inspection and Data-Model Design

Inspect the actual data-model implementation and its tests.

Verify:

- The approved light-curve data model exists.
- Its classes, fields, types, and relationships.
- Source-file and provenance representation.
- Measurement representation.
- Uncertainty representation and associations.
- Time values and time-reference metadata.
- Measurement units.
- Quality flags and cadence identifiers.
- Missing and non-finite value representation.
- Validation warnings and errors.
- Original versus derived data distinctions.
- Schema or model versioning, where implemented.

Compare the implementation against the approved 2.2.1 Plan and Build reports, if available.

Identify:
- Requirements satisfied.
- Requirements partially satisfied.
- Requirements not implemented.
- Differences from the approved design.
- Missing or inadequate tests.
- Documentation inconsistencies.

Do not redesign the data model as part of this verification task.

## 4. Verify Subtask 2.2.2 — FITS Import and Validation

Inspect the actual FITS importer, validation logic, and tests.

Verify:

### FITS handling
- FITS files are opened using the approved Astropy-based approach.
- HDUs are identified appropriately.
- Relevant light-curve tables are identified by structure rather than an unjustified fixed index.
- Measurement columns are extracted according to the approved design.
- Different flux types remain distinct.
- Uncertainties remain associated with the correct measurements.
- Quality flags and cadence identifiers are preserved.

### Metadata extraction
Verify handling of:
- Source and target information.
- Mission and instrument information.
- Observation cadence.
- Measurement units.
- Time units.
- Time reference or epoch.
- Time scale.
- Original column information.
- Other relevant FITS headers.

### Validation
Verify how the importer handles:
- Missing required columns.
- Missing optional columns.
- Missing metadata.
- Non-numeric values.
- Non-finite values.
- Missing uncertainties.
- Invalid timestamps.
- Unexpected array shapes.
- Nonzero quality flags.
- Unsupported or ambiguous metadata.

Determine whether warnings and errors are distinguished appropriately.

Compare implementation behavior against the approved 2.2.2 Plan and Build reports, if available.

Identify any scientific-integrity risks, implementation gaps, or inadequate tests.

Do not reimplement the importer during this task.

## 5. Verify Subtask 2.2.3 — Project Integration and Provisional Persistence

Inspect the actual project integration and persistence implementation.

Verify:

### Project association
- Imported datasets can be associated with a research project.
- Dataset identity is maintained.
- Source information remains associated with the dataset.
- Multiple datasets are handled according to the approved design.
- Project metadata and scientific dataset content remain appropriately separated.

### Persistence
- Dataset content can be saved.
- Dataset content can be recovered after project reopening.
- Measurements remain intact.
- Uncertainties remain correctly associated.
- Units and time references remain intact.
- Quality flags and cadence identifiers remain intact.
- Missing and non-finite values are handled according to the approved data model.
- Source and provenance information survive persistence.

### Lifecycle integration
Verify behavior involving:
- Project creation.
- Project opening.
- Project saving.
- Project closing.
- Project switching.
- Dirty-state tracking.
- Save/Discard/Cancel behavior.
- Failed dataset persistence.
- Missing original source files.
- Missing or corrupted persisted content.
- Recovery when one dataset cannot be loaded.

### Provisional storage boundary
Verify that:
- The implementation follows the approved provisional persistence design.
- D6 remains respected.
- Permanent storage architecture has not been represented as finalized.
- Storage limitations are documented.
- No unnecessary database, ORM, or storage dependency has been introduced without approval.

Compare the implementation against the approved 2.2.3 Plan and Build reports, if available.

Do not redesign the persistence architecture during this task.

## 6. Evaluate automated test coverage

Inspect the existing test suite before proposing additional tests.

Identify:
- Existing test modules.
- Test counts and organization.
- Fixtures and test-data generation.
- Tests using temporary directories.
- Tests depending on machine-specific paths.
- Tests requiring the real Kepler-10b dataset.
- Missing failure-path coverage.
- Potentially misleading or incomplete tests.
- Existing regressions or flaky behavior.

Determine whether the current tests adequately cover the combined 2.2.1–2.2.3 workflow.

At minimum, assess coverage of the following areas:

| Area | Verification target |
|---|---|
| Data model | Correct construction and preservation |
| FITS structure | HDU and table identification |
| Importing | Correct measurement extraction |
| Metadata | Units, time references, source information |
| Measurements | Flux values and uncertainty associations |
| Quality | Quality flags and cadence identifiers |
| Missing data | Missing and non-finite value handling |
| Validation | Correct warnings and errors |
| Project integration | Dataset association and identity |
| Persistence | Save and reopen behavior |
| Recovery | Missing or corrupted content |
| Regression | Existing project lifecycle behavior |

Do not assume a test passes simply because it exists. Inspect its assertions and whether it actually exercises the intended code path.

Do not weaken or remove tests to make the suite pass.

### Test execution

Determine which tests can safely be executed during Plan mode.

You may run existing read-only test commands where useful, provided they do not modify user data or repository files beyond ordinary test-generated temporary artifacts.

If tests are executed, report:
- Exact commands.
- Exit codes.
- Actual pass, fail, and skipped counts.
- Relevant warnings or errors.

Do not claim that a test was executed if it was only inspected.

If a test causes a real application dialog to appear, identify the behavior and distinguish it from an actual test failure.

## 7. Plan real-dataset end-to-end verification

The user's existing Kepler-10b FITS file is located at:

`C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits`

Previously established information about this file includes:
- FITS format.
- Kepler long-cadence observations.
- Approximately 476 rows.
- Approximately 9.7 days of observations.
- TIME represented in BKJD with TDB reference.
- SAP_FLUX and PDCSAP_FLUX measurements.
- Corresponding uncertainty fields.
- SAP_QUALITY and CADENCENO fields.
- Missing or non-finite flux values and nonzero quality flags.

Treat these details as historical information to verify, not guaranteed current findings.

Determine whether the file is available in the current environment.

If available, inspect it read-only and determine how it could be used for optional end-to-end verification.

Propose a controlled workflow:

1. Open or create a project.
2. Import the Kepler-10b FITS file.
3. Inspect imported measurements and metadata.
4. Save the project.
5. Close the project.
6. Reopen the project.
7. Recover the dataset.
8. Compare the recovered representation against the pre-save imported representation.

Define appropriate comparison methods for:
- Measurement values.
- Uncertainties.
- Units.
- Time values and references.
- Quality flags.
- Cadence identifiers.
- Missing and non-finite values.
- Source and provenance metadata.

The original FITS file must never be modified.

Routine automated tests must not depend on this absolute path. Real-data verification should complement controlled automated tests, not replace them.

Do not execute destructive or modifying operations on the original dataset.

## 8. Scientific integrity assessment

Conduct a focused review of the entire import and persistence workflow.

Determine whether the implementation preserves:

1. Original source information.
2. Imported measurement values.
3. Uncertainty values and associations.
4. Measurement units.
5. Time values and conventions.
6. Quality flags.
7. Cadence identifiers.
8. Missing and non-finite values.
9. Original column information.
10. Validation warnings and provenance information.

Check for evidence of unintended:
- Normalization.
- Detrending.
- Filtering.
- Data removal.
- Unit conversion.
- Time conversion.
- Metadata substitution.
- Source-file modification.

Verify that the application distinguishes:

- Original source FITS data.
- Imported dataset representation.
- Future derived or transformed scientific data.

Identify any behavior that could change the scientific interpretation of the dataset.

Do not silently classify an unresolved scientific concern as acceptable.

## 9. Project lifecycle and regression assessment

Assess whether the new scientific-data workflow has affected previously completed project functionality.

Review the existing project lifecycle tests and implementation.

Verify or propose verification of:
- Project creation and discovery.
- Project opening.
- Project saving.
- Project closing.
- Project switching.
- Dirty-state handling.
- Save/Discard/Cancel behavior.
- Preservation of the active project when switching fails.
- Existing project metadata persistence.
- Existing project status behavior.

Identify any regressions or areas where scientific dataset changes may not be integrated correctly with project lifecycle operations.

Do not refactor unrelated project functionality.

## 10. Documentation audit

Inspect all relevant documentation and compare it with the actual implementation and test coverage.

Consider:

- Development roadmap.
- Development log.
- Architecture documentation.
- Data-model documentation.
- Data-flow documentation.
- Module responsibilities.
- Persistence and storage decisions.
- Testing and validation documentation.
- Project state and continuity records.

Determine whether the documents accurately describe:

- The implemented data model.
- FITS import and validation behavior.
- Project-to-dataset integration.
- Provisional persistence.
- Scientific-data preservation.
- Error handling and recovery.
- Actual automated test coverage.
- Real-dataset verification status.
- Known limitations.
- Deferred architecture decisions.

Identify:
- Outdated statements.
- Missing documentation.
- Contradictions between documents.
- Claims unsupported by implementation or tests.
- Roadmap statuses that do not reflect actual completion.

Follow `AGENTS.md` documentation-maintenance requirements.

Do not modify documentation during Plan mode.

Do not modify Foundation.

## 11. Identify defects and classify required work

For every identified issue, classify it as one of:

- **Blocking defect:** Prevents Stage 2.2 from meeting its required objective.
- **Non-blocking defect:** Does not prevent the initial workflow but should be documented or scheduled.
- **Test gap:** Behavior may work, but sufficient verification is missing.
- **Documentation gap:** Implementation is present, but documentation is inaccurate or incomplete.
- **Architectural concern:** Design or implementation may conflict with approved architecture or Foundation requirements.
- **Deferred decision:** Intentionally unresolved and not a blocker for the current stage.

For each issue, provide:
- Description.
- Evidence and affected files.
- Requirement or decision affected.
- Why it matters.
- Recommended next action.
- Whether explicit approval is required.

Do not automatically propose broad refactoring as the solution.

If a defect requires changes to 2.2.1, 2.2.2, or 2.2.3 implementation, identify the smallest appropriate correction and explain whether it should be handled before or separately from completion verification.

## 12. Completion criteria assessment

Assess whether the combined Stage 2.2 work meets its intended objective:

> Import a real astronomical light-curve dataset into a project, preserve its original scientific information and provenance, support project-level persistence and recovery, and provide a reliable foundation for subsequent data presentation and analysis.

Evaluate the following completion criteria:

- The approved light-curve data model exists and is tested.
- The FITS importer can import and validate the initial supported dataset.
- Scientific measurements and metadata are preserved.
- Original source files remain unchanged.
- Imported datasets can be associated with research projects.
- Dataset content survives project save and reopen.
- Project lifecycle behavior remains correct.
- Failure handling is sufficiently tested.
- Automated tests are portable and do not depend on the user's permanent dataset path.
- Documentation reflects actual implementation and test results.
- Provisional storage limitations are documented.
- No unresolved blocking defects remain.

Do not mark Stage 2.2 complete solely because the test suite passes.

A complete assessment must consider implementation, scientific integrity, tests, documentation, and outstanding issues.

## 13. Required Plan report

Produce a structured report with the following sections.

### A. Repository and working-state findings
- Current branch and working-tree status.
- Relevant implementation and test files.
- Changes since earlier completion reports.
- Any uncommitted work or environmental limitations.

### B. Subtask 2.2.1 verification
- Actual implementation.
- Data-model requirements satisfied.
- Test coverage.
- Documentation consistency.
- Identified gaps.

### C. Subtask 2.2.2 verification
- Actual importer and validation behavior.
- FITS handling.
- Metadata and measurement preservation.
- Test coverage.
- Documentation consistency.
- Identified gaps.

### D. Subtask 2.2.3 verification
- Project integration.
- Dataset association.
- Persistence and recovery.
- Lifecycle integration.
- Error handling.
- Test coverage.
- Documentation consistency.
- Identified gaps.

### E. Automated testing assessment
- Existing test modules.
- Test coverage analysis.
- Commands executed and results.
- Proposed additional tests.
- Portability and fixture assessment.
- Regression risks.

### F. Real-dataset verification plan
- Kepler-10b file availability.
- Verified file characteristics, if inspected.
- Proposed end-to-end procedure.
- Comparison and integrity criteria.
- Any limitations preventing verification.

### G. Scientific integrity assessment
- Measurement preservation.
- Metadata preservation.
- Uncertainty handling.
- Quality flags.
- Missing values.
- Provenance.
- Original-file integrity.
- Remaining scientific concerns.

### H. Project lifecycle assessment
- Save, close, reopen, switching, and dirty-state behavior.
- Regression findings.
- Remaining concerns.

### I. Documentation audit
- Documents reviewed.
- Documents requiring updates.
- Inaccuracies or contradictions.
- Proposed documentation changes.

### J. Defect and gap register
For every issue, provide its classification, evidence, impact, and recommended action.

### K. Proposed implementation and verification sequence
Provide an appropriately scoped sequence for completing 2.2.4.

Separate:
- Verification activities.
- Required corrective implementation.
- Documentation updates.
- Final completion assessment.

Identify which work can be performed within 2.2.4 and which work requires separate approval.

### L. Approval decisions and unresolved questions
Identify all decisions requiring user approval.

Do not treat recommendations as approved decisions.

### M. Final readiness assessment
State one of:

- **Ready for 2.2.4 Build:** No blocking issues prevent the planned verification and documentation work.
- **Conditionally ready:** Specific conditions or narrowly scoped corrections must be resolved.
- **Blocked:** Prerequisites or significant defects prevent responsible completion verification.

Explain the reasoning.

---

## 14. Plan-mode restrictions

During this task:

- Do not create, edit, delete, rename, or move repository files.
- Do not implement code.
- Do not fix defects.
- Do not change dependencies or configuration.
- Do not modify the original Kepler-10b FITS file.
- Do not modify Foundation.
- Do not commit or push.
- Do not reset, clean, or rewrite Git history.
- Do not begin Stage 2.3 or later work.

You may inspect files, inspect FITS data read-only, review test code, and execute existing tests where safe.

Clearly report every command executed and its result.

If a significant defect is found, document it and stop short of making changes.

**Stop after delivering the complete Plan report. Wait for review and explicit authorization before making any changes.**



# BUILD MODE PROMPT

# Subtask 2.2.4 — Testing, Documentation, and Completion Verification
## BUILD Prompt

**Mode: BUILD. Perform the approved verification, testing, documentation, and narrowly scoped corrective work described in the reviewed 2.2.4 Plan report.**

You are working on the New_Project astronomy research application.

Repository:
`C:\Code\New_Project`

GitHub:
`https://github.com/brettadin/New_Project`

The application is a local-first astronomy research application built with Python 3.13 and PySide6.

Your task is to complete **Stage 2, Subtask 2.2.4 — Testing, Documentation, and Completion Verification**.

This is the final verification subtask for Stage 2.2 — Light-Curve Import.

The objective is to verify that Subtasks 2.2.1, 2.2.2, and 2.2.3 collectively provide a working, tested, documented, and scientifically reliable light-curve import workflow.

The approved 2.2.4 Plan report is the implementation specification for this task.

Do not independently expand the approved scope or redesign previously approved architecture.

---

## 1. Mandatory pre-implementation review

Before modifying anything:

1. Read and follow `AGENTS.md`.
2. Review applicable Foundation requirements. Foundation is authoritative and read-only.
3. Read the current development roadmap and development log.
4. Read the approved 2.2.4 Plan report.
5. Review the approved Plan and Build reports for 2.2.1, 2.2.2, and 2.2.3, where available.
6. Inspect the actual implementations from all three subtasks.
7. Inspect their automated tests.
8. Review relevant architecture, data-model, data-flow, persistence, testing, and decision documentation.
9. Inspect the current Git branch and working-tree status.

Verify that the current repository still matches the assumptions and findings in the approved Plan report.

**Do not overwrite, discard, or reset existing user changes.**

If the current implementation differs materially from the approved Plan report, stop and report the discrepancy before making affected changes.

If a prerequisite or significant defect requires a decision outside the approved plan, request approval rather than silently changing the design.

## 2. Overall verification objective

Verify the complete Stage 2.2 workflow:

1. Represent an astronomical light-curve dataset using the approved data model.
2. Import and validate a supported FITS dataset.
3. Preserve scientific measurements and metadata.
4. Associate the imported dataset with a research project.
5. Persist the dataset using the approved provisional storage mechanism.
6. Close and reopen the project.
7. Recover the dataset with its scientific information intact.

Verify that the workflow remains compatible with the existing project lifecycle.

The goal is to establish whether the initial scientific import workflow is ready for subsequent data presentation and analysis work.

## 3. Review Subtask 2.2.1 — Data-model implementation

Inspect the implemented data model and its tests.

Verify that the actual implementation satisfies the approved design for:

- Source-file information and provenance.
- Measurement representation.
- Measurement uncertainties and associations.
- Time values and time-reference metadata.
- Measurement units.
- Quality flags.
- Cadence identifiers.
- Missing and non-finite values.
- Validation warnings and errors.
- Original versus derived data distinctions.

Verify that:
- Required and optional fields behave as designed.
- Unknown metadata remains unknown.
- Measurement relationships remain unambiguous.
- Existing tests meaningfully exercise the model.
- Documentation matches the actual implementation.

Do not redesign or extend the data model merely to prepare for future features.

If a blocking defect is identified, implement only the narrowly scoped correction explicitly authorized by the approved Plan report.

## 4. Review Subtask 2.2.2 — FITS importer and validation

Inspect the importer, validation logic, and automated tests.

Verify:

### FITS handling
- FITS files are read using the approved Astropy-based implementation.
- Relevant HDUs and light-curve tables are identified correctly.
- Measurement columns are extracted according to the approved design.
- Different flux types remain distinct.
- Uncertainties remain associated with the correct measurements.
- Quality flags and cadence identifiers are preserved.

### Metadata
Verify preservation of:
- Source and target information.
- Mission and instrument information.
- Observation cadence.
- Measurement units.
- Time units.
- Time reference or epoch.
- Time scale.
- Original column information.
- Relevant FITS header information.

### Validation
Verify handling of:
- Missing required columns.
- Missing optional columns.
- Missing metadata.
- Non-numeric values.
- Non-finite values.
- Missing uncertainties.
- Invalid timestamps.
- Unexpected array shapes.
- Nonzero quality flags.
- Unsupported or ambiguous metadata.

Confirm that warnings and errors are reported appropriately.

Do not reimplement or replace the importer.

Correct only explicitly approved defects necessary to satisfy the existing requirements.

## 5. Review Subtask 2.2.3 — Project integration and persistence

Inspect the project-to-dataset integration and provisional persistence implementation.

Verify:

### Project association
- Datasets can be associated with the correct project.
- Dataset identity remains stable.
- Source information remains associated with each dataset.
- Multiple datasets are handled according to the approved design.
- Project metadata and scientific measurement content remain appropriately separated.

### Persistence
- Imported dataset content can be saved.
- Saved content can be recovered after reopening a project.
- Measurement values remain intact.
- Uncertainties remain correctly associated.
- Units and time references remain intact.
- Quality flags and cadence identifiers remain intact.
- Missing and non-finite values are handled according to the approved model.
- Source and provenance information remain available.

### Lifecycle integration
Verify:
- Project creation.
- Project opening.
- Project saving.
- Project closing.
- Project switching.
- Dirty-state tracking.
- Save/Discard/Cancel behavior.
- Failed dataset persistence.
- Missing original source files.
- Missing or corrupted persisted content.
- Recovery when one dataset cannot be loaded.

### Provisional storage
Confirm that:
- The approved provisional storage mechanism is used.
- Project metadata persistence remains appropriately separated from scientific dataset persistence.
- D6 remains respected.
- Permanent storage architecture is still deferred.
- Known limitations are documented.
- No unapproved database, ORM, or storage dependency has been introduced.

Do not redesign persistence during this task.

## 6. Automated testing

Review existing test coverage and execute the approved verification strategy.

At minimum, run:

- Data-model tests from 2.2.1.
- FITS importer and validation tests from 2.2.2.
- Project integration and persistence tests from 2.2.3.
- Existing project lifecycle regression tests.
- The complete automated test suite.

Inspect test assertions and ensure they exercise the intended behavior.

### Required testing principles

- Use temporary directories for project and persistence tests.
- Use controlled FITS fixtures for routine importer tests.
- Keep routine tests independent of machine-specific paths.
- Do not require the real Kepler-10b dataset for the standard test suite.
- Do not weaken, remove, or skip tests merely to obtain passing results.
- Preserve existing regression-test intent.
- Report test failures honestly.

Test coverage should address:

| Area | Verification |
|---|---|
| Data model | Construction and preservation |
| FITS structure | HDU and table identification |
| Importing | Correct measurement extraction |
| Metadata | Units, time references, source information |
| Measurements | Flux values and uncertainty associations |
| Quality | Quality flags and cadence identifiers |
| Missing data | Missing and non-finite value handling |
| Validation | Correct warnings and errors |
| Project integration | Dataset association and identity |
| Persistence | Save and reopen behavior |
| Recovery | Missing or corrupted content |
| Regression | Existing project lifecycle behavior |

If the approved Plan report identifies missing tests, implement those tests within the approved scope.

If a test exposes a defect, determine whether the correction is explicitly authorized by the Plan.

Do not make unrelated implementation changes.

### Test reporting

For every test command executed, report:
- Exact command.
- Exit code.
- Number of passed tests.
- Number of failed tests.
- Number of skipped tests, if applicable.
- Relevant warnings or errors.

Do not report tests as passing unless they were actually executed and passed.

## 7. Real Kepler-10b dataset verification

The existing user dataset is located at:

`C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits`

Use it for optional local end-to-end verification if it is available.

Previously reported characteristics include:
- FITS format.
- Kepler long-cadence observations.
- Approximately 476 rows.
- Approximately 9.7 days of observations.
- TIME represented in BKJD with TDB reference.
- SAP_FLUX and PDCSAP_FLUX measurements.
- Corresponding uncertainty fields.
- SAP_QUALITY and CADENCENO fields.
- Missing or non-finite flux values and nonzero quality flags.

Verify these characteristics from the actual file rather than assuming they remain correct.

### End-to-end procedure

If the dataset is available and the approved implementation supports the workflow:

1. Open or create a research project.
2. Import the Kepler-10b FITS dataset.
3. Inspect the imported measurements and metadata.
4. Save the project.
5. Close the project.
6. Reopen the project.
7. Recover the dataset.
8. Compare the recovered representation against the imported pre-save representation.

Verify preservation of:
- Measurement values.
- Uncertainties.
- Units.
- Time values and references.
- Quality flags.
- Cadence identifiers.
- Missing and non-finite values.
- Source and provenance metadata.

The original FITS file must remain unchanged.

Do not move, rename, overwrite, delete, or modify the dataset.

If the file is unavailable, report that real-dataset verification could not be performed. Do not treat its absence as an automated-test failure.

Real-dataset verification complements automated tests; it does not replace them.

## 8. Scientific integrity verification

Perform a focused review of the complete import and persistence workflow.

Confirm that the application does not silently:

- Normalize flux measurements.
- Detrend or filter observations.
- Remove nonzero quality flags.
- Drop missing or non-finite values.
- Convert units or time references.
- Invent missing metadata.
- Modify the original FITS file.

Verify that the application distinguishes:

1. Original source FITS data.
2. Imported dataset representation.
3. Future derived or transformed scientific data.

Document any limitations or unresolved scientific concerns.

Scientific-data preservation must not be inferred solely from successful serialization or passing generic tests. Verify the relevant values and metadata directly.

## 9. Project lifecycle regression verification

Confirm that adding scientific dataset functionality has not broken previously completed project behavior.

Run and inspect the existing tests for:

- Project creation and discovery.
- Project opening.
- Project saving.
- Project closing.
- Project switching.
- Dirty-state handling.
- Save/Discard/Cancel behavior.
- Preservation of the active project when switching fails.
- Existing project metadata persistence.
- Project status management.

Verify that dataset persistence failures are handled consistently with the existing project lifecycle.

Do not refactor unrelated project lifecycle functionality.

## 10. Documentation reconciliation

Follow the documentation-maintenance requirements in `AGENTS.md`.

Compare every relevant document against the actual code and test results.

Update applicable documents, including:

- Development roadmap.
- Development log.
- Architecture documentation.
- Data-model documentation.
- Data-flow documentation.
- Module responsibilities.
- Persistence and storage decisions.
- Testing and validation documentation.
- Project state and continuity records.

Document accurately:

- Implemented data-model behavior.
- FITS import and validation.
- Project-to-dataset integration.
- Provisional persistence.
- Scientific-data preservation.
- Error handling and recovery.
- Actual test coverage.
- Actual test results.
- Real-dataset verification status.
- Known limitations.
- Deferred architecture decisions.

### Documentation rules

- Do not claim functionality exists unless it is implemented.
- Do not claim tests passed unless they were executed and passed.
- Do not claim real-dataset verification occurred unless it was performed.
- Do not describe provisional persistence as a finalized permanent storage architecture.
- Do not mark future subtasks complete.
- Do not modify Foundation requirements or documents.

Before completion, compare documentation against the final code and test results.

Report documents changed and relevant documents intentionally left unchanged, with reasons.

## 11. Defect correction boundaries

The purpose of this task is verification, but narrowly scoped corrective implementation may be necessary.

Only correct defects that:

1. Prevent Stage 2.2 from meeting its approved requirements.
2. Are explicitly covered by the approved 2.2.4 Plan report.
3. Can be corrected without redesigning previously approved architecture.
4. Do not require unapproved scope expansion.

For every correction:

- Identify the original defect.
- Explain why it matters.
- Identify the affected files.
- Make the smallest appropriate correction.
- Add or update tests.
- Update relevant documentation.
- Verify that existing behavior remains intact.

If a defect requires:
- A new architectural decision.
- A change to an approved interface.
- A new dependency.
- A redesign of persistence.
- A substantial change to 2.2.1, 2.2.2, or 2.2.3.

Stop and request approval.

Do not use 2.2.4 as authorization for broad refactoring or new functionality.

## 12. Completion criteria

Assess the complete Stage 2.2 workflow against these requirements:

- The approved light-curve data model exists and is tested.
- The FITS importer supports the initial target dataset.
- FITS validation behaves as designed.
- Scientific measurements and metadata are preserved.
- Original source files remain unchanged.
- Imported datasets can be associated with research projects.
- Dataset content survives project save and reopen.
- Project lifecycle behavior remains correct.
- Failure handling is adequately tested.
- Automated tests are portable.
- Routine tests do not depend on the user's permanent dataset path.
- Documentation reflects actual implementation and test results.
- Provisional storage limitations are documented.
- No unresolved blocking defects remain.

Do not mark Stage 2.2 complete solely because the test suite passes.

The completion decision must consider implementation, scientific integrity, automated tests, documentation, and outstanding issues.

## 13. Scope exclusions

Do not implement or begin:

- New scientific functionality beyond the approved 2.2.1–2.2.3 scope.
- Data table interface (2.3).
- Light-curve visualization (2.3).
- BLS transit analysis (2.4).
- BLS uncertainty calculations (2.4).
- Analysis operation records (2.5).
- External astronomical archive integration.
- Permanent storage architecture redesign.
- New accounts, authentication, groups, or multi-user infrastructure.
- Unrelated project lifecycle refactoring.
- Unapproved dependencies or features.

If a requirement cannot be satisfied without work outside this scope, document the issue and request approval.

## 14. Implementation discipline

- Follow the approved 2.2.4 Plan report.
- Preserve existing user changes.
- Keep corrective changes minimal and traceable.
- Follow existing naming, typing, error-handling, and testing conventions.
- Do not duplicate existing functionality.
- Do not silently change public interfaces.
- Do not make unrelated formatting or cleanup changes.
- Do not modify the original FITS dataset.
- Do not modify Foundation.
- Do not commit or push.
- Do not reset, clean, or rewrite Git history.

If additional approval is needed, stop before implementing the affected change.

## 15. Final completion report

After completing verification, testing, approved corrections, and documentation updates, produce a structured report.

### A. Overall completion summary
- What was verified.
- What was corrected.
- Whether Stage 2.2 meets its completion criteria.

### B. Subtask verification
Report separately for:
- 2.2.1 — FITS Inspection and Data-Model Design.
- 2.2.2 — FITS Import and Validation.
- 2.2.3 — Project Integration and Provisional Persistence.

For each, identify verified functionality, test coverage, and remaining limitations.

### C. Files changed
For every changed or created file:
- Exact path.
- Purpose.
- Summary of changes.

### D. Automated testing
Include:
- Exact commands executed.
- Targeted test results.
- Full test-suite results.
- Passed, failed, and skipped counts.
- Warnings or errors.
- Any tests not executed and why.

### E. Real-dataset verification
Report:
- Whether the Kepler-10b FITS file was available.
- Whether the end-to-end workflow was executed.
- Which values and metadata were compared.
- Results.
- Any limitations.

### F. Scientific integrity
Explain how the implementation preserves:
- Measurement values.
- Uncertainties.
- Units.
- Time references.
- Quality flags.
- Cadence identifiers.
- Missing and non-finite values.
- Source and provenance information.
- Original-file integrity.

Identify unresolved scientific concerns.

### G. Project lifecycle and regression results
Report save, close, reopen, switching, dirty-state, and recovery behavior.

### H. Documentation updates
List documents changed and explain why.

Also list relevant documents intentionally left unchanged and explain why.

### I. Defect and limitation register
Separate:
- Blocking defects.
- Non-blocking defects.
- Test gaps.
- Documentation gaps.
- Architectural concerns.
- Deferred decisions.

Identify whether each issue was corrected, documented, or requires further approval.

### J. Scope compliance
Confirm that no Stage 2.3 or later functionality was implemented.

### K. Final completion assessment
Choose one:

**Complete**
- All required Stage 2.2 functionality is implemented.
- Required tests pass.
- Scientific integrity requirements are satisfied.
- Documentation is accurate.
- No unresolved blocking defects remain.

**Partially complete**
- Core functionality exists, but one or more required tests, corrections, or documentation items remain incomplete.

**Blocked**
- Significant defects, missing prerequisites, or unresolved architectural decisions prevent reliable completion.

Explain the decision and identify the next required action.

---

**Stop after completing Subtask 2.2.4. Do not begin Stage 2.3 or any later work.**

Do not commit or push. Leave all changes in the working tree for user review.

Wait for the user to review the completion report and explicitly authorize the next task.