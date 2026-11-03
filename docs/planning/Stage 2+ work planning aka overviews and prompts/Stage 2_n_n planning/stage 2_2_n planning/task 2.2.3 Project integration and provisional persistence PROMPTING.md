# PLAN MODE PROMPT

# Subtask 2.2.3 — Project Integration and Provisional Persistence
## PLAN Prompt

**Mode: PLAN ONLY. Inspect, analyze, and propose. Do not modify files or implement anything.**

You are working on the New_Project astronomy research application.

Repository:
`C:\Code\New_Project`

GitHub:
`https://github.com/brettadin/New_Project`

The project is a local-first astronomy research application built with Python 3.13 and PySide6. Its existing project lifecycle supports project creation, discovery, opening, saving, closing, status management, and dirty-state handling.

Your task is to investigate and prepare an implementation plan for **Stage 2, Subtask 2.2.3 — Project Integration and Provisional Persistence**.

Do not begin implementation. Your responsibility is to inspect the current repository, verify prerequisites, identify the appropriate integration design, and produce a detailed plan for review and approval.

---

## 1. Mandatory governance and context review

Before analyzing implementation details, read and follow:

- `AGENTS.md`
- The applicable Foundation requirements referenced by `AGENTS.md`
- The current development roadmap
- The current development log
- Relevant architecture and data-model documentation
- Relevant decision records
- Relevant testing and validation documentation
- Current project-state and continuity documentation

Pay particular attention to:

- Project lifecycle and workspace separation.
- Local storage and data integrity.
- Data ownership, provenance, and traceability.
- Scientific-data preservation.
- Reproducibility.
- Documentation maintenance during implementation.
- Approval requirements for architecture and storage decisions.

Foundation is authoritative and read-only. Do not modify Foundation requirements or documents.

Follow the existing repository's documentation structure rather than assuming that every document named in earlier discussions exists.

## 2. Verify prerequisites before proceeding

Subtask 2.2.3 depends on the completed work from:

- **2.2.1 — FITS Inspection and Data-Model Design**
- **2.2.2 — FITS Import and Validation**

Inspect the actual repository to establish whether both subtasks have been implemented, tested, and documented.

Do not rely solely on development-log statements or previous conversation summaries.

Specifically verify:

### 2.2.1
- The approved light-curve data model exists.
- Its actual classes, fields, relationships, and interfaces.
- How source information, measurements, uncertainties, metadata, and validation information are represented.
- How original measurements are distinguished from derived data.
- What tests cover the model.

### 2.2.2
- The FITS importer exists.
- Its actual input and output interfaces.
- How HDUs and measurement columns are identified.
- How measurements and scientific metadata are extracted.
- How missing values, non-finite values, uncertainties, and quality flags are handled.
- How validation warnings and errors are represented.
- Whether the importer preserves the original source file and measurement values.
- What tests cover importing and validation.

**Prerequisite gate:**

If either prerequisite is incomplete, materially inconsistent, or lacks an established interface needed for integration:

1. Stop before designing implementation around assumed interfaces.
2. Report exactly what is missing or unresolved.
3. Explain what must be completed or clarified first.
4. Identify whether the issue is a genuine blocker or simply a documentation gap.
5. Do not silently redesign or replace the approved 2.2.1 or 2.2.2 work.

If both prerequisites are sufficiently complete, continue with the investigation below.

## 3. Inspect the existing project lifecycle

Review the actual implementation of:

- Project metadata/model.
- Project repository.
- Project service.
- Project creation and discovery.
- Project opening and closing.
- Project saving.
- Dirty-state tracking.
- Save/Discard/Cancel behavior.
- Project switching.
- Existing external data-reference handling.
- Configuration and project-location management.

Identify the actual modules, classes, methods, and tests involved.

Establish how project metadata is currently persisted and how scientific datasets should integrate without unnecessarily coupling scientific measurements to project metadata.

Do not assume the existing project persistence mechanism is suitable for storing scientific measurement arrays.

## 4. Design project-to-dataset integration

Determine how imported light-curve datasets should be associated with research projects.

Investigate and propose:

