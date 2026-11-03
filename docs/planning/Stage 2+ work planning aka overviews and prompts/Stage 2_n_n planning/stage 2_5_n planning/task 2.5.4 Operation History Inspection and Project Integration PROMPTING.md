
# PLAN PROMPT

# Task 2.5.4 — Operation History Inspection and Project Integration
## PLAN Prompt

**Mode: PLAN ONLY — inspect the current implementation and produce an implementation plan. Do not modify the repository.**

Prepare an implementation plan for Task 2.5.4 of Stage 2.5 in the New_Project repository.

The objective is to introduce a user-facing operation-history interface that allows users to inspect previously recorded operations within their research projects.

Tasks 2.5.2 and 2.5.3 establish the operation-record model, persistence, and BLS analysis integration. This task makes those records accessible through the existing desktop application.

The interface should allow users to view a project's operation history, select individual operations, and inspect their recorded inputs, configuration, results, uncertainty information, warnings, and limitations.

This is an inspection and project-integration task. It must use the existing operation-record architecture and persistence interfaces.

Do not redesign the operation-record model, persistence system, or BLS analysis workflow.

---

## 1. Mandatory governance and project inspection

Before preparing the plan:

1. Read the repository's `AGENTS.md`.
2. Respect the Foundation documentation and its read-only requirement.
3. Inspect the current Stage 2 roadmap and development log.
4. Review the Stage 2.5 overview.
5. Review the Task 2.5.1 design documentation.
6. Review the Task 2.5.2 overview, approved PLAN, implementation, tests, and completion report.
7. Review the Task 2.5.3 overview, approved PLAN, implementation, tests, and completion report.
8. Review this Task 2.5.4 overview.
9. Inspect the current repository state and Git working tree.

Verify the actual implementation of Tasks 2.5.2 and 2.5.3 rather than relying exclusively on earlier reports.

If the operation-record model, persistence interfaces, or BLS operation-record integration are not sufficiently implemented to support this task, identify the missing prerequisites and stop.

Do not design the history interface around functionality that does not actually exist.

Do not assume the repository is identical to an earlier snapshot.

### Inspect the current application

Examine the existing source code and tests for:

- Main application window and navigation.
- Project selection and project lifecycle.
- Existing project-specific panels or views.
- Dataset display and selection.
- Existing BLS result presentation.
- Existing visualization components.
- Operation-record model.
- Operation-record persistence and retrieval interfaces.
- BLS operation-record integration.
- Error and warning presentation.
- Existing UI architecture and styling conventions.
- Relevant tests and test fixtures.

Identify the exact source files, classes, functions, and interfaces involved.

---

## 2. Verify operation-record availability

Inspect the actual operation-record implementation and establish what information the history interface can retrieve.

Verify:

- How records are retrieved for a project.
- Whether records can be retrieved individually.
- How operation identity is represented.
- How operation types are represented.
- How project and dataset associations work.
- How timestamps are stored and interpreted.
- How operation statuses are represented.
- How input information is stored.
- How configuration and parameters are stored.
- How results are stored.
- How uncertainty information is represented.
- How warnings, errors, and limitations are stored.
- How missing or unavailable source datasets are represented.
- Whether result arrays or structured outputs can be retrieved safely.
- Whether records from earlier schema or software versions require special handling.

Identify the exact retrieval interfaces Task 2.5.4 should use.

Do not read or manipulate persisted files directly from the UI if the established persistence layer already provides retrieval interfaces.

Do not propose a separate operation-history storage mechanism.

If required information cannot be retrieved from the existing implementation, identify the exact gap and explain whether it belongs to Task 2.5.2, Task 2.5.3, or an unresolved design decision.

Do not silently expand Task 2.5.4 to redesign earlier work.

---

## 3. Plan the operation-history interface

Inspect the current desktop application's structure and recommend the most appropriate way to expose operation history.

Consider possible approaches such as:

- A dedicated operation-history panel.
- A project-specific history section.
- A separate history view.
- Another approach consistent with the existing application architecture.

Do not select a design without inspecting the current UI.

The proposed interface should make operation history easy to access while preserving the existing project workflow.

Explain:

- Where the history entry point should appear.
- How it relates to the active project.
- How the user accesses the list of operations.
- How an individual operation is selected.
- How the user returns to the history list or project.
- How the interface behaves when no records exist.

