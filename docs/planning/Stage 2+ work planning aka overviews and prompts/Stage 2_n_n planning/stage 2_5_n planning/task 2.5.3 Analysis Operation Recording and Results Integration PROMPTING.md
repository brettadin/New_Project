# PLAN PROMPT

# Task 2.5.3 — Analysis Operation Recording and Results Integration
## PLAN Prompt

**Mode: PLAN ONLY — inspect the current implementation and produce an implementation plan. Do not modify the repository.**

Prepare an implementation plan for Task 2.5.3 of Stage 2.5 in the New_Project repository.

The objective is to connect the existing BLS analysis workflow to the operation-record model and persistence system established in Task 2.5.2.

The application should automatically create and persist an operation record for each BLS analysis execution, retaining the actual inputs, configuration, results, uncertainty information, warnings, limitations, and project/dataset associations.

This task is an integration task. It must use the existing BLS implementation and approved operation-record architecture rather than redesigning either one.

---

## 1. Mandatory governance and project inspection

Before preparing the plan:

1. Read the repository's `AGENTS.md`.
2. Respect the Foundation documentation and its read-only requirement.
3. Inspect the current Stage 2 roadmap and development log.
4. Review the Stage 2.5 overview.
5. Review the Task 2.5.1 design documentation.
6. Review the Task 2.5.2 overview, approved PLAN, implementation documentation, and completion report.
7. Inspect the current repository state and Git working tree.
8. Verify the actual implementation of Tasks 2.5.1 and 2.5.2 rather than relying exclusively on previous reports.

If Task 2.5.2 has not been implemented and verified sufficiently to provide the operation-record interfaces required by this task, identify the missing prerequisites and stop. Do not design around an assumed interface.

Do not assume the repository is identical to an earlier snapshot.

### Inspect the relevant implementation

Examine the actual source code and tests for:

- BLS analysis execution.
- BLS configuration and parameter handling.
- Analysis input preparation and data selection.
- Measurement and uncertainty-column selection.
- Time values, time references, and units.
- Existing preprocessing or quality filtering behavior.
- BLS results and periodogram structures.
- Phase-folded light curves and transit models.
- Parameter uncertainty calculations.
- Detection assessment and false-alarm probability, where implemented.
- Warnings, limitations, and error handling.
- Project lifecycle and active-project identification.
- Dataset identity and project/dataset associations.
- Operation-record model and persistence interfaces.
- Existing UI actions that initiate BLS analysis.
- Existing tests covering these workflows.

Identify the actual files, classes, functions, and interfaces involved.

Do not assume that the implementation matches the Task 2.5.3 overview exactly. Report discrepancies.

---

## 2. Verify the approved operation-record interfaces

Inspect the Task 2.5.2 implementation and establish:

- How operation records are created.
- Which fields are required.
- Which fields are optional.
- How operation types are represented.
- How operation statuses are represented.
- How project and dataset associations work.
- How input information and configuration are stored.
- How results, warnings, errors, and limitations are stored.
- How records are saved.
- How records are retrieved.
- How persistence failures are reported.
- What validation and serialization rules apply.

Identify the exact interfaces that Task 2.5.3 should use.

Do not propose a duplicate BLS-specific record model or a separate persistence mechanism.

If the existing interfaces cannot represent information required by BLS recording, identify the specific gap and explain whether it requires a narrowly scoped change to Task 2.5.2 or an unresolved design decision.

Do not silently expand Task 2.5.3 to redesign the record model.

---

## 3. Plan BLS workflow integration

Determine where operation recording should occur in the existing BLS workflow.

The plan must explain the sequence of events from the user's analysis request through completion and persistence.

Consider:

1. Identifying the active project.
2. Identifying the selected dataset.
3. Capturing the actual analysis inputs.
4. Capturing the actual BLS configuration.
5. Creating the operation record.
6. Executing BLS.
7. Associating results with the correct operation.
8. Updating the operation status.
9. Persisting the completed or incomplete record.
10. Handling any errors during execution or persistence.

Identify the appropriate integration points and explain why they are suitable.

