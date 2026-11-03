# PLAN PROMPT

# Task 2.5.1 — Operation Record Design and Implementation Planning

## MODE: PLAN ONLY

You are working on the New_Project astronomy research application.

**Your task is to inspect the existing repository and produce a detailed design and implementation plan for Stage 2.5.1: Operation Record Design and Implementation Planning.**

This is an inspection and planning task only.

Do not implement anything. Do not modify source code, tests, documentation, configuration, dependencies, datasets, or Git state.

Stop after presenting your findings and proposed plan. Wait for explicit approval before any implementation.

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

The application is intended to support persistent research projects, imported astronomical datasets, scientific analysis, visualization, and traceable research operations.

### Stage 2 context

Stage 2's overall objective is:

> Project create/open/save; import one light-curve dataset; preserve original + provenance; table + light-curve visualization; one photometric operation (BLS) with uncertainty; record operation and parameters.

Stage 2.5 concerns recording scientific analysis operations and making their history inspectable within research projects.

The proposed Stage 2.5 task breakdown is:

| Task | Name |
|---|---|
| 2.5.1 | Operation Record Design and Implementation Planning |
| 2.5.2 | Operation Record Model and Persistence |
| 2.5.3 | Analysis Operation Recording and Results Integration |
| 2.5.4 | Operation History Inspection and Project Integration |
| 2.5.5 | Testing, Documentation, and Completion Verification |

Verify these task titles and boundaries against the actual roadmap. Do not silently change approved roadmap content.

### Important: Verify Stage 2.4

Stage 2.5 depends on the existing BLS analysis workflow.

Inspect the current repository and establish the actual implementation status of Stage 2.4, including:

- BLS search implementation.
- BLS result structures.
- Transit parameter uncertainty estimation.
- Detection assessment.
- False-alarm probability, if implemented.
- Application integration.
- Current tests and scientific validation evidence.

Do not assume Stage 2.4 is complete simply because earlier plans or reports describe it as complete.

Identify any incomplete, provisional, or missing functionality that affects the operation-record design.

Operation recording must accommodate what actually exists, not an imagined implementation.

---

## 2. Required Initial Inspection

Before developing the proposed design, inspect the governing project instructions and current repository.

### 2.1 Governance and Foundation

Read:

- Root `AGENTS.md`.
- Relevant Foundation documentation referenced by `AGENTS.md`.
- Existing project governance and approval requirements.

Foundation documentation is read-only.

Do not modify Foundation files, reinterpret Foundation requirements, or propose changes to Foundation as part of this task.

Pay particular attention to requirements concerning:

- Persistent research projects.
- Project and workspace separation.
- Local storage and data integrity.
- Data ownership and provenance.
- Scientific reproducibility.
- Uncertainty and scientific interpretation.
- Architecture decisions.
- Testing and quality assurance.
- Documentation maintenance.
- Research continuity.

### 2.2 Roadmap and Project Documentation

Inspect the actual current versions of relevant documentation, including:

- Development roadmap.
- Development log.
- Architecture documentation.
- Data models.
- Data flow.
- Module responsibilities.
- Validation and testing strategy.
- Architecture decision records.
- Project state and continuity documentation.
- Existing persistence documentation.

Use actual filenames and current content.

Do not assume filenames, document contents, or implementation status from previous conversations.

### 2.3 Source Code

Inspect the relevant implementation modules and identify:

- Project lifecycle and project identity.
- Project creation, opening, saving, and closing.
- Project persistence.
- Dataset import and validation.
- Dataset identity and source information.
- Dataset-to-project relationships.
- Light-curve data models.
- BLS implementation.
- Uncertainty estimation.
- Detection assessment.
- Analysis result structures.
- UI integration and result presentation.
- Existing error-handling patterns.
- Existing testing conventions.

Trace the actual data flow from project and dataset selection through analysis execution and result presentation.

Identify the modules and interfaces that an operation-record system would need to interact with.

Do not modify any files during inspection.

---

## 3. Design the General Operation Record

Propose a general operation-record structure suitable for retaining scientific operations performed within research projects.

Determine which fields should be shared by all operation types and which should be specific to individual analysis methods.

Evaluate the need for the following information:

### General identity and lifecycle

- Unique operation identifier.
- Operation type.
- Associated project identifier.
- Creation or execution timestamp.
- Operation status.
- Completion state.
- Relevant software version.
- Relevant method or algorithm version.
- Warnings.
- Errors.
- Limitations.

### Input provenance

- Dataset identifier.
- Original source filename or source reference.
- Source location, where appropriate.
- Selected measurement column.
- Selected uncertainty column.
- Other input columns.
- Relevant dataset metadata.
- Units.
- Time reference.
- Input selection details.

### Configuration

