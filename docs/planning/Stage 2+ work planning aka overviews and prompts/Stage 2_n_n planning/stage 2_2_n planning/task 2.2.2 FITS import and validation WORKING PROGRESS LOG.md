# getting chatgpt to read the files initially

Yes. I still have the context for Stage 2, Subtask 2.2, including the approved 2.2.1 design, implementation scope, FITS inspection findings, and the 224-test result.

I located and read the requested `task 2.2.2 FITS import and validation OVERVIEW.md` in the uploaded repository snapshot.

One qualification: I inspected the uploaded snapshot, not your live working directory.

## Subtask 2.2.2 — What the overview establishes

Primary objective: Implement a FITS importer that reads a real astronomical light-curve file, extracts its measurements and metadata, validates the data, and constructs the `LightCurveDataset` model implemented in 2.2.1.

The overview divides the work into four main areas:

| Area            | Required functionality                                                                     |
| --------------- | ------------------------------------------------------------------------------------------ |
| FITS reading    | Open FITS files, inspect HDUs, identify the appropriate light-curve table                  |
| Data extraction | Extract time, SAP/PDCSAP flux, uncertainties, quality flags, and cadence numbers           |
| Metadata        | Preserve time conventions, units, instrument, mission, target, and source-file information |
| Validation      | Detect structural problems, missing values, non-finite measurements, and quality flags     |

### Important requirements

1. Do not assume the first HDU contains the measurements. Identify the appropriate table.
2. Preserve SAP_FLUX and PDCSAP_FLUX independently, including their corresponding uncertainty columns.
3. Preserve the Kepler time convention: BKJD, with the TDB time system. Do not silently convert timestamps.
4. Preserve non-finite values and quality flags. Do not automatically discard observations.
5. Distinguish fatal import errors from warnings.
6. Never modify the original FITS file.
7. Keep the importer independent of the GUI unless UI integration is explicitly approved.
8. Use temporary FITS fixtures for controlled tests, and the real Kepler dataset for verification when available.
9. Do not depend on an absolute, user-specific file path in automated tests.

## How this connects to 2.2.1

The model we just implemented provides the destination for the importer.

| FITS information                          | 2.2.1 model destination              |
| ----------------------------------------- | ------------------------------------ |
| Source filename/path and archive metadata | `DatasetSource`                      |
| TIME and its scientific conventions       | `TimeInfo`                           |
| SAP_FLUX and PDCSAP_FLUX                  | Separate `MeasurementColumn` objects |
| SAP_FLUX_ERR and PDCSAP_FLUX_ERR          | Corresponding `uncertainties` arrays |
| SAP_QUALITY                               | `quality_flags`                      |
| CADENCENO                                 | `cadence_numbers`                    |
| Import warnings and findings              | `ValidationReport`                   |
| Complete imported dataset                 | `LightCurveDataset`                  |

This is a direct continuation of the architecture we established. We should not need to redesign the data model to accommodate the initial Kepler importer unless implementation reveals a genuine incompatibility.

## Boundaries

The overview explicitly keeps these features outside 2.2.2:

- Project association — 2.2.3.
- Dataset persistence and reopening — 2.2.3.
- Data table and interactive graph — 2.3.
- BLS analysis — 2.4.
- Analysis operation records — 2.5.

Documentation updates are expected, but we should continue consolidating those for 2.2.4 rather than scattering them across subtasks.

## Recommended next step

Overview reviewed

We should move to the 2.2.2 PLAN review, not directly into implementation.

The plan should establish:

- Which module will contain the importer.
- How FITS HDU and column detection will work.
- How the importer maps FITS metadata into the existing model.
- How it reports failures versus warnings.
- How real-data and temporary-fixture testing will work.
- Which existing files, if any, need modification.

I also have the earlier Kepler FITS inspection findings available as context, including the 476-row `LIGHTCURVE` table, distinct SAP/PDCSAP measurements, non-finite values, and 37 nonzero quality flags.

