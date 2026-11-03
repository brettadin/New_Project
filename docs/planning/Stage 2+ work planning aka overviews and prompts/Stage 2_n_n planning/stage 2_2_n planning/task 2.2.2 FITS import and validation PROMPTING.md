# PLAN MODE PROMPT

# Subtask 2.2.2 — FITS Import and Validation

## Mode: PLAN ONLY

Inspect the current application architecture and the approved implementation from Subtask 2.2.1. Develop a detailed implementation plan for reading astronomical FITS light-curve files, extracting measurements and metadata, validating the contents, and producing the approved internal light-curve data model.

**Do not implement anything. Do not create, modify, delete, or overwrite files.**

This task is limited to FITS reading, extraction, and validation. Full project integration and scientific-data persistence belong to Subtask 2.2.3.

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

The project already includes project lifecycle functionality:

- Create projects.
- Discover and open projects.
- Save and close projects.
- Track unsaved changes.
- Manage project statuses.
- Persist project metadata.

Stage 2.2 introduces scientific light-curve import.

The overall objective is to import real astronomical light-curve data into a project while preserving its scientific measurements, metadata, and provenance.

---

## 2. Required Preparation

Before planning:

1. Read the root `AGENTS.md` completely.
2. Read the relevant Foundation requirements. Foundation documents are authoritative and read-only.
3. Read the current development roadmap and development log.
4. Review the approved Subtask 2.2.1 Plan report.
5. Inspect the actual Subtask 2.2.1 implementation and its tests.
6. Review the resulting data model, interfaces, validation structures, and module responsibilities.
7. Review existing project lifecycle and data-reference functionality.
8. Review relevant scientific review documents and decision records.
9. Verify the current repository state and test baseline.

Do not rely solely on the previous planning conversation or historical reports. The current repository and approved implementation are authoritative for the implementation plan.

If Subtask 2.2.1 has not been implemented, stop and report that Subtask 2.2.2 depends on it. Do not design an importer around an assumed data model.

Identify relevant documentation and any missing documentation. Do not modify any files.

---

## 3. Selected Scientific Dataset

The initial target is the existing Kepler-10b FITS dataset.

Local path:

`C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits`

Filename:

`kplr011904151-2009131105131_llc_full.fits`

This file is outside the repository and must remain outside the repository.

It is read-only.

Do not move, rename, overwrite, modify, or delete it.

Previously established characteristics include:

- FITS format.
- Kepler long-cadence photometry.
- Approximately 9.7 days of observations.
- Approximately 476 observation rows.
- `TIME` values using the BKJD time reference and TDB time system.
- `SAP_FLUX` and `PDCSAP_FLUX` measurement columns.
- Corresponding uncertainty columns.
- `SAP_QUALITY` quality flags.
- `CADENCENO` cadence identifiers.
- Approximately four missing flux measurements.
- Approximately 37 observations with nonzero quality flags.

These details must be verified against the actual local dataset if it is accessible.

Do not substitute synthetic data or another dataset for the real Kepler file.

If the file cannot be accessed, report that limitation and distinguish previously established information from currently verified findings.

---

## 4. Investigation A — Existing Data Model and Import Interfaces

Inspect the implementation produced by Subtask 2.2.1.

Determine:

1. What classes or structures represent a light-curve dataset?
2. How are source-file references represented?
3. How are measurement columns represented?
4. How are uncertainties associated with their measurements?
5. How are quality flags and cadence identifiers represented?
6. How are units and time conventions represented?
7. How are missing or unknown metadata values represented?
8. How are validation findings represented?
9. How are errors distinguished from warnings?
10. What constructors, methods, or interfaces should the importer use?

Identify any assumptions or limitations in the existing model that affect FITS import.

Do not redesign the data model merely because another design might be preferable.

If the model cannot adequately represent the selected FITS dataset, identify the specific incompatibility and propose the smallest necessary correction. Do not implement that correction or silently expand the scope.

The importer must use the approved model rather than creating a competing representation.

---

## 5. Investigation B — FITS Reading and HDU Identification

Inspect the actual Kepler FITS file using Astropy where available.

