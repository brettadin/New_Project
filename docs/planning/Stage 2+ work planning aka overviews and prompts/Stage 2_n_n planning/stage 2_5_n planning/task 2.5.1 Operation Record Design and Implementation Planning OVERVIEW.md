# Task 2.5.1 — Operation Record Design and Implementation Planning

## 1. Purpose

The purpose of Task 2.5.1 is to inspect the existing New_Project application architecture and establish a detailed design and implementation plan for recording scientific analysis operations within research projects.

The application currently performs scientific work on imported datasets and produces analysis results. However, retaining only the latest displayed result is insufficient for a research environment. The application needs a structured way to preserve what operation was performed, which data it used, which parameters were applied, and what results and limitations were produced.

This task establishes the design for that capability before implementation begins.

This is a planning and design task only. No application functionality, source code, tests, or documentation should be modified during this task. Implementation will follow in subsequent tasks after the design has been reviewed and approved.

## 2. Review the Existing Application Architecture

Before proposing a design, inspect the actual repository and determine how the application currently handles:

- Research project creation, opening, saving, closing, and lifecycle management.
- Project metadata and persistence.
- Imported light-curve datasets and their project associations.
- Dataset identity and source-file information.
- Light-curve data models and measurement columns.
- BLS transit-search implementation.
- Transit parameter uncertainty estimation.
- Detection assessment and false-alarm probability calculations, where implemented.
- Analysis results and their current data structures.
- Application interfaces that display analysis results.
- Existing documentation, architecture decisions, and testing conventions.

The design must build on the architecture that actually exists.

Do not assume that a feature is implemented simply because it appears in the roadmap or an earlier task report. Verify the current implementation and distinguish completed functionality from incomplete or provisional functionality.

Identify existing models, modules, interfaces, and persistence mechanisms that could support operation recording. Avoid introducing new abstractions where existing ones can reasonably be extended.

## 3. Define the Operation Record

Establish a proposed structure for an operation record that captures the information necessary to understand and trace a scientific operation performed within a research project.

The design should consider the following information.

### 3.1 General operation information

- Unique operation identifier.
- Operation type.
- Associated research project.
- Date and time the operation was performed.
- Operation status or completion state.
- Relevant software and method version information.
- Any applicable warnings, limitations, or error information.

### 3.2 Input dataset information

- Identity of the dataset used.
- Dataset source and original filename, where available.
- Association with the research project.
- Selected measurement or flux column.
- Associated uncertainty column, if applicable.
- Other input columns used by the operation.
- Relevant dataset metadata, units, and time references.
- Information needed to distinguish the original dataset from any prepared or derived inputs.

### 3.3 Operation configuration and parameters

- Analysis method.
- User-selected parameters.
- Default parameters that materially affect the result.
- Search ranges and resolution settings.
- Any relevant algorithm configuration.
- Explicit preprocessing or preparation settings.
- Quality filtering choices.
- Other transformations or selections applied to the input data.

The record should preserve the actual configuration used, rather than relying on whatever defaults or application settings exist when the record is later inspected.

### 3.4 Results

- Structured operation results.
- Relevant numerical measurements.
- Candidate results, where applicable.
- Associated uncertainty estimates.
- Detection assessment information, where applicable.
- Warnings and limitations associated with the results.
- Any relevant references to supporting result data.

Determine which information should be shared across all operation types and which belongs specifically to an individual analysis method.

The design should avoid unnecessarily duplicating large datasets or result structures when references to existing project data are sufficient.

## 4. Design BLS-Specific Operation Recording

The first operation type to be recorded will be the existing BLS transit-search workflow.

The design must account for the actual BLS implementation and its existing result structures.

Consider how the operation record will preserve:

### 4.1 BLS inputs

- Research project.
- Selected light-curve dataset.
- Selected flux measurement, such as PDCSAP_FLUX or SAP_FLUX.
- Correct associated uncertainty measurement.
- Relevant time information.
- Any other input data required by the implemented method.

### 4.2 BLS configuration

- Period search range.
- Transit duration configuration.
- Search resolution or frequency settings.
- Other implemented BLS parameters.
- Any explicit data preparation.
- Quality filtering choices.
- Relevant method and software version information.

### 4.3 BLS results

- Periodogram information, where retained.
- Identified candidate signals.
- Candidate period.
- Transit epoch.
- Transit duration.
- Transit depth.
- BLS power.
- Other values returned by the actual implementation.