- Analysis method.
- Parameters.
- Search configuration.
- Explicit preprocessing.
- Quality filtering.
- Transformations.
- Other settings that materially affect the result.

### Results

- Structured results.
- Numerical outputs.
- Candidate results.
- Uncertainty estimates.
- Detection assessment.
- Warnings and limitations.
- References to associated result data, where appropriate.

For each proposed field or group of fields:

1. Explain why it is needed.
2. Determine whether it belongs in a shared record structure or a method-specific structure.
3. Identify whether the information already exists elsewhere in the application.
4. Explain whether it should be copied, referenced, or derived from existing data.
5. Identify any unresolved design questions.

Avoid unnecessary duplication of datasets or large result structures.

Do not design an unnecessarily complicated universal framework.

---

## 4. Design BLS-Specific Recording

The first supported operation type will be the existing BLS transit-search workflow.

Inspect the actual BLS implementation and its result structures.

Determine how the operation record should capture the following information where it is available.

### Inputs

- Project.
- Dataset.
- Selected flux measurement.
- Associated uncertainty measurement.
- Time information.
- Other required input data.

Pay particular attention to the relationship between:

- `PDCSAP_FLUX` and `PDCSAP_FLUX_ERR`.
- `SAP_FLUX` and `SAP_FLUX_ERR`.

The selected uncertainty measurement must correspond to the selected flux measurement.

### BLS configuration

- Period search range.
- Transit duration configuration.
- Search resolution.
- Frequency or period sampling.
- Other implemented BLS parameters.
- Explicit preparation or preprocessing.
- Quality filtering choices.
- Relevant method and software versions.

Record the actual configuration used, not merely the application's current defaults.

### BLS results

Inspect the actual returned result structures and determine how to retain:

- Periodogram information, where available.
- Candidate signals.
- Period.
- Transit epoch.
- Duration.
- Depth.
- BLS power.
- Other relevant numerical outputs.

Do not assume that all these outputs are currently implemented or retained. Identify what exists and what does not.

### Uncertainty and detection assessment

Determine how the operation record should retain uncertainty and detection information separately from the underlying BLS candidate results.

Inspect whether the implementation currently provides:

- Parameter uncertainty estimates.
- Uncertainty estimation method.
- Bootstrap or simulation settings.
- Random seeds.
- Null-model configuration.
- False-alarm probability.
- Detection assessment.
- Calibration information.
- Warnings and limitations.

Do not conflate:

- Candidate identification.
- Parameter uncertainty.
- Statistical detection significance.
- Planetary confirmation.

The record must not imply that identifying a BLS candidate establishes a confirmed planet.

### Partial completion and failure

Determine how the design should represent:

- Successful BLS search and successful uncertainty estimation.
- Successful BLS search but failed uncertainty estimation.
- Successful BLS search with incomplete detection assessment.
- Partial candidate results.
- An operation that fails before producing usable results.
- An operation that completes with warnings.

Recommend a status representation consistent with the existing application.

Do not introduce status complexity without a demonstrated need.

---

## 5. Design Operation Identity and Relationships

Determine how operation records should relate to:

- Research projects.
- Imported datasets.
- Analysis inputs.
- Analysis results.
- Other operation records, if relevant.

The design must support:

- Multiple operations within one project.
- Multiple operations on the same dataset.
- Different configurations applied to the same dataset.
- Different datasets analyzed within the same project.
- Historical results remaining distinguishable.
- Each operation retaining its own input selections and parameters.

Evaluate how the record should identify its original input if:

- A source file is moved.
- A source file becomes unavailable.
- A dataset is replaced.
- A dataset is re-imported.
- Dataset metadata changes.

Do not rely exclusively on mutable filenames or file paths as operation identity.

Inspect the existing identity mechanisms before proposing new identifiers or relationships.

Explain which relationships should use stable identifiers and which information should be retained as historical metadata.

---

## 6. Design Persistence and Project Integration

Inspect the current project persistence implementation.

The project has an approved provisional storage direction:

**D6 defers the permanent storage architecture. Provisional local file persistence is permitted for the initial vertical slice, with limitations documented.**

Verify the actual D6 decision record and its wording before making architectural recommendations.

The operation-record design must respect this decision.

Determine how operation records could be integrated into the existing persistence architecture.

Evaluate:

- Saving operation records.
- Loading records when a project is reopened.
- Retrieving multiple records.
- Retrieving an individual record by identifier.
- Maintaining project and dataset associations.
- Preserving historical records.
- Handling incomplete writes.
- Handling missing source datasets.
- Handling corrupted or incomplete records.
- Maintaining consistency between operation records and their results.
- Future schema evolution.

If the current persistence architecture creates limitations, document them.

Do not use this task to introduce:

- A permanent database architecture.
- An ORM.
- A new persistence framework.
- A new dependency.
- A broad storage redesign.

If an architectural change appears necessary, identify it as a separate decision requiring explicit approval.

Do not assume that the current persistence system can support every proposed feature without modification.

---

## 7. Design Operation Retrieval and Access

Establish the application-level interfaces needed to retrieve operation records.

Consider support for:

- Retrieving all operations associated with a project.
- Retrieving operations by type.
- Retrieving an operation by its identifier.
- Accessing operation inputs and configuration.
- Accessing results and uncertainty information.
- Accessing warnings and limitations.
- Identifying operation completion status.

Determine which responsibilities belong to:

- The operation-record model.
- Persistence.
- Analysis integration.
- The future user interface.

The detailed history interface belongs to Task 2.5.4.

Do not implement or fully design the history UI during this task.

---

## 8. Future Operation-Type Compatibility

BLS is the initial operation type.

The general record structure should allow reasonable future expansion to other scientific operations.

Consider potential future examples such as:

- Other transit-search methods.
- Periodic signal analysis.
- Light-curve preprocessing.
- Data-quality assessment.
- Other scientific analysis methods.

Explain how the proposed structure could accommodate these without requiring a complete redesign.

However:

- Do not implement future methods.
- Do not create a universal scientific workflow engine.
- Do not introduce abstractions without a current architectural justification.
- Do not allow hypothetical future functionality to unnecessarily complicate the initial BLS implementation.

Recommend the simplest design that satisfies the current requirements while preserving a reasonable extension path.

---

## 9. Scientific Integrity and Provenance

Evaluate the design against the project's scientific integrity requirements.

The proposed system must preserve the distinction between:

1. Original imported measurements.
2. Selected analysis inputs.
3. Prepared or transformed analysis inputs.
4. Analysis configuration.
5. Derived results.
6. Uncertainty estimates.
7. Detection assessment.

Ensure the design accounts for:

- Original measurements remaining unchanged.
- Correct flux and uncertainty associations.
- Accurate recording of input columns.
- Explicit preprocessing and filtering.
- Preservation of quality-filtering choices.
- Unknown metadata remaining unknown.
- Units and time references being retained.
- Historical records remaining distinguishable from current results.
- Results not being silently modified by later analyses.

Identify any existing architecture or implementation behavior that could undermine these requirements.

Do not propose silent data modification or automatic filtering.

---

## 10. Reproducibility Boundaries

Establish what information operation recording should preserve to support research traceability.

At minimum, evaluate the retention of:

- Dataset identity.
- Selected measurements.
- Uncertainty columns.
- Analysis method.
- Parameters.
- Configuration.
- Preprocessing and filtering.
- Relevant software and method versions.
- Results.
- Uncertainty estimates.
- Detection assessment.
- Warnings and limitations.
- Provenance information.

Clearly distinguish:

**Operation inspection:** Understanding what was performed and what results were produced.

**Reproducibility:** Retaining enough information to understand and independently reproduce an analysis.

**Operation replay:** Automatically reconstructing and rerunning a historical operation within the application.

Stage 2.5 establishes operation recording and inspection.

A complete replay engine, automatic reconstruction of historical workflows, and automatic rerunning of previous operations are outside scope.

Do not allow the proposed design to imply that replay is already supported.

---

## 11. Testing and Validation Plan

Design the testing strategy for subsequent implementation tasks.

Evaluate tests for:

### Record structure

- Record creation.
- Required fields.
- Optional fields.
- Unique identifiers.
- Valid operation types.
- Status representation.
- Parameter preservation.
- Result preservation.

### Relationships

- Project association.
- Dataset association.
- Multiple operations within one project.
- Multiple operations on one dataset.
- Different input selections.
- Historical record identity.

### Persistence

- Save and reopen.
- Retrieval by project.
- Retrieval by operation identifier.
- Multiple records.
- Missing datasets.
- Incomplete records.
- Corrupted records.
- Interrupted writes.
- Persistence compatibility.

### Scientific integrity

- Correct flux/uncertainty associations.
- Preservation of input selections.
- Preservation of configuration.
- Preservation of results.
- No modification of original measurements.
- Correct representation of missing metadata.
- Correct handling of partial operations and failures.

### Future compatibility

- Shared operation fields.
- Method-specific fields.
- Ability to represent a non-BLS operation in a future implementation without requiring a universal framework.

Use the existing testing conventions.

Automated tests must use portable fixtures and temporary directories.

**Do not make the standard test suite depend on the user's permanent Kepler-10b dataset or any machine-specific absolute path.**

Do not weaken existing tests to accommodate the new design.

---

## 12. Documentation Impact Assessment

Identify the documentation that should be updated during implementation.

