# PLAN PROMPT

# Task 2.5.5 — Testing, Documentation, and Completion Verification OVERVIEW

## 1. Purpose

Task 2.5.5 is the final verification task for Stage 2.5: Operation Records.

Its purpose is to determine whether the complete operation-record workflow has been implemented correctly, tested adequately, documented accurately, and integrated with the existing application.

This task does not introduce another major feature. It verifies the work completed across Tasks 2.5.1–2.5.4 and determines whether Stage 2.5 meets its overall objectives.

The central question is:

Can the application reliably record, preserve, retrieve, and display the history of scientific operations associated with a research project?

## 2. Relationship to Previous Tasks

Task 2.5.5 depends on the completion of the preceding Stage 2.5 tasks.

| Task  | Responsibility                                       | What Task 2.5.5 verifies                                                                         |
| ----- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| 2.5.1 | Operation Record Design and Implementation Planning  | The approved design was followed and relevant requirements were addressed.                       |
| 2.5.2 | Operation Record Model and Persistence               | Records are structured, stored, retrieved, and preserved correctly.                              |
| 2.5.3 | Analysis Operation Recording and Results Integration | BLS executions produce accurate records containing their actual inputs, parameters, and results. |
| 2.5.4 | Operation History Inspection and Project Integration | Users can inspect historical operations within the correct research project.                     |
| 2.5.5 | Testing, Documentation, and Completion Verification  | The complete workflow is verified and Stage 2.5 readiness is established.                        |

Task 2.5.5 should evaluate the integrated implementation rather than treating each previous task as an isolated feature.

Previous completion reports are useful evidence, but the current repository, implementation, tests, and documentation must be inspected directly.

## 3. Full Workflow Verification

Verify the complete operation-record workflow from analysis execution through historical inspection.

The intended workflow is:

1. Open or create a research project.
2. Import or access a dataset associated with that project.
3. Configure and execute a BLS analysis.
4. Automatically create an operation record containing the actual analysis information.
5. Persist the record using the established storage approach.
6. Close and reopen the project.
7. Retrieve the historical operation record.
8. Display it in the project's operation history.
9. Select the operation and inspect its recorded information.
10. Confirm that the historical record accurately represents the original operation.

Verify that this workflow operates consistently and that each stage preserves the information needed by subsequent stages.

## 4. Operation Record Integrity

Verify that operation records preserve the information necessary to understand what the application did.

This includes:

- Operation identity and type.
- Project association.
- Dataset association.
- Execution date and time.
- Selected measurement and input columns.
- Associated uncertainty information.
- Relevant units and time references.
- Data preparation or filtering actually applied.
- Actual BLS configuration and parameters.
- Recorded analysis results.
- Uncertainty information.
- Detection assessment.
- Warnings, errors, and limitations.
- Relevant software and method information.

Confirm that historical records are not silently altered during saving, loading, project reopening, or inspection.

Verify that multiple operations can be retained independently, including multiple analyses involving the same dataset.

Missing or unavailable information must remain distinguishable from actual measured or calculated values.

## 5. Persistence and Project Lifecycle Verification

Verify that operation records remain accessible across the normal project lifecycle.

Test the following scenarios:

- Creating a project and recording an operation.
- Saving a project containing operation records.
- Closing and reopening that project.
- Retrieving its historical operation records.
- Switching between projects containing different operation histories.
- Closing a project and ensuring its history is no longer presented as belonging to the active project.
- Handling projects with no recorded operations.
- Handling unavailable source datasets.
- Handling missing, malformed, or inaccessible operation records.

Verify that records remain associated with their original projects and datasets.

Confirm that the implementation continues to respect the approved provisional persistence approach under D6. This task does not authorize permanent storage architecture or database redesign.

## 6. BLS Recording and Scientific Integrity Verification

Verify that the operation-record workflow captures the actual BLS execution rather than merely storing a summary of the currently displayed results.

Check that recorded information corresponds to the parameters and inputs actually used.

Verify that:

- The selected measurement is correctly identified.
- The associated uncertainty information is preserved.
- The time column, units, and time reference are accurately represented.
- Actual runtime BLS parameters are retained.
- Recorded results correspond to the completed analysis.
- Incomplete and failed analyses are represented appropriately.
- Analysis failures are distinguishable from persistence failures.
- Warnings and limitations remain associated with the relevant operation.

Scientific interpretation must remain accurate.

In particular:

- A candidate detection must not be presented as a confirmed planet.
- Parameter uncertainty must not be confused with detection significance.
- False-alarm probability must retain its relationship to the specified noise-only null model.
- Historical results must not be silently recalculated or substituted with newer results.

Task 2.5.5 verifies these behaviors. It does not authorize changes to the BLS methodology or scientific analysis scope.

## 7. Operation History and User Interface Verification

Verify that users can inspect operation history reliably through the existing application interface.

Review:

- History access and navigation.
- Operation identification.
- Chronological ordering.
- Status presentation.
- Warning and error indicators.
- Empty-history behavior.
- Individual operation detail views.
- Input and provenance presentation.
- Configuration and parameter presentation.
- Results and uncertainty presentation.
- Scientific limitations and warnings.
- Navigation back to the history list and project.

Verify that historical information is displayed from persisted records.

Confirm that opening an operation does not automatically rerun its analysis or modify its record.

The interface should remain understandable when optional metadata or historical results are unavailable.

## 8. Error Handling and Edge-Case Testing

Evaluate how the complete workflow behaves under less common conditions.

Include applicable cases such as:

- Failed analysis execution.
- Partially completed analysis.
- Persistence failure after successful analysis.
- Missing optional metadata.
- Missing uncertainty values.
- Unavailable source datasets.
- Missing historical result information.
- Multiple operations associated with one dataset.
- Multiple datasets within one project.
- Multiple projects with separate operation histories.
- Invalid or incomplete records.
- Unsupported or incompatible record information.

Verify that errors are communicated accurately and that one failed operation does not corrupt unrelated records or project data.

Do not introduce artificial recovery behavior that could misrepresent scientific results.

## 9. Automated Testing and Regression Verification

Review the existing automated test suite and identify whether it adequately covers the operation-record workflow.

Testing should cover:

### A. Record model and persistence

- Record creation and validation.
- Serialization and deserialization.
- Saving and retrieving records.
- Multiple records per project and dataset.
- Preservation of recorded values.
- Missing and invalid information.
- Persistence and retrieval failures.

### B. BLS integration

- Automatic operation-record creation.
- Actual input and parameter capture.
- Results association.
- Uncertainty and detection-assessment capture.
- Incomplete and failed operations.
- Separation of analysis and persistence failures.

### C. History interface

- Record listing and ordering.
- Status and warning presentation.
- Individual operation inspection.
- Empty and incomplete records.
- Missing source information.
- Historical result presentation without recalculation.

### D. Project integration

- Project opening and closing.
- Project switching.
- Project reopening.
- Project-specific history isolation.
- Persistence across application sessions.

### E. Regression testing

Verify that operation-record functionality has not broken existing capabilities, including:

- Project creation and management.
- Dataset importing.
- Dataset persistence.
- Light-curve visualization.
- BLS analysis.
- Existing result presentation.
- Existing project navigation.

Use portable test fixtures and temporary directories.

Automated tests must not depend on the user's absolute Kepler-10b dataset path or modify the original FITS file.

Run the appropriate targeted tests and the complete available regression suite.

Report actual test execution results, including failures, skipped tests, and tests that could not be executed.

## 10. Documentation Review and Accuracy

Review the documentation affected by Stage 2.5.

The objective is to ensure that documentation accurately describes the implemented system rather than the original plan or intended future behavior.

Review relevant documentation, including:

- Stage 2 roadmap.
- Development log.
- Operation-record design documentation.
- Architecture documentation.
- Data models and data-flow documentation.
- Module responsibilities.
- Persistence documentation.
- BLS workflow documentation.
- UI and navigation documentation.
- Testing and validation documentation.
- Relevant decision records.
- Project continuity documentation.

Verify that documentation accurately describes:

- The operation-record model.
- Record relationships and project associations.
- Persistence and retrieval behavior.
- BLS operation recording.
- Recorded inputs and provenance.
- Configuration and results.
- Uncertainty and detection assessment.
- Historical operation inspection.
- Error handling and limitations.
- Existing testing coverage.
- Deferred functionality and architectural decisions.

Identify documentation that is outdated, incomplete, inconsistent, or unsupported by the current implementation.

Do not rewrite unrelated documentation or modify Foundation documents.

## 11. Roadmap and Development Status

Evaluate whether Stage 2.5 meets its completion criteria.

The roadmap and development log should distinguish:

- Tasks completed and verified.
- Tasks implemented but not fully verified.
- Outstanding issues.
- Deferred capabilities.
- Remaining architectural decisions.