Determine how the importer should:

1. Open FITS files safely.
2. Inspect the available HDUs.
3. Identify the appropriate light-curve table.
4. Distinguish primary headers from table-extension headers.
5. Inspect column names, types, shapes, and units.
6. Retrieve relevant header metadata.
7. Handle files with missing, unexpected, or ambiguous HDU structures.
8. Close file resources reliably, including when errors occur.

Do not assume the relevant table is always located at the same HDU index.

Assess whether the importer should identify a suitable table by its structure and required columns rather than relying on a fixed position.

Identify which FITS characteristics are general and which are specific to the selected Kepler dataset.

Do not implement a universal FITS framework.

---

## 6. Investigation C — Measurement Extraction

Plan how the importer will extract the supported light-curve measurements.

For the initial Kepler dataset, investigate:

| Column | Purpose |
|---|---|
| `TIME` | Observation timestamps |
| `SAP_FLUX` | Simple Aperture Photometry flux |
| `PDCSAP_FLUX` | Pipeline-corrected flux |
| `SAP_FLUX_ERR` | SAP flux uncertainty |
| `PDCSAP_FLUX_ERR` | PDCSAP flux uncertainty |
| `SAP_QUALITY` | Observation-quality flags |
| `CADENCENO` | Observation cadence identifier |

Determine:

1. How timestamps are extracted.
2. How flux measurements are extracted.
3. How uncertainty values remain associated with the correct flux measurements.
4. How multiple flux columns remain independently accessible.
5. How cadence identifiers are preserved.
6. How quality flags are preserved.
7. How missing or non-finite values are represented.
8. How original column identities are retained.
9. How extracted measurements are passed into the approved data model.

The importer must not merge SAP and PDCSAP measurements or treat them as interchangeable.

Do not silently select one measurement column and discard the others.

Do not perform normalization, filtering, detrending, or other scientific processing.

---

## 7. Investigation D — Scientific Metadata Extraction

Determine how the importer should extract and preserve relevant metadata.

Investigate:

- Time units.
- Time reference or epoch.
- Time system or scale.
- Flux units.
- Instrument and mission information.
- Target identification.
- Observation cadence.
- Relevant FITS header metadata.
- Table-column metadata.
- Original filename and source path.

For the selected Kepler dataset, pay particular attention to:

- BKJD time reference.
- TDB time system.
- Flux units.
- The relationship between the primary and table-extension headers.

Do not assume that a numerical timestamp represents ordinary Julian Date.

Do not silently convert timestamps or units.

Do not invent missing metadata.

If a metadata value cannot be established reliably, determine how the approved data model should represent it as unknown or unavailable.

Identify any FITS-specific metadata that may not fit the existing data model.

---

## 8. Investigation E — Validation Design

Develop a detailed validation strategy using the structures established in Subtask 2.2.1.

### A. File-level validation

Consider:

- Unreadable or corrupted FITS files.
- Invalid FITS structures.
- Unsupported FITS contents.
- Missing or ambiguous measurement tables.
- Files with no usable light-curve measurements.

### B. Structural validation

Consider:

- Missing required columns.
- Missing optional columns.
- Unexpected column types.
- Incompatible column shapes.
- Inconsistent array lengths.
- Missing or ambiguous units and metadata.

### C. Measurement validation

Consider:

- Non-numeric timestamps.
- Non-finite timestamps.
- Non-numeric flux values.
- NaN or infinite flux measurements.
- Missing uncertainty values.
- Non-finite or negative uncertainty values.
- Duplicate or non-monotonic timestamps.

Do not assume every unusual condition must cause import failure. Recommend an appropriate response based on scientific meaning and the approved model.

### D. Quality validation

Preserve original quality flags.

For the Kepler dataset, investigate the nonzero `SAP_QUALITY` values and determine how their presence should be reported.

Do not automatically remove observations with nonzero flags.

Do not create an arbitrary quality-bitmask policy during this task.

### E. Error and warning classification

For each relevant condition, recommend whether it should:

1. Prevent import.
2. Permit import with a warning.
3. Be preserved without modifying the measurements.
4. Require an explicit future user decision.

