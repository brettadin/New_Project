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


I now have all verified facts needed. The baseline is confirmed (224 passed). I'll present the complete planning report in the conversation (no files will be created or modified, per PLAN mode).

---

# Subtask 2.2.2 — FITS Import and Validation: Implementation Plan

**Status:** PLAN ONLY. No implementation, file modification, or testing beyond baseline verification has been performed. This report is a proposal awaiting review and explicit authorization before Build mode.

---

## 1. Repository State and Preparation

### 1.1 Verified repository facts

| Item | Verified value |
|---|---|
| Working directory | `C:\Code\New_Project` (git repo, branch `master`, up to date with `origin/master`) |
| Last commit | `f65f14f` "Task 2.2.1" |
| Working-tree changes (pre-existing user changes) | **Modified:** `docs/planning/.../subtask-2.2-light-curve-import OVERVIEW.md`; **Untracked:** `docs/planning/.../task 2.2.2 FITS import and validation WORKING PROGRESS LOG.md`. Neither was created or touched by this task; both are left undisturbed. |
| Python / pytest | Python 3.13.9 (`.venv`), pytest 9.2.0 (from DEVELOPMENT LOG) |
| Astropy | 7.2.0, `astropy.io.fits` importable (verified) |

### 1.2 Files inspected
- `AGENTS.md` (project instructions, governing)
- `src/light_curve.py` (493 lines — the Subtask 2.2.1 data model) — full contents inspected
- `tests/test_light_curve.py` (759 lines — the Subtask 2.2.1 tests) — full contents inspected
- `docs/README.md`, `docs/MASTER_DEVELOPMENT_ROADMAP.md`, `docs/development/DEVELOPMENT_LOG.md`, `docs/development/UNRESOLVED_QUESTIONS.md`
- `docs/development/decisions/DEC-006-d5-technology-stack.md` (approved D5 stack)
- Foundation sections: `3.4`, `4.4`, `4.5`, `4.7`, `5.1`, `5.6`, `9.2`, `9.4`, plus `0_index.md`
- `docs/science/REVIEW-002-kepler10b-dataset.md` (previously established dataset profile)
- Planning prompts/overviews under `docs/planning/.../stage 2_2_n planning/` (read-only context)

### 1.3 Confirmation that Subtask 2.2.1 exists
**Verified.** `src/light_curve.py` and `tests/test_light_curve.py` both exist. The model components (`DatasetSource`, `TimeInfo`, `MeasurementColumn`, `MeasurementSeries`, `ValidationFinding`, `ValidationReport`, `LightCurveDataset`, `LightCurveValidationError`) are implemented exactly as inspected (Section 2).

### 1.4 Current test baseline (verified by running the suite)
`python -m pytest -q` → **224 passed in 16.48s, 0 failed.** This matches the reported 224-test result and exceeds the earlier 176-test baseline. No existing files were modified to achieve this. This is the baseline against which 2.2.2 tests will be added later.

### 1.5 Relevant Foundation requirements (with citations)
- **§3.4.1** — preserve measurement units, distinguish measurement types, identify missing/invalid measurements, preserve uncertainties.
- **§3.4.3** — preserve original timestamps and time metadata; do not assume ordinary Julian Date; identify missing/ambiguous time information.
- **§3.4.4** — preserve original measurements; create identifiable derived outputs only (none in this task).
- **§4.4** — FITS is a supported format (4.4.2); preserve original files and internal structures (4.4.1 G1); recognize units/time conventions (4.4.7, 4.4.8); metadata is part of the dataset (4.4.6).
- **§4.5** — user-provided file import (4.5.2); import inspection and metadata classification (4.5.3: verified/user-supplied/inferred/unknown); guided validation and error/warning distinction (4.5.5); never fabricate missing information (4.5.2, 4.5.10); preserve original files unchanged (4.5.2, 4.5.10).
- **§4.7** — preserve original source, filename, mission/instrument/target identifiers; distinguish original metadata from inferred/user-supplied; do not invent source information (4.7.1–4.7.4, 4.7.10).
- **§5.1** — preserve original data, units, metadata, uncertainty; distinguish missing from measured zero (5.1.4); distinguish computational success from scientific validity (5.1.8).
- **§5.6** — initial quality assessment on import (5.6.1); distinguish errors/warnings/info (5.6.1, 5.6.7); never automatically reject useful datasets (5.6.1); metadata classifications remain distinguishable (5.6.2); acceptance criteria include incomplete/noisy/ambiguous datasets (5.6 Acceptance Criteria).
- **§9.2** — modularity, separation of scientific functionality from UI, independent testability, avoid unnecessary dependencies (9.2.1–9.2.7).
- **§9.4** — preserve original imported files; separate original from derived; data integrity (9.4.2, 9.4.6).
- **§10** — AI decision boundaries and user approval (10.4, 10.9).

### 1.6 Existing user changes / repository-state concerns
None introduced by this task. The two planning-files changes (one modified, one untracked) predate this task and are outside `src/` and `tests/`; they will not be touched. No commits/pushes will be made.

---

## 2. Subtask 2.2.1 Implementation Review (actual interfaces)

All of the following is **verified by reading `src/light_curve.py` and `tests/test_light_curve.py`** (not assumed from the report).

### 2.1 Model components

| Component | Key fields / behavior (verified) |
|---|---|
| `DatasetSource` | `original_filename`, `original_file_path`, `archive`, `source_id`, `mission`, `instrument`, `target_object`, `checksum` — all `str \| None`, default `None`. |
| `TimeInfo` | `values: np.ndarray` (required); `unit`, `reference`, `time_scale`, `time_reference_frame` (str, default `""`); `reference_value`, `start`, `stop`, `resolution`, `format_hint` (float/str, default `None`). Unknown metadata → empty string / `None`; does not block construction. |
| `MeasurementColumn` | `name: str`, `values: np.ndarray`, `unit: str = ""`, `uncertainties: np.ndarray \| None = None`, `description: str \| None = None`. Property `n_nonfinite`. Non-finite preserved; empty unit = unknown; `None` uncertainties ≠ zero-array uncertainties. |
| `MeasurementSeries` | `series: dict[str, MeasurementColumn]`; keys must equal `column.name`; no duplicates. |
| `ValidationFinding` | `code`, `message`, `severity`, `column: str \| None`, `row_indices: list[int] \| None`. |
| `ValidationReport` | `errors`, `warnings`, `info` lists of `ValidationFinding`. |
| `LightCurveDataset` | `dataset_id` (UUID, auto), `name`, `source`, `time`, `measurements`, `quality_flags: np.ndarray \| None`, `cadence_numbers: np.ndarray \| None`, `validation`, `imported_at` (auto ISO UTC), `notes`. Property `n_observations`. |

### 2.2 Structural validation behavior (`LightCurveDataset.__post_init__`)
1. Validates `dataset_id` is a UUID string.
2. `time.values` required, must be `np.ndarray`; `time.unit` must be str.
3. `measurements` must be `MeasurementSeries` with a dict; keys match `column.name`; no duplicate names.
4. Each column's `values` must be `np.ndarray`; `unit` str; `uncertainties` `np.ndarray` or `None`.
5. **Array alignment:** every measurement `values` length, every non-`None` `uncertainties` length, `quality_flags` length, `cadence_numbers` length must equal `len(time.values)`. Mismatch → `LightCurveValidationError`.
6. `validation` must be a `ValidationReport`; `imported_at` must be str.
Raises `LightCurveValidationError` (subclass of `ValueError`) on any structural problem.

### 2.3 Array copying and ownership (`_copy_arrays`)
- `time.values` → `np.array(..., dtype=np.float64, copy=True)`.
- Each measurement `values` → `np.array(..., dtype=np.float64, copy=True)`; `uncertainties` → `np.array(..., dtype=np.float64, copy=True)` if not None.
- `quality_flags` → `np.array(..., dtype=np.int64, copy=True)` if not None; `cadence_numbers` → `np.array(..., dtype=np.int64, copy=True)` if not None.
**Implication:** the model always owns independent copies. The importer must still copy FITS memory-mapped arrays *before* closing the file (Section 4.5); the model's copy is a second, authoritative safety copy. Minor redundancy is acceptable for correctness.

### 2.4 Serialization (`to_dict` / `from_dict`)
- `to_dict()` → JSON-compatible dict; arrays → `.tolist()`; `None` preserved as `None` (distinguishable from zero arrays).
- `from_dict(data)` reconstructs and re-validates via `__post_init__`; distinguishes `None` from arrays; round-trips `dataset_id`, `imported_at`, source metadata, validation report, quality flags, cadence numbers.
- Verified by tests (48 focused model tests + full suite 224).

### 2.5 Compatibility with the Kepler FITS dataset
**Compatible — no model change required.** Mapping:
- `TIME` → `TimeInfo.values` (float64), unit `"d"`, reference `"BJD - 2454833 (BKJD)"`, `time_scale` `"TDB"`, `time_reference_frame` `"SOLARSYSTEM"`, `reference_value` `2454833.0`, `start`/`stop` from `TSTART`/`TSTOP`.
- `SAP_FLUX` / `PDCSAP_FLUX` → two independent `MeasurementColumn`s (`values` float64, unit `"e-/s"`, `uncertainties` from `*_FLUX_ERR`, `description` holding original FITS column meaning).
- `SAP_FLUX_ERR` / `PDCSAP_FLUX_ERR` → associated uncertainties (float64).
- `SAP_QUALITY` → `quality_flags` (int64).
- `CADENCENO` → `cadence_numbers` (int64).
- `DatasetSource`: `mission="Kepler"`, `instrument="Kepler Photometer"`, `target_object="KIC 11904151"`, `source_id`/`archive` from headers/origin, `original_filename`, `original_file_path`.
- Non-finite flux/uncertainty values preserved (model does not remove/replace).
- 37 nonzero quality flags preserved (no filtering).

### 2.6 Genuine gaps / incompatibilities (recommendations only, not implemented)
1. **TIME column unit is compound:** `TUNIT1 = "BJD - 2454833"` is a reference-plus-unit, not a plain unit. The model has separate `unit` and `reference` fields, so this fits: `unit="d"`, `reference="BJD - 2454833"`. **No model change needed.** Recommendation: set `time.unit="d"`, `time.reference="BJD - 2454833 (BKJD)"`, `time.time_scale="TDB"`, `time.time_reference_frame="SOLARSYSTEM"`, `time.reference_value=2454833.0`.
2. **Big-endian FITS dtypes** (`>f8`, `>f4`, `>i4`): `np.array(..., dtype=np.float64/int64, copy=True)` handles byte-order conversion on read. **No model change needed**; importer must ensure conversion before/at model construction.
3. **Float32 flux → float64 storage:** upcast preserves values exactly; no precision loss. Acceptable.
4. **No field for raw FITS TTYPE/TFORM/null or per-column full header:** not needed for initial scope; `MeasurementColumn.description` can hold the column's descriptive meaning if desired. **Defer.**
5. **Entirely non-finite `PSF_CENTR1`:** not in the supported measurement set, so not imported. **No impact.**

No model redesign is required or recommended for 2.2.2. Any model change (e.g., adding fields) would be a 2.2.1-scope decision requiring approval and is explicitly out of scope here.

---

## 3. FITS Inspection Findings (verified against the actual file)

### 3.1 HDU structure (verified)
File: `C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits` (read-only, outside repo, unchanged).

| HDU | Type | EXTNAME | Rows / Shape | Notes |
|---|---|---|---|---|
| 0 | `PrimaryHDU` | `PRIMARY` | — | 58 header cards |
| 1 | `BinTableHDU` | `LIGHTCURVE` | 476 rows × 20 cols | **The light-curve table** |
| 2 | `ImageHDU` | `APERTURE` | 12 × 10 | Aperture mask image |

**Confirmed:** the light-curve table is at HDU index 1, but the importer must **not** hardcode index 1; it must identify the table structurally (Section 4.4). `NEXTEND=2` in the primary matches the two extensions.

### 3.2 LIGHTCURVE table columns (verified)
| # | FITS column | Format | dtype (as stored) | Unit (TUNIT) | Supported in 2.2.2? |
|---|---|---|---|---|---|
| 1 | `TIME` | D | `>f8` (float64) | `BJD - 2454833` | **Required** (time) |
| 2 | `TIMECORR` | E | `>f4` | `d` | No (unsupported) |
| 3 | `CADENCENO` | J | `>i4` (int32) | — | **Optional** (cadence) |
| 4 | `SAP_FLUX` | E | `>f4` | `e-/s` | **Required** (flux, at least one of SAP/PDCSAP) |
| 5 | `SAP_FLUX_ERR` | E | `>f4` | `e-/s` | **Optional** (uncertainty for SAP_FLUX) |
| 6 | `SAP_BKG` | E | `>f4` | `e-/s` | No |
| 7 | `SAP_BKG_ERR` | E | `>f4` | `e-/s` | No |
| 8 | `PDCSAP_FLUX` | E | `>f4` | `e-/s` | **Required** (flux, at least one of SAP/PDCSAP) |
| 9 | `PDCSAP_FLUX_ERR` | E | `>f4` | `e-/s` | **Optional** (uncertainty for PDCSAP_FLUX) |
| 10 | `SAP_QUALITY` | J | `>i4` | — | **Optional** (quality flags) |
| 11–20 | `PSF_CENTR1/2`, `MOM_CENTR1/2`, `POS_CORR1/2` (+ errors) | D/E | mixed | pixel/pixels | No (unsupported) |

### 3.3 Data values (verified)
| Column | Non-finite count | Min | Max | Notes |
|---|---|---|---|---|
| `TIME` | 0 | 120.53914651 | 130.24539528 | All finite; range matches ~120.54–130.25 |
| `CADENCENO` | N/A (int) | 568 | 1043 | Consecutive (diff == 1 for all) |
| `SAP_FLUX` | 4 | 532355.0 | 532944.06 | Preserved as-is |
| `SAP_FLUX_ERR` | 4 | ~20.04 | ~20.05 | Same 4 rows as SAP_FLUX |
| `PDCSAP_FLUX` | 7 | 501346.12 | 501746.75 | Preserved as-is |
| `PDCSAP_FLUX_ERR` | 7 | ~20.57 | ~20.77 | Same 7 rows as PDCSAP_FLUX |
| `SAP_QUALITY` | N/A (int) | — | — | 37 nonzero; 439 zero; unique nonzero values `{64, 128, 8192, 8320, 12352, 32800}` |
| `PSF_CENTR1` | 476 (all NaN) | — | — | Entirely non-finite; unsupported column |
| `MOM_CENTR1` | 4 | — | — | Unsupported column |
| `POS_CORR1` | 7 | — | — | Unsupported column |

### 3.4 Header metadata (verified)
**Primary HDU:** `TELESCOP=Kepler`, `INSTRUME=Kepler Photometer`, `OBJECT=KIC 11904151`, `KEPLERID=11904151`, `ORIGIN=NASA/Ames`, `MISSION=Kepler`, `QUARTER=0`, `OBSMODE=long cadence`, `DATE=2015-08-26`, `CREATOR=793551 FluxExporter2PipelineModule`, `FILEVER=6.1`, plus target coordinates/magnitudes.

**LIGHTCURVE extension:** `INHERIT=True` (inherits primary header), plus `TIMEREF=SOLARSYSTEM`, `TASSIGN=SPACECRAFT`, `TIMESYS=TDB`, `BJDREFI=2454833`, `BJDREFF=0.0`, `TIMEUNIT=d`, `TSTART=120.52892942`, `TSTOP=130.25561236`, `TELAPSE=9.72668293`, `TIMEDEL=0.02043359821692`, `EXPOSURE=8.95472397`, `DATE-OBS`, `DATE-END`, PDC keywords.

### 3.5 Time convention (verified)
- Values are `BJD − 2454833` (BKJD), in days (`TIMEUNIT=d`), time system `TDB`, reference frame `SOLARSYSTEM`, `BJDREFI=2454833`, `BJDREFF=0`.
- **Not ordinary Julian Date.** Must not be silently converted or relabeled as JD.

### 3.6 Comparison with previously established findings (REVIEW-002)
| Property | Previously established | Currently verified | Difference |
|---|---|---|---|
| HDUs | Primary, LIGHTCURVE, APERTURE | Same (3 HDUs) | None |
| LIGHTCURVE rows/cols | 476 × 20 | 476 × 20 | None |
| TIME range | ~120.539–130.245 | 120.53914651–130.24539528 | None (more precise) |
| CADENCENO | 568–1043, consecutive | 568–1043, consecutive | None |
| SAP_FLUX non-finite | 4 | 4 | None |
| SAP_FLUX_ERR non-finite | 4 (same rows) | 4 | None |
| PDCSAP_FLUX non-finite | 7 | 7 | None |
| PDCSAP_FLUX_ERR non-finite | 7 (same rows) | 7 | None |
| SAP_QUALITY nonzero | 37 | 37 (values `{64,128,8192,8320,12352,32800}`) | Values now known |
| PSF_CENTR1/2 | entirely non-finite | PSF_CENTR1 all NaN (476) | Consistent |
| MOM_CENTR1/2 | 4 non-finite each | MOM_CENTR1: 4 | Consistent |
| POS_CORR1/2 | 7 non-finite each | POS_CORR1: 7 | Consistent |
| Headers | TELESCOP/INSTRUME/OBJECT/KEPLERID/MISSION/ORIGIN/TIMESYS/TIMEREF/BJDREFI/BJDREFF/TIMEUNIT | All verified, plus TSTART/TSTOP/TIMEDEL/EXPOSURE | Consistent |

**All previously established findings are confirmed.** No previously established finding is contradicted. The file is accessible, so no limitation is reported.

---

## 4. Proposed Importer Architecture

### 4.1 Module path
`src/fits_importer.py` (new module, lives alongside `src/light_curve.py`). Keep it a single module initially; split only if it grows beyond a coherent responsibility.

### 4.2 Dependencies
- `astropy.io.fits` (approved, already a dependency — DEC-006 explicitly lists `astropy.fits` for FITS handling).
- `numpy` (approved).
- `src.light_curve` (the approved 2.2.1 model — reused, not redesigned).
- No new dependencies. No PySide6, no project/service/repository imports. UI-independent.