One thing: I will coordinate the running implementation record with the copy you saved. If you want me to update that exact document later, provide your copy when we reach the documentation stage.


# me

ok now look at `docs\planning\Stage 2+ work planning aka overviews and prompts\Stage 2_n_n planning\stage 2_2_n planning\task 2.2.2 FITS import and validation PROMPTING.md` check out the plan prompt we have there, does it need revision/updating? 
When you're done give me the revised prompt to send off to nemotron 3.5 super VL


# chatgpt response / prompt

* in a new chat on opencode* 

The existing PLAN prompt is thorough, but I recommend revising it before sending it to Nemotron.

It has the right overall investigation areas. The main issue is that it was written before 2.2.1 was implemented, so some instructions and dataset descriptions need to be brought into line with the current state.

I identified four important improvements:

1. Make the completed 2.2.1 implementation authoritative. Nemotron must inspect the actual `src/light_curve.py` and its tests, rather than plan around the earlier design alone.
2. Correct the FITS reference information. The previous inspection established different non-finite counts for SAP and PDCSAP, not simply four missing flux measurements.
3. Clarify the 2.2.2 boundary. The importer constructs a `LightCurveDataset`; it does not attach it to a project or persist it. Those remain 2.2.3 responsibilities.
4. Make the planning deliverable more decision-oriented. Nemotron should recommend concrete interfaces, module locations, validation classifications, and tests, while clearly identifying anything requiring your approval.

There is one important repository-state caveat: the uploaded November 4 snapshot contains the planning document and `AGENTS.md`, but does not contain `src/light_curve.py` or `tests/test_light_curve.py`. That snapshot therefore predates the implementation report you supplied, or is otherwise incomplete. The revised prompt explicitly tells Nemotron to inspect your actual working repository and verify those files before proceeding.

I also tightened the Foundation/documentation instructions to follow `AGENTS.md`, without authorizing any file changes during PLAN mode.

## Revised PLAN prompt

Send this to Nemotron 3.5 Super VL in PLAN mode.

# PLAN MODE — Subtask 2.2.2: FITS Import and Validation

## Operating mode and authorization

**PLAN ONLY. No implementation or file modifications are authorized.**

Inspect the current repository, the completed Subtask 2.2.1 implementation, the relevant Foundation requirements, and the selected Kepler FITS dataset.

Produce a detailed, technically grounded implementation plan for a FITS importer that:

1. Reads astronomical FITS light-curve files.
2. Identifies the appropriate light-curve table.
3. Extracts supported measurements and their uncertainties.
4. Preserves scientific metadata and source information.
5. Validates the imported contents.
6. Constructs the existing `LightCurveDataset` model from Subtask 2.2.1.

The importer must use the existing approved data model. Do not redesign it or create a competing scientific representation.

**Do not create, modify, delete, rename, or overwrite any files. Do not install dependencies, change configuration, or modify the original FITS dataset.**

This task is limited to FITS reading, extraction, and validation. Project association and scientific-data persistence belong to Subtask 2.2.3.

---

## 1. Repository and project context

Repository:

`C:\Code\New_Project`

GitHub:

`https://github.com/brettadin/New_Project`

The application is a local desktop astronomy research application using:

- Python 3.13
- PySide6
- NumPy
- SciPy
- Astropy
- Matplotlib (QtAgg)
- pytest

The application already has project lifecycle functionality, including project creation, discovery, opening, saving, closing, and metadata persistence.

Stage 2.2 introduces scientific light-curve import.

### Current task status

- Subtask 2.2.1 — FITS inspection and light-curve data-model design: implemented.
- Subtask 2.2.2 — FITS import and validation: current task.
- Subtask 2.2.3 — Project association and provisional persistence: future task.
- Subtask 2.2.4 — Testing, documentation, and completion verification: future task.

The 2.2.1 implementation report supplied by the user states:

- `src/light_curve.py` was created.
- `tests/test_light_curve.py` was created.
- The focused model tests passed: 48.
- The full suite passed: 224 tests.
- The previous full-suite baseline was 176 tests.
- No existing files were modified for that implementation.
- No commits or pushes were made.