Avoid unnecessary coupling between the UI, scientific calculation code, operation-record model, and persistence layer.

Prefer the existing architectural patterns.

The plan must also explain how the existing BLS result-display behavior will remain functional.

---

## 4. Plan input and provenance capture

Determine exactly which information the existing BLS workflow uses and how that information should be captured.

Inspect and plan for the applicable information:

### Dataset identity
- Project association.
- Dataset identifier.
- Source file or source reference.
- Relevant dataset metadata.
- Original versus prepared or derived data distinctions.

### Measurement selection
- Selected measurement column.
- Associated uncertainty column.
- Time column.
- Measurement units.
- Time units and reference system.
- Other metadata relevant to interpreting the inputs.

### Data preparation
- Actual rows or measurements supplied to BLS.
- Excluded or invalid measurements, if applicable.
- Quality filtering, if actually applied.
- Preprocessing or transformations, if actually applied.
- Relevant warnings about missing or unusable information.

Do not assume that a preprocessing operation occurs merely because the application has the ability to perform one.

The record must describe what actually happened, not what could have happened.

Do not introduce automatic filtering, normalization, detrending, or other preprocessing.

Explain which information should be stored directly and which should be referenced through existing dataset identity or metadata interfaces, following the approved Task 2.5.1 and 2.5.2 designs.

---

## 5. Plan BLS configuration capture

Inspect the actual BLS implementation and identify every parameter that materially affects the analysis.

Consider the existing implementation's:

- Period search limits.
- Period-grid configuration.
- Frequency factor or resolution.
- Transit-duration configuration.
- Other search parameters.
- Relevant calculation settings.
- Any user-selectable options.

For each parameter, identify:

- Where it originates.
- Its actual runtime value.
- Whether it is a default or user-selected value.
- How it is passed into the calculation.
- How it should be represented in the operation record.

The record must capture the values actually used by the analysis, not merely the values displayed in the UI or the defaults that were available.

Do not invent new BLS parameters or change the scientific method.

---

## 6. Plan BLS results integration

Inspect the actual result structures and determine how they should be associated with the operation record.

Consider all applicable outputs currently produced by the implementation:

- Best-fit period.
- Transit epoch.
- Transit duration.
- Transit depth.
- BLS power.
- Periodogram data.
- Phase-folded light-curve information.
- Transit model information.
- Parameter uncertainty estimates.
- Detection assessment.
- False-alarm probability, if implemented.
- Warnings and limitations.

For each output, identify:

- Its current source in the code.
- Its data type and structure.
- Whether it is a scalar, array, structured result, or derived output.
- Whether it is already serializable.
- How it should be stored or referenced.
- Whether any information would be lost during serialization.

Do not assume that every displayed plot or derived visualization needs to be persisted independently. Follow the approved record design and identify any unresolved storage requirements.

### Scientific interpretation

Preserve the distinction between:

- Numerical analysis results.
- Parameter uncertainty.
- Detection significance or assessment.
- Scientific interpretation.

Do not alter the existing scientific methodology or imply that a candidate detection is a confirmed planet.

If false-alarm probability is recorded, preserve its relationship to the specified null model and existing implementation.

Identify any result information that the current record model cannot adequately represent.

---

## 7. Plan operation status and failure handling

Inspect the actual BLS execution and persistence error paths.

Determine how the integration should represent:

- Successful completion.
- Completion with warnings.
- Partial completion.
- Invalid configuration.
- Missing required inputs.
- Insufficient usable measurements.
- Numerical or computational failure.
- Interrupted analysis, if applicable.
- Operation-record persistence failure.

Follow the status model approved in Task 2.5.2.

The plan must explain when a record is created, when its status changes, and what information is retained if execution fails.

Do not represent an incomplete or failed analysis as successful.

Consider the distinction between an analysis failure and a persistence failure. Explain how each should be reported without misleading the user about whether the analysis ran or whether its results were saved.

Do not invent new status categories or change the record model without identifying the need and requesting approval.

---

## 8. Plan project and dataset relationships

Explain how multiple BLS operations will be associated with the correct project and dataset.

