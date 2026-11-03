# PLAN PROMPT

# Task 2.5.2 — Operation Record Model and Persistence

## MODE: PLAN ONLY

You are working on the New_Project astronomy research application.

**Your task is to inspect the current repository and produce a detailed implementation plan for Task 2.5.2: Operation Record Model and Persistence.**

This task follows Task 2.5.1 — Operation Record Design and Implementation Planning.

The objective is to implement the approved operation-record data model and persistence foundation so that subsequent tasks can connect the existing BLS workflow to operation recording and provide user-facing operation history.

**This is a planning task only. Do not implement anything.**

Do not modify source code, tests, documentation, configuration, dependencies, datasets, or Git state.

Stop after presenting your findings and proposed implementation plan. Wait for explicit approval before proceeding to BUILD.

---

## 1. Project Context

Repository:

`C:\Code\New_Project`

GitHub:

`https://github.com/brettadin/New_Project`

The application is a local desktop astronomy research environment built with:

- Python 3.13
- PySide6
- NumPy
- SciPy
- Astropy
- Matplotlib (QtAgg)
- pytest

The project uses a local Python virtual environment.

### Stage 2 objective

> Project create/open/save; import one light-curve dataset; preserve original + provenance; table + light-curve visualization; one photometric operation (BLS) with uncertainty; record operation and parameters.

### Stage 2.5 task breakdown

Verify the current roadmap for the approved task names and boundaries.

The intended sequence is:

| Task | Name | Responsibility |
|---|---|---|
| 2.5.1 | Operation Record Design and Implementation Planning | Establish the approved operation-record design. |
| 2.5.2 | Operation Record Model and Persistence | Implement the approved model and persistence foundation. |
| 2.5.3 | Analysis Operation Recording and Results Integration | Connect the existing BLS workflow to operation recording. |
| 2.5.4 | Operation History Inspection and Project Integration | Provide user-facing operation-history inspection. |
| 2.5.5 | Testing, Documentation, and Completion Verification | Verify the complete Stage 2.5 implementation. |

Task 2.5.2 must not absorb responsibilities assigned to later tasks.

---

## 2. Required Initial Inspection

Before developing the implementation plan, inspect the actual repository.

### 2.1 Governance and approval

Read:

- Root `AGENTS.md`.
- Relevant Foundation documentation referenced by `AGENTS.md`.
- Applicable architecture decision records.
- Documentation-maintenance requirements.
- Current development roadmap and development log.

Foundation documents are read-only.

Do not modify Foundation requirements or propose changes to them as part of this task.

Confirm the required approval workflow and identify any restrictions relevant to implementation.

### 2.2 Task 2.5.1 design

Locate and inspect the completed Task 2.5.1 design documentation and its approved PLAN/BUILD findings.

Verify:

- General operation-record structure.
- Required and optional fields.
- Shared versus method-specific information.
- Operation identifiers.
- Project and dataset relationships.
- Operation status representation.
- Input and provenance requirements.
- Configuration and parameter representation.
- Results and result references.
- Persistence approach.
- Retrieval interfaces.
- Error and incomplete-record handling.
- Testing strategy.
- Documentation impact.
- Unresolved decisions.

**The approved Task 2.5.1 design is the authority for this task.**

Do not silently redesign it.

If the approved design is missing, incomplete, or contains unresolved decisions that block implementation planning, identify the issue and request clarification rather than guessing.

### 2.3 Existing project and persistence architecture

Inspect the current implementation of:

- Project creation.
- Project opening and closing.
- Project saving.
- Project identity.
- Project metadata.
- Dataset import and persistence.
- Dataset identity.
- Dataset-to-project associations.
- Existing file or metadata storage.
- Existing validation and error-handling patterns.

Trace how project and dataset information is currently stored and retrieved.

Identify the exact modules, classes, functions, and data structures that operation-record persistence would need to interact with.

### 2.4 Existing data models and analysis structures

Inspect:

- Light-curve data models.
- Dataset metadata structures.
- BLS result structures.
- Uncertainty result structures.
- Detection-assessment structures.
- Existing configuration or parameter representations.
- Existing serialization utilities, if any.

