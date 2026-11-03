# PLAN MODE PROMPT

# Subtask 2.2.1 — FITS Inspection and Data-Model Design

## Mode: PLAN ONLY

Inspect the existing project, examine the selected astronomical FITS dataset, and develop a proposed data-model and import-design approach.

**Do not implement anything. Do not modify, create, delete, or overwrite files.**

This task is limited to understanding the FITS data structure and determining how the application should represent an imported light-curve dataset. Import implementation, project integration, and persistence implementation belong to later subtasks.

---

## 1. Project Context

Repository:

`C:\Code\New_Project`

GitHub:

https://github.com/brettadin/New_Project

The application is a local desktop astronomy research application built with:

- Python 3.13
- PySide6
- NumPy
- SciPy
- Astropy
- Matplotlib (QtAgg)
- pytest

The project currently has working project lifecycle functionality:

- Create projects.
- Discover and open projects.
- Save and close projects.
- Track unsaved changes.
- Manage project statuses.
- Persist project metadata.

The current full test-suite baseline is 135 passing tests, as reported in the latest development log. Verify the current repository state rather than assuming this count is still current.

The next development objective is Stage 2.2 — Light-Curve Import.

The overall objective is to import a real astronomical light curve into a project, preserve its scientific context, and make it available for subsequent visualization and analysis.

---

## 2. Governing Instructions and Required Reading

Before beginning the investigation:

1. Read the root `AGENTS.md` completely.
2. Follow all applicable project governance and approval requirements.
3. Read the relevant sections of:
   - `docs/MASTER_DEVELOPMENT_ROADMAP.md`
   - `docs/development/DEVELOPMENT_LOG.md`
   - Relevant architecture and module documentation.
   - Relevant data-model documentation.
   - Relevant decision records.
   - Relevant scientific review documents.
4. Review the existing project lifecycle implementation, especially:
   - `src/project_model.py`
   - `src/project_repository.py`
   - `src/project_service.py`
   - Any existing data-reference or project-association functionality.
5. Review existing tests to understand established conventions and architectural expectations.
6. Inspect the Foundation requirements relevant to:
   - Scientific data formats and metadata.
   - Original-data preservation.
   - Data lineage and provenance.
   - Scientific integrity.
   - Uncertainty and validation.
   - Reproducibility.
   - Local storage and data ownership.
   - Project and workspace separation.

Foundation documents are authoritative and read-only. Do not modify them or reinterpret their requirements to fit a proposed implementation.

Do not assume that every document listed above exists. Identify actual files and report missing or incomplete documentation where relevant.

---

## 3. Selected Scientific Dataset

The initial target is the existing Kepler-10b FITS dataset.

Local path:

`C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits`

Filename:

`kplr011904151-2009131105131_llc_full.fits`

This file is outside the repository and is intended to remain outside the repository.

It must be treated as read-only.

Do not move, rename, overwrite, modify, or delete it.

Previously established information about this dataset includes:

- FITS format.
- Kepler long-cadence photometry.
- Approximately 9.7 days of observations.
- Approximately 476 observation rows.
- `TIME` values using the BKJD time reference and TDB time system.
- `SAP_FLUX` and `PDCSAP_FLUX` measurement columns.
- Corresponding flux uncertainty columns.
- `SAP_QUALITY` quality flags.
- `CADENCENO` cadence identifiers.
- Approximately four missing flux measurements.
- Approximately 37 observations with nonzero quality flags.

These details are prior findings, not substitutes for inspection. Verify them against the actual local file.

If the file cannot be accessed, report that limitation. Do not substitute synthetic data or another dataset.

---

## 4. Investigation A — FITS File Structure

Inspect the actual FITS file using Astropy.

Determine and report:

1. The number of HDUs.
2. The purpose of each HDU.
3. Which HDU contains the relevant light-curve measurements.
4. The structure and names of the available table columns.
5. The data types and shapes of the columns.
6. Relevant FITS header metadata.
7. Units associated with the measurements.
8. Time reference, time system, and relevant timing metadata.
9. Available uncertainty information.
10. Available data-quality information.
11. Missing, non-finite, or otherwise unusual values.

Pay particular attention to the relationship between:

- `TIME`
- `SAP_FLUX`
- `PDCSAP_FLUX`
- `SAP_FLUX_ERR`
- `PDCSAP_FLUX_ERR`
- `SAP_QUALITY`
- `CADENCENO`

Do not assume all FITS files use this exact structure.

Identify which properties are specific to this Kepler dataset and which are general FITS or astronomical light-curve concepts.

Do not perform scientific analysis or attempt to detect a transit during this task.

---

## 5. Investigation B — Proposed Light-Curve Data Model

Examine the existing application architecture and propose how an imported light-curve dataset should be represented internally.

The proposal should address the following categories.

### A. Source information

Determine how the application should represent:

- Original source-file path.
- Original filename.
- Source identifier, if available.
- Source or archive information, if available.
- Import date/time.
- Relevant source metadata.
- Whether the source file is currently accessible.

Do not assume that a local file path alone constitutes complete scientific provenance.

### B. Measurement data

Determine how the model should represent:

- Observation timestamps.
- Flux measurements.
- Flux uncertainties.
- Observation identifiers or cadence numbers.
- Data-quality flags.
- Missing or invalid values.
- The identity of the selected measurement column.

Consider whether multiple measurement columns should remain independently accessible.

For example, `SAP_FLUX` and `PDCSAP_FLUX` should not be merged or treated as interchangeable.

### C. Scientific metadata

Determine how the model should preserve:

- Measurement units.
- Time units.
- Time reference or epoch.
- Time system or scale.
- Instrument or mission information, where available.
- Observation cadence.
- Relevant FITS header information.
- Original column names and their relationships.

Do not silently assume units or time conventions when metadata is missing.

### D. Validation and warnings

Determine how validation findings should be represented.

Consider:

- Missing required fields.
- Missing optional fields.
- Non-finite values.
- Invalid timestamps.
- Missing uncertainty values.
- Nonzero quality flags.
- Unsupported or ambiguous metadata.
- Unexpected column structures.

Distinguish between:

1. A condition that prevents importing a dataset.
2. A condition that permits import but generates a warning.
3. A condition that should be preserved as metadata without automatically changing the measurements.

Do not propose automatically discarding all observations with nonzero quality flags.

### E. Original and derived data

The model must conceptually distinguish:

- Original source measurements.
- Imported representations of those measurements.
- Future derived or transformed measurements.

Normalization, filtering, detrending, quality filtering, and other processing operations must not silently overwrite original measurements.

Do not implement any processing functionality during this task.

---

## 6. Investigation C — Existing Architecture and Integration

Examine how the proposed data model would fit into the existing application.

Determine:

1. Which existing modules could reasonably own the scientific dataset model.
2. Whether a new module is justified.
3. How the dataset should relate to `ProjectMetadata`.
4. Whether the current project model already provides a suitable relationship mechanism.
5. Whether any existing functionality should be reused.
6. Whether the proposed design creates unnecessary coupling between the UI, scientific data, and persistence layers.

Do not assume that the scientific dataset should be stored directly inside `ProjectMetadata`.

The application should preserve the conceptual distinction between:

- Project metadata.
- Scientific datasets.
- Source-file references.
- Scientific metadata.
- Future analysis results.

The design should also leave room for later support of additional astronomical datasets and formats without attempting to implement them now.

---

## 7. Investigation D — Storage and Persistence Boundaries

Decision D6 deferred the permanent storage architecture.

The current approved direction permits provisional local file persistence for the first working vertical slice, but does not establish a complete permanent storage architecture.

For this task:

- Identify what the data model needs to represent independently of storage.
- Identify which information must eventually survive project save and reopen.
- Identify any storage-related requirements that the next task will need to address.
- Explain the implications of referencing an external source file versus copying data into a project.
- Identify limitations of relying on external file paths.

Do not make a permanent storage architecture decision.

Do not introduce a database, file-copying system, or new persistence mechanism as part of this planning task.

If a decision requires formal approval, identify it explicitly rather than making it on the project's behalf.

---

## 8. Investigation E — Future Compatibility

The first implementation targets the selected Kepler FITS dataset.

However, the longer-term project is intended to support additional astronomical research data.

Consider whether the proposed model can reasonably accommodate future:

- FITS light curves from other missions.
- Different measurement columns.
- Different time conventions.
- Different flux or intensity units.
- Different uncertainty representations.
- Different data-quality systems.
- Additional photometric datasets.