Inspect actual documentation and determine whether the following need changes:

- Development roadmap.
- Development log.
- Architecture documentation.
- Data-model documentation.
- Data-flow documentation.
- Module responsibility documentation.
- Persistence documentation.
- Validation and testing documentation.
- Architecture decision records.
- Project state and continuity documentation.

For each document, explain:

1. Why it may need an update.
2. What information should be added or changed.
3. Which implementation task should make the update.

Do not modify any documentation during this planning task.

Foundation documentation must remain read-only.

Follow the documentation-maintenance requirements in `AGENTS.md`.

---

## 13. Establish Subsequent Task Boundaries

Review the proposed Stage 2.5 breakdown and recommend clear boundaries for the remaining tasks.

| Task | Intended responsibility |
|---|---|
| 2.5.2 — Operation Record Model and Persistence | Implement the approved record structure and project persistence. |
| 2.5.3 — Analysis Operation Recording and Results Integration | Connect the existing BLS workflow to operation recording. |
| 2.5.4 — Operation History Inspection and Project Integration | Provide user-facing inspection of historical operation records. |
| 2.5.5 — Testing, Documentation, and Completion Verification | Verify the complete Stage 2.5 implementation, scientific integrity, persistence, documentation, and regression behavior. |

Determine whether these boundaries are appropriate based on the actual repository.

If changes are recommended, explain why.

Do not implement any functionality belonging to these subsequent tasks.

---

## 14. Required PLAN Report

Present a detailed report with the following sections.

### A. Repository and Governance Findings

- Repository and branch context, as visible from the local environment.
- Relevant AGENTS.md requirements.
- Relevant Foundation requirements.
- Relevant architecture decisions.
- Documentation inspected.
- Any conflicts or missing governance information.

### B. Existing Architecture Findings

Describe the actual implementation of:

- Project lifecycle.
- Persistence.
- Dataset import and identity.
- Data models.
- BLS.
- Uncertainty.
- Detection assessment.
- Results.
- UI integration.
- Tests.

Identify exact relevant file paths and classes/functions where possible.

### C. Stage 2.4 Readiness Assessment

Provide a clear assessment of which Stage 2.4 capabilities exist, which are incomplete, and which are missing.

Explain how each finding affects the operation-record design.

Do not claim completion without supporting evidence.

### D. Proposed Operation Record Design

Present the recommended general record structure.

Include:

- Fields.
- Data types, where determinable.
- Required versus optional fields.
- Shared versus method-specific information.
- Identity and relationships.
- Status handling.
- Result references.
- Provenance.

Clearly distinguish verified existing structures from proposed new structures.

### E. BLS Recording Design

Explain how the actual BLS implementation and its associated uncertainty/detection results would be represented.

Identify missing or incomplete information that would prevent reliable recording.

### F. Persistence and Retrieval Design

Explain how the proposed design fits the current persistence architecture.

Identify limitations and any decisions requiring approval.

### G. Scientific Integrity and Reproducibility

Explain how the design preserves data integrity, provenance, historical results, and the distinction between inspection, reproducibility, and replay.

### H. Testing and Validation Plan

List the proposed tests, validation cases, portable fixture requirements, and regression concerns.

### I. Documentation Impact

Identify affected documentation, proposed changes, and the task responsible for each update.

### J. Subsequent Task Boundaries

Confirm or recommend boundaries for Tasks 2.5.2–2.5.5.

### K. Unresolved Questions and Decisions

List decisions that cannot be settled from existing architecture or approved requirements.

For each, identify:

- The question.
- Why it matters.
- Available options.
- Your recommendation.
- Whether explicit user approval is required.

Do not silently make architectural decisions on the user's behalf.

### L. Recommended Implementation Plan

Provide a practical, ordered implementation plan for Tasks 2.5.2–2.5.5.

Identify dependencies, sequencing, expected outputs, and verification points.

### M. Build Readiness Assessment

Conclude with one of:

- **Ready for approval:** The design is sufficiently grounded and no blocking decisions remain.
- **Ready after clarification:** The design is mostly complete but requires specific user decisions.
- **Not ready:** Important architectural or implementation information is missing.

Explain the conclusion.

Do not begin implementation regardless of the readiness assessment.

---

## 15. Strict Scope Restrictions

During this PLAN task, you must not:

- Modify source code.
- Create or modify tests.
- Modify documentation.
- Modify configuration files.
- Install or update dependencies.
- Create operation-record models.
- Implement persistence changes.
- Integrate BLS recording.
- Create an operation-history interface.
- Modify project data.
- Modify the permanent Kepler-10b FITS dataset.
- Modify Foundation documents.
- Commit, push, reset, clean, or otherwise alter Git history or state.
- Expand the project scope.
- Implement a replay engine.
- Make unapproved architecture decisions.