Do not assume the BLS implementation or its result structures have changed since previous tasks. Verify the current code.

Task 2.5.2 must provide a model capable of representing the approved design, but BLS workflow integration belongs to Task 2.5.3.

### 2.5 Existing tests

Inspect the current test structure and relevant tests for:

- Project persistence.
- Dataset persistence.
- Project lifecycle.
- Data models.
- Serialization.
- Error handling.
- Integrity.
- Regression behavior.

Determine how new operation-record tests should fit into the existing test organization.

Do not modify or execute tests as part of this PLAN task unless the user separately authorizes it.

---

## 3. Implementation Plan: General Operation Record Model

Develop a concrete implementation plan for the approved general operation-record model.

Use the approved Task 2.5.1 design to identify the actual fields and constraints.

For each proposed field or field group, specify:

- Field name.
- Proposed data type.
- Required or optional status.
- Default behavior, if applicable.
- Validation requirements.
- Whether the field is shared or method-specific.
- Whether it stores a value or references existing information.
- Any serialization considerations.

Distinguish verified existing project types and structures from proposed new structures.

### 3.1 Identity

Plan implementation of:

- Unique operation identifiers.
- Operation type.
- Project association.
- Creation or execution timestamp.
- Operation status.
- Completion information.

Determine how identifiers should be generated and validated using existing project conventions.

Consider duplicate identifiers and invalid identifiers.

Do not invent a new identifier convention if the approved design or existing architecture already establishes one.

### 3.2 Inputs and provenance

Plan the model representation for:

- Dataset identity.
- Source information.
- Selected measurement columns.
- Associated uncertainty columns.
- Other input columns.
- Units.
- Time references.
- Relevant metadata.
- Explicit preprocessing.
- Quality filtering.
- Transformations.

Determine which information should be preserved as a historical snapshot and which should reference existing project data.

Explain how records remain meaningful if the source dataset becomes unavailable.

### 3.3 Configuration and parameters

Plan how the model will preserve operation configuration.

Determine:

- How parameters are represented.
- How parameter values are validated.
- How optional parameters are handled.
- How actual values used by an operation are retained.
- How method-specific settings are separated from shared operation information.

Do not implement a universal configuration framework without an approved requirement.

### 3.4 Results and supporting information

Plan how the record will represent or reference:

- Structured results.
- Numerical outputs.
- Uncertainty information.
- Detection assessment information.
- Warnings.
- Errors.
- Limitations.
- Relevant software and method versions.

Determine whether results should be stored directly, referenced, or represented through a method-specific structure.

Avoid unnecessary duplication of large datasets or existing result structures.

### 3.5 Status and partial records

Plan the implementation of the approved status representation.

Consider how the model will validate:

- Successfully completed operations.
- Partially completed operations.
- Failed operations.
- Operations completed with warnings, where supported.

Determine which fields must exist for each status.

Do not assume all result sections must be present for an incomplete operation.

Do not introduce status categories that are not supported by the approved design.

---

## 4. Implementation Plan: Project and Dataset Relationships

Develop a concrete plan for linking operation records to research projects and datasets.

The implementation must support:

- Multiple operations within one project.
- Multiple operations using the same dataset.
- Different operations using different datasets.
- Different parameter configurations applied to the same dataset.
- Historical records remaining independently identifiable.

Inspect existing project and dataset identity mechanisms.

Determine:

- How project references will be validated.
- How dataset references will be validated.
- How missing datasets will be represented.
- Whether any historical metadata needs to be retained independently of the current dataset.
- How records will be prevented from becoming attached to the wrong project or dataset.

Do not implement a new project or dataset identity system unless explicitly authorized.

---

## 5. Implementation Plan: Persistence

Develop a concrete implementation plan for saving and loading operation records.

### 5.1 Storage decision

Verify the approved D6 decision.

D6 defers the permanent storage architecture and permits provisional local file persistence for the initial vertical slice, with limitations documented.

The implementation plan must respect this decision.

Do not introduce:

- A permanent database architecture.
- An ORM.
- A new persistence framework.
- Additional dependencies.
- Broad storage redesign.