Avoid unnecessary navigation complexity or a complete UI redesign.

---

## 4. Plan operation-history presentation

Determine which identifying information should appear in the history list.

Consider the information actually available in the operation-record model:

- Operation name or type.
- Operation identifier, if useful.
- Date and time.
- Associated dataset.
- Operation status.
- Relevant summary information.
- Presence of warnings or errors.

The plan should explain:

- Which fields should appear in the main history list.
- Which fields belong in the individual operation detail view.
- How operations should be ordered.
- How successful, warning, incomplete, and failed operations should be distinguished.
- How missing or unavailable metadata should be presented.
- How records with incomplete information should remain understandable.

Prefer a clear and compact list rather than displaying every record field in the main history view.

### Ordering

Plan a consistent ordering approach, preferably chronological with recent operations easy to locate.

Verify the timestamp semantics before deciding how dates and times should be displayed.

Do not assume a timezone or silently reinterpret stored timestamps.

### Optional organization

Consider whether basic sorting or grouping is justified by the existing architecture and expected record volume.

Potential examples:

- Sorting by date.
- Sorting by operation type.
- Grouping by dataset.
- Distinguishing operation statuses.

Do not automatically include advanced search, filtering, or comparison functionality.

Explain which organization features are necessary for the initial implementation and which should be deferred.

---

## 5. Plan individual operation inspection

Determine how a user should inspect an individual operation.

The detail view should expose the information retained by the operation-record system.

Organize the proposed presentation into logical sections.

### A. Operation information

Consider:

- Operation identity.
- Operation type.
- Execution date and time.
- Completion status.
- Project association.
- Dataset association.
- Relevant software and method information.

### B. Input information

Consider:

- Dataset identity.
- Source reference.
- Selected measurement column.
- Associated uncertainty column.
- Time column.
- Measurement units.
- Time units and reference system.
- Relevant metadata.
- Original versus prepared or derived data distinctions.
- Data preparation or quality filtering actually applied.
- Excluded measurements, if recorded.

### C. Configuration

Consider:

- Actual BLS parameters.
- Period search limits.
- Period-grid configuration.
- Transit-duration configuration.
- Other parameters retained by the record.
- Relevant method information.

Display the values recorded for the historical operation.

Do not substitute current application defaults or current UI selections.

### D. Results

Consider the actual results available from the record:

- Best-fit period.
- Transit epoch.
- Transit duration.
- Transit depth.
- BLS power.
- Periodogram information.
- Phase-folded light-curve information.
- Transit model information.
- Parameter uncertainty estimates.
- Detection assessment.
- False-alarm probability, if implemented and recorded.

Determine which values should be shown as summary information and which belong in expanded details or existing visualizations.

Identify whether existing visualization components can be reused.

Do not assume that every stored result requires a separate plot or display component.

### E. Warnings, errors, and limitations

Plan how to display:

- Missing metadata.
- Analysis warnings.
- Errors.
- Incomplete results.
- Failed operations.
- Known limitations.
- Unavailable source datasets.
- Information that could not be persisted or retrieved.

Warnings and failures must not be hidden behind ordinary status labels.

The interface must not imply that a failed or incomplete operation succeeded.

---

## 6. Plan historical BLS result presentation

Inspect the existing BLS result-display and visualization implementations.

Determine how historical results can be presented without duplicating scientific calculation logic.

Consider:

- Reusing existing result widgets.
- Reusing existing periodogram visualizations.
- Reusing existing phase-folded light-curve visualizations.
- Displaying stored scalar results and uncertainty information.
- Displaying recorded detection assessments.
- Handling missing or incomplete stored result information.

The plan must distinguish between displaying persisted results and recalculating an analysis.

Historical operation inspection must not silently execute BLS again.

If a plot cannot be reconstructed from persisted information, the interface should explain that limitation.

Preserve scientific interpretation:

- A candidate detection is not a confirmed planet.
- Parameter uncertainty is not the same as detection significance.
- False-alarm probability is conditional on its specified null model.
- Historical results must be presented as outputs of the recorded operation, not as newly calculated results.

Do not change the BLS methodology or introduce new scientific analysis functionality.

---

## 7. Plan project integration and lifecycle behavior

Operation history belongs to the research project.

Inspect the existing project lifecycle and determine how the history interface should respond to project changes.