The proposed behavior must be consistent with the approved validation model.

Do not invent arbitrary thresholds or silently discard measurements.

---

## 9. Investigation F — Import Result and Error Handling

Determine the appropriate interface between the FITS importer and the rest of the application.

The import operation should be capable of producing:

- A successfully constructed light-curve dataset.
- Source information.
- Extracted measurements.
- Scientific metadata.
- Validation results.
- Warnings.
- Import errors.

Determine how to distinguish:

- Successful import without warnings.
- Successful import with warnings.
- Failed import.

Plan meaningful error reporting so the application can explain why a file could not be imported.

Keep the scientific importer independent of UI-specific functionality unless the approved architecture explicitly establishes otherwise.

A file-selection dialog or other user-facing import interface should not be included automatically. Determine whether it belongs to this task or a later integration task based on the actual architecture and approved scope.

---

## 10. Investigation G — Data Integrity and Resource Management

The original FITS file must remain unchanged.

Plan how the importer will ensure:

- Original source measurements are not modified.
- Original source metadata is retained.
- Missing values remain identifiable.
- Quality flags remain available.
- Separate measurement columns remain distinct.
- No silent filtering occurs.
- No normalization or detrending occurs.
- FITS file resources are closed safely.

Determine whether any Astropy or NumPy behaviors could cause unintended data mutation or resource-management problems.

Do not introduce unnecessary copying of large arrays without a reason.

Do not claim complete scientific provenance or reproducibility from the import operation alone.

---

## 11. Investigation H — Testing Strategy

Inspect the existing testing conventions and propose tests for the importer.

Include:

### A. Controlled FITS fixtures

Plan fixtures for:

- A valid FITS light-curve table.
- Multiple HDUs.
- Missing required columns.
- Missing optional columns.
- Unexpected column types.
- Inconsistent column lengths, where constructible.
- NaN and infinite measurements.
- Missing uncertainties.
- Nonzero quality flags.
- Missing or ambiguous metadata.
- Corrupted or unreadable files.
- Unsupported FITS structures.

### B. Actual Kepler dataset

Plan real-data verification using the existing local dataset.

Verify:

- Correct HDU identification.
- Correct column extraction.
- Correct row count.
- Correct metadata.
- Correct uncertainty relationships.
- Correct quality-flag preservation.
- Expected handling of missing values.
- Successful construction of the approved data model.

### C. Data integrity

Determine how tests can establish that:

- The original FITS file is not modified.
- The importer does not silently discard measurements.
- The importer does not silently change units or timestamps.
- Original quality flags remain available.

### D. Test portability

Automated tests must not depend on the user's absolute local dataset path.

Use temporary FITS fixtures for routine tests.

The actual Kepler dataset may be used for optional local integration verification, but its absence on another machine must not cause the standard test suite to fail.

Do not weaken or replace existing tests.

---

## 12. Investigation I — Architecture and Implementation Boundaries

Determine the appropriate module responsibilities and implementation boundaries.

Identify:

- Which existing modules should be reused.
- Whether a dedicated FITS importer module is appropriate.
- Whether separate validation logic is justified.
- How the importer should interact with the approved data model.
- Whether additional dependencies are necessary.
- Whether any proposed changes introduce unnecessary UI coupling.

Astropy is already an approved dependency. Do not recommend another dependency unless there is a specific, demonstrated need.

Keep the implementation focused on FITS import and validation.

Do not implement project persistence or a permanent storage architecture.

---

## 13. Investigation J — Subtask Boundaries

Assess the appropriate division between the remaining Stage 2.2 tasks.

### Subtask 2.2.1 — FITS Inspection and Data-Model Design

Already completed or pending verification.

### Subtask 2.2.2 — FITS Import and Validation

Current task.

Responsible for reading FITS data, extracting measurements and metadata, validating contents, and producing the approved internal data model.

### Subtask 2.2.3 — Project Integration and Provisional Persistence

Future task.

Responsible for associating imported scientific datasets with projects and making them available after project save and reopen.

### Subtask 2.2.4 — Testing, Documentation, and Completion Verification

Future task.

