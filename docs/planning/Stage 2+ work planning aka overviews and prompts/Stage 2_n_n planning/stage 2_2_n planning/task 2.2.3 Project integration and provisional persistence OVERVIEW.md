# Subtask 2.2.3 — Project Integration and Provisional Persistence

Primary objective: Integrate the imported light-curve dataset into the existing project lifecycle so that it can be associated with a project, saved, and recovered when that project is reopened.

This is where the scientific dataset becomes part of the application's persistent research workflow.

Subtask 2.2.1 establishes the data model, and 2.2.2 implements FITS importing and validation. Subtask 2.2.3 connects those capabilities to the existing project system.

## 1. Review the existing project architecture

Before implementation, inspect the existing project lifecycle and the completed work from 2.2.1 and 2.2.2.

Review:

- Project metadata and models.
- Project repository and service.
- Project creation, opening, saving, and closing.
- Existing external data-reference handling.
- The approved light-curve data model.
- FITS importer and import-result interfaces.
- Existing persistence and testing patterns.

Determine how scientific datasets should be associated with projects without putting all scientific data directly into the project metadata model.

## 2. Integrate imported datasets with projects

Implement the ability to associate an imported light-curve dataset with an active research project.

This should account for:

- Identifying which project owns the dataset association.
- Maintaining dataset identity.
- Tracking the original source file.
- Supporting multiple datasets within one project, if consistent with the approved design.
- Preserving relevant source and scientific metadata.
- Handling project switching and closing safely.

The project should retain enough information to identify and recover its imported datasets.

## 3. Implement provisional persistence

D6 explicitly deferred the permanent storage architecture but permits provisional local persistence for the first vertical slice.

Implement only the persistence necessary to support this initial workflow.

The persistence design should address:

- Saving imported dataset information.
- Saving measurement data.
- Preserving metadata, units, time references, uncertainties, and quality flags.
- Recovering datasets when reopening a project.
- Maintaining dataset identity across save and reopen.
- Handling missing or inaccessible original source files.
- Handling incomplete or failed saves safely.

The implementation should avoid prematurely committing the application to a permanent database architecture.

Important: The original FITS file must remain unchanged. The application should preserve its original values and metadata in its imported representation.

## 4. Preserve scientific integrity

Persistence must not silently alter scientific data.

In particular:

- Do not normalize flux values.
- Do not detrend or filter measurements.
- Do not remove nonzero quality flags.
- Do not silently discard missing or non-finite values.
- Do not change units or time references without an explicitly documented and approved conversion.
- Do not replace unknown metadata with assumptions.
- Preserve the distinction between original measurements and future derived data.

The application should be able to distinguish the original source file from the application's persisted representation.

## 5. Integrate with the project lifecycle

The dataset persistence workflow must work with existing project operations.

Verify behavior when:

- A project is created and a dataset is imported.
- A project is saved.
- A saved project is closed.
- The project is reopened.
- The dataset is recovered.
- A project containing multiple datasets is reopened.
- A project is switched while changes are pending.
- The original FITS file is no longer available.
- Dataset persistence fails.

The existing Save/Discard/Cancel behavior and dirty-state tracking must remain consistent.

## 6. Handle errors and recovery

Consider failure cases explicitly.

Examples include:

- Missing persisted dataset files.
- Corrupted persisted data.
- Incomplete writes.
- Invalid dataset references.
- Missing original FITS files.
- Unsupported or outdated data-model versions.
- Failure while loading one dataset in a project containing multiple datasets.

A failure to load one dataset should not unnecessarily destroy or invalidate the rest of the project.

The application should provide understandable error messages and preserve recoverable project information wherever possible.

## 7. Add automated tests

Testing should use temporary project directories and controlled datasets rather than relying on the user's permanent Kepler-10b file path.

Tests should cover:

- Dataset association with a project.
- Saving imported datasets.
- Loading datasets after reopening.
- Preservation of measurement values.
- Preservation of metadata and units.
- Preservation of uncertainties and quality flags.
- Multiple datasets within one project.
- Missing original source files.
- Missing or corrupted persisted data.
- Persistence failures.
- Project switching and closing behavior.
- Dirty-state integration.
- Compatibility with existing project lifecycle tests.

The full test suite must continue passing.

## 8. Update documentation

Follow the documentation-maintenance requirements in `AGENTS.md`.

Review and update relevant documents, including:

- Development roadmap.
- Development log.
- Architecture documentation.
- Data-model documentation.
- Module responsibilities.
- Data-flow documentation.
- Storage and persistence decisions.
- Testing and validation documentation.
- Project state and decision records.

Document the provisional nature of the persistence implementation and its known limitations.

Do not modify Foundation requirements.

## 9. Explicitly excluded work

| Functionality                           | Subtask  |
| --------------------------------------- | -------- |
| FITS inspection and data-model design   | 2.2.1    |
| FITS importing and validation           | 2.2.2    |
| Data table interface                    | 2.3      |
| Light-curve visualization               | 2.3      |
| BLS transit analysis                    | 2.4      |
| Analysis operation records              | 2.5      |
| Permanent storage architecture redesign | Deferred |
| External archive integration            | Stage 4  |

## Completion checklist

## 2.2.3 expected deliverables

- Review completed 2.2.1 and 2.2.2 implementations.
- Define how datasets associate with projects.
- Implement project-level dataset management.
- Implement provisional dataset persistence.
- Implement dataset recovery after reopening.
- Preserve scientific measurements and metadata.
- Support multiple datasets where approved.
- Handle missing source files and persistence failures.
- Integrate with project dirty-state and lifecycle behavior.
- Add automated persistence and integration tests.
- Update relevant documentation.
- Verify the complete test suite.
- Document provisional-storage limitations.

Central success criterion: A user can import a real light-curve dataset into a research project, save the project, close the application, reopen the project, and recover the dataset with its scientific measurements and metadata intact.

Sequence: Review 2.2.1 and 2.2.2 → Plan → review and approval → Build → implementation review → completion verification.

Important boundary: This task should deliver working persistence for the initial scientific workflow, not settle the application's permanent storage architecture.