- How a project identifies its associated datasets.
- How each dataset receives and retains a stable identity.
- How source-file information is associated with the dataset.
- How dataset metadata is connected to its measurement content.
- How multiple datasets within one project should be represented.
- How duplicate imports or repeated references should be handled.
- How dataset associations behave during project save, close, reopen, and switching.
- How project dirty-state tracking should respond to dataset additions or changes.

Consider the relationship between project metadata and scientific dataset content.

The design should preserve the existing separation of responsibilities and avoid putting large measurement arrays directly into the project metadata model unless the approved architecture explicitly supports that approach.

Do not assume that a particular class, field, or repository interface should be modified before inspecting the code.

## 5. Investigate provisional persistence

Decision D6 deferred the permanent storage architecture. It permits provisional local persistence for the initial scientific vertical slice, provided the limitations are documented.

Investigate the smallest appropriate persistence approach that supports the current Stage 2 workflow.

Determine:

- What information needs to be persisted.
- Where project-associated scientific data should be stored.
- How the existing project directory structure affects the design.
- Whether the existing JSON-based project metadata persistence can remain separate from scientific dataset persistence.
- How imported measurement arrays should be serialized.
- How scientific metadata and original source information should be preserved.
- How dataset identity should survive save and reopen.
- How persistence failures should be handled.
- How incomplete writes or corrupted persisted data should be detected.
- How future schema or data-model changes could be accommodated without prematurely designing a permanent storage system.

Evaluate reasonable alternatives where necessary, but do not overengineer the initial implementation.

Clearly distinguish:
- Existing project metadata persistence.
- Provisional scientific dataset persistence.
- The deferred permanent storage architecture.

Do not introduce a database, ORM, or new storage dependency merely because it may be useful later. Any such proposal must be justified and explicitly identified as requiring approval.

Do not implement persistence during this task.

## 6. Scientific integrity and provenance requirements

The persistence design must preserve the scientific meaning and traceability of the imported data.

Account for:

- Original source-file path and filename.
- Source identity and available provenance information.
- Measurement values.
- Measurement uncertainties.
- Measurement units.
- Time values and their reference conventions.
- Time scale and other available time metadata.
- Quality flags.
- Cadence identifiers.
- Original column information.
- Missing and non-finite values.
- Validation warnings and relevant import information.

The design must not silently:

- Normalize measurements.
- Detrend or filter observations.
- Remove nonzero quality flags.
- Drop missing or non-finite values.
- Convert units or time references.
- Replace unknown metadata with assumed values.
- Overwrite or modify the original FITS file.

Preserve the distinction between:

1. The original source file.
2. The application's imported representation.
3. Future derived or transformed scientific data.

The application should be able to identify the original source independently of its persisted imported representation.

Investigate how the application should behave if the original FITS file is moved, renamed, deleted, or becomes inaccessible after import.

Do not assume that a missing original source file makes an already persisted dataset unusable.

## 7. Project lifecycle and failure handling

Analyze how the proposed integration should behave during normal and abnormal project operations.

Consider:

- Creating a project and importing a dataset.
- Saving a project containing imported datasets.
- Closing a project after saving.
- Reopening a project and recovering its datasets.
- Switching between projects.
- Closing a project with pending dataset changes.
- Saving while dataset persistence fails.
- Loading a project with missing dataset files.
- Loading a project with corrupted persisted data.
- Loading a project with an unsupported dataset schema version.
- Recovering a project containing multiple datasets when one dataset cannot be loaded.

The design must preserve existing project lifecycle behavior, including Save/Discard/Cancel semantics and protection against losing the active project when a project switch fails.

Determine whether the existing dirty-state mechanism can accommodate scientific dataset changes or whether a carefully scoped extension is necessary.

Avoid unrelated changes to the completed project lifecycle implementation.

## 8. Testing strategy

Inspect the current testing structure and propose specific tests for the integration and persistence work.

At minimum, consider:

### Project integration
- Associating an imported dataset with a project.
- Dataset identity and association persistence.
- Multiple datasets within one project.
- Dataset additions affecting project dirty state.
- Project switching and closing behavior.