Responsible for broader Stage 2.2 verification, integration testing, documentation reconciliation, and completion assessment.

Identify any overlap or dependencies that need clarification.

Do not implement or plan unrelated future functionality.

---

## 14. Required Planning Deliverable

Produce a structured report containing:

### 1. Repository findings

- Current repository state.
- Relevant files inspected.
- Relevant existing interfaces.
- Existing test conventions.
- Verified test baseline.

### 2. Subtask 2.2.1 implementation review

- Actual data model.
- Actual validation structures.
- Existing interfaces the importer must use.
- Any incompatibilities or gaps.

### 3. FITS inspection findings

- Actual HDU structure.
- Relevant headers.
- Column names, types, shapes, and units.
- Metadata and time conventions.
- Missing or unusual values.
- Differences from previously established dataset information.

### 4. Importer design

- Proposed module and responsibilities.
- FITS opening and HDU identification approach.
- Measurement extraction approach.
- Metadata extraction approach.
- Data-model construction approach.
- Resource-management approach.

### 5. Validation design

Provide a clear table of validation conditions, recommended classifications, and expected behavior.

### 6. Error and warning reporting

Explain how successful imports, imports with warnings, and failed imports will be represented.

### 7. Testing plan

Identify unit tests, FITS fixture tests, real-data verification, and data-integrity tests.

### 8. Architecture and dependency assessment

Identify affected modules, interfaces, and any proposed dependencies.

### 9. Documentation impact assessment

Identify documentation likely to require updates during implementation.

### 10. Decisions requiring approval

Separate:

- Existing approved decisions.
- Recommendations within existing authority.
- New scientific or architectural decisions requiring approval.

### 11. Implementation breakdown

Recommend a practical implementation sequence for Subtask 2.2.2.

Identify any work that should be deferred to Subtask 2.2.3 or 2.2.4.

### 12. Risks and unresolved issues

Identify anything that could prevent reliable implementation or compromise scientific data integrity.

---

## 15. Scope Restrictions

This is strictly a PLAN task.

**Permitted:**

- Read repository files.
- Inspect the actual FITS dataset.
- Run read-only inspection commands.
- Review existing tests.
- Run existing tests if needed to establish the baseline.
- Produce a detailed implementation proposal.

**Not permitted:**

- Create, modify, delete, or overwrite files.
- Implement the FITS importer.
- Implement validation logic.
- Create tests.
- Modify documentation.
- Modify Foundation documents.
- Install or upgrade dependencies.
- Change project configuration.
- Modify the original FITS file.
- Implement project persistence.
- Introduce a permanent storage architecture.
- Commit or push changes.

If a required investigation cannot be completed, report the limitation instead of making assumptions.

---

## 16. Final Instruction

Present the complete planning report.

Clearly distinguish:

- Verified findings.
- Previously established information.
- Assumptions.
- Recommendations.
- Unresolved decisions.

The proposed design must follow the actual Subtask 2.2.1 implementation and existing Foundation requirements.

Do not begin implementation.

Do not begin Subtask 2.2.3.

Stop and wait for review and explicit authorization before any Build-mode work.



# BUILD MODE PROMPT

# Subtask 2.2.2 — FITS Import and Validation

## Mode: BUILD

Implement the approved FITS import and validation design for astronomical light-curve datasets.

This task is authorized only after the corresponding Plan report has been reviewed and explicitly approved.

The approved Plan report and the completed Subtask 2.2.1 data model are the implementation specifications.

**Do not independently expand, reinterpret, or replace the approved design.**

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

The application already supports project creation, discovery, opening, saving, closing, dirty-state tracking, and project status management.

Subtask 2.2.1 establishes the internal light-curve data model.

Subtask 2.2.2 implements the actual FITS-reading and validation functionality that produces instances of that model.

The initial target dataset is:

`C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits`

This file is outside the repository and must remain unchanged.

---

## 2. Required Preparation

Before implementation:

1. Read the root `AGENTS.md` completely.
2. Review the approved Subtask 2.2.2 Plan report.
3. Review the completed Subtask 2.2.1 implementation and tests.
4. Review the relevant Foundation requirements.
5. Inspect the current repository state.
6. Confirm that the approved importer design matches the actual codebase.
7. Identify the exact files expected to change.
8. Identify affected documentation.
9. Verify that all required architectural and scientific decisions have been approved.

Do not rely solely on historical reports or earlier repository snapshots.

If Subtask 2.2.1 is incomplete, or if the approved design conflicts with the actual implementation, stop and report the problem.

If an unresolved decision prevents implementation, do not make that decision independently.

---

## 3. FITS Reading

Implement the approved FITS-reading functionality using Astropy.

The importer should:

- Accept a FITS file path through the approved interface.
- Open the file safely.
- Inspect the available HDUs.
- Identify the appropriate light-curve table.
- Read relevant primary and extension headers.
- Inspect and extract supported table columns.
- Close FITS resources reliably.
- Handle unreadable, corrupted, unsupported, or structurally invalid files appropriately.

Do not assume that the first HDU always contains the relevant measurements.

Use the approved HDU-identification approach rather than relying on an unjustified fixed HDU index.

Keep FITS-reading responsibilities separate from UI functionality unless the approved architecture explicitly authorizes UI integration.

---

## 4. Measurement Extraction

Implement extraction of the measurement fields supported by the approved design.

For the initial Kepler dataset, the relevant columns include:

| Column | Purpose |
|---|---|
| `TIME` | Observation timestamps |
| `SAP_FLUX` | Simple Aperture Photometry flux |
| `PDCSAP_FLUX` | Pipeline-corrected flux |
| `SAP_FLUX_ERR` | SAP flux uncertainty |
| `PDCSAP_FLUX_ERR` | PDCSAP flux uncertainty |
| `SAP_QUALITY` | Observation-quality flags |
| `CADENCENO` | Observation cadence identifier |

Requirements:

- Preserve the relationship between each flux column and its corresponding uncertainty.
- Keep SAP and PDCSAP measurements distinct.
- Preserve cadence identifiers and quality flags.
- Preserve original column identities.
- Represent missing or non-finite measurements according to the approved data model.
- Preserve the original measurement values.
- Construct the approved internal light-curve data model.

Do not merge separate measurement columns.

Do not silently select one flux column and discard the others.

Do not silently discard observations.

Do not normalize, filter, detrend, resample, or otherwise scientifically process measurements.

---

## 5. Scientific Metadata Extraction

Implement extraction of the scientific metadata approved in the Plan report.

Where available, preserve:

- Time units.
- Time reference or epoch.
- Time system or scale.
- Flux units.
- Instrument information.
- Mission information.
- Target identification.
- Observation cadence.
- Relevant FITS header information.
- Table-column metadata.
- Original filename and source path.

For the selected Kepler dataset, preserve the distinction between:

- BKJD time reference.
- TDB time system.

Do not treat timestamps as ordinary Julian Dates without evidence.

Do not silently convert timestamps, units, or measurement values.

Do not invent missing metadata.

Represent unknown or unavailable metadata according to the approved data model.

Do not claim complete scientific provenance merely because source metadata has been extracted.

---

## 6. Validation Implementation

Implement the validation behavior approved in the Plan report.

### A. File-level validation

Handle:

- Unreadable FITS files.
- Corrupted files.
- Invalid FITS structures.
- Unsupported FITS contents.
- Missing or ambiguous measurement tables.
- Files without usable light-curve measurements.

### B. Structural validation

Handle:

- Missing required columns.
- Missing optional columns.
- Unexpected data types.
- Incompatible column structures.
- Inconsistent array lengths.
- Missing or ambiguous metadata.

### C. Measurement validation

Handle the approved validation cases, including:

- Non-numeric timestamps.
- Non-finite timestamps.
- Non-numeric flux values.
- NaN or infinite flux measurements.
- Missing uncertainty values.
- Non-finite or invalid uncertainty values.
- Duplicate or non-monotonic timestamps.

Do not invent arbitrary scientific thresholds.

Do not automatically classify every unusual measurement as invalid.

### D. Quality validation

Preserve original quality flags.

For the selected Kepler dataset, report the presence of nonzero quality flags.