Verify that:

- Each operation has its own identity.
- Repeated analyses of the same dataset produce separate records.
- Different parameter configurations remain distinguishable.
- Records do not overwrite one another.
- Records remain associated with their original project.
- Historical records do not silently become associated with a different dataset if a source file is replaced or moved.

Follow the approved identity and relationship design.

Do not implement operation-history browsing or filtering screens.

---

## 9. Plan testing

Identify the exact tests that should be added or modified.

Include the following categories where applicable:

### A. Operation-record integration
- A BLS execution creates an operation record.
- The record has the correct operation type.
- The correct project and dataset are associated.
- Multiple executions create independent records.

### B. Input and configuration capture
- Actual measurement selection is recorded.
- Correct uncertainty association is recorded.
- Time column and reference information are preserved.
- Actual BLS parameter values are recorded.
- Input preparation and exclusions are represented accurately.

### C. Results integration
- BLS results are associated with the correct operation.
- Relevant uncertainty information is retained.
- Detection-assessment information is preserved.
- Warnings and limitations are retained.
- Serialization does not silently lose relevant result information.

### D. Failure handling
- Invalid configuration is handled correctly.
- Missing or insufficient input data is handled correctly.
- Failed and incomplete operations are represented accurately.
- Persistence failures are reported correctly.
- A failed operation is not presented as successful.

### E. Persistence and project reopening
- Operation records survive project closure and reopening.
- Multiple records remain independently retrievable.
- Historical configuration and results remain intact.

### F. Regression testing
- Project lifecycle remains functional.
- Dataset import and persistence remain functional.
- Light-curve visualization remains functional.
- BLS calculations remain unchanged.
- Existing uncertainty and detection-assessment behavior remains unchanged.

Use portable fixtures and temporary directories.

Do not make automated tests depend on the user's absolute Kepler-10b dataset path.

Do not modify the original Kepler-10b FITS file.

Do not weaken or remove existing tests.

The plan should identify the exact existing test files and proposed test locations wherever possible.

---

## 10. Plan documentation updates

Follow the documentation-maintenance requirements in `AGENTS.md`.

Identify which documentation should change as a result of BLS operation-record integration.

Consider:

- BLS module responsibilities.
- Operation-record architecture.
- Data models and serialization.
- Data flow.
- Project persistence.
- Scientific workflow and provenance.
- Testing and validation.
- Decisions and known limitations.
- Stage 2 roadmap.
- Development log.

For each proposed documentation change, explain what needs to be updated and why.

Do not modify Foundation documents.

Do not mark Task 2.5.3 complete during planning.

---

## 11. Explicit scope boundaries

The implementation plan must preserve the following boundaries.

### Included in Task 2.5.3
- Connecting BLS analysis to the operation-record system.
- Capturing actual BLS inputs and configuration.
- Associating BLS results with operation records.
- Recording warnings, limitations, and failures.
- Persisting BLS operation records.
- Testing and documenting the integration.

### Excluded from Task 2.5.3
- Rebuilding the operation-record model.
- Redesigning project persistence.
- Building operation-history UI.
- Searching or filtering historical operations through the UI.
- Reconstructing or replaying historical operations.
- Automatically rerunning previous analyses.
- Adding new scientific analysis methods.
- Changing BLS scientific methodology.
- Introducing new preprocessing methods.
- Permanent database architecture or migration.
- New dependencies or frameworks without explicit approval.

Task 2.5.4 is responsible for user-facing operation-history inspection.

Task 2.5.5 is responsible for final Stage 2.5 testing, documentation, and completion verification.

### D6 constraint

The existing D6 decision defers permanent storage architecture. Continue using the approved provisional persistence approach.

Do not introduce a permanent database, ORM, new persistence framework, or broad storage redesign.

If the existing implementation cannot support the required integration within these boundaries, report the specific issue and stop for user review.

---

## 12. Required PLAN report

Return a detailed implementation plan using the following sections.

### A. Governance and prerequisites
- Relevant AGENTS.md and Foundation requirements.
- Task 2.5.1 design verification.
- Task 2.5.2 implementation and verification status.
- Current Git working-tree state.
- Any missing prerequisites.