### Persistence and recovery
- Saving a dataset.
- Loading a saved dataset.
- Closing and reopening a project.
- Preserving measurement values.
- Preserving uncertainties.
- Preserving units and time references.
- Preserving quality flags and cadence identifiers.
- Preserving missing and non-finite values according to the approved data model.
- Preserving source and provenance metadata.
- Recovering multiple datasets.

### Failure cases
- Missing original FITS file.
- Missing persisted dataset content.
- Corrupted persisted content.
- Unsupported schema version.
- Failed or incomplete persistence.
- Failure loading one dataset without unnecessarily invalidating the rest of the project.
- Project lifecycle behavior when dataset saving fails.

Use temporary project directories and controlled test datasets.

Do not make the standard automated test suite depend on the user's permanent Kepler-10b dataset or an absolute machine-specific path.

The real Kepler-10b FITS file may be used for optional local verification if available, but routine tests must remain portable.

Do not weaken or remove existing tests to make the proposed implementation easier.

## 9. Documentation impact

Identify which existing documentation files will need changes during implementation.

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

Follow the documentation-maintenance requirements in `AGENTS.md`.

Document that this is provisional persistence and identify its limitations.

Do not modify documentation during Plan mode.

## 10. Scope boundaries

This subtask is limited to project integration and provisional persistence.

Do not include:

- Reworking the 2.2.1 data model without an identified issue and approval.
- Reimplementing the 2.2.2 FITS importer.
- Building the data table or visualization interface (2.3).
- Implementing BLS analysis or uncertainty calculations (2.4).
- Implementing analysis operation records (2.5).
- Integrating external astronomical archives.
- Implementing permanent storage architecture.
- Introducing accounts, authentication, groups, or multi-user infrastructure.
- Unrelated project lifecycle refactoring.
- Unapproved dependency changes.

The objective is to make the initial imported scientific dataset persist reliably within a project, not to complete the application's entire scientific workflow.

## 11. Required Plan report

Produce a structured report with the following sections.

### A. Prerequisite verification
- Status of 2.2.1.
- Status of 2.2.2.
- Actual classes, modules, and interfaces verified.
- Any prerequisite gaps or blockers.

### B. Existing project architecture
- Relevant modules and responsibilities.
- Existing project persistence behavior.
- Existing dirty-state and lifecycle behavior.
- Existing external-reference handling.

### C. Current data-model and importer integration
- Actual dataset representation.
- Actual importer interface.
- How import results should enter the project system.
- Any interface gaps.

### D. Proposed project-dataset relationship
- Dataset identity.
- Project association.
- Multiple-dataset handling.
- Source and provenance relationships.
- Dirty-state implications.

### E. Provisional persistence design
- Proposed storage location and structure.
- Serialization approach.
- Metadata and measurement preservation.
- Dataset recovery.
- Versioning considerations.
- Failure handling.
- Explicit limitations and deferred decisions.

### F. Scientific integrity assessment
Explain how the proposed design preserves:
- Original source information.
- Measurement values.
- Uncertainties.
- Units and time references.
- Quality flags and cadence identifiers.
- Missing and non-finite values.
- Provenance and validation information.

Identify any risks to scientific integrity.

### G. Project lifecycle and recovery
Describe expected behavior for:
- Save.
- Close.
- Reopen.
- Switch.
- Pending changes.
- Missing or corrupted dataset content.
- Persistence failures.

### H. Testing plan
Identify proposed test modules, scenarios, fixtures, and expected assertions.

### I. Architecture and dependency impact
Identify:
- Files likely to change.
- New files that may be justified.
- Existing interfaces that may need extension.
- Dependencies, if any.
- Potential architectural risks.

Do not present proposed file changes as verified modifications.

### J. Documentation impact
List the documents that should be updated and explain why.

### K. Implementation breakdown
Propose a logical, appropriately scoped sequence of implementation steps.

Each step should identify:
- Objective.
- Likely modules involved.
- Tests required.
- Documentation implications.
- Dependencies on earlier steps.

### L. Risks, unresolved questions, and approval decisions
Separate:
- Verified facts.
- Assumptions.
- Recommendations.
- Unresolved decisions.
- Decisions requiring explicit user approval.