Plan behavior for:

### Opening a project
- Retrieve the operation records associated with that project.
- Display only that project's records.

### Switching projects
- Retrieve the newly active project's history.
- Prevent records from different projects from being mixed.
- Release or replace previously displayed history appropriately.

### Closing a project
- Clear or release project-specific history.
- Avoid displaying stale records as though they belong to another project.

### Reopening a project
- Retrieve historical records again.
- Preserve access to previously saved operations.

### Empty history
- Display an appropriate empty state.
- Do not treat an empty history as a loading or persistence error unless one actually occurred.

### Retrieval errors
- Handle missing, malformed, or inaccessible records safely.
- Communicate errors without corrupting existing project state.

### Missing source datasets
- Preserve access to historical record information where possible.
- Distinguish an unavailable source file from an unavailable operation record.
- Do not silently associate a historical operation with a replacement dataset.

Use the established project and persistence interfaces.

Do not introduce a separate history cache or storage mechanism without identifying why the existing architecture cannot support the requirement.

---

## 8. Plan record integrity and read-only inspection

Operation history is an inspection interface.

Determine how to ensure that viewing a record does not modify its historical information.

The implementation must preserve:

- Operation identity.
- Original timestamps.
- Historical input references.
- Actual parameter values.
- Recorded results.
- Uncertainty information.
- Warnings and limitations.
- Operation status.

The plan must explicitly prevent:

- Recalculating historical results simply to display them.
- Replacing historical parameter values with current defaults.
- Modifying operation records when they are opened or inspected.
- Treating missing values as zero.
- Hiding warnings or failures.
- Implying that historical results have been independently verified.
- Changing the original dataset.

If the existing UI architecture uses mutable data structures, explain how inspection can remain read-only.

Editing historical records is outside this task.

---

## 9. Plan testing

Identify the exact existing test files and propose the tests required for Task 2.5.4.

### A. History-view tests

Verify that:

- The history view is accessible from the intended project interface.
- Records are retrieved for the active project.
- Multiple operations appear independently.
- Records are ordered consistently.
- Operation types and statuses are represented correctly.
- Warning and error indicators are accurate.
- Empty histories are handled appropriately.
- Missing optional metadata is displayed safely.

### B. Operation-detail tests

Verify that:

- Selecting an operation displays its recorded information.
- Input information is displayed accurately.
- Actual BLS parameters are displayed accurately.
- Stored results are displayed correctly.
- Uncertainty information is preserved.
- Detection-assessment information is presented accurately.
- Warnings, limitations, and errors remain visible.
- Missing or unavailable information is represented appropriately.

### C. Project integration tests

Verify that:

- Opening a project retrieves its operation history.
- Switching projects displays the correct history.
- Closing a project clears or releases its history appropriately.
- Reopening a project restores access to historical operations.
- Records remain associated with their original datasets.
- Records from different projects are never mixed.

### D. Historical result presentation tests

Verify that:

- Persisted results are displayed without rerunning BLS.
- Existing visualization components are reused where appropriate.
- Missing stored visualization data is handled clearly.
- Historical results are not presented as newly calculated results.
- Scientific interpretation and warnings are retained.

### E. Integrity tests

Verify that:

- Inspecting an operation does not modify its record.
- Historical parameters are not replaced by current defaults.
- Historical results are not silently recalculated.
- Missing source files do not cause unrelated records to disappear.
- Incomplete and failed operations are not presented as successful.
- Empty or missing values are not converted into measured or calculated values.

### F. Regression tests

Verify that existing functionality remains operational:

- Project creation, opening, saving, and closing.
- Dataset import and persistence.
- Light-curve visualization.
- BLS analysis.
- Operation-record creation and persistence.
- Existing BLS result presentation.
- Existing project navigation.

Use portable fixtures and temporary directories.

Do not make automated tests depend on the user's absolute Kepler-10b dataset path.

Do not modify the original Kepler-10b FITS file.

Do not weaken or remove existing tests.

The plan should identify exact test files and proposed test locations wherever possible.

---

## 10. Plan documentation updates

Follow the documentation-maintenance requirements in `AGENTS.md`.

Identify which documents should change as a result of Task 2.5.4.

Consider:

- UI architecture.
- Main-window and navigation responsibilities.
- Project integration.
- Operation-history view responsibilities.
- Operation-detail presentation.
- Data flow and retrieval.
- Historical BLS result presentation.
- Read-only inspection behavior.
- Testing and validation.
- Known limitations.
- Stage 2 roadmap.
- Development log.

For each proposed documentation change, explain what should be updated and why.

Do not modify Foundation documents.

Do not mark Task 2.5.4 complete during planning.

---

## 11. Explicit scope boundaries

The implementation plan must preserve these boundaries.

### Included in Task 2.5.4
- User-facing operation-history access.
- Project-specific history retrieval.
- Operation-history list presentation.
- Individual operation inspection.
- Display of recorded inputs and configuration.
- Display of stored BLS results and uncertainty information.
- Display of warnings, limitations, and errors.
- Project lifecycle integration.
- Read-only historical inspection.
- Testing and documentation.

### Excluded from Task 2.5.4
- Rebuilding the operation-record model.
- Redesigning operation-record persistence.
- Changing BLS analysis or scientific methodology.
- Recalculating historical results.
- Replaying or automatically rerunning historical operations.
- Editing historical operation records.
- Building a new scientific comparison engine.
- Advanced reporting, export, or notebook functionality.
- Automated research workflows.
- Permanent storage architecture or database migration.
- Multi-user infrastructure or cloud synchronization.

Task 2.5.5 is responsible for final Stage 2.5 testing, documentation review, and completion verification.

### D6 constraint

Continue using the approved provisional persistence approach.

Do not introduce a permanent database, ORM, new persistence framework, or broad storage redesign.

If the existing retrieval interfaces cannot support the history interface, report the specific gap and stop for user review.

---

## 12. Required PLAN report

Return a detailed implementation plan using the following sections.

### A. Governance and prerequisites
- Relevant AGENTS.md and Foundation requirements.
- Task 2.5.1 design verification.
- Task 2.5.2 implementation and verification status.
- Task 2.5.3 implementation and verification status.
- Current Git working-tree state.
- Any missing prerequisites.

### B. Current UI and architecture findings
- Main-window structure.
- Navigation and project views.
- Existing result-display components.
- Existing visualization components.
- Project lifecycle integration points.
- Relevant source files and tests.

### C. Operation-record retrieval findings
- Exact retrieval interfaces.
- Available record fields.
- Project and dataset associations.
- Result and configuration structures.
- Status and warning information.
- Known retrieval or serialization limitations.

### D. Proposed history interface
- Recommended location in the application.
- Navigation and interaction flow.
- History-list structure.
- Identifying information to display.
- Ordering and status presentation.
- Empty and error states.

### E. Proposed operation-detail interface
- Information sections.
- Input and provenance presentation.
- Configuration presentation.
- Results and uncertainty presentation.
- Warnings, errors, and limitations.
- Handling of missing information.

### F. Historical BLS result presentation
- Existing components to reuse.
- Stored information available for display.
- Visualization requirements.
- Missing-result behavior.
- Confirmation that no historical recalculation is required.

### G. Project lifecycle integration
- Opening projects.
- Switching projects.
- Closing projects.
- Reopening projects.
- Empty history and retrieval failures.
- Dataset availability behavior.

### H. Record integrity
- How inspection remains read-only.
- How historical values are preserved.
- How warnings and limitations remain visible.
- Any risks involving mutable data or UI state.

### I. Testing plan
- Exact existing test files.
- Proposed new or modified tests.
- UI and project integration coverage.
- Historical result presentation coverage.
- Integrity and regression coverage.
- Portable fixture strategy.

### J. Documentation plan
- Exact documents to update.
- Purpose of each change.
- Documents inspected but intentionally left unchanged.

### K. Implementation sequence
Provide a step-by-step implementation order that minimizes unnecessary changes and allows focused testing.

### L. Risks and unresolved decisions
Identify:
- Missing operation-record fields.
- Retrieval limitations.
- UI architecture conflicts.
- Visualization limitations.
- Project lifecycle risks.
- Data integrity concerns.
- Any issue requiring explicit user approval.

### M. Readiness assessment
State whether Task 2.5.4 is ready for implementation.

If ready, provide a concise summary of the recommended design and expected files to change.

If not ready, identify the exact prerequisite or decision that must be resolved first.

---

## 13. Strict PLAN restrictions

This is a planning task only.