### B. Current architecture findings
- BLS execution flow.
- Analysis inputs and configuration.
- Results and uncertainty structures.
- Project and dataset identification.
- Operation-record model and persistence interfaces.
- Relevant source files and tests.

### C. Integration design
- Proposed execution sequence.
- Exact integration points.
- Responsibilities of affected modules.
- How UI, scientific calculations, record model, and persistence will interact.

### D. Input and provenance capture
- Exact input fields.
- Measurement and uncertainty associations.
- Dataset identity and metadata.
- Data preparation and exclusions.
- Stored versus referenced information.

### E. BLS configuration capture
- Actual parameters.
- Their sources in the implementation.
- How runtime values will be recorded.

### F. Results integration
- Existing result structures.
- Proposed record associations.
- Serialization considerations.
- Uncertainty and detection-assessment handling.
- Any gaps in the approved record model.

### G. Status and failure handling
- Record creation and update sequence.
- Successful, warning, partial, and failed execution behavior.
- Persistence-failure handling.

### H. Project and dataset relationships
- Multiple-operation behavior.
- Identity preservation.
- Project association.
- Historical dataset references.

### I. Testing plan
- Exact existing test files.
- Proposed new or modified tests.
- Integration and regression coverage.
- Portable fixture strategy.

### J. Documentation plan
- Exact documents to update.
- Purpose of each change.
- Documents intentionally left unchanged.

### K. Implementation sequence
Provide a step-by-step implementation order that minimizes unnecessary changes and allows focused testing.

### L. Risks and unresolved decisions
Identify:
- Architectural conflicts.
- Missing record fields.
- Serialization limitations.
- Scientific provenance gaps.
- Error-handling concerns.
- Any issue requiring explicit user approval.

### M. Readiness assessment
State whether Task 2.5.3 is ready for implementation.

If ready, provide a concise summary of the recommended implementation approach and the files expected to change.

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
- Implement any portion of Task 2.5.3.

You may inspect files, run non-destructive commands, and execute existing tests if useful for verifying current behavior.

Do not treat planning as approval to implement.

Finish by presenting the complete PLAN report and wait for explicit user approval before any BUILD work.



# BUILD PROMPT

# Task 2.5.3 — Analysis Operation Recording and Results Integration
## BUILD Prompt

**Mode: BUILD — implementation authorized only after explicit user approval of the Task 2.5.3 PLAN.**

Implement Task 2.5.3 of Stage 2.5 in the New_Project repository.

The objective is to connect the existing BLS analysis workflow to the operation-record model and persistence system established in Task 2.5.2.

Each BLS analysis execution should produce an appropriately identified, persistent operation record containing the actual inputs, configuration, results, uncertainty information, warnings, limitations, and project/dataset associations.

This is an integration task. Preserve the existing BLS scientific implementation and approved operation-record architecture.

Do not independently redesign either system.

---

## 1. Mandatory pre-implementation checks

Before modifying anything:

1. Read the repository's `AGENTS.md` and follow its instructions.
2. Respect the Foundation documentation and its read-only requirement.
3. Inspect the current Stage 2 roadmap and development log.
4. Review the Stage 2.5 overview.
5. Review the approved Task 2.5.1 design documentation.
6. Review the Task 2.5.2 overview, approved PLAN, implementation, tests, and completion report.
7. Review the Task 2.5.3 overview and approved PLAN.
8. Verify that the user has explicitly approved the Task 2.5.3 PLAN.
9. Inspect the current Git working tree and repository state.
10. Verify the actual implementation before editing.

**If the approved Task 2.5.3 PLAN or explicit approval is missing, stop. Do not implement anything.**

Confirm that Task 2.5.2 provides the operation-record model and persistence interfaces required by the approved plan.

If those prerequisites are incomplete or differ materially from the approved design, stop and report the specific issue.

Do not assume earlier reports accurately describe the current repository.

Preserve existing user changes. Do not overwrite, revert, or discard unrelated work.

---