Do not use this task as an opportunity to refactor unrelated modules.

If you discover an unrelated issue, report it separately only if it materially affects the proposed design.

---

## 16. Final Instruction

Inspect the current repository thoroughly, ground every recommendation in verified implementation details, and produce the complete PLAN report.

Clearly distinguish:

- Verified facts.
- Existing implementation behavior.
- Proposed design.
- Recommendations.
- Assumptions.
- Unresolved questions.
- Decisions requiring approval.

Do not treat prior conversation summaries or earlier agent reports as proof of current repository state.

**PLAN ONLY. Make no changes. Stop after the report and wait for explicit approval before proceeding to BUILD.**



# BUILD PROMPT

# Task 2.5.1 — Operation Record Design and Implementation Planning

## MODE: BUILD

You are working on the New_Project astronomy research application.

**Your task is to complete the approved design and planning work for Stage 2.5.1: Operation Record Design and Implementation Planning.**

This task follows the completed PLAN phase.

You must use the user's approved PLAN report and any explicitly approved revisions as the authority for this BUILD task.

If the approved plan or required approval is not available, stop and request it. Do not infer approval from the existence of a plan or from this prompt.

This BUILD task authorizes the creation or updating of planning and design documentation only. It does not authorize implementation of the operation-record system.

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

The project supports persistent research projects, imported astronomical datasets, scientific analysis, visualization, and traceable research operations.

### Stage 2 objective

> Project create/open/save; import one light-curve dataset; preserve original + provenance; table + light-curve visualization; one photometric operation (BLS) with uncertainty; record operation and parameters.

### Stage 2.5 task breakdown

Verify the current roadmap and approved plan for the exact task names and boundaries.

The intended breakdown is:

| Task | Name |
|---|---|
| 2.5.1 | Operation Record Design and Implementation Planning |
| 2.5.2 | Operation Record Model and Persistence |
| 2.5.3 | Analysis Operation Recording and Results Integration |
| 2.5.4 | Operation History Inspection and Project Integration |
| 2.5.5 | Testing, Documentation, and Completion Verification |

Task 2.5.1 establishes the design and implementation plan for operation recording. The subsequent tasks implement and verify that design.

---

## 2. Required Pre-Build Verification

Before changing any documentation, inspect the current repository.

### 2.1 Confirm the approved plan

Locate and review:

- The completed Task 2.5.1 PLAN report.
- User-approved changes or clarifications.
- Any explicit approval conditions.
- The current Stage 2 roadmap.
- The current development log.

Confirm that the work you are about to perform matches the approved plan.

If the approved plan contains unresolved questions requiring user decisions, do not silently settle them. Follow the approved plan's instructions and preserve unresolved decisions in the documentation.

### 2.2 Review governing instructions

Read:

- Root `AGENTS.md`.
- Relevant Foundation documentation referenced by `AGENTS.md`.
- Applicable architecture decision records.
- Documentation-maintenance requirements.

Foundation documentation is read-only.

Do not modify Foundation documents or alter their requirements.

### 2.3 Verify actual implementation

Reinspect the relevant source code and tests before documenting architectural facts.

Verify the current state of:

- Project lifecycle.
- Project persistence.
- Dataset import and identity.
- Dataset-to-project associations.
- Light-curve data models.
- BLS search.
- Transit parameter uncertainty.
- Detection assessment.
- BLS result structures.
- Application integration.
- Existing testing and validation.

Pay particular attention to the actual Stage 2.4 implementation.

Do not copy unverified claims from earlier reports into the design documentation.

If the current implementation differs from the approved PLAN report, assess whether the difference affects the approved design.

Do not expand the task or make unapproved architecture changes. Document material discrepancies and request clarification if they prevent safe completion.

### 2.4 Verify current documentation

Identify the actual documentation files that are relevant to Task 2.5.1.

Do not assume filenames or create duplicate documents merely because a suggested filename differs from the repository's existing naming conventions.

Follow the repository's existing documentation organization unless the approved plan explicitly authorizes a change.

---

## 3. Complete the Operation Record Design

Create or update the approved design documentation to describe the proposed operation-record structure.

The documentation must distinguish between:

1. Existing functionality verified in the repository.
2. Proposed operation-record design.
3. Implementation details deferred to subsequent tasks.
4. Unresolved questions or decisions requiring approval.

### 3.1 General operation record

Document the proposed shared record structure.

Address:

- Unique operation identifier.
- Operation type.
- Associated project.
- Execution timestamp.
- Operation status.
- Completion state.
- Relevant software and method versions.
- Warnings.
- Errors.
- Limitations.
- Input provenance.
- Configuration and parameters.
- Results and result references.