**Do not:**
- Modify source code.
- Create or modify tests.
- Modify documentation.
- Change configuration or dependencies.
- Modify datasets.
- Modify Foundation files.
- Commit or push changes.
- Reset, clean, or rewrite Git history.
- Implement any portion of Task 2.5.4.

You may inspect files, run non-destructive commands, and execute existing tests if useful for verifying current behavior.

Do not treat planning as approval to implement.

Finish by presenting the complete PLAN report and wait for explicit user approval before any BUILD work.



# BUILD PROMPT

# Task 2.5.4 — Operation History Inspection and Project Integration
## BUILD Prompt

**Mode: BUILD — implementation authorized only after explicit user approval of the Task 2.5.4 PLAN.**

Implement Task 2.5.4 of Stage 2.5 in the New_Project repository.

The objective is to introduce a user-facing operation-history interface that allows users to inspect previously recorded operations within their research projects.

Tasks 2.5.2 and 2.5.3 establish the operation-record model, persistence, and BLS analysis integration. This task makes those records accessible through the existing desktop application.

Users should be able to:

1. Open a research project.
2. Access that project's operation history.
3. Review previously recorded operations.
4. Select an individual operation.
5. Inspect its recorded inputs, configuration, results, uncertainty information, warnings, and limitations.
6. Return to the history list or project.

This is an inspection and project-integration task. It must use the existing operation-record architecture and persistence interfaces.

Do not redesign the operation-record model, persistence system, or BLS analysis workflow.

---

## 1. Mandatory pre-implementation checks

Before modifying anything:

1. Read the repository's `AGENTS.md` and follow its instructions.
2. Respect the Foundation documentation and its read-only requirement.
3. Inspect the current Stage 2 roadmap and development log.
4. Review the Stage 2.5 overview.
5. Review the approved Task 2.5.1 design documentation.
6. Review the Task 2.5.2 overview, approved PLAN, implementation, tests, and completion report.
7. Review the Task 2.5.3 overview, approved PLAN, implementation, tests, and completion report.
8. Review the Task 2.5.4 overview and approved PLAN.
9. Verify that the user has explicitly approved the Task 2.5.4 PLAN.
10. Inspect the current Git working tree and repository state.

**If the approved Task 2.5.4 PLAN or explicit approval is missing, stop. Do not implement anything.**

Verify that the operation-record model, persistence, and BLS recording functionality provide the interfaces and data required by the approved plan.

If prerequisites are incomplete or differ materially from the approved design, stop and report the specific issue.

Do not assume earlier reports accurately describe the current repository.

Preserve existing user changes. Do not overwrite, revert, or discard unrelated work.

---

## 2. Implement the approved history interface

Implement the history interface according to the approved PLAN.

The interface must fit naturally into the existing desktop application and project navigation.

Use the existing UI architecture, styling conventions, and project lifecycle mechanisms.

Follow the approved design for the location and structure of the history view.

The implementation should provide:

- An accessible entry point to operation history.
- A list of operations associated with the active project.
- Clear identification of individual operations.
- Consistent ordering.
- Appropriate status and warning indicators.
- Selection of an individual operation.
- Access to its recorded details.
- A straightforward way to return to the history list or project.

Do not redesign the main application window or introduce unnecessary navigation complexity.

Do not implement interface features that were not included in the approved PLAN.

### History-list presentation

Use the information actually available in the operation-record model.

Display appropriate identifying information, such as:

- Operation type or name.
- Date and time.
- Associated dataset.
- Operation status.
- Relevant summary information.
- Presence of warnings or errors.

Keep the list reasonably compact. Detailed information belongs in the individual operation view.

Follow the approved ordering and timestamp-display design.

Do not assume a timezone or silently reinterpret stored timestamps.

Clearly distinguish successful, warning, incomplete, and failed operations using the existing status model.

An operation must not appear successful merely because it is present in the history list.

### Empty history

Provide an appropriate empty state when the active project has no recorded operations.

An empty history must not be presented as a loading failure or persistence error unless an actual error occurred.

---

## 3. Implement individual operation inspection

Allow users to select an operation and inspect the information stored in its record.

Use the existing operation-record retrieval interfaces.

Do not read or modify persisted files directly from the UI when the established persistence layer already provides the required interfaces.

Organize the detail view into clear sections following the approved PLAN.

### A. Operation information