## 2. Implement the approved integration design

Implement the exact integration sequence established by the approved PLAN.

The implementation should connect:

- The existing BLS execution workflow.
- The existing project and dataset identification mechanisms.
- The approved operation-record model.
- The approved persistence interfaces.
- The existing BLS result and uncertainty structures.

The integration should follow the existing architecture and avoid unnecessary coupling between the UI, scientific calculation code, operation-record model, and persistence layer.

Use the interfaces established in Task 2.5.2. Do not introduce a separate BLS-specific record model or independent persistence mechanism.

Do not change the BLS algorithm or scientific methodology.

### Expected execution sequence

Follow the approved plan for the precise sequence, but ensure the implementation accounts for:

1. Identifying the active project.
2. Identifying the selected dataset.
3. Capturing the actual analysis inputs.
4. Capturing the actual BLS configuration.
5. Creating an operation record.
6. Executing BLS.
7. Associating the resulting outputs with the correct record.
8. Updating the operation status.
9. Persisting the record.
10. Handling execution and persistence errors.

Do not create misleading successful records for analyses that did not complete successfully.

Preserve the existing BLS result-display behavior.

---

## 3. Capture actual analysis inputs and provenance

Record the information the BLS calculation actually uses.

Follow the approved record design and PLAN for field names, relationships, and storage.

Capture applicable information including:

### Dataset identity
- Project association.
- Dataset identifier.
- Source file or source reference.
- Relevant dataset metadata.
- Original versus prepared or derived data distinctions.

### Measurement selection
- Selected measurement column.
- Associated uncertainty column.
- Time column.
- Measurement units, where available.
- Time units and reference system.
- Other metadata needed to interpret the inputs.

### Data preparation
- Actual measurements supplied to BLS.
- Excluded or invalid measurements, if applicable.
- Quality filtering, if actually applied.
- Preprocessing or transformations, if actually applied.
- Relevant warnings about missing or unusable information.

The record must describe what actually happened.

Do not assume preprocessing or filtering occurred merely because the application supports those capabilities.

Do not introduce automatic filtering, normalization, detrending, or other transformations.

Preserve the distinction between original imported data and the specific data supplied to the calculation.

Do not modify original datasets.

---

## 4. Capture actual BLS configuration

Record the BLS parameters that materially affect each analysis.

Inspect the actual implementation and follow the approved PLAN.

Capture applicable values such as:

- Period search limits.
- Period-grid configuration.
- Frequency factor or resolution.
- Transit-duration configuration.
- Other search parameters.
- Relevant calculation settings.
- User-selectable options.

Record the actual runtime values supplied to the calculation.

Do not substitute interface defaults for the values actually used.

Do not invent parameters or change the scientific method.

Preserve the distinction between default and user-selected values where the approved design requires it.

---

## 5. Integrate BLS results

Associate the actual results produced by the BLS implementation with the operation record.

Follow the approved plan for serialization and storage.

Capture applicable outputs, including:

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
- False-alarm probability, if implemented.
- Warnings and limitations.

Preserve the actual result structures and avoid unnecessary duplication.

Do not silently discard information that is necessary to interpret the results.

If a result contains arrays or structured data, follow the approved serialization approach and verify that the stored representation can be retrieved without unintended loss.

Do not assume every displayed plot needs a separate persisted copy. Follow the approved record design.

### Scientific integrity

Maintain the distinction between:

- Numerical results.
- Parameter uncertainty.
- Detection significance or assessment.
- Scientific interpretation.

Do not change the existing scientific methodology.

Do not present a candidate detection as a confirmed planet.

If false-alarm probability is recorded, preserve its relationship to the specified null model. Do not describe it as the probability that the period is correct or that a planet exists.

Do not add new scientific conclusions or confidence claims.

---

## 6. Implement operation status and failure handling

Use the status model established in Task 2.5.2.

Implement the status transitions and error handling specified by the approved PLAN.

Account for applicable situations including:

- Successful completion.
- Completion with warnings.
- Partial completion.
- Invalid configuration.
- Missing required inputs.
- Insufficient usable measurements.
- Numerical or computational failure.
- Interrupted analysis, if applicable.
- Operation-record persistence failure.