If the existing architecture cannot support the approved design, identify the limitation and request approval before proposing a material departure.

### 5.2 Saving

Plan the implementation of:

- Saving one operation record.
- Saving multiple operation records within one project.
- Preserving unique identifiers.
- Preserving project and dataset associations.
- Preserving parameters and configuration.
- Preserving results and provenance.
- Validating records before persistence.

Determine how writes should interact with the existing project-save workflow.

### 5.3 Loading

Plan the implementation of:

- Loading operation records for an opened project.
- Retrieving multiple records.
- Retrieving an individual record by identifier.
- Validating loaded records.
- Handling missing or unavailable referenced data.
- Handling malformed or incomplete stored information.

### 5.4 Updates and historical integrity

Determine which fields are immutable after operation creation and which may be updated as an operation progresses.

The implementation must preserve historical input selections and configuration.

Updating a status or adding results must not silently replace the original analysis inputs or parameters.

Follow the approved design for partial records and operation lifecycle.

### 5.5 Error handling and integrity

Plan explicit handling for:

- Duplicate identifiers.
- Invalid identifiers.
- Invalid project associations.
- Invalid dataset references.
- Interrupted writes.
- Incomplete records.
- Corrupted stored data.
- Missing associated data.
- Serialization failures.
- Persistence failures.

Determine how errors should be reported to the calling application layer.

Do not silently discard existing project data or present invalid records as valid.

---

## 6. Retrieval Interfaces

Plan the underlying interfaces needed by Tasks 2.5.3 and 2.5.4.

The model and persistence layers should support the approved requirements for:

- Retrieving all records associated with a project.
- Retrieving a record by identifier.
- Retrieving records by operation type, if included in the approved design.
- Accessing input information.
- Accessing configuration and parameters.
- Accessing results and supporting information.
- Determining operation status.

For each proposed interface, identify:

- Its responsibility.
- Its expected inputs.
- Its expected outputs.
- Validation behavior.
- Error behavior.
- The module or layer where it belongs.

Keep the interfaces appropriately small.

Do not implement the BLS workflow integration or operation-history UI.

---

## 7. Serialization and Schema Evolution

Inspect the existing serialization approach.

Determine how the proposed record model will be converted into and restored from the existing persistence format.

Evaluate:

- Supported data types.
- Nested structures.
- Optional fields.
- Date and time representation.
- Numeric values.
- Missing values.
- Method-specific result structures.
- Serialization validation.
- Deserialization validation.
- Compatibility with existing project files.
- Future schema evolution.

The design should avoid making provisional storage decisions unnecessarily difficult to replace.

Do not introduce a new serialization dependency without approval.

If schema versioning is necessary, explain why and propose a minimal implementation consistent with the approved design.

---

## 8. Testing and Validation Plan

Develop a detailed test plan for the model and persistence implementation.

### 8.1 Model tests

Plan tests for:

- Valid record creation.
- Required fields.
- Optional fields.
- Unique identifiers.
- Invalid identifiers.
- Operation types.
- Status representation.
- Project associations.
- Dataset associations.
- Parameter preservation.
- Result preservation.
- Missing optional information.
- Invalid record handling.

### 8.2 Persistence tests

Plan tests for:

- Saving a record.
- Loading a saved record.
- Saving multiple records.
- Retrieving records by project.
- Retrieving records by identifier.
- Preserving information across project closure and reopening.
- Duplicate identifier handling.
- Missing associated datasets.
- Incomplete records.
- Corrupted records.
- Interrupted or failed writes.
- Serialization and deserialization.

### 8.3 Integrity tests

Plan tests verifying:

- Original measurements remain unchanged.
- Operation inputs remain associated with the correct dataset.
- Flux and uncertainty references remain correct.
- Configuration and parameters remain unchanged after persistence.
- Results remain unchanged after persistence.
- Historical records remain distinct.
- Unknown metadata is not invented.
- Unrelated project information is not altered.

### 8.4 Regression tests

Identify existing tests that may be affected by operation-record integration.

Plan to verify that:

- Project creation still works.
- Project opening still works.
- Project saving still works.
- Dataset import and persistence still work.
- Existing project metadata remains intact.
- Existing application behavior remains functional.