### M. Final readiness assessment
State whether the task is:
- Ready for implementation planning and approval.
- Conditionally ready, with specific conditions.
- Blocked, with specific reasons.

Do not treat a recommendation as an approved architectural decision.

---

## 12. Plan-mode restrictions

During this task:

- Do not create, edit, delete, rename, or move repository files.
- Do not implement code.
- Do not change dependencies or configuration.
- Do not modify the original FITS dataset.
- Do not modify Foundation.
- Do not change Git history.
- Do not commit, push, reset, or clean the repository.
- Do not begin Subtask 2.2.4 or later work.

You may inspect files, execute read-only commands, inspect FITS data, and run existing tests if useful for verification. Clearly report any commands executed and their results.

If a proposed design requires a decision outside the existing approvals, identify it and stop short of making that decision.

**Stop after delivering the complete Plan report. Wait for review and explicit authorization before making any changes.**



# BUILD MODE PROMPT


# Subtask 2.2.3 — Project Integration and Provisional Persistence
## BUILD Prompt

**Mode: BUILD. Implement only the design explicitly approved after review of the 2.2.3 Plan report.**

You are working on the New_Project astronomy research application.

Repository:
`C:\Code\New_Project`

GitHub:
`https://github.com/brettadin/New_Project`

The project is a local-first astronomy research application built with Python 3.13 and PySide6.

Your task is to implement **Stage 2, Subtask 2.2.3 — Project Integration and Provisional Persistence**.

This Build task follows the completed and approved planning process. The approved 2.2.3 Plan report is the implementation specification for this task.

Do not independently redesign approved architecture, introduce unapproved features, or expand the scope.

---

## 1. Mandatory pre-implementation review

Before modifying anything:

1. Read and follow `AGENTS.md`.
2. Review the applicable Foundation requirements. Foundation is authoritative and read-only.
3. Read the current roadmap and development log.
4. Read the approved 2.2.3 Plan report.
5. Review the completed 2.2.1 data-model implementation.
6. Review the completed 2.2.2 FITS importer and validation implementation.
7. Inspect the current project model, repository, service, and lifecycle implementation.
8. Review relevant architecture, data-model, persistence, testing, and decision documentation.
9. Inspect the current Git status and working tree.

Verify that the current repository still matches the assumptions and interfaces established during planning.

**Do not overwrite or discard existing user changes.**

If the approved Plan report conflicts with the current implementation, or a required prerequisite is missing or materially different:

- Stop before implementing the affected work.
- Explain the discrepancy.
- Identify the affected approved design decisions.
- Request clarification or approval for a revised approach.

Do not silently modify the approved design to accommodate unexpected repository conditions.

## 2. Scope and implementation objective

Implement the approved integration that allows a light-curve dataset imported through Subtask 2.2.2 to become associated with a research project and persist across project save, close, and reopen operations.

The completed workflow should support:

1. Opening or creating a research project.
2. Importing a supported light-curve dataset through the existing importer.
3. Associating the imported dataset with the active project.
4. Saving the project and its scientific dataset content.
5. Closing the project.
6. Reopening the project.
7. Recovering the associated dataset with its scientific measurements and metadata intact.

Implement only the project integration and provisional persistence design approved in the Plan report.

## 3. Project-to-dataset integration

Implement the approved relationship between projects and scientific datasets.

Account for:

- Stable dataset identity.
- Project association.
- Original source-file information.
- Dataset metadata.
- Measurement content.
- Multiple datasets within one project, if included in the approved design.
- Duplicate import or reference behavior, if explicitly approved.
- Dataset additions and changes affecting project dirty-state tracking.

Maintain the separation between:

- Project metadata and lifecycle.
- Scientific dataset metadata.
- Scientific measurement content.
- Original source files.

Reuse existing project services and repositories where appropriate.

Do not place large measurement arrays directly into project metadata unless that approach was explicitly approved.

Do not unnecessarily refactor the completed project lifecycle implementation.

## 4. Provisional scientific-data persistence

Implement the persistence mechanism explicitly approved in the Plan report.

The implementation must:

- Save the imported dataset content.
- Preserve dataset identity.
- Preserve scientific metadata.
- Preserve measurement arrays and their relationships.
- Preserve uncertainty information.
- Preserve quality flags and cadence identifiers.
- Preserve source and provenance information.
- Recover datasets after project reopening.
- Handle missing or inaccessible original source files.
- Detect and report missing or corrupted persisted content.
- Handle persistence failures without silently losing existing project data.

Preserve the separation between project metadata persistence and scientific dataset persistence as established by the approved design.

D6 remains in effect: permanent storage architecture is deferred.

Do not introduce a database, ORM, storage framework, or new dependency unless explicitly approved.

Document the provisional nature and limitations of the implementation.

## 5. Scientific integrity requirements

Scientific-data integrity is mandatory.

The implementation must preserve the imported representation without silently changing scientific meaning.

Specifically:

- Preserve original measurement values.
- Preserve uncertainty values and their associations.
- Preserve measurement units.
- Preserve timestamps and time references.
- Preserve time scales and available time metadata.
- Preserve quality flags.
- Preserve cadence identifiers.
- Preserve original column information where represented by the approved model.
- Preserve missing and non-finite values according to the approved data model.
- Preserve relevant validation warnings and provenance information.
- Preserve unknown metadata as unknown.

Do not:

- Normalize flux values.
- Detrend or filter observations.
- Remove nonzero quality flags.
- Drop missing or non-finite measurements.
- Silently convert units or time references.
- Invent missing metadata.
- Modify, overwrite, move, or delete the original FITS file.

Maintain the distinction between:

1. The original FITS source file.
2. The application's imported dataset representation.
3. Future derived or transformed scientific data.

The persisted representation must not be presented as the original FITS file.

## 6. Project lifecycle integration

Integrate the approved persistence behavior with existing project lifecycle operations.

Verify and preserve:

- Project creation.
- Project opening.
- Project saving.
- Project closing.
- Project switching.
- Dirty-state tracking.
- Save/Discard/Cancel behavior.
- Active-project preservation when a switch or open operation fails.

Dataset changes must participate in the existing project lifecycle consistently with the approved design.

A failed dataset save must not silently result in a project being treated as successfully saved.

A failed project switch must not leave the application in an inconsistent state or unnecessarily discard the previously active project.

Do not weaken existing project lifecycle guarantees or rewrite unrelated functionality.

## 7. Error handling and recovery

Implement the approved failure-handling behavior for:

- Missing persisted dataset content.
- Corrupted persisted content.
- Incomplete or failed writes.
- Invalid dataset references.
- Missing original FITS files.
- Unsupported persisted dataset schema versions.
- Failure loading one dataset when a project contains multiple datasets.

Where possible, isolate dataset-loading failures so that one unavailable dataset does not unnecessarily prevent the project or other datasets from being recovered.

Provide understandable error messages through the existing application error-reporting conventions.

Do not silently substitute empty or fabricated scientific measurements for unavailable data.

## 8. Automated tests

Implement the tests specified in the approved Plan report.

Use temporary project directories and controlled test datasets.

The standard test suite must not depend on:

`C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits`

The real Kepler-10b dataset may be used for optional local verification, but routine automated tests must remain portable.

At minimum, verify the following where applicable to the approved design.

### Project integration
- Associating an imported dataset with a project.
- Stable dataset identity.
- Multiple datasets in one project.
- Dataset additions affecting dirty-state tracking.
- Dataset association surviving project save and reopen.

### Persistence and recovery
- Saving dataset content.
- Loading saved dataset content.
- Closing and reopening a project.
- Preserving measurement values.
- Preserving uncertainties.
- Preserving units and time references.
- Preserving quality flags and cadence identifiers.
- Preserving missing and non-finite values.
- Preserving source and provenance metadata.
- Recovering multiple datasets.

### Failure handling
- Missing original FITS source.
- Missing persisted dataset content.
- Corrupted persisted content.
- Unsupported schema version.
- Failed or incomplete persistence.
- Failure loading one dataset without unnecessarily invalidating the rest.
- Project save failure caused by dataset persistence failure.
- Project switching and closing behavior when dataset changes cannot be saved.