Display applicable information:

- Operation identity.
- Operation type.
- Execution date and time.
- Completion status.
- Associated project.
- Associated dataset.
- Relevant software and method information.

### B. Input information

Display the information actually retained by the record:

- Dataset identity.
- Source reference.
- Selected measurement column.
- Associated uncertainty column.
- Time column.
- Measurement units.
- Time units and reference system.
- Relevant metadata.
- Original versus prepared or derived data distinctions.
- Data preparation or quality filtering actually applied.
- Excluded measurements, if recorded.

Do not invent missing information.

Do not imply that preprocessing occurred when it did not.

### C. Configuration

Display the actual configuration recorded for the historical operation.

Include applicable BLS parameters, such as:

- Period search limits.
- Period-grid configuration.
- Transit-duration configuration.
- Other recorded search parameters.
- Relevant method information.

Do not substitute current application defaults or current UI selections for historical values.

### D. Results

Display the recorded results available from the operation record.

Consider the applicable information:

- Best-fit period.
- Transit epoch.
- Transit duration.
- Transit depth.
- BLS power.
- Periodogram information.
- Phase-folded light-curve information.
- Transit model information.
- Parameter uncertainty estimates.
- Detection assessment.
- False-alarm probability, if implemented and recorded.

Follow the approved PLAN for which results appear in the main detail view and which appear in expanded details or existing visualizations.

Do not duplicate scientific calculation logic.

Do not assume that every stored result requires a separate visualization.

### E. Warnings, errors, and limitations

Display applicable:

- Missing metadata.
- Analysis warnings.
- Errors.
- Incomplete results.
- Failed-operation information.
- Known limitations.
- Unavailable source datasets.
- Information that could not be persisted or retrieved.

Warnings and failures must remain visible and understandable.

Do not hide important limitations behind a generic status label.

Do not present incomplete or failed operations as successful.

---

## 4. Integrate historical BLS result presentation

Inspect and reuse the existing BLS result-display and visualization components wherever appropriate.

The history interface should allow users to inspect the BLS results retained by Task 2.5.3.

Where the persisted information supports it, provide access to:

- Best-fit transit parameters.
- Periodogram information.
- Phase-folded light-curve information.
- Transit model information.
- Uncertainty information.
- Detection assessment.
- Associated warnings and limitations.

### Historical results must not be recalculated

Displaying a historical operation must not automatically execute BLS again.

The interface must display the persisted results associated with that operation.

If a plot cannot be displayed because the required information was not persisted, communicate that limitation.

Do not silently reconstruct missing scientific outputs or substitute results from a different operation.

### Scientific interpretation

Preserve the distinction between:

- Numerical results.
- Parameter uncertainty.
- Detection significance or assessment.
- Scientific interpretation.

Do not present a candidate detection as a confirmed planet.

If false-alarm probability is displayed, preserve its relationship to the specified null model. Do not describe it as the probability that the period is correct or that a planet exists.

Historical results must be clearly identified as the outputs of the recorded operation, not as newly calculated results.

---

## 5. Implement project lifecycle integration

Operation history belongs to the research project.

Use the existing project lifecycle and operation-record retrieval interfaces.

Implement the behavior specified in the approved PLAN.

### Opening a project

- Retrieve the operation records associated with that project.
- Display only that project's records.
- Handle retrieval failures appropriately.

### Switching projects

- Retrieve the newly active project's history.
- Replace or release the previously displayed project history.
- Prevent records from different projects from being mixed.

### Closing a project

- Clear or release project-specific history.
- Avoid displaying stale records as though they belong to another project.

### Reopening a project

- Retrieve historical records again.
- Restore access to previously persisted operations.

### Empty history

- Display the appropriate empty state.
- Distinguish a genuinely empty history from a retrieval failure.

### Missing source datasets

- Preserve access to historical record information where possible.
- Distinguish an unavailable source file from an unavailable operation record.
- Do not silently associate a historical operation with a replacement dataset.

### Retrieval errors

Handle missing, malformed, or inaccessible records safely.

Communicate actual retrieval errors without corrupting existing project state.

Do not introduce a separate history-storage mechanism or unnecessary history cache.

---

## 6. Preserve record integrity and read-only inspection

The history interface is an inspection layer.

Viewing an operation must not modify its historical record.

Preserve:

- Operation identity.
- Original timestamps.
- Historical input references.
- Actual parameter values.
- Recorded results.
- Uncertainty information.
- Warnings and limitations.
- Operation status.

The implementation must not:

- Recalculate historical results simply to display them.
- Replace historical parameters with current defaults.
- Modify operation records when they are opened or inspected.
- Treat missing values as zero.
- Hide warnings or failures.
- Imply that historical results have been independently verified.
- Modify original datasets.
- Associate a historical record with a different dataset without an explicitly supported relationship.

If the existing UI architecture uses mutable data structures, ensure that the detail view does not accidentally modify the underlying record.

Editing historical operation records is outside this task.

---

## 7. Handle missing and incomplete information

The interface must remain usable when records do not contain every possible field.

Account for:

- Missing optional metadata.
- Incomplete records.
- Failed operations.
- Operations completed with warnings.
- Results that were not produced.
- Missing or unavailable source files.
- Unavailable stored result data.
- Older or incompatible record structures, where supported by the existing implementation.

Distinguish unavailable information from actual measured or calculated values.

Do not silently omit important information.

Do not invent default values to make the interface appear complete.

If a historical record can only be partially inspected, clearly identify which information is unavailable and why, where that information is known.

---

## 8. Testing and validation

Implement the tests identified in the approved PLAN.

Do not weaken, delete, or skip existing tests merely to make the implementation pass.

### A. History-view tests

Verify that:

- The history view is accessible through the intended project interface.
- Records are retrieved for the active project.
- Multiple operations appear independently.
- Records are ordered consistently.
- Operation types and statuses are represented correctly.
- Warning and error indicators are accurate.
- Empty histories are handled appropriately.
- Missing optional metadata is displayed safely.

### B. Operation-detail tests

Verify that:

- Selecting an operation displays its recorded information.
- Input information is displayed accurately.
- Actual BLS parameters are displayed accurately.
- Stored results are displayed correctly.
- Uncertainty information is preserved.
- Detection-assessment information is presented accurately.
- Warnings, limitations, and errors remain visible.
- Missing or unavailable information is represented appropriately.

### C. Project integration tests

Verify that:

- Opening a project retrieves its operation history.
- Switching projects displays the correct history.
- Closing a project clears or releases its history appropriately.
- Reopening a project restores access to historical operations.
- Records remain associated with their original datasets.
- Records from different projects are never mixed.

### D. Historical result presentation tests

Verify that:

- Persisted results are displayed without rerunning BLS.
- Existing visualization components are reused where appropriate.
- Missing stored visualization data is handled clearly.
- Historical results are not presented as newly calculated results.
- Scientific interpretation and warnings are retained.

### E. Integrity tests

Verify that:

- Inspecting an operation does not modify its record.
- Historical parameters are not replaced by current defaults.
- Historical results are not silently recalculated.
- Missing source files do not cause unrelated records to disappear.
- Incomplete and failed operations are not presented as successful.
- Empty or missing values are not converted into measured or calculated values.

### F. Regression tests

Verify that existing functionality remains operational:

- Project creation, opening, saving, and closing.
- Dataset import and persistence.
- Light-curve visualization.
- BLS analysis.
- Operation-record creation and persistence.
- Existing BLS result presentation.
- Existing project navigation.

Use portable fixtures and temporary directories.

Do not make automated tests depend on the user's absolute Kepler-10b dataset path.

Do not modify the original Kepler-10b FITS file.

Run targeted tests first, followed by the appropriate broader regression suite.

Report actual commands and results. Distinguish passed, failed, skipped, and unexecuted tests.

---

## 9. Documentation maintenance

Follow the documentation-maintenance requirements in `AGENTS.md`.

Before implementation, identify the documents affected by this task.

Update relevant documentation when the implementation changes or establishes:

- How operation history is accessed.
- How project-specific records are retrieved.
- How individual operations are inspected.
- Which inputs, parameters, results, and warnings are displayed.
- How incomplete or unavailable information is represented.
- How historical BLS results are presented.
- How read-only inspection is maintained.
- How project switching and closing affect history.
- Testing coverage and known limitations.

Update the appropriate UI, architecture, module-responsibility, data-flow, testing, roadmap, and development-log documentation as applicable.

Do not update every document indiscriminately.

Keep a clear distinction between:

- Functionality implemented in the current code.
- Functionality reserved for later development.
- Known limitations.
- Deferred architectural decisions.

Do not modify Foundation documents.

Do not mark Task 2.5.4 complete until implementation, tests, and documentation have been verified.

---

## 10. Explicit scope exclusions

Do not implement any of the following:

- Rebuilding the operation-record model.
- Redesigning operation-record persistence.
- Changing BLS analysis or scientific methodology.
- Recalculating historical results.
- Replaying or automatically rerunning historical operations.
- Editing historical operation records.
- Building a new scientific comparison engine.
- Advanced reporting, export, or notebook functionality.
- Automated research workflows.
- Permanent storage architecture or database migration.
- Multi-user infrastructure or cloud synchronization.

Task 2.5.5 remains responsible for final Stage 2.5 testing, documentation review, and completion verification.

### D6 storage constraint

Continue using the approved provisional persistence approach.

Do not introduce a permanent database, ORM, new persistence framework, or broad storage redesign.

If the existing retrieval interfaces cannot support the approved history interface, stop and report the specific gap rather than independently redesigning persistence.

---

## 11. Git and change-safety requirements

- Do not commit changes.
- Do not push to GitHub.
- Do not reset, clean, or rewrite Git history.
- Do not discard existing user changes.
- Do not overwrite unrelated files.
- Do not perform broad refactoring outside the approved scope.
- Keep modifications limited to the files necessary for Task 2.5.4.

Before finishing, inspect the working tree and review the complete diff.

---

## 12. Required completion report

Provide a structured report containing the following sections.

### A. Implementation summary

Explain:

- Where operation history is accessed.
- How the history interface is structured.
- How records are retrieved for the active project.
- How individual operations are inspected.
- How historical BLS results are presented.

### B. Files changed

For every changed file, explain:

- What changed.
- Why the change was necessary.
- Whether it contains implementation, tests, or documentation.

### C. History-view verification

Explain:

- How records are listed.
- How ordering works.
- How statuses and warnings are presented.
- How empty histories are handled.

### D. Operation-detail verification

Explain how the interface displays:

- Operation information.
- Inputs and provenance.
- Configuration.
- Results.
- Uncertainty and detection assessment.
- Warnings, errors, and limitations.

Identify any information that cannot currently be displayed and explain why.

### E. Project integration verification

Explain how the interface behaves when:

- Opening a project.
- Switching projects.
- Closing a project.
- Reopening a project.
- Encountering missing datasets or retrieval errors.

### F. Record-integrity verification

Explain how read-only inspection is maintained.

Confirm that historical parameters and results are not silently modified or recalculated.

### G. Testing results

Report:

- Exact test commands.
- Number of passed, failed, and skipped tests.
- Any failures and their causes.
- Any tests that could not be run.
- Regression-test results.

Do not report tests as passing unless they were actually executed successfully.

### H. Documentation updates

List:

- Documents updated and why.
- Relevant documents inspected but intentionally left unchanged.
- Remaining documentation gaps.

### I. Scope verification

Explicitly confirm that:

- No operation-record model redesign occurred.
- No persistence redesign occurred.
- No BLS scientific methodology was changed.
- Historical results are not automatically recalculated.
- Replay and automatic rerunning were not implemented.
- Historical operation editing was not implemented.
- No permanent storage redesign was introduced.
- No Foundation documents were modified.
- No unauthorized dependencies or frameworks were added.

### J. Git and working-tree status

Report:

- Modified and untracked files.
- Whether pre-existing user changes were preserved.
- Whether the final diff was inspected.
- Confirm that no commit or push was performed.

### K. Remaining issues and readiness

Identify unresolved issues, limitations, or decisions requiring user attention.

State whether Task 2.5.4 meets its completion criteria and is ready for review.

Do not declare the entire Stage 2.5 complete. Task 2.5.5 remains outstanding.

---

## 13. Final instruction

Implement only the explicitly approved Task 2.5.4 PLAN.

Prioritize clear operation-history inspection, accurate presentation of historical scientific information, project isolation, record integrity, and compatibility with the existing application architecture.

If the approved design proves incompatible with the current code, or implementation requires an unapproved architectural or scientific decision, stop and report the specific conflict.

Do not silently redesign around it.

When implementation and verification are complete, provide the required report and wait for the user's review before proceeding to Task 2.5.5.