These are reported results, not a substitute for inspecting the actual repository.

### Important repository-state verification

Before planning:

1. Inspect the actual working tree.
2. Confirm that `src/light_curve.py` exists.
3. Confirm that `tests/test_light_curve.py` exists.
4. Inspect their actual contents.
5. Confirm the current Git status.
6. Check whether there are uncommitted or untracked files.
7. Distinguish existing user changes from files created by the current task.

If the implementation files are absent, do not invent their contents or plan against the earlier design as if it were implemented. Stop and report the discrepancy.

Do not overwrite, delete, reset, clean, or otherwise disturb existing user changes.

---

## 2. Required project and Foundation preparation

Read the root `AGENTS.md` completely and follow its requirements.

Before developing the plan, inspect:

- `docs/README.md`
- `docs/MASTER_DEVELOPMENT_ROADMAP.md`
- `docs/development/DEVELOPMENT_LOG.md`
- `docs/development/UNRESOLVED_QUESTIONS.md`
- Relevant decision records under `docs/development/decisions/`
- Relevant scientific and technical review documents
- Relevant module responsibility and architecture documentation

Consult the Foundation using its index and relevant detailed sections.

At minimum, identify the authoritative requirements relevant to:

- Photometry and time-series data.
- Scientific data integrity and validation.
- Data provenance.
- Application architecture and module responsibilities.
- Platform and dependency constraints.
- Development planning, approval, and testing boundaries.

Use `docs/Foundation/0_index.md` to locate the appropriate detailed Foundation documents. Read the actual relevant documents rather than relying on summaries.

Foundation documents are authoritative and read-only.

In the planning report, cite original relative document paths and relevant sections/headings when relying on Foundation requirements.

Do not modify any documentation during this PLAN task.

### Authority and evidence

Distinguish clearly between:

- Verified repository facts.
- Verified FITS inspection findings.
- Previously established findings that still require verification.
- Existing approved decisions.
- Recommendations.
- Assumptions.
- Decisions requiring user approval.

Do not present recommendations as approved decisions.

Do not rely solely on this prompt or historical conversation. The current repository, Foundation, and actual dataset are authoritative.

---

## 3. Selected scientific dataset

The initial target is the existing Kepler-10b FITS dataset.

Local path:

`C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits`

Filename:

`kplr011904151-2009131105131_llc_full.fits`

The dataset is outside the repository and must remain outside the repository.

It is read-only.

Do not move, rename, overwrite, modify, or delete it.

### Previously established FITS inspection findings

The file was previously inspected using Astropy. The following findings should guide the investigation, but must be checked against the actual file if it is accessible.

| Property         | Previously observed result                            |
| ---------------- | ----------------------------------------------------- |
| HDUs             | PrimaryHDU, LIGHTCURVE BinTableHDU, APERTURE ImageHDU |
| LIGHTCURVE table | 476 rows, 20 columns                                  |
| TIME             | float64, days, BKJD convention                        |
| TIME range       | Approximately 120.539–130.245                         |
| CADENCENO        | int32, 568–1043, consecutive                          |
| SAP_FLUX         | float32, e-/s, 4 non-finite values                    |
| SAP_FLUX_ERR     | 4 non-finite values, same rows as SAP_FLUX            |
| PDCSAP_FLUX      | float32, e-/s, 7 non-finite values                    |
| PDCSAP_FLUX_ERR  | 7 non-finite values, same rows as PDCSAP_FLUX         |
| SAP_QUALITY      | Integer quality bitmask; 37 of 476 values nonzero     |
| PSF_CENTR1/2     | Entirely non-finite                                   |
| MOM_CENTR1/2     | 4 non-finite values each                              |
| POS_CORR1/2      | 7 non-finite values each                              |

Previously observed header metadata includes:

- `TELESCOP`: Kepler
- `INSTRUME`: Kepler Photometer
- `OBJECT`: KIC 11904151
- `KEPLERID`: 11904151
- `MISSION`: Kepler
- `ORIGIN`: NASA/Ames
- `TIMESYS`: TDB
- `TIMEREF`: SOLARSYSTEM
- `BJDREFI`: 2454833
- `BJDREFF`: 0
- `TIMEUNIT`: d

The exact values, headers, units, and column metadata must be verified if the actual file is accessible.

If it is not accessible, report that limitation. Do not substitute another dataset or synthetic data for real-data verification.

Clearly distinguish previous findings from current inspection results.

---

## 4. Investigation A — Completed light-curve model

Inspect the actual implementation from Subtask 2.2.1, including its tests.

At minimum, inspect:

- `src/light_curve.py`
- `tests/test_light_curve.py`

Determine the actual interfaces, types, constructors, validation behavior, and serialization behavior.

The reported model components are:

- `DatasetSource`
- `TimeInfo`
- `MeasurementColumn`
- `MeasurementSeries`
- `ValidationFinding`
- `ValidationReport`
- `LightCurveDataset`

Verify their actual implementations rather than assuming the report is exact.

Determine:

1. How source filename and path are represented.
2. How source identity, archive, mission, instrument, and target are represented.
3. How time values and time metadata are represented.
4. How measurement values and units are represented.
5. How uncertainty arrays are associated with measurements.
6. How quality flags and cadence numbers are represented.
7. How validation findings and reports are constructed.
8. How structural validation behaves.
9. How non-finite values are preserved.
10. How arrays are copied and typed.
11. How `to_dict()` and `from_dict()` behave.
12. How the importer should construct a valid dataset.

The importer must use the actual model interfaces.

Do not redesign the data model simply because another structure might be preferable.

If the model cannot adequately represent the selected FITS dataset, identify the exact incompatibility and propose the smallest necessary correction. Do not implement it or silently expand scope.

### Specific integration questions

Investigate how the importer should handle:

- `TimeInfo.values` as float64.
- `MeasurementColumn.values` as float64.
- Optional uncertainty arrays.
- Optional integer quality flags.
- Optional integer cadence numbers.
- Empty strings for unknown units.
- `None` for absent uncertainties.
- `DatasetSource.original_file_path`.
- `ValidationReport` warnings and informational findings.
- Dataset UUID and timestamp generation.

The importer must supply the original source-file path for the current local-file workflow.

Do not add project IDs, ownership, permissions, or project metadata to the scientific dataset.

---

## 5. Investigation B — FITS reading and HDU identification

Inspect the actual Kepler FITS file using Astropy if available.

Determine how the importer should:

1. Open FITS files safely.
2. Inspect available HDUs.
3. Identify the appropriate light-curve table.
4. Distinguish primary-header metadata from extension-header metadata.
5. Inspect table-column names, types, dimensions, and units.
6. Retrieve relevant metadata from headers and table columns.
7. Handle missing, unexpected, or ambiguous HDU structures.
8. Close file resources reliably, including when extraction or validation fails.

Do not assume the light-curve table is always at a fixed HDU index.

Evaluate identifying a suitable table by its structure and required columns rather than relying on a fixed position.

Recommend a concrete HDU-identification strategy for the initial Kepler importer.

Identify which aspects are general FITS behavior and which are specific to the selected Kepler product.

Do not build a universal FITS framework.

---

## 6. Investigation C — Measurement extraction

The initial supported Kepler columns are:

| FITS column       | Meaning                         |
| ----------------- | ------------------------------- |
| `TIME`            | Observation timestamps          |
| `SAP_FLUX`        | Simple Aperture Photometry flux |
| `PDCSAP_FLUX`     | Pipeline-corrected flux         |
| `SAP_FLUX_ERR`    | SAP flux uncertainty            |
| `PDCSAP_FLUX_ERR` | PDCSAP flux uncertainty         |
| `SAP_QUALITY`     | Observation-quality flags       |
| `CADENCENO`       | Observation cadence identifier  |

Determine a concrete extraction strategy.

Investigate:

1. How to extract time values.
2. How to extract supported flux measurements.
3. How to associate each uncertainty column with the correct flux column.
4. How to keep SAP and PDCSAP independently identifiable.
5. How to preserve cadence identifiers.
6. How to preserve quality flags.
7. How to represent missing and non-finite values.
8. How to retain original column names and units.
9. How to construct `MeasurementColumn` and `MeasurementSeries` objects.
10. How to construct the final `LightCurveDataset`.

Do not merge SAP and PDCSAP measurements.

Do not silently select one flux series and discard the other.

Do not perform normalization, filtering, detrending, interpolation, or other scientific processing.

### Required design questions

Recommend behavior for these situations:

- Both SAP and PDCSAP are available.
- Only one supported flux series is available.
- A flux column exists but its corresponding uncertainty column is absent.
- A recognized uncertainty column exists but its associated flux column is absent.
- Optional quality or cadence columns are absent.
- Additional numeric columns exist that are not part of the initial supported measurement set.
- A required time column is absent.

Clearly distinguish required columns from optional columns and justify the recommendation.

Do not invent a universal policy for arbitrary FITS tables.

---

## 7. Investigation D — Scientific metadata extraction

Determine how the importer should extract and preserve:

- Time units.
- Time reference or epoch.
- Time system or scale.
- Time reference frame.
- Flux units.
- Mission.
- Instrument.
- Target identity.
- Observation cadence information.
- Relevant primary-header metadata.
- Relevant extension-header metadata.
- Relevant table-column metadata.
- Original filename and source path.

For the Kepler dataset, pay particular attention to:

- BKJD time convention.
- TDB time system.
- `BJDREFI` and `BJDREFF`.
- `TIMEREF`.
- `TIMEUNIT`.
- Flux units.
- The relationship between primary and extension headers.

Do not assume a numerical timestamp represents ordinary Julian Date.

Do not silently convert time values or measurement units.

Do not invent missing metadata.

If metadata cannot be established reliably, represent it as unknown using the existing model's conventions.

Identify any FITS metadata that cannot be represented by the current model and explain whether it is important enough to require a model change or can remain outside the initial scope.

---

## 8. Investigation E — Validation strategy

Develop a concrete validation matrix using the actual `ValidationFinding` and `ValidationReport` interfaces.

Distinguish file-level import failures from dataset-level scientific warnings.

### A. File and FITS structure

Consider:

- Unreadable or missing files.
- Corrupted FITS files.
- Invalid FITS structures.
- Unsupported FITS contents.
- Missing or ambiguous light-curve tables.
- Files with no usable time or measurement columns.

### B. Column and array structure

Consider:

- Missing required columns.
- Missing optional columns.
- Unexpected column types.
- Unsupported or incompatible shapes.
- Inconsistent array lengths.
- Missing units.
- Unknown or ambiguous time metadata.

### C. Measurement quality

Consider:

- Non-numeric timestamps.
- Non-finite timestamps.
- Non-numeric flux values.
- NaN or infinite flux values.
- Missing uncertainty values.
- Non-finite uncertainty values.
- Negative uncertainty values.
- Duplicate timestamps.
- Non-monotonic timestamps.

Do not assume every unusual condition must prevent import.

Recommend whether each condition should:

- Prevent dataset construction.
- Permit import with a warning.
- Be preserved without modification.
- Be reported as informational.
- Require a future user decision.

Explain the scientific reasoning behind consequential classifications.

Do not silently discard observations to make an import succeed.

Do not replace missing values with zero or invented values.

### D. Time validation

Investigate how to report:

- Missing time units.
- Missing time reference.
- Missing time scale.
- Non-finite timestamps.
- Duplicate timestamps.
- Non-monotonic timestamps.
- Unexpected time spacing.

Do not impose arbitrary cadence or time-spacing thresholds.

Do not silently reorder observations.

### E. Uncertainty validation

Investigate how to report:

- Missing uncertainty columns.
- Non-finite uncertainty values.
- Negative uncertainty values.
- Length mismatches.