A failed or incomplete analysis must not be represented as a successful completed operation.

Retain relevant warnings, limitations, and error information according to the approved record design.

### Distinguish execution and persistence failures

An analysis failure and a persistence failure are different events.

The implementation must not imply that an analysis failed merely because its record could not be saved.

Likewise, it must not imply that results were successfully recorded when persistence failed.

Follow the approved PLAN for handling these situations, including what is communicated to the user and what information remains available.

Do not introduce new status categories or redesign the record model without approval.

---

## 7. Preserve project and dataset relationships

Each BLS operation record must remain associated with the correct project and dataset.

Support multiple analyses of the same dataset.

For example, analyzing the same dataset with different period ranges or transit-duration configurations must produce separate operation records.

Verify that:

- Each operation has its own identity.
- Repeated analyses do not overwrite earlier records.
- Different configurations remain distinguishable.
- Records retain their original project association.
- Historical dataset references follow the approved identity design.
- Replacing or moving a source file does not silently associate historical records with different data.

Use the approved Task 2.5.2 identity and relationship mechanisms.

---

## 8. Preserve existing application behavior

Keep changes focused on BLS operation recording.

The existing BLS calculation and result-display workflow must continue to function.

Preserve:

- Existing BLS parameters and defaults.
- Existing calculation behavior.
- Existing uncertainty calculations.
- Existing detection assessment.
- Existing warnings and limitations.
- Existing visualization and result presentation.
- Existing project lifecycle behavior.

Any UI modifications must be limited to what is necessary for correct operation recording and appropriate error reporting.

Do not implement a complete operation-history interface.

---

## 9. Testing and validation

Implement the tests identified in the approved PLAN.

Do not weaken or remove existing tests to make the implementation pass.

### A. Operation-record integration tests

Verify that:

- A BLS execution creates an operation record.
- The correct operation type is assigned.
- The correct project is associated.
- The correct dataset is associated.
- Multiple executions create independent records.
- Repeated analyses do not overwrite earlier records.

### B. Input and configuration tests

Verify that:

- The actual measurement selection is recorded.
- The correct uncertainty association is recorded.
- Time column and reference information are preserved.
- Actual BLS parameter values are recorded.
- Data preparation and exclusions are represented accurately.
- Missing metadata is not replaced with assumed values.

### C. Results integration tests

Verify that:

- Results are associated with the correct operation.
- Best-fit parameters are preserved.
- Periodogram and other structured outputs are serialized appropriately.
- Relevant uncertainty information is retained.
- Detection-assessment information is preserved.
- Warnings and limitations are retained.
- Serialization and retrieval do not silently lose relevant information.

### D. Failure-handling tests

Verify that:

- Invalid configurations are handled correctly.
- Missing required inputs are handled correctly.
- Insufficient usable data is handled correctly.
- Failed and incomplete operations are represented accurately.
- Persistence failures are reported appropriately.
- Failed operations are never represented as successful.
- Analysis failures and persistence failures are distinguishable.

### E. Persistence tests

Verify that:

- BLS operation records are saved through the approved persistence system.
- Records can be retrieved after closing and reopening a project.
- Multiple records remain independently retrievable.
- Historical parameters and results remain intact.
- Existing project and dataset information remains intact.

### F. Regression tests

Verify that existing functionality remains operational:

- Project creation, opening, saving, and closing.
- Dataset import and persistence.
- Light-curve visualization.
- BLS calculations.
- Uncertainty and detection-assessment behavior.
- Existing operation-record model and persistence behavior.

Use portable test fixtures and temporary directories.

Do not make automated tests depend on the user's absolute Kepler-10b dataset path.

Do not modify the original Kepler-10b FITS file.

Run targeted tests first, followed by the appropriate broader regression suite.

Report actual commands and results. Distinguish passed, failed, skipped, and unexecuted tests.

---

## 10. Documentation maintenance

Follow the documentation-maintenance requirements in `AGENTS.md`.