### 4.4 Uncertainty and detection assessment

Preserve uncertainty estimation and detection assessment as distinguishable parts of the operation record.

Where implemented, consider recording:

- Uncertainty estimation method.
- Estimated parameter uncertainties.
- Simulation or bootstrap configuration.
- Random seeds, where applicable.
- Null-model configuration.
- False-alarm probability.
- Detection assessment results.
- Relevant calibration information.
- Known limitations and warnings.

Do not treat BLS candidate identification, parameter uncertainty, and detection significance as interchangeable concepts.

The record must preserve what the analysis actually established without implying that a candidate is a confirmed planet.

### 4.5 Partial results and failures

Determine how the record should represent cases where:

- BLS completes successfully but uncertainty estimation fails.
- BLS completes but detection assessment is incomplete.
- Some candidates are available while other processing steps fail.
- An operation terminates before producing usable results.
- An operation completes with warnings or limitations.

A failed or incomplete operation should not silently disappear if meaningful information about the attempt needs to be retained.

The design should distinguish successful completion, partial completion, and failure without inventing statuses that are inconsistent with the existing application architecture.

## 5. Operation Identity and Relationships

Determine how operation records will relate to research projects, datasets, and analysis results.

The design must support:

- Multiple operations within one research project.
- Multiple operations performed on the same dataset.
- Different operations performed on different datasets within the same project.
- Multiple BLS searches using different parameters.
- Historical results remaining distinguishable from the most recent results.
- Each operation retaining its own input selections and configuration.

Consider how operation records will identify their original inputs if a dataset is later replaced, moved, or becomes unavailable.

The design should avoid relying exclusively on a mutable filename or file path as the identity of an analysis input.

Determine which relationships should use stable identifiers and which information should be preserved as historical metadata.

## 6. Persistence and Project Integration

Determine how operation records will be saved as part of the existing research project structure.

Inspect the current project persistence implementation and identify the most appropriate integration point.

The design should address:

- Saving operation records.
- Loading operation records when a project is reopened.
- Retrieving multiple operations for one project.
- Retrieving a specific operation by its identifier.
- Maintaining dataset and project associations.
- Preserving records across application restarts.
- Handling incomplete or interrupted writes.
- Handling missing source files.
- Handling incomplete or corrupted records.
- Maintaining consistency between operation records and their associated results.
- Potential future schema evolution.

Respect the existing approved storage decisions.

In particular, the project's formal storage architecture was deferred under DEC-005/DEC-006? Do not reinterpret or change existing decision identifiers. Verify the actual decision records before referencing them. The relevant approved decision is D6: permanent storage architecture is deferred, and provisional local file persistence is permitted for the initial vertical slice, with limitations documented.

Do not use this task to introduce a permanent database architecture, ORM, new persistence framework, or additional dependency.

If the current persistence mechanism creates limitations, document them and explain their implications for the proposed operation-record design.

Any change to the approved storage direction must be identified as a decision requiring separate approval.

## 7. Operation Retrieval and Access

Establish the application-level boundaries for retrieving operation records.

The design should support future functionality to:

- Retrieve all operation records associated with a research project.
- Retrieve records by operation type.
- Retrieve an individual operation by its unique identifier.
- Inspect the inputs and configuration associated with an operation.
- Inspect its results, uncertainty information, and limitations.
- Distinguish completed, partially completed, and failed operations.

Determine what functionality should belong to the underlying record and persistence layers versus the future user interface.

The detailed operation-history interface belongs to Task 2.5.4 and should not be implemented or fully designed here.

## 8. Future Compatibility

Although BLS is the first operation type, the record design should not make the entire system dependent on BLS-specific fields.

Consider how the general operation structure could eventually accommodate other scientific operations without requiring a complete redesign.

Potential future operation types may include:

- Other transit-search methods.
- Periodic signal analysis.
- Light-curve preprocessing.
- Data-quality assessment.
- Other scientific analysis methods.

The design should establish a reasonable extension path while remaining appropriate for the current application.

Do not build a universal analysis framework or implement future analysis methods as part of this task.

## 9. Scientific Integrity and Provenance

Operation recording must preserve the distinction between original research data, analysis inputs, processing, and derived results.

The design should ensure that:

- Original imported measurements remain unchanged.
- Analysis inputs can be identified.
- Selected measurement columns are recorded accurately.
- Associated uncertainty measurements remain correctly identified.
- Preprocessing and transformations are recorded when applied.
- Quality filtering is recorded accurately.
- Unknown metadata remains unknown rather than being inferred.
- Units and time references are preserved.
- Derived results remain distinguishable from original measurements.
- Historical records do not silently change when the application is updated or new analyses are performed.