For each proposed field, document:

- Purpose.
- Whether it is required or optional.
- Whether it is shared or method-specific.
- Whether it already exists in the application.
- Whether it should be stored directly or referenced.
- Any relevant constraints or unresolved questions.

Do not invent data types or implementation details that cannot be justified by the existing architecture or approved design.

Where a data type is proposed rather than verified, identify it as a proposal.

### 3.2 Input and provenance information

Document how an operation will identify and retain information about its inputs.

Include:

- Dataset identity.
- Source information.
- Selected measurement columns.
- Selected uncertainty columns.
- Other input columns.
- Units.
- Time references.
- Relevant metadata.
- Explicit preprocessing.
- Quality filtering.
- Transformations.

Explain how historical input information remains understandable if a source file is moved, replaced, or becomes unavailable.

Do not treat a mutable filename or path as sufficient dataset identity without justification.

### 3.3 Results and operation status

Document how results and operation status should be represented.

Include the distinction between:

- Successful operations.
- Partially successful operations.
- Failed operations.
- Operations completed with warnings.

Preserve meaningful partial results where appropriate.

Do not introduce unnecessary status complexity or claim that a proposed status mechanism already exists.

---

## 4. Complete the BLS-Specific Design

Document how the existing BLS workflow will be represented within the proposed operation-record system.

Ground the design in the actual BLS implementation.

### 4.1 Inputs

Document the required relationships between:

- Research project.
- Dataset.
- Selected flux measurement.
- Associated uncertainty measurement.
- Time information.
- Other relevant input data.

Preserve the correct associations:

- `PDCSAP_FLUX` with `PDCSAP_FLUX_ERR`.
- `SAP_FLUX` with `SAP_FLUX_ERR`.

Do not assume these are the only possible inputs without checking the actual implementation.

### 4.2 Parameters

Document how the record should retain the actual BLS configuration, including applicable:

- Period search range.
- Transit duration configuration.
- Search resolution.
- Frequency or period sampling.
- Other implemented parameters.
- Data preparation.
- Quality filtering.
- Method and software version information.

The design must explain why retaining the actual configuration is necessary rather than relying on application defaults at a later date.

### 4.3 Results

Document the BLS outputs that the actual implementation produces and how they will be represented in an operation record.

Consider:

- Periodogram information.
- Candidate signals.
- Period.
- Epoch.
- Duration.
- Depth.
- BLS power.
- Other relevant outputs.

Clearly distinguish currently implemented outputs from proposed future record fields.

### 4.4 Uncertainty and detection assessment

Document uncertainty estimation and detection assessment separately from BLS candidate identification.

Where implemented, address:

- Uncertainty method.
- Parameter uncertainty.
- Bootstrap or simulation configuration.
- Random seeds.
- Null-model configuration.
- False-alarm probability.
- Detection assessment.
- Calibration information.
- Warnings and limitations.

Preserve the scientific distinction between:

- Candidate identification.
- Parameter uncertainty.
- Statistical detection significance.
- Planetary confirmation.

Do not describe a BLS candidate as a confirmed planet.

### 4.5 Partial results and failures

Document how the proposed system should represent incomplete analysis stages.

Include cases such as:

- BLS succeeds but uncertainty estimation fails.
- BLS succeeds but detection assessment is incomplete.
- Candidate results are available but later processing fails.
- The operation fails before usable results are produced.
- The operation completes with warnings.

Ensure the proposed design does not discard useful results merely because a later stage fails.

---

## 5. Document Operation Identity and Relationships

Document the relationships between:

- Projects.
- Datasets.
- Operations.
- Analysis inputs.
- Results.

The design must explain how it supports:

- Multiple operations within one project.
- Multiple operations on the same dataset.
- Different configurations applied to the same dataset.
- Different datasets analyzed within one project.
- Historical results remaining distinguishable.
- Each operation retaining its own input selections and parameters.

Explain how operation identity and historical input information should be preserved if a dataset changes or becomes unavailable.

Identify any limitations in the current project or dataset identity mechanisms.

Do not implement new identity mechanisms during this task.

---

## 6. Document Persistence and Retrieval Design

Document how the proposed record structure will integrate with the existing project persistence architecture.

Respect the approved storage decision.

**D6 defers the permanent storage architecture and permits provisional local file persistence for the initial vertical slice, with limitations documented.**

Verify the exact decision record before referencing it.

The design must address:

- Saving operation records.
- Loading records when a project reopens.
- Retrieving multiple records.
- Retrieving a specific operation.
- Preserving project and dataset associations.
- Maintaining historical records.
- Handling incomplete writes.
- Handling missing source datasets.
- Handling corrupted or incomplete records.
- Maintaining consistency between records and results.
- Future schema evolution.