### Regression testing
- Run the existing project lifecycle tests.
- Run the existing 2.2.1 data-model tests.
- Run the existing 2.2.2 importer and validation tests.
- Run the complete test suite.

Do not remove, weaken, skip, or rewrite existing tests merely to make the implementation pass.

If an existing test requires adjustment because the approved behavior changes, explain why and preserve its original intent.

## 9. Documentation maintenance

Follow the documentation-maintenance requirements in `AGENTS.md`.

Before implementation, identify the affected documents. During implementation, update documentation alongside relevant code changes.

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

Document:

- The implemented project-to-dataset relationship.
- The actual persistence mechanism.
- Dataset save and recovery behavior.
- Scientific-integrity protections.
- Error and recovery behavior.
- Test coverage and results.
- Provisional storage limitations.
- Deferred architectural decisions.

Do not claim that permanent storage architecture has been established.

Do not modify Foundation requirements or documents.

Do not mark later subtasks as complete.

## 10. Scope exclusions

Do not implement or begin:

- Changes to the 2.2.1 data model beyond specifically approved corrections.
- Reimplementation of the 2.2.2 FITS importer.
- Data table interface (2.3).
- Light-curve visualization (2.3).
- BLS transit analysis (2.4).
- BLS uncertainty calculations (2.4).
- Analysis operation records (2.5).
- External astronomical archive integration.
- Permanent storage architecture redesign.
- Accounts, authentication, groups, or multi-user infrastructure.
- Unrelated project lifecycle refactoring.
- Unapproved dependencies or features.

If an issue in an excluded area prevents completion, document it and stop for approval rather than expanding scope.

## 11. Implementation discipline

- Implement in the sequence established by the approved Plan report.
- Keep changes focused and appropriately scoped.
- Follow existing naming, typing, error-handling, and testing conventions.
- Add comments where they clarify non-obvious scientific or persistence behavior.
- Avoid unnecessary abstractions and speculative future infrastructure.
- Do not duplicate existing functionality.
- Do not silently change public interfaces.
- Do not make unrelated formatting or cleanup changes.
- Preserve all existing user work.
- Do not modify the original FITS file.
- Do not modify Foundation.
- Do not commit or push changes.
- Do not reset, clean, or rewrite Git history.

If an additional architectural decision becomes necessary, stop and request approval before proceeding with the affected implementation.

## 12. Final verification and report

After implementation, run the targeted tests and the complete test suite.

Compare the resulting implementation against:

- The approved 2.2.3 Plan report.
- The requirements in this Build prompt.
- `AGENTS.md`.
- Relevant Foundation requirements.
- Existing project lifecycle behavior.
- Scientific-integrity requirements.

Inspect the final working tree and identify all changed and newly created files.

Provide a structured completion report containing:

### A. Implementation summary
- What was implemented.
- How project-to-dataset integration works.
- How provisional persistence works.

### B. Files changed
For every changed or created file:
- Path.
- Purpose.
- Summary of changes.

### C. Scientific integrity
Explain how measurements, uncertainties, units, time references, quality flags, missing values, and provenance are preserved.

### D. Project lifecycle behavior
Report how save, close, reopen, switching, and dirty-state behavior work.

### E. Error handling and recovery
Identify implemented failure cases and any limitations.

### F. Testing results
Include:
- Exact commands executed.
- Targeted test results.
- Full test-suite result.
- Any failures, warnings, or skipped tests.
- Whether the real Kepler-10b dataset was used for optional verification.

Do not report tests as passing unless they were actually executed and passed.

### G. Documentation updates
List each document changed and explain its purpose.

Also identify relevant documents intentionally left unchanged.

### H. Scope compliance
Confirm which planned functionality was implemented and which later-subtask functionality was excluded.

### I. Outstanding issues
List unresolved decisions, limitations, technical debt, or deferred work.

### J. Completion assessment
State whether Subtask 2.2.3 is complete, partially complete, or blocked.

Do not mark it complete if required implementation, tests, or documentation remain unfinished.

---

**Stop after completing Subtask 2.2.3. Do not begin 2.2.4 or any later subtask.**

Do not commit or push. Leave all changes in the working tree for user review.

Wait for the user to review the implementation and explicitly authorize the next task.