The record must provide sufficient provenance to understand how the results were obtained.

It should not imply that an operation can be automatically reproduced simply because its parameters and results were retained.

## 10. Reproducibility Boundaries

Establish what operation recording is expected to preserve for future research reproducibility.

At minimum, the design should consider retaining:

- Input dataset identity.
- Selected measurements and uncertainty columns.
- Analysis method.
- Parameters and configuration.
- Explicit preprocessing and filtering.
- Relevant software and method versions.
- Results.
- Uncertainty estimates.
- Detection assessment information.
- Warnings and limitations.
- Relevant provenance information.

Clearly distinguish between:

1. Operation inspection: understanding what was performed and what it produced.
2. Operation reproducibility: having sufficient information to understand and independently reproduce the analysis.
3. Operation replay: automatically reconstructing and rerunning a historical operation within the application.

The scope of Stage 2.5 is to establish operation recording and inspection.

A complete analysis-replay engine, automatic reconstruction of historical workflows, and automatic rerunning of previous operations are explicitly outside this task.

## 11. Testing and Validation Design

Establish how the proposed operation-record system should be tested in subsequent tasks.

Consider tests for:

- Operation record creation.
- Required and optional fields.
- Unique operation identifiers.
- Project associations.
- Dataset associations.
- Input measurement and uncertainty references.
- Parameter preservation.
- Result preservation.
- Multiple operations within one project.
- Multiple operations associated with one dataset.
- Save and reopen behavior.
- Retrieval by project and operation identifier.
- Missing or unavailable source datasets.
- Partial and failed operations.
- Incomplete or corrupted records.
- Historical record integrity.
- Compatibility with existing project persistence.
- Future operation-type extensibility.

Testing should follow the existing project conventions.

Use portable test fixtures and temporary data locations. Standard automated tests must not depend on the user's permanent Kepler-10b dataset or any other machine-specific absolute path.

Testing should verify that operation recording does not modify original scientific measurements.

## 12. Documentation and Architecture Decisions

Identify which existing documentation will need to change during implementation.

Review the actual documentation structure and determine whether updates will be needed to:

- Development roadmap.
- Development log.
- Architecture documentation.
- Data-model documentation.
- Data-flow documentation.
- Module responsibility documentation.
- Persistence documentation.
- Validation and testing documentation.
- Architecture decision records.
- Project-state and continuity documentation.

Do not modify documentation during this planning task.

Identify any architectural choices that require explicit approval before implementation.

Foundation documents remain read-only.

## 13. Implementation Boundaries for Subsequent Tasks

The design should establish clear responsibilities for the remaining Stage 2.5 tasks.

| Task                                                         | Responsibility                                                                                                           |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| 2.5.2 — Operation Record Model and Persistence               | Implement the approved operation-record structure and project persistence.                                               |
| 2.5.3 — Analysis Operation Recording and Results Integration | Connect the existing BLS workflow to the operation-record system.                                                        |
| 2.5.4 — Operation History Inspection and Project Integration | Provide the user-facing ability to inspect historical operation records.                                                 |
| 2.5.5 — Testing, Documentation, and Completion Verification  | Verify the complete Stage 2.5 implementation, scientific integrity, persistence, documentation, and regression behavior. |

Refine these boundaries if inspection reveals that the current architecture requires a different division of work.

Do not implement functionality belonging to subsequent tasks during 2.5.1.

## 14. Expected Outcome

At the end of Task 2.5.1, there should be a reviewed design and implementation plan that establishes:

1. The actual existing architecture relevant to operation recording.
2. The proposed general operation-record structure.
3. The BLS-specific information that must be retained.
4. The relationships between projects, datasets, operations, and results.
5. The persistence and retrieval approach.
6. The handling of incomplete, failed, and partially successful operations.
7. The scientific integrity and provenance requirements.
8. The distinction between operation inspection, reproducibility, and replay.
9. The testing and validation strategy.
10. The documentation updates expected during implementation.
11. The implementation boundaries for Tasks 2.5.2–2.5.5.
12. Any unresolved decisions requiring approval.

The resulting plan must be grounded in the current repository and approved project decisions.

Task 2.5.1 is complete only when the design has been documented, reviewed, and approved. No implementation should begin until that approval is given.