Do not mark a task complete merely because its implementation exists.

Completion should reflect actual implementation, testing, documentation, and integration evidence.

If Stage 2.5 is not ready for completion, document the specific gaps and identify the work required to resolve them.

## 12. Architectural and Scope Compliance

Confirm that Stage 2.5 remained within its approved scope.

Verify that:

- The approved operation-record design was followed.
- The existing persistence architecture was retained.
- D6 storage constraints were respected.
- Original datasets remain unchanged.
- Existing scientific methodology was preserved.
- No unapproved dependencies or frameworks were introduced.
- No unnecessary multi-user or cloud infrastructure was added.
- Historical operation inspection remains read-only.
- No automatic replay or historical rerunning was introduced.
- No unrelated architectural redesign occurred.
- Foundation documentation remains unchanged.

Identify any deviations and explain whether they were explicitly approved.

## 13. Known Limitations and Deferred Work

Document remaining limitations honestly.

Stage 2.5 establishes operation recording and historical inspection. It does not establish a complete scientific workflow-replay system.

The following remain outside its scope unless separately approved:

- Automatic reconstruction of historical analysis environments.
- Automatic replay or rerunning of historical operations.
- Advanced operation comparison.
- Advanced history search and filtering.
- Exporting operation histories into external reporting formats.
- Notebook-based analysis history.
- Workflow automation.
- Additional scientific analysis methods.
- Permanent storage architecture redesign.
- Multi-user synchronization or cloud services.

These capabilities may be considered in later stages.

## 14. Expected Outcome

At the end of Task 2.5.5, the project should have a verified operation-record workflow that allows users to:

- Execute a scientific analysis.
- Automatically record the operation.
- Preserve its inputs, configuration, results, and relevant scientific context.
- Retain the record within the correct research project.
- Close and reopen the project without losing access to its history.
- Inspect historical operations and their results.
- Understand warnings, uncertainty, and limitations associated with each operation.

The documentation and roadmap should accurately reflect what has been implemented and verified.

## 15. Completion Criteria

Task 2.5.5 can be considered complete when:

1. Tasks 2.5.1–2.5.4 have been inspected and their required functionality is present.
2. The complete operation-record workflow has been verified.
3. Records preserve the required inputs, configuration, results, and provenance.
4. Persistence and project lifecycle behavior are verified.
5. BLS operation recording accurately reflects actual executions.
6. Historical operation inspection works correctly.
7. Error handling and important edge cases have been evaluated.
8. Relevant automated tests pass, with failures and limitations accounted for.
9. Existing functionality passes the appropriate regression tests.
10. Documentation accurately reflects the implementation.
11. Roadmap and development-log status are accurate.
12. D6, Foundation, and other approved architectural constraints have been respected.
13. Remaining limitations and deferred work are documented.
14. No unresolved issue prevents the operation-record workflow from meeting its intended objectives.

If these criteria are not met, Task 2.5.5 should identify the remaining work rather than declaring Stage 2.5 complete.

## 16. Final Stage 2.5 Outcome

Successful completion of Task 2.5.5 establishes the first complete operation-history foundation for New_Project.

The application will no longer depend solely on its latest displayed analysis results. It will retain a project-associated history of scientific operations and provide a way to inspect what was done, which data and parameters were used, what results were produced, and what limitations applied.

This provides an important foundation for future scientific reproducibility, traceability, and more advanced research workflows without prematurely implementing a full replay system.



# BUILD PROMPT

# Task 2.5.5 — Testing, Documentation, and Completion Verification
## BUILD Prompt

**Mode: BUILD — implementation and documentation updates are authorized only after the Task 2.5.5 PLAN has been reviewed and explicitly approved by the user.**

Complete Task 2.5.5, the final task of Stage 2.5: Operation Records, in the New_Project repository.

The objective is to verify the complete operation-record workflow, address approved-scope deficiencies identified during planning, update documentation to reflect the verified implementation, and establish whether Stage 2.5 meets its completion criteria.

This is the final verification task for Stage 2.5. It is not an authorization for new feature development or architectural redesign.

The work must follow the approved Task 2.5.5 PLAN and the existing project governance requirements.

---

## 1. Mandatory pre-implementation checks

Before making changes:

1. Read the repository's `AGENTS.md` and follow its instructions.
2. Respect all applicable Foundation requirements. Foundation documents are read-only.
3. Review the current Stage 2 roadmap and development log.
4. Review the Stage 2.5 overview.
5. Review the Task 2.5.1 overview, approved PLAN, and implementation-related documentation.
6. Review the Task 2.5.2 overview, approved PLAN, implementation, tests, and completion report.
7. Review the Task 2.5.3 overview, approved PLAN, implementation, tests, and completion report.
8. Review the Task 2.5.4 overview, approved PLAN, implementation, tests, and completion report.
9. Review the Task 2.5.5 overview and approved PLAN.
10. Inspect the current source code, tests, documentation, and Git working tree.
11. Verify that the user has explicitly approved the Task 2.5.5 PLAN.

**If the approved PLAN or explicit user approval is missing, stop. Do not implement anything.**

Verify that the repository still matches the assumptions and findings in the approved PLAN.

Do not assume that previous completion reports accurately describe the current implementation.

Preserve all existing user changes. Do not overwrite, revert, discard, or reorganize unrelated work.

If the repository has materially changed since the PLAN was approved, stop and report the discrepancy before proceeding.

---

## 2. Follow the approved PLAN

Use the approved Task 2.5.5 PLAN as the implementation and verification specification.

Complete the verification activities in the approved sequence.

The PLAN should establish:

- Which requirements are already implemented.
- Which requirements need additional testing.
- Which implementation deficiencies require correction.
- Which documentation requires updates.
- Which manual checks are necessary.
- Which completion criteria must be satisfied.

Do not independently expand or reinterpret the approved scope.

If the PLAN identifies a defect, address it only when:

1. The correction is within the approved Stage 2.5 scope.
2. The correction is included in the approved PLAN.
3. The correction does not require an unapproved architectural or scientific decision.

If an issue requires a new architectural decision, scientific-method change, storage redesign, or scope expansion, stop and report it for user review.

Do not silently make an unapproved decision.

---

## 3. Verify Tasks 2.5.1–2.5.4

Evaluate the actual implementation of each preceding task.

### Task 2.5.1 — Operation Record Design and Implementation Planning

Verify that:

- The approved design documentation exists.
- The implementation follows the approved design.
- General operation-record requirements are represented.
- BLS-specific information is appropriately supported.
- Project and dataset relationships are defined.
- Persistence and retrieval responsibilities are clear.
- Historical inspection is distinguished from replay and rerunning.
- Relevant limitations and decisions are documented.

Report any discrepancies between the approved design and actual implementation.

Do not redesign the record model during final verification.

### Task 2.5.2 — Operation Record Model and Persistence

Verify that:

- The operation-record model is implemented.
- Record identity and relationships are retained.
- Multiple records can belong to one project.
- Multiple records can reference the same dataset.
- Inputs, configuration, results, status, warnings, and limitations are represented as designed.
- Serialization and deserialization work correctly.
- Records can be saved and retrieved.
- Historical information survives project reopening.
- Missing and invalid information is handled appropriately.
- The implementation respects D6.

Run the relevant model and persistence tests.

Address only approved-scope defects identified in the approved PLAN.

### Task 2.5.3 — Analysis Operation Recording and Results Integration

Verify that:

- BLS executions create operation records as intended.
- Actual analysis inputs are captured.
- Measurement and uncertainty associations are preserved.
- Time references, units, and relevant metadata are retained.
- Actual runtime BLS parameters are recorded.
- Results are associated with the correct operation.
- Uncertainty and detection-assessment information is retained.
- Warnings and limitations are captured.
- Incomplete and failed operations are represented appropriately.
- Analysis failures are distinguishable from persistence failures.
- Multiple analyses create independent records.

Confirm that recorded information corresponds to the actual execution.

Do not change the BLS scientific methodology as part of this task.

### Task 2.5.4 — Operation History Inspection and Project Integration

Verify that:

- Users can access operation history.
- Only the active project's records are displayed.
- Records are ordered consistently.
- Statuses and warnings are represented accurately.
- Individual operations can be inspected.
- Historical inputs, parameters, results, and limitations are displayed.
- Historical BLS results are presented without automatic recalculation.
- Empty and incomplete histories are handled appropriately.
- Project switching, closing, and reopening behave correctly.
- Historical inspection does not modify operation records.

Confirm that the UI uses the established operation-record retrieval interfaces.

Do not add new history features or redesign the interface during this task.

---

## 4. Verify the complete end-to-end workflow

Test the integrated workflow using the actual application architecture.