### 8.5 Portable test requirements

All standard automated tests must use portable fixtures and temporary directories.

They must not depend on:

- The user's permanent Kepler-10b FITS dataset.
- Machine-specific absolute paths.
- External services.
- Files outside the controlled test environment.

Do not weaken existing tests.

---

## 9. Documentation Impact Assessment

Identify which documentation files should be updated during BUILD.

Inspect the actual repository and identify relevant files, potentially including:

- Development roadmap.
- Development log.
- Data-model documentation.
- Architecture documentation.
- Data-flow documentation.
- Module responsibility documentation.
- Persistence documentation.
- Validation and testing documentation.
- Architecture decision records.
- Project state and continuity documentation.

For each document, explain:

1. Why an update is needed.
2. What implementation information should be documented.
3. Which changes should wait until Tasks 2.5.3–2.5.5.
4. Whether any document should intentionally remain unchanged.

Do not modify documentation during this PLAN task.

Foundation documents remain read-only.

Follow the documentation-maintenance requirements in `AGENTS.md`.

---

## 10. Subsequent Task Boundaries

Confirm that the proposed implementation plan preserves the boundaries between Tasks 2.5.2–2.5.5.

### Task 2.5.2 — Operation Record Model and Persistence

This task implements:

- General operation-record model.
- Approved operation fields and validation.
- Project and dataset associations.
- Operation status representation.
- Persistence.
- Serialization and deserialization.
- Retrieval interfaces.
- Model and persistence tests.
- Relevant documentation.

### Task 2.5.3 — Analysis Operation Recording and Results Integration

This task connects the existing BLS workflow to the operation-record system.

It must not need to redesign the model or persistence layer.

### Task 2.5.4 — Operation History Inspection and Project Integration

This task provides the user-facing ability to inspect historical operation records.

It must use the underlying interfaces established by Task 2.5.2.

### Task 2.5.5 — Testing, Documentation, and Completion Verification

This task verifies the complete Stage 2.5 implementation and its scientific integrity.

Do not move BLS recording, history UI, or full Stage 2.5 completion work into Task 2.5.2.

---

## 11. Required PLAN Report

Present a detailed report with the following sections.

### A. Repository and Governance Findings

- Repository and branch context.
- Relevant AGENTS.md requirements.
- Relevant Foundation requirements.
- Applicable architecture decisions.
- Documentation inspected.
- Approval requirements.
- Any governance conflicts.

### B. Task 2.5.1 Design Verification

Summarize the approved design.

Identify:

- Fields and structures to implement.
- Relationships.
- Persistence approach.
- Retrieval requirements.
- Validation requirements.
- Unresolved decisions.

Explain whether the approved design is sufficiently complete to implement.

### C. Existing Architecture Findings

Describe the actual implementation of:

- Project lifecycle.
- Project persistence.
- Dataset identity and associations.
- Data models.
- Serialization.
- Error handling.
- Testing conventions.

Identify exact file paths, classes, and functions where possible.

### D. Proposed Model Implementation

Present the proposed implementation structure.

Include:

- Modules and files expected to change.
- New classes or structures.
- Fields and types.
- Validation.
- Required and optional information.
- Status handling.
- Relationships.
- Serialization considerations.

Distinguish existing components from proposed additions.

### E. Proposed Persistence Implementation

Explain:

- Storage location and format.
- Save workflow.
- Load workflow.
- Retrieval interfaces.
- Update behavior.
- Error handling.
- Integrity safeguards.
- Schema evolution.
- Compatibility with current project persistence.
- D6 compliance.

### F. Testing Plan

List the planned model, persistence, integrity, and regression tests.

Identify existing test files to extend and any new test files that may be needed.

Explain how tests will remain portable.

### G. Documentation Plan

List the documents to update during BUILD and describe the intended changes.

### H. Implementation Sequence

Provide a practical ordered implementation sequence.

For each step, identify:

- Objective.
- Files or modules involved.
- Dependencies.
- Expected result.
- Verification method.

Keep the sequence focused on Task 2.5.2.

### I. Scope and Risk Assessment

Identify:

- Architectural risks.
- Persistence risks.
- Data-integrity risks.
- Serialization risks.
- Compatibility risks.
- Testing risks.
- Potential scope creep.

Explain how each risk will be controlled.

### J. Unresolved Questions and Decisions

List any issues requiring user clarification or explicit approval.

For each issue, provide:

- The question.
- Why it matters.
- Available options.
- Your recommendation.
- Whether implementation is blocked.

Do not silently settle architectural decisions.

### K. BUILD Readiness Assessment

Conclude with one of:

- **Ready for approval:** The implementation plan follows the approved design and no blocking decisions remain.
- **Ready after clarification:** The plan is substantially complete but needs specific user decisions.
- **Not ready:** Important design or repository information is missing.

Explain the conclusion.

Do not begin implementation.

---

## 12. Strict Scope Restrictions

During this PLAN task, you must not:

- Modify source code.
- Create or modify tests.
- Modify documentation.
- Modify configuration files.
- Install or update dependencies.
- Create operation-record models.
- Implement serialization.
- Implement persistence.
- Modify project lifecycle behavior.
- Modify dataset identity mechanisms.
- Integrate BLS operation recording.
- Create an operation-history interface.
- Modify original research data.
- Modify the permanent Kepler-10b FITS dataset.
- Modify Foundation documents.
- Commit, push, reset, clean, or otherwise alter Git history or state.
- Expand the project scope.
- Implement operation replay.
- Make unapproved architecture decisions.

Do not refactor unrelated modules.

If you discover an unrelated issue, report it separately only if it materially affects Task 2.5.2.

---

## 13. Final Instruction

Inspect the actual repository and the approved Task 2.5.1 design.

Produce a complete, implementation-ready plan for Task 2.5.2.

Ground every recommendation in verified repository evidence.

Clearly distinguish:

- Verified facts.
- Existing implementation behavior.
- Approved design requirements.
- Proposed implementation.
- Recommendations.
- Assumptions.
- Unresolved decisions.

Do not treat prior conversation summaries or earlier agent reports as proof of current repository state.

**PLAN ONLY. Make no changes. Stop after the report and wait for explicit approval before proceeding to BUILD.**



# BUILD PROMPT

# Task 2.5.2 — Operation Record Model and Persistence
## BUILD Prompt

**Mode: BUILD — implementation authorized only after explicit approval of the Task 2.5.2 PLAN.**

Implement Task 2.5.2 of Stage 2.5 in the New_Project repository.

The objective is to implement the approved operation-record model and its project-level persistence foundation. This work must follow the approved Task 2.5.1 design and the explicitly approved Task 2.5.2 PLAN.

Do not independently redesign the architecture or expand the task's scope.

---

## 1. Mandatory pre-implementation checks

Before modifying anything:

1. Read the repository's `AGENTS.md` and follow its instructions.
2. Respect the Foundation documentation and its read-only requirement.
3. Inspect the current Stage 2 roadmap and development log.
4. Review the approved Task 2.5.1 design documentation.
5. Review the approved Task 2.5.2 PLAN and verify that it has received explicit user approval.
6. Inspect the current repository state, including:
   - Project lifecycle and project metadata.
   - Existing persistence and serialization.
   - Dataset models and dataset identity.
   - BLS analysis implementation and result structures.
   - Uncertainty and detection-assessment information.
   - Existing tests and test fixtures.
   - Documentation identified by the approved plan.

**If the approved Task 2.5.2 PLAN or explicit approval is missing, stop. Do not implement anything.**

Do not assume the repository is unchanged since planning. Verify the current implementation before editing.

Identify existing user changes and preserve them. Do not overwrite or revert unrelated work.

---

## 2. Implementation scope

Implement only the operation-record model and persistence foundation described in the approved plan.

The implementation must support the approved design for:

- Operation record identity.
- Association with the relevant research project.
- Association with one or more relevant input datasets, as specified by the approved design.
- Operation type and identifying information.
- Operation status and completion information.
- Creation and relevant execution timestamps.
- Input measurement and uncertainty-column references.
- Relevant dataset and source metadata.
- Operation configuration and parameters.
- Analysis results and associated uncertainty information.
- Warnings, limitations, and errors.
- Relevant software and method information.
- Historical retrieval after a project is reopened.