Clearly identify limitations of the current persistence architecture.

Do not implement persistence changes.

Do not introduce a permanent database architecture, ORM, new persistence framework, or new dependency.

Any proposed departure from approved storage decisions must remain an unresolved decision requiring explicit user approval.

---

## 7. Document Retrieval and Access Boundaries

Document the intended application-level retrieval capabilities:

- Retrieve all operations associated with a project.
- Retrieve operations by type.
- Retrieve an operation by identifier.
- Inspect inputs and parameters.
- Inspect results.
- Inspect uncertainty and detection information.
- Inspect warnings and limitations.
- Determine operation status.

Identify the responsibilities of:

- Operation-record model.
- Persistence layer.
- Analysis integration.
- User interface.

Keep the detailed history interface within Task 2.5.4.

Do not implement retrieval interfaces or user-facing history functionality in this task.

---

## 8. Document Future Compatibility

Explain how the proposed shared operation structure could accommodate future scientific operations.

Potential examples include:

- Other transit-search methods.
- Periodic signal analysis.
- Light-curve preprocessing.
- Data-quality assessment.
- Other scientific analysis methods.

Document a reasonable extension path without creating a universal workflow engine.

Do not implement future operation types or unnecessary abstractions.

The initial design should remain proportionate to the current BLS use case.

---

## 9. Document Scientific Integrity and Reproducibility

The design documentation must clearly preserve the distinction between:

1. Original imported measurements.
2. Selected analysis inputs.
3. Prepared or transformed data.
4. Analysis configuration.
5. Derived results.
6. Uncertainty estimates.
7. Detection assessment.

Document requirements for:

- Original measurements remaining unchanged.
- Correct measurement and uncertainty associations.
- Accurate recording of selected columns.
- Explicit preprocessing and filtering.
- Unknown metadata remaining unknown.
- Preservation of units and time references.
- Historical records remaining distinguishable.
- Results not being silently altered by later operations.

Also document the distinction between:

**Operation inspection:** Understanding what was performed and what it produced.

**Reproducibility:** Retaining enough information to understand and independently reproduce an analysis.

**Operation replay:** Automatically reconstructing and rerunning a historical operation within the application.

Stage 2.5 covers operation recording and inspection. A complete replay engine is outside scope.

Do not imply that recording an operation automatically makes it replayable.

---

## 10. Document the Testing and Validation Strategy

Establish the proposed tests for Tasks 2.5.2–2.5.5.

Cover:

- Record creation.
- Required and optional fields.
- Unique identifiers.
- Operation types and statuses.
- Project associations.
- Dataset associations.
- Multiple operations.
- Input and uncertainty references.
- Parameter preservation.
- Result preservation.
- Save and reopen.
- Retrieval by project and identifier.
- Missing datasets.
- Incomplete and corrupted records.
- Partial and failed operations.
- Historical record integrity.
- Persistence compatibility.
- Scientific data integrity.
- Future operation-type compatibility.

Testing documentation must follow existing repository conventions.

All standard automated tests must use portable fixtures and temporary directories.

They must not depend on the user's permanent Kepler-10b FITS dataset or machine-specific absolute paths.

Do not create or modify tests during Task 2.5.1.

Do not weaken existing tests.

---

## 11. Define Subsequent Task Boundaries

Document the approved implementation sequence.

### Task 2.5.2 — Operation Record Model and Persistence

Responsibility:

- Implement the approved record structure.
- Implement persistence within the approved architecture.
- Support project association and record retrieval.
- Verify model and persistence behavior.

### Task 2.5.3 — Analysis Operation Recording and Results Integration

Responsibility:

- Connect the existing BLS workflow to operation recording.
- Capture inputs, configuration, results, uncertainty, and detection information.
- Handle partial and failed operations appropriately.
- Preserve scientific provenance.

### Task 2.5.4 — Operation History Inspection and Project Integration

Responsibility:

- Provide the user-facing ability to inspect historical operation records.
- Integrate history access with the research project interface.
- Display relevant operation information and results.

### Task 2.5.5 — Testing, Documentation, and Completion Verification

Responsibility:

- Verify the complete Stage 2.5 implementation.
- Test persistence and retrieval.
- Validate scientific integrity and provenance.
- Verify integration and regression behavior.
- Complete documentation and assess Stage 2.5 completion.

Use the approved plan to refine these boundaries if necessary.

Do not implement any of these subsequent tasks.

---

## 12. Documentation Maintenance

Update the actual documentation files identified in the approved PLAN report.

Likely documentation areas include:

- Development roadmap.
- Development log.
- Architecture documentation.
- Data-model documentation.
- Data-flow documentation.
- Module responsibility documentation.
- Persistence documentation.
- Validation and testing documentation.
- Architecture decision records.
- Project state and continuity documentation.