The initial design should avoid unnecessary Kepler-specific assumptions in the general data model.

However, do not design an elaborate universal astronomy data framework or implement support for formats that are outside the current scope.

Explain which parts of the design should be general and which can remain specific to the initial Kepler importer.

---

## 9. Required Deliverable — Proposed Design

Produce a structured planning report containing:

### 1. Repository and architecture findings

- Relevant files inspected.
- Existing functionality that can be reused.
- Relevant existing interfaces and models.
- Missing or incomplete documentation.
- Current test baseline, if verified.

### 2. FITS inspection results

- Actual HDU structure.
- Relevant headers and metadata.
- Column names, types, shapes, and units.
- Time conventions.
- Missing or unusual data.
- Any differences from previously established dataset information.

### 3. Proposed data model

Provide a clear proposed model, including:

- Suggested classes or structures.
- Proposed fields.
- Field types where appropriate.
- Relationships between structures.
- Required versus optional information.
- How missing or unknown metadata should be represented.

Explain the purpose of each major part of the model.

If useful, provide a conceptual example or pseudocode. Do not provide implementation-ready code that implies authorization to modify the repository.

### 4. Validation design

Explain:

- Which conditions should prevent import.
- Which conditions should generate warnings.
- Which conditions should be preserved without automatically modifying data.
- How the application should communicate validation results.

### 5. Architecture integration proposal

Identify:

- Proposed module responsibilities.
- Existing modules to reuse.
- Any new modules that may be needed.
- How the data model should relate to projects.
- Dependencies or coupling concerns.

### 6. Storage implications

Explain what the data model requires from future persistence, without selecting or implementing a permanent storage architecture.

### 7. Decisions requiring approval

List any unresolved decisions that require my approval.

Separate:

- Decisions already approved by existing documentation.
- Recommendations that remain within existing authority.
- New architectural or scientific decisions requiring approval.

### 8. Proposed implementation breakdown

Recommend the appropriate implementation boundaries for the next tasks:

- Subtask 2.2.2 — FITS import and validation.
- Subtask 2.2.3 — Project integration and provisional persistence.
- Subtask 2.2.4 — Testing, documentation, and completion verification.

Identify dependencies between them.

Do not assume these boundaries are final if the investigation reveals a better division. Explain any proposed changes.

### 9. Testing strategy

Recommend tests for the proposed data model and FITS inspection/import interfaces.

Distinguish between:

- Unit tests.
- FITS fixture tests.
- Tests using the actual Kepler dataset.
- Project integration tests.
- Scientific metadata and integrity tests.

Do not weaken or replace existing tests.

### 10. Documentation impact assessment

Identify which existing documentation will likely need updates during subsequent implementation.

Do not edit those documents now.

---

## 10. Scope Restrictions

This is strictly a PLAN task.

**You may:**
- Read repository files.
- Inspect the actual FITS dataset.
- Run read-only inspection commands.
- Run existing tests only if needed to establish or verify the baseline.
- Examine existing documentation and decisions.
- Produce a design proposal and implementation recommendations.

**You may not:**
- Create or modify source files.
- Create or modify tests.
- Modify documentation.
- Modify Foundation documents.
- Install or upgrade dependencies.
- Change project configuration.
- Change the dataset.
- Commit or push changes.
- Begin implementation.
- Make unapproved architectural or scientific decisions.

If a necessary investigation cannot be completed, clearly report the limitation rather than filling the gap with assumptions.

---

## 11. Final Instruction

Finish by presenting the complete planning report.

Clearly distinguish verified findings, assumptions, recommendations, and unresolved decisions.

Do not begin Subtask 2.2.2.

Stop and wait for review and explicit authorization before any Build-mode work.



# BUILD MODE PROMPT


# Subtask 2.2.1 — FITS Inspection and Light-Curve Data Model

## Mode: BUILD

Implement the approved data-model design for the initial light-curve import workflow.

This Build task is authorized only after the corresponding Plan report has been reviewed and explicitly approved.

**The approved Plan report is the implementation specification. Do not independently expand, reinterpret, or replace its approved design.**

---

## 1. Project Context

Repository:

`C:\Code\New_Project`

GitHub:

https://github.com/brettadin/New_Project