Use the exact field definitions, relationships, validation rules, and serialization decisions established by the approved design and plan.

Do not introduce fields, requirements, or abstractions simply because they might be useful in the future.

### Record integrity

Operation records must preserve the information necessary to understand what was performed and what information was used.

In particular:

- Preserve the distinction between original, prepared, and derived data.
- Preserve the association between measurements and their uncertainty information.
- Retain relevant units, time references, and available metadata.
- Preserve the actual configuration and parameter values used.
- Do not silently replace missing or unknown metadata with assumed values.
- Do not modify original imported datasets when creating or saving operation records.
- Do not introduce automatic filtering, normalization, detrending, or other preprocessing.

Follow the approved plan for how input datasets are referenced and how historical records behave if an original source file is moved, unavailable, or replaced.

### Operation status

Implement the status model specified in the approved plan.

Where supported by that design, records must be able to represent successful, partially completed, and failed operations without misrepresenting incomplete results as successful results.

Preserve warnings and error information as specified by the design.

Do not invent additional status categories without approval.

---

## 3. Persistence requirements

Implement persistence using the existing project architecture and the approach approved in the Task 2.5.2 PLAN.

The implementation must support:

- Saving operation records to the appropriate project.
- Loading operation records when a project is reopened.
- Retrieving multiple records from the same project.
- Retrieving records associated with a particular dataset or operation, where specified by the approved design.
- Preserving record identity and relationships.
- Handling missing, malformed, or incompatible persisted records safely.
- Avoiding accidental loss or corruption of existing project information.

Follow the approved plan for serialization, validation, update behavior, and error handling.

### Important: D6 storage constraint

The existing D6 decision defers the formal permanent storage architecture. Provisional local file persistence is permitted for the initial implementation.

Therefore:

- Do not introduce a permanent database architecture.
- Do not add an ORM or a new persistence framework.
- Do not introduce new dependencies unless the approved plan explicitly establishes that they are necessary and the user has approved the change.
- Do not redesign project storage.
- Do not replace existing project persistence mechanisms.
- Do not treat this implementation as the final storage architecture.

Document any limitations of the provisional persistence approach.

If implementation appears to require a change beyond D6 or the approved plan, stop and report the issue rather than making that change independently.

---

## 4. Retrieval interfaces

Implement the retrieval interfaces identified in the approved plan.

These interfaces must provide a reliable foundation for later tasks:

- **Task 2.5.3:** Connecting the BLS analysis workflow to operation records.
- **Task 2.5.4:** Presenting and inspecting operation history in the application.

Do not build those later features as part of this task.

Keep the model and persistence interfaces sufficiently clear and documented that later work can use them without bypassing the record system or directly manipulating persisted files.

Do not build a universal operation framework or introduce unnecessary abstraction.

---

## 5. Testing and validation

Implement the tests specified in the approved plan.

At minimum, verify the applicable behavior for:

### Model tests
- Valid operation-record creation.
- Required and optional fields.
- Field validation.
- Record identity.
- Project and dataset associations.
- Operation status handling.
- Preservation of parameters, results, warnings, and limitations.
- Handling of incomplete or failed records, where supported.

### Persistence tests
- Saving records.
- Loading records.
- Saving and retrieving multiple records in one project.
- Preserving record identity and relationships.
- Retrieving records after closing and reopening a project.
- Handling missing or malformed persisted data.
- Handling missing source files according to the approved design.
- Preventing unintended modification of existing project data.

### Regression tests
- Existing project lifecycle behavior remains functional.
- Existing dataset import and persistence behavior remains functional.
- Existing BLS analysis behavior remains functional.
- Existing visualization and other completed Stage 2 functionality remains functional.

Use temporary directories and portable test fixtures.

**Do not make automated tests depend on the user's absolute Kepler-10b dataset path.** Do not modify the original research FITS file.

Do not weaken, delete, skip, or rewrite existing tests merely to make the suite pass.

Run the targeted tests first, followed by the appropriate broader regression suite.