Do not blindly update every document.

Only update documents where Task 2.5.1 materially changes or establishes information relevant to that document.

For every document changed:

1. Preserve existing structure and terminology.
2. Make focused additions or corrections.
3. Avoid duplicating existing content.
4. Distinguish proposed design from implemented functionality.
5. Identify unresolved decisions.
6. Keep progress and completion status accurate.

Do not mark Tasks 2.5.2–2.5.5 as complete.

Do not mark Stage 2.5 as complete.

Do not claim operation recording has been implemented.

### Documentation status

Update the roadmap and development log to reflect Task 2.5.1 accurately.

The status should indicate that the design/planning work has been completed only when the documentation and verification work is actually finished.

Any implementation work must remain assigned to its subsequent task.

Foundation documents remain read-only.

---

## 13. Verification Before Completion

After documentation updates, verify the resulting work.

### 13.1 Documentation consistency

Check that:

- The proposed record structure is internally consistent.
- General and BLS-specific fields are distinguishable.
- Existing implementation facts are accurate.
- Proposed features are not described as implemented.
- Persistence recommendations respect D6.
- Scientific integrity requirements are preserved.
- Reproducibility and replay are distinguished.
- Subsequent task boundaries are clear.
- Unresolved decisions remain visible.
- Roadmap and development log statuses are accurate.

### 13.2 Repository consistency

Verify that:

- Only approved documentation files were changed.
- No source code was modified.
- No tests were modified.
- No configuration or dependency files were modified.
- No datasets were changed.
- No Foundation documents were modified.
- No unrelated work was overwritten.

### 13.3 Tests

No new tests are authorized for this task.

If documentation changes do not affect executable behavior, a full test run is not automatically required.

If you believe a test run is useful, explain why. Do not modify code or tests to address unrelated failures.

Never claim tests passed unless they were actually executed and the results were observed.

### 13.4 Git review

Inspect the final Git diff and status.

Report:

- Files changed.
- Files added.
- Files deleted, if any.
- Untracked files, if any.
- Unrelated pre-existing modifications.
- Any unexpected changes.

Do not commit, push, reset, clean, or otherwise alter Git history or state.

Preserve all pre-existing user changes.

---

## 14. Scope Restrictions

This task does not authorize:

- Operation-record model implementation.
- Persistence implementation.
- BLS workflow integration.
- Operation-history UI implementation.
- New scientific analysis methods.
- Replay functionality.
- Database redesign.
- ORM introduction.
- New dependencies.
- Source-code refactoring.
- Test implementation.
- Changes to original research datasets.
- Changes to the permanent Kepler-10b FITS file.
- Foundation document changes.
- Git commits or pushes.
- Unrelated documentation rewrites.

If the approved plan reveals that an implementation change is necessary to complete Task 2.5.1, stop and explain the issue rather than silently expanding scope.

---

## 15. Required Final BUILD Report

When finished, provide a report containing the following sections.

### A. Task Completion Summary

- What planning and design work was completed.
- Whether Task 2.5.1 is complete.
- Any remaining limitations.

### B. Approved Plan Compliance

- How the work followed the approved PLAN report.
- Any deviations.
- Why deviations were necessary.
- Any decisions requiring further approval.

### C. Design Documentation

Summarize the documented:

- General operation-record structure.
- BLS-specific record design.
- Identity and relationships.
- Persistence and retrieval approach.
- Partial/failure handling.
- Future compatibility.
- Scientific integrity and provenance.
- Reproducibility boundaries.

### D. Documentation Changes

List each changed or created document and explain its purpose.

Also list important documents intentionally left unchanged and explain why.

### E. Verification Results

Report:

- Documentation consistency checks.
- Repository scope checks.
- Git status and diff review.
- Tests executed, if any, with actual results.
- Any remaining issues.

### F. Outstanding Decisions

List unresolved questions and decisions requiring user approval.

Do not conceal unresolved issues behind a completion claim.

### G. Subsequent Work

Summarize the approved scope and dependencies for Tasks 2.5.2–2.5.5.

### H. Final Status

Choose one:

- **Complete:** Task 2.5.1 documentation and planning work is complete and verified.
- **Complete with outstanding decisions:** The design is documented, but specific decisions remain for approval before subsequent implementation.
- **Incomplete:** Required design or documentation work remains.

Explain the selected status.

---

## 16. Final Instruction

Carry out only the approved Task 2.5.1 design and documentation work.

Use verified repository evidence. Preserve existing user work and project governance.

Do not implement the operation-record system.

Do not begin Task 2.5.2 or any later task.

Do not commit or push changes.

At completion, provide the full BUILD report and wait for the user's next instruction.