Do not automatically remove observations with nonzero flags.

Do not implement an unapproved quality-bitmask policy.

Quality filtering belongs to a separately defined scientific operation, not an implicit import behavior.

### E. Error and warning classification

Follow the classifications approved in the Plan report.

Distinguish:

1. Conditions that prevent import.
2. Conditions that permit import with warnings.
3. Conditions that should be preserved without modifying measurements.
4. Conditions requiring future user decisions.

Do not silently discard data to make an import succeed.

---

## 7. Import Results and Error Handling

Implement the approved importer result interface.

It should communicate:

- Whether import succeeded.
- The constructed light-curve dataset, when successful.
- Source information.
- Extracted measurement information.
- Scientific metadata.
- Validation findings.
- Warnings.
- Import errors.

The application or calling service must be able to distinguish:

- Successful import without warnings.
- Successful import with warnings.
- Failed import.

Provide meaningful error information that explains why an import failed.

Avoid generic error handling that hides the underlying cause.

Follow the approved separation between importer logic and UI logic.

Do not introduce a file-selection dialog or broader user-interface workflow unless explicitly included in the approved Plan.

---

## 8. Data Integrity and Resource Management

The original Kepler FITS file is read-only.

The importer must not:

- Modify the original file.
- Move or rename it.
- Delete or replace it.
- Silently change measurement values.
- Silently convert units or timestamps.
- Discard observations without an approved reason.
- Remove quality flags.
- Merge distinct measurement columns.
- Replace missing values with invented values.

Ensure FITS file resources are closed reliably, including when extraction or validation raises an exception.

Use appropriate array handling without unnecessary duplication of large datasets.

Preserve the distinction between original source measurements and future derived measurements.

Do not implement derived-data processing in this task.

---

## 9. Testing Requirements

Create or update tests according to the approved Plan.

### A. FITS-reading tests

Test:

- Valid FITS files.
- Multiple HDUs.
- Appropriate table identification.
- Missing or ambiguous HDUs.
- Unreadable files.
- Corrupted files.
- Unsupported structures.

### B. Measurement extraction tests

Test:

- Timestamp extraction.
- Flux extraction.
- Multiple flux columns.
- Corresponding uncertainty relationships.
- Cadence identifiers.
- Quality flags.
- Missing and non-finite values.
- Preservation of original column identities.

### C. Metadata tests

Test:

- Measurement units.
- Time units.
- Time references.
- Time systems.
- Relevant FITS header metadata.
- Missing or unknown metadata.

### D. Validation tests

Test:

- Missing required columns.
- Missing optional columns.
- Invalid data types.
- Inconsistent structures.
- Non-finite measurements.
- Missing uncertainties.
- Invalid timestamps.
- Nonzero quality flags.
- Correct error-versus-warning classification.

### E. Data-integrity tests

Verify that:

- Original source measurements are not silently modified.
- Quality flags remain available.
- Distinct measurement columns remain distinct.
- Missing values remain identifiable.
- The original FITS file remains unchanged.

### F. Real-data verification

Use the existing Kepler-10b dataset when available.

Verify:

- Correct HDU identification.
- Correct measurement extraction.
- Expected row count.
- Correct metadata.
- Correct uncertainty relationships.
- Quality-flag preservation.
- Expected missing-value handling.
- Successful construction of the approved data model.

Do not make the standard automated test suite dependent on the user's absolute local dataset path.

Use temporary FITS fixtures for routine automated tests.

The absence of the real Kepler dataset on another machine must not cause the standard test suite to fail.

Do not weaken or remove existing tests.

Run relevant targeted tests and the complete test suite.

Report actual results.

---

## 10. Architecture and Dependency Restrictions

Follow the approved architecture and existing module responsibilities.

- Reuse the completed Subtask 2.2.1 data model.
- Use Astropy, which is already an approved dependency.
- Avoid unnecessary new dependencies.
- Keep scientific import logic separate from the UI.
- Avoid unnecessary coupling with project lifecycle code.
- Preserve existing project functionality.
- Do not introduce a competing data model.

Do not introduce a database, permanent storage architecture, or project-level dataset persistence mechanism.