The expected sequence is:

1. Create or open a research project.
2. Import or access a dataset associated with that project.
3. Configure a BLS analysis.
4. Execute the analysis.
5. Verify that an operation record is created automatically.
6. Inspect the record's captured inputs and provenance.
7. Verify that actual BLS parameters are retained.
8. Verify that analysis results are associated with the correct record.
9. Verify that the record is persisted.
10. Close the project.
11. Reopen the project.
12. Retrieve the historical operation.
13. Open the operation-history interface.
14. Select the historical operation.
15. Inspect its details and results.
16. Confirm that the historical information remains unchanged.

For each step:

- Execute the appropriate automated or manual verification.
- Record the actual outcome.
- Identify the relevant test or source module.
- Report failures or limitations.
- Confirm whether the expected behavior is satisfied.

Do not report the complete workflow as verified if only individual components were tested.

Clearly distinguish automated end-to-end coverage from manually verified application behavior.

---

## 5. Verify operation-record integrity

Confirm that records preserve the information necessary to understand historical scientific operations.

Evaluate:

- Operation identity and type.
- Project association.
- Dataset association.
- Execution date and time.
- Selected measurement and input columns.
- Associated uncertainty information.
- Units and time references.
- Relevant metadata.
- Original, prepared, and derived data distinctions.
- Data preparation or quality filtering actually applied.
- Actual BLS configuration and runtime parameters.
- Recorded results.
- Parameter uncertainty.
- Detection assessment.
- Warnings, errors, and limitations.
- Relevant software and method information.

Verify that:

- Saving and loading do not unintentionally change recorded values.
- Multiple operations remain independent.
- Multiple operations on the same dataset remain distinguishable.
- Multiple datasets retain their correct relationships.
- Missing information remains distinguishable from actual values.
- Historical inspection does not modify persisted records.
- Project switching does not mix records.
- Unavailable source files do not silently invalidate unrelated historical records.

Do not replace missing information with invented defaults.

Do not convert missing values into numerical zero.

Do not change the record schema without explicit authorization.

---

## 6. Verify persistence and project lifecycle behavior

Test the actual project lifecycle and persistence integration.

### A. Project creation and recording

Verify that a newly created project can receive and persist operation records.

### B. Project reopening

Verify that a project containing operation records can be closed and reopened without losing access to its history.

### C. Project switching

Verify that switching between projects retrieves the correct history for each project.

Confirm that records from different projects are never mixed.

### D. Project closing

Verify that project-specific history is cleared or released appropriately when a project closes.

### E. Missing or unavailable information

Verify handling of:

- Unavailable source datasets.
- Missing operation records.
- Malformed records.
- Inaccessible persistence files.
- Empty histories.
- Retrieval errors.

The interface must distinguish a genuinely empty history from a retrieval failure.

Respect the existing persistence architecture and D6.

Do not introduce a permanent database, ORM, or new persistence framework.

---

## 7. Verify BLS recording and scientific integrity

Confirm that operation records reflect the actual BLS execution.

Verify the capture of:

- Selected measurement column.
- Associated uncertainty column.
- Time column and reference.
- Measurement and time units.
- Data preparation or quality filtering actually applied.
- Actual period-search limits.
- Period-grid configuration.
- Transit-duration configuration.
- Other runtime parameters.
- Best-fit period.
- Transit epoch.
- Transit duration.
- Transit depth.
- BLS power.
- Periodogram information.
- Phase-folded light-curve information.
- Transit model information.
- Parameter uncertainty.
- Detection assessment.
- False-alarm probability, if implemented and recorded.
- Warnings and limitations.

Verify the following distinctions:

- Candidate detection is not confirmed planetary detection.
- Parameter uncertainty is not detection significance.
- False-alarm probability is conditional on its specified noise-only null model.
- False-alarm probability is not the probability that the period is correct or that a planet exists.
- Analysis failure is distinct from persistence failure.
- Missing results are distinct from numerical zero values.

Historical results must be displayed from the persisted operation record.

Do not silently recalculate or substitute historical results.

If an existing implementation cannot satisfy a scientific-integrity requirement, document the limitation and stop if resolving it requires an unapproved scientific or architectural decision.

---

## 8. Verify operation-history interface behavior

Verify the existing history interface and detail views.

Evaluate:

- History access and navigation.
- Record listing.
- Chronological ordering.
- Operation identification.
- Status presentation.
- Warning and error indicators.
- Empty-history behavior.
- Individual operation selection.
- Input and provenance presentation.
- Configuration presentation.
- Results presentation.
- Uncertainty and detection-assessment presentation.
- Warning and limitation presentation.
- Navigation back to history and project.

Confirm that:

- Historical results are read from persisted records.
- Existing BLS visualizations are reused where appropriate.
- Selecting an operation does not rerun BLS.
- Historical parameters are not replaced by current defaults.
- Historical results are not silently recalculated.
- Inspecting an operation does not modify its record.

If a visualization cannot be displayed because the required information was not persisted, verify that the interface communicates the limitation clearly.

Do not create artificial replacement data.

---

## 9. Verify error handling and edge cases

Execute the approved tests for applicable cases:

- Analysis execution failure.
- Partial analysis completion.
- Persistence failure after successful analysis.
- Missing optional metadata.
- Missing uncertainty information.
- Unavailable source datasets.
- Missing stored result information.
- Multiple operations on one dataset.
- Multiple datasets in one project.
- Multiple projects with independent histories.
- Malformed records.
- Inaccessible persistence files.
- Unsupported or incompatible record information.
- Empty operation histories.

For each case, verify:

- Expected application behavior.
- Expected operation-record state.
- Expected user-visible behavior.
- Whether unrelated records and project data remain intact.

Do not hide failures or introduce unapproved recovery behavior.

---

## 10. Automated testing and regression verification

Execute the test plan approved for Task 2.5.5.

At minimum, verify the following areas.

### A. Record model and persistence

- Model construction and validation.
- Serialization and deserialization.
- Saving and retrieval.
- Multiple records.
- Project and dataset relationships.
- Missing and invalid information.
- Persistence failures.

### B. BLS integration

- Automatic record creation.
- Input capture.
- Parameter capture.
- Results association.
- Uncertainty and detection assessment.
- Failed and incomplete analyses.
- Persistence failure behavior.

### C. History interface

- Listing and ordering.
- Status and warning presentation.
- Detail inspection.
- Empty and incomplete histories.
- Historical result presentation.

### D. Project lifecycle

- Opening and closing.
- Switching projects.
- Reopening projects.
- Project-specific record isolation.

### E. Regression

Verify that the following continue to work:

- Project creation and management.
- Dataset import and persistence.
- Light-curve visualization.
- BLS analysis.
- Existing result presentation.
- Operation-record creation and persistence.
- Existing project navigation.

### Testing rules

- Use portable fixtures and temporary directories.
- Do not make tests depend on the user's absolute Kepler-10b dataset path.
- Do not modify the original FITS file.
- Do not weaken, delete, or skip existing tests to make the suite pass.
- Do not introduce artificial test shortcuts that bypass actual application behavior.
- Do not report unexecuted tests as passing.
- Report passed, failed, skipped, and unexecuted tests separately.

Run targeted tests first, followed by the appropriate complete regression suite.

If a test fails:

1. Determine whether it is an implementation defect, test defect, environment issue, or unrelated pre-existing failure.
2. Compare the failure with the approved PLAN.
3. Correct it only if the correction is within approved scope.
4. Rerun the affected test.
5. Rerun relevant regression tests.
6. Document unresolved failures accurately.

Do not change unrelated code to obtain a passing test suite.

---

## 11. Manual verification

Perform the manual UI and workflow checks identified in the approved PLAN.

At minimum, evaluate the complete user-facing history workflow where the application environment permits:

- Open a project.
- Access its operation history.
- Inspect an existing operation.
- Navigate back to the history list.
- Switch projects.
- Close and reopen a project.
- Inspect a historical BLS result.
- Verify the displayed information remains associated with the correct operation.

Record:

- Exact steps performed.
- Expected behavior.
- Actual behavior.
- Any failures or limitations.

Do not claim manual verification if the application was not actually launched or the relevant workflow was not performed.

If a manual check cannot be completed because of an environment limitation, explain the limitation and identify what remains unverified.

---

## 12. Documentation maintenance and final review

Follow the documentation-maintenance requirements in `AGENTS.md`.

Inspect and update only documentation relevant to the verified implementation.

Potentially affected documents include:

- Stage 2 roadmap.
- Development log.
- Stage 2.5 overview.
- Operation-record design documentation.
- Architecture documentation.
- Data models.
- Data flow.
- Module responsibilities.
- Persistence documentation.
- BLS workflow documentation.
- UI and navigation documentation.
- Testing and validation documentation.
- Relevant decision records.
- Project continuity documentation.