Before implementation, identify the documents affected by this task.

Update relevant documentation when the implementation changes or establishes:

- BLS operation-record integration.
- Input and provenance capture.
- BLS configuration capture.
- Result serialization and association.
- Operation status transitions.
- Failure and persistence error handling.
- Project and dataset relationships.
- Integration testing.
- Known limitations.

Update the appropriate architecture, module, data-flow, testing, decision, roadmap, and development-log documents as applicable.

Do not modify every document indiscriminately.

Keep a clear distinction between:

- Functionality implemented in the current code.
- Functionality reserved for Task 2.5.4.
- Functionality reserved for Task 2.5.5.
- Known limitations.
- Deferred architectural decisions.

Do not modify Foundation documents.

Do not mark Task 2.5.3 complete until implementation, tests, and documentation have been verified.

---

## 11. Explicit scope exclusions

Do not implement any of the following:

- Rebuilding the operation-record model.
- Redesigning project persistence.
- Creating a separate BLS persistence system.
- Building operation-history UI.
- Searching or filtering historical operations through the UI.
- Reconstructing or replaying historical operations.
- Automatically rerunning previous analyses.
- Adding new scientific analysis methods.
- Changing BLS scientific methodology.
- Introducing new preprocessing methods.
- Automating research workflows.
- Implementing permanent database architecture or migration.
- Adding new dependencies or frameworks without explicit approval.

**Task 2.5.4** is responsible for user-facing operation-history inspection.

**Task 2.5.5** is responsible for final Stage 2.5 testing, documentation, and completion verification.

### D6 storage constraint

Continue using the approved provisional persistence approach.

Do not introduce a permanent database, ORM, new persistence framework, or broad storage redesign.

If the approved integration cannot be implemented within the existing architecture and D6 constraints, stop and report the specific issue.

---

## 12. Git and change-safety requirements

- Do not commit changes.
- Do not push to GitHub.
- Do not reset, clean, or rewrite Git history.
- Do not discard existing user changes.
- Do not overwrite unrelated files.
- Do not perform broad refactoring outside the approved scope.
- Keep modifications limited to the files necessary for Task 2.5.3.

Before finishing, inspect the working tree and review the complete diff.

---

## 13. Required completion report

Provide a structured report containing the following sections.

### A. Implementation summary
Explain:
- How BLS execution now creates operation records.
- How the integration uses the Task 2.5.2 interfaces.
- How inputs, configuration, and results are captured.
- How records are associated with projects and datasets.

### B. Files changed
For every changed file, explain:
- What changed.
- Why the change was necessary.
- Whether it contains implementation, tests, or documentation.

### C. Input and provenance verification
Explain which actual analysis inputs are recorded and how original, prepared, and derived data are distinguished.

### D. Configuration and results verification
Explain how actual BLS parameters, results, uncertainty information, and detection-assessment information are preserved.

Identify any result information that is not persisted and explain why.

### E. Status and failure handling
Explain how successful, warning, partial, and failed operations are represented.

Explain how analysis failures are distinguished from persistence failures.

### F. Persistence verification
Explain how records are saved and retrieved, including after project reopening.

Identify any limitations resulting from the provisional D6 storage approach.

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
- No BLS scientific methodology was changed.
- No new scientific analysis method was introduced.
- No unauthorized preprocessing was added.
- No separate BLS persistence mechanism was created.
- No operation-history UI was implemented.
- No replay or automatic rerunning was implemented.
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

State whether Task 2.5.3 meets its completion criteria and is ready for review.

Do not declare the entire Stage 2.5 complete. Tasks 2.5.4 and 2.5.5 remain separate.

---

## 14. Final instruction

Implement only the explicitly approved Task 2.5.3 PLAN.

Prioritize scientific traceability, accurate provenance, data integrity, correct result association, and compatibility with the existing project architecture.

If the approved design proves incompatible with the current code, or implementation requires an unapproved architectural or scientific decision, stop and report the specific conflict.

Do not silently redesign around it.

When implementation and verification are complete, provide the required report and wait for the user's review before proceeding to Task 2.5.4.