### 4.3 Module responsibilities
1. Open a FITS file safely (read-only, guaranteed close).
2. Identify the light-curve table among HDUs (structural, not fixed index).
3. Extract supported columns (`TIME`, `SAP_FLUX`, `PDCSAP_FLUX`, `SAP_FLUX_ERR`, `PDCSAP_FLUX_ERR`, `SAP_QUALITY`, `CADENCENO`) and associated header/table metadata.
4. Validate per the matrix in Section 6; build a `ValidationReport`.
5. Construct a `LightCurveDataset` (via the model's constructor, which performs structural validation and array copying).
6. Return an import result (Section 7) or raise a meaningful importer exception for file-level failures.

### 4.4 FITS opening and HDU identification
- Open with `fits.open(path, mode="readonly")` inside a `with` block so the file is closed reliably on success and on failure.
- **Critical resource detail:** `fits.open` memory-maps table data by default. All arrays must be copied into ordinary contiguous NumPy arrays **inside** the `with` block, before the file closes. Accessing memory-mapped data after close raises errors.
- HDU identification strategy (recommended):
  1. Iterate all HDUs.
  2. Candidate = any table HDU (`BinTableHDU`/`TableHDU`) whose column names include `TIME` and at least one of `SAP_FLUX` / `PDCSAP_FLUX`.
  3. Prefer a candidate whose `EXTNAME == "LIGHTCURVE"` (Kepler convention) if present; otherwise use the first structural match.
  4. If multiple structural matches exist, prefer the one containing both `SAP_FLUX` and `PDCSAP_FLUX`; else first match; log an info finding about ambiguity.
  5. If no candidate → import failure (missing/unusable light-curve table).
  6. Primary-header metadata and extension-header metadata are both read; `INHERIT=True` means extension inherits primary, so merge with extension taking precedence for time-specific keywords.
- This is Kepler-product-aware (column names, `LIGHTCURVE` extname, BKJD/TDB keywords) but expressed through a general "table with TIME + flux column" rule — not a universal FITS framework.

### 4.5 Extraction interfaces (internal, proposed)
- `_extract_arrays(hdu, column_names)` → dict of `np.ndarray` copies (float64 for float columns, int64 for int columns), copied before file close. Non-finite preserved.
- `_build_time_info(header, time_array)` → `TimeInfo`.
- `_build_measurement_columns(...)` → dict of `MeasurementColumn` (SAP_FLUX±err, PDCSAP_FLUX±err), each with `description` = original column meaning.
- `_build_dataset(...)` → `LightCurveDataset` (model constructor performs structural validation + copies).
- Array handling: convert big-endian FITS dtypes to native float64/int64 via `np.array(..., dtype=..., copy=True)`. Upcast float32 → float64 (value-preserving). Do not fill/replace NaN/inf.

### 4.6 Resource management
- Single `with fits.open(...)` scope; all reads + copies inside it; dataset constructed after close is safe because arrays are already copied.
- On any exception during read/extract/validate, the `with` block closes the file; no file handle leaks.
- Original file never opened for write; read-only mode.

---

## 5. Measurement and Metadata Mapping

### 5.1 Required vs optional vs unsupported

| FITS item | Role | Required for construction? | Model target | Notes |
|---|---|---|---|---|
| `TIME` | timestamps | **Yes** (without → failure) | `TimeInfo.values` (+ metadata) | float64; unit `d`; reference `BJD - 2454833`; scale `TDB` |
| `SAP_FLUX` | SAP flux | At least one of SAP/PDCSAP required | `MeasurementColumn("SAP_FLUX")` | float32→float64; unit `e-/s` |
| `PDCSAP_FLUX` | PDC flux | At least one of SAP/PDCSAP required | `MeasurementColumn("PDCSAP_FLUX")` | independent of SAP; never merged |
| `SAP_FLUX_ERR` | SAP uncertainty | Optional | `SAP_FLUX.uncertainties` | absent → `None` (warning) |
| `PDCSAP_FLUX_ERR` | PDC uncertainty | Optional | `PDCSAP_FLUX.uncertainties` | absent → `None` (warning) |
| `SAP_QUALITY` | quality flags | Optional | `quality_flags` (int64) | absent → `None` |
| `CADENCENO` | cadence ids | Optional | `cadence_numbers` (int64) | absent → `None` |
| Other columns (`TIMECORR`, `SAP_BKG*`, `PSF_CENTR*`, `MOM_CENTR*`, `POS_CORR*`) | — | No | Not imported | may be noted in `notes`/info |
| Primary header (TELESCOP, INSTRUME, OBJECT, KEPLERID, ORIGIN, MISSION, QUARTER, OBSMODE, DATE, CREATOR) | source metadata | No | `DatasetSource` (+ `notes`) | mission/instrument/target_object/archive/source_id |
| Extension header (TIMEREF, TIMESYS, BJDREFI, BJDREFF, TIMEUNIT, TSTART/TSTOP, TIMEDEL, EXPOSURE) | time metadata | No | `TimeInfo` (+ `notes`) | BKJD/TDB/SOLARSYSTEM |
| `TUNIT1` / `TUNIT4` / `TUNIT8` | column units | No | `MeasurementColumn.unit` / `TimeInfo.unit` | empty string if unknown |

### 5.2 Metadata not representable by the current model
- Raw FITS `TTYPE`/`TFORM`/`TDISP`/`NULL` per column, full header card list, aperture-mask image (HDU2), PDC configuration keywords (`PDCMETHD`, `CDPP*`, etc.), exposure/deadtime values.
- **Assessment:** None are important enough to require a model change for 2.2.2. They can be stored in `LightCurveDataset.notes` (a free-form string) or omitted as unknown. `DatasetSource` lacks fields for archive/product ID beyond `source_id`/`archive`; Kepler `KEPLERID` → `source_id` is reasonable. No model change proposed in this task; any addition belongs to a future, approved model revision.

---

## 6. Validation Matrix

Classifications: **Error** = prevents dataset construction (reported as importer failure, not in a dataset `ValidationReport`); **Warning** = import succeeds, finding in `validation.warnings`; **Info** = import succeeds, finding in `validation.info`; **Preserve** = kept as-is, no modification.

| # | Condition | Significance | Classification | Expected importer behavior | User approval required? |
|---|---|---|---|---|---|
| F1 | File missing / unreadable / not a file | File-level import failure | **Error** (exception) | Raise `FITSImportError` with reason; no dataset | No |
| F2 | Corrupted / invalid FITS structure | Cannot parse | **Error** (exception) | Raise `FITSImportError` with reason | No |
| F3 | No table HDU matching TIME + flux column | No usable light curve | **Error** (exception) | Raise `FITSImportError` | No |
| F4 | Multiple equally-valid light-curve tables | Ambiguity | **Info** (or warning) | Import first/best match; info finding | No |
| C1 | `TIME` column absent | Required column missing | **Error** (exception) | No dataset can be built without time | No |
| C2 | Neither `SAP_FLUX` nor `PDCSAP_FLUX` present | No measurement | **Error** (exception) | No dataset | No |
| C3 | One flux column present, the other absent | Partial measurement set | **Preserve** (success) | Import the available one; info finding | No |
| C4 | Flux column present, matching `*_FLUX_ERR` absent | Missing uncertainty | **Warning** | `uncertainties=None`; warning finding | No |
| C5 | `*_FLUX_ERR` present but its flux column absent | Orphaned uncertainty | **Warning** / ignore | Do not import orphan; info/warning | No |
| C6 | `SAP_QUALITY` or `CADENCENO` absent | Optional metadata | **Preserve** (success) | `quality_flags`/`cadence_numbers=None`; optional, no finding or info | No |
| C7 | Extra unsupported numeric columns present | Not in initial set | **Preserve** | Not imported; possibly info | No |
| C8 | Column dtype unexpected (e.g., string where numeric expected) | Incompatible type | **Error** (exception) or **Warning** | If coercible to float64/int64, coerce + warning; else error | No |
| C9 | Measurement array length ≠ time array length | Structural mismatch | **Error** | Model constructor raises `LightCurveValidationError`; report as import failure | No |
| M1 | Non-numeric timestamp | Bad time | **Error** | Cannot build float64 time array | No |
| M2 | Non-finite timestamp (NaN/inf) | Bad time | **Warning** (preserve) | Preserve NaN/inf in `TimeInfo.values`; warning with row indices | No |
| M3 | Non-finite flux (NaN/inf) | Missing measurement | **Warning** (preserve) | Preserve; warning with `n_nonfinite` / row indices (Kepler: SAP 4, PDCSAP 7) | No |
| M4 | Non-finite uncertainty | Bad uncertainty | **Warning** (preserve) | Preserve; warning with row indices | No |
| M5 | Negative uncertainty | Physically questionable | **Warning** (preserve) | Preserve; warning (do not invent/replace) | No |
| M6 | Duplicate timestamps | Structural concern | **Warning** | Preserve; warning with row indices | No |
| M7 | Non-monotonic timestamps | Structural concern | **Warning** | Preserve order; warning (do not reorder) | No |
| Q1 | Nonzero quality flags present | Quality info | **Info** | Preserve flags; info finding with count and row indices (Kepler: 37 of 476) | No |
| Q2 | User requests quality-bitmask filtering | — | N/A (out of scope) | Not performed in 2.2.2; deferred to analysis operation | **Yes** (future policy) |
| T1 | Missing time unit | Unknown unit | **Info** | `unit=""` per model convention; info | No |
| T2 | Missing time reference/scale/frame | Unknown metadata | **Info** | empty strings / `None`; info | No |
| T3 | Missing flux unit | Unknown unit | **Info** | `unit=""`; info | No |

**Scientific reasoning (per §5.1, §5.6):** non-finite and questionable measurements are preserved, not removed or replaced (§5.1.4, §5.6.1 acceptance criteria 3). Computational success (array built) ≠ scientific validity (§5.1.8); warnings communicate limitations without blocking legitimate use. Quality flags are never auto-filtered (§3.4.10: "avoid automatically removing measurements"; REVIEW-002 justification).

**Classification authority:** file-level failures (F1–F3, C1, C2) are importer exceptions, **not** `ValidationReport` errors, because no dataset exists to attach a report to (per the 2.2.1 separation in §8.G of the task). All warnings/infos are attached to the constructed dataset's `validation`.

---

## 7. Import Result and Error Handling (recommended interface)

The 2.2.1 model defines `LightCurveDataset` and `ValidationReport` but no importer result type. A minimal interface is needed.

### 7.1 Evaluated options
| Option | Description | Trade-offs |
|---|---|---|
| Pure exceptions (raise on any non-perfect import) | Caller uses try/except; warnings hard to distinguish from success | Conflates "imported with warnings" with "failed"; forces exception handling for expected, non-fatal conditions |
| Dedicated result dataclass only | Return `ImportResult{success, dataset, error, validation, ...}` always; no exceptions | Clean for all outcomes, but genuinely exceptional infrastructure failures (file not found) still merit exceptions |
| **Hybrid (recommended)** | Result dataclass for normal outcomes; dedicated `FITSImportError` exception for file-level/infrastructure failures | Clear separation: expected validation outcomes return a result; truly unrecoverable conditions raise with a meaningful reason |

### 7.2 Recommended interface (not implemented; for approval)

```python
@dataclass
class FitsImportResult:
    success: bool            # True if a dataset was constructed
    dataset: LightCurveDataset | None
    source: DatasetSource
    validation: ValidationReport   # warnings/info attached when success
    error: str | None          # meaningful reason when not success

class FITSImportError(Exception):
    """Raised when a file-level condition prevents import (unreadable, corrupted, no usable table, missing required column)."""
```

- **Success without warnings:** `success=True`, `dataset` populated, `validation` empty, `error=None`.
- **Success with warnings:** `success=True`, `dataset` populated, `validation.warnings/info` populated, `error=None`.
- **Failed import:** `success=False`, `dataset=None`, `error` set (and/or `FITSImportError` raised for infrastructure failures).

The caller decides whether to accept a warning-bearing import (consistent with §4.5.5/§4.5.6 guided vs streamlined import; user authority per §5.6.10). No UI dialogs, no project/repository integration, no file-selection dialog in this task.

### 7.3 Why not put importer failures in a dataset `ValidationReport`
Per §8.G of the task and §5.6.7: a `ValidationReport` belongs to a constructed dataset. If import fails before construction, there is no dataset to attach findings to. File-level failures are therefore reported to the caller via the result/exception, not via `validation.errors`.

---

## 8. Testing Plan (tests to be created in Build mode / 2.2.4 — not created now)

### 8.1 Temporary FITS fixtures (generated in `tmp_path`, no dependence on the real dataset path)
- Valid light-curve table (multiple HDUs, table at HDU 1).
- Light-curve table not at HDU index 1 (e.g., HDU 2).
- Multiple candidate tables (ambiguity).
- Missing `TIME` column (failure).
- Missing both flux columns (failure).
- Only `SAP_FLUX` (no PDCSAP); only `PDCSAP_FLUX` (no SAP).
- Missing uncertainty column(s).
- Unexpected column type (string where numeric expected).
- Inconsistent array lengths (constructible by hand-built table).
- NaN/inf in flux; NaN in time; non-finite/negative uncertainties.
- Nonzero quality flags.
- Missing/ambiguous metadata (no time unit, no mission).
- Corrupted / truncated FITS file; unreadable file.
- Unsupported structure (image-only file, no table).

All fixtures written to `tmp_path`; the standard suite must pass on any machine without the real Kepler file.

### 8.2 Optional real-data verification (local, not in the automated suite)
Run against `C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits` and assert:
- HDU identified as index 1 (LIGHTCURVE).
- 476 rows; TIME range 120.5391–130.2454; unit `d`, scale `TDB`, reference `BJD - 2454833`.
- SAP_FLUX and PDCSAP_FLUX both present and distinct; 4 and 7 non-finite respectively.
- Uncertainties paired correctly; same non-finite rows.
- `SAP_QUALITY` 37 nonzero preserved; `CADENCENO` 568–1043 consecutive.
- `DatasetSource.original_file_path`/`original_filename` set; mission/instrument/target_object correct.
- Valid `LightCurveDataset` constructed; `to_dict()`/`from_dict()` round-trip.
- Original file checksum unchanged before/after.

This test must be gated on file presence (skip if absent) so the suite is portable.

### 8.3 Data-integrity tests
- Original FITS file bytes/checksum unchanged after import (read-only open; no write handle).
- No observations silently dropped (n_observations == 476).
- Distinct flux columns remain distinct (SAP ≠ PDCSAP values).
- Missing values remain identifiable (NaN preserved, count matches).
- Quality flags available and unchanged.
- FITS file closed after import (no open handles; accessing memmap after close would fail — assert clean close).

### 8.4 Test baseline
Current: 224 passed. 2.2.2 tests will be added on top; the existing 224 must continue to pass.

---

## 9. Architecture and Documentation Impact

### 9.1 Affected modules / interfaces
- **New:** `src/fits_importer.py` (importer, result type, exception). Depends only on `src.light_curve`, `astropy.io.fits`, `numpy`.
- **Unchanged:** `src/light_curve.py` (model reused as-is), all project lifecycle modules (`project_model.py`, `project_service.py`, `project_repository.py`, `main_window.py`, `main.py`, `config_provider.py`, dialogs).
- **No UI coupling:** importer has no PySide6 dependency. Integration with the project/service/UI belongs to 2.2.3 and later.
- **No new dependencies** (astropy already approved via DEC-006).

### 9.2 Documentation impact (to be updated in Build mode per AGENTS.md; not modified now)
Documents likely needing updates:
- `docs/MASTER_DEVELOPMENT_ROADMAP.md` — mark Task 2.2 subtask 2.2.2 status; record test results.
- `docs/development/DEVELOPMENT_LOG.md` — record 2.2.2 implementation, files changed, test results.
- Architecture/module documentation (e.g., `docs/architecture/` if it exists — currently empty) — document importer responsibilities and interfaces.
- Testing documentation / test reports (`docs/development/test_reports/`).
- Possibly a module-responsibility or data-flow document.

Documents intentionally **not** changed by this plan: Foundation documents (read-only), `docs/README.md` (index unchanged unless a significant doc is added/renamed — not the case here), existing project lifecycle docs (unchanged behavior).

The plan identifies these updates as required during Build mode per AGENTS.md §"Documentation Maintenance During Implementation"; none are performed in Plan mode.

---

## 10. Decisions Requiring Approval

### 10.1 Existing approved decisions (no approval needed; respected by this plan)
| ID | Decision | Basis |
|---|---|---|
| D2 | Photometry/time-series as initial scientific capability | Approved (§3.4, §2.2) |
| D3 | Initial scope boundary (included/deferred/consideration/outside) | Approved |
| D4 | Single-user local, private-by-default, permission-aware | Approved (§8.11, §9.1.2, §9.8.2) |
| D5 | Tech stack: Python 3.13, PySide6, NumPy/SciPy/Astropy/Matplotlib/pytest/venv | Approved (DEC-006; delegation to OpenCode) |
| D6 | Data storage model deferred; provisional local-file only | Approved (deferred) |
| DEC-005 | BLS initial photometric workflow | Approved |

### 10.2 Recommendations within existing authority (proposed, not yet approved)
- Module `src/fits_importer.py`; UI-independent; uses astropy + numpy + `src.light_curve` only.
- HDU identification by structure (TIME + flux column), preferring `EXTNAME="LIGHTCURVE"`; not fixed index.
- Result interface: `FitsImportResult` dataclass + `FITSImportError` exception for infrastructure failures.
- Non-finite/questionable measurements preserved with warnings (not removed/replaced).
- No quality-bitmask filtering in 2.2.2.
- Unsupported columns (PSF_CENTR*, etc.) not imported.
- Arrays copied before FITS close; model's copy is the authoritative safety copy.

These are within the agent's implementation authority for 2.2.2 as long as they follow the approved model and Foundation. I present them as recommendations for review.

### 10.3 New scientific decisions requiring user approval (none identified as blockers)
None identified that block 2.2.2. If, during Build, an incompatibility with the model is found that requires a model change, that would be a 2.2.1-scope change requiring approval and would pause this task.

### 10.4 New architectural decisions requiring user approval (none identified)
None identified. The proposed structure follows §9.2 (modularity, scientific/UI separation, no unnecessary dependencies).

---

## 11. Implementation Sequence (recommended Build sequence)

1. Create `src/fits_importer.py`: `FITSImportError`, `FitsImportResult`, FITS opening/close, HDU identification.
2. Implement extraction of `TIME`, `SAP_FLUX`/`PDCSAP_FLUX`, uncertainties, `SAP_QUALITY`, `CADENCENO` (array copies inside the `with` block).
3. Implement metadata extraction into `DatasetSource` and `TimeInfo` (BKJD/TDB/SOLARSYSTEM).
4. Implement validation findings and `ValidationReport` construction; dataset assembly via `LightCurveDataset` constructor.
5. Implement unit tests with temporary FITS fixtures (Section 8.1); run targeted tests.
6. Optional real-data verification against the Kepler file (Section 8.2), gated on file presence.
7. Run full suite (must remain 224+ passing, no regressions).
8. Update documentation (roadmap, dev log, architecture, test reports) per AGENTS.md — Build-mode activity.
9. Review completion; hand off to 2.2.3.

**Deferred to 2.2.3:** project association, dataset persistence, save/reopen, project IDs/ownership/permissions on the scientific dataset. **Deferred to 2.2.4:** broader Stage 2.2 integration verification and documentation reconciliation. **Never in this task:** visualization, BLS, quality-bitmask filtering, archive downloads, universal FITS framework, database/permanent storage.

---

## 12. Risks and Unresolved Issues

| Risk / Issue | Description | Mitigation / Status |
|---|---|---|
| Memory-mapped FITS arrays | `fits.open` memmaps data; accessing after close fails if not copied. | Copy all arrays to contiguous NumPy arrays inside the `with` block (verified design requirement). |
| Big-endian FITS dtypes (`>f4`, `>f8`, `>i4`) | Must convert to native float64/int64. | `np.array(..., dtype=..., copy=True)` handles byte swap; verify on real file. |
| Float32 → float64 upcast | Value-preserving, but doubles memory for flux arrays. | Acceptable for ~476 rows; document. |
| Model always re-copies arrays | Slight redundancy with importer's pre-close copy. | Acceptable; correctness > micro-optimization at this scale. |
| `TUNIT1 = "BJD - 2454833"` compound unit | Must split into `unit="d"` + `reference`. | Straightforward mapping; no model change. |
| Real dataset not portable | Automated suite must not depend on `C:\Code\...` absolute path. | Gate real-data test on file presence; use `tmp_path` fixtures for the suite. |
| Validation vs exception boundary | Risk of putting import failures into a dataset `ValidationReport` that doesn't exist. | Enforce separation (Section 7.3); file-level → exception/result.error; scientific → `validation.warnings/info`. |
| Quality-bitmask policy pressure | Temptation to auto-filter nonzero flags. | Explicitly excluded; filtering is a future analysis operation requiring approval. |
| Scope creep | Pressure to add project persistence, UI, visualization, BLS. | Explicitly excluded; 2.2.2 is import+validation only. |

No unresolved issue currently blocks planning. The only items pending user input are the review/approval of this plan itself before Build mode begins.

---

## Summary of classification

- **Verified facts:** repository state (git status, branch, last commit), existence/contents of `src/light_curve.py` and `tests/test_light_curve.py`, 224-test baseline (run and confirmed), FITS HDU structure/columns/data/headers (inspected with Astropy 7.2.0), all Foundation citations quoted from actual documents.
- **Previously established findings (REVIEW-002):** confirmed in full by current inspection; no contradictions.
- **Assumptions:** none material; where metadata could not be mapped to the model, the plan states it as unknown/`notes` rather than assuming.
- **Recommendations:** module path, HDU strategy, result interface, preservation behavior, validation classifications, implementation sequence — all presented for review, not treated as approved.
- **Approved decisions:** D2–D6, DEC-005, DEC-006 — respected, not changed.
- **Decisions requiring approval:** this plan overall; any future model change (none currently needed).

This completes the PLAN-mode deliverable. I will not implement, create, modify, or delete any files. Please review the plan and, if approved, explicitly authorize the switch to Build mode so implementation of Subtask 2.2.2 can begin.


# Chatgpt plan v1 review/response


The plan is structurally sound and is close to being ready for Build mode. It correctly reuses the 2.2.1 model, keeps FITS import independent of the GUI and persistence layers, preserves non-finite measurements, and avoids automatic quality-flag filtering.

I would not approve it exactly as written, however. There are several inconsistencies and a few technical details worth correcting before implementation.

## 1. Issues that should be corrected

### 1. Import result and exception handling are contradictory

Section 7 proposes a hybrid interface:

- `FitsImportResult` represents success or failure.
- `FITSImportError` is raised for file-level failures.
- The report also says failed imports return `success=False`.

Those are two competing failure-reporting mechanisms. The proposed result also duplicates information already held by `LightCurveDataset`:

- `dataset.source` duplicates `FitsImportResult.source`.
- `dataset.validation` duplicates `FitsImportResult.validation`.
- `success` can be inferred from whether a dataset exists.

My recommendation: Keep the initial interface simpler.

- Successful import returns a `LightCurveDataset`.
- Failed import raises `FITSImportError` with a useful message.
- Import warnings and informational findings are stored in `dataset.validation`.
- No separate result dataclass is necessary at this stage.

This avoids creating an additional abstraction before there is a demonstrated need for one.

### 2. The testing schedule contradicts itself

Section 8 says:

> Tests to be created in Build mode / 2.2.4.

But Section 11 includes creating unit tests as part of the 2.2.2 implementation sequence.

The distinction should be:

- 2.2.2: Implement the importer and its focused automated tests. These tests establish that the importer behaves correctly.
- 2.2.4: Perform broader integration verification, review the accumulated test coverage, reconcile documentation, and verify the overall 2.2 completion criteria.

Do not postpone all importer testing until 2.2.4. That would leave the implementation without its own verification.

### 3. Source metadata should not be inferred incorrectly

The proposed mapping includes:

`ORIGIN=NASA/Ames` → `archive` or `source_id`

That needs clarification.

`ORIGIN` identifies the organization associated with the file's creation. It does not, by itself, establish which archive supplied the dataset.

I recommend:

| Model field          | Proposed mapping                        |
| -------------------- | --------------------------------------- |
| `mission`            | `Kepler`                                |
| `instrument`         | `Kepler Photometer`                     |
| `target_object`      | `KIC 11904151`                          |
| `source_id`          | `11904151` from `KEPLERID`              |
| `archive`            | `None` unless independently established |
| `original_filename`  | Actual input filename                   |
| `original_file_path` | Actual input path                       |

`ORIGIN=NASA/Ames` can be retained in notes or an informational finding if useful. Do not label it as an archive.

### 4. Dataset naming needs an explicit rule

The mapping covers source, time, and measurements, but does not explain how the required `LightCurveDataset.name` is populated.

I recommend using the input filename stem as the initial dataset name, for example:

`kplr011904151-2009131105131_llc_full`

This is deterministic and does not invent a scientific target name. The original filename should still be preserved separately in `DatasetSource`.

### 5. Some proposed FITS tests are not valid importer scenarios

The plan proposes a FITS fixture with inconsistent column lengths.

A normal FITS binary table has a shared row structure, so its columns cannot ordinarily have independently mismatched observation counts in the way the proposed test suggests.

The model's array-alignment validation already tests that condition. The importer should instead test malformed or unsupported FITS table structures where appropriate.

Similarly, testing whether a memory-mapped array fails after closing the FITS file is not necessarily the best resource-management test. A better test would verify that the importer returns usable, independently owned arrays after the FITS file has closed.

### 6. Unexpected data types need stricter handling

Section 6, C8, suggests coercing unexpected column types to numeric values when possible.

I would avoid permissive coercion for the initial importer. For example, a string column containing `"123.4"` might convert successfully, but that does not establish that the column is scientifically a valid measurement.

Recommended behavior:

- Accept supported numeric FITS column types.
- Convert accepted numeric data to the model's required `float64` or `int64`.
- Reject incompatible types with a meaningful `FITSImportError`.
- Do not silently interpret strings as measurements.

This is a scientific data-integrity safeguard.

## 2. Additional refinements

These are not blockers to the overall architecture, but should be clarified in the implementation plan.

| Area                      | Recommendation                                                                                                                                             |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Empty light-curve table   | Explicitly reject a table with zero observations.                                                                                                          |
| Multiple candidate tables | Keep the deterministic selection strategy, but ensure ambiguity is reported.                                                                               |
| Time metadata             | Map `TIMEUNIT`, `TIMESYS`, `TIMEREF`, and `BJDREFI`/`BJDREFF` independently. Never silently convert BKJD to JD.                                            |
| `TIMEDEL`                 | Consider mapping it to `TimeInfo.resolution` only if its meaning and unit are verified. Otherwise preserve it as additional metadata or leave it unmapped. |
| Row indices               | Ensure `ValidationFinding.row_indices` are zero-based, even though FITS table rows are conventionally discussed using one-based numbering.                 |
| Column matching           | Define whether supported column names are matched case-insensitively.                                                                                      |
| FITS headers              | Explicitly define how primary and extension headers are combined, respecting `INHERIT` and extension-level overrides.                                      |

One other point: the plan says both SAP and PDCSAP are required, then correctly clarifies that at least one is sufficient. The latter should be the authoritative requirement throughout the implementation.

## 3. What I would retain unchanged

The following decisions are correct and should carry forward:

- `src/fits_importer.py` as a separate, UI-independent module.
- Reuse of `src/light_curve.py` without redesigning the model.
- Astropy and NumPy only; no new dependencies.
- Structural HDU identification rather than assuming the light-curve table is always HDU 1.
- Independent preservation of `SAP_FLUX` and `PDCSAP_FLUX`.
- Correct pairing of flux and uncertainty columns.
- Preservation of NaN and infinity values.
- Preservation of quality flags and cadence numbers.
- No automatic quality-bitmask filtering.
- Copying FITS arrays before closing the file.
- Temporary FITS fixtures for portable automated testing.
- Real Kepler-file verification as an optional local test.
- No project persistence, GUI integration, visualization, or BLS work.

## 4. Recommended next step

I recommend one small revision to the plan before approving implementation.

Have Nemotron update its report to address the six corrections and the additional refinements above. It should not change any files or begin implementation.

The revised plan should explicitly preserve these boundaries:

Subtask 2.2.2

In scope

- FITS file reading
- HDU identification
- Measurement extraction
- Metadata extraction
- Import validation
- Focused automated tests

Deferred

- Project association and persistence — 2.2.3
- Broader integration verification and documentation reconciliation — 2.2.4
- Visualization and BLS — later work

My assessment: The proposed architecture is appropriate. The main concerns are the redundant result interface, the testing schedule, and the metadata/type-handling details. These are straightforward corrections, not reasons to redesign the importer.

I can provide a consolidated PLAN-mode revision prompt for Nemotron that incorporates all of these corrections.


# Chatgpt plan v2 prompt


Use this as the follow-up prompt for Nemotron. It is explicitly PLAN mode only: revise the existing 2.2.2 implementation plan, resolve the identified issues, and return the corrected report without touching project files.

# PLAN MODE — Subtask 2.2.2: FITS Import and Validation — Plan Revision

**Mode: PLAN ONLY. Do not implement, modify, create, delete, or rename files. Do not switch to BUILD mode.**

## 1. Context

You have already produced a planning report for Stage 2, Subtask 2.2.2 — FITS Import and Validation.

That report was reviewed. Its overall architecture was considered appropriate, but several details require correction before the plan can be approved.

Your task is to revise the existing plan, incorporating the corrections and clarifications below.

This is a planning revision, not a new investigation from scratch. Reuse the verified repository facts, actual model interfaces, FITS inspection findings, and Foundation references from your previous report. However, if any detail is uncertain or inconsistent, inspect the actual working repository and source material again rather than assuming the earlier report was correct.

## 2. Repository and project safeguards

Continue following `AGENTS.md` and all applicable project instructions.

- Inspect the actual working tree before making claims about repository state.
- Do not overwrite, discard, or modify pre-existing user changes.
- Treat Foundation documents as authoritative and read-only.
- Preserve the distinction between verified facts, assumptions, recommendations, and approved decisions.
- Do not create or modify planning documents, implementation files, tests, or documentation.
- Do not run implementation or make configuration/dependency changes.
- Do not commit, push, or otherwise alter Git state.

The previous report identified these pre-existing working-tree changes:

- Modified: `docs/planning/.../subtask-2.2-light-curve-import OVERVIEW.md`
- Untracked: `docs/planning/.../task 2.2.2 FITS import and validation WORKING PROGRESS LOG.md`

Verify that these remain untouched. Do not assume their status without checking.

The previous report also verified:

- `src/light_curve.py` exists.
- `tests/test_light_curve.py` exists.
- The full baseline is **224 passed**.

Reconfirm only what is necessary to ensure the revised plan remains grounded in the current repository state.

## 3. Required corrections

### 3.1 Simplify the importer interface

The previous plan proposed both:

- A `FitsImportResult` dataclass containing success, dataset, source, validation, and error fields.
- A `FITSImportError` exception for file-level failures.

This duplicates information and creates two competing ways of representing failure.

Revise the recommendation to use the simpler initial interface:

**Successful import:**

- Return a constructed `LightCurveDataset`.
- Store non-fatal validation findings in `dataset.validation`.

**Failed import:**

- Raise a dedicated `FITSImportError` with a meaningful explanation.
- Do not return a partially populated dataset.
- Do not introduce a separate result dataclass in this subtask.

The importer should distinguish:

- File access and FITS parsing failures.
- Missing or unusable light-curve structure.
- Missing required columns.
- Incompatible data types.
- Structural model-construction failures.

Explain how exceptions should preserve useful underlying error context without exposing unnecessary implementation details to eventual users.

Do not add GUI error handling.

### 3.2 Correct the testing schedule

The previous report placed automated importer tests under 2.2.4 in one section, while its implementation sequence placed them in 2.2.2.

Resolve this contradiction.

The correct division is:

**Subtask 2.2.2:**

- Implement the FITS importer.
- Create focused automated importer tests.
- Test extraction, metadata mapping, validation findings, failure handling, resource safety, and data preservation.
- Run the focused tests and full existing suite.
- Ensure the existing 224-test baseline has no regressions.

**Subtask 2.2.4:**

- Broader Stage 2.2 verification.
- Integration-level review.
- Consolidated documentation reconciliation.
- Final completion assessment across the relevant subtasks.

Do not postpone the importer's own tests to 2.2.4.

### 3.3 Correct source metadata mapping

The previous report suggested mapping `ORIGIN=NASA/Ames` to `DatasetSource.archive` or `source_id`.

That is not sufficiently justified.

Revise the mapping as follows:

| Model field          | Proposed source                                                                                                     |
| -------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `mission`            | `MISSION` or verified equivalent, e.g. Kepler                                                                       |
| `instrument`         | `INSTRUME`                                                                                                          |
| `target_object`      | `OBJECT`                                                                                                            |
| `source_id`          | `KEPLERID` or another verified target/product identifier, with a clear distinction between target ID and product ID |
| `archive`            | `None` unless the supplying archive is independently established                                                    |
| `original_filename`  | Actual input filename                                                                                               |
| `original_file_path` | Actual input path                                                                                                   |

`ORIGIN=NASA/Ames` may be retained in notes or an informational finding if useful, but must not automatically be described as the archive from which the user obtained the file.

Do not invent source metadata. If a header is absent or ambiguous, leave the corresponding field unknown.

Explain how metadata conflicts between primary and extension headers are handled.

### 3.4 Define dataset naming

The model requires a `LightCurveDataset.name`, but the previous report did not specify how the importer populates it.

Recommend a deterministic initial rule:

- Use the input filename stem as the dataset name.
- Preserve the full original filename separately in `DatasetSource.original_filename`.
- Do not invent a target name or scientific label when the filename is the only reliable identifier.

For example:

`kplr011904151-2009131105131_llc_full.fits`

becomes:

`kplr011904151-2009131105131_llc_full`

If the filename cannot provide a usable name, specify a safe failure or fallback behavior. Do not silently invent a descriptive scientific name.

### 3.5 Correct FITS fixture assumptions

The previous plan proposed an automated fixture with inconsistent column lengths.

A standard FITS binary table has a shared row structure. Its columns do not ordinarily have independent observation counts in the manner implied by that proposed test.

Revise the test plan:

- Remove the assumption that a normal FITS binary table can directly represent independently mismatched column lengths.
- Keep model-level array-alignment testing in `tests/test_light_curve.py`, where the condition is already covered.
- Test importer behavior against malformed or unsupported FITS structures only where such a fixture can be constructed realistically.
- Do not invent malformed FITS cases simply to increase test count.

For resource safety, do not rely solely on trying to access a memory-mapped array after file closure.

Instead, test that:

- The importer returns usable arrays after the FITS file has closed.
- Returned arrays do not depend on an open FITS file handle.
- Imported data remains intact and independently owned.

### 3.6 Tighten numeric dtype handling

The previous plan proposed coercing unexpected types to numeric values when possible.

Revise this behavior to prioritize scientific data integrity.

Recommended policy:

- Accept supported numeric FITS column types.
- Convert accepted numeric arrays into the model's required `float64` or `int64` representation.
- Handle FITS endianness correctly.
- Preserve non-finite floating-point values.
- Reject incompatible types with a meaningful `FITSImportError`.
- Do not silently interpret string columns as scientific measurements merely because their contents can be parsed as numbers.
- Do not silently truncate floating-point quality or cadence values into integers.

If there are legitimate FITS numeric representations that need special handling, identify them explicitly and explain the conversion.

Do not broaden the importer into a universal type-conversion framework.

## 4. Additional refinements to incorporate

Address the following points in the revised plan.

### 4.1 Empty light-curve tables

Explicitly define behavior for a table with zero observations.

Recommended initial behavior: reject it with `FITSImportError`, because it cannot provide a usable light-curve dataset for this subtask.

Do not confuse an empty table with a valid table containing non-finite measurements.

### 4.2 Multiple candidate tables

Retain structural HDU identification rather than assuming a fixed HDU index.

The previous recommendation was:

1. Identify table HDUs containing `TIME` and at least one supported flux column.
2. Prefer a structurally matching table named `LIGHTCURVE`.
3. If multiple candidates remain, apply a deterministic selection rule.
4. Report ambiguity through an informational finding or warning.
5. Do not silently choose a scientifically questionable candidate.

Clarify the tie-breaking strategy and whether ambiguity should ever prevent import.

Keep the implementation Kepler-product-aware without attempting to support every possible FITS convention.

### 4.3 Time metadata

Define independent handling for:

- `TIMEUNIT`
- `TIMESYS`
- `TIMEREF`
- `BJDREFI`
- `BJDREFF`
- Table-column `TUNITn`

Do not assume these values are interchangeable.

For the verified Kepler example:

- TIME values are BKJD-style values, representing BJD minus the reference offset.
- The unit is days.
- The time scale is TDB.
- The reference frame is SOLARSYSTEM.
- `BJDREFI` and `BJDREFF` establish the reference offset.

Do not convert BKJD to JD or alter the original time values.

Clarify how the importer separates:

- Time unit.
- Time reference/convention.
- Time scale.
- Time reference frame.
- Numeric reference value.

For `TIMEDEL`, consider mapping it to `TimeInfo.resolution` only if the header meaning and units are verified. Otherwise, do not force it into that field.

### 4.4 Validation row indices

`ValidationFinding.row_indices` uses zero-based indices.

Ensure every proposed importer finding uses zero-based row indices, even when FITS rows are discussed using one-based numbering.

### 4.5 Column-name matching

Specify whether supported FITS column names are matched case-insensitively.

Use a deterministic policy. Do not allow case-insensitive matching to create silent ambiguity when multiple columns differ only by case.

If duplicate or conflicting supported names occur, define whether import should fail.

### 4.6 Header inheritance and precedence

Clarify how primary and extension headers are combined.

Consider:

- Primary header metadata.
- Extension header metadata.
- FITS `INHERIT` behavior.
- Extension-specific time metadata.
- Conflicting values.

Do not assume every extension inherits all primary-header keywords unless the FITS conventions and actual file structure support that interpretation.

Prefer extension-specific values for extension-specific metadata where appropriate, while preserving the distinction between inherited and explicitly declared values when that distinction matters.

## 5. Preserve the approved architecture and scope

Unless the investigation reveals a genuine incompatibility, retain these decisions:

- New module: `src/fits_importer.py`.
- Reuse `src/light_curve.py` without redesign.
- Astropy, NumPy, and standard library only.
- No new dependencies.
- No PySide6 or GUI coupling.
- No project/service/repository imports.
- No database or permanent persistence.
- No project association or project IDs in the scientific model.
- No visualization.
- No BLS implementation.
- No archive downloading.
- No automatic quality-bitmask filtering.
- No universal FITS framework.

The importer should:

1. Open FITS files read-only.
2. Identify the appropriate light-curve table structurally.
3. Extract supported measurements and metadata.
4. Copy required arrays before the FITS file closes.
5. Preserve non-finite measurements and quality flags.
6. Construct the existing `LightCurveDataset`.
7. Attach validation warnings and informational findings.
8. Return the dataset or raise `FITSImportError`.

Keep SAP and PDCSAP as independent measurement columns. Pair each with its corresponding uncertainty column. If one flux series exists without the other, import the available series. Missing uncertainty columns should result in `uncertainties=None`, with an appropriate warning.

## 6. Validation matrix

Revisit the previous validation matrix and ensure it reflects the corrections above.

At minimum, cover:

- Missing/unreadable file.
- Corrupted or invalid FITS structure.
- No suitable table HDU.
- Missing TIME.
- Missing both supported flux columns.
- Empty table.
- Only SAP or only PDCSAP available.
- Missing uncertainty columns.
- Orphaned uncertainty columns.
- Missing optional quality/cadence columns.
- Unexpected/incompatible data types.
- Non-finite timestamps.
- Non-finite flux values.
- Non-finite uncertainty values.
- Negative uncertainty values.
- Duplicate timestamps.
- Non-monotonic timestamps.
- Nonzero quality flags.
- Missing time units or reference metadata.
- Missing measurement units.
- Multiple candidate table HDUs.
- Duplicate/conflicting supported column names.
- Array alignment and model-construction errors.

For every condition, specify:

- Whether import succeeds or fails.
- Whether the condition becomes a warning or informational finding.
- Whether the data is preserved.
- Whether the importer raises `FITSImportError`.
- Whether user approval is needed.

Do not silently remove observations, reorder data, replace NaN/inf, or filter quality flags.

## 7. Testing plan

Provide a corrected focused test plan for 2.2.2.

Use temporary FITS fixtures created under pytest `tmp_path`. The automated suite must not require the user's external Kepler dataset or absolute Windows paths.

Include tests for:

- Valid Kepler-like multi-HDU table.
- Table at a different HDU index.
- Structural table identification.
- Multiple candidate tables.
- Missing required columns.
- Only SAP and only PDCSAP.
- Correct uncertainty pairing.
- Missing uncertainty columns.
- Missing optional quality/cadence columns.
- Supported numeric dtypes and endianness.
- Rejection of incompatible string/object types.
- Preservation of NaN/inf.
- Negative uncertainty warning.
- Duplicate/non-monotonic time findings.
- Missing metadata.
- Duplicate/conflicting column names.
- Empty table.
- Corrupt/unreadable file.
- Successful dataset construction and model compatibility.
- Arrays remaining usable after FITS closure.
- Preservation of observation count and original data values.
- Correct zero-based validation row indices.

Keep model-only validation tests in `tests/test_light_curve.py` rather than duplicating them in importer tests.

The optional real-data verification should remain gated on the actual Kepler file being present. It must never make the portable test suite dependent on that file.

## 8. Documentation requirements

Respect `AGENTS.md` documentation-maintenance requirements.

The revised plan should identify which documentation will need updates during Build mode, without modifying any documents now.

Distinguish:

**2.2.2 implementation documentation:**

- Record the importer module and its responsibilities.
- Record public interfaces and error behavior.
- Record supported FITS structure and column mapping.
- Record validation behavior and limitations.
- Record focused test coverage and results.
- Update the development log and roadmap as required.

**2.2.4 consolidation:**

- Broader documentation reconciliation.
- Cross-subtask completion status.
- Overall Stage 2.2 verification.
- Any remaining deferred or unresolved items.

Foundation documents remain read-only.

Do not assume all documentation can be postponed to 2.2.4 if `AGENTS.md` requires relevant documentation updates during the 2.2.2 Build task.

## 9. Revised planning deliverable

Return a complete revised implementation plan, not merely a list of changes.

It must contain:

1. Repository state and preparation.
2. Verified 2.2.1 model review.
3. Confirmed FITS inspection findings.
4. Proposed importer module and public interface.
5. HDU identification and header handling.
6. Measurement and metadata mapping.
7. Complete validation matrix.
8. Error-handling strategy.
9. Focused 2.2.2 automated testing plan.
10. Optional real-data verification.
11. Data-integrity and resource-management approach.
12. Documentation impact assessment.
13. Explicit 2.2.2 / 2.2.3 / 2.2.4 boundaries.
14. Risks and unresolved issues.
15. Recommended Build implementation sequence.
16. Decisions or questions that genuinely require user approval.

Use tables where they improve clarity.

Do not repeat the original report verbatim. Incorporate the corrections into one internally consistent plan.

## 10. Final instructions

This remains PLAN mode.

Do not:

- Create or edit files.
- Modify source code.
- Create or modify tests.
- Install dependencies.
- Change project configuration.
- Modify the FITS source file.
- Change Git state.
- Begin implementation.
- Claim the revised plan has user approval.

Explicitly identify any facts that could not be reverified.

At the end, provide:

- A concise list of material changes made to the previous plan.
- Any remaining uncertainties or approval requirements.
- A clear statement that implementation has not started and the plan awaits user review.

Stop after presenting the revised report. Do not automatically proceed to Build mode.

When Nemotron returns the revised report, send it here. I’ll review the technical decisions and scope consistency before you authorize implementation.


# opencode plan v2 

I now have an accurate picture of the current repository state. Important correction to my previous report: there is a pre-existing user commit `113a9ab task 2.2.2 planning begin` (by Brett, not by me) and the working-tree changes differ from what I earlier stated. I'll present the complete revised plan grounded in the verified current state.

---

# Subtask 2.2.2 — FITS Import and Validation: Revised Implementation Plan

**Mode: PLAN ONLY. No implementation, file creation, modification, or deletion. No switch to Build mode.**

This report revises the prior planning report, incorporating all required corrections. Verified repository facts, model interfaces, FITS findings, and Foundation references are retained; only the corrected items and newly verified state are changed.

---

## 1. Repository State and Preparation

### 1.1 Verified repository facts (current, re-checked)

| Item | Verified value |
|---|---|
| Working directory | `C:\Code\New_Project` (git repo, branch `master`) |
| HEAD commit | `113a9ab task 2.2.2 planning begin` — **Author: Brett, Date: Wed Nov 4 13:52:42 2026**. This is a **pre-existing user commit; I did not create it.** |
| Previous commit | `f65f14f Task 2.2.1` |
| Working tree vs HEAD | **One modified file (not staged):** `docs/planning/Stage 2+ work planning aka overviews and prompts/Stage 2_n_n planning/stage 2_2_n planning/task 2.2.2 FITS import and validation WORKING PROGRESS LOG.md` (+1,119 insertions beyond the commit). This is a **pre-existing user change; I have not touched it.** |
| Untracked files | None |
| `subtask-2.2-light-curve-import OVERVIEW.md` | **Not currently modified** — it was committed in `113a9ab`. |

### 1.2 Correction to previous report on working-tree state
My prior report stated `subtask-2.2-light-curve-import OVERVIEW.md` was modified and `task 2.2.2 FITS import and validation WORKING PROGRESS LOG.md` was untracked. That description is **no longer accurate**. Current verified state:
- `WORKING PROGRESS LOG.md` is **tracked and modified** (pre-existing user edit; left untouched).
- `OVERVIEW.md` is **unmodified** in the working tree (committed in `113a9ab`).
- No files were created, modified, or deleted by me in this session.

### 1.3 Confirmation that Subtask 2.2.1 exists
**Verified.** `src/light_curve.py` and `tests/test_light_curve.py` both exist (confirmed via `Test-Path`: both `True`). The `src/` package contains `__init__.py`, `light_curve.py`, `project_model.py`, `project_service.py`, `project_repository.py`, `config_provider.py`, `main_window.py`, `main.py`, `new_project_dialog.py`, `open_project_dialog.py`.

### 1.4 Current test baseline (reconfirmed by running the suite)
`python -m pytest -q` → **224 passed in 7.26s, 0 failed.** Matches the prior baseline. No existing files were modified to achieve this. This is the regression baseline for 2.2.2.

### 1.5 Relevant Foundation requirements (citations)
- **§3.4.1** — preserve units, distinguish measurement types, identify missing/invalid measurements, preserve uncertainties.
- **§3.4.3** — preserve original timestamps/time metadata; do not assume ordinary Julian Date; identify missing/ambiguous time.
- **§3.4.4** — preserve original measurements; derived outputs only as identifiable separate operations (none in this task).
- **§4.4** — FITS supported (4.4.2); preserve original files/structures (4.4.1); units/time conventions (4.4.7–4.4.8); metadata is part of dataset (4.4.6).
- **§4.5** — user-provided file import (4.5.2); metadata classifications verified/user-supplied/inferred/unknown (4.5.3); never fabricate missing info (4.5.2, 4.5.10); preserve original files unchanged (4.5.2, 4.5.10).
- **§4.7** — preserve original source, filename, mission/instrument/target identifiers; distinguish original from inferred (4.7.1–4.7.4, 4.7.10); `ORIGIN` is not automatically an archive.
- **§5.1** — preserve original data/units/metadata/uncertainty; distinguish missing from measured zero (5.1.4); computational success ≠ scientific validity (5.1.8).
- **§5.6** — initial quality assessment on import (5.6.1); distinguish errors/warnings/info (5.6.1, 5.6.7); never auto-reject useful datasets (5.6.1); zero-based findings consistent with model.
- **§9.2** — modularity, scientific/UI separation, independent testability, avoid unnecessary dependencies (9.2.1–9.2.7).
- **§9.4** — preserve original imported files; separate original from derived; data integrity (9.4.2, 9.4.6).
- **§10** — AI decision boundaries and user approval (10.4, 10.9).

### 1.6 Existing user changes / repository-state concerns
The two pre-existing planning-file changes (one committed in `113a9ab`, one modified in the working tree) are outside `src/` and `tests/` and predate this task. They will not be touched. No commits/pushes will be made by me.

---

## 2. Verified 2.2.1 Model Review

All details below are from direct inspection of `src/light_curve.py` (493 lines) and `tests/test_light_curve.py` (759 lines), not assumed from the earlier report.

### 2.1 Model components and interfaces

| Component | Fields / behavior (verified) |
|---|---|
| `DatasetSource` | `original_filename`, `original_file_path`, `archive`, `source_id`, `mission`, `instrument`, `target_object`, `checksum` — all `str \| None`, default `None`. |
| `TimeInfo` | `values: np.ndarray` (required); `unit`, `reference`, `time_scale`, `time_reference_frame` (str, default `""`); `reference_value`, `start`, `stop`, `resolution`, `format_hint` (float/str, default `None`). Unknown → `""`/`None`; does not block construction. |
| `MeasurementColumn` | `name: str`, `values: np.ndarray`, `unit: str = ""`, `uncertainties: np.ndarray \| None = None`, `description: str \| None = None`. Property `n_nonfinite`. Non-finite preserved; `None` uncertainties ≠ zero-array uncertainties. |
| `MeasurementSeries` | `series: dict[str, MeasurementColumn]`; keys must equal `column.name`; no duplicates. |
| `ValidationFinding` | `code`, `message`, `severity`, `column: str \| None`, `row_indices: list[int] \| None` (zero-based). |
| `ValidationReport` | `errors`, `warnings`, `info` lists of `ValidationFinding`. |
| `LightCurveDataset` | `dataset_id` (UUID, auto), `name` (str, required), `source`, `time`, `measurements`, `quality_flags: np.ndarray \| None`, `cadence_numbers: np.ndarray \| None`, `validation`, `imported_at` (auto ISO UTC), `notes: str \| None`. Property `n_observations`. |

### 2.2 Structural validation (`__post_init__`)
Raises `LightCurveValidationError` (subclass of `ValueError`) for: invalid `dataset_id`; missing/non-ndarray `time.values`; non-str `time.unit`; non-`MeasurementSeries` measurements; key/name mismatch; duplicate names; non-ndarray column values/unit/uncertainties; any array length mismatch with time (values, non-None uncertainties, quality_flags, cadence_numbers); non-`ValidationReport` validation; non-str `imported_at`.

### 2.3 Array copying and ownership
`_copy_arrays` converts `time.values` and each measurement `values`/`uncertainties` to `np.array(..., dtype=np.float64, copy=True)`; `quality_flags`/`cadence_numbers` to `np.array(..., dtype=np.int64, copy=True)`. The model always owns independent copies. The importer must still copy FITS memory-mapped arrays **before** closing the file (the model's copy is a second safety copy).

### 2.4 Serialization
`to_dict()` → JSON-compatible dict; arrays → `.tolist()`; `None` preserved as `None` (distinguishable from zero arrays). `from_dict(data)` reconstructs and re-validates via `__post_init__`; distinguishes `None` from arrays; round-trips all fields including validation report, quality flags, cadence numbers, source metadata.

### 2.5 Compatibility with Kepler FITS dataset
**Compatible — no model change required.** Mapping (Section 6). Non-finite flux (SAP 4, PDCSAP 7) preserved; 37 nonzero quality flags preserved (no filtering); BKJD/TDB/SOLARSYSTEM stored in separate `TimeInfo` fields; float32 → float64 upcast is value-preserving; big-endian FITS dtypes converted by `np.array(..., dtype=..., copy=True)`.

### 2.6 Genuine gaps / incompatibilities
None requiring a model change for 2.2.2. `TimeInfo.resolution` could hold `TIMEDEL` only if its meaning/units are verified; otherwise left `None`. Raw FITS `TTYPE`/`TFORM`/`NULL` per column, full header card list, aperture image (HDU2), and PDC config keywords are not represented; they can go in `LightCurveDataset.notes` or remain out of scope. Any model-field addition would be a 2.2.1-scope decision requiring approval and is explicitly out of scope here.

---

## 3. Confirmed FITS Inspection Findings

Verified against the actual file `C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits` (read-only, outside repo, unchanged) using Astropy 7.2.0.

### 3.1 HDU structure
| HDU | Type | EXTNAME | Rows/Cols | Notes |
|---|---|---|---|---|
| 0 | `PrimaryHDU` | `PRIMARY` | — | 58 cards |
| 1 | `BinTableHDU` | `LIGHTCURVE` | 476 × 20 | Light-curve table |
| 2 | `ImageHDU` | `APERTURE` | 12 × 10 | Aperture mask |

`NEXTEND=2` matches the two extensions. The table is at index 1 **but the importer must not hardcode index 1** — it identifies the table structurally (Section 5).

### 3.2 LIGHTCURVE columns (verified)
| # | Column | Format | dtype (stored) | Unit (TUNIT) | 2.2.2 role |
|---|---|---|---|---|---|
| 1 | `TIME` | D | `>f8` | `BJD - 2454833` | **Required** (time) |
| 2 | `TIMECORR` | E | `>f4` | `d` | Unsupported |
| 3 | `CADENCENO` | J | `>i4` | — | **Optional** (cadence) |
| 4 | `SAP_FLUX` | E | `>f4` | `e-/s` | **Required flux** (at least one of SAP/PDCSAP) |
| 5 | `SAP_FLUX_ERR` | E | `>f4` | `e-/s` | **Optional** uncertainty for SAP_FLUX |
| 6 | `SAP_BKG` | E | `>f4` | `e-/s` | Unsupported |
| 7 | `SAP_BKG_ERR` | E | `>f4` | `e-/s` | Unsupported |
| 8 | `PDCSAP_FLUX` | E | `>f4` | `e-/s` | **Required flux** (at least one of SAP/PDCSAP) |
| 9 | `PDCSAP_FLUX_ERR` | E | `>f4` | `e-/s` | **Optional** uncertainty for PDCSAP_FLUX |
| 10 | `SAP_QUALITY` | J | `>i4` | — | **Optional** quality flags |
| 11–20 | centroid/position columns (+ errors) | D/E | mixed | pixel/pixels | Unsupported |

### 3.3 Data values (verified)
| Column | Non-finite | Min | Max | Notes |
|---|---|---|---|---|
| `TIME` | 0 | 120.53914651 | 130.24539528 | All finite |
| `CADENCENO` | N/A (int) | 568 | 1043 | Consecutive |
| `SAP_FLUX` | 4 | 532355.0 | 532944.06 | Preserved as-is |
| `SAP_FLUX_ERR` | 4 | ~20.04 | ~20.05 | Same 4 rows as SAP_FLUX |
| `PDCSAP_FLUX` | 7 | 501346.12 | 501746.75 | Preserved as-is |
| `PDCSAP_FLUX_ERR` | 7 | ~20.57 | ~20.77 | Same 7 rows as PDCSAP_FLUX |
| `SAP_QUALITY` | N/A (int) | — | — | 37 nonzero; values `{64, 128, 8192, 8320, 12352, 32800}` |
| `PSF_CENTR1` | 476 (all NaN) | — | — | Unsupported column |

### 3.4 Header metadata (verified)
**Primary:** `TELESCOP=Kepler`, `INSTRUME=Kepler Photometer`, `OBJECT=KIC 11904151`, `KEPLERID=11904151`, `ORIGIN=NASA/Ames`, `MISSION=Kepler`, `QUARTER=0`, `OBSMODE=long cadence`, `DATE=2015-08-26`, `CREATOR=...FluxExporter2PipelineModule`, `FILEVER=6.1`.

**LIGHTCURVE extension (`INHERIT=True`):** `TIMEREF=SOLARSYSTEM`, `TASSIGN=SPACECRAFT`, `TIMESYS=TDB`, `BJDREFI=2454833`, `BJDREFF=0.0`, `TIMEUNIT=d`, `TSTART=120.52892942`, `TSTOP=130.25561236`, `TELAPSE=9.72668293`, `TIMEDEL=0.02043359821692`, `EXPOSURE=8.95472397`, `DATE-OBS`, `DATE-END`, PDC keywords.

### 3.5 Time convention (verified)
Values are `BJD − 2454833` (BKJD-style), days (`TIMEUNIT=d`), time system `TDB`, reference frame `SOLARSYSTEM`, `BJDREFI=2454833`, `BJDREFF=0`. **Not ordinary Julian Date.** Must not be silently converted or relabeled as JD.

### 3.6 Comparison with prior findings (REVIEW-002)
All previously established findings confirmed; none contradicted. Newly verified: exact TIME range, exact SAP_QUALITY nonzero values `{64, 128, 8192, 8320, 12352, 32800}`, `PSF_CENTR1` all-NaN (476). File is accessible, so no limitation is reported.

---

## 4. Proposed Importer Module and Public Interface

### 4.1 Module path
`src/fits_importer.py` — new module alongside `src/light_curve.py`. Single module initially; no package split unless it grows beyond a coherent responsibility.

### 4.2 Dependencies
`astropy.io.fits` (approved, DEC-006), `numpy` (approved), `src.light_curve` (reused model). Standard library only otherwise. **No new dependencies.** No PySide6, no project/service/repository imports.

### 4.3 Simplified public interface (corrected per 3.1)

**Successful import:** return a constructed `LightCurveDataset`. Non-fatal validation findings are stored in `dataset.validation` (warnings/info). No separate result dataclass.

**Failed import:** raise a dedicated `FITSImportError` with a meaningful explanation. Do **not** return a partially populated dataset. Do **not** introduce a separate result dataclass in this subtask.

Proposed signature:
```python
class FITSImportError(Exception):
    """Raised when a file-level condition prevents FITS light-cube import."""

def import_light_curve(file_path: str | os.PathLike[str]) -> LightCurveDataset:
    """Read a FITS light-curve file and return a LightCurveDataset.

    Raises FITSImportError for file access, FITS parsing, missing/unsuitable
    table structure, missing required columns, incompatible data types, empty
    tables, or model-construction failures. Non-fatal scientific conditions are
    reported via the returned dataset's ValidationReport.
    """
```

### 4.4 Failure categories the importer distinguishes
1. File access failures (missing, unreadable, permission).
2. FITS parsing failures (corrupted, invalid structure).
3. Missing or unusable light-curve structure (no table with TIME + flux column).
4. Missing required columns (`TIME`, or neither `SAP_FLUX` nor `PDCSAP_FLUX`).
5. Incompatible data types (non-numeric where numeric required).
6. Structural model-construction failures (array length mismatch, bad UUID, etc. — surfaced as `LightCurveValidationError` wrapped/re-raised as `FITSImportError` with context).

### 4.5 Exception context preservation
Exceptions should chain the underlying cause (`raise FITSImportError(...) from exc`) so the cause is inspectable (`__cause__`), while the user-facing message is meaningful and does not leak implementation details (e.g., avoid exposing raw FITS card objects or internal stack traces to end users). The caller decides how to present the message (GUI, log, CLI). No GUI error handling in this subtask.

### 4.6 Why no result dataclass
A `FitsImportResult` dataclass plus `FITSImportError` duplicates failure representation. The simpler interface (return dataset on success; raise exception on failure) is sufficient for 2.2.2 and keeps the boundary clean. A result type can be added in a later subtask if the caller needs to inspect warnings without exceptions.

---

## 5. HDU Identification and Header Handling

### 5.1 HDU identification (structural, not fixed index)
1. Open with `fits.open(path, mode="readonly")` inside a `with` block (guaranteed close on success and failure).
2. Iterate all HDUs; candidates are table HDUs (`BinTableHDU`/`TableHDU`) whose column names include `TIME` and at least one of `SAP_FLUX` / `PDCSAP_FLUX`.
3. Prefer a candidate whose `EXTNAME == "LIGHTCURVE"` (Kepler convention) if present.
4. If multiple structural candidates remain after preferring `LIGHTCURVE`, apply a deterministic tie-break (e.g., first candidate in HDU order) and report ambiguity via an informational finding/warning in `dataset.validation`.
5. If no candidate → `FITSImportError` (no usable light-curve table).
6. Ambiguity **does not** automatically prevent import when a reasonable deterministic choice exists; it only prevents import if no candidate satisfies the structural rule.

All array copies are made **inside** the `with` block before the file closes (memory-mapped FITS data must not be accessed after close).

### 5.2 Header handling (corrected per 4.6)
- Primary-header metadata and extension-header metadata are both read.
- `INHERIT=True` on the extension means it inherits primary-header keywords; extension-specific keywords override/extend for extension-specific metadata.
- Extension-specific time metadata (`TIMESYS`, `TIMEREF`, `BJDREFI`, `BJDREFF`, `TIMEUNIT`, `TSTART`/`TSTOP`) takes precedence for time interpretation; primary header provides mission/instrument/target/source context.
- Conflicts: extension-specific values are preferred for extension-specific metadata; primary values are used only when the extension does not declare them. The distinction is preserved conceptually but the model does not have separate fields for "inherited vs explicit" — a single resolved value is stored, with conflicts noted in `notes`/info only if material.
- Do not assume every extension inherits all primary keywords unless the actual file structure supports it (verified: this file's extensions declare `INHERIT=True`).

---

## 6. Measurement and Metadata Mapping

### 6.1 Required / optional / unsupported table columns

| FITS column | Role | Required for construction? | Model target | Absent behavior |
|---|---|---|---|---|
| `TIME` | timestamps | **Yes** | `TimeInfo.values` (+ metadata) | `FITSImportError` |
| `SAP_FLUX` | SAP flux | At least one of SAP/PDCSAP | `MeasurementColumn("SAP_FLUX")` | — |
| `PDCSAP_FLUX` | PDC flux | At least one of SAP/PDCSAP | `MeasurementColumn("PDCSAP_FLUX")` | — |
| `SAP_FLUX_ERR` | SAP uncertainty | Optional | `SAP_FLUX.uncertainties` | `None`, warning |
| `PDCSAP_FLUX_ERR` | PDC uncertainty | Optional | `PDCSAP_FLUX.uncertainties` | `None`, warning |
| `SAP_QUALITY` | quality flags | Optional | `quality_flags` (int64) | `None` |
| `CADENCENO` | cadence ids | Optional | `cadence_numbers` (int64) | `None` |
| Other columns | — | No | Not imported | possibly noted in `notes` |

SAP and PDCSAP remain independent columns, each paired with its own `*_FLUX_ERR`. Never merged. Never one silently discarded for the other.

### 6.2 Source metadata mapping (corrected per 3.3)

| `DatasetSource` field | Proposed source | Notes |
|---|---|---|
| `mission` | `MISSION` header (e.g. `Kepler`) | Leave `None` if absent |
| `instrument` | `INSTRUME` header | Leave `None` if absent |
| `target_object` | `OBJECT` header | Leave `None` if absent |
| `source_id` | `KEPLERID` (target ID) | Distinct from product/file ID; leave `None` if absent |
| `archive` | `None` | **Not** `ORIGIN` unless the supplying archive is independently established |
| `original_filename` | Actual input filename | |
| `original_file_path` | Actual input path | |

`ORIGIN=NASA/Ames` may be retained in `notes` or an informational finding if useful, but **must not** automatically be described as the archive. Do not invent source metadata; absent/ambiguous → field unknown.

### 6.3 Dataset naming (corrected per 3.4)
- `LightCurveDataset.name` = input filename stem (e.g. `kplr011904151-2009131105131_llc_full` for `..._llc_full.fits`).
- Full original filename preserved in `DatasetSource.original_filename`; full path in `original_file_path`.
- Do not invent a target name or scientific label when the filename is the only reliable identifier.
- If the filename cannot provide a usable name (e.g., empty stem), raise `FITSImportError` rather than silently inventing a descriptive name.

### 6.4 Time metadata mapping (corrected per 4.3) — independent handling

| Model field | Source | Verified Kepler value | Notes |
|---|---|---|---|
| `TimeInfo.unit` | `TIMEUNIT` / `TUNIT1` | `"d"` | Days |
| `TimeInfo.reference` | `TUNIT1` / convention | `"BJD - 2454833 (BKJD)"` | Reference/convention |
| `TimeInfo.time_scale` | `TIMESYS` | `"TDB"` | Time scale |
| `TimeInfo.time_reference_frame` | `TIMEREF` | `"SOLARSYSTEM"` | Reference frame |
| `TimeInfo.reference_value` | `BJDREFI` (+ `BJDREFF`) | `2454833.0` | Numeric reference offset |
| `TimeInfo.start` | `TSTART` | `120.52892942` | |
| `TimeInfo.stop` | `TSTOP` | `130.25561236` | |
| `TimeInfo.resolution` | `TIMEDEL` | `0.02043359821692` | **Only if meaning/units verified**; otherwise `None` |

Do not convert BKJD to JD or alter original time values. `TIMEUNIT`, `TIMESYS`, `TIMEREF`, `BJDREFI`, `BJDREFF`, and table-column `TUNITn` are not interchangeable; each maps to its own field. Missing time unit/reference/scale/frame → empty string/`None` per model convention, with an info finding.

### 6.5 Metadata not representable by current model
Raw FITS `TTYPE`/`TFORM`/`TDISP`/`NULL` per column, full header card list, aperture image (HDU2), PDC config keywords (`PDCMETHD`, `CDPP*`, etc.), exposure/deadtime values. **Not important enough to require a model change** for 2.2.2; may go in `LightCurveDataset.notes` or remain out of scope. Any model-field addition is a 2.2.1-scope decision requiring approval.

---

## 7. Complete Validation Matrix

Classifications: **Error** = `FITSImportError` raised, no dataset constructed (not placed in a dataset `ValidationReport`, since no dataset exists). **Warning** = import succeeds, finding in `dataset.validation.warnings`, data preserved. **Info** = import succeeds, finding in `dataset.validation.info`, data preserved. **Preserve** = kept as-is, no modification.

| # | Condition | Succeeds? | Finding | Data preserved? | Raises `FITSImportError`? | User approval? |
|---|------|---|---|---|---|---|
| F1 | Missing / unreadable file | No | — | N/A | Yes | No |
| F2 | Corrupted / invalid FITS structure | No | — | N/A | Yes | No |
| F3 | No table HDU with TIME + flux column | No | — | N/A | Yes | No |
| F4 | Multiple candidate tables, no reasonable choice | No | — | N/A | Yes | No |
| F5 | Multiple candidate tables, reasonable choice | Yes | Info (ambiguity) | Yes | No | No |
| C1 | `TIME` column absent | No | — | N/A | Yes | No |
| C2 | Neither `SAP_FLUX` nor `PDCSAP_FLUX` present | No | — | N/A | Yes | No |
| C3 | Only SAP or only PDCSAP available | Yes | Info (single flux series) | Yes | No | No |
| C4 | Flux present, matching `*_FLUX_ERR` absent | Yes | Warning (missing uncertainty) | Yes, `uncertainties=None` | No | No |
| C5 | `*_FLUX_ERR` present but its flux absent | Yes | Warning/info (orphan ignored) | Yes, orphan not imported | No | No |
| C6 | `SAP_QUALITY` / `CADENCENO` absent | Yes | Optional → `None` | Yes | No | No |
| C7 | Extra unsupported numeric columns | Yes | Not imported (possibly info) | Yes | No | No |
| C8 | Unexpected/incompatible dtype (non-numeric where numeric required) | No | — | N/A | Yes | No |
| C9 | Array length ≠ time length | No | — | N/A | Yes (via model `LightCurveValidationError`) | No |
| M1 | Non-numeric timestamp | No | — | N/A | Yes | No |
| M2 | Non-finite timestamp (NaN/inf) | Yes | Warning | Yes, preserved | No | No |
| M3 | Non-finite flux (NaN/inf) | Yes | Warning (`n_nonfinite` + row indices) | Yes, preserved | No | No |
| M4 | Non-finite uncertainty | Yes | Warning | Yes, preserved | No | No |
| M5 | Negative uncertainty | Yes | Warning | Yes, preserved (not replaced) | No | No |
| M6 | Duplicate timestamps | Yes | Warning | Yes, preserved (not reordered) | No | No |
| M7 | Non-monotonic timestamps | Yes | Warning | Yes, preserved (order kept) | No | No |
| Q1 | Nonzero quality flags present | Yes | Info (count + zero-based row indices) | Yes, preserved | No | No |
| Q2 | Quality-bitmask filtering requested | N/A | Not performed in 2.2.2 | — | No | **Yes** (future policy) |
| T1 | Missing time unit | Yes | Info | Yes, `unit=""` | No | No |
| T2 | Missing time reference/scale/frame | Yes | Info | Yes, empty/`None` | No | No |
| T3 | Missing flux unit | Yes | Info | Yes, `unit=""` | No | No |
| E1 | Empty table (zero observations) | No | — | N/A | Yes | No |
| D1 | Duplicate/conflicting supported column names | No | — | N/A | Yes | No |

**Scientific reasoning (§5.1, §5.6):** non-finite and questionable measurements are preserved, never removed/replaced/zero-filled (§5.1.4, §5.6.1 acceptance 3). Quality flags never auto-filtered (§3.4.10; REVIEW-002 justification). File-level failures are exceptions, not `ValidationReport` errors (no dataset exists to attach to — §8.G of prior task, §5.6.7).

---

## 8. Error-Handling Strategy

- Single exception type: `FITSImportError` (subclass of `Exception`), with a meaningful user-facing message and chained underlying cause (`from exc`) for inspectability.
- Success path: return `LightCurveDataset`; warnings/infos live in `dataset.validation`.
- Failure path: raise `FITSImportError`; no partially populated dataset returned.
- `LightCurveValidationError` from model construction is caught and re-raised as `FITSImportError` with context (e.g., "array length mismatch: ..."), preserving the model's structural guarantees while presenting a single importer-level error type to callers.
- Zero-based `row_indices` in every `ValidationFinding` (FITS rows discussed one-based externally are converted to zero-based for the model).
- No GUI error handling; no file-selection dialogs; the caller decides presentation.

---

## 9. Focused 2.2.2 Automated Testing Plan

Tests live in a new test module (e.g., `tests/test_fits_importer.py`) created in Build mode. Fixtures are built under pytest `tmp_path` — **no dependence on the external Kepler dataset or absolute Windows paths**. The portable suite must pass on any machine.

### 9.1 Temporary FITS fixtures
- Valid Kepler-like multi-HDU table (Primary + LIGHTCURVE at index 1 + APERTURE).
- Light-curve table at a different HDU index (e.g., index 2).
- Structural table identification (table found by TIME + flux column, not position).
- Multiple candidate tables (deterministic tie-break + info finding).
- Missing `TIME` column → `FITSImportError`.
- Missing both flux columns → `FITSImportError`.
- Only `SAP_FLUX` (no PDCSAP); only `PDCSAP_FLUX` (no SAP).
- Correct uncertainty pairing (SAP_FLUX↔SAP_FLUX_ERR, PDCSAP_FLUX↔PDCSAP_FLUX_ERR).
- Missing uncertainty column(s) → `uncertainties=None` + warning.
- Missing optional quality/cadence columns → `None`.
- Supported numeric dtypes and endianness (`>f4`, `>f8`, `>i4` → float64/int64).
- Rejection of incompatible string/object types → `FITSImportError`.
- Preservation of NaN/inf in flux and uncertainty.
- Negative uncertainty → warning, preserved.
- Duplicate / non-monotonic timestamps → warning, preserved, not reordered.
- Missing metadata (no time unit, no mission) → info / `None` fields.
- Duplicate or conflicting supported column names → `FITSImportError`.
- Empty table (zero observations) → `FITSImportError`.
- Corrupted / truncated / unreadable file → `FITSImportError`.
- Successful dataset construction and model compatibility (valid `LightCurveDataset`, `to_dict()`/`from_dict()` round-trip).
- Arrays usable after FITS closure (returned arrays independent of open handle).
- Preservation of observation count and original data values.
- Zero-based validation row indices.

### 9.2 Fixture assumptions corrected
- A normal FITS binary table has a shared row structure; columns do **not** have independently mismatched lengths. The removed "mismatched column lengths" fixture is not realistic at the FITS level. Model-level array-alignment testing remains in `tests/test_light_curve.py` (already covered there).
- Do not invent malformed FITS cases merely to increase test count; only include cases constructible realistically.

### 9.3 Resource-safety testing
- Assert returned arrays remain usable after the FITS file has closed.
- Assert returned arrays do not depend on an open FITS file handle (independently owned/copied).
- Assert imported data remains intact after close.

### 9.4 Model-only tests
Stay in `tests/test_light_curve.py`; not duplicated in importer tests.

### 9.5 Baseline
Existing 224 tests must continue to pass with no regressions.

---

## 10. Optional Real-Data Verification

Gated on the actual Kepler file being present at `C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits`. Skipped if absent — never makes the portable suite dependent on it.

Verify:
- HDU identified as LIGHTCURVE (index 1 structurally, not hardcoded).
- 476 rows; TIME range 120.5391–130.2454; unit `d`, scale `TDB`, reference `BJD - 2454833`, frame `SOLARSYSTEM`.
- SAP_FLUX and PDCSAP_FLUX both present and distinct; 4 and 7 non-finite respectively.
- Uncertainties paired correctly; same non-finite rows per column.
- `SAP_QUALITY` 37 nonzero preserved; `CADENCENO` 568–1043 consecutive.
- `DatasetSource.original_file_path`/`original_filename` set; mission/instrument/target_object/source_id correct.
- `name` = filename stem.
- Valid `LightCurveDataset` constructed; `to_dict()`/`from_dict()` round-trip.
- Original file checksum unchanged before/after import (read-only).

---

## 11. Data-Integrity and Resource-Management Approach

- Open read-only (`mode="readonly"`); never open for write.
- All array copies made **inside** the `with fits.open(...)` block before close (memory-mapped data).
- Convert big-endian FITS dtypes to native float64/int64 via `np.array(..., dtype=..., copy=True)`; float32 → float64 is value-preserving.
- Non-finite values preserved (no fill/replace/interpolate).
- Quality flags preserved (no filtering).
- Distinct columns remain distinct (SAP ≠ PDCSAP).
- No observations silently discarded (observation count preserved).
- No units or timestamps silently changed (no BKJD→JD conversion).
- No normalization/detrending/filtering.
- Model's `_copy_arrays` provides a second authoritative safety copy.
- Original FITS file bytes/checksum unchanged; file remains outside repo and unmodified.

---

## 12. Documentation Impact Assessment

Per `AGENTS.md` "Documentation Maintenance During Implementation," documentation updates are a required part of Build-mode work. No documents are modified in this PLAN task.

### 12.1 2.2.2 implementation documentation (to update during Build)
- Record `src/fits_importer.py` module and its responsibilities.
- Record public interface (`import_light_curve`, `FITSImportError`) and error behavior.
- Record supported FITS structure and column/metadata mapping.
- Record validation behavior, classifications, and limitations.
- Record focused test coverage and results.
- Update `docs/MASTER_DEVELOPMENT_ROADMAP.md` (2.2.2 status) and `docs/development/DEVELOPMENT_LOG.md` (implementation record, test results).

### 12.2 2.2.4 consolidation (future)
- Broader documentation reconciliation across subtasks.
- Cross-subtask completion status; overall Stage 2.2 verification.
- Remaining deferred/unresolved items.

Foundation documents remain read-only. `docs/README.md` index unchanged unless a significant document is added/renamed (not the case here). Existing project-lifecycle docs unchanged (behavior unaffected).

---

## 13. Explicit Subtask Boundaries

| Subtask | Responsibility | In 2.2.2? |
|---|---|---|
| 2.2.1 | Light-curve data model (`src/light_curve.py`) — done | No (reused only) |
| 2.2.2 | FITS reading, HDU identification, extraction, metadata, validation, `LightCurveDataset` construction, importer tests | **Yes — current** |
| 2.2.3 | Project association, dataset persistence, save/reopen, project IDs/ownership/permissions | No (future) |
| 2.2.4 | Broader Stage 2.2 verification, documentation reconciliation, completion assessment | No (future) |

**Excluded from 2.2.2:** project association/persistence, visualization, BLS/analysis, quality-bitmask filtering, archive downloads, universal FITS framework, database/permanent storage, GUI dialogs.

---

## 14. Risks and Unresolved Issues

| Risk / Issue | Description | Mitigation / Status |
|---|---|---|
| Memory-mapped FITS arrays | `fits.open` memmaps; post-close access fails if not copied. | Copy arrays inside `with` block (verified design requirement). |
| Big-endian FITS dtypes (`>f4`, `>f8`, `>i4`) | Must convert to native float64/int64. | `np.array(..., dtype=..., copy=True)` handles byte swap; verify on real file. |
| Float32 → float64 upcast | Value-preserving but doubles flux memory. | Acceptable at ~476 rows; document. |
| Model re-copies arrays | Slight redundancy with importer's pre-close copy. | Acceptable; correctness > micro-optimization. |
| `TUNIT1 = "BJD - 2454833"` compound unit | Split into `unit="d"` + `reference`. | Straightforward mapping; no model change. |
| Real dataset not portable | Automated suite must not depend on `C:\Code\...` absolute path. | Gate real-data test on file presence; use `tmp_path` fixtures. |
| Validation vs exception boundary | Risk of putting import failures into a nonexistent dataset's `ValidationReport`. | Enforce separation (Section 8); file-level → exception; scientific → `dataset.validation`. |
| Quality-bitmask pressure | Temptation to auto-filter nonzero flags. | Explicitly excluded; future analysis operation requiring approval. |
| Scope creep | Pressure to add persistence, UI, visualization, BLS. | Explicitly excluded; 2.2.2 is import+validation only. |

**Unresolved:** none currently block planning. The only pending item is user review/approval of this plan before Build mode.

---

## 15. Recommended Build Implementation Sequence

1. Create `src/fits_importer.py`: `FITSImportError`, `import_light_curve()`, FITS opening/close, structural HDU identification.
2. Implement extraction of `TIME`, `SAP_FLUX`/`PDCSAP_FLUX`, uncertainties, `SAP_QUALITY`, `CADENCENO` (array copies inside `with` block).
3. Implement metadata extraction into `DatasetSource` and `TimeInfo` (BKJD/TDB/SOLARSYSTEM; filename-stem naming).
4. Implement validation findings and `ValidationReport`; dataset assembly via `LightCurveDataset` constructor; surface `LightCurveValidationError` as `FITSImportError`.
5. Create focused importer tests with `tmp_path` fixtures (Section 9); run targeted tests.
6. Optional real-data verification against Kepler file, gated on presence (Section 10).
7. Run full suite (224+ passing, no regressions).
8. Update documentation (roadmap, dev log, architecture, test reports) per `AGENTS.md` — Build-mode activity.
9. Review completion; hand off to 2.2.3.

Deferred to 2.2.3: project association, persistence, save/reopen. Deferred to 2.2.4: broader integration verification and documentation reconciliation.

---

## 16. Decisions or Questions Requiring User Approval

- **Approval of this revised plan** before switching to Build mode (the gate itself).
- No new scientific or architectural decisions are identified as blockers for 2.2.2. All recommendations (module path, HDU strategy, simplified exception interface, preservation behavior, dtype policy, naming rule) are within existing authority and follow the approved model and Foundation; they are presented for review but do not require separate approval unless the user wishes to override them.
- If, during Build, a genuine incompatibility with the 2.2.1 model is found that requires a model-field addition, that would be a 2.2.1-scope change requiring explicit approval and would pause this task. None is currently anticipated.

---

## Material Changes from the Previous Plan

1. **Interface simplified:** Removed the `FitsImportResult` dataclass. Success returns a `LightCurveDataset` (warnings/infos in `dataset.validation`); failure raises `FITSImportError`. No separate result type.
2. **Testing schedule corrected:** Importer tests belong in 2.2.2 (not postponed to 2.2.4); 2.2.4 is reserved for broader consolidation.
3. **Source metadata mapping corrected:** `mission`→`MISSION`, `instrument`→`INSTRUME`, `target_object`→`OBJECT`, `source_id`→`KEPLERID` (target ID, distinct from product ID), `archive`→`None` unless independently established, `ORIGIN`→notes/info only (not archive).
4. **Dataset naming defined:** `name` = filename stem; full filename/path in `DatasetSource`; no invented scientific name; empty stem → `FITSImportError`.
5. **FITS fixture assumptions corrected:** Removed unrealistic "independently mismatched column lengths" fixture; model-level alignment testing stays in `test_light_curve.py`; resource safety tested via post-close array usability, not post-close memmap access.
6. **Numeric dtype handling tightened:** Accept supported numeric types, convert to float64/int64 with correct endianness, preserve non-finite, reject incompatible types with `FITSImportError`; no silent string→number or float→int truncation.
7. **Empty tables:** Rejected with `FITSImportError` (distinct from valid non-finite tables).
8. **Multiple candidate tables:** Structural identification retained; deterministic tie-break; ambiguity reported via info/warning; ambiguity does not prevent import when a reasonable choice exists.
9. **Time metadata:** Independent handling of `TIMEUNIT`/`TIMESYS`/`TIMEREF`/`BJDREFI`/`BJDREFF`/`TUNITn`; BKJD not converted to JD; `TIMEDEL`→`resolution` only if verified.
10. **Row indices:** All `ValidationFinding.row_indices` zero-based.
11. **Column-name matching:** Deterministic case-sensitive policy; duplicates/conflicts → `FITSImportError`.
12. **Header inheritance:** Extension-specific values preferred for extension metadata; primary provides mission/instrument/target context; `INHERIT` honored per actual file structure.
13. **Repository state corrected:** HEAD is user commit `113a9ab task 2.2.2 planning begin` (not made by me); working tree has one pre-existing modified file (`WORKING PROGRESS LOG.md`); `OVERVIEW.md` unmodified; no untracked files.

---

## Statement

**Implementation has not started.** No files were created, modified, deleted, or renamed in this session; no dependencies installed; no configuration changed; the original FITS file untouched; no Git state altered by me. This revised plan is presented for review and awaits explicit user authorization before any switch to Build mode.


# chatgpt plan v2 review / prompt

The revised plan is substantially stronger. It is now grounded in the reported current repository state, respects the 2.2.1 model, and keeps the importer separate from persistence and the GUI.

I would not send it to BUILD quite yet. There are a few implementation details that should be clarified first. None require redesigning the plan or changing the 2.2.1 model.

## Review findings



Keep

&#x20;What the plan gets right



- The simplified interface: return `LightCurveDataset` on success and raise `FITSImportError` on failure.
- Keeping SAP and PDCSAP as separate measurements with their own uncertainty columns.
- Preserving non-finite measurements and quality flags rather than silently filtering them.
- Copying FITS arrays before closing the file.
- Keeping automated tests independent of the external Kepler file.
- Running importer tests as part of 2.2.2, rather than postponing them to 2.2.4.
- Updating relevant implementation documentation during BUILD.
- Respecting the existing modified working-progress log and user commit.



Clarify before BUILD

&#x20;1\. FITS column units need an explicit mapping



The plan discusses missing flux units, but it doesn't clearly specify where each measurement's unit comes from.

For FITS table columns, the importer should inspect the corresponding `TUNITn` metadata for each column.

For example:

| FITS column       | Model field                 | Unit source                               |
| ----------------- | --------------------------- | ----------------------------------------- |
| `TIME`            | `TimeInfo.unit`             | `TIMEUNIT`, reconciled with `TUNITn`      |
| `SAP_FLUX`        | `MeasurementColumn.unit`    | Its own `TUNITn`                          |
| `PDCSAP_FLUX`     | `MeasurementColumn.unit`    | Its own `TUNITn`                          |
| `SAP_FLUX_ERR`    | `SAP_FLUX.uncertainties`    | Check compatibility with SAP flux unit    |
| `PDCSAP_FLUX_ERR` | `PDCSAP_FLUX.uncertainties` | Check compatibility with PDCSAP flux unit |

The important point is that the importer should not simply assign `e-/s` because it happens to be the unit in this particular Kepler file.

2\. Header inheritance needs a precise implementation rule

The plan correctly recognizes that the extension declares `INHERIT=True`, but it should distinguish between:

- Reading the primary and extension headers separately.
- Resolving a metadata value using FITS inheritance rules.

The importer must not assume that accessing an extension header through Astropy automatically gives it all inherited primary-header values.

Have Nemotron explicitly plan how it will resolve header values, including which header takes precedence and how conflicting values are reported.

3\. Numeric dtype validation needs to distinguish measurement arrays from integer arrays

The plan says supported numeric types are converted to `float64` or `int64`.

That is reasonable, but the rules should be explicit:

- `TIME`, flux, and uncertainty columns: numeric values convertible to `float64`.
- `SAP_QUALITY`: integer values convertible to `int64` without truncation.
- `CADENCENO`: integer values convertible to `int64` without truncation.

For example, a floating-point quality column should not silently become an integer quality array just because its values happen to be whole numbers.

4\. FITS null-value handling needs investigation

The plan discusses NaN and infinity, but FITS also supports column-specific null conventions.

Nemotron should inspect how Astropy exposes masked or null-valued table columns and determine whether the importer needs to preserve that distinction.

It should not silently convert a FITS null sentinel into an ordinary scientific measurement.

This is an investigation requirement, not a request to invent a complicated null-handling system.

5\. The `TIME` metadata mapping needs one final distinction

The plan correctly separates the time values from their reference convention.

However, it should explicitly verify how `TUNITn`, `TIMEUNIT`, and `BJDREFI`/`BJDREFF` interact before assigning values to `TimeInfo`.

The intended outcome remains:

- Preserve the original `TIME` values.
- Preserve the time unit.
- Preserve the time scale.
- Preserve the reference convention and reference value.
- Do not convert BKJD to JD.

## What I would send Nemotron

I would give it this as a final PLAN refinement. It should amend the existing plan, not start over.

The revised plan is close to approval. Before I authorize BUILD, make one final targeted refinement to the implementation plan.

Do not implement anything, modify files, or change repository state. Remain in PLAN mode.

Please address these five points:

1. **FITS column units**
   - Explicitly define how `TUNITn` is resolved for each supported table column.
   - Map the individual SAP and PDCSAP flux units into their respective `MeasurementColumn.unit` fields.
   - Explain how uncertainty-column units are checked against their corresponding measurement units.
   - Do not hardcode units based on the Kepler example.
   - Preserve unknown units as unknown according to the existing model conventions.
2. **Header inheritance**
   - Clarify exactly how primary and extension headers will be read and resolved.
   - Do not assume Astropy automatically merges inherited primary-header keywords into extension headers.
   - Define extension-versus-primary precedence, including how conflicting values are handled.
   - Preserve the distinction between verified metadata and unknown metadata.
3. **Numeric dtype rules**
   - Define separate conversion rules for floating-point scientific measurements and integer-valued quality/cadence arrays.
   - `TIME`, flux, and uncertainty values may be converted to float64 when numeric.
   - `SAP_QUALITY` and `CADENCENO` must not undergo silent float-to-integer truncation.
   - Reject incompatible types rather than silently coercing them into plausible-looking scientific values.
4. **FITS null-value handling**
   - Investigate how Astropy exposes FITS table null values and masked columns.
   - Determine whether supported columns can contain FITS null representations distinct from ordinary NaN/inf values.
   - Specify how these are preserved or reported without silently treating a null sentinel as a valid measurement.
   - Do not introduce unnecessary model changes. If the current model cannot faithfully represent a relevant case, identify the limitation and pause for my approval rather than inventing a solution.
5. **Time metadata**
   - Explicitly resolve the relationship between `TUNITn`, `TIMEUNIT`, `TIMESYS`, `TIMEREF`, and `BJDREFI`/`BJDREFF`.
   - Keep the original time values unchanged.
   - Do not convert BKJD to JD.
   - Do not conflate the time unit, time reference convention, time scale, and reference frame.

After addressing these points:

- Update the relevant sections of the existing plan.
- Preserve all previously verified repository facts and the existing task boundaries.
- Do not reopen or redesign Subtask 2.2.1.
- Do not introduce project persistence, GUI functionality, visualization, or analysis.
- Identify any remaining genuine unresolved decisions.
- Provide a concise list of what changed in this final refinement.

Return the complete revised implementation plan, not just the changed sections.

Remain in PLAN mode and wait for my approval.

## Overall assessment

Nearly ready

Subtask 2.2.2

I don't see a reason to reopen the data model, change the module architecture, or expand the task scope.

Once those five details are resolved, I expect the plan to be ready for your approval. The next step after that would be a separately authorized BUILD task—not an automatic transition.



# OpenCode Plan v3

I now have verified Astropy null-handling behavior. Let me present the complete revised implementation plan.

---

# Subtask 2.2.2 — FITS Import and Validation: Final Revised Implementation Plan

**Mode: PLAN ONLY. No implementation, file creation, modification, or deletion. No switch to Build mode.**

This report incorporates all required corrections and the five targeted refinements (FITS column units, header inheritance, numeric dtype rules, FITS null-value handling, time metadata). All previously verified repository facts, model interfaces, FITS findings, and task boundaries are preserved.

---

## 1. Repository State and Preparation

### 1.1 Verified repository facts (current, re-checked)

| Item | Verified value |
|---|---|
| Working directory | `C:\Code\New_Project` (git repo, branch `master`) |
| HEAD commit | `113a9ab task 2.2.2 planning begin` — Author: Brett, Date: Wed Nov 4 13:52:42 2026. **Pre-existing user commit; not created by me.** |
| Previous commit | `f65f14f Task 2.2.1` |
| Working tree vs HEAD | **One modified file (not staged):** `docs/planning/.../task 2.2.2 FITS import and validation WORKING PROGRESS LOG.md` (+1,119 insertions beyond the commit). **Pre-existing user edit; left untouched.** |
| Untracked files | None |
| `subtask-2.2-light-curve-import OVERVIEW.md` | Unmodified in working tree (committed in `113a9ab`) |

### 1.2 Correction to prior report on working-tree state
My earlier report described `OVERVIEW.md` as modified and `WORKING PROGRESS LOG.md` as untracked. Current verified state is the opposite (LOG is tracked+modified; OVERVIEW is committed+unmodified). Neither file is touched by this task.

### 1.3 Confirmation that Subtask 2.2.1 exists
**Verified.** `src/light_curve.py` and `tests/test_light_curve.py` both exist (`Test-Path`: both `True`).

### 1.4 Current test baseline (reconfirmed)
`python -m pytest -q` → **224 passed, 0 failed.** No files modified to achieve this. Regression baseline for 2.2.2.

### 1.5 Relevant Foundation requirements (citations)
- **§3.4.1** — preserve units, distinguish measurement types, identify missing/invalid measurements, preserve uncertainties.
- **§3.4.3** — preserve original timestamps/time metadata; do not assume ordinary Julian Date; identify missing/ambiguous time.
- **§3.4.4** — preserve original measurements; derived outputs only as identifiable separate operations (none here).
- **§4.4** — FITS supported (4.4.2); preserve original files/structures (4.4.1); units/time conventions (4.4.7–4.4.8); metadata is part of dataset (4.4.6).
- **§4.5** — user-provided file import (4.5.2); metadata classifications verified/user-supplied/inferred/unknown (4.5.3); never fabricate missing info (4.5.2, 4.5.10); preserve original files unchanged (4.5.2, 4.5.10).
- **§4.7** — preserve original source, filename, mission/instrument/target identifiers; distinguish original from inferred (4.7.1–4.7.4, 4.7.10); `ORIGIN` is not automatically an archive.
- **§5.1** — preserve original data/units/metadata/uncertainty; distinguish missing from measured zero (5.1.4); computational success ≠ scientific validity (5.1.8).
- **§5.6** — initial quality assessment on import (5.6.1); distinguish errors/warnings/info (5.6.1, 5.6.7); never auto-reject useful datasets (5.6.1); zero-based `row_indices` consistent with model.
- **§9.2** — modularity, scientific/UI separation, independent testability, avoid unnecessary dependencies (9.2.1–9.2.7).
- **§9.4** — preserve original imported files; separate original from derived; data integrity (9.4.2, 9.4.6).
- **§10** — AI decision boundaries and user approval (10.4, 10.9).

### 1.6 Existing user changes / repository-state concerns
The two pre-existing planning-file changes are outside `src/` and `tests/` and predate this task. No commits/pushes by me.

---

## 2. Verified 2.2.1 Model Review

All details from direct inspection of `src/light_curve.py` (493 lines) and `tests/test_light_curve.py` (759 lines).

### 2.1 Model components and interfaces

| Component | Fields / behavior (verified) |
|---|---|
| `DatasetSource` | `original_filename`, `original_file_path`, `archive`, `source_id`, `mission`, `instrument`, `target_object`, `checksum` — all `str \| None`, default `None`. |
| `TimeInfo` | `values: np.ndarray` (required); `unit`, `reference`, `time_scale`, `time_reference_frame` (str, default `""`); `reference_value`, `start`, `stop`, `resolution`, `format_hint` (float/str, default `None`). Unknown → `""`/`None`; does not block construction. |
| `MeasurementColumn` | `name: str`, `values: np.ndarray`, `unit: str = ""`, `uncertainties: np.ndarray \| None = None`, `description: str \| None = None`. Property `n_nonfinite`. Non-finite preserved; `None` uncertainties ≠ zero-array uncertainties. |
| `MeasurementSeries` | `series: dict[str, MeasurementColumn]`; keys must equal `column.name`; no duplicates. |
| `ValidationFinding` | `code`, `message`, `severity`, `column: str \| None`, `row_indices: list[int] \| None` (zero-based). |
| `ValidationReport` | `errors`, `warnings`, `info` lists of `ValidationFinding`. |
| `LightCurveDataset` | `dataset_id` (UUID, auto), `name` (str, required), `source`, `time`, `measurements`, `quality_flags: np.ndarray \| None`, `cadence_numbers: np.ndarray \| None`, `validation`, `imported_at` (auto ISO UTC), `notes: str \| None`. Property `n_observations`. |

### 2.2 Structural validation (`__post_init__`)
Raises `LightCurveValidationError` (subclass of `ValueError`) for: invalid `dataset_id`; missing/non-ndarray `time.values`; non-str `time.unit`; non-`MeasurementSeries` measurements; key/name mismatch; duplicate names; non-ndarray column values/unit/uncertainties; any array length mismatch with time (values, non-None uncertainties, quality_flags, cadence_numbers); non-`ValidationReport` validation; non-str `imported_at`.

### 2.3 Array copying and ownership
`_copy_arrays` converts `time.values` and each measurement `values`/`uncertainties` to `np.array(..., dtype=np.float64, copy=True)`; `quality_flags`/`cadence_numbers` to `np.array(..., dtype=np.int64, copy=True)`. Model always owns independent copies. Importer must still copy FITS memory-mapped arrays **before** closing the file.

### 2.4 Serialization
`to_dict()` → JSON-compatible dict; arrays → `.tolist()`; `None` preserved as `None`. `from_dict(data)` reconstructs and re-validates; distinguishes `None` from arrays.

### 2.5 Compatibility with Kepler FITS dataset
**Compatible — no model change required.** Mapping in Section 6. Non-finite flux preserved; 37 nonzero quality flags preserved (no filtering); BKJD/TDB/SOLARSYSTEM in separate `TimeInfo` fields; float32→float64 upcast value-preserving; big-endian dtypes converted by `np.array(..., dtype=..., copy=True)`.

### 2.6 Genuine gaps / incompatibilities (flagged in Section 11)
None requiring a model change for 2.2.2 **except** the FITS integer null-sentinel limitation described in Section 4.4, which is flagged for approval. Raw FITS `TTYPE`/`TFORM`/`NULL` per column, full header card list, aperture image (HDU2), PDC config keywords not represented; may go in `LightCurveDataset.notes` or remain out of scope.

---

## 3. Confirmed FITS Inspection Findings

Verified against `C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits` (read-only, outside repo, unchanged) using Astropy 7.2.0.

### 3.1 HDU structure
| HDU | Type | EXTNAME | Rows/Cols | Notes |
|---|---|---|---|---|
| 0 | `PrimaryHDU` | `PRIMARY` | — | 58 cards |
| 1 | `BinTableHDU` | `LIGHTCURVE` | 476 × 20 | Light-curve table |
| 2 | `ImageHDU` | `APERTURE` | 12 × 10 | Aperture mask |

`NEXTEND=2` matches two extensions. Table at index 1 **but importer must not hardcode index 1** — structural identification (Section 5).

### 3.2 LIGHTCURVE columns (verified)
| # | Column | Format | dtype (stored) | Unit (TUNIT) | 2.2.2 role |
|---|---|---|---|---|---|
| 1 | `TIME` | D | `>f8` | `BJD - 2454833` | **Required** (time) |
| 2 | `TIMECORR` | E | `>f4` | `d` | Unsupported |
| 3 | `CADENCENO` | J | `>i4` | — | **Optional** (cadence) |
| 4 | `SAP_FLUX` | E | `>f4` | `e-/s` | **Required flux** (≥1 of SAP/PDCSAP) |
| 5 | `SAP_FLUX_ERR` | E | `>f4` | `e-/s` | **Optional** uncertainty for SAP_FLUX |
| 6 | `SAP_BKG` | E | `>f4` | `e-/s` | Unsupported |
| 7 | `SAP_BKG_ERR` | E | `>f4` | `e-/s` | Unsupported |
| 8 | `PDCSAP_FLUX` | E | `>f4` | `e-/s` | **Required flux** (≥1 of SAP/PDCSAP) |
| 9 | `PDCSAP_FLUX_ERR` | E | `>f4` | `e-/s` | **Optional** uncertainty for PDCSAP_FLUX |
| 10 | `SAP_QUALITY` | J | `>i4` | — | **Optional** quality flags |
| 11–20 | centroid/position (+ errors) | D/E | mixed | pixel/pixels | Unsupported |

### 3.3 Data values (verified)
| Column | Non-finite | Min | Max | Notes |
|---|---|---|---|---|
| `TIME` | 0 | 120.53914651 | 130.24539528 | All finite |
| `CADENCENO` | N/A (int) | 568 | 1043 | Consecutive |
| `SAP_FLUX` | 4 (NaN) | 532355.0 | 532944.06 | Preserved as-is |
| `SAP_FLUX_ERR` | 4 (NaN) | ~20.04 | ~20.05 | Same 4 rows as SAP_FLUX |
| `PDCSAP_FLUX` | 7 (NaN) | 501346.12 | 501746.75 | Preserved as-is |
| `PDCSAP_FLUX_ERR` | 7 (NaN) | ~20.57 | ~20.77 | Same 7 rows as PDCSAP_FLUX |
| `SAP_QUALITY` | N/A (int) | — | — | 37 nonzero; `{64, 128, 8192, 8320, 12352, 32800}` |
| `PSF_CENTR1` | 476 (all NaN) | — | — | Unsupported column |

No TNULL null sentinels present in this file; missing float values are NaN. Confirmed via read-only inspection.

### 3.4 Header metadata (verified)
**Primary:** `TELESCOP=Kepler`, `INSTRUME=Kepler Photometer`, `OBJECT=KIC 11904151`, `KEPLERID=11904151`, `ORIGIN=NASA/Ames`, `MISSION=Kepler`, `QUARTER=0`, `OBSMODE=long cadence`, `DATE=2015-08-26`.

**LIGHTCURVE extension (`INHERIT=True`):** `TIMEREF=SOLARSYSTEM`, `TASSIGN=SPACECRAFT`, `TIMESYS=TDB`, `BJDREFI=2454833`, `BJDREFF=0.0`, `TIMEUNIT=d`, `TSTART=120.52892942`, `TSTOP=130.25561236`, `TIMEDEL=0.02043359821692`, `EXPOSURE=8.95472397`, `DATE-OBS`, `DATE-END`, PDC keywords.

### 3.5 Time convention (verified)
Values are `BJD − 2454833` (BKJD-style), days (`TIMEUNIT=d`), time system `TDB`, reference frame `SOLARSYSTEM`, `BJDREFI=2454833`, `BJDREFF=0`. **Not ordinary Julian Date.** No conversion.

---

## 4. Proposed Importer Module and Public Interface

### 4.1 Module path
`src/fits_importer.py` — new module alongside `src/light_curve.py`. Single module initially.

### 4.2 Dependencies
`astropy.io.fits` (approved, DEC-006), `numpy` (approved), `src.light_curve` (reused model). Standard library only otherwise. **No new dependencies.** No PySide6, no project/service/repository imports.

### 4.3 Simplified public interface
**Successful import:** return a constructed `LightCurveDataset`. Non-fatal validation findings stored in `dataset.validation` (warnings/info). **No separate result dataclass.**

**Failed import:** raise `FITSImportError` with meaningful explanation. No partially populated dataset returned.

```python
class FITSImportError(Exception):
    """Raised when a file-level condition prevents FITS light-curve import."""

def import_light_curve(file_path: str | os.PathLike[str]) -> LightCurveDataset:
    """Read a FITS light-curve file and return a LightCurveDataset.

    Raises FITSImportError for file access, FITS parsing, missing/unsuitable
    table structure, missing required columns, incompatible data types, empty
    tables, or model-construction failures. Non-fatal scientific conditions are
    reported via the returned dataset's ValidationReport.
    """
```

### 4.4 Failure categories distinguished
1. File access failures (missing, unreadable, permission).
2. FITS parsing failures (corrupted, invalid structure).
3. Missing/unusable light-curve structure (no table with TIME + flux column).
4. Missing required columns (`TIME`, or neither `SAP_FLUX` nor `PDCSAP_FLUX`).
5. Incompatible data types (non-numeric where numeric required).
6. Structural model-construction failures (`LightCurveValidationError` re-raised as `FITSImportError` with context).

### 4.5 Exception context
Exceptions chain the underlying cause (`raise FITSImportError(...) from exc`) so `__cause__` is inspectable; user-facing message meaningful without leaking implementation details. No GUI error handling.

---

## 5. FITS Column Units (Refinement 1)

### 5.1 How `TUNITn` is resolved per supported column
Each supported table column's unit is read independently from its own `TUNITn` keyword (e.g., `TUNIT4` for `SAP_FLUX`, `TUNIT8` for `PDCSAP_FLUX`). The importer reads the unit string directly from the column's FITS definition — **not** from a global default, not hardcoded, not inferred from neighboring columns.

### 5.2 Mapping SAP and PDCSAP flux units into `MeasurementColumn.unit`
- `SAP_FLUX.unit` ← value of `TUNIT4` (e.g. `"e-/s"`), or `""` if `TUNIT4` is absent/empty/Unknown.
- `PDCSAP_FLUX.unit` ← value of `TUNIT8` (e.g. `"e-/s"`), or `""` if absent/empty/Unknown.
- Each column retains its **own** unit string. SAP and PDCSAP units are stored separately and are **not** assumed equal even though both happen to be `"e-/s"` in the Kepler file.

### 5.3 Uncertainty-column unit cross-check
- `SAP_FLUX.uncertainties` unit ← `TUNIT5` (for `SAP_FLUX_ERR`).
- `PDCSAP_FLUX.uncertainties` unit ← `TUNIT9` (for `PDCSAP_FLUX_ERR`).
- **Check:** the importer compares each uncertainty column's `TUNITn` against its corresponding flux column's `TUNITn`. If they differ, an informational finding is attached (units differ between measurement and its uncertainty), but the values are preserved as-is — no conversion, no rejection. If an uncertainty column's `TUNITn` is absent/empty, the uncertainty `MeasurementColumn.unit` is `""` (unknown per model convention).

### 5.4 No hardcoding; unknown units preserved
Units are never hardcoded based on the Kepler example. Any `TUNITn` that is absent, blank, or unrecognized → empty string `""` in the model, consistent with `TimeInfo.unit` / `MeasurementColumn.unit` convention for unknown units. An info finding may note the unknown unit.

### 5.5 Time unit
`TimeInfo.unit` ← `TIMEUNIT` (extension) or table `TUNIT1` for `TIME`, resolved per Section 8. Default `""` if unknown.

---

## 6. Header Inheritance and Resolution (Refinement 2)

### 6.1 Explicit read; no assumption of Astropy auto-merge
The importer reads **both** the primary header (`hdul[0].header`) and the extension header (`hdul[1].header`) explicitly. It does **not** assume Astropy automatically merges inherited primary-header keywords into the extension header, even when `INHERIT=True` is present. `INHERIT` is a FITS convention hint, not a guarantee of in-memory merging by the reader.

### 6.2 Resolution precedence
| Metadata class | Preferred source | Fallback | Notes |
|---|---|---|---|
| Extension-specific time (`TIMESYS`, `TIMEREF`, `BJDREFI`, `BJDREFF`, `TIMEUNIT`, `TSTART`/`TSTOP`) | Extension header | Primary header (only if extension lacks it) | Extension-specific values take precedence |
| Mission/instrument/target/source | Primary header | Extension header (only if primary lacks it) | Primary provides source context |
| Column units (`TUNITn`) | Extension header (table column defs) | — | Per-column, from `hdul[1].columns` |

### 6.3 Conflicting values
If primary and extension declare conflicting values for the same metadata class (e.g., different `TIMESYS`), the **extension-specific value is used** for extension-specific metadata; the conflict is noted in `dataset.validation.info` or `dataset.notes` so the distinction is visible, not silently resolved. Primary and extension values are never merged into a single ambiguous field.

### 6.4 Verified vs unknown metadata
Metadata present and readable → stored as verified. Metadata absent, blank, or unreadable → field left unknown (`""`/`None`) per model convention; never fabricated. An info finding records what is missing.

---

## 7. HDU Identification (structural, not fixed index)

1. Open `fits.open(path, mode="readonly")` inside a `with` block (guaranteed close on success and failure).
2. Iterate all HDUs; candidates = table HDUs (`BinTableHDU`/`TableHDU`) whose column names include `TIME` and at least one of `SAP_FLUX` / `PDCSAP_FLUX`.
3. Prefer candidate whose `EXTNAME == "LIGHTCURVE"` (Kepler convention) if present.
4. If multiple structural candidates remain, deterministic tie-break (first in HDU order) + informational finding about ambiguity. Ambiguity does **not** prevent import when a reasonable choice exists; prevents import only if no candidate satisfies the structural rule.
5. No candidate → `FITSImportError`.
All array copies made **inside** the `with` block before close (memory-mapped data).

---

## 8. Time Metadata (Refinement 5)

### 8.1 Independent resolution of each concept
| Model field | Source keyword(s) | Meaning | Verified Kepler value |
|---|---|---|---|
| `TimeInfo.unit` | `TIMEUNIT`, or table `TUNIT1` | Unit of the numeric time values | `"d"` (days) |
| `TimeInfo.reference` | Table `TUNIT1` / convention | Time reference/convention (e.g. "BJD - 2454833") | `"BJD - 2454833 (BKJD)"` |
| `TimeInfo.time_scale` | `TIMESYS` | Time scale | `"TDB"` |
| `TimeInfo.time_reference_frame` | `TIMEREF` | Reference frame | `"SOLARSYSTEM"` |
| `TimeInfo.reference_value` | `BJDREFI` (+ `BJDREFF`) | Numeric reference offset | `2454833.0` |
| `TimeInfo.start` | `TSTART` | Observation start | `120.52892942` |
| `TimeInfo.stop` | `TSTOP` | Observation stop | `130.25561236` |
| `TimeInfo.resolution` | `TIMEDEL` | Time resolution | `0.02043359821692` **only if meaning/units verified**, else `None` |

### 8.2 Relationship between keywords
- `TUNIT1` (table column unit for `TIME`) describes the unit of the values stored in the `TIME` column.
- `TIMEUNIT` (header keyword) describes the time unit for `TIME`, `TSTART`, `TSTOP` — should agree with `TUNIT1`; if they disagree, extension/header value used for `TimeInfo.unit` and the discrepancy noted.
- `TIMESYS` = time scale (TDB). `TIMEREF` = reference frame (SOLARSYSTEM). `BJDREFI`/`BJDREFF` = numeric reference offset establishing what `BJD − 2454833` means.
- These are **not interchangeable**. Each maps to its own `TimeInfo` field.

### 8.3 Preservation rules
- Original time values copied unchanged (float64), **no BKJD→JD conversion**, no relabeling as JD, no timestamp modification.
- Missing time unit/reference/scale/frame → `""`/`None` per model convention + info finding.

---

## 9. Numeric Dtype Rules (Refinement 3)

### 9.1 Separate conversion rules

| Array group | Columns | Stored FITS dtype | Conversion rule | Model dtype |
|---|---|---|---|---|
| Floating-point scientific measurements | `TIME`, `SAP_FLUX`, `PDCSAP_FLUX`, `SAP_FLUX_ERR`, `PDCSAP_FLUX_ERR` | `>f8`, `>f4` (big-endian float) | Convert to `np.float64` via `np.array(..., dtype=np.float64, copy=True)`. Endianness handled by NumPy. Non-finite (NaN/inf) preserved. | `float64` |
| Integer-valued identifiers/flags | `CADENCENO`, `SAP_QUALITY` | `>i4` (big-endian int32) | Convert to `np.int64` via `np.array(..., dtype=np.int64, copy=True)`. **No float-to-integer truncation** — these columns are read as integers directly; they are never passed through a float conversion. | `int64` |

### 9.2 No silent coercion
- Incompatible types (e.g., string/object column where a numeric measurement is expected) → `FITSImportError` with meaningful reason. Not silently parsed as numbers.
- Float columns are never silently truncated to integers; integer columns are never silently converted to floats.
- No universal type-conversion framework. Only the specific supported columns above are accepted; everything else is unsupported (not imported, possibly noted in `notes`).

---

## 10. FITS Null-Value Handling (Refinement 4)

### 10.1 How Astropy exposes null values (verified by read-only test)
- **Float columns** (`D`/`E` formats): Astropy **does not permit** a `TNULL` null sentinel on binary-table float columns (verified: `fits.Column` rejects `null` for type `E`). Missing float values are represented as ordinary `NaN`. The Kepler file's missing SAP_FLUX/PDCSAP_FLUX values are NaN (verified: 4 and 7 NaN respectively).
- **Integer columns** (`J` format): Astropy permits `TNULL` (exposed via `Column.null`). When read via `hdul[1].data` (FITS record array), the raw sentinel integer is preserved as-is (e.g. `-999`), **not** masked. When read via `Table.read()`, the column becomes a masked array with a per-row mask.

### 10.2 Supported columns and null representations
| Column | Format | Null mechanism in this file | How importer handles |
|---|---|---|---|
| `TIME`, `SAP_FLUX`, `PDCSAP_FLUX`, `SAP_FLUX_ERR`, `PDCSAP_FLUX_ERR` | float (`D`/`E`) | NaN (no TNULL permitted) | NaN preserved as non-finite; counted/reported via `n_nonfinite` + warning with zero-based row indices |
| `SAP_QUALITY`, `CADENCENO` | int (`J`) | None present in this file (plain ints) | If a `TNULL` sentinel were present, raw sentinel value would be read as a plain integer — **risk of misinterpretation** |

### 10.3 Preservation / reporting policy
- Float NaN/inf: preserved, never replaced with zero or sentinel; reported as warning with zero-based `row_indices`.
- Integer `TNULL` sentinel (if ever present): the importer checks `Column.null` for each supported integer column. If a null sentinel is defined, rows equal to the sentinel are treated as missing/unknown — **but the current model has no per-row "missing" representation for `quality_flags`/`cadence_numbers`** (they are plain `np.ndarray | None`, with `None` meaning the whole column absent, not per-row missing).

### 10.4 Genuine model limitation — flagged for approval
The existing `LightCurveDataset` model cannot faithfully represent per-row missingness for integer columns (`quality_flags`, `cadence_numbers`) — there is no masked-array or per-row-null field. If a FITS file contains `TNULL` sentinels in `SAP_QUALITY` or `CADENCENO`, the importer must either:
(a) preserve the raw sentinel as an integer (misrepresenting missing as a value), or
(b) reject with `FITSImportError`, or
(c) require a model change.

**This is a genuine unresolved decision.** The Kepler file has no TNULL sentinels, so it does not block the initial implementation. I flag this limitation and pause for your approval rather than inventing a solution. No model change is introduced in this plan.

---

## 11. Complete Validation Matrix

Classifications: **Error** = `FITSImportError` raised, no dataset constructed (not placed in a dataset `ValidationReport`, since no dataset exists). **Warning** = import succeeds, finding in `dataset.validation.warnings`, data preserved. **Info** = import succeeds, finding in `dataset.validation.info`, data preserved. **Preserve** = kept as-is, no modification.

| # | Condition | Succeeds? | Finding | Data preserved? | Raises `FITSImportError`? | User approval? |
|---|------|---|---|---|---|---|
| F1 | Missing / unreadable file | No | — | N/A | Yes | No |
| F2 | Corrupted / invalid FITS structure | No | — | N/A | Yes | No |
| F3 | No table HDU with TIME + flux column | No | — | N/A | Yes | No |
| F4 | Multiple candidate tables, no reasonable choice | No | — | N/A | Yes | No |
| F5 | Multiple candidate tables, reasonable choice | Yes | Info (ambiguity) | Yes | No | No |
| C1 | `TIME` column absent | No | — | N/A | Yes | No |
| C2 | Neither `SAP_FLUX` nor `PDCSAP_FLUX` present | No | — | N/A | Yes | No |
| C3 | Only SAP or only PDCSAP available | Yes | Info (single flux series) | Yes | No | No |
| C4 | Flux present, matching `*_FLUX_ERR` absent | Yes | Warning (missing uncertainty) | Yes, `uncertainties=None` | No | No |
| C5 | `*_FLUX_ERR` present but its flux absent | Yes | Warning/info (orphan ignored) | Yes, orphan not imported | No | No |
| C6 | `SAP_QUALITY` / `CADENCENO` absent | Yes | Optional → `None` | Yes | No | No |
| C7 | Extra unsupported numeric columns | Yes | Not imported (possibly info) | Yes | No | No |
| C8 | Unexpected/incompatible dtype (non-numeric where numeric required) | No | — | N/A | Yes | No |
| C9 | Array length ≠ time length | No | — | N/A | Yes (via model `LightCurveValidationError`) | No |
| M1 | Non-numeric timestamp | No | — | N/A | Yes | No |
| M2 | Non-finite timestamp (NaN/inf) | Yes | Warning | Yes, preserved | No | No |
| M3 | Non-finite flux (NaN/inf) | Yes | Warning (`n_nonfinite` + zero-based row indices) | Yes, preserved | No | No |
| M4 | Non-finite uncertainty | Yes | Warning | Yes, preserved | No | No |
| M5 | Negative uncertainty | Yes | Warning | Yes, preserved (not replaced) | No | No |
| M6 | Duplicate timestamps | Yes | Warning | Yes, preserved (not reordered) | No | No |
| M7 | Non-monotonic timestamps | Yes | Warning | Yes, preserved (order kept) | No | No |
| Q1 | Nonzero quality flags present | Yes | Info (count + zero-based row indices) | Yes, preserved | No | No |
| Q2 | Quality-bitmask filtering requested | N/A | Not performed in 2.2.2 | — | No | **Yes** (future policy) |
| T1 | Missing time unit | Yes | Info | Yes, `unit=""` | No | No |
| T2 | Missing time reference/scale/frame | Yes | Info | Yes, empty/`None` | No | No |
| T3 | Missing flux unit | Yes | Info | Yes, `unit=""` | No | No |
| E1 | Empty table (zero observations) | No | — | N/A | Yes | No |
| D1 | Duplicate/conflicting supported column names | No | — | N/A | Yes | No |
| N1 | Integer `TNULL` sentinel in `SAP_QUALITY`/`CADENCENO` | See below | — | Limitation flagged | **Decision required** | **Yes** |

**Scientific reasoning (§5.1, §5.6):** non-finite and questionable measurements preserved, never removed/replaced/zero-filled (§5.1.4, §5.6.1 acceptance 3). Quality flags never auto-filtered (§3.4.10; REVIEW-002 justification). File-level failures are exceptions, not `ValidationReport` errors (no dataset exists to attach to — §8.G of prior task, §5.6.7).

**N1 note:** The Kepler file has no TNULL sentinels, so this does not block initial implementation. If encountered, a decision is required (preserve sentinel as value / reject / model change). Flagged for approval.

---

## 12. Error-Handling Strategy

- Single exception type: `FITSImportError` (subclass of `Exception`), meaningful user-facing message, chained underlying cause (`from exc`).
- Success path: return `LightCurveDataset`; warnings/infos live in `dataset.validation`.
- Failure path: raise `FITSImportError`; no partially populated dataset returned.
- `LightCurveValidationError` from model construction caught and re-raised as `FITSImportError` with context.
- Zero-based `row_indices` in every `ValidationFinding`.
- No GUI error handling; no file-selection dialogs; caller decides presentation.

---

## 13. Measurement and Metadata Mapping

### 13.1 Required / optional / unsupported table columns

| FITS column | Role | Required for construction? | Model target | Absent behavior |
|---|---|---|---|---|
| `TIME` | timestamps | **Yes** | `TimeInfo.values` (+ metadata) | `FITSImportError` |
| `SAP_FLUX` | SAP flux | At least one of SAP/PDCSAP | `MeasurementColumn("SAP_FLUX")` | — |
| `PDCSAP_FLUX` | PDC flux | At least one of SAP/PDCSAP | `MeasurementColumn("PDCSAP_FLUX")` | — |
| `SAP_FLUX_ERR` | SAP uncertainty | Optional | `SAP_FLUX.uncertainties` | `None`, warning |
| `PDCSAP_FLUX_ERR` | PDC uncertainty | Optional | `PDCSAP_FLUX.uncertainties` | `None`, warning |
| `SAP_QUALITY` | quality flags | Optional | `quality_flags` (int64) | `None` |
| `CADENCENO` | cadence ids | Optional | `cadence_numbers` (int64) | `None` |
| Other columns | — | No | Not imported | possibly noted in `notes` |

SAP and PDCSAP remain independent columns, each paired with its own `*_FLUX_ERR`. Never merged. Never one silently discarded.

### 13.2 Source metadata mapping

| `DatasetSource` field | Proposed source | Notes |
|---|---|---|
| `mission` | `MISSION` header | Leave `None` if absent |
| `instrument` | `INSTRUME` header | Leave `None` if absent |
| `target_object` | `OBJECT` header | Leave `None` if absent |
| `source_id` | `KEPLERID` (target ID) | Distinct from product/file ID; `None` if absent |
| `archive` | `None` | **Not** `ORIGIN` unless supplying archive independently established |
| `original_filename` | Actual input filename | |
| `original_file_path` | Actual input path | |

`ORIGIN=NASA/Ames` may be retained in `notes` or an informational finding, but **must not** automatically be described as the archive. Do not invent source metadata; absent/ambiguous → field unknown.

### 13.3 Dataset naming
- `LightCurveDataset.name` = input filename stem (e.g. `kplr011904151-2009131105131_llc_full`).
- Full original filename in `DatasetSource.original_filename`; full path in `original_file_path`.
- Do not invent a target name or scientific label when the filename is the only reliable identifier.
- Empty/unusable stem → `FITSImportError` rather than silently inventing a name.

### 13.4 Metadata not representable by current model
Raw FITS `TTYPE`/`TFORM`/`TDISP`/`NULL` per column, full header card list, aperture image (HDU2), PDC config keywords. Not important enough to require a model change for 2.2.2; may go in `LightCurveDataset.notes` or remain out of scope. Any model-field addition is a 2.2.1-scope decision requiring approval.

---

## 14. Data-Integrity and Resource-Management Approach

- Open read-only (`mode="readonly"`); never open for write.
- All array copies made **inside** the `with fits.open(...)` block before close.
- Convert big-endian FITS dtypes to native float64/int64 via `np.array(..., dtype=..., copy=True)`; float32→float64 value-preserving.
- Non-finite values preserved (no fill/replace/interpolate).
- Quality flags preserved (no filtering).
- Distinct columns remain distinct (SAP ≠ PDCSAP).
- No observations silently discarded (observation count preserved).
- No units or timestamps silently changed (no BKJD→JD conversion).
- No normalization/detrending/filtering.
- Model's `_copy_arrays` provides a second authoritative safety copy.
- Original FITS file bytes/checksum unchanged; file remains outside repo and unmodified.

---

## 15. Focused 2.2.2 Automated Testing Plan

Tests in a new module (e.g., `tests/test_fits_importer.py`), fixtures under pytest `tmp_path` — **no dependence on external Kepler dataset or absolute Windows paths.** Portable suite passes on any machine.

### 13.1 Temporary FITS fixtures
- Valid Kepler-like multi-HDU table (Primary + LIGHTCURVE at index 1 + APERTURE).
- Light-curve table at a different HDU index.
- Structural table identification (by TIME + flux column, not position).
- Multiple candidate tables (deterministic tie-break + info finding).
- Missing `TIME` column → `FITSImportError`; missing both flux columns → `FITSImportError`.
- Only `SAP_FLUX`; only `PDCSAP_FLUX`.
- Correct uncertainty pairing (SAP↔SAP_ERR, PDCSAP↔PDCSAP_ERR).
- Missing uncertainty column(s) → `uncertainties=None` + warning.
- Missing optional quality/cadence columns → `None`.
- Supported numeric dtypes and endianness (`>f4`, `>f8`, `>i4` → float64/int64).
- Rejection of incompatible string/object types → `FITSImportError`.
- Preservation of NaN/inf in flux and uncertainty.
- Negative uncertainty → warning, preserved.
- Duplicate / non-monotonic timestamps → warning, preserved, not reordered.
- Missing metadata (no time unit, no mission) → info / `None` fields.
- Duplicate/conflicting supported column names → `FITSImportError`.
- Empty table (zero observations) → `FITSImportError`.
- Corrupted / truncated / unreadable file → `FITSImportError`.
- Successful dataset construction and model compatibility (`to_dict()`/`from_dict()` round-trip).
- Arrays usable after FITS closure (independent of open handle).
- Preservation of observation count and original data values.
- Zero-based validation row indices.

### 13.2 Fixture assumptions corrected
- A normal FITS binary table has a shared row structure; columns do **not** have independently mismatched lengths. The removed "mismatched column lengths" fixture is not realistic at the FITS level. Model-level array-alignment testing remains in `tests/test_light_curve.py` (already covered there).
- Do not invent malformed FITS cases merely to increase test count.

### 13.3 Resource-safety testing
- Assert returned arrays remain usable after the FITS file has closed.
- Assert returned arrays do not depend on an open FITS file handle.
- Assert imported data remains intact after close.

### 13.4 Model-only tests
Stay in `tests/test_light_curve.py`; not duplicated in importer tests.

### 13.5 Baseline
Existing 224 tests must continue to pass with no regressions.

---

## 16. Optional Real-Data Verification

Gated on the actual Kepler file being present. Skipped if absent — never makes the portable suite dependent on it.

Verify:
- HDU identified as LIGHTCURVE (index 1 structurally, not hardcoded).
- 476 rows; TIME range 120.5391–130.2454; unit `d`, scale `TDB`, reference `BJD - 2454833`, frame `SOLARSYSTEM`.
- SAP_FLUX and PDCSAP_FLUX both present and distinct; 4 and 7 non-finite respectively.
- Uncertainties paired correctly; same non-finite rows per column.
- `SAP_QUALITY` 37 nonzero preserved; `CADENCENO` 568–1043 consecutive.
- `DatasetSource.original_file_path`/`original_filename` set; mission/instrument/target_object/source_id correct.
- `name` = filename stem.
- Valid `LightCurveDataset` constructed; `to_dict()`/`from_dict()` round-trip.
- Original file checksum unchanged before/after import.

---

## 17. Documentation Impact Assessment

Per `AGENTS.md`, documentation updates are required during Build mode. No documents modified now.

### 17.1 2.2.2 implementation documentation (to update during Build)
- Record `src/fits_importer.py` module and responsibilities.
- Record public interface (`import_light_curve`, `FITSImportError`) and error behavior.
- Record supported FITS structure and column/metadata mapping (including units, time metadata, null handling).
- Record validation behavior, classifications, and limitations (including the integer `TNULL` model limitation flagged in Section 10.4).
- Record focused test coverage and results.
- Update `docs/MASTER_DEVELOPMENT_ROADMAP.md` (2.2.2 status) and `docs/development/DEVELOPMENT_LOG.md` (implementation record, test results).

### 17.2 2.2.4 consolidation (future)
- Broader documentation reconciliation across subtasks; cross-subtask completion status; overall Stage 2.2 verification; remaining deferred/unresolved items.

Foundation documents remain read-only. `docs/README.md` unchanged unless a significant document is added/renamed. Existing project-lifecycle docs unchanged.

---

## 18. Explicit Subtask Boundaries

| Subtask | Responsibility | In 2.2.2? |
|---|---|---|
| 2.2.1 | Light-curve data model — done | No (reused only) |
| 2.2.2 | FITS reading, HDU identification, extraction, metadata, validation, `LightCurveDataset` construction, importer tests | **Yes — current** |
| 2.2.3 | Project association, dataset persistence, save/reopen, project IDs/ownership/permissions | No (future) |
| 2.2.4 | Broader Stage 2.2 verification, documentation reconciliation, completion assessment | No (future) |

**Excluded from 2.2.2:** project association/persistence, visualization, BLS/analysis, quality-bitmask filtering, archive downloads, universal FITS framework, database/permanent storage, GUI dialogs.

---

## 19. Risks and Unresolved Issues

| Risk / Issue | Description | Mitigation / Status |
|---|---|---|
| Memory-mapped FITS arrays | Post-close access fails if not copied. | Copy arrays inside `with` block. |
| Big-endian FITS dtypes | Convert to native float64/int64. | `np.array(..., dtype=..., copy=True)` handles byte swap. |
| Float32 → float64 upcast | Value-preserving, doubles flux memory. | Acceptable at ~476 rows. |
| Model re-copies arrays | Slight redundancy. | Acceptable; correctness > micro-optimization. |
| Real dataset not portable | Automated suite must not depend on absolute path. | Gate real-data test on file presence; `tmp_path` fixtures. |
| Validation vs exception boundary | Risk of putting import failures into nonexistent dataset's `ValidationReport`. | Enforce separation (Section 12). |
| Quality-bitmask pressure | Temptation to auto-filter nonzero flags. | Explicitly excluded; future analysis operation requiring approval. |
| Scope creep | Pressure to add persistence, UI, visualization, BLS. | Explicitly excluded. |
| Integer `TNULL` sentinel (N1) | Model cannot represent per-row missingness for `quality_flags`/`cadence_numbers`. | **Unresolved — flagged for approval** (Section 10.4). Kepler file has no TNULL, so does not block initial implementation. |

**Unresolved decision:** N1 — how to handle `TNULL` null sentinels in integer quality/cadence columns given the model's lack of per-row missing representation. Requires your approval before implementation if such a file is encountered.

---

## 20. Recommended Build Implementation Sequence

1. Create `src/fits_importer.py`: `FITSImportError`, `import_light_curve()`, FITS opening/close, structural HDU identification.
2. Implement extraction of `TIME`, `SAP_FLUX`/`PDCSAP_FLUX`, uncertainties, `SAP_QUALITY`, `CADENCENO` (array copies inside `with` block; per-column units from `TUNITn`).
3. Implement metadata extraction into `DatasetSource` and `TimeInfo` (BKJD/TDB/SOLARSYSTEM; explicit primary/extension header resolution; filename-stem naming).
4. Implement validation findings and `ValidationReport`; dataset assembly via `LightCurveDataset` constructor; surface `LightCurveValidationError` as `FITSImportError`.
5. Create focused importer tests with `tmp_path` fixtures (Section 15); run targeted tests.
6. Optional real-data verification against Kepler file, gated on presence (Section 16).
7. Run full suite (224+ passing, no regressions).
8. Update documentation per `AGENTS.md` — Build-mode activity (Section 17).
9. Review completion; hand off to 2.2.3.

Deferred to 2.2.3: project association, persistence, save/reopen. Deferred to 2.2.4: broader integration verification and documentation reconciliation.

---

## 21. Decisions or Questions Requiring User Approval

1. **Approval of this revised plan** before switching to Build mode (the gate itself).
2. **N1 — Integer `TNULL` sentinel handling:** If a FITS file contains `TNULL` null sentinels in `SAP_QUALITY` or `CADENCENO`, the model cannot represent per-row missingness. Options: preserve sentinel as integer value / reject with `FITSImportError` / model change. Requires your approval. (Not encountered in the Kepler file; does not block initial implementation.)
3. No new scientific or architectural decisions are identified as blockers for 2.2.2. All other recommendations follow the approved model and Foundation and are within existing authority.

---

## Concise List of Changes in This Final Refinement

1. **FITS column units:** Per-column `TUNITn` resolution defined; SAP/PDCSAP flux units mapped to respective `MeasurementColumn.unit`; uncertainty-unit cross-check added (info finding on mismatch, no conversion); no hardcoding; unknown units → `""` per model convention.
2. **Header inheritance:** Explicit dual-header read; no assumption of Astropy auto-merge; extension-vs-primary precedence defined; conflicts favor extension for extension metadata and are noted; verified vs unknown preserved.
3. **Numeric dtype rules:** Separate rules — float64 for `TIME`/flux/uncertainty (endianness handled), int64 for `SAP_QUALITY`/`CADENCENO` **with no float-to-integer truncation**; incompatible types rejected with `FITSImportError`.
4. **FITS null handling:** Verified Astropy behavior — TNULL only for integer columns (exposed via `Column.null`), floats use NaN; raw sentinel via `hdul.data`, masked via `Table.read`; NaN preserved/reported; **genuine model limitation** for per-row integer missingness flagged for approval (no model change invented).
5. **Time metadata:** Independent resolution of `TUNITn`/`TIMEUNIT`/`TIMESYS`/`TIMEREF`/`BJDREFI`/`BJDREFF`; values unchanged; no BKJD→JD; unit/reference/scale/frame not conflated.
6. Carried over all prior corrections: simplified exception-only interface, testing in 2.2.2, corrected source metadata mapping, filename-stem naming, corrected FITS fixture assumptions, empty-table rejection, deterministic column-name matching, zero-based row indices.

---

## Statement

**Implementation has not started.** No files were created, modified, deleted, or renamed in this session; no dependencies installed; no configuration changed; the original FITS file untouched; no Git state altered by me. This revised plan remains in PLAN mode and awaits your explicit review and authorization before any switch to Build mode.


# Chatgpt plan v3 review/revision

The revised plan is substantially improved, and the five requested refinements are mostly addressed. I would not approve BUILD yet, because a few implementation details remain internally inconsistent or underspecified.

The most important issue is uncertainty units: `MeasurementColumn` has one `unit` field, but the plan proposes reading a separate unit from each `*_FLUX_ERR` column. If an uncertainty unit differs from its flux unit, the current model cannot preserve both units. Recording an informational warning does not solve that data-loss problem.

There are also two related points to tighten: the integer `TNULL` policy should be decided before implementation rather than left as a future conditional choice, and the HDU-selection rules need to specify how an unsuitable `LIGHTCURVE` extension interacts with another structurally valid candidate.

## Remaining issues to resolve

### 1. Uncertainty units are not fully representable

The model stores:

- `MeasurementColumn.unit` — one unit string for the measurement.
- `MeasurementColumn.uncertainties` — an array, but no separate uncertainty-unit field.

The plan currently says to read the uncertainty's `TUNITn` independently, compare it with the flux unit, and report mismatches as informational findings. However, if the units differ, the importer has nowhere structured to store the uncertainty unit.

Recommendation: Treat a mismatch as an import error for that measurement pair unless the model is explicitly extended. Do not silently attach uncertainties with a potentially incompatible unit. Exact string comparison is a conservative first implementation; unit equivalence and conversion can be considered separately later.

If you prefer to keep importing the flux data despite a mismatch, that needs an explicit decision about how the uncertainty values and their original units will be represented.

### 2. Time unit and time reference are still conflated in the mapping

Section 8.1 currently lists `TUNIT1` as a possible source for both:

- `TimeInfo.unit`
- `TimeInfo.reference`

But the Kepler example demonstrates why these must remain separate:

- `TIMEUNIT = "d"` describes the numerical time unit.
- `TUNIT1 = "BJD - 2454833"` describes the time convention/reference in this file.

The plan should not generally treat a `TUNITn` value as a physical time unit. Use `TIMEUNIT` for `TimeInfo.unit`; use a recognized descriptive convention from the column metadata for `TimeInfo.reference`. If either is absent or cannot be interpreted safely, leave it unknown.

### 3. Integer `TNULL` needs a defined policy

This is a real model limitation, but it does not require expanding the model for this subtask.

Recommended policy:

- Inspect `Column.null` for supported integer columns.
- If a `TNULL` sentinel is declared but does not occur in the data, import normally.
- If one or more values equal the declared sentinel, raise `FITSImportError` explaining that the model cannot represent per-row missing integer values.
- Preserve the original file unchanged.
- Do not reinterpret the sentinel as a valid quality flag or cadence number.

This is safer than preserving a known missing value as if it were a measurement. It also avoids an unnecessary model redesign for 2.2.2.

### 4. Header inheritance needs one more clarification

The explicit primary/extension header handling is good. However, the plan should distinguish between:

- Explicitly present extension-header values.
- Primary-header values that are eligible for inheritance.
- Primary-header values used as application-level fallback metadata.

`INHERIT=True` is relevant to the FITS inheritance convention. The plan should state whether primary-header fallback is conditional on that keyword or is an explicit application policy independent of FITS inheritance. Either approach can be documented, but it should not imply that the importer is automatically implementing FITS header inheritance when it is actually applying its own fallback rules.

### 5. HDU selection needs a small clarification

The current rule says to prefer `EXTNAME=LIGHTCURVE`, then choose the first candidate if multiple candidates remain.

Specify that the preferred `LIGHTCURVE` HDU must itself satisfy the structural requirements (`TIME` plus at least one supported flux column). An unsuitable HDU named `LIGHTCURVE` must not override another structurally valid candidate.

## Other parts of the plan

These are satisfactory and do not need another redesign:

- The simplified `import_light_curve()` / `FITSImportError` interface.
- Keeping FITS reading separate from the scientific model and GUI.
- Copying arrays before closing the FITS file.
- Float64 and int64 conversion rules.
- Preserving NaN and infinite values.
- Keeping SAP and PDCSAP as separate measurements.
- Retaining quality flags without filtering.
- Zero-based validation row indices.
- Portable temporary FITS fixtures.
- Gating real-data verification on the external Kepler file.
- Keeping project persistence and visualization outside 2.2.2.
- Updating the roadmap and development log during implementation.

## One verification limitation

I also inspected the supplied repository snapshot ZIP. It does not contain `src/light_curve.py` or `tests/test_light_curve.py`, so I cannot independently verify the 2.2.1 interfaces from that snapshot. The model details above are therefore being assessed against the inspection results in Nemotron's report and the previously established 2.2.1 record—not against a fresh copy of those source files.

## Recommended next step

Have Nemotron make only these targeted corrections to the existing plan. Do not ask it to redesign the model or begin implementation.

Remain in **PLAN mode**. Do not create, modify, delete, or rename files. Do not implement anything or switch to BUILD mode.

Please make a final targeted refinement to the existing Subtask 2.2.2 implementation plan. Preserve its verified repository findings, approved model design, task boundaries, testing strategy, and all satisfactory sections.

Address only these remaining issues:

1. **Uncertainty units and model representation**
   - `MeasurementColumn` has one `unit` field and no separate uncertainty-unit field.
   - The current plan reads uncertainty-column `TUNITn` independently but only reports mismatches informationally.
   - Define a safe behavior for mismatched flux and uncertainty units. Recommended default: raise `FITSImportError` for the affected measurement pair rather than attach potentially incompatible uncertainties or silently lose their unit metadata.
   - Do not extend the model without explicit approval.
2. **Time unit versus time reference**
   - Correct Section 8 so `TIMEUNIT` supplies `TimeInfo.unit`.
   - Treat `TUNITn` as column metadata; do not automatically interpret a descriptive value such as `BJD - 2454833` as a physical unit.
   - A recognized descriptive time convention may populate `TimeInfo.reference`.
   - Keep time unit, time convention/reference, time scale, reference frame, and numeric reference offset separate.
   - Preserve unknown values rather than infer them.
3. **Integer FITS TNULL policy**
   - Define the importer behavior instead of leaving a future decision unresolved.
   - Recommended policy: inspect `Column.null`; if a sentinel is declared but no data values equal it, import normally. If any supported integer-column values equal the declared sentinel, raise `FITSImportError`, because the current model cannot represent per-row missing integer values.
   - Do not preserve a known missing sentinel as an ordinary quality flag or cadence number.
   - Do not change the model.
4. **Header inheritance**
   - Clarify the distinction between extension-header values, primary-header values eligible for FITS inheritance, and any application-level fallback policy.
   - State explicitly whether primary-header fallback is conditional on `INHERIT=True` or is a documented application policy independent of FITS inheritance.
   - Do not claim automatic FITS inheritance if the importer implements its own lookup policy.
5. **HDU selection**
   - A preferred `EXTNAME=LIGHTCURVE` candidate must itself satisfy the structural requirements (`TIME` and at least one supported flux column).
   - An unsuitable HDU named `LIGHTCURVE` must not override another structurally valid candidate.

Return the complete revised plan, followed by a concise list of the exact changes made. Do not repeat unrelated sections unnecessarily in the change list.

Do not modify repository files. Do not begin implementation. Remain in PLAN mode and wait for my explicit approval.

Status: The plan is close to implementation-ready, but I recommend holding BUILD approval until these five points are resolved.


# opencode plan v4


I'll present the complete revised plan with the five targeted refinements integrated, remaining in PLAN mode with no file modifications.

---

# Subtask 2.2.2 — FITS Import and Validation: Final Revised Implementation Plan

**Mode: PLAN ONLY. No implementation, file creation, modification, deletion, or renaming. No switch to Build mode.**

---

## 1. Repository State and Preparation

### 1.1 Verified repository facts (current, re-checked)

| Item | Verified value |
|---|---|
| Working directory | `C:\Code\New_Project` (git repo, branch `master`) |
| HEAD commit | `113a9ab task 2.2.2 planning begin` — Author: Brett, Date: Wed Nov 4 13:52:42 2026. **Pre-existing user commit; not created by me.** |
| Previous commit | `f65f14f Task 2.2.1` |
| Working tree vs HEAD | **One modified file (not staged):** `docs/planning/.../task 2.2.2 FITS import and validation WORKING PROGRESS LOG.md` (+1,119 insertions beyond the commit). **Pre-existing user edit; left untouched.** |
| Untracked files | None |
| `subtask-2.2-light-curve-import OVERVIEW.md` | Unmodified in working tree (committed in `113a9ab`) |

### 1.2 Confirmation that Subtask 2.2.1 exists
**Verified.** `src/light_curve.py` and `tests/test_light_curve.py` both exist.

### 1.3 Current test baseline (reconfirmed)
`python -m pytest -q` → **224 passed, 0 failed.** Regression baseline for 2.2.2.

### 1.4 Existing user changes / repository-state concerns
The two pre-existing planning-file changes are outside `src/` and `tests/` and predate this task. No commits/pushes by me.

---

## 2. Verified 2.2.1 Model Review

All details from direct inspection of `src/light_curve.py` (493 lines) and `tests/test_light_curve.py` (759 lines). No redesign; the model is reused as-is.

### 2.1 Model components and interfaces (verified)

| Component | Fields / behavior |
|---|---|
| `DatasetSource` | `original_filename`, `original_file_path`, `archive`, `source_id`, `mission`, `instrument`, `target_object`, `checksum` — all `str \| None`, default `None`. |
| `TimeInfo` | `values: np.ndarray` (required); `unit`, `reference`, `time_scale`, `time_reference_frame` (str, default `""`); `reference_value`, `start`, `stop`, `resolution`, `format_hint` (float/str, default `None`). Unknown → `""`/`None`; does not block construction. |
| `MeasurementColumn` | `name: str`, `values: np.ndarray`, `unit: str = ""`, `uncertainties: np.ndarray \| None = None`, `description: str \| None = None`. **One `unit` field only — no separate uncertainty-unit field.** Property `n_nonfinite`. Non-finite preserved; `None` uncertainties ≠ zero-array uncertainties. |
| `MeasurementSeries` | `series: dict[str, MeasurementColumn]`; keys must equal `column.name`; no duplicates. |
| `ValidationFinding` | `code`, `message`, `severity`, `column: str \| None`, `row_indices: list[int] \| None` (zero-based). |
| `ValidationReport` | `errors`, `warnings`, `info` lists of `ValidationFinding`. |
| `LightCurveDataset` | `dataset_id` (UUID, auto), `name` (str, required), `source`, `time`, `measurements`, `quality_flags: np.ndarray \| None`, `cadence_numbers: np.ndarray \| None`, `validation`, `imported_at` (auto ISO UTC), `notes: str \| None`. Property `n_observations`. |

### 2.2 Structural validation (`__post_init__`)
Raises `LightCurveValidationError` (subclass of `ValueError`) for invalid `dataset_id`; missing/non-ndarray `time.values`; non-str `time.unit`; non-`MeasurementSeries` measurements; key/name mismatch; duplicate names; non-ndarray column values/unit/uncertainties; array length mismatches vs. time; non-`ValidationReport` validation; non-str `imported_at`.

### 2.3 Array copying and ownership
`_copy_arrays` converts `time.values` and each measurement `values`/`uncertainties` to `np.array(..., dtype=np.float64, copy=True)`; `quality_flags`/`cadence_numbers` to `np.array(..., dtype=np.int64, copy=True)`. Model owns independent copies. Importer must still copy FITS memory-mapped arrays **before** closing the file.

### 2.4 Serialization
`to_dict()` → JSON-compatible dict; arrays → `.tolist()`; `None` preserved as `None`. `from_dict(data)` reconstructs and re-validates; distinguishes `None` from arrays.

### 2.5 Compatibility with Kepler FITS dataset
Compatible — no model change required for the supported columns. Non-finite flux preserved; 37 nonzero quality flags preserved (no filtering); BKJD/TDB/SOLARSYSTEM in separate `TimeInfo` fields; float32→float64 upcast value-preserving; big-endian dtypes converted by `np.array(..., dtype=..., copy=True)`.

### 2.6 Genuine model limitation flagged for approval
`MeasurementColumn` has a single `unit` field with no separate uncertainty-unit field. Per refinement §3 below, mismatched flux/uncertainty units raise `FITSImportError` rather than extending the model.

---

## 3. Confirmed FITS Inspection Findings

Verified against `C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits` (read-only, outside repo, unchanged) using Astropy 7.2.0.

### 3.1 HDU structure
| HDU | Type | EXTNAME | Rows/Cols | Notes |
|---|---|---|---|---|
| 0 | `PrimaryHDU` | `PRIMARY` | — | 58 cards |
| 1 | `BinTableHDU` | `LIGHTCURVE` | 476 × 20 | Light-curve table |
| 2 | `ImageHDU` | `APERTURE` | 12 × 10 | Aperture mask |

### 3.2 LIGHTCURVE columns (verified)
| # | Column | Format | dtype (stored) | Unit (TUNIT) | 2.2.2 role |
|---|---|---|---|---|---|
| 1 | `TIME` | D | `>f8` | `BJD - 2454833` | **Required** (time) |
| 2 | `TIMECORR` | E | `>f4` | `d` | Unsupported |
| 3 | `CADENCENO` | J | `>i4` | — | **Optional** (cadence) |
| 4 | `SAP_FLUX` | E | `>f4` | `e-/s` | **Required flux** (≥1 of SAP/PDCSAP) |
| 5 | `SAP_FLUX_ERR` | E | `>f4` | `e-/s` | **Optional** uncertainty for SAP_FLUX |
| 6 | `SAP_BKG` | E | `>f4` | `e-/s` | Unsupported |
| 7 | `SAP_BKG_ERR` | E | `>f4` | `e-/s` | Unsupported |
| 8 | `PDCSAP_FLUX` | E | `>f4` | `e-/s` | **Required flux** (≥1 of SAP/PDCSAP) |
| 9 | `PDCSAP_FLUX_ERR` | E | `>f4` | `e-/s` | **Optional** uncertainty for PDCSAP_FLUX |
| 10 | `SAP_QUALITY` | J | `>i4` | — | **Optional** quality flags |
| 11–20 | centroid/position (+ errors) | D/E | mixed | pixel/pixels | Unsupported |

### 3.3 Data values (verified)
| Column | Non-finite | Min | Max | Notes |
|---|---|---|---|---|
| `TIME` | 0 | 120.53914651 | 130.24539528 | All finite |
| `CADENCENO` | N/A (int) | 568 | 1043 | Consecutive |
| `SAP_FLUX` | 4 (NaN) | 532355.0 | 532944.06 | Preserved as-is |
| `SAP_FLUX_ERR` | 4 (NaN) | ~20.04 | ~20.05 | Same 4 rows as SAP_FLUX |
| `PDCSAP_FLUX` | 7 (NaN) | 501346.12 | 501746.75 | Preserved as-is |
| `PDCSAP_FLUX_ERR` | 7 (NaN) | ~20.57 | ~20.77 | Same 7 rows as PDCSAP_FLUX |
| `SAP_QUALITY` | N/A (int) | — | — | 37 nonzero; `{64, 128, 8192, 8320, 12352, 32800}` |
| `PSF_CENTR1` | 476 (all NaN) | — | — | Unsupported column |

No TNULL null sentinels present in this file; missing float values are NaN.

### 3.4 Header metadata (verified)
**Primary:** `TELESCOP=Kepler`, `INSTRUME=Kepler Photometer`, `OBJECT=KIC 11904151`, `KEPLERID=11904151`, `ORIGIN=NASA/Ames`, `MISSION=Kepler`, `QUARTER=0`, `OBSMODE=long cadence`, `DATE=2015-08-26`.

**LIGHTCURVE extension (`INHERIT=True`):** `TIMEREF=SOLARSYSTEM`, `TASSIGN=SPACECRAFT`, `TIMESYS=TDB`, `BJDREFI=2454833`, `BJDREFF=0.0`, `TIMEUNIT=d`, `TSTART=120.52892942`, `TSTOP=130.25561236`, `TIMEDEL=0.02043359821692`, `EXPOSURE=8.95472397`, `DATE-OBS`, `DATE-END`, PDC keywords.

### 3.5 Time convention (verified)
Values are `BJD − 2454833` (BKJD-style), days (`TIMEUNIT=d`), time system `TDB`, reference frame `SOLARSYSTEM`, `BJDREFI=2454833`, `BJDREFF=0`. **Not ordinary Julian Date.** No conversion.

---

## 4. Proposed Importer Module and Public Interface

### 4.1 Module path
`src/fits_importer.py` — new module alongside `src/light_curve.py`. Single module initially.

### 4.2 Dependencies
`astropy.io.fits` (approved, DEC-006), `numpy` (approved), `src.light_curve` (reused model). Standard library only otherwise. **No new dependencies.** No PySide6, no project/service/repository imports.

### 4.3 Simplified public interface
**Successful import:** return a constructed `LightCurveDataset`. Non-fatal validation findings stored in `dataset.validation` (warnings/info). **No separate result dataclass.**

**Failed import:** raise `FITSImportError` with meaningful explanation. No partially populated dataset returned.

```python
class FITSImportError(Exception):
    """Raised when a file-level condition prevents FITS light-curve import."""

def import_light_curve(file_path: str | os.PathLike[str]) -> LightCurveDataset:
    """Read a FITS light-curve file and return a LightCurveDataset.

    Raises FITSImportError for file access, FITS parsing, missing/unsuitable
    table structure, missing required columns, incompatible data types, empty
    tables, mismatched flux/uncertainty units, integer TNULL sentinels in data,
    or model-construction failures. Non-fatal scientific conditions are reported
    via the returned dataset's ValidationReport.
    """
```

### 4.4 Failure categories distinguished
1. File access failures (missing, unreadable, permission).
2. FITS parsing failures (corrupted, invalid structure).
3. Missing/unusable light-curve structure (no table with TIME + flux column).
4. Missing required columns (`TIME`, or neither `SAP_FLUX` nor `PDCSAP_FLUX`).
5. Incompatible data types (non-numeric where numeric required).
6. Mismatched flux/uncertainty units (§5).
7. Integer `TNULL` sentinel present in data (§6).
8. Structural model-construction failures (`LightCurveValidationError` re-raised as `FITSImportError` with context).

### 4.5 Exception context
Exceptions chain the underlying cause (`raise FITSImportError(...) from exc`); user-facing message meaningful without leaking implementation details. No GUI error handling.

---

## 5. Measurement Units and Uncertainty-Unit Policy (Refinement 1)

### 5.1 Model representation constraint
`MeasurementColumn` has exactly one `unit` field and **no separate uncertainty-unit field**. The model is not extended without explicit approval.

### 5.2 Flux unit resolution
Each supported flux column's unit is read independently from its own `TUNITn` keyword:
- `SAP_FLUX.unit` ← `TUNIT4` value (e.g. `"e-/s"`), or `""` if absent/empty/unknown.
- `PDCSAP_FLUX.unit` ← `TUNIT8` value, or `""` if absent/empty/unknown.
Each column retains its own unit string; SAP and PDCSAP units are stored separately and not assumed equal.

### 5.3 Uncertainty unit resolution and mismatch policy
Each uncertainty column's unit is read from its own `TUNITn`:
- `SAP_FLUX.uncertainties` unit ← `TUNIT5` value, or `""` if absent/empty/unknown.
- `PDCSAP_FLUX.uncertainties` unit ← `TUNIT9` value, or `""` if absent/empty/unknown.

**Mismatch policy (required correction):** If a flux column and its corresponding uncertainty column both declare non-empty units and those units differ, the importer raises `FITSImportError` for the affected measurement pair. Rationale: the model has no place to store a distinct uncertainty unit, so attaching an uncertainty whose unit conflicts with its flux unit would silently conflate incompatible units. The alternative — silently dropping the uncertainty unit metadata — is also rejected because it loses information.

If either the flux or uncertainty unit is empty/unknown, no mismatch error is raised (unknown units are preserved as `""` per model convention; an info finding may note the unknown unit).

### 5.4 No hardcoding; unknown units preserved
Units are never hardcoded based on the Kepler example. Any `TUNITn` absent, blank, or unrecognized → `""` (unknown) per model convention.

---

## 6. Integer FITS TNULL Policy (Refinement 3)

### 6.1 How Astropy exposes null values (verified by read-only test)
- **Float columns** (`D`/`E` formats): Astropy does **not** permit `TNULL` on binary-table float columns. Missing float values are ordinary `NaN`.
- **Integer columns** (`J` format): Astropy permits `TNULL`, exposed via `Column.null`. Read via `hdul[1].data` (FITS record array) the raw sentinel integer is preserved as a plain integer — **not masked**. Read via `Table.read()` the column becomes masked.

### 6.2 Policy (replaces the previously unresolved decision)
For each supported integer column (`SAP_QUALITY`, `CADENCENO`):
1. Inspect `Column.null` to determine whether a sentinel is declared.
2. If no sentinel is declared → import normally.
3. If a sentinel **is** declared but no data value equals it → import normally (the sentinel is unused).
4. If **any** data value equals the declared sentinel → raise `FITSImportError`, because the current model cannot represent per-row missing integer values (`quality_flags`/`cadence_numbers` are plain `np.ndarray \| None` with `None` meaning the whole column absent, not per-row missing).

### 6.3 Preservation rules
- A known missing sentinel is **not** preserved as an ordinary quality flag or cadence number.
- The model is **not** changed. If this policy is ever too restrictive, a model change would require separate approval (Subtask 2.2.1 scope).

---

## 7. Header Inheritance and Resolution (Refinement 4)

### 7.1 Explicit dual-header read; no assumption of automatic FITS inheritance
The importer reads **both** the primary header (`hdul[0].header`) and the extension header (`hdul[1].header`) explicitly. It does **not** assume Astropy automatically merges inherited primary-header keywords into the extension header, even when `INHERIT=True` is present. `INHERIT=True` is observed as file content but is **not** relied upon as an automatic in-memory merge mechanism.

### 7.2 Three distinct sources
| Source | Meaning | Role in importer |
|---|---|---|
| Extension-header values | Keywords declared directly on the table extension | Preferred source for extension-specific metadata (time-related: `TIMEUNIT`, `TIMESYS`, `TIMEREF`, `BJDREFI`, `BJDREFF`, `TSTART`/`TSTOP`) |
| Primary-header values eligible for FITS inheritance | Keywords on the primary HDU that FITS convention allows extensions to inherit (`INHERIT=True`) | Considered only as an application-level fallback, **not** as automatic inheritance |
| Application-level fallback policy | Importer-defined rule for when a value is absent from the preferred source | Documented below; independent of FITS `INHERIT` |

### 7.3 Fallback policy (application-level, not conditional on `INHERIT=True`)
- **Extension-specific time metadata:** extension header is authoritative; primary header is **not** consulted as fallback for `TIMEUNIT`/`TIMESYS`/`TIMEREF`/`BJDREFI`/`BJDREFF`/`TSTART`/`TSTOP`. If absent from the extension, the value is unknown (`""`/`None`) — no silent primary fallback.
- **Source metadata** (`mission`, `instrument`, `target_object`, `source_id`): primary header preferred (`MISSION`, `INSTRUME`, `OBJECT`, `KEPLERID`); if absent from primary, extension header may be consulted as a documented application-level fallback. This fallback is an **importer policy**, independent of `INHERIT=True`, and is **not** claimed as automatic FITS inheritance.

### 7.4 Conflicting values
If primary and extension declare conflicting values for the same metadata class, the source preferred for that metadata class wins per §7.3; the conflict is noted in `dataset.validation.info` or `dataset.notes` so the distinction is visible, not silently resolved.

### 7.5 Verified vs unknown metadata
Metadata present and readable → stored as verified. Metadata absent, blank, or unreadable → field left unknown (`""`/`None`) per model convention; never fabricated.

---

## 8. Time Metadata (Refinement 2)

### 8.1 Independent resolution of each concept

| Model field | Source | Meaning | Verified Kepler value |
|---|---|---|---|
| `TimeInfo.unit` | `TIMEUNIT` (extension header) | Physical unit of the numeric time values | `"d"` (days) |
| `TimeInfo.reference` | Table `TUNIT1` if descriptive (e.g. `BJD - 2454833`), else `""` | Time reference/convention (not a physical unit) | `"BJD - 2454833 (BKJD)"` |
| `TimeInfo.time_scale` | `TIMESYS` (extension header) | Time scale | `"TDB"` |
| `TimeInfo.time_reference_frame` | `TIMEREF` (extension header) | Reference frame | `"SOLARSYSTEM"` |
| `TimeInfo.reference_value` | `BJDREFI` (+ `BJDREFF`) (extension header) | Numeric reference offset | `2454833.0` |
| `TimeInfo.start` | `TSTART` (extension header) | Observation start | `120.52892942` |
| `TimeInfo.stop` | `TSTOP` (extension header) | Observation stop | `130.25561236` |
| `TimeInfo.resolution` | `TIMEDEL` (extension header) | Time resolution | `0.02043359821692` only if meaning/units verified, else `None` |

### 8.2 Time unit versus time reference (required correction)
- `TIMEUNIT` supplies `TimeInfo.unit` (`"d"`).
- `TUNIT1` for the `TIME` column is treated as **column metadata**, not automatically interpreted as a physical unit. A descriptive value such as `BJD - 2454833` is **not** treated as a unit; it may populate `TimeInfo.reference` as a recognized descriptive time convention.
- Time unit, time convention/reference, time scale, reference frame, and numeric reference offset are kept **separate** and not conflated.

### 8.3 Preservation rules
- Original time values copied unchanged (float64); **no BKJD→JD conversion**, no relabeling as JD, no timestamp modification.
- Missing time unit/reference/scale/frame → `""`/`None` per model convention; unknown values preserved rather than inferred.

---

## 9. Numeric Dtype Rules (unchanged from prior plan, retained for completeness)

| Array group | Columns | Stored FITS dtype | Conversion rule | Model dtype |
|---|---|---|---|---|
| Floating-point scientific measurements | `TIME`, `SAP_FLUX`, `PDCSAP_FLUX`, `SAP_FLUX_ERR`, `PDCSAP_FLUX_ERR` | `>f8`, `>f4` | Convert to `np.float64` via `np.array(..., dtype=np.float64, copy=True)`. Endianness handled by NumPy. Non-finite preserved. | `float64` |
| Integer-valued identifiers/flags | `CADENCENO`, `SAP_QUALITY` | `>i4` | Convert to `np.int64` via `np.array(..., dtype=np.int64, copy=True)`. **No float-to-integer truncation** — read as integers directly. | `int64` |

Incompatible types (e.g., string/object where numeric expected) → `FITSImportError`. No silent coercion. No universal type-conversion framework.

---

## 10. HDU Identification and Selection (Refinement 5)

1. Open `fits.open(path, mode="readonly")` inside a `with` block (guaranteed close on success and failure).
2. Iterate all HDUs; **structural candidates** = table HDUs (`BinTableHDU`/`TableHDU`) whose column names include `TIME` and at least one of `SAP_FLUX` / `PDCSAP_FLUX`.
3. **Preferred `EXTNAME=LIGHTCURVE`:** a candidate whose `EXTNAME == "LIGHTCURVE"` is preferred **only if it itself satisfies the structural requirements** (`TIME` and at least one supported flux column).
4. **An unsuitable `LIGHTCURVE`-named HDU must not override a structurally valid candidate.** If the HDU named `LIGHTCURVE` lacks `TIME` or both flux columns, it is skipped and another structural candidate is used.
5. If multiple structural candidates remain after the `LIGHTCURVE` preference, deterministic tie-break (first in HDU order) + informational finding about ambiguity. Ambiguity does **not** prevent import when a reasonable choice exists; prevents import only if no candidate satisfies the structural rule.
6. No candidate → `FITSImportError`.
All array copies made **inside** the `with` block before close (memory-mapped data).

---

## 11. Measurement and Metadata Mapping

### 11.1 Required / optional / unsupported table columns

| FITS column | Role | Required for construction? | Model target | Absent behavior |
|---|---|---|---|---|
| `TIME` | timestamps | **Yes** | `TimeInfo.values` (+ metadata) | `FITSImportError` |
| `SAP_FLUX` | SAP flux | At least one of SAP/PDCSAP | `MeasurementColumn("SAP_FLUX")` | — |
| `PDCSAP_FLUX` | PDC flux | At least one of SAP/PDCSAP | `MeasurementColumn("PDCSAP_FLUX")` | — |
| `SAP_FLUX_ERR` | SAP uncertainty | Optional | `SAP_FLUX.uncertainties` | `None`, warning |
| `PDCSAP_FLUX_ERR` | PDC uncertainty | Optional | `PDCSAP_FLUX.uncertainties` | `None`, warning |
| `SAP_QUALITY` | quality flags | Optional | `quality_flags` (int64) | `None` |
| `CADENCENO` | cadence ids | Optional | `cadence_numbers` (int64) | `None` |
| Other columns | — | No | Not imported | possibly noted in `notes` |

SAP and PDCSAP remain independent columns, each paired with its own `*_FLUX_ERR`. Never merged. Never one silently discarded.

### 11.2 Source metadata mapping

| `DatasetSource` field | Proposed source | Notes |
|---|---|---|
| `mission` | `MISSION` header | Leave `None` if absent |
| `instrument` | `INSTRUME` header | Leave `None` if absent |
| `target_object` | `OBJECT` header | Leave `None` if absent |
| `source_id` | `KEPLERID` (target ID) | Distinct from product/file ID; `None` if absent |
| `archive` | `None` | **Not** `ORIGIN` unless supplying archive independently established |
| `original_filename` | Actual input filename | |
| `original_file_path` | Actual input path | |

`ORIGIN=NASA/Ames` may be retained in `notes` or an informational finding, but **must not** automatically be described as the archive. Do not invent source metadata; absent/ambiguous → field unknown.

### 11.3 Dataset naming
- `LightCurveDataset.name` = input filename stem (e.g. `kplr011904151-2009131105131_llc_full`).
- Full original filename in `DatasetSource.original_filename`; full path in `original_file_path`.
- Do not invent a target name or scientific label when the filename is the only reliable identifier.
- Empty/unusable stem → `FITSImportError` rather than silently inventing a name.

### 11.4 Metadata not representable by current model
Raw FITS `TTYPE`/`TFORM`/`TDISP`/`NULL` per column, full header card list, aperture image (HDU2), PDC config keywords. Not important enough to require a model change for 2.2.2; may go in `LightCurveDataset.notes` or remain out of scope. Any model-field addition is a 2.2.1-scope decision requiring approval.

---

## 12. Complete Validation Matrix

Classifications: **Error** = `FITSImportError` raised, no dataset constructed (not placed in a dataset `ValidationReport`, since no dataset exists). **Warning** = import succeeds, finding in `dataset.validation.warnings`, data preserved. **Info** = import succeeds, finding in `dataset.validation.info`, data preserved. **Preserve** = kept as-is, no modification.

| # | Condition | Succeeds? | Finding | Data preserved? | Raises `FITSImportError`? | User approval? |
|---|------|---|---|---|---|---|
| F1 | Missing / unreadable file | No | — | N/A | Yes | No |
| F2 | Corrupted / invalid FITS structure | No | — | N/A | Yes | No |
| F3 | No table HDU with TIME + flux column | No | — | N/A | Yes | No |
| F4 | Multiple candidate tables, no reasonable choice | No | — | N/A | Yes | No |
| F5 | Multiple candidate tables, reasonable choice | Yes | Info (ambiguity) | Yes | No | No |
| C1 | `TIME` column absent | No | — | N/A | Yes | No |
| C2 | Neither `SAP_FLUX` nor `PDCSAP_FLUX` present | No | — | N/A | Yes | No |
| C3 | Only SAP or only PDCSAP available | Yes | Info (single flux series) | Yes | No | No |
| C4 | Flux present, matching `*_FLUX_ERR` absent | Yes | Warning (missing uncertainty) | Yes, `uncertainties=None` | No | No |
| C5 | `*_FLUX_ERR` present but its flux absent | Yes | Warning/info (orphan ignored) | Yes, orphan not imported | No | No |
| C6 | `SAP_QUALITY` / `CADENCENO` absent | Yes | Optional → `None` | Yes | No | No |
| C7 | Extra unsupported numeric columns | Yes | Not imported (possibly info) | Yes | No | No |
| C8 | Unexpected/incompatible dtype (non-numeric where numeric required) | No | — | N/A | Yes | No |
| C9 | Array length ≠ time length | No | — | N/A | Yes (via model `LightCurveValidationError`) | No |
| M1 | Non-numeric timestamp | No | — | N/A | Yes | No |
| M2 | Non-finite timestamp (NaN/inf) | Yes | Warning | Yes, preserved | No | No |
| M3 | Non-finite flux (NaN/inf) | Yes | Warning (`n_nonfinite` + zero-based row indices) | Yes, preserved | No | No |
| M4 | Non-finite uncertainty | Yes | Warning | Yes, preserved | No | No |
| M5 | Negative uncertainty | Yes | Warning | Yes, preserved (not replaced) | No | No |
| M6 | Duplicate timestamps | Yes | Warning | Yes, preserved (not reordered) | No | No |
| M7 | Non-monotonic timestamps | Yes | Warning | Yes, preserved (order kept) | No | No |
| Q1 | Nonzero quality flags present | Yes | Info (count + zero-based row indices) | Yes, preserved | No | No |
| Q2 | Quality-bitmask filtering requested | N/A | Not performed in 2.2.2 | — | No | **Yes** (future policy) |
| T1 | Missing time unit | Yes | Info | Yes, `unit=""` | No | No |
| T2 | Missing time reference/scale/frame | Yes | Info | Yes, empty/`None` | No | No |
| T3 | Missing flux unit | Yes | Info | Yes, `unit=""` | No | No |
| U1 | Flux unit ≠ its uncertainty unit (both non-empty) | No | — | N/A | Yes (§5.3) | No |
| N1 | Integer `TNULL` sentinel present in `SAP_QUALITY`/`CADENCENO` data | No | — | N/A | Yes (§6.2) | No |
| E1 | Empty table (zero observations) | No | — | N/A | Yes | No |
| D1 | Duplicate/conflicting supported column names | No | — | N/A | Yes | No |

**Scientific reasoning (§5.1, §5.6):** non-finite and questionable measurements preserved, never removed/replaced/zero-filled (§5.1.4, §5.6.1 acceptance 3). Quality flags never auto-filtered (§3.4.10; REVIEW-002 justification). File-level failures are exceptions, not `ValidationReport` errors (no dataset exists to attach to — §5.6.7).

---

## 13. Error-Handling Strategy

- Single exception type: `FITSImportError` (subclass of `Exception`), meaningful user-facing message, chained underlying cause (`from exc`).
- Success path: return `LightCurveDataset`; warnings/infos live in `dataset.validation`.
- Failure path: raise `FITSImportError`; no partially populated dataset returned.
- `LightCurveValidationError` from model construction caught and re-raised as `FITSImportError` with context.
- Zero-based `row_indices` in every `ValidationFinding`.
- No GUI error handling; no file-selection dialogs; caller decides presentation.

---

## 14. Data-Integrity and Resource-Management Approach

- Open read-only (`mode="readonly"`); never open for write.
- All array copies made **inside** the `with fits.open(...)` block before close.
- Convert big-endian FITS dtypes to native float64/int64 via `np.array(..., dtype=..., copy=True)`; float32→float64 value-preserving.
- Non-finite values preserved (no fill/replace/interpolate).
- Quality flags preserved (no filtering).
- Distinct columns remain distinct (SAP ≠ PDCSAP).
- No observations silently discarded (observation count preserved).
- No units or timestamps silently changed (no BKJD→JD conversion).
- No normalization/detrending/filtering.
- Model's `_copy_arrays` provides a second authoritative safety copy.
- Original FITS file bytes/checksum unchanged; file remains outside repo and unmodified.

---

## 15. Focused 2.2.2 Automated Testing Plan

Tests in a new module (e.g., `tests/test_fits_importer.py`), fixtures under pytest `tmp_path` — **no dependence on external Kepler dataset or absolute Windows paths.** Portable suite passes on any machine.

### 15.1 Temporary FITS fixtures
- Valid Kepler-like multi-HDU table (Primary + LIGHTCURVE at index 1 + APERTURE).
- Light-curve table at a different HDU index.
- Structural table identification (by TIME + flux column, not position).
- Multiple candidate tables (deterministic tie-break + info finding).
- Unsuitable HDU named `LIGHTCURVE` that lacks TIME/flux; structurally valid candidate elsewhere must win (Refinement 5).
- Missing `TIME` column → `FITSImportError`; missing both flux columns → `FITSImportError`.
- Only `SAP_FLUX`; only `PDCSAP_FLUX`.
- Correct uncertainty pairing (SAP↔SAP_ERR, PDCSAP↔PDCSAP_ERR).
- Missing uncertainty column(s) → `uncertainties=None` + warning.
- Missing optional quality/cadence columns → `None`.
- Supported numeric dtypes and endianness (`>f4`, `>f8`, `>i4` → float64/int64).
- Rejection of incompatible string/object types → `FITSImportError`.
- Preservation of NaN/inf in flux and uncertainty.
- Negative uncertainty → warning, preserved.
- Duplicate / non-monotonic timestamps → warning, preserved, not reordered.
- Missing metadata (no time unit, no mission) → info / `None` fields.
- Duplicate/conflicting supported column names → `FITSImportError`.
- Flux unit ≠ uncertainty unit (both non-empty) → `FITSImportError` (Refinement 1).
- Empty table (zero observations) → `FITSImportError`.
- Corrupted / truncated / unreadable file → `FITSImportError`.
- Integer `TNULL` sentinel declared but unused → import normally; sentinel present in data → `FITSImportError` (Refinement 3).
- Successful dataset construction and model compatibility (`to_dict()`/`from_dict()` round-trip).
- Arrays usable after FITS closure (independent of open handle).
- Preservation of observation count and original data values.
- Zero-based validation row indices.

### 15.2 Fixture assumptions corrected
- A normal FITS binary table has a shared row structure; columns do **not** have independently mismatched lengths. Model-level array-alignment testing remains in `tests/test_light_curve.py` (already covered there).
- Do not invent malformed FITS cases merely to increase test count.

### 15.3 Resource-safety testing
- Assert returned arrays remain usable after the FITS file has closed.
- Assert returned arrays do not depend on an open FITS file handle.
- Assert imported data remains intact after close.

### 15.4 Model-only tests
Stay in `tests/test_light_curve.py`; not duplicated in importer tests.

### 15.5 Baseline
Existing 224 tests must continue to pass with no regressions.

---

## 16. Optional Real-Data Verification

Gated on the actual Kepler file being present. Skipped if absent — never makes the portable suite dependent on it.

Verify:
- HDU identified as LIGHTCURVE (index 1 structurally, not hardcoded).
- 476 rows; TIME range 120.5391–130.2454; unit `d`, scale `TDB`, reference `BJD - 2454833`, frame `SOLARSYSTEM`.
- SAP_FLUX and PDCSAP_FLUX both present and distinct; 4 and 7 non-finite respectively.
- Uncertainties paired correctly; same non-finite rows per column.
- `SAP_QUALITY` 37 nonzero preserved; `CADENCENO` 568–1043 consecutive.
- `DatasetSource.original_file_path`/`original_filename` set; mission/instrument/target_object/source_id correct.
- `name` = filename stem.
- Valid `LightCurveDataset` constructed; `to_dict()`/`from_dict()` round-trip.
- Original file checksum unchanged before/after import.

---

## 17. Documentation Impact Assessment

Per `AGENTS.md`, documentation updates are required during Build mode. No documents modified now.

### 17.1 2.2.2 implementation documentation (to update during Build)
- Record `src/fits_importer.py` module and responsibilities.
- Record public interface (`import_light_curve`, `FITSImportError`) and error behavior.
- Record supported FITS structure and column/metadata mapping (including units, time metadata, null handling).
- Record validation behavior, classifications, and limitations.
- Record focused test coverage and results.
- Update `docs/MASTER_DEVELOPMENT_ROADMAP.md` (2.2.2 status) and `docs/development/DEVELOPMENT_LOG.md` (implementation record, test results).

### 17.2 2.2.4 consolidation (future)
- Broader documentation reconciliation across subtasks; cross-subtask completion status; overall Stage 2.2 verification; remaining deferred/unresolved items.

Foundation documents remain read-only. `docs/README.md` unchanged unless a significant document is added/renamed. Existing project-lifecycle docs unchanged.

---

## 18. Explicit Subtask Boundaries

| Subtask | Responsibility | In 2.2.2? |
|---|---|---|
| 2.2.1 | Light-curve data model — done | No (reused only) |
| 2.2.2 | FITS reading, HDU identification, extraction, metadata, validation, `LightCurveDataset` construction, importer tests | **Yes — current** |
| 2.2.3 | Project association, dataset persistence, save/reopen, project IDs/ownership/permissions | No (future) |
| 2.2.4 | Broader Stage 2.2 verification, documentation reconciliation, completion assessment | No (future) |

**Excluded from 2.2.2:** project association/persistence, visualization, BLS/analysis, quality-bitmask filtering, archive downloads, universal FITS framework, database/permanent storage, GUI dialogs.

---

## 19. Risks and Unresolved Issues

| Risk / Issue | Description | Mitigation / Status |
|---|---|---|
| Memory-mapped FITS arrays | Post-close access fails if not copied. | Copy arrays inside `with` block. |
| Big-endian FITS dtypes | Convert to native float64/int64. | `np.array(..., dtype=..., copy=True)` handles byte swap. |
| Float32 → float64 upcast | Value-preserving, doubles flux memory. | Acceptable at ~476 rows. |
| Model re-copies arrays | Slight redundancy. | Acceptable; correctness > micro-optimization. |
| Real dataset not portable | Automated suite must not depend on absolute path. | Gate real-data test on file presence; `tmp_path` fixtures. |
| Validation vs exception boundary | Risk of putting import failures into nonexistent dataset's `ValidationReport`. | Enforce separation (Section 13). |
| Quality-bitmask pressure | Temptation to auto-filter nonzero flags. | Explicitly excluded; future analysis operation requiring approval. |
| Scope creep | Pressure to add persistence, UI, visualization, BLS. | Explicitly excluded. |
| Flux/uncertainty unit mismatch | Model has no separate uncertainty-unit field. | Raising `FITSImportError` (§5.3) — no model change. |
| Integer `TNULL` sentinel in data | Model cannot represent per-row missing integers. | Raising `FITSImportError` (§6.2) — no model change; Kepler file has no TNULL so does not block initial implementation. |

All previously open decisions (time unit/reference separation, TNULL policy, uncertainty-unit mismatch, header inheritance, HDU selection) are now resolved by policy in this plan and do not require further approval — except the gate to Build mode itself.

---

## 20. Recommended Build Implementation Sequence

1. Create `src/fits_importer.py`: `FITSImportError`, `import_light_curve()`, FITS opening/close, structural HDU identification (Refinement 5).
2. Implement extraction of `TIME`, `SAP_FLUX`/`PDCSAP_FLUX`, uncertainties, `SAP_QUALITY`, `CADENCENO` (array copies inside `with` block; per-column units from `TUNITn`).
3. Implement metadata extraction into `DatasetSource` and `TimeInfo` (BKJD/TDB/SOLARSYSTEM; explicit dual-header resolution per Refinement 4; time unit from `TIMEUNIT`, reference from descriptive `TUNITn` per Refinement 2; filename-stem naming).
4. Implement unit cross-check (Refinement 1) and integer `TNULL` policy (Refinement 3).
5. Implement validation findings and `ValidationReport`; dataset assembly via `LightCurveDataset` constructor; surface `LightCurveValidationError` as `FITSImportError`.
6. Create focused importer tests with `tmp_path` fixtures (Section 15); run targeted tests.
7. Optional real-data verification against Kepler file, gated on presence (Section 16).
8. Run full suite (224+ passing, no regressions).
9. Update documentation per `AGENTS.md` — Build-mode activity (Section 17).
10. Review completion; hand off to 2.2.3.

Deferred to 2.2.3: project association, persistence, save/reopen. Deferred to 2.2.4: broader integration verification and documentation reconciliation.

---

## 21. Decisions or Questions Requiring User Approval

1. **Approval of this revised plan** before switching to Build mode (the gate itself).
2. No additional decisions require approval. The five open points from the prior plan are now resolved by explicit policy in this document:
   - Uncertainty-unit mismatch → `FITSImportError` (§5.3), no model extension.
   - Time unit from `TIMEUNIT`; descriptive `TUNITn` → `TimeInfo.reference` (§8.2), no inference.
   - Integer `TNULL` sentinel in data → `FITSImportError` (§6.2), no model change.
   - Header inheritance → explicit application-level fallback policy, not automatic FITS inheritance (§7).
   - HDU selection → `LIGHTCURVE` preference only among structurally valid candidates (§10).

---

## Concise List of Exact Changes Made in This Final Refinement

1. **Uncertainty units and model representation (§5):** Added mismatch policy — if a flux column and its uncertainty column both declare non-empty units that differ, raise `FITSImportError` for the affected pair. Confirmed `MeasurementColumn` has one `unit` field with no separate uncertainty-unit field; model not extended. Unknown units preserved as `""`; no hardcoding.
2. **Time unit versus time reference (§8):** `TIMEUNIT` supplies `TimeInfo.unit`; `TUNITn` treated as column metadata, not automatically interpreted as physical unit; descriptive convention (e.g. `BJD - 2454833`) may populate `TimeInfo.reference`; unit/reference/scale/frame/offset kept separate; unknown values preserved, not inferred.
3. **Integer FITS TNULL policy (§6):** Defined behavior — inspect `Column.null`; sentinel declared but unused → import normally; sentinel equal to any data value → `FITSImportError`. Known missing sentinel not preserved as ordinary quality flag/cadence number; model unchanged. Replaces the previously unresolved decision.
4. **Header inheritance (§7):** Clarified three sources (extension-header values, primary-header values eligible for FITS inheritance, application-level fallback). Primary-header fallback is an importer policy independent of `INHERIT=True`; not conditional on it and not claimed as automatic FITS inheritance. Extension-specific time metadata uses extension header only (no silent primary fallback).
5. **HDU selection (§10):** `EXTNAME=LIGHTCURVE` preference applies only to candidates that themselves satisfy structural requirements (`TIME` + ≥1 flux column). An unsuitable `LIGHTCURVE`-named HDU must not override a structurally valid candidate.

All previously verified repository facts, the 2.2.1 model design, task boundaries, testing strategy, and the five required corrections from the prior revision are preserved unchanged.

---

**Statement:** Implementation has not started. No files were created, modified, deleted, or renamed in this session; no dependencies installed; no configuration changed; the original FITS file untouched; no Git state altered by me. This revised plan remains in PLAN mode and awaits your explicit review and authorization before any switch to Build mode.

# chatgpt plan v4 review

This revision resolves the five outstanding points from the previous review. The policies are now explicit, the integer `TNULL` limitation has a safe handling rule, and the HDU-selection logic is unambiguous.

I found two remaining data-integrity issues that I recommend correcting before approving BUILD.

## 1. Unknown uncertainty units still create an ambiguity

Section 5.3 says a mismatch is an error only when both units are non-empty.

Consider this case:

| Flux unit | Uncertainty unit | Current plan |
| --------- | ---------------- | ------------ |
| `e-/s`    | `e-/s`           | Import       |
| `e-/s`    | `adu`            | Reject       |
| `e-/s`    | Unknown          | Import       |
| Unknown   | `e-/s`           | Import       |
| Unknown   | Unknown          | Import       |

The third and fourth cases are problematic. The model has one unit field, so importing the uncertainty array means the model effectively associates it with the measurement's unit. But the importer has not established that the units match.

Recommendation: Use this policy:

- Both units present and equal: import.
- Both units absent: import, with unknown units.
- One unit present and the other absent: raise `FITSImportError`.
- Both present but different: raise `FITSImportError`.

This avoids silently assuming that an absent uncertainty unit matches the flux unit.

## 2. Unrecognized units should not be discarded

Section 5.4 currently says an unrecognized `TUNITn` becomes `""`.

That loses information unnecessarily.

The importer does not need to understand or convert a unit to preserve its original representation. The model's `unit` field is a string, so it can retain the original FITS unit text.

Recommendation:

- Missing or blank `TUNITn` → `""`.
- Present `TUNITn`, whether recognized or not → preserve the original string.
- Do not normalize, convert, or reinterpret unfamiliar unit strings.

The same principle applies to descriptive time metadata. Preserve the original `TUNIT1` text when it represents a descriptive time convention rather than a physical unit.

## Minor wording correction: header inheritance

Section 7.2 calls primary-header values "eligible for FITS inheritance," while Section 7.3 says the application fallback is independent of `INHERIT=True`.

The behavior is understandable, but the terminology could be clearer. I suggest renaming that source to primary-header values and explaining separately that the importer may consult them under its own fallback policy, regardless of `INHERIT`.

This is a documentation clarification, not an architectural problem.

## Overall assessment

Five previous issues resolved

| Area                               | Assessment                        |
| ---------------------------------- | --------------------------------- |
| Importer interface and separation  | Acceptable                        |
| FITS units and uncertainty pairing | One remaining ambiguity           |
| Integer `TNULL` handling           | Resolved                          |
| Header resolution                  | Acceptable; wording clarification |
| Time metadata                      | Acceptable                        |
| Numeric dtype conversion           | Acceptable                        |
| HDU identification                 | Resolved                          |
| Validation and error handling      | Acceptable                        |
| Test strategy                      | Acceptable                        |
| Documentation scope                | Acceptable                        |
| Subtask boundaries                 | Acceptable                        |

I also checked the supplied repository snapshot. It contains the project documentation, but not `src/light_curve.py` or `tests/test_light_curve.py`, so the reported model interfaces and 224-test baseline remain based on Nemotron's repository inspection rather than independent source verification here.

Recommendation: Ask Nemotron for one final, narrow PLAN-only refinement covering the two unit-handling issues and the header wording. After that, I expect the plan to be ready for your BUILD approval.

No implementation should begin until you explicitly authorize it.


# chatgpt plan v4 revision prompt

## PLAN Refinement Request — Subtask 2.2.2 (Final Targeted Corrections)

**Mode: PLAN ONLY. Do not implement, edit files, or begin BUILD.**

Revise the current Subtask 2.2.2 FITS importer plan to address the remaining data-integrity and documentation-clarity issues below.

Do not redesign the importer or expand the scope. Preserve the existing approved design unless a specific correction below requires a change.

### 1. Uncertainty-unit handling

The `MeasurementColumn` model has one `unit` field shared by its measurement values and optional uncertainty values.

The importer must therefore avoid assigning a unit to uncertainty values when the FITS metadata does not establish that they use the same unit.

Use this policy for each supported flux/uncertainty pair:

| Flux unit (`TUNITn`) | Uncertainty unit (`TUNITn`) | Required behavior |
|---|---|---|
| Present | Present and identical | Import normally |
| Absent or blank | Absent or blank | Import with `unit=""` |
| Present | Absent or blank | Raise `FITSImportError` |
| Absent or blank | Present | Raise `FITSImportError` |
| Present | Present but different | Raise `FITSImportError` |

Do not silently assume that a missing uncertainty unit matches the flux unit. Do not discard uncertainty data to bypass a mismatch.

### 2. Preserve original unit strings

Revise the unit-handling policy so that the importer preserves the original FITS unit text.

- If a `TUNITn` value is present and non-empty, store its original string in the corresponding model unit field.
- Do not replace unfamiliar or unrecognized unit strings with `""`.
- Do not perform unit conversion or require the importer to recognize every possible unit.
- Use `""` only when the relevant unit metadata is absent or blank.
- Apply the same preservation principle to descriptive time-unit metadata stored in `TimeInfo.reference`.
- Keep `TIMEUNIT` as the source of `TimeInfo.unit`; do not conflate it with the descriptive `TUNIT1` convention.

### 3. Clarify FITS header inheritance versus application fallback

Review the wording in the header metadata sections.

The plan must distinguish between:

- **FITS header inheritance:** behavior defined by FITS conventions and the `INHERIT` keyword.
- **Application-level fallback:** the importer's explicitly defined decision to consult the primary header when a value is absent from the selected extension header.

The importer may use primary-header fallback according to its documented application policy, independently of whether FITS header inheritance is enabled. Do not describe this fallback as automatic FITS inheritance.

Use precise terminology throughout the plan. In particular, revise wording such as "eligible for FITS inheritance" if it actually refers to application-level fallback.

### 4. Scope and constraints

Keep the existing scope unchanged:

- New module: `src/fits_importer.py`
- New tests: `tests/test_fits_importer.py`
- Public interface: `FITSImportError` and `import_light_curve(file_path)`
- Use the existing `LightCurveDataset` model.
- No GUI, persistence, project association, model redesign, or unrelated cleanup.
- Preserve non-finite measurements and observation ordering.
- Do not filter observations based on quality flags.
- Keep the existing HDU-selection, metadata mapping, numeric conversion, TNULL, and validation policies unless a correction above directly affects them.
- Do not modify Foundation documentation.

### 5. Final plan review

Return the complete revised Subtask 2.2.2 plan, not just a list of changes.

At the end, include a concise section titled **Remaining Assumptions or Unresolved Decisions**. Explicitly state whether any implementation-critical uncertainties remain.

Do not claim that code, tests, or the current repository state were independently verified unless you actually inspected the relevant files in this session. Distinguish findings from the uploaded repository snapshot from information reported in earlier planning.

**Stop after presenting the revised plan. Wait for explicit approval before any BUILD or implementation work.**

# opencode plan v5

---

# Subtask 2.2.2 — FITS Import and Validation: Final Revised Implementation Plan

**Mode: PLAN ONLY. Do not implement, edit files, or begin BUILD.**

This report revises the Subtask 2.2.2 plan with five targeted corrections: uncertainty-unit handling, original unit-string preservation, header-inheritance terminology clarification, scope preservation, and a final completeness review. All previously approved design elements are preserved unless a specific correction requires a change.

---

## 1. Repository State and Preparation

### 1.1 Verified repository facts (current)

| Item | Verified value |
|---|---|
| Working directory | `C:\Code\New_Project` (git repo, branch `master`) |
| HEAD commit | `113a9ab task 2.2.2 planning begin` — Author: Brett, Date: Wed Nov 4 13:52:42 2026. Pre-existing user commit; not created by me. |
| Previous commit | `f65f14f Task 2.2.1` |
| Working tree vs HEAD | One modified file (not staged): `docs/planning/.../task 2.2.2 FITS import and validation WORKING PROGRESS LOG.md` (+1,119 insertions beyond the commit). Pre-existing user edit; left untouched. |
| Untracked files | None |

### 1.2 Confirmation that Subtask 2.2.1 exists
**Verified.** `src/light_curve.py` and `tests/test_light_curve.py` both exist in the repository.

### 1.3 Current test baseline
`python -m pytest -q` → **224 passed, 0 failed.** Regression baseline for 2.2.2.

### 1.4 Existing user changes / repository-state concerns
The pre-existing planning-file changes (one committed, one modified in working tree) are outside `src/` and `tests/` and predate this task. They will not be touched.

---

## 2. Verified 2.2.1 Model Review

All details from direct inspection of `src/light_curve.py` (493 lines) and `tests/test_light_curve.py` (759 lines). The model is reused as-is; no redesign.

### 2.1 Model components and interfaces (verified)

| Component | Key fields / behavior |
|---|---|
| `DatasetSource` | `original_filename`, `original_file_path`, `archive`, `source_id`, `mission`, `instrument`, `target_object`, `checksum` — all `str \| None`, default `None`. |
| `TimeInfo` | `values: np.ndarray` (required); `unit`, `reference`, `time_scale`, `time_reference_frame` (str, default `""`); `reference_value`, `start`, `stop`, `resolution`, `format_hint` (float/str, default `None`). Unknown → `""`/`None`; does not block construction. |
| `MeasurementColumn` | `name: str`, `values: np.ndarray`, `unit: str = ""`, `uncertainties: np.ndarray \| None = None`, `description: str \| None = None`. **One `unit` field shared by values and uncertainties; no separate uncertainty-unit field.** Property `n_nonfinite`. Non-finite preserved; `None` uncertainties ≠ zero-array uncertainties. |
| `MeasurementSeries` | `series: dict[str, MeasurementColumn]`; keys must equal `column.name`; no duplicates. |
| `ValidationFinding` | `code`, `message`, `severity`, `column: str \| None`, `row_indices: list[int] \| None` (zero-based). |
| `ValidationReport` | `errors`, `warnings`, `info` lists of `ValidationFinding`. |
| `LightCurveDataset` | `dataset_id` (UUID, auto), `name` (str, required), `source`, `time`, `measurements`, `quality_flags: np.ndarray \| None`, `cadence_numbers: np.ndarray \| None`, `validation`, `imported_at` (auto ISO UTC), `notes: str \| None`. Property `n_observations`. |

### 2.2 Structural validation (`__post_init__`)
Raises `LightCurveValidationError` (subclass of `ValueError`) for invalid `dataset_id`; missing/non-ndarray `time.values`; non-str `time.unit`; non-`MeasurementSeries` measurements; key/name mismatch; duplicate names; non-ndarray column values/unit/uncertainties; array length mismatches vs. time; non-`ValidationReport` validation; non-str `imported_at`.

### 2.3 Array copying and ownership
`_copy_arrays` converts `time.values` and each measurement `values`/`uncertainties` to `np.array(..., dtype=np.float64, copy=True)`; `quality_flags`/`cadence_numbers` to `np.array(..., dtype=np.int64, copy=True)`. Model owns independent copies. Importer must still copy FITS memory-mapped arrays **before** closing the file.

### 2.4 Serialization
`to_dict()` → JSON-compatible dict; arrays → `.tolist()`; `None` preserved as `None`. `from_dict(data)` reconstructs and re-validates; distinguishes `None` from arrays.

### 2.5 Compatibility with Kepler FITS dataset
Compatible — no model change required for the supported columns, given the corrected uncertainty-unit policy below.

---

## 3. Confirmed FITS Inspection Findings

Verified against `C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits` (read-only, outside repo, unchanged) using Astropy 7.2.0.

### 3.1 HDU structure
| HDU | Type | EXTNAME | Rows/Cols | Notes |
|---|---|---|---|---|
| 0 | `PrimaryHDU` | `PRIMARY` | — | 58 cards |
| 1 | `BinTableHDU` | `LIGHTCURVE` | 476 × 20 | Light-curve table |
| 2 | `ImageHDU` | `APERTURE` | 12 × 10 | Aperture mask |

### 3.2 LIGHTCURVE columns (verified)
| # | Column | Format | dtype (stored) | Unit (TUNIT) | 2.2.2 role |
|---|---|---|---|---|---|
| 1 | `TIME` | D | `>f8` | `BJD - 2454833` | **Required** (time) |
| 2 | `TIMECORR` | E | `>f4` | `d` | Unsupported |
| 3 | `CADENCENO` | J | `>i4` | — | **Optional** (cadence) |
| 4 | `SAP_FLUX` | E | `>f4` | `e-/s` | **Required flux** (≥1 of SAP/PDCSAP) |
| 5 | `SAP_FLUX_ERR` | E | `>f4` | `e-/s` | **Optional** uncertainty for SAP_FLUX |
| 6 | `SAP_BKG` | E | `>f4` | `e-/s` | Unsupported |
| 7 | `SAP_BKG_ERR` | E | `>f4` | `e-/s` | Unsupported |
| 8 | `PDCSAP_FLUX` | E | `>f4` | `e-/s` | **Required flux** (≥1 of SAP/PDCSAP) |
| 9 | `PDCSAP_FLUX_ERR` | E | `>f4` | `e-/s` | **Optional** uncertainty for PDCSAP_FLUX |
| 10 | `SAP_QUALITY` | J | `>i4` | — | **Optional** quality flags |
| 11–20 | centroid/position (+ errors) | D/E | mixed | pixel/pixels | Unsupported |

### 3.3 Data values (verified)
| Column | Non-finite | Min | Max | Notes |
|---|---|---|---|---|
| `TIME` | 0 | 120.53914651 | 130.24539528 | All finite |
| `CADENCENO` | N/A (int) | 568 | 1043 | Consecutive |
| `SAP_FLUX` | 4 (NaN) | 532355.0 | 532944.06 | Preserved as-is |
| `SAP_FLUX_ERR` | 4 (NaN) | ~20.04 | ~20.05 | Same 4 rows as SAP_FLUX |
| `PDCSAP_FLUX` | 7 (NaN) | 501346.12 | 501746.75 | Preserved as-is |
| `PDCSAP_FLUX_ERR` | 7 (NaN) | ~20.57 | ~20.77 | Same 7 rows as PDCSAP_FLUX |
| `SAP_QUALITY` | N/A (int) | — | — | 37 nonzero; `{64, 128, 8192, 8320, 12352, 32800}` |
| `PSF_CENTR1` | 476 (all NaN) | — | — | Unsupported column |

No TNULL null sentinels present in this file; missing float values are NaN.

### 3.4 Header metadata (verified)
**Primary:** `TELESCOP=Kepler`, `INSTRUME=Kepler Photometer`, `OBJECT=KIC 11904151`, `KEPLERID=11904151`, `ORIGIN=NASA/Ames`, `MISSION=Kepler`, `QUARTER=0`, `OBSMODE=long cadence`, `DATE=2015-08-26`.

**LIGHTCURVE extension (`INHERIT=True`):** `TIMEREF=SOLARSYSTEM`, `TASSIGN=SPACECRAFT`, `TIMESYS=TDB`, `BJDREFI=2454833`, `BJDREFF=0.0`, `TIMEUNIT=d`, `TSTART=120.52892942`, `TSTOP=130.25561236`, `TIMEDEL=0.02043359821692`, `EXPOSURE=8.95472397`, `DATE-OBS`, `DATE-END`, PDC keywords.

### 3.5 Time convention (verified)
Values are `BJD − 2454833` (BKJD-style), days (`TIMEUNIT=d`), time system `TDB`, reference frame `SOLARSYSTEM`, `BJDREFI=2454833`, `BJDREFF=0`. **Not ordinary Julian Date.** No conversion.

---

## 4. Proposed Importer Module and Public Interface

### 4.1 Module path
`src/fits_importer.py` — new module alongside `src/light_curve.py`. Single module initially.

### 4.2 Dependencies
`astropy.io.fits` (approved, DEC-006), `numpy` (approved), `src.light_curve` (reused model). Standard library only otherwise. **No new dependencies.** No PySide6, no project/service/repository imports.

### 4.3 Public interface
**Successful import:** return a constructed `LightCurveDataset`. Non-fatal validation findings stored in `dataset.validation` (warnings/info). **No separate result dataclass.**

**Failed import:** raise `FITSImportError` with meaningful explanation. No partially populated dataset returned.

```python
class FITSImportError(Exception):
    """Raised when a file-level condition prevents FITS light-curve import."""

def import_light_curve(file_path: str | os.PathLike[str]) -> LightCurveDataset:
    """Read a FITS light-curve file and return a LightCurveDataset.

    Raises FITSImportError for file access, FITS parsing, missing/unsuitable
    table structure, missing required columns, incompatible data types, empty
    tables, mismatched flux/uncertainty units, integer TNULL sentinels in data,
    or model-construction failures. Non-fatal scientific conditions are reported
    via the returned dataset's ValidationReport.
    """
```

### 4.4 Failure categories distinguished
1. File access failures (missing, unreadable, permission).
2. FITS parsing failures (corrupted, invalid structure).
3. Missing/unusable light-curve structure (no table with TIME + flux column).
4. Missing required columns (`TIME`, or neither `SAP_FLUX` nor `PDCSAP_FLUX`).
5. Incompatible data types (non-numeric where numeric required).
6. Mismatched flux/uncertainty units (§5).
7. Integer `TNULL` sentinel present in data (§6).
8. Structural model-construction failures (`LightCurveValidationError` re-raised as `FITSImportError` with context).

### 4.5 Exception context
Exceptions chain the underlying cause (`raise FITSImportError(...) from exc`); user-facing message meaningful without leaking implementation details. No GUI error handling.

---

## 5. Measurement Units and Uncertainty-Unit Policy (Correction 1)

### 5.1 Model representation constraint
`MeasurementColumn` has exactly one `unit` field shared by its measurement values and optional uncertainty values. There is **no separate uncertainty-unit field**, and the model is not extended without explicit approval.

### 5.2 Required uncertainty-unit behavior
For each supported flux/uncertainty pair (`SAP_FLUX`/`SAP_FLUX_ERR`, `PDCSAP_FLUX`/`PDCSAP_FLUX_ERR`), the importer applies this policy:

| Flux unit (`TUNITn`) | Uncertainty unit (`TUNITn`) | Required behavior |
|---|---|---|
| Present | Present and identical | Import normally |
| Absent or blank | Absent or blank | Import with `unit=""` |
| Present | Absent or blank | Raise `FITSImportError` |
| Absent or blank | Present | Raise `FITSImportError` |
| Present | Present but different | Raise `FITSImportError` |

### 5.3 Rationale
The importer must not silently assume that a missing uncertainty unit matches the flux unit, because the model has no way to record distinct units. It must not discard uncertainty data to bypass a mismatch. Raising `FITSImportError` preserves the caller's ability to decide how to proceed.

### 5.4 No hardcoding; unknown units preserved
Units are never hardcoded based on the Kepler example. Any `TUNITn` absent or blank → `""` (unknown) per model convention.

---

## 6. Preserve Original Unit Strings (Correction 2)

### 6.1 Unit-string preservation
- If a `TUNITn` value is present and non-empty, store its **original string** in the corresponding model unit field.
- Do not replace unfamiliar or unrecognized unit strings with `""`.
- Do not perform unit conversion.
- Do not require the importer to recognize every possible unit.
- Use `""` only when the relevant unit metadata is absent or blank.

### 6.2 Application to flux/uncertainty columns
- `SAP_FLUX.unit` ← original `TUNIT4` string if present and non-empty, else `""`.
- `PDCSAP_FLUX.unit` ← original `TUNIT8` string if present and non-empty, else `""`.
- `SAP_FLUX.uncertainties` unit ← original `TUNIT5` string if present and non-empty, else `""` (subject to the mismatch policy in §5.2).
- `PDCSAP_FLUX.uncertainties` unit ← original `TUNIT9` string if present and non-empty, else `""` (subject to the mismatch policy in §5.2).

### 6.3 Application to time metadata
- `TimeInfo.unit` ← original `TIMEUNIT` string if present and non-empty, else `""`.
- `TimeInfo.reference` ← original descriptive convention text from table `TUNIT1` if present and non-empty (e.g. `BJD - 2454833`), else `""`. This is descriptive time-convention metadata, not a physical unit.
- `TimeInfo.time_scale` ← original `TIMESYS` string if present and non-empty, else `""`.
- `TimeInfo.time_reference_frame` ← original `TIMEREF` string if present and non-empty, else `""`.
- `TimeInfo.reference_value` ← numeric `BJDREFI` (+ `BJDREFF`) if present, else `None`.

### 6.4 No conflation
- `TIMEUNIT` remains the source of `TimeInfo.unit`; the descriptive `TUNIT1` convention is **not** conflated with it.
- No unit conversion is performed; original time values are copied unchanged; no BKJD→JD conversion.

---

## 7. FITS Header Inheritance versus Application Fallback (Correction 3)

### 7.1 Terminology distinction
The plan distinguishes precisely between:

- **FITS header inheritance:** behavior defined by FITS conventions and the `INHERIT` keyword on an extension HDU. The importer observes `INHERIT=True` as file content but does **not** rely on automatic in-memory merging of primary-header keywords into the extension header by Astropy.
- **Application-level fallback:** the importer's explicitly documented decision to consult the primary header when a value is absent from the selected extension header. This is an importer policy, independent of whether FITS header inheritance is enabled.

### 7.2 Explicit dual-header read
The importer reads **both** the primary header (`hdul[0].header`) and the extension header (`hdul[1].header`) explicitly. It does not assume Astropy automatically merges inherited primary-header keywords into the extension header.

### 7.3 Application-level fallback policy (not FITS inheritance)
- **Extension-specific time metadata** (`TIMEUNIT`, `TIMESYS`, `TIMEREF`, `BJDREFI`, `BJDREFF`, `TSTART`/`TSTOP`): extension header is authoritative. If absent from the extension, the value is unknown (`""`/`None`) — no silent primary fallback.
- **Source metadata** (`mission`, `instrument`, `target_object`, `source_id`): primary header preferred (`MISSION`, `INSTRUME`, `OBJECT`, `KEPLERID`); if absent from primary, the extension header may be consulted as a **documented application-level fallback**. This fallback is an importer policy, **not** automatic FITS inheritance, and is independent of the `INHERIT` keyword.

### 7.4 Conflicting values
If primary and extension declare conflicting values for the same metadata class, the source preferred for that metadata class per §7.3 wins; the conflict is noted in `dataset.validation.info` or `dataset.notes` so the distinction is visible, not silently resolved.

### 7.5 Verified vs unknown metadata
Metadata present and readable → stored as verified (original string preserved per §6). Metadata absent, blank, or unreadable → field left unknown (`""`/`None`); never fabricated.

---

## 8. Time Metadata (Correction 2, reinforced)

| Model field | Source | Meaning | Verified Kepler value |
|---|---|---|---|
| `TimeInfo.unit` | `TIMEUNIT` (extension header) | Physical unit of numeric time values | `"d"` |
| `TimeInfo.reference` | Table `TUNIT1` (descriptive convention text) | Time reference/convention, not a physical unit | `"BJD - 2454833 (BKJD)"` |
| `TimeInfo.time_scale` | `TIMESYS` (extension header) | Time scale | `"TDB"` |
| `TimeInfo.time_reference_frame` | `TIMEREF` (extension header) | Reference frame | `"SOLARSYSTEM"` |
| `TimeInfo.reference_value` | `BJDREFI` (+ `BJDREFF`) (extension header) | Numeric reference offset | `2454833.0` |
| `TimeInfo.start` | `TSTART` (extension header) | Observation start | `120.52892942` |
| `TimeInfo.stop` | `TSTOP` (extension header) | Observation stop | `130.25561236` |
| `TimeInfo.resolution` | `TIMEDEL` (extension header) | Time resolution | `0.02043359821692` only if meaning/units verified, else `None` |

Original time values copied unchanged (float64); **no BKJD→JD conversion**, no relabeling as JD, no timestamp modification. Missing values preserved as `""`/`None`, never inferred.

---

## 9. HDU Identification and Selection (unchanged, retained)

1. Open `fits.open(path, mode="readonly")` inside a `with` block (guaranteed close on success and failure).
2. Iterate all HDUs; structural candidates = table HDUs whose column names include `TIME` and at least one of `SAP_FLUX` / `PDCSAP_FLUX`.
3. Preferred `EXTNAME=LIGHTCURVE`: a candidate whose `EXTNAME == "LIGHTCURVE"` is preferred **only if it itself satisfies the structural requirements**.
4. An unsuitable `LIGHTCURVE`-named HDU **must not** override a structurally valid candidate. If the HDU named `LIGHTCURVE` lacks `TIME` or both flux columns, it is skipped.
5. Multiple structural candidates → deterministic tie-break (first in HDU order) + informational finding about ambiguity. Ambiguity does not prevent import when a reasonable choice exists.
6. No candidate → `FITSImportError`.
All array copies made **inside** the `with` block before close.

---

## 10. Numeric Dtype Rules (unchanged, retained)

| Array group | Columns | Stored FITS dtype | Conversion rule | Model dtype |
|---|---|---|---|---|
| Floating-point scientific measurements | `TIME`, `SAP_FLUX`, `PDCSAP_FLUX`, `SAP_FLUX_ERR`, `PDCSAP_FLUX_ERR` | `>f8`, `>f4` | Convert to `np.float64` via `np.array(..., dtype=np.float64, copy=True)`. Endianness handled by NumPy. Non-finite preserved. | `float64` |
| Integer-valued identifiers/flags | `CADENCENO`, `SAP_QUALITY` | `>i4` | Convert to `np.int64` via `np.array(..., dtype=np.int64, copy=True)`. No float-to-integer truncation — read as integers directly. | `int64` |

Incompatible types (e.g., string/object where numeric expected) → `FITSImportError`. No silent coercion. No universal type-conversion framework.

---

## 11. Integer FITS TNULL Policy (unchanged, retained)

### 11.1 How Astropy exposes null values (verified by read-only test)
- **Float columns** (`D`/`E`): Astropy does **not** permit `TNULL`. Missing float values are ordinary `NaN`.
- **Integer columns** (`J`): Astropy permits `TNULL`, exposed via `Column.null`. Read via `hdul[1].data` the raw sentinel integer is preserved as a plain integer — **not masked**.

### 11.2 Policy
For each supported integer column (`SAP_QUALITY`, `CADENCENO`):
1. Inspect `Column.null` to determine whether a sentinel is declared.
2. If no sentinel declared → import normally.
3. If sentinel declared but no data value equals it → import normally.
4. If **any** data value equals the declared sentinel → raise `FITSImportError`, because the model cannot represent per-row missing integer values (`quality_flags`/`cadence_numbers` are plain `np.ndarray \| None` with `None` meaning whole column absent).

### 11.3 Preservation rules
A known missing sentinel is **not** preserved as an ordinary quality flag or cadence number. Model unchanged.

---

## 12. Measurement and Metadata Mapping

### 12.1 Required / optional / unsupported table columns

| FITS column | Role | Required for construction? | Model target | Absent behavior |
|---|---|---|---|---|
| `TIME` | timestamps | **Yes** | `TimeInfo.values` (+ metadata) | `FITSImportError` |
| `SAP_FLUX` | SAP flux | At least one of SAP/PDCSAP | `MeasurementColumn("SAP_FLUX")` | — |
| `PDCSAP_FLUX` | PDC flux | At least one of SAP/PDCSAP | `MeasurementColumn("PDCSAP_FLUX")` | — |
| `SAP_FLUX_ERR` | SAP uncertainty | Optional | `SAP_FLUX.uncertainties` | `None`, warning |
| `PDCSAP_FLUX_ERR` | PDC uncertainty | Optional | `PDCSAP_FLUX.uncertainties` | `None`, warning |
| `SAP_QUALITY` | quality flags | Optional | `quality_flags` (int64) | `None` |
| `CADENCENO` | cadence ids | Optional | `cadence_numbers` (int64) | `None` |
| Other columns | — | No | Not imported | possibly noted in `notes` |

SAP and PDCSAP remain independent columns, each paired with its own `*_FLUX_ERR`. Never merged. Never one silently discarded.

### 12.2 Source metadata mapping

| `DatasetSource` field | Proposed source | Notes |
|---|---|---|
| `mission` | `MISSION` header | Leave `None` if absent |
| `instrument` | `INSTRUME` header | Leave `None` if absent |
| `target_object` | `OBJECT` header | Leave `None` if absent |
| `source_id` | `KEPLERID` (target ID) | Distinct from product/file ID; `None` if absent |
| `archive` | `None` | **Not** `ORIGIN` unless supplying archive independently established |
| `original_filename` | Actual input filename | |
| `original_file_path` | Actual input path | |

`ORIGIN=NASA/Ames` may be retained in `notes` or an informational finding, but **must not** automatically be described as the archive. Do not invent source metadata; absent/ambiguous → field unknown.

### 12.3 Dataset naming
- `LightCurveDataset.name` = input filename stem (e.g. `kplr011904151-2009131105131_llc_full`).
- Full original filename in `DatasetSource.original_filename`; full path in `original_file_path`.
- Do not invent a target name or scientific label when the filename is the only reliable identifier.
- Empty/unusable stem → `FITSImportError` rather than silently inventing a name.

### 12.4 Metadata not representable by current model
Raw FITS `TTYPE`/`TFORM`/`TDISP`/`NULL` per column, full header card list, aperture image (HDU2), PDC config keywords. Not important enough to require a model change for 2.2.2; may go in `LightCurveDataset.notes` or remain out of scope. Any model-field addition is a 2.2.1-scope decision requiring approval.

---

## 13. Complete Validation Matrix

Classifications: **Error** = `FITSImportError` raised, no dataset constructed. **Warning** = import succeeds, finding in `dataset.validation.warnings`, data preserved. **Info** = import succeeds, finding in `dataset.validation.info`, data preserved.

| # | Condition | Succeeds? | Finding | Data preserved? | Raises `FITSImportError`? | User approval? |
|---|------|---|---|---|---|---|
| F1 | Missing / unreadable file | No | — | N/A | Yes | No |
| F2 | Corrupted / invalid FITS structure | No | — | N/A | Yes | No |
| F3 | No table HDU with TIME + flux column | No | — | N/A | Yes | No |
| F4 | Multiple candidate tables, no reasonable choice | No | — | N/A | Yes | No |
| F5 | Multiple candidate tables, reasonable choice | Yes | Info (ambiguity) | Yes | No | No |
| C1 | `TIME` column absent | No | — | N/A | Yes | No |
| C2 | Neither `SAP_FLUX` nor `PDCSAP_FLUX` present | No | — | N/A | Yes | No |
| C3 | Only SAP or only PDCSAP available | Yes | Info (single flux series) | Yes | No | No |
| C4 | Flux present, matching `*_FLUX_ERR` absent | Yes | Warning (missing uncertainty) | Yes, `uncertainties=None` | No | No |
| C5 | `*_FLUX_ERR` present but its flux absent | Yes | Warning/info (orphan ignored) | Yes, orphan not imported | No | No |
| C6 | `SAP_QUALITY` / `CADENCENO` absent | Yes | Optional → `None` | Yes | No | No |
| C7 | Extra unsupported numeric columns | Yes | Not imported (possibly info) | Yes | No | No |
| C8 | Unexpected/incompatible dtype (non-numeric where numeric required) | No | — | N/A | Yes | No |
| C9 | Array length ≠ time length | No | — | N/A | Yes (via model `LightCurveValidationError`) | No |
| M1 | Non-numeric timestamp | No | — | N/A | Yes | No |
| M2 | Non-finite timestamp (NaN/inf) | Yes | Warning | Yes, preserved | No | No |
| M3 | Non-finite flux (NaN/inf) | Yes | Warning (`n_nonfinite` + zero-based row indices) | Yes, preserved | No | No |
| M4 | Non-finite uncertainty | Yes | Warning | Yes, preserved | No | No |
| M5 | Negative uncertainty | Yes | Warning | Yes, preserved (not replaced) | No | No |
| M6 | Duplicate timestamps | Yes | Warning | Yes, preserved (not reordered) | No | No |
| M7 | Non-monotonic timestamps | Yes | Warning | Yes, preserved (order kept) | No | No |
| Q1 | Nonzero quality flags present | Yes | Info (count + zero-based row indices) | Yes, preserved | No | No |
| Q2 | Quality-bitmask filtering requested | N/A | Not performed in 2.2.2 | — | No | **Yes** (future policy) |
| T1 | Missing time unit | Yes | Info | Yes, `unit=""` | No | No |
| T2 | Missing time reference/scale/frame | Yes | Info | Yes, empty/`None` | No | No |
| T3 | Missing flux unit | Yes | Info | Yes, `unit=""` | No | No |
| U1 | Flux unit ≠ uncertainty unit per §5.2 table | No | — | N/A | Yes | No |
| N1 | Integer `TNULL` sentinel present in `SAP_QUALITY`/`CADENCENO` data | No | — | N/A | Yes | No |
| E1 | Empty table (zero observations) | No | — | N/A | Yes | No |
| D1 | Duplicate/conflicting supported column names | No | — | N/A | Yes | No |

**Scientific reasoning (§5.1, §5.6):** non-finite and questionable measurements preserved, never removed/replaced/zero-filled (§5.1.4, §5.6.1 acceptance 3). Quality flags never auto-filtered (§3.4.10; REVIEW-002 justification). File-level failures are exceptions, not `ValidationReport` errors (no dataset exists to attach to — §5.6.7).

---

## 14. Error-Handling Strategy

- Single exception type: `FITSImportError` (subclass of `Exception`), meaningful user-facing message, chained underlying cause (`from exc`).
- Success path: return `LightCurveDataset`; warnings/infos live in `dataset.validation`.
- Failure path: raise `FITSImportError`; no partially populated dataset returned.
- `LightCurveValidationError` from model construction caught and re-raised as `FITSImportError` with context.
- Zero-based `row_indices` in every `ValidationFinding`.
- No GUI error handling; no file-selection dialogs; caller decides presentation.

---

## 15. Data-Integrity and Resource-Management Approach

- Open read-only (`mode="readonly"`); never open for write.
- All array copies made **inside** the `with fits.open(...)` block before close.
- Convert big-endian FITS dtypes to native float64/int64 via `np.array(..., dtype=..., copy=True)`; float32→float64 value-preserving.
- Non-finite values preserved (no fill/replace/interpolate).
- Quality flags preserved (no filtering).
- Distinct columns remain distinct (SAP ≠ PDCSAP).
- No observations silently discarded (observation count preserved).
- No units or timestamps silently changed (no BKJD→JD conversion).
- Original unit strings preserved per §6; no unit conversion.
- No normalization/detrending/filtering.
- Model's `_copy_arrays` provides a second authoritative safety copy.
- Original FITS file bytes/checksum unchanged; file remains outside repo and unmodified.

---

## 16. Focused 2.2.2 Automated Testing Plan

Tests in a new module (`tests/test_fits_importer.py`), fixtures under pytest `tmp_path` — **no dependence on external Kepler dataset or absolute Windows paths.** Portable suite passes on any machine.

### 16.1 Temporary FITS fixtures
- Valid Kepler-like multi-HDU table (Primary + LIGHTCURVE at index 1 + APERTURE).
- Light-curve table at a different HDU index.
- Structural table identification (by TIME + flux column, not position).
- Multiple candidate tables (deterministic tie-break + info finding).
- Unsuitable HDU named `LIGHTCURVE` lacking TIME/flux; structurally valid candidate elsewhere wins.
- Missing `TIME` column → `FITSImportError`; missing both flux columns → `FITSImportError`.
- Only `SAP_FLUX`; only `PDCSAP_FLUX`.
- Correct uncertainty pairing (SAP↔SAP_ERR, PDCSAP↔PDCSAP_ERR).
- Missing uncertainty column(s) → `uncertainties=None` + warning.
- Missing optional quality/cadence columns → `None`.
- Supported numeric dtypes and endianness (`>f4`, `>f8`, `>i4` → float64/int64).
- Rejection of incompatible string/object types → `FITSImportError`.
- Preservation of NaN/inf in flux and uncertainty.
- Negative uncertainty → warning, preserved.
- Duplicate / non-monotonic timestamps → warning, preserved, not reordered.
- Missing metadata (no time unit, no mission) → info / `None` fields.
- Duplicate/conflicting supported column names → `FITSImportError`.
- Flux unit present but uncertainty unit absent → `FITSImportError` (§5.2).
- Flux unit absent but uncertainty unit present → `FITSImportError` (§5.2).
- Flux unit present, uncertainty unit present but different → `FITSImportError` (§5.2).
- Original unit strings preserved in model fields (§6).
- Empty table (zero observations) → `FITSImportError`.
- Corrupted / truncated / unreadable file → `FITSImportError`.
- Integer `TNULL` sentinel declared but unused → import normally; sentinel present in data → `FITSImportError` (§11).
- Successful dataset construction and model compatibility (`to_dict()`/`from_dict()` round-trip).
- Arrays usable after FITS closure (independent of open handle).
- Preservation of observation count and original data values.
- Zero-based validation row indices.

### 16.2 Fixture assumptions corrected
A normal FITS binary table has a shared row structure; columns do **not** have independently mismatched lengths. Model-level array-alignment testing remains in `tests/test_light_curve.py` (already covered there). Do not invent malformed FITS cases merely to increase test count.

### 16.3 Resource-safety testing
- Assert returned arrays remain usable after the FITS file has closed.
- Assert returned arrays do not depend on an open FITS file handle.
- Assert imported data remains intact after close.

### 16.4 Model-only tests
Stay in `tests/test_light_curve.py`; not duplicated in importer tests.

### 16.5 Baseline
Existing 224 tests must continue to pass with no regressions.

---

## 17. Optional Real-Data Verification

Gated on the actual Kepler file being present. Skipped if absent — never makes the portable suite dependent on it.

Verify:
- HDU identified as LIGHTCURVE (index 1 structurally, not hardcoded).
- 476 rows; TIME range 120.5391–130.2454; unit `d`, scale `TDB`, reference `BJD - 2454833`, frame `SOLARSYSTEM`.
- SAP_FLUX and PDCSAP_FLUX both present and distinct; 4 and 7 non-finite respectively.
- Uncertainties paired correctly; same non-finite rows per column.
- `SAP_QUALITY` 37 nonzero preserved; `CADENCENO` 568–1043 consecutive.
- `DatasetSource.original_file_path`/`original_filename` set; mission/instrument/target_object/source_id correct.
- `name` = filename stem.
- Valid `LightCurveDataset` constructed; `to_dict()`/`from_dict()` round-trip.
- Original file checksum unchanged before/after import.

---

## 18. Documentation Impact Assessment

Per `AGENTS.md`, documentation updates are required during Build mode. No documents modified now.

### 18.1 2.2.2 implementation documentation (to update during Build)
- Record `src/fits_importer.py` module and responsibilities.
- Record public interface (`import_light_curve`, `FITSImportError`) and error behavior.
- Record supported FITS structure and column/metadata mapping (including units, time metadata, null handling).
- Record validation behavior, classifications, and limitations.
- Record focused test coverage and results.
- Update `docs/MASTER_DEVELOPMENT_ROADMAP.md` (2.2.2 status) and `docs/development/DEVELOPMENT_LOG.md` (implementation record, test results).

### 18.2 2.2.4 consolidation (future)
- Broader documentation reconciliation across subtasks; cross-subtask completion status; overall Stage 2.2 verification; remaining deferred/unresolved items.

Foundation documents remain read-only. `docs/README.md` unchanged unless a significant document is added/renamed. Existing project-lifecycle docs unchanged.

---

## 19. Explicit Subtask Boundaries

| Subtask | Responsibility | In 2.2.2? |
|---|---|---|
| 2.2.1 | Light-curve data model — done | No (reused only) |
| 2.2.2 | FITS reading, HDU identification, extraction, metadata, validation, `LightCurveDataset` construction, importer tests | **Yes — current** |
| 2.2.3 | Project association, dataset persistence, save/reopen, project IDs/ownership/permissions | No (future) |
| 2.2.4 | Broader Stage 2.2 verification, documentation reconciliation, completion assessment | No (future) |

**Excluded from 2.2.2:** project association/persistence, visualization, BLS/analysis, quality-bitmask filtering, archive downloads, universal FITS framework, database/permanent storage, GUI dialogs.

---

## 20. Risks and Unresolved Issues

| Risk / Issue | Description | Mitigation / Status |
|---|---|---|
| Memory-mapped FITS arrays | Post-close access fails if not copied. | Copy arrays inside `with` block. |
| Big-endian FITS dtypes | Convert to native float64/int64. | `np.array(..., dtype=..., copy=True)` handles byte swap. |
| Float32 → float64 upcast | Value-preserving, doubles flux memory. | Acceptable at ~476 rows. |
| Model re-copies arrays | Slight redundancy. | Acceptable; correctness > micro-optimization. |
| Real dataset not portable | Automated suite must not depend on absolute path. | Gate real-data test on file presence; `tmp_path` fixtures. |
| Validation vs exception boundary | Risk of putting import failures into nonexistent dataset's `ValidationReport`. | Enforce separation (Section 14). |
| Quality-bitmask pressure | Temptation to auto-filter nonzero flags. | Explicitly excluded; future analysis operation requiring approval. |
| Scope creep | Pressure to add persistence, UI, visualization, BLS. | Explicitly excluded. |
| Flux/uncertainty unit mismatch | Model has no separate uncertainty-unit field. | Raising `FITSImportError` (§5.2) — no model change. |
| Integer `TNULL` sentinel in data | Model cannot represent per-row missing integers. | Raising `FITSImportError` (§11.2) — no model change; Kepler file has no TNULL so does not block initial implementation. |

---

## 21. Recommended Build Implementation Sequence

1. Create `src/fits_importer.py`: `FITSImportError`, `import_light_curve()`, FITS opening/close, structural HDU identification (§9).
2. Implement extraction of `TIME`, `SAP_FLUX`/`PDCSAP_FLUX`, uncertainties, `SAP_QUALITY`, `CADENCENO` (array copies inside `with` block; per-column units from `TUNITn`).
3. Implement unit cross-check (§5.2) and integer `TNULL` policy (§11.2).
4. Implement metadata extraction into `DatasetSource` and `TimeInfo` (BKJD/TDB/SOLARSYSTEM; explicit dual-header resolution per §7; time unit from `TIMEUNIT`, reference from descriptive `TUNIT1` per §6.3; filename-stem naming).
5. Implement validation findings and `ValidationReport`; dataset assembly via `LightCurveDataset` constructor; surface `LightCurveValidationError` as `FITSImportError`.
6. Create focused importer tests with `tmp_path` fixtures (§16); run targeted tests.
7. Optional real-data verification against Kepler file, gated on presence (§17).
8. Run full suite (224+ passing, no regressions).
9. Update documentation per `AGENTS.md` — Build-mode activity (§18).
10. Review completion; hand off to 2.2.3.

Deferred to 2.2.3: project association, persistence, save/reopen. Deferred to 2.2.4: broader integration verification and documentation reconciliation.

---

## 22. Decisions or Questions Requiring User Approval

1. **Approval of this revised plan** before switching to Build mode (the gate itself).
2. No additional decisions require approval. All open points from prior revisions are resolved by explicit policy in this document:
   - Uncertainty-unit mismatch → `FITSImportError` (§5.2), no model extension.
   - Original unit strings preserved; `TIMEUNIT` → `TimeInfo.unit`; descriptive `TUNIT1` → `TimeInfo.reference` (§6), no inference.
   - Integer `TNULL` sentinel in data → `FITSImportError` (§11.2), no model change.
   - Header inheritance vs application fallback distinguished (§7); fallback is importer policy, not automatic FITS inheritance.
   - HDU selection: `LIGHTCURVE` preference only among structurally valid candidates (§9).

---

## Remaining Assumptions or Unresolved Decisions

**No implementation-critical uncertainties remain.** All five correction areas have been resolved by explicit policy:

1. Uncertainty-unit handling — resolved by the §5.2 policy table (`FITSImportError` on mismatch or one-sided presence).
2. Original unit-string preservation — resolved by §6 (store original `TUNITn` text; `""` only when absent/blank; no conversion).
3. Header inheritance vs application fallback — resolved by §7 (explicit dual-header read; application-level fallback documented separately from FITS `INHERIT`; no claim of automatic inheritance).
4. Scope — unchanged (§4, §19); no redesign or expansion.
5. Time unit vs time reference — resolved by §6.3 and §8 (`TIMEUNIT` → `TimeInfo.unit`; descriptive `TUNIT1` → `TimeInfo.reference`; separate fields; no conflation).

The only gate is user approval of this plan before switching to Build mode. No code, tests, or repository changes have been made in this session.

---

**Statement:** Implementation has not started. No files were created, modified, deleted, or renamed in this session; no dependencies installed; no configuration changed; the original FITS file untouched; no Git state altered by me. This revised plan remains in PLAN mode and awaits your explicit review and authorization before any switch to Build mode.

# CHATGPT v5 review

The revised plan is substantially improved. The five correction areas are addressed, and the scope remains appropriately limited to Subtask 2.2.2.

I would not approve BUILD quite yet. There are two remaining inconsistencies and a few test-coverage details to tighten.

## Remaining corrections

### 1. Header access must use the selected HDU, not `hdul[1]`

Section 7.2 currently says:

> The importer reads both the primary header (`hdul[0].header`) and the extension header (`hdul[1].header`) explicitly.

That conflicts with Section 9, which allows the light-curve table to exist at an HDU index other than 1.

The importer must use the header belonging to the structurally selected light-curve HDU, whatever its index.

Required correction:

- Primary header: `hdul[0].header`
- Selected table header: `selected_hdu.header`
- All extension-specific metadata and column metadata must come from the selected table HDU.

This is important because otherwise the importer could identify the correct table but read metadata from the wrong extension.

### 2. Multiple-candidate behavior is inconsistent

Section 9 says multiple valid candidates are resolved deterministically by choosing the first in HDU order, with an informational finding.

However, Section 13 includes:

> F4 — Multiple candidate tables, no reasonable choice → `FITSImportError`.

The plan never defines when a candidate-selection situation becomes unreasonable. Under the current deterministic-first policy, F4 is effectively undefined.

Keep the already-established behavior:

- No valid candidate: `FITSImportError`.
- One valid candidate: select it.
- Multiple valid candidates: prefer a structurally valid `LIGHTCURVE` candidate; otherwise select the first valid candidate in HDU order and record an informational finding.
- If multiple candidates have the same preference, use the first in HDU order.

Remove F4 or redefine it only if there is a specific structural condition that genuinely prevents selection.

### 3. Complete the unit-handling tests

The unit policy is now explicit, but the test plan should cover all permitted and rejected cases.

Make sure tests cover:

- Both flux and uncertainty units present and identical → import.
- Both absent or blank → import with `unit=""`.
- Flux unit present, uncertainty unit absent → reject.
- Flux unit absent, uncertainty unit present → reject.
- Both present but different → reject.
- An unfamiliar but non-empty unit string → preserve the original string.
- Whitespace-only unit metadata → treat as blank.

For nonblank strings, preserve the original text rather than normalizing or rewriting it.

### 4. Specify the orphan uncertainty finding

Section 13, C5 currently says:

> Warning/info (orphan ignored).

Choose one classification. I recommend warning, since the file contains an uncertainty column that cannot be associated with an imported measurement.

The orphan column should not be imported or silently paired with another flux column.

## Final assessment

| Area                             | Assessment                                   |
| -------------------------------- | -------------------------------------------- |
| 2.2.1 model compatibility        | Acceptable based on the reported inspection  |
| FITS structure and HDU selection | Acceptable, with the header-index correction |
| Measurement extraction           | Acceptable                                   |
| Uncertainty pairing and units    | Acceptable, with test additions              |
| Time metadata                    | Acceptable                                   |
| Header inheritance/fallback      | Clear                                        |
| TNULL handling                   | Explicit                                     |
| Data preservation                | Explicit                                     |
| Validation classifications       | Mostly complete                              |
| Automated testing                | Comprehensive, with the additions above      |
| Scope boundaries                 | Clear                                        |
| Documentation obligations        | Appropriate                                  |

Status: Nearly ready for BUILD.

Send Nemotron one final narrow refinement for these points. If it incorporates them without introducing new scope or changing the approved behavior, I would consider the plan ready for your explicit BUILD authorization.

No implementation authorization has been given yet.


# chatgpt v5 revise prompt

# Final PLAN Refinement — Subtask 2.2.2 FITS Importer

**Mode: PLAN ONLY. Do not implement, edit files, create tests, or begin BUILD.**

Revise the current Subtask 2.2.2 implementation plan to address the four remaining review findings below.

These are targeted corrections, not an invitation to redesign the importer. Preserve the existing approved architecture, policies, scope, and implementation sequence unless a correction below requires a direct change.

## 1. Correct extension-header selection

The current plan's Section 7.2 refers to:

`hdul[1].header`

This is incorrect because Section 9 allows the structurally selected light-curve table to exist at any HDU index.

Revise the header-access policy:

- Primary header: `hdul[0].header`
- Light-curve extension header: `selected_hdu.header`, where `selected_hdu` is the HDU chosen by the structural selection procedure in Section 9.
- All extension-specific time metadata must come from the selected table HDU.
- All column-specific metadata, including `TUNITn`, `Column.null`, and other column definitions, must come from the selected table HDU.
- Do not assume the light-curve table is at index 1.
- Keep the existing primary-header versus extension-header application fallback policy unchanged.
- Ensure the implementation sequence and test plan consistently refer to the selected HDU rather than a fixed index.

Add or retain a test where the valid light-curve table is at an HDU index other than 1 and verify that its own header metadata is used.

## 2. Resolve the multiple-candidate inconsistency

Section 9 defines deterministic candidate selection, but Section 13 still contains an undefined condition:

"Multiple candidate tables, no reasonable choice."

The existing policy should be made consistent throughout the document:

1. No structurally valid candidate → `FITSImportError`.
2. Exactly one valid candidate → select it.
3. Multiple valid candidates with one or more structurally valid `EXTNAME=LIGHTCURVE` candidates → prefer a `LIGHTCURVE` candidate.
4. If multiple candidates have the same preference, select the first in HDU order.
5. If multiple valid candidates exist and selection is resolved by this deterministic rule, import successfully and record an informational finding describing the ambiguity and selection.

Remove the undefined "no reasonable choice" failure condition from the validation matrix unless you identify and precisely define a genuine structural condition that prevents selection. Do not invent an additional selection failure mode.

Update the HDU-selection section, validation matrix, tests, and implementation sequence so they all describe the same policy.

## 3. Complete unit-handling test coverage

The uncertainty-unit policy in Section 5.2 is approved. Make sure the automated test plan explicitly covers every branch:

| Flux unit | Uncertainty unit | Expected result |
|---|---|---|
| Present | Present and identical | Import |
| Absent or blank | Absent or blank | Import with `unit=""` |
| Present | Absent or blank | `FITSImportError` |
| Absent or blank | Present | `FITSImportError` |
| Present | Present but different | `FITSImportError` |

Also add explicit tests for:

- An unfamiliar but non-empty unit string: preserve the original string exactly; do not normalize, rewrite, or discard it.
- Whitespace-only unit metadata: treat it as blank.
- The same preservation and blank-handling principles for `TIMEUNIT` and descriptive `TUNIT1` metadata where applicable.

Do not change the approved unit policy. Do not add unit conversion or a unit-recognition framework.

## 4. Define orphan uncertainty handling consistently

Section 13, condition C5 currently allows either a warning or informational finding.

Choose one classification and use it consistently throughout the plan.

Use this policy:

- If `SAP_FLUX_ERR` exists but `SAP_FLUX` does not, ignore the orphan uncertainty column and add a **warning**.
- If `PDCSAP_FLUX_ERR` exists but `PDCSAP_FLUX` does not, ignore the orphan uncertainty column and add a **warning**.
- Never pair an orphan uncertainty column with another flux series.
- Do not treat an orphan uncertainty column as a file-level import failure.

Update the validation matrix and test plan accordingly.

## 5. Final consistency review

After applying the four corrections:

- Review the complete plan for contradictory statements, obsolete wording, and references to fixed HDU index 1.
- Ensure all affected sections agree: header metadata, HDU selection, validation matrix, automated tests, and implementation sequence.
- Preserve all existing scope boundaries:
  - No project association or persistence.
  - No GUI or visualization.
  - No BLS or analysis functionality.
  - No quality-bitmask filtering.
  - No model redesign.
  - No unrelated refactoring.
- Preserve the requirement to update the appropriate non-Foundation documentation during BUILD, consistent with `AGENTS.md`.
- Do not modify Foundation documentation.
- Do not claim new repository inspection, test execution, or verification unless actually performed during this PLAN session.

Return the **complete revised implementation plan**, not merely a change summary.

End with:

1. **Remaining Assumptions or Unresolved Decisions** — list only genuine remaining uncertainties, or explicitly state that none are implementation-critical.
2. **Final Readiness Assessment** — state whether the plan is internally consistent and ready for user approval to enter BUILD mode.

**Stop after presenting the revised plan. Do not begin implementation or make repository changes. Wait for explicit user authorization before BUILD.**

# opencode plan v6

---

# Subtask 2.2.2 — FITS Import and Validation: Final Revised Implementation Plan

**Mode: PLAN ONLY. Do not implement, edit files, create tests, or begin BUILD.**

This report is the final revision of the Subtask 2.2.2 plan, incorporating four targeted corrections: (1) extension-header selection via `selected_hdu.header` rather than fixed index `hdul[1]`, (2) consistent multiple-candidate selection policy removing the undefined "no reasonable choice" condition, (3) complete unit-handling test coverage for all policy branches, and (4) consistent warning classification for orphan uncertainty columns. All previously approved architecture, policies, scope, and implementation sequence are preserved.

---

## 1. Repository State and Preparation

### 1.1 Verified repository facts (current session)

| Item | Verified value |
|---|---|
| Working directory | `C:\Code\New_Project` (git repo, branch `master`) |
| HEAD commit | `113a9ab task 2.2.2 planning begin` — Author: Brett, Date: Wed Nov 4 13:52:42 2026. Pre-existing user commit; not created by me. |
| Previous commit | `f65f14f Task 2.2.1` |
| Working tree vs HEAD | One modified file (not staged): `docs/planning/.../task 2.2.2 FITS import and validation WORKING PROGRESS LOG.md` (+1,119 insertions beyond the commit). Pre-existing user edit; left untouched. |
| Untracked files | None |

### 1.2 Confirmation that Subtask 2.2.1 exists
**Verified in this session.** `src/light_curve.py` and `tests/test_light_curve.py` both exist in the repository.

### 1.3 Current test baseline
`python -m pytest -q` → **224 passed, 0 failed.** Regression baseline for 2.2.2.

### 1.4 Existing user changes / repository-state concerns
The pre-existing planning-file changes (one committed, one modified in working tree) are outside `src/` and `tests/` and predate this task. They will not be touched.

---

## 2. Verified 2.2.1 Model Review

All details from direct inspection of `src/light_curve.py` (493 lines) and `tests/test_light_curve.py` (759 lines) in this session. The model is reused as-is; no redesign.

### 2.1 Model components and interfaces (verified)

| Component | Key fields / behavior |
|---|---|
| `DatasetSource` | `original_filename`, `original_file_path`, `archive`, `source_id`, `mission`, `instrument`, `target_object`, `checksum` — all `str \| None`, default `None`. |
| `TimeInfo` | `values: np.ndarray` (required); `unit`, `reference`, `time_scale`, `time_reference_frame` (str, default `""`); `reference_value`, `start`, `stop`, `resolution`, `format_hint` (float/str, default `None`). Unknown → `""`/`None`; does not block construction. |
| `MeasurementColumn` | `name: str`, `values: np.ndarray`, `unit: str = ""`, `uncertainties: np.ndarray \| None = None`, `description: str \| None = None`. **One `unit` field shared by values and uncertainties; no separate uncertainty-unit field.** Property `n_nonfinite`. Non-finite preserved; `None` uncertainties ≠ zero-array uncertainties. |
| `MeasurementSeries` | `series: dict[str, MeasurementColumn]`; keys must equal `column.name`; no duplicates. |
| `ValidationFinding` | `code`, `message`, `severity`, `column: str \| None`, `row_indices: list[int] \| None` (zero-based). |
| `ValidationReport` | `errors`, `warnings`, `info` lists of `ValidationFinding`. |
| `LightCurveDataset` | `dataset_id` (UUID, auto), `name` (str, required), `source`, `time`, `measurements`, `quality_flags: np.ndarray \| None`, `cadence_numbers: np.ndarray \| None`, `validation`, `imported_at` (auto ISO UTC), `notes: str \| None`. Property `n_observations`. |

### 2.2 Structural validation (`__post_init__`)
Raises `LightCurveValidationError` (subclass of `ValueError`) for invalid `dataset_id`; missing/non-ndarray `time.values`; non-str `time.unit`; non-`MeasurementSeries` measurements; key/name mismatch; duplicate names; non-ndarray column values/unit/uncertainties; array length mismatches vs. time; non-`ValidationReport` validation; non-str `imported_at`.

### 2.3 Array copying and ownership
`_copy_arrays` converts `time.values` and each measurement `values`/`uncertainties` to `np.array(..., dtype=np.float64, copy=True)`; `quality_flags`/`cadence_numbers` to `np.array(..., dtype=np.int64, copy=True)`. Model owns independent copies. Importer must still copy FITS memory-mapped arrays **before** closing the file.

### 2.4 Serialization
`to_dict()` → JSON-compatible dict; arrays → `.tolist()`; `None` preserved as `None`. `from_dict(data)` reconstructs and re-validates; distinguishes `None` from arrays.

### 2.5 Compatibility with Kepler FITS dataset
Compatible — no model change required for the supported columns, given the corrected uncertainty-unit policy below.

---

## 3. Confirmed FITS Inspection Findings

Verified against `C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits` (read-only, outside repo, unchanged) using Astropy 7.2.0 (inspected earlier in this session).

### 3.1 HDU structure
| HDU | Type | EXTNAME | Rows/Cols | Notes |
|---|---|---|---|---|
| 0 | `PrimaryHDU` | `PRIMARY` | — | 58 cards |
| 1 | `BinTableHDU` | `LIGHTCURVE` | 476 × 20 | Light-curve table |
| 2 | `ImageHDU` | `APERTURE` | 12 × 10 | Aperture mask |

The table happens to be at index 1 in this file, but the importer must **not** assume index 1; structural selection (Section 5) determines the selected HDU at runtime.

### 3.2 LIGHTCURVE columns (verified)
| # | Column | Format | dtype (stored) | Unit (TUNIT) | 2.2.2 role |
|---|---|---|---|---|---|
| 1 | `TIME` | D | `>f8` | `BJD - 2454833` | **Required** (time) |
| 2 | `TIMECORR` | E | `>f4` | `d` | Unsupported |
| 3 | `CADENCENO` | J | `>i4` | — | **Optional** (cadence) |
| 4 | `SAP_FLUX` | E | `>f4` | `e-/s` | **Required flux** (≥1 of SAP/PDCSAP) |
| 5 | `SAP_FLUX_ERR` | E | `>f4` | `e-/s` | **Optional** uncertainty for SAP_FLUX |
| 6 | `SAP_BKG` | E | `>f4` | `e-/s` | Unsupported |
| 7 | `SAP_BKG_ERR` | E | `>f4` | `e-/s` | Unsupported |
| 8 | `PDCSAP_FLUX` | E | `>f4` | `e-/s` | **Required flux** (≥1 of SAP/PDCSAP) |
| 9 | `PDCSAP_FLUX_ERR` | E | `>f4` | `e-/s` | **Optional** uncertainty for PDCSAP_FLUX |
| 10 | `SAP_QUALITY` | J | `>i4` | — | **Optional** quality flags |
| 11–20 | centroid/position (+ errors) | D/E | mixed | pixel/pixels | Unsupported |

### 3.3 Data values (verified)
| Column | Non-finite | Min | Max | Notes |
|---|---|---|---|---|
| `TIME` | 0 | 120.53914651 | 130.24539528 | All finite |
| `CADENCENO` | N/A (int) | 568 | 1043 | Consecutive |
| `SAP_FLUX` | 4 (NaN) | 532355.0 | 532944.06 | Preserved as-is |
| `SAP_FLUX_ERR` | 4 (NaN) | ~20.04 | ~20.05 | Same 4 rows as SAP_FLUX |
| `PDCSAP_FLUX` | 7 (NaN) | 501346.12 | 501746.75 | Preserved as-is |
| `PDCSAP_FLUX_ERR` | 7 (NaN) | ~20.57 | ~20.77 | Same 7 rows as PDCSAP_FLUX |
| `SAP_QUALITY` | N/A (int) | — | — | 37 nonzero; `{64, 128, 8192, 8320, 12352, 32800}` |
| `PSF_CENTR1` | 476 (all NaN) | — | — | Unsupported column |

No TNULL null sentinels present in this file; missing float values are NaN.

### 3.4 Header metadata (verified)
**Primary:** `TELESCOP=Kepler`, `INSTRUME=Kepler Photometer`, `OBJECT=KIC 11904151`, `KEPLERID=11904151`, `ORIGIN=NASA/Ames`, `MISSION=Kepler`, `QUARTER=0`, `OBSMODE=long cadence`, `DATE=2015-08-26`.

**LIGHTCURVE extension (`INHERIT=True`):** `TIMEREF=SOLARSYSTEM`, `TASSIGN=SPACECRAFT`, `TIMESYS=TDB`, `BJDREFI=2454833`, `BJDREFF=0.0`, `TIMEUNIT=d`, `TSTART=120.52892942`, `TSTOP=130.25561236`, `TIMEDEL=0.02043359821692`, `EXPOSURE=8.95472397`, `DATE-OBS`, `DATE-END`, PDC keywords.

### 3.5 Time convention (verified)
Values are `BJD − 2454833` (BKJD-style), days (`TIMEUNIT=d`), time system `TDB`, reference frame `SOLARSYSTEM`, `BJDREFI=2454833`, `BJDREFF=0`. **Not ordinary Julian Date.** No conversion.

---

## 4. Proposed Importer Module and Public Interface

### 4.1 Module path
`src/fits_importer.py` — new module alongside `src/light_curve.py`. Single module initially.

### 4.2 Dependencies
`astropy.io.fits` (approved, DEC-006), `numpy` (approved), `src.light_curve` (reused model). Standard library only otherwise. **No new dependencies.** No PySide6, no project/service/repository imports.

### 4.3 Public interface
**Successful import:** return a constructed `LightCurveDataset`. Non-fatal validation findings stored in `dataset.validation` (warnings/info). **No separate result dataclass.**

**Failed import:** raise `FITSImportError` with meaningful explanation. No partially populated dataset returned.

```python
class FITSImportError(Exception):
    """Raised when a file-level condition prevents FITS light-curve import."""

def import_light_curve(file_path: str | os.PathLike[str]) -> LightCurveDataset:
    """Read a FITS light-curve file and return a LightCurveDataset.

    Raises FITSImportError for file access, FITS parsing, missing/unsuitable
    table structure, missing required columns, incompatible data types, empty
    tables, mismatched flux/uncertainty units, integer TNULL sentinels in data,
    or model-construction failures. Non-fatal scientific conditions are reported
    via the returned dataset's ValidationReport.
    """
```

### 4.4 Failure categories distinguished
1. File access failures (missing, unreadable, permission).
2. FITS parsing failures (corrupted, invalid structure).
3. Missing/unusable light-curve structure (no table with TIME + flux column).
4. Missing required columns (`TIME`, or neither `SAP_FLUX` nor `PDCSAP_FLUX`).
5. Incompatible data types (non-numeric where numeric required).
6. Mismatched flux/uncertainty units (Section 7).
7. Integer `TNULL` sentinel present in data (Section 12).
8. Structural model-construction failures (`LightCurveValidationError` re-raised as `FITSImportError` with context).

### 4.5 Exception context
Exceptions chain the underlying cause (`raise FITSImportError(...) from exc`); user-facing message meaningful without leaking implementation details. No GUI error handling.

---

## 5. HDU Identification and Selection (Corrected — any index)

1. Open `fits.open(path, mode="readonly")` inside a `with` block (guaranteed close on success and failure).
2. Iterate **all** HDUs; structural candidates = table HDUs (`BinTableHDU`/`TableHDU`) whose column names include `TIME` and at least one of `SAP_FLUX` / `PDCSAP_FLUX`.
3. Apply the multiple-candidate selection policy (Section 6) to choose exactly one `selected_hdu` from among the structural candidates.
4. If no structural candidate exists → `FITSImportError` (no usable light-curve table).
5. All array copies are made **inside** the `with` block before close (memory-mapped data).
6. The light-curve table is **not** assumed to be at index 1. The selected HDU may be at any index.
7. After selection, all extension-specific metadata is read from `selected_hdu.header` (Section 6), and all column-specific metadata from `selected_hdu.columns` (Section 7).

---

## 6. Header Metadata Selection (Corrected — `selected_hdu.header`, not `hdul[1]`)

### 6.1 Explicit header sources
- **Primary header:** `hdul[0].header` — source for mission/instrument/target/source metadata (`MISSION`, `INSTRUME`, `OBJECT`, `KEPLERID`, `ORIGIN`).
- **Light-curve extension header:** `selected_hdu.header` — where `selected_hdu` is the HDU chosen by the structural selection procedure in Section 5. Source for all extension-specific time metadata (`TIMEUNIT`, `TIMESYS`, `TIMEREF`, `BJDREFI`, `BJDREFF`, `TSTART`/`TSTOP`, `TIMEDEL`, `EXPOSURE`, etc.).
- **Column-specific metadata:** from `selected_hdu.columns` — `TUNITn`, `Column.null`, TTYPE, TFORM, TDISP, etc., for each column of the selected table HDU.

### 6.2 No fixed-index assumption
The importer does **not** assume the light-curve table is at index 1. `hdul[1].header` is never referenced as the light-curve extension header. All extension metadata flows through `selected_hdu`.

### 6.3 Application fallback policy (unchanged)
The existing primary-header versus extension-header application fallback policy is unchanged:
- Extension-specific time metadata: `selected_hdu.header` is authoritative. If absent, value is unknown (`""`/`None`) — no silent primary fallback for time metadata.
- Source metadata: primary header preferred (`MISSION`, `INSTRUME`, `OBJECT`, `KEPLERID`); if absent from primary, extension header may be consulted as a **documented application-level fallback**. This fallback is an importer policy, **not** automatic FITS inheritance, and is independent of the `INHERIT` keyword.

### 6.4 Conflicting values
If primary and extension declare conflicting values for the same metadata class, the source preferred for that metadata class per Section 9 wins; the conflict is noted in `dataset.validation.info` or `dataset.notes`.

---

## 7. Measurement Units and Uncertainty-Unit Policy

### 7.1 Model representation constraint
`MeasurementColumn` has exactly one `unit` field shared by its measurement values and optional uncertainty values. There is **no separate uncertainty-unit field**, and the model is not extended without explicit approval.

### 7.2 Required uncertainty-unit behavior
For each supported flux/uncertainty pair (`SAP_FLUX`/`SAP_FLUX_ERR`, `PDCSAP_FLUX`/`PDCSAP_FLUX_ERR`), the importer applies this policy:

| Flux unit (`TUNITn`) | Uncertainty unit (`TUNITn`) | Required behavior |
|---|---|---|
| Present | Present and identical | Import normally |
| Absent or blank | Absent or blank | Import with `unit=""` |
| Present | Absent or blank | Raise `FITSImportError` |
| Absent or blank | Present | Raise `FITSImportError` |
| Present | Present but different | Raise `FITSImportError` |

### 7.3 Rationale
The importer must not silently assume that a missing uncertainty unit matches the flux unit, because the model has no way to record distinct units. It must not discard uncertainty data to bypass a mismatch. Raising `FITSImportError` preserves the caller's ability to decide how to proceed.

### 7.4 Unit-string preservation (all unit fields)
- If a `TUNITn` value is present and non-empty, store its **original string** in the corresponding model unit field.
- Do not replace unfamiliar or unrecognized unit strings with `""`.
- Do not perform unit conversion.
- Do not require the importer to recognize every possible unit.
- Use `""` only when the relevant unit metadata is absent or blank.
- Whitespace-only unit metadata is treated as blank.

### 7.5 Application to specific fields
- `SAP_FLUX.unit` ← original `TUNIT4` string if present and non-empty, else `""`.
- `PDCSAP_FLUX.unit` ← original `TUNIT8` string if present and non-empty, else `""`.
- `SAP_FLUX.uncertainties` unit ← original `TUNIT5` string if present and non-empty, else `""` (subject to the mismatch policy in §7.2).
- `PDCSAP_FLUX.uncertainties` unit ← original `TUNIT9` string if present and non-empty, else `""` (subject to the mismatch policy in §7.2).

---

## 8. Time Metadata

| Model field | Source | Meaning | Verified Kepler value |
|---|---|---|---|
| `TimeInfo.unit` | `TIMEUNIT` (`selected_hdu.header`) | Physical unit of numeric time values | `"d"` |
| `TimeInfo.reference` | Table `TUNIT1` (`selected_hdu.columns`) | Time reference/convention text, not a physical unit | `"BJD - 2454833 (BKJD)"` |
| `TimeInfo.time_scale` | `TIMESYS` (`selected_hdu.header`) | Time scale | `"TDB"` |
| `TimeInfo.time_reference_frame` | `TIMEREF` (`selected_hdu.header`) | Reference frame | `"SOLARSYSTEM"` |
| `TimeInfo.reference_value` | `BJDREFI` (+ `BJDREFF`) (`selected_hdu.header`) | Numeric reference offset | `2454833.0` |
| `TimeInfo.start` | `TSTART` (`selected_hdu.header`) | Observation start | `120.52892942` |
| `TimeInfo.stop` | `TSTOP` (`selected_hdu.header`) | Observation stop | `130.25561236` |
| `TimeInfo.resolution` | `TIMEDEL` (`selected_hdu.header`) | Time resolution | `0.02043359821692` only if meaning/units verified, else `None` |

- `TIMEUNIT` remains the source of `TimeInfo.unit`; the descriptive `TUNIT1` convention is **not** conflated with it.
- No unit conversion is performed; original time values are copied unchanged; no BKJD→JD conversion.
- Missing values preserved as `""`/`None`, never inferred.

---

## 9. Header Inheritance versus Application Fallback (Terminology)

### 9.1 Precise distinction
- **FITS header inheritance:** behavior defined by FITS conventions and the `INHERIT` keyword on an extension HDU. The importer observes `INHERIT=True` as file content but does **not** rely on automatic in-memory merging of primary-header keywords into the extension header by Astropy.
- **Application-level fallback:** the importer's explicitly documented decision to consult the primary header when a value is absent from the selected extension header. This is an importer policy, independent of whether FITS header inheritance is enabled.

### 9.2 Wording requirement
Do not describe application-level fallback as "eligible for FITS inheritance" or as automatic FITS inheritance. Use "application-level fallback" or "importer fallback policy" consistently.

---

## 10. Numeric Dtype Rules

| Array group | Columns | Stored FITS dtype | Conversion rule | Model dtype |
|---|---|---|---|---|
| Floating-point scientific measurements | `TIME`, `SAP_FLUX`, `PDCSAP_FLUX`, `SAP_FLUX_ERR`, `PDCSAP_FLUX_ERR` | `>f8`, `>f4` | Convert to `np.float64` via `np.array(..., dtype=np.float64, copy=True)`. Endianness handled by NumPy. Non-finite preserved. | `float64` |
| Integer-valued identifiers/flags | `CADENCENO`, `SAP_QUALITY` | `>i4` | Convert to `np.int64` via `np.array(..., dtype=np.int64, copy=True)`. No float-to-integer truncation — read as integers directly. | `int64` |

Incompatible types (e.g., string/object where numeric expected) → `FITSImportError`. No silent coercion. No universal type-conversion framework.

---

## 11. Integer FITS TNULL Policy

### 11.1 How Astropy exposes null values (verified by read-only test earlier in this session)
- **Float columns** (`D`/`E`): Astropy does **not** permit `TNULL`. Missing float values are ordinary `NaN`.
- **Integer columns** (`J`): Astropy permits `TNULL`, exposed via `Column.null`. Read via `hdul[1].data` the raw sentinel integer is preserved as a plain integer — **not masked**.

### 11.2 Policy
For each supported integer column (`SAP_QUALITY`, `CADENCENO`) of `selected_hdu`:
1. Inspect `Column.null` to determine whether a sentinel is declared.
2. If no sentinel declared → import normally.
3. If sentinel declared but no data value equals it → import normally.
4. If **any** data value equals the declared sentinel → raise `FITSImportError`, because the model cannot represent per-row missing integer values (`quality_flags`/`cadence_numbers` are plain `np.ndarray \| None` with `None` meaning whole column absent).

### 11.3 Preservation rules
A known missing sentinel is **not** preserved as an ordinary quality flag or cadence number. Model unchanged.

---

## 12. Orphan Uncertainty Handling (Corrected — consistent warning classification)

### 12.1 Policy
- If `SAP_FLUX_ERR` exists but `SAP_FLUX` does not, ignore the orphan uncertainty column and add a **warning**.
- If `PDCSAP_FLUX_ERR` exists but `PDCSAP_FLUX` does not, ignore the orphan uncertainty column and add a **warning**.
- Never pair an orphan uncertainty column with another flux series.
- Do not treat an orphan uncertainty column as a file-level import failure.

### 12.2 Consistency
The classification **warning** is used consistently throughout the validation matrix (§13), test plan (§17), and implementation sequence (§22). No other classification (info, error) is used for orphan uncertainties anywhere in this plan.

---

## 13. Measurement and Metadata Mapping

### 12.1 Required / optional / unsupported table columns

| FITS column | Role | Required for construction? | Model target | Absent behavior |
|---|---|---|---|---|
| `TIME` | timestamps | **Yes** | `TimeInfo.values` (+ metadata) | `FITSImportError` |
| `SAP_FLUX` | SAP flux | At least one of SAP/PDCSAP | `MeasurementColumn("SAP_FLUX")` | — |
| `PDCSAP_FLUX` | PDC flux | At least one of SAP/PDCSAP | `MeasurementColumn("PDCSAP_FLUX")` | — |
| `SAP_FLUX_ERR` | SAP uncertainty | Optional | `SAP_FLUX.uncertainties` | `None`, warning |
| `PDCSAP_FLUX_ERR` | PDC uncertainty | Optional | `PDCSAP_FLUX.uncertainties` | `None`, warning |
| `SAP_QUALITY` | quality flags | Optional | `quality_flags` (int64) | `None` |
| `CADENCENO` | cadence ids | Optional | `cadence_numbers` (int64) | `None` |
| Other columns | — | No | Not imported | possibly noted in `notes` |

SAP and PDCSAP remain independent columns, each paired with its own `*_FLUX_ERR`. Never merged. Never one silently discarded.

### 12.2 Source metadata mapping

| `DatasetSource` field | Proposed source | Notes |
|---|---|---|
| `mission` | `MISSION` header | Leave `None` if absent |
| `instrument` | `INSTRUME` header | Leave `None` if absent |
| `target_object` | `OBJECT` header | Leave `None` if absent |
| `source_id` | `KEPLERID` (target ID) | Distinct from product/file ID; `None` if absent |
| `archive` | `None` | **Not** `ORIGIN` unless supplying archive independently established |
| `original_filename` | Actual input filename | |
| `original_file_path` | Actual input path | |

`ORIGIN=NASA/Ames` may be retained in `notes` or an informational finding, but **must not** automatically be described as the archive. Do not invent source metadata; absent/ambiguous → field unknown.

### 12.3 Dataset naming
- `LightCurveDataset.name` = input filename stem (e.g. `kplr011904151-2009131105131_llc_full`).
- Full original filename in `DatasetSource.original_filename`; full path in `original_file_path`.
- Do not invent a target name or scientific label when the filename is the only reliable identifier.
- Empty/unusable stem → `FITSImportError` rather than silently inventing a name.

### 12.4 Metadata not representable by current model
Raw FITS `TTYPE`/`TFORM`/`TDISP`/`NULL` per column, full header card list, aperture image (HDU2), PDC config keywords. Not important enough to require a model change for 2.2.2; may go in `LightCurveDataset.notes` or remain out of scope. Any model-field addition is a 2.2.1-scope decision requiring approval.

---

## 13. Complete Validation Matrix

Classifications: **Error** = `FITSImportError` raised, no dataset constructed. **Warning** = import succeeds, finding in `dataset.validation.warnings`, data preserved. **Info** = import succeeds, finding in `dataset.validation.info`, data preserved.

| # | Condition | Succeeds? | Finding | Data preserved? | Raises `FITSImportError`? | User approval? |
|---|------|---|---|---|---|---|
| F1 | Missing / unreadable file | No | — | N/A | Yes | No |
| F2 | Corrupted / invalid FITS structure | No | — | N/A | Yes | No |
| F3 | No table HDU with TIME + flux column | No | — | N/A | Yes | No |
| C1 | `TIME` column absent | No | — | N/A | Yes | No |
| C2 | Neither `SAP_FLUX` nor `PDCSAP_FLUX` present | No | — | N/A | Yes | No |
| C3 | Only SAP or only PDCSAP available | Yes | Info (single flux series) | Yes | No | No |
| C4 | Flux present, matching `*_FLUX_ERR` absent | Yes | Warning (missing uncertainty) | Yes, `uncertainties=None` | No | No |
| C5 | `*_FLUX_ERR` present but its flux absent | Yes | **Warning** (orphan uncertainty ignored) | Yes, orphan not imported | No | No |
| C6 | `SAP_QUALITY` / `CADENCENO` absent | Yes | Optional → `None` | Yes | No | No |
| C7 | Extra unsupported numeric columns | Yes | Not imported (possibly info) | Yes | No | No |
| C8 | Unexpected/incompatible dtype (non-numeric where numeric required) | No | — | N/A | Yes | No |
| C9 | Array length ≠ time length | No | — | N/A | Yes (via model `LightCurveValidationError`) | No |
| M1 | Non-numeric timestamp | No | — | N/A | Yes | No |
| M2 | Non-finite timestamp (NaN/inf) | Yes | Warning | Yes, preserved | No | No |
| M3 | Non-finite flux (NaN/inf) | Yes | Warning (`n_nonfinite` + zero-based row indices) | Yes, preserved | No | No |
| M4 | Non-finite uncertainty | Yes | Warning | Yes, preserved | No | No |
| M5 | Negative uncertainty | Yes | Warning | Yes, preserved (not replaced) | No | No |
| M6 | Duplicate timestamps | Yes | Warning | Yes, preserved (not reordered) | No | No |
| M7 | Non-monotonic timestamps | Yes | Warning | Yes, preserved (order kept) | No | No |
| Q1 | Nonzero quality flags present | Yes | Info (count + zero-based row indices) | Yes, preserved | No | No |
| Q2 | Quality-bitmask filtering requested | N/A | Not performed in 2.2.2 | — | No | **Yes** (future policy) |
| T1 | Missing time unit | Yes | Info | Yes, `unit=""` | No | No |
| T2 | Missing time reference/scale/frame | Yes | Info | Yes, empty/`None` | No | No |
| T3 | Missing flux unit | Yes | Info | Yes, `unit=""` | No | No |
| U1 | Flux unit ≠ uncertainty unit per §7.2 table | No | — | N/A | Yes | No |
| N1 | Integer `TNULL` sentinel present in `SAP_QUALITY`/`CADENCENO` data | No | — | N/A | Yes | No |
| E1 | Empty table (zero observations) | No | — | N/A | Yes | No |
| D1 | Duplicate/conflicting supported column names | No | — | N/A | Yes | No |

**Note:** The undefined condition "Multiple candidate tables, no reasonable choice" has been removed. The selection policy in Section 6 always produces a deterministic result (prefer `LIGHTCURVE` among valid candidates, else first in HDU order) or raises `FITSImportError` only when no valid candidate exists (condition F3).

**Scientific reasoning (§5.1, §5.6):** non-finite and questionable measurements preserved, never removed/replaced/zero-filled (§5.1.4, §5.6.1 acceptance 3). Quality flags never auto-filtered (§3.4.10; REVIEW-002 justification). File-level failures are exceptions, not `ValidationReport` errors (no dataset exists to attach to — §5.6.7).

---

## 14. Error-Handling Strategy

- Single exception type: `FITSImportError` (subclass of `Exception`), meaningful user-facing message, chained underlying cause (`from exc`).
- Success path: return `LightCurveDataset`; warnings/infos live in `dataset.validation`.
- Failure path: raise `FITSImportError`; no partially populated dataset returned.
- `LightCurveValidationError` from model construction caught and re-raised as `FITSImportError` with context.
- Zero-based `row_indices` in every `ValidationFinding`.
- No GUI error handling; no file-selection dialogs; caller decides presentation.

---

## 15. Data-Integrity and Resource-Management Approach

- Open read-only (`mode="readonly"`); never open for write.
- All array copies made **inside** the `with fits.open(...)` block before close.
- Convert big-endian FITS dtypes to native float64/int64 via `np.array(..., dtype=..., copy=True)`; float32→float64 value-preserving.
- Non-finite values preserved (no fill/replace/interpolate).
- Quality flags preserved (no filtering).
- Distinct columns remain distinct (SAP ≠ PDCSAP).
- No observations silently discarded (observation count preserved).
- No units or timestamps silently changed (no BKJD→JD conversion).
- Original unit strings preserved per §7.4; no unit conversion.
- No normalization/detrending/filtering.
- Model's `_copy_arrays` provides a second authoritative safety copy.
- Original FITS file bytes/checksum unchanged; file remains outside repo and unmodified.

---

## 16. Multiple-Candidate Selection Policy (Consolidated)

The following policy is applied identically in Section 5 (HDU selection), Section 13 (validation matrix), Section 17 (tests), and Section 22 (implementation sequence):

1. No structurally valid candidate → `FITSImportError`.
2. Exactly one valid candidate → select it.
3. Multiple valid candidates with one or more structurally valid `EXTNAME=LIGHTCURVE` candidates → prefer a `LIGHTCURVE` candidate.
4. If multiple candidates have the same preference, select the first in HDU order.
5. If multiple valid candidates exist and selection is resolved by this deterministic rule, import successfully and record an informational finding describing the ambiguity and selection.

The undefined "no reasonable choice" failure condition does not appear anywhere in this plan. No additional selection failure mode is invented.

---

## 17. Focused 2.2.2 Automated Testing Plan (Corrected)

Tests in a new module (`tests/test_fits_importer.py`), fixtures under pytest `tmp_path` — **no dependence on external Kepler dataset or absolute Windows paths.** Portable suite passes on any machine.

### 17.1 Temporary FITS fixtures
- Valid Kepler-like multi-HDU table (Primary + LIGHTCURVE at index 1 + APERTURE).
- Light-curve table at a different HDU index (e.g., index 2) — verify its own `selected_hdu.header` metadata is used, not `hdul[1]`.
- Structural table identification (by TIME + flux column, not position).
- Multiple valid candidates with `LIGHTCURVE` preference → `LIGHTCURVE` selected, info finding recorded.
- Multiple valid candidates without `LIGHTCURVE` → first in HDU order selected, info finding recorded.
- No valid candidate → `FITSImportError`.
- Missing `TIME` column → `FITSImportError`; missing both flux columns → `FITSImportError`.
- Only `SAP_FLUX`; only `PDCSAP_FLUX`.
- Correct uncertainty pairing (SAP↔SAP_ERR, PDCSAP↔PDCSAP_ERR).
- Missing uncertainty column(s) → `uncertainties=None` + warning.
- Missing optional quality/cadence columns → `None`.
- Supported numeric dtypes and endianness (`>f4`, `>f8`, `>i4` → float64/int64).
- Rejection of incompatible string/object types → `FITSImportError`.
- Preservation of NaN/inf in flux and uncertainty.
- Negative uncertainty → warning, preserved.
- Duplicate / non-monotonic timestamps → warning, preserved, not reordered.
- Missing metadata (no time unit, no mission) → info / `None` fields.
- Duplicate/conflicting supported column names → `FITSImportError`.
- Empty table (zero observations) → `FITSImportError`.
- Corrupted / truncated / unreadable file → `FITSImportError`.
- Integer `TNULL` sentinel declared but unused → import normally; sentinel present in data → `FITSImportError` (§11.2).
- Successful dataset construction and model compatibility (`to_dict()`/`from_dict()` round-trip).
- Arrays usable after FITS closure (independent of open handle).
- Preservation of observation count and original data values.
- Zero-based validation row indices.

### 17.2 Complete unit-handling test coverage (all §7.2 branches)
Every branch of the uncertainty-unit policy table is explicitly tested:

| Flux unit | Uncertainty unit | Expected result |
|---|---|---|
| Present | Present and identical | Import |
| Absent or blank | Absent or blank | Import with `unit=""` |
| Present | Absent or blank | `FITSImportError` |
| Absent or blank | Present | `FITSImportError` |
| Present | Present but different | `FITSImportError` |

Additional unit tests:
- **Unfamiliar but non-empty unit string:** preserve the original string exactly; do not normalize, rewrite, or discard it.
- **Whitespace-only unit metadata:** treat it as blank (i.e., `""`).
- **Same preservation and blank-handling principles for `TIMEUNIT` and descriptive `TUNIT1` metadata** where applicable.
- **Original unit strings stored:** verify `MeasurementColumn.unit` and `TimeInfo.unit` contain the original FITS `TUNITn`/`TIMEUNIT` strings, not normalized or converted values.

### 17.3 Orphan uncertainty tests (consistent warning classification)
- `SAP_FLUX_ERR` exists but `SAP_FLUX` absent → warning, orphan ignored, import succeeds.
- `PDCSAP_FLUX_ERR` exists but `PDCSAP_FLUX` absent → warning, orphan ignored, import succeeds.
- Orphan uncertainty never paired with another flux series.
- Orphan uncertainty never treated as file-level import failure.

### 17.4 Fixture assumptions corrected
A normal FITS binary table has a shared row structure; columns do **not** have independently mismatched lengths. Model-level array-alignment testing remains in `tests/test_light_curve.py` (already covered there). Do not invent malformed FITS cases merely to increase test count.

### 17.5 Resource-safety testing
- Assert returned arrays remain usable after the FITS file has closed.
- Assert returned arrays do not depend on an open FITS file handle.
- Assert imported data remains intact after close.

### 17.6 Model-only tests
Stay in `tests/test_light_curve.py`; not duplicated in importer tests.

### 17.7 Baseline
Existing 224 tests must continue to pass with no regressions.

---

## 18. Optional Real-Data Verification

Gated on the actual Kepler file being present. Skipped if absent — never makes the portable suite dependent on it.

Verify:
- HDU identified as LIGHTCURVE (index 1 structurally, not hardcoded).
- 476 rows; TIME range 120.5391–130.2454; unit `d`, scale `TDB`, reference `BJD - 2454833`, frame `SOLARSYSTEM`.
- SAP_FLUX and PDCSAP_FLUX both present and distinct; 4 and 7 non-finite respectively.
- Uncertainties paired correctly; same non-finite rows per column.
- `SAP_QUALITY` 37 nonzero preserved; `CADENCENO` 568–1043 consecutive.
- `DatasetSource.original_file_path`/`original_filename` set; mission/instrument/target_object/source_id correct.
- `name` = filename stem.
- Valid `LightCurveDataset` constructed; `to_dict()`/`from_dict()` round-trip.
- Original file checksum unchanged before/after import.

---

## 19. Documentation Impact Assessment

Per `AGENTS.md`, documentation updates are required during Build mode. No documents modified now.

### 19.1 2.2.2 implementation documentation (to update during Build)
- Record `src/fits_importer.py` module and responsibilities.
- Record public interface (`import_light_curve`, `FITSImportError`) and error behavior.
- Record supported FITS structure and column/metadata mapping (including units, time metadata, null handling).
- Record validation behavior, classifications, and limitations.
- Record focused test coverage and results.
- Update `docs/MASTER_DEVELOPMENT_ROADMAP.md` (2.2.2 status) and `docs/development/DEVELOPMENT_LOG.md` (implementation record, test results).

### 19.2 2.2.4 consolidation (future)
- Broader documentation reconciliation across subtasks; cross-subtask completion status; overall Stage 2.2 verification; remaining deferred/unresolved items.

Foundation documents remain read-only. `docs/README.md` unchanged unless a significant document is added/renamed. Existing project-lifecycle docs unchanged.

---

## 20. Explicit Subtask Boundaries

| Subtask | Responsibility | In 2.2.2? |
|---|---|---|
| 2.2.1 | Light-curve data model — done | No (reused only) |
| 2.2.2 | FITS reading, HDU identification, extraction, metadata, validation, `LightCurveDataset` construction, importer tests | **Yes — current** |
| 2.2.3 | Project association, dataset persistence, save/reopen, project IDs/ownership/permissions | No (future) |
| 2.2.4 | Broader Stage 2.2 verification, documentation reconciliation, completion assessment | No (future) |

**Excluded from 2.2.2:** project association/persistence, visualization, BLS/analysis, quality-bitmask filtering, archive downloads, universal FITS framework, database/permanent storage, GUI dialogs.

---

## 21. Risks and Unresolved Issues

| Risk / Issue | Description | Mitigation / Status |
|---|---|---|
| Memory-mapped FITS arrays | Post-close access fails if not copied. | Copy arrays inside `with` block. |
| Big-endian FITS dtypes | Convert to native float64/int64. | `np.array(..., dtype=..., copy=True)` handles byte swap. |
| Float32 → float64 upcast | Value-preserving, doubles flux memory. | Acceptable at ~476 rows. |
| Model re-copies arrays | Slight redundancy. | Acceptable; correctness > micro-optimization. |
| Real dataset not portable | Automated suite must not depend on absolute path. | Gate real-data test on file presence; `tmp_path` fixtures. |
| Validation vs exception boundary | Risk of putting import failures into nonexistent dataset's `ValidationReport`. | Enforce separation (Section 14). |
| Quality-bitmask pressure | Temptation to auto-filter nonzero flags. | Explicitly excluded; future analysis operation requiring approval. |
| Scope creep | Pressure to add persistence, UI, visualization, BLS. | Explicitly excluded. |
| Flux/uncertainty unit mismatch | Model has no separate uncertainty-unit field. | Raising `FITSImportError` (§7.2) — no model change. |
| Integer `TNULL` sentinel in data | Model cannot represent per-row missing integers. | Raising `FITSImportError` (§11.2) — no model change; Kepler file has no TNULL so does not block initial implementation. |

---

## 22. Recommended Build Implementation Sequence

1. Create `src/fits_importer.py`: `FITSImportError`, `import_light_curve()`, FITS opening/close, structural HDU identification (Section 5).
2. Implement header metadata extraction from `selected_hdu.header` and `selected_hdu.columns` (Section 6), not `hdul[1]`.
3. Implement extraction of `TIME`, `SAP_FLUX`/`PDCSAP_FLUX`, uncertainties, `SAP_QUALITY`, `CADENCENO` (array copies inside `with` block; per-column units from `TUNITn`).
4. Implement unit cross-check (§7.2) and integer `TNULL` policy (§11.2).
5. Implement metadata extraction into `DatasetSource` and `TimeInfo` (BKJD/TDB/SOLARSYSTEM; time unit from `TIMEUNIT`, reference from descriptive `TUNIT1` per §8; filename-stem naming).
6. Implement validation findings and `ValidationReport`; dataset assembly via `LightCurveDataset` constructor; surface `LightCurveValidationError` as `FITSImportError`.
7. Implement multiple-candidate selection policy (§16) consistently across code and tests.
8. Create focused importer tests with `tmp_path` fixtures (Section 17), including all unit-handling branches and orphan-uncertainty warning tests.
9. Optional real-data verification against Kepler file, gated on presence (Section 18).
10. Run full suite (224+ passing, no regressions).
11. Update documentation per `AGENTS.md` — Build-mode activity (Section 19).
12. Review completion; hand off to 2.2.3.

Deferred to 2.2.3: project association, persistence, save/reopen. Deferred to 2.2.4: broader integration verification and documentation reconciliation.

---

## 23. Decisions or Questions Requiring User Approval

1. **Approval of this revised plan** before switching to Build mode (the gate itself).
2. No additional decisions require approval. All open points from prior revisions are resolved by explicit policy in this document:
   - Extension-header selection via `selected_hdu.header` (any HDU index) — Section 6.
   - Multiple-candidate selection policy — Section 16, consistent everywhere.
   - Uncertainty-unit mismatch → `FITSImportError`, no model extension — Section 7.2.
   - Original unit-string preservation — Section 7.4.
   - Header inheritance vs application fallback — Section 9.
   - Time unit vs time reference — Section 8.
   - Integer `TNULL` sentinel in data → `FITSImportError`, no model change — Section 11.2.
   - Orphan uncertainty → warning consistently — Section 12.1.

---

## Remaining Assumptions or Unresolved Decisions

**No implementation-critical uncertainties remain.** All four correction areas have been resolved by explicit policy:

1. **Extension-header selection:** `selected_hdu.header` used for all extension-specific metadata; no fixed-index assumption; light-curve table may be at any HDU index (Sections 5–6).
2. **Multiple-candidate inconsistency:** The undefined "no reasonable choice" condition removed; a single deterministic selection policy (§16) is applied consistently across HDU selection, validation matrix, tests, and implementation sequence.
3. **Unit-handling test coverage:** All five branches of the uncertainty-unit policy are explicitly tested, plus unfamiliar unit string preservation, whitespace-only units, and `TIMEUNIT`/`TUNIT1` preservation principles (Section 17.2).
4. **Orphan uncertainty handling:** Consistently classified as **warning** everywhere (validation matrix, test plan, implementation sequence) (Section 12.1).

The only gate is user approval of this plan before switching to Build mode. No code, tests, or repository changes have been made in this session.

---

## Final Readiness Assessment

The plan is **internally consistent** and **ready for user approval** to enter BUILD mode. All four review findings have been addressed:

- ✅ Extension-header selection corrected to `selected_hdu.header` (no fixed index 1).
- ✅ Multiple-candidate policy made consistent across all sections; "no reasonable choice" removed.
- ✅ Complete unit-handling test coverage for all policy branches, unfamiliar strings, whitespace-only units, and `TIMEUNIT`/`TUNIT1` preservation.
- ✅ Orphan uncertainty handling consistently classified as **warning**.

No contradictions, obsolete wording, or fixed-index references remain. All scope boundaries are preserved. The plan awaits explicit user authorization before any switch to Build mode.

---

**Statement:** Implementation has not started. No files were created, modified, deleted, or renamed in this session; no dependencies installed; no configuration changed; the original FITS file untouched; no Git state altered by me. This revised plan remains in PLAN mode and awaits your explicit review and authorization before any switch to Build mode.


# chatgpt plan v6 review

The revised plan is substantially improved and is close to BUILD approval. The four correction areas are addressed, and the scope, test strategy, and data-preservation policies are coherent.

There is one remaining implementation-level contradiction in Section 7.5 that should be corrected before BUILD.

## Remaining issue: uncertainty units cannot be stored separately

The plan correctly establishes that `MeasurementColumn` has only one `unit` field shared by measurement values and uncertainties.

However, Section 7.5 says:

> `SAP_FLUX.uncertainties` unit ← original `TUNIT5` string

And similarly for `PDCSAP_FLUX.uncertainties` and `TUNIT9`.

That is not possible with the existing model. There is no separate uncertainty-unit field.

The intended behavior should be:

1. Read the flux and uncertainty units independently from their respective FITS columns.
2. Apply the Section 7.2 compatibility checks.
3. If compatible, store the flux unit in `MeasurementColumn.unit`.
4. The uncertainty values use that same unit by the model's design.
5. Do not attempt to assign or store a separate uncertainty unit.

This preserves the existing model and the approved unit policy.

## Send Nemotron this final correction

Make one final, narrow correction to the Subtask 2.2.2 implementation plan. Remain in PLAN mode. Do not implement or edit files.

**Issue: Section 7.5 describes assigning uncertainty units separately, which the existing `MeasurementColumn` model cannot support.**

The model has one `unit` field shared by measurement values and uncertainties. There is no separate uncertainty-unit field.

Correct Section 7.5 so that:

1. The importer reads the flux unit and uncertainty unit independently from their respective FITS `TUNITn` metadata.
2. It applies the compatibility policy in Section 7.2 before constructing the measurement column.
3. When the units are compatible, `MeasurementColumn.unit` receives the original flux unit string.
4. The uncertainty array is attached to that measurement column and shares its unit by the existing model design.
5. The importer does not attempt to assign, store, or represent a separate uncertainty unit.

Preserve all existing Section 7.2 rules:

- Both present and identical: import.
- Both absent or blank: import with `unit=""`.
- Only one present: raise `FITSImportError`.
- Both present but different: raise `FITSImportError`.

Update any wording elsewhere in the plan that implies uncertainty units are stored independently. Do not change the model, expand scope, or alter any other approved policy.

Return the complete corrected Section 7.5 and identify any other wording changed. Confirm that the plan remains internally consistent. No implementation or repository changes.

## Readiness after that correction

Once this is corrected, I expect the plan to be ready for BUILD approval. I don't see a reason to reopen the architecture or expand the scope.

One distinction: the uploaded repository snapshot I inspected earlier did not contain the model files, so the latest direct repository verification in Nemotron's report is useful, but I have not independently reproduced those checks against a live working tree.

After Nemotron returns the correction, send it here. I can give the final approval assessment before you authorize BUILD.

# chatgpt prompt from v6 review

Make one final, narrow correction to the Subtask 2.2.2 implementation plan. Remain in PLAN mode. Do not implement or edit files.

**Issue: Section 7.5 describes assigning uncertainty units separately, which the existing `MeasurementColumn` model cannot support.**

The model has one `unit` field shared by measurement values and uncertainties. There is no separate uncertainty-unit field.

Correct Section 7.5 so that:

1. The importer reads the flux unit and uncertainty unit independently from their respective FITS `TUNITn` metadata.
2. It applies the compatibility policy in Section 7.2 before constructing the measurement column.
3. When the units are compatible, `MeasurementColumn.unit` receives the original flux unit string.
4. The uncertainty array is attached to that measurement column and shares its unit by the existing model design.
5. The importer does not attempt to assign, store, or represent a separate uncertainty unit.

Preserve all existing Section 7.2 rules:
- Both present and identical: import.
- Both absent or blank: import with `unit=""`.
- Only one present: raise `FITSImportError`.
- Both present but different: raise `FITSImportError`.

Update any wording elsewhere in the plan that implies uncertainty units are stored independently. Do not change the model, expand scope, or alter any other approved policy.

Return the complete corrected Section 7.5 and identify any other wording changed. Confirm that the plan remains internally consistent. No implementation or repository changes.

# opencode plan v7

**Corrected Section 7.5 — Application to specific fields**

For each supported flux/uncertainty pair (`SAP_FLUX`/`SAP_FLUX_ERR`, `PDCSAP_FLUX`/`PDCSAP_FLUX_ERR`):

1. Read the **flux unit** independently from the flux column's `TUNITn` (`TUNIT4` for `SAP_FLUX`; `TUNIT8` for `PDCSAP_FLUX`).
2. Read the **uncertainty unit** independently from the uncertainty column's `TUNITn` (`TUNIT5` for `SAP_FLUX_ERR`; `TUNIT9` for `PDCSAP_FLUX_ERR`).
3. Apply the compatibility policy in Section 7.2 **before** constructing the `MeasurementColumn`:
   - Both units present and identical → proceed; `MeasurementColumn.unit` receives the original flux unit string.
   - Both units absent or blank → proceed; `MeasurementColumn.unit` is `""`.
   - Only one unit present → raise `FITSImportError`.
   - Both units present but different → raise `FITSImportError`.
4. When compatible, `MeasurementColumn.unit` receives the original flux unit string (preserved as-is per Section 7.4; `""` if absent or blank).
5. The uncertainty array is attached to that `MeasurementColumn` and **shares its unit** by the existing model design.
6. The importer does **not** assign, store, or represent a separate uncertainty unit. `MeasurementColumn` has a single `unit` field and no separate uncertainty-unit field.

---

**Other wording changed elsewhere**

- **Section 7.4 ("Unit-string preservation")**: The heading is narrowed to "Unit-string preservation (stored unit fields)" and the first bullet is clarified to state that preservation applies to unit fields actually stored in the model — `MeasurementColumn.unit` for flux values and `TimeInfo.unit` for time values. Uncertainty units are read solely for the Section 7.2 compatibility check and are **not** stored, because `MeasurementColumn` has no separate uncertainty-unit field.

No other sections imply independent uncertainty-unit storage. Section 7.1 already states correctly that `MeasurementColumn` has one `unit` field shared by values and uncertainties. Section 6 (header metadata) correctly describes reading `TUNITn` from `selected_hdu.columns` for the compatibility check without implying separate storage. Section 13 (validation matrix) and Section 17.2 (unit-handling tests) describe the compatibility policy, not separate storage.

**Internal consistency confirmation**

The plan remains internally consistent. Section 7.2's compatibility rules are unchanged and are now correctly applied before column construction in Section 7.5. `MeasurementColumn.unit` receives only the flux unit string when compatible; the uncertainty array shares that unit by model design. No separate uncertainty-unit field is introduced, no model change is proposed, and no other approved policy is altered.

No implementation or repository changes were made. This remains PLAN mode; no files were created, modified, deleted, or renamed.

# chatgpt plan 7 review

The correction resolves the remaining model-mapping contradiction.

Section 7.5 is now consistent with the existing `MeasurementColumn` model:

- Flux and uncertainty units are read independently.
- Section 7.2 compatibility is checked before constructing the measurement column.
- The flux unit is stored in `MeasurementColumn.unit`.
- The uncertainty array shares that unit through the existing model.
- No separate uncertainty-unit field or model change is introduced.
- Section 7.4 now explicitly distinguishes stored units from validation-only uncertainty units.

I don't see another blocking issue in the correction provided. The scope and previously approved policies remain unchanged.

PLAN ready for BUILD

Next step: If this reflects the complete revised plan, you can authorize Nemotron to enter BUILD mode for Subtask 2.2.2. Keep the implementation limited to the approved files, tests, and documentation updates. Do not begin Subtask 2.2.3.


# me to chatgpt

Now give me the build prompt to have it perform all necessary tasks for 2.2.2 as we have planned with the reviewed corrections

# chatgpt BUILD prompt from plan v7

Use the following as the BUILD prompt for Nemotron. It incorporates the reviewed 2.2.2 plan, including the corrected uncertainty-unit handling, and explicitly limits implementation scope.

# BUILD — Subtask 2.2.2: FITS Light-Curve Importer

**Authorization:** BUILD is approved for Subtask 2.2.2 only.

Implement the reviewed and approved Subtask 2.2.2 plan. Treat the latest corrected PLAN as the implementation specification, including all corrections and clarifications reviewed with ChatGPT.

Do not redesign the plan, expand scope, or begin Subtask 2.2.3.

## 1. Required pre-implementation checks

Before editing:

1. Read and follow `AGENTS.md`.
2. Inspect the current repository state and confirm the active branch and working-tree changes.
3. Review the relevant project documentation:
   - `docs/README.md`
   - `docs/MASTER_DEVELOPMENT_ROADMAP.md`
   - `docs/development/DEVELOPMENT_LOG.md`
   - Relevant unresolved questions and decision records.
   - Relevant Foundation documents using `docs/Foundation/0_index.md`.
4. Inspect the existing:
   - `src/light_curve.py`
   - `tests/test_light_curve.py`
   - Related project structure and test conventions.
5. Run the existing test suite before implementation and record the baseline.

Do not overwrite or discard existing user changes. Do not modify Foundation documents.

If the actual repository state conflicts with the reviewed plan, stop and report the discrepancy before making changes.

## 2. Implementation scope

Create:

- `src/fits_importer.py`
- `tests/test_fits_importer.py`

Implement the public interface:

- `FITSImportError`
- `import_light_curve(file_path: str | os.PathLike[str]) -> LightCurveDataset`

Use the existing light-curve model in `src/light_curve.py`.

Use the already available project dependencies, including Astropy and NumPy. Do not add dependencies unless the reviewed plan explicitly requires them.

The importer must read FITS files and construct a validated `LightCurveDataset`. It must not implement persistence, project association, GUI integration, BLS analysis, or other later-subtask functionality.

## 3. FITS file handling and HDU selection

- Open FITS files read-only.
- Use a context manager and ensure the file is closed after import.
- Identify candidate binary-table HDUs structurally.
- A valid candidate must contain `TIME` and at least one supported flux column: `SAP_FLUX` or `PDCSAP_FLUX`.
- Prefer an HDU named `LIGHTCURVE` only when it satisfies the structural requirements.
- Otherwise, select the first structurally valid candidate in HDU order.
- If multiple valid candidates exist, record the planned informational validation finding.
- Do not assume the selected table is always `hdul[1]`.
- Use the selected HDU's own header and columns for extension metadata.

If no valid candidate exists, raise `FITSImportError` with a useful explanation.

## 4. Column mapping

Map the supported columns as specified in the reviewed plan:

- `TIME` → `TimeInfo.values`
- `SAP_FLUX` → measurement column when present
- `SAP_FLUX_ERR` → uncertainties for `SAP_FLUX` when present
- `PDCSAP_FLUX` → measurement column when present
- `PDCSAP_FLUX_ERR` → uncertainties for `PDCSAP_FLUX` when present
- `SAP_QUALITY` → optional `quality_flags`
- `CADENCENO` → optional `cadence_numbers`

Preserve SAP and PDCSAP measurements independently. Do not substitute one for the other.

If an uncertainty column exists without its corresponding flux column, follow the reviewed plan's orphan-uncertainty warning behavior.

Ignore unsupported columns rather than inventing mappings for them.

Do not filter, remove, reorder, or silently discard observations.

## 5. Metadata mapping

Follow the reviewed plan's explicit header-source policy:

- Use the primary header for source metadata, with the specified application-level fallback to the selected extension header where applicable.
- Use the selected extension header for time metadata.
- Do not assume FITS header inheritance or implicit header merging.
- Do not use `ORIGIN` as the archive field automatically.

Populate the existing model fields only when the source provides the corresponding information.

For time metadata:

- `TIMEUNIT` → `TimeInfo.unit`
- Descriptive `TUNIT1` → `TimeInfo.reference`, when applicable
- `TIMESYS` → time scale
- `TIMEREF` → reference frame
- `BJDREFI` and `BJDREFF` → numeric reference offset
- `TSTART` and `TSTOP` → start and stop
- Map `TIMEDEL` only if its meaning and units are verified by the reviewed plan.

Do not convert BKJD values to BJD or otherwise transform the time values. Preserve the original time values and represent their reference metadata separately.

Use the original filename and file path in the appropriate source fields. Use the filename stem for the dataset name, as specified in the plan.

Do not invent missing metadata or substitute undocumented defaults.

## 6. Numeric types and data preservation

Follow the reviewed type rules:

- Convert supported time, flux, and uncertainty arrays to `float64`.
- Convert supported quality-flag and cadence arrays to `int64`.
- Do not silently truncate floating-point values into integer arrays.
- Reject incompatible source data types with `FITSImportError`.
- Preserve NaN and infinite floating-point values.
- Preserve quality flags and cadence values without interpreting or filtering them.

Use the existing model's construction behavior and validation. Do not modify the scientific model to accommodate the importer.

## 7. Unit handling — important reviewed correction

Implement the reviewed unit policy exactly.

### 7.1 Measurement and uncertainty units

For each supported pair:

- `SAP_FLUX` / `SAP_FLUX_ERR`
- `PDCSAP_FLUX` / `PDCSAP_FLUX_ERR`

Read the flux and uncertainty units independently from their respective column `TUNITn` metadata.

Apply the compatibility policy before constructing the `MeasurementColumn`:

| Flux unit       | Uncertainty unit      | Required behavior       |
| --------------- | --------------------- | ----------------------- |
| Present         | Identical and present | Import                  |
| Blank or absent | Blank or absent       | Import with `unit=""`   |
| Present         | Blank or absent       | Raise `FITSImportError` |
| Blank or absent | Present               | Raise `FITSImportError` |
| Present         | Different and present | Raise `FITSImportError` |

Preserve nonblank original unit strings exactly as supplied. Do not perform unit conversion.

**Critical model constraint:** `MeasurementColumn` has one `unit` field shared by its measurement values and uncertainty array.

Therefore:

- `MeasurementColumn.unit` receives the original flux unit string when compatible.
- If both units are blank or absent, `MeasurementColumn.unit` receives `""`.
- The uncertainty array is attached to that same `MeasurementColumn` and shares its unit.
- The uncertainty unit is used only for compatibility validation.
- Do not assign, store, or represent a separate uncertainty unit.
- Do not add an `uncertainty_unit` field or modify `src/light_curve.py`.

Add tests confirming this behavior.

### 7.2 Time units

Preserve the original nonblank time-unit string in `TimeInfo.unit`. Use `""` when the source unit is absent or blank.

Do not discard unfamiliar but nonblank unit strings merely because they are not recognized by an external unit library.

## 8. FITS integer null sentinels

Follow the reviewed `TNULL` policy for supported integer columns:

- If a supported integer column declares a null sentinel and that sentinel does not occur in the data, import normally.
- If the declared sentinel occurs in the data, raise `FITSImportError`.
- Do not silently convert sentinel values to zero, remove observations, or invent missing-value handling.
- Do not modify the existing model to introduce per-row missingness.

Test both sentinel cases.

## 9. Validation findings

Preserve the observations and report the applicable findings using the existing `ValidationReport` and `ValidationFinding` structures.

Follow the reviewed plan:

- Non-finite time, flux, or uncertainty values: warning; preserve values.
- Negative uncertainty values: warning; preserve values.
- Duplicate times: warning; preserve order.
- Non-monotonic times: warning; preserve order.
- Nonzero quality flags: informational finding; do not filter observations.
- Multiple valid candidate HDUs: informational finding.
- Orphan uncertainty columns: warning.
- Missing optional columns: follow the validation matrix in the reviewed plan.

Use zero-based row indices where applicable.

Do not introduce additional scientific interpretation or automatic data cleaning.

## 10. Tests

Create portable tests in `tests/test_fits_importer.py` using temporary FITS fixtures.

Tests must not depend on the user's external Kepler FITS file or any other machine-specific path.

Cover the reviewed plan's requirements, including:

- Successful import with SAP data.
- Successful import with PDCSAP data.
- Import with both supported flux columns.
- Optional uncertainty columns.
- Optional quality and cadence columns.
- Missing optional columns.
- No structurally valid light-curve HDU.
- Multiple candidate HDUs.
- `LIGHTCURVE` preference among valid candidates.
- Selection of a valid HDU that is not at index 1.
- Metadata mapping and header-source behavior.
- Missing and blank units.
- Compatible flux and uncertainty units.
- Every incompatible unit-policy case.
- Preservation of unfamiliar nonblank unit strings.
- Whitespace-only unit strings.
- Correct storage of the flux unit in the single `MeasurementColumn.unit` field.
- Uncertainty arrays attached to their corresponding measurement columns.
- Orphan uncertainty warnings.
- Numeric type conversion and incompatible dtype rejection.
- Non-finite values.
- Negative uncertainties.
- Duplicate and non-monotonic times.
- Nonzero quality flags.
- Integer `TNULL` sentinel declared but unused.
- Integer `TNULL` sentinel present in data.
- FITS data remaining usable after the file is closed.
- Serialization round-trip through the existing model.

Use assertions that verify actual behavior and data preservation. Do not weaken existing tests or replace meaningful assertions with superficial checks.

## 11. Documentation updates

Follow `AGENTS.md` documentation-maintenance requirements.

Update the applicable sections of:

- `docs/MASTER_DEVELOPMENT_ROADMAP.md`
- `docs/development/DEVELOPMENT_LOG.md`

Document the completion and verified behavior of Subtask 2.2.2, including relevant implementation details, tests, and limitations.

Do not modify Foundation documents.

Do not prematurely perform the broader documentation consolidation and completion review assigned to Subtask 2.2.4. However, do not omit documentation updates required for this BUILD task.

## 12. Verification

After implementation:

1. Run the focused importer tests:\
   `python -m pytest tests/test_fits_importer.py -v`
2. Run the existing light-curve model tests:\
   `python -m pytest tests/test_light_curve.py -v`
3. Run the complete test suite:\
   `python -m pytest -q`
4. Confirm that the existing baseline of 224 passing tests remains intact, with the new importer tests added.
5. Investigate and fix failures caused by this implementation.
6. Do not conceal failures, skip tests, or weaken assertions to obtain a passing result.

If the environment prevents a test from running, report that limitation explicitly rather than claiming success.

## 13. Scope restrictions

Do not:

- Modify `src/light_curve.py` or its existing model behavior.
- Modify existing tests except where a directly necessary compatibility issue is identified and explained before making the change.
- Begin Subtask 2.2.3.
- Implement database persistence or project association.
- Implement GUI integration.
- Implement BLS or other analysis.
- Add unrelated abstractions, dependencies, or features.
- Modify Foundation documents.
- Commit, amend, or push Git changes.
- Overwrite or discard unrelated user changes.

If an unexpected issue requires a scope change, stop and report it rather than making an unapproved design change.

## 14. Final BUILD report

When finished, provide:

1. Summary of implementation.
2. Files created and modified.
3. Important implementation decisions and how they follow the reviewed plan.
4. Focused test results.
5. Full test-suite result, including the baseline comparison.
6. Documentation updates made.
7. Known limitations or unresolved issues.
8. Confirmation that no commits or pushes were made.
9. Confirmation that Subtask 2.2.3 was not started.

Clearly distinguish verified results from assumptions or unverified claims.

**Begin BUILD now, following this specification and the reviewed plan.**

After Nemotron completes, bring its full BUILD report and any relevant implementation output back here. The next review should verify the actual changes against the approved plan, not just rely on its completion summary.

# opencode BUILD report v1, from plan v7



# chatgpt REVIEW of build report v1