The application is a local desktop astronomy research application using:

- Python 3.13
- PySide6
- NumPy
- SciPy
- Astropy
- Matplotlib (QtAgg)
- pytest

The project already has project lifecycle functionality, including project creation, discovery, opening, saving, closing, dirty-state tracking, and status management.

Stage 2.2 introduces scientific light-curve data import.

The initial scientific dataset is:

`C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits`

This file is outside the repository and must remain unchanged.

---

## 2. Required Preparation

Before implementation:

1. Read the root `AGENTS.md` completely.
2. Review the approved Subtask 2.2.1 Plan report.
3. Review the relevant Foundation requirements identified during planning.
4. Reinspect the current repository state.
5. Review the existing project lifecycle implementation and relevant tests.
6. Verify that the proposed implementation still matches the current codebase.
7. Identify the exact files expected to change.
8. Identify documentation that will need updating under the project's documentation-maintenance requirements.
9. Confirm that all implementation decisions have already been approved.

Do not rely solely on an earlier repository snapshot or the Plan report if the current code has changed.

If the approved Plan report is unavailable, or if an unresolved architectural or scientific decision prevents implementation, stop and report the issue.

Do not silently make a new decision on the user's behalf.

---

## 3. Implementation Scope

Implement only the approved light-curve data-model design.

The implementation should establish a clear representation of an imported astronomical light-curve dataset, including the approved structures for:

### A. Source information

As specified by the approved Plan, support appropriate representation of:

- Original source-file path.
- Original filename.
- Source identifier, when available.
- Source information, when available.
- Import date/time, if approved.
- Source-file availability information, if approved.

Do not claim that storing a source path provides complete scientific provenance.

### B. Measurement data

Implement the approved representation of:

- Observation timestamps.
- Flux measurements.
- Flux uncertainties.
- Observation identifiers or cadence numbers.
- Data-quality flags.
- Missing or invalid measurements.
- Measurement-column identity.

Preserve the distinction between separate measurement columns.

For the initial Kepler dataset, `SAP_FLUX` and `PDCSAP_FLUX` must remain distinguishable.

Do not merge or treat them as interchangeable.

### C. Scientific metadata

Implement the approved representation of relevant metadata, including where available:

- Measurement units.
- Time units.
- Time reference or epoch.
- Time system or scale.
- Instrument or mission information.
- Observation cadence.
- Original column names.
- Relevant source metadata.

Missing or unknown metadata must not be silently replaced with assumed values.

### D. Validation information

Implement only the validation-related structures approved in the Plan.

The data model should be capable of representing relevant validation findings, such as:

- Missing required information.
- Missing optional information.
- Non-finite values.
- Invalid timestamps.
- Missing uncertainty values.
- Nonzero quality flags.
- Unsupported or ambiguous metadata.

Maintain the distinction between errors and warnings.

Do not introduce automatic filtering or data removal unless explicitly approved.

### E. Original and derived data distinctions

Maintain the approved separation between:

1. Original source measurements.
2. Imported representations of those measurements.
3. Future derived or transformed measurements.

Do not implement normalization, filtering, detrending, quality filtering, or other scientific processing operations as part of this task.

---

## 4. Architecture Requirements

Follow the approved Plan and existing project architecture.

In particular:

- Keep scientific data structures appropriately separated from project metadata.
- Avoid placing large measurement arrays directly inside `ProjectMetadata` unless explicitly approved.
- Maintain appropriate separation between scientific data, UI functionality, and persistence.
- Reuse existing interfaces where appropriate.
- Avoid unnecessary dependencies and abstractions.
- Preserve compatibility with the existing project lifecycle.
- Avoid introducing a permanent storage architecture prematurely.

Do not introduce a database, file-copying system, or new persistence mechanism unless the approved Plan explicitly authorizes it.

Decision D6 remains authoritative unless a subsequent decision has been formally approved.

---

## 5. Data Integrity Requirements

The selected Kepler FITS file is read-only.

Do not:

- Modify the original FITS file.
- Move or rename it.
- Delete it.
- Replace it with a synthetic dataset.
- Silently discard observations.
- Silently modify measurement values.
- Treat missing metadata as known information.
- Conflate different measurement columns.

The data model must preserve the scientific distinctions identified in the approved design.