Ensure that documentation accurately describes:

- The operation-record model.
- Project and dataset relationships.
- Persistence and retrieval behavior.
- BLS operation recording.
- Recorded inputs and provenance.
- Actual configuration and parameters.
- Recorded results.
- Uncertainty and detection assessment.
- Historical operation inspection.
- Project lifecycle integration.
- Error handling.
- Testing coverage.
- Known limitations.
- Deferred functionality.

Do not document planned functionality as though it is implemented.

Distinguish:

- Implemented and verified functionality.
- Implemented but incompletely verified functionality.
- Known limitations.
- Deferred capabilities.
- Unresolved decisions.

Do not rewrite unrelated documentation.

Do not modify Foundation documents.

### Documentation consistency review

Before declaring completion:

1. Compare documentation against the current source code.
2. Compare documented behavior against actual tests.
3. Check for contradictory or outdated descriptions.
4. Verify that roadmap status reflects actual evidence.
5. Verify that the development log accurately summarizes completed work.
6. Identify relevant documents inspected but intentionally left unchanged.

---

## 13. Roadmap and Stage 2.5 completion assessment

Evaluate whether each Stage 2.5 task meets its completion criteria.

Do not mark a task complete solely because its implementation exists.

Completion must be supported by implementation, testing, documentation, and integration evidence appropriate to that task.

### Task-level status

Verify and report the status of:

- Task 2.5.1 — Operation Record Design and Implementation Planning.
- Task 2.5.2 — Operation Record Model and Persistence.
- Task 2.5.3 — Analysis Operation Recording and Results Integration.
- Task 2.5.4 — Operation History Inspection and Project Integration.
- Task 2.5.5 — Testing, Documentation, and Completion Verification.

### Stage-level status

Stage 2.5 may be marked complete only if its overall objectives have been met.

If a required task remains incomplete, a critical test fails, or an unresolved issue prevents reliable operation recording and historical inspection, do not mark Stage 2.5 complete.

Update the roadmap and development log to reflect the actual status.

Clearly distinguish completed work from deferred future functionality.

---

## 14. Architectural and scope compliance

Confirm that the implementation respects the approved Stage 2.5 scope.

Verify that:

- The approved operation-record design was followed.
- The existing persistence architecture was retained.
- D6 storage constraints were respected.
- Original datasets remain unchanged.
- Existing scientific methodology was preserved.
- No unapproved dependencies or frameworks were introduced.
- No unnecessary cloud or multi-user infrastructure was added.
- Historical inspection remains read-only.
- No automatic replay or historical rerunning was introduced.
- No Foundation documents were modified.
- No unrelated architectural redesign occurred.

Report any deviations.

Do not independently approve or resolve new architectural decisions.

---

## 15. Known limitations and deferred work

Document limitations that remain after verification.

Keep deferred functionality separate from incomplete required functionality.

The following are outside Stage 2.5 unless separately approved:

- Automatic reconstruction of historical analysis environments.
- Automatic replay or rerunning of historical operations.
- Advanced operation comparison.
- Advanced history search and filtering.
- Notebook-based history.
- Advanced reporting or export.
- Workflow automation.
- Additional scientific analysis methods.
- Permanent storage architecture redesign.
- Multi-user synchronization or cloud services.

Do not implement these features during Task 2.5.5.

---

## 16. Documentation and completion criteria

Task 2.5.5 is complete only when:

1. Tasks 2.5.1–2.5.4 have been inspected and their required functionality is verified.
2. The complete operation-record workflow has been evaluated.
3. Record integrity has been verified.
4. Persistence and project lifecycle behavior have been verified.
5. BLS operation recording accurately reflects actual executions.
6. Historical operation inspection works correctly.
7. Error handling and important edge cases have been evaluated.
8. Relevant automated tests pass, with failures and limitations accounted for.
9. Existing functionality passes the appropriate regression tests.
10. Necessary manual UI verification has been completed or its limitations explicitly documented.
11. Documentation accurately reflects the implementation.
12. Roadmap and development-log status are accurate.
13. D6, Foundation, and other approved architectural constraints have been respected.
14. Remaining limitations and deferred work are documented.
15. No unresolved issue prevents the operation-record workflow from meeting its intended objectives.

If these criteria are not satisfied, report the remaining work and do not declare Stage 2.5 complete.

---

## 17. Git and change-safety requirements

