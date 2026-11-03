# Task 2.5.2 — Operation Record Model and Persistence

Suggested filename: `task 2.5.2 Operation Record Model and Persistence OVERVIEW.md`

## 1. Purpose

The purpose of Task 2.5.2 is to implement the operation-record data model and its persistence mechanism within New_Project.

Task 2.5.1 establishes the design for recording scientific analysis operations. Task 2.5.2 takes that approved design and turns it into working application functionality.

The application needs to retain more than the latest analysis result. It needs a structured way to save information about individual operations, associate them with research projects and datasets, and retrieve them after a project is closed and reopened.

This task establishes the underlying infrastructure that subsequent tasks will use to record BLS analyses and display operation history.

The primary objective is to make operation records persist reliably as part of a research project without compromising existing project data or scientific provenance.

## 2. Scope and Relationship to Task 2.5.1

Implementation must follow the design approved during Task 2.5.1.

Before implementation begins, the approved design must establish:

- General operation-record structure.
- Required and optional fields.
- Operation identifiers.
- Project and dataset relationships.
- Operation status representation.
- Result and input references.
- Persistence approach.
- Retrieval interfaces.
- Error-handling expectations.
- Scientific integrity and provenance requirements.

The approved design is the authority for implementation.

Do not independently redesign the record structure or introduce new architectural decisions simply because another approach appears more convenient.

If implementation reveals that the approved design cannot be followed because of an existing architectural limitation, document the issue and request clarification or approval before making a material design change.

## 3. Operation Record Data Model

Implement the general operation-record model established in Task 2.5.1.

The model should provide a consistent representation of scientific operations performed within a research project.

Depending on the approved design, the model should account for:

### 3.1 Operation identity

- Unique operation identifier.
- Operation type.
- Associated research project.
- Execution timestamp.
- Operation status.
- Completion information.

Each operation must have its own identity.

Multiple operations performed on the same dataset must remain independently identifiable.

### 3.2 Input information

The record must support retaining or referencing:

- Dataset identity.
- Source information.
- Selected measurement columns.
- Associated uncertainty columns.
- Other relevant input columns.
- Units and time references.
- Relevant dataset metadata.

The model must preserve enough information to understand which data an operation used.

### 3.3 Configuration and parameters

The record must accommodate the operation's actual configuration, including:

- Analysis method.
- User-selected parameters.
- Relevant default parameters.
- Search configuration.
- Explicit preprocessing.
- Quality filtering.
- Transformations.
- Other settings that materially affect the operation.

Configuration must be retained as historical information rather than reconstructed from current application defaults.

### 3.4 Results and supporting information

The model must support retaining or referencing:

- Structured operation results.
- Numerical outputs.
- Uncertainty information.
- Detection assessment information, where applicable.
- Warnings.
- Errors.
- Limitations.
- Relevant software and method version information.

The implementation should follow the approved distinction between shared operation fields and method-specific information.

## 4. Operation Status and Incomplete Records

Implement the operation-status representation established during Task 2.5.1.

The system must be able to distinguish between operations that:

- Complete successfully.
- Complete partially.
- Fail.
- Complete with warnings, where the approved design represents this separately.

An operation record should not become invalid merely because a later stage of an analysis fails.

For example, a BLS search may successfully identify candidate signals while uncertainty estimation fails. The underlying operation record must be capable of retaining the meaningful information that was successfully produced.

The model should also handle incomplete records appropriately when an operation is interrupted or persistence fails.

Do not invent additional status categories without justification from the approved design.

## 5. Project and Dataset Relationships

Operation records must be associated with the correct research project.

The implementation must support:

- Multiple operation records within one project.
- Multiple operations using the same dataset.
- Operations using different datasets within the same project.
- Different parameter configurations applied to the same dataset.
- Independent historical records for each operation.

The system must not assume that a project can contain only one analysis operation or that a dataset can only be analyzed once.

Dataset relationships must follow the identity and provenance design approved in Task 2.5.1.

The record should remain understandable if its original source file is moved or becomes unavailable.