Report actual commands and results. Distinguish tests that passed, failed, were skipped, or could not be run.

---

## 6. Documentation maintenance

Follow the documentation-maintenance requirements in `AGENTS.md`.

Before implementation, identify the documents affected by this task.

Update relevant documentation when the implementation changes or establishes:

- Operation-record model definitions.
- Persistence behavior.
- Serialization and validation.
- Project and dataset relationships.
- Retrieval interfaces.
- Error handling and limitations.
- Testing coverage.
- Development progress.

Update the appropriate architecture, module, data-model, testing, decision, roadmap, and development-log documents as applicable.

Do not update every document indiscriminately. Only change documents that are genuinely affected.

Keep the distinction between:

- Functionality implemented in the current code.
- Functionality planned for later tasks.
- Known limitations.
- Deferred architectural decisions.

Do not mark Task 2.5.2 complete until implementation, tests, and documentation have been verified.

Do not modify Foundation documents.

---

## 7. Explicit exclusions

The following are outside Task 2.5.2 and must not be implemented:

- Automatic BLS operation recording or workflow integration. This belongs to Task 2.5.3.
- Operation-history user interface or history inspection screens. This belongs to Task 2.5.4.
- Automatic reconstruction or replay of historical operations.
- Automatic rerunning of previous analyses.
- Workflow automation.
- New scientific analysis methods.
- New preprocessing or data-transformation methods.
- Permanent storage architecture or database migration.
- Multi-user accounts, permissions infrastructure, or cloud synchronization.
- New dependencies or frameworks not authorized by the approved plan.

The record model should support future extension where the approved design requires it, but do not implement future functionality prematurely.

---

## 8. Git and change-safety requirements

- Do not commit changes.
- Do not push to GitHub.
- Do not reset, clean, or rewrite Git history.
- Do not discard existing user changes.
- Do not overwrite unrelated files.
- Do not perform broad refactoring outside the approved scope.
- Keep modifications limited to the files necessary for Task 2.5.2.

Before finishing, inspect the working tree and review the complete diff.

---

## 9. Required completion report

Provide a structured report containing:

### A. Implementation summary
- What was implemented.
- How the operation-record model is structured.
- How records relate to projects and datasets.
- How persistence works.

### B. Files changed
For every changed file, explain:
- What changed.
- Why the change was necessary.
- Whether it contains implementation, tests, or documentation.

### C. Persistence verification
Explain how records are saved, loaded, associated with projects, and retrieved after reopening.

Identify any limitations resulting from the provisional D6 storage approach.

### D. Testing results
Report:
- Exact test commands.
- Number of passed, failed, and skipped tests.
- Any failures and their causes.
- Any tests that could not be run.
- Regression-test results.

Do not report tests as passing unless they were actually executed successfully.

### E. Documentation updates
List:
- Documents updated and why.
- Relevant documents inspected but intentionally left unchanged.
- Any remaining documentation gaps.

### F. Scope verification
Explicitly confirm that:
- BLS workflow integration was not implemented.
- Operation-history UI was not implemented.
- Replay and automatic rerunning were not implemented.
- No permanent storage redesign was introduced.
- No Foundation documents were modified.
- No unauthorized dependencies or frameworks were added.

### G. Git and working-tree status
Report:
- Modified and untracked files.
- Whether pre-existing user changes were preserved.
- Whether the final diff was inspected.
- Confirm that no commit or push was performed.

### H. Remaining issues and readiness
Identify unresolved issues, limitations, or decisions requiring user attention.

State whether Task 2.5.2 meets its completion criteria and is ready for review.

Do not declare the entire Stage 2.5 complete. Tasks 2.5.3, 2.5.4, and 2.5.5 remain separate.

---

## 10. Final instruction

Implement only the approved Task 2.5.2 plan.

Prioritize scientific traceability, data integrity, compatibility with the existing project architecture, and clear interfaces for later tasks.

If the approved design proves incompatible with the current code, or implementation requires an unapproved architectural decision, stop and report the specific conflict. Do not silently redesign around it.

When implementation and verification are complete, provide the required report and wait for the user's review before proceeding to Task 2.5.3.