- Do not commit changes.
- Do not push to GitHub.
- Do not reset, clean, or rewrite Git history.
- Do not discard existing user changes.
- Do not overwrite unrelated files.
- Do not perform broad refactoring outside the approved scope.
- Keep modifications limited to the approved verification, testing, necessary corrections, and documentation work.

Before finishing:

1. Inspect the complete Git working tree.
2. Review the complete diff.
3. Identify every modified and untracked file.
4. Confirm that pre-existing user changes were preserved.
5. Confirm that no unauthorized files or Foundation documents were modified.

---

## 18. Required completion report

Provide a structured report with the following sections.

### A. Executive summary

Summarize:

- What was verified.
- Whether the complete operation-record workflow works.
- Whether Task 2.5.5 meets its completion criteria.
- Whether Stage 2.5 is ready to be marked complete.

### B. Previous-task verification

For each Task 2.5.1–2.5.4, report:

- Relevant implementation.
- Verification performed.
- Test evidence.
- Outstanding issues.
- Final status.

### C. End-to-end workflow results

Describe the complete workflow verification.

Identify which steps were automated and which were manually verified.

Report actual outcomes and any limitations.

### D. Operation-record integrity

Explain how record identity, inputs, provenance, configuration, results, uncertainty, warnings, and relationships were verified.

Report any missing or incomplete information.

### E. Persistence and project lifecycle

Report results for:

- Saving.
- Closing.
- Reopening.
- Project switching.
- Project isolation.
- Missing source datasets.
- Retrieval failures.

### F. BLS scientific-integrity verification

Explain how actual input and parameter capture, result association, uncertainty, detection assessment, and failure handling were verified.

Identify any scientific-integrity limitations.

### G. History interface verification

Report history-list, detail-view, navigation, empty-state, status, and historical-result verification.

Confirm whether historical results were displayed without automatic recalculation.

### H. Error handling and edge cases

List the scenarios tested and their actual outcomes.

Identify unresolved error-handling issues.

### I. Automated testing results

Provide:

- Exact commands executed.
- Number of passed tests.
- Number of failed tests.
- Number of skipped tests.
- Tests not executed.
- Failure explanations.
- Regression-test results.

Do not claim tests passed unless they were actually executed successfully.

### J. Manual verification results

List the steps performed, expected outcomes, actual outcomes, and any unverified behavior.

### K. Documentation changes

For every changed document, explain:

- What changed.
- Why it changed.
- How its accuracy was verified.

Also list relevant documents inspected but intentionally left unchanged and identify remaining documentation gaps.

### L. Roadmap and development-log status

Report the final status of each Stage 2.5 task.

Explain the evidence supporting each status.

Identify any remaining blockers or deferred work.

### M. Architectural and scope compliance

Explicitly confirm whether:

- D6 was respected.
- Foundation documents remained unchanged.
- Original datasets remained unchanged.
- Scientific methodology was preserved.
- No unauthorized dependencies or frameworks were added.
- No permanent storage redesign occurred.
- No replay or automatic rerunning was introduced.
- No unrelated refactoring occurred.

Report any deviations.

### N. Known limitations and deferred work

Separate required incomplete functionality from optional future capabilities.

### O. Git and working-tree status

Report:

- Modified files.
- Untracked files.
- Pre-existing changes preserved.
- Final diff review.
- Confirmation that no commit or push occurred.

### P. Final readiness assessment

Choose one:

- **Task 2.5.5 Complete — Stage 2.5 Complete:** All required criteria are satisfied and supported by verification evidence.
- **Task 2.5.5 Complete — Stage 2.5 Not Complete:** Verification and documentation are complete, but required functionality or other Stage 2.5 criteria remain unmet.
- **Task 2.5.5 Incomplete:** Verification, testing, documentation, or required corrections remain outstanding.

Explain the decision and identify the exact remaining work, if any.

---

## 19. Final instruction

Complete Task 2.5.5 using only the approved PLAN.

The goal is to establish, with evidence, whether New_Project can reliably record, preserve, retrieve, and display the history of scientific operations associated with research projects.

Prioritize scientific accuracy, record integrity, persistence, project isolation, historical inspection, testing quality, and documentation accuracy.

Do not expand the project scope or independently resolve unapproved architectural or scientific decisions.

Do not mark Stage 2.5 complete unless its actual completion criteria have been satisfied.

When finished, provide the full completion report and wait for the user's review before proceeding to any subsequent stage.