Do not claim that the implementation provides complete data provenance or reproducibility if those capabilities have not yet been implemented.

---

## 6. Testing Requirements

Create or update automated tests according to the approved Plan.

Testing should cover the implemented data model and its validation behavior.

Where applicable, test:

- Valid data-model construction.
- Required and optional fields.
- Missing metadata.
- Measurement-column distinctions.
- Uncertainty representation.
- Quality-flag representation.
- Missing and non-finite values.
- Validation errors and warnings.
- Preservation of source information.
- Appropriate handling of unknown units and time conventions.
- Any approved serialization or conversion behavior.

Use controlled test fixtures where appropriate.

Do not weaken existing tests, remove assertions, or substitute synthetic data for real scientific observations in the application workflow.

Do not introduce tests for functionality that belongs to later subtasks merely to make this task appear more complete.

Run the relevant targeted tests and the complete test suite.

Report actual results, including failures.

---

## 7. Documentation Requirements

Follow the documentation-maintenance requirements in `AGENTS.md`.

Update relevant documentation when the implementation changes:

- Data models.
- Module responsibilities.
- Interfaces.
- Architecture.
- Validation behavior.
- Testing strategy.
- Development progress.

Likely affected documentation should have been identified during Plan mode.

Do not modify Foundation documents.

Do not make unrelated roadmap or documentation changes.

Before completion, compare the final documentation against the actual source code and tests.

Report:

- Documents changed.
- Documents reviewed but intentionally unchanged.
- Any documentation gaps that remain.

---

## 8. Explicitly Excluded Work

The following work belongs to later subtasks and is not authorized here:

### Subtask 2.2.2 — FITS Import and Validation

Do not implement:

- A complete FITS file importer.
- File-selection UI.
- FITS parsing workflows.
- Import dialogs.
- Full dataset extraction from the selected file.
- User-facing import workflows.

### Subtask 2.2.3 — Project Integration and Provisional Persistence

Do not implement:

- Full project association workflows.
- Dataset persistence.
- Database changes.
- Project save/reopen integration for scientific datasets.
- Permanent storage architecture.

### Subtask 2.2.4 — Testing and Completion Verification

Do not attempt to complete the entire Stage 2.2 testing and verification milestone here.

Only create and run tests necessary for the approved data-model implementation.

### Later stages

Do not implement:

- Data tables.
- Light-curve visualization.
- BLS analysis.
- Scientific processing operations.
- Analysis history.
- Analysis replay.
- External archive integration.

---

## 9. Scope and Change Control

Implement only the approved design.

If implementation reveals:

- An architectural conflict.
- An inconsistency with Foundation requirements.
- An unsupported assumption.
- A need for an additional dependency.
- A new scientific or data-model decision.
- A significant change to the approved scope.

Stop the affected work and report the issue.

Do not silently expand the implementation or make unapproved architectural decisions.

Preserve all existing functionality.

Do not perform unrelated refactoring.

Do not commit, push, reset, clean, or otherwise modify Git history.

---

## 10. Final Verification and Report

After implementation:

1. Review every modified source file.
2. Review every modified test.
3. Run the relevant targeted tests.
4. Run the complete test suite.
5. Report actual test results.
6. Confirm that the original Kepler FITS file remains unchanged.
7. Confirm that no excluded functionality was implemented.
8. Compare documentation against the resulting implementation.
9. Identify any unresolved issues or deferred work.

Provide a final report containing:

### A. Implementation summary
What was implemented and why.

### B. Files changed
List every created, modified, or deleted file and explain its purpose.

### C. Data-model summary
Explain the resulting model and its major fields and relationships.

### D. Testing results
Provide actual commands and results.

### E. Data-integrity verification
Explain how original measurements and scientific metadata are represented and protected.

### F. Documentation updates
Identify changed and intentionally unchanged documents.

### G. Scope compliance
Confirm whether implementation remained within the approved Plan.

### H. Remaining work
Identify anything intentionally deferred to Subtasks 2.2.2–2.2.4.

---

## 11. Completion Boundary

This task is complete when the approved light-curve data model has been implemented, tested, and documented.

Do not begin Subtask 2.2.2.

Do not proceed to another Stage 2.2 task without separate review and explicit authorization.

Stop after providing the final implementation report.