Do not rely exclusively on mutable file paths or filenames to identify historical inputs.

## 6. Persistence Implementation

Implement operation-record persistence using the existing project persistence architecture and the approved Task 2.5.1 design.

The objective is to ensure that operation records survive application restarts and remain associated with their research projects.

### 6.1 Saving records

Implement the ability to:

- Save a new operation record.
- Preserve its unique identifier.
- Preserve its project association.
- Preserve its dataset association.
- Preserve its configuration and parameters.
- Preserve its results and supporting information.
- Handle optional fields correctly.

### 6.2 Loading records

Implement the ability to:

- Load operation records when a project is opened.
- Retrieve multiple operation records belonging to a project.
- Retrieve an individual operation using its identifier.
- Preserve the original record information.
- Handle missing or unavailable associated data appropriately.

### 6.3 Updating records

Where the approved design permits updates, ensure that changes do not silently overwrite historical information.

Determine which fields are immutable after creation and which may change as an operation progresses from incomplete to completed.

Preserve the distinction between updating an operation's status and changing the historical inputs or parameters associated with it.

### 6.4 Persistence integrity

The implementation must consider:

- Interrupted writes.
- Incomplete records.
- Corrupted records.
- Missing source datasets.
- Invalid identifiers.
- Duplicate identifiers.
- Invalid project associations.
- Inconsistent record references.

Errors should be handled explicitly.

The application must not silently discard existing project data or present corrupted information as a valid operation record.

## 7. Storage Architecture Constraints

The implementation must respect the existing approved storage decision.

D6 defers the permanent storage architecture and permits provisional local file persistence for the initial vertical slice, with limitations documented.

Task 2.5.2 must implement operation-record persistence within the approved architecture.

It is not authorization to introduce a permanent database architecture.

Unless separately approved, do not introduce:

- A new database system.
- An ORM.
- A new persistence framework.
- Additional dependencies.
- A broad storage redesign.

If the existing persistence approach creates limitations, document them and explain their implications.

The implementation should avoid making provisional storage decisions unnecessarily difficult to replace in a future approved architecture.

## 8. Retrieval Interfaces

Provide the underlying interfaces needed by subsequent tasks to access operation records.

The persistence and model layers should support the approved retrieval requirements, including:

- Retrieve all records associated with a project.
- Retrieve a specific record by identifier.
- Retrieve records by operation type, if included in the approved design.
- Access operation inputs and configuration.
- Access results and supporting information.
- Determine operation status.

These interfaces should be suitable for later integration with the BLS workflow and operation-history interface.

The goal is to establish reliable underlying functionality without implementing the user-facing history interface.

## 9. Scientific Integrity and Provenance

Operation-record persistence must preserve the project's scientific integrity requirements.

The implementation must ensure that:

- Original imported measurements remain unchanged.
- Operation records do not modify source datasets.
- Selected measurements are represented accurately.
- Associated uncertainty measurements remain correctly identified.
- Units and time references are preserved.
- Unknown metadata remains unknown.
- Preprocessing and filtering are represented accurately when recorded.
- Derived results remain distinguishable from original measurements.
- Historical operation information remains associated with the inputs that produced it.

Saving an operation record must not introduce automatic data transformations, quality filtering, normalization, or other scientific processing.

This task concerns retaining information about operations, not changing the scientific data itself.

## 10. Future Compatibility

Although BLS is the first operation type to use the record system, the general model should support reasonable future expansion.

The implementation should follow the approved separation between:

- Shared operation information.
- Operation-specific configuration.
- Operation-specific results.

Potential future operations may include:

- Other transit-search methods.
- Periodic signal analysis.
- Light-curve preprocessing.
- Data-quality assessment.

However, this task should not implement those methods or introduce a universal analysis framework.

The objective is a practical general record structure that can support the current application and be extended later without unnecessary redesign.

## 11. Testing and Validation

Develop automated tests for the operation-record model and persistence implementation.

Testing should follow the existing repository conventions.

### 11.1 Model tests

Verify:

- Valid operation-record creation.
- Required and optional fields.
- Unique identifiers.
- Operation types.
- Status representation.
- Project associations.
- Dataset associations.
- Parameter preservation.
- Result preservation.
- Correct handling of missing optional information.
- Invalid record handling.

### 11.2 Persistence tests

Verify:

- Saving operation records.
- Loading saved records.
- Saving multiple records to one project.
- Retrieving records by project.
- Retrieving individual records by identifier.
- Preserving record information across application restarts.
- Correct handling of missing associated datasets.
- Correct handling of invalid or incomplete records.
- Duplicate identifier handling.
- Persistence error handling.

### 11.3 Integrity tests

Verify:

- Original scientific measurements remain unchanged.
- Operation inputs remain correctly associated with their datasets.
- Flux and uncertainty references are preserved.
- Parameters and results are retained accurately.
- Historical records remain distinguishable.
- Missing metadata is not invented.
- Saving or loading operation records does not alter unrelated project information.

### 11.4 Portable test requirements

All standard automated tests must use portable fixtures and temporary directories.

Tests must not depend on:

- The user's permanent Kepler-10b FITS dataset.
- Machine-specific absolute paths.
- Files outside the repository's controlled test environment.

Do not weaken existing tests to make the new implementation pass.

## 12. Documentation Requirements

Update relevant documentation to reflect the implemented operation-record model and persistence functionality.

Review the actual documentation structure and update applicable files, including:

- Development roadmap.
- Development log.
- Data-model documentation.
- Architecture documentation.
- Data-flow documentation.
- Module responsibility documentation.
- Persistence documentation.
- Validation and testing documentation.
- Architecture decision records, where justified.
- Project state and continuity documentation.

Documentation must distinguish between:

- Functionality implemented in Task 2.5.2.
- Functionality designed but not yet implemented.
- Functionality deferred to Tasks 2.5.3–2.5.5.

Do not mark subsequent tasks as complete.

Do not mark Stage 2.5 as complete.

Foundation documentation remains read-only.

Follow the documentation-maintenance requirements in `AGENTS.md`.

## 13. Explicit Exclusions

Task 2.5.2 does not include:

- Connecting the BLS workflow to operation recording.
- Automatically creating records when BLS runs.
- Implementing the operation-history interface.
- Displaying operation history in the application.
- Implementing new scientific analysis methods.
- Implementing a complete analysis-replay system.
- Automatically reconstructing or rerunning historical operations.
- Introducing a permanent storage architecture.
- Introducing an ORM or unapproved dependency.
- Broad refactoring unrelated to operation records.

These responsibilities belong to later tasks or require separate approval.

## 14. Expected Outcome

At the end of Task 2.5.2, the application should have a working foundation for scientific operation records.

The implementation should provide:

1. A structured general operation-record model.
2. Appropriate support for operation-specific information.
3. Unique operation identity.
4. Project and dataset associations.
5. Operation status and incomplete-record handling.
6. Persistence within the approved project architecture.
7. Retrieval of saved operation records.
8. Preservation of configuration, inputs, and results.
9. Error handling and integrity safeguards.
10. Automated tests for the model and persistence functionality.
11. Updated documentation reflecting the actual implementation.

The operation-record system should be usable by Task 2.5.3 without requiring that task to redesign the underlying model or persistence layer.

## 15. Completion Criteria

Task 2.5.2 should only be considered complete when:

- The approved Task 2.5.1 design has been implemented.
- Operation records can be created and validated.
- Records can be associated with research projects and datasets.
- Multiple records can coexist within a project.
- Records can be saved and retrieved successfully.
- Record information survives project closure and reopening.
- Incomplete and invalid records are handled appropriately.
- Original scientific data remains unchanged.
- Existing project functionality continues to work.
- Automated tests pass.
- Documentation accurately reflects the implementation.
- The final implementation has been reviewed for scope compliance and data integrity.

Passing tests alone does not establish completion if the design, persistence, or scientific integrity requirements remain unmet.

The expected result is a reliable operation-record model and persistence foundation, ready for integration with the existing BLS workflow in Task 2.5.3.