Do not invent uncertainty values.

Do not replace missing uncertainties with zeros.

Recommend whether questionable uncertainty values should be preserved with warnings or prevent import, and justify the choice.

### F. Quality flags

Preserve original quality flags.

For the Kepler dataset, report the presence and distribution of nonzero quality values.

Do not automatically remove observations with nonzero flags.

Do not implement an unapproved Kepler quality-bitmask interpretation or filtering policy.

Quality filtering belongs to a separately defined scientific operation.

### G. Validation responsibility

Respect the distinction established in 2.2.1:

- Structural model errors prevent construction of an invalid dataset.
- Importer-specific failures that prevent dataset construction must be reported separately to the caller.
- Scientific warnings and informational findings should be retained in the dataset's `ValidationReport` when a valid dataset can still be constructed.

Do not attempt to put importer failures into a validation report belonging to a dataset that was never constructed.

---

## 9. Investigation F — Import result and error-handling interface

The 2.2.1 model does not automatically establish a complete importer result interface.

Inspect existing project conventions and recommend a minimal interface between the FITS importer and its caller.

Determine how to represent:

1. Successful import without warnings.
2. Successful import with warnings.
3. Failed import.

The design must communicate:

- Whether import succeeded.
- The constructed dataset when successful.
- Source information.
- Validation findings.
- Warnings.
- A meaningful failure reason when unsuccessful.

Evaluate whether a dedicated result dataclass, a clear exception-based interface, or another minimal approach is most appropriate.

Explain the trade-offs and recommend one approach.

Do not create a competing scientific data model.

Keep FITS parsing and scientific validation independent of GUI-specific functionality.

Do not introduce file-selection dialogs, import windows, or other UI workflows unless they are explicitly part of the approved scope.

Do not modify the project service or repository to integrate the importer.

---

## 10. Investigation G — Data integrity and resource management

The original FITS file must remain unchanged.

Recommend how the importer will ensure:

- Original source measurements are preserved.
- Original source metadata is retained.
- Missing values remain identifiable.
- Quality flags remain available.
- Distinct measurement columns remain distinct.
- No observations are silently discarded.
- No units or timestamps are silently changed.
- No normalization or detrending occurs.
- FITS resources are closed reliably.

Investigate relevant Astropy and NumPy behaviors, including memory-mapped FITS data and array ownership.

The existing model copies incoming arrays during dataset construction. Account for that behavior when recommending array handling. Avoid unnecessary duplicate copies without compromising data integrity or resource safety.

Do not implement derived-data processing or a provenance system for future analysis operations.

---

## 11. Investigation H — Testing strategy

Inspect existing test conventions and recommend a focused importer test suite.

Do not create tests during PLAN mode.

### A. Temporary FITS fixtures

Recommend fixtures for:

- A valid FITS light-curve table.
- Multiple HDUs.
- A light-curve table not located at HDU index 1.
- Missing required columns.
- Missing optional columns.
- Only SAP or only PDCSAP data.
- Missing uncertainty columns.
- Unexpected column types.
- Incompatible array shapes.
- NaN and infinite measurements.
- Non-finite timestamps.
- Non-finite and negative uncertainties.
- Nonzero quality flags.
- Missing or ambiguous metadata.
- Corrupted or unreadable FITS files.
- Unsupported FITS structures.

Use small controlled fixtures for routine automated tests.

### B. Real Kepler dataset

Plan optional local verification using the actual Kepler-10b FITS file.

Verify:

- Correct HDU identification.
- Expected table dimensions.
- Correct time extraction and conventions.
- Correct SAP and PDCSAP extraction.
- Correct uncertainty relationships.
- Correct units and metadata.
- Quality-flag preservation.
- Cadence-number preservation.
- Expected non-finite-value handling.
- Successful construction of the approved model.

The automated test suite must not depend on the user's absolute local dataset path.

The absence of the real dataset on another machine must not cause standard tests to fail.

### C. Data integrity

Recommend tests establishing that:

- The original FITS file is unchanged.
- Measurements are not silently filtered or transformed.
- Distinct flux columns remain distinct.
- Missing values remain identifiable.
- Quality flags remain available.
- FITS resources are properly closed.

Do not weaken, skip, or replace existing tests.

### D. Test baseline

Inspect the current test configuration and run the existing suite if appropriate to establish a verified baseline.

The reported previous result was 224 passed, but verify the actual current result. Report any differences.

---

## 12. Investigation I — Module architecture and implementation boundaries

Recommend the smallest maintainable module structure for the importer.

Determine:

- Whether a dedicated FITS importer module is appropriate.
- Where the module should reside.
- Whether validation should be contained in the importer or separated.
- Which existing modules should be reused.
- How the importer should depend on `src/light_curve.py`.
- Whether an importer result type is necessary.
- How exceptions should be structured.
- Whether additional dependencies are needed.

Astropy is already an approved dependency.

Do not introduce unnecessary dependencies.

Keep scientific import logic separate from GUI and project lifecycle functionality.

Do not introduce a database, permanent storage architecture, project-level persistence, or a competing data model.

D6 remains deferred unless an existing formally approved decision says otherwise.

---

## 13. Investigation J — Subtask boundaries

Respect the division of responsibility across Stage 2.2.

### 2.2.1 — FITS inspection and data-model design

Implemented.

Provides the scientific data model in `src/light_curve.py`.

### 2.2.2 — FITS import and validation

Current task.

Responsible for:

- Reading FITS files.
- Identifying light-curve tables.
- Extracting supported measurements.
- Extracting scientific metadata.
- Validating imported contents.
- Constructing `LightCurveDataset` objects.
- Reporting import failures and warnings.

### 2.2.3 — Project association and provisional persistence

Future task.

Responsible for:

- Associating datasets with projects.
- Saving and reopening scientific datasets.
- Project-level dataset management.
- Provisional persistence behavior.

Do not implement these features in 2.2.2.

### 2.2.4 — Testing, documentation, and completion verification

Future task.

Responsible for broader Stage 2.2 integration verification, documentation reconciliation, and completion assessment.

The current task still requires focused importer tests and a verified test report.

Do not claim the entire Stage 2.2 milestone is complete.

### Other excluded work

Do not plan or implement:

- Interactive measurement tables.
- Light-curve visualization.
- BLS or other scientific analysis.
- Transit parameter estimation.
- Analysis operation records.
- External archive downloads.
- General-purpose support for unrelated astronomical data formats.

---

## 14. Documentation impact assessment

Review the documentation requirements in `AGENTS.md`.

Identify which existing documents may need updating when the importer is implemented, particularly documentation concerning:

- Module responsibilities.
- Scientific data flow.
- FITS import interfaces.
- Metadata extraction.
- Validation rules.
- Error and warning behavior.
- Testing.
- Development progress.

Do not modify documentation during PLAN mode.

Distinguish documentation that must be updated because implementation changes established behavior from documentation that can remain unchanged.

Do not modify Foundation documents.

Do not assume all documentation work can be postponed if `AGENTS.md` requires relevant implementation documentation to be maintained during Build mode. Identify the appropriate updates and their scope in the plan.

---

## 15. Required planning deliverable

Produce a detailed report with these sections.

### 1. Repository state and preparation

- Current branch and Git status.
- Relevant files inspected.
- Confirmation that the 2.2.1 implementation exists.
- Current test baseline.
- Relevant Foundation requirements and citations.
- Existing user changes or repository-state concerns.

### 2. Subtask 2.2.1 implementation review

- Actual model components and interfaces.
- Actual validation structures.
- Actual array types and ownership behavior.
- Serialization behavior.
- Compatibility with the selected FITS dataset.
- Any genuine gaps or incompatibilities.

### 3. FITS inspection findings

- Actual HDU structure.
- Relevant headers.
- Table dimensions.
- Column names, types, shapes, and units.
- Time conventions.
- Missing and non-finite values.
- Quality flags.
- Differences from previously established findings.