Decision D6 remains authoritative unless a subsequent decision has been formally approved.

---

## 11. Documentation Requirements

Follow the documentation-maintenance instructions in `AGENTS.md`.

Update relevant documentation when the implementation changes:

- Importer interfaces.
- Module responsibilities.
- FITS-reading behavior.
- Metadata extraction.
- Validation rules.
- Error and warning behavior.
- Testing strategy.
- Development progress.

Likely affected documents should have been identified during Plan mode.

Do not modify Foundation documents.

Do not make unrelated documentation changes.

Before completion, compare documentation against the actual source code and tests.

Report:

- Documents changed.
- Documents reviewed but intentionally unchanged.
- Any remaining documentation gaps.

---

## 12. Explicitly Excluded Work

The following functionality is outside this Build task.

### Subtask 2.2.3 — Project Integration and Provisional Persistence

Do not implement:

- Full project association workflows.
- Scientific dataset persistence.
- Database changes.
- Project save/reopen integration for imported datasets.
- Permanent storage architecture.
- Dataset management across multiple projects.

### Subtask 2.2.4 — Testing and Completion Verification

Do not attempt to complete the entire Stage 2.2 verification milestone.

Only implement and run tests required for the importer.

Broader integration and completion verification remain for 2.2.4.

### Subtask 2.3 — Data Table and Visualization

Do not implement:

- Measurement tables.
- Interactive light-curve plots.
- Zooming and panning.
- Observation selection.
- Visualization controls.

### Subtask 2.4 — BLS Analysis and Uncertainty

Do not implement:

- Transit searches.
- Periodograms.
- BLS analysis.
- Transit parameter estimation.
- Period uncertainty calculations.
- False-alarm probability calculations.

### Subtask 2.5 — Analysis Operation Records

Do not implement:

- Analysis history.
- Operation records.
- Parameter tracking.
- Analysis replay.

### Later stages

Do not implement external archive integration, automatic data downloads, or unrelated astronomical data formats beyond the approved scope.

---

## 13. Scope and Change Control

Implement only the approved Plan.

If implementation reveals:

- An architectural conflict.
- An inconsistency with Foundation requirements.
- An incompatibility with the completed data model.
- An unsupported scientific assumption.
- A need for an additional dependency.
- A new architectural or scientific decision.
- A significant change to the approved scope.

Stop the affected work and report the issue.

Do not silently expand the implementation or make unapproved decisions.

Preserve existing functionality.

Do not perform unrelated refactoring.

Do not commit, push, reset, clean, or otherwise alter Git history.

---

## 14. Final Verification and Report

After implementation:

1. Review every modified source file.
2. Review every modified test.
3. Run relevant targeted tests.
4. Run the complete test suite.
5. Report actual commands and results.
6. Verify the original Kepler FITS file remains unchanged.
7. Confirm that the importer uses the approved 2.2.1 data model.
8. Confirm that no excluded functionality was implemented.
9. Compare documentation against the resulting implementation.
10. Identify unresolved issues and deferred work.

Provide a final report containing:

### A. Implementation summary
What was implemented and why.

### B. Files changed
List every created, modified, or deleted file and explain its purpose.

### C. Importer behavior
Explain how FITS files are opened, inspected, and extracted.

### D. Metadata and validation
Explain what metadata is preserved and how warnings and errors are handled.

### E. Data-integrity verification
Explain how original measurements, quality flags, and metadata are protected.

### F. Testing results
Provide actual test commands and results.

### G. Documentation updates
Identify changed and intentionally unchanged documents.

### H. Scope compliance
Confirm whether implementation remained within the approved Plan.

### I. Remaining work
Identify anything deferred to Subtasks 2.2.3 and 2.2.4.

---

## 15. Completion Boundary

This task is complete when the approved FITS importer can reliably read the selected astronomical FITS dataset, extract its supported measurements and scientific metadata, validate its contents, and construct the approved internal light-curve data model.

Do not begin Subtask 2.2.3.

Do not proceed to another Stage 2.2 task without separate review and explicit authorization.

Stop after providing the final implementation report.