### 4. Proposed importer architecture

- Proposed module path.
- Module responsibilities.
- Dependencies.
- FITS opening and HDU identification.
- Extraction interfaces.
- Dataset construction.
- Resource management.

### 5. Measurement and metadata mapping

Provide a clear mapping from FITS columns and headers to the existing model.

Identify required, optional, unsupported, and unknown information.

### 6. Validation matrix

Provide a table containing:

- Condition.
- Scientific or structural significance.
- Proposed classification.
- Expected importer behavior.
- Whether user approval is required.

### 7. Import result and error handling

Recommend the actual interface for successful imports, warning-bearing imports, and failed imports.

### 8. Testing plan

Identify focused unit tests, temporary FITS fixtures, optional real-data verification, resource-management tests, and data-integrity tests.

### 9. Architecture and documentation impact

Identify affected modules, existing interfaces, documentation, and dependencies.

### 10. Decisions requiring approval

Separate:

- Existing approved decisions.
- Recommendations within existing authority.
- New scientific decisions requiring approval.
- New architectural decisions requiring approval.

Do not treat recommendations as approved.

### 11. Implementation sequence

Recommend a practical, incremental Build sequence for Subtask 2.2.2.

Identify dependencies and work that belongs to 2.2.3 or 2.2.4.

### 12. Risks and unresolved issues

Identify anything that could prevent reliable implementation or compromise scientific data integrity.

---

## 16. Scope restrictions

This is strictly a PLAN task.

### Permitted

- Read repository files.
- Inspect Foundation and project documentation.
- Inspect the actual FITS dataset.
- Run read-only inspection commands.
- Inspect source code and tests.
- Run existing tests to establish a baseline.
- Produce a detailed implementation proposal.

### Not permitted

- Create, modify, delete, rename, or overwrite files.
- Implement the importer.
- Implement validation logic.
- Create or modify tests.
- Modify documentation.
- Modify Foundation documents.
- Install or upgrade dependencies.
- Change project configuration.
- Modify the original FITS file.
- Implement project association or persistence.
- Introduce permanent storage architecture.
- Commit, push, reset, clean, or otherwise modify Git history.

If an investigation cannot be completed, report the limitation instead of guessing.

If a material architectural or scientific decision is required, identify it for user approval rather than making it silently.

---

## 17. Final instruction

Present the complete planning report.

Clearly distinguish verified findings, previously established findings, assumptions, recommendations, approved decisions, and unresolved decisions.

The proposed design must follow:

1. The actual current repository.
2. The completed Subtask 2.2.1 implementation.
3. The relevant Foundation requirements.
4. Existing approved architectural and scientific decisions.

Do not begin implementation.

Do not begin Subtask 2.2.3.

Do not modify any files.

Stop after presenting the plan and wait for review and explicit authorization before Build mode.

### What I changed and why

| Change                                           | Reason                                                                                       |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------- |
| Added explicit 2.2.1 implementation verification | Prevents planning against a model that may differ from the actual code                       |
| Added exact prior FITS findings                  | Avoids losing important distinctions between SAP and PDCSAP                                  |
| Added importer-to-model mapping requirements     | Forces Nemotron to demonstrate exactly how the existing model will be populated              |
| Clarified required vs optional FITS columns      | Prevents arbitrary import-failure behavior                                                   |
| Expanded uncertainty and time validation         | These can affect scientific usability without necessarily making a file unreadable           |
| Added import-result interface design             | The existing data model does not itself define a complete importer success/failure interface |
| Added array ownership and FITS resource handling | Prevents memory-mapping and mutation problems                                                |
| Clarified documentation responsibilities         | Keeps the plan aligned with `AGENTS.md`                                                      |
| Strengthened approval gates                      | Keeps scientific and architectural decisions under your control                              |

My recommendation: Send this revised version rather than the original. It preserves the original investigation depth but gives Nemotron a more accurate starting point and makes the resulting plan easier to review before authorizing implementation.


# opencode plan v1