# OVERVIEW

# Subtask 2.2.2 — FITS Import and Validation

Primary objective: Implement the actual FITS import workflow so the application can read an astronomical FITS file, extract its light-curve measurements, validate the data, and produce a structured dataset using the data model established in Subtask 2.2.1.

The distinction between 2.2.1 and 2.2.2 is:

- 2.2.1: Establishes how the application represents a light-curve dataset.
- 2.2.2: Implements how the application reads and validates an actual FITS file.

This task should make the importer functional without yet implementing full project persistence.

## 1. FITS file selection and reading

[Getting Started with Astropy. Quick tutorial to viewing FITS files… | by Beyza Ulasti | Medium](https://images.openai.com/static-rsc-4/qZl9GmjXfFwr4YE_UEzjWtVOkRwOJuW20ZawyIoPjqX8iKGHw3MNOnswF5qGj12cOHkM7aogPy0Qia0izkVgQVcArf0fpvjwRLQ8QQCxqDyZoAR4ROs2asj3_a6go-wqKFCPye8FaCUsRhvyBaXXjiPJipU-y2VWpK0XYdTsZvo?purpose=inline)

Initial target

`kplr011904151-2009131105131_llc_full.fits`

The existing Kepler-10b dataset outside the repository.

The importer needs to:

- Accept a FITS file path.
- Open the file using Astropy.
- Inspect its HDUs.
- Identify the appropriate light-curve table.
- Read the relevant headers and columns.
- Extract measurements into the data model from 2.2.1.
- Close file resources appropriately after reading.

The importer should not assume that the first HDU always contains the measurements.

It should identify the appropriate data structure rather than relying on a fixed HDU index without validation.

## 2. Extract light-curve measurements

For the initial Kepler dataset, the importer should support the relevant measurement fields:

| Field             | Import responsibility                    |
| ----------------- | ---------------------------------------- |
| `TIME`            | Extract observation timestamps           |
| `SAP_FLUX`        | Extract aperture-photometry measurements |
| `PDCSAP_FLUX`     | Extract corrected flux measurements      |
| `SAP_FLUX_ERR`    | Extract corresponding uncertainty        |
| `PDCSAP_FLUX_ERR` | Extract corresponding uncertainty        |
| `SAP_QUALITY`     | Preserve quality flags                   |
| `CADENCENO`       | Preserve cadence identifiers             |

The importer should retain the distinction between SAP and PDCSAP measurements.

It should also preserve the relationship between each flux column and its corresponding uncertainty column.

Important: The importer should not silently choose one measurement type and discard the others.

The data model and importer should make the available measurements accessible for later selection in the visualization and analysis workflows.

## 3. Metadata extraction

The importer needs to retrieve relevant scientific metadata from the FITS headers and table definitions.

This includes:

- Time units.
- Time reference or epoch.
- Time system (such as TDB).
- Flux units.
- Instrument and mission information.
- Observation cadence.
- Target identification, where available.
- Relevant column metadata.
- Original filename and source path.

For the Kepler dataset, the importer needs to preserve the BKJD time reference and TDB time system.

It must not silently convert timestamps or assume that a time value represents an ordinary Julian Date.

Missing metadata should remain identifiable as missing or unknown.

## 4. Data validation

Critical scientific integrity requirement

The importer must detect problems and communicate them clearly.

### A. Structural validation

- Is the file a readable FITS file?
- Does it contain a suitable table?
- Are the required measurement columns available?
- Are the column structures compatible?
- Are the data types usable?
- Are the expected metadata fields available?

### B. Measurement validation

- Are timestamps numeric and usable?
- Are flux measurements numeric?
- Are uncertainty values available?
- Are there NaN or infinite values?
- Are there invalid or duplicate timestamps?
- Are array lengths consistent?

### C. Quality validation

The importer must preserve quality information.

For example, the selected Kepler dataset has approximately 37 observations with nonzero quality flags.

These should not automatically be removed.

The importer should report their presence and preserve the original flags so a later analysis operation can establish and record an appropriate filtering policy.

### D. Error versus warning handling

The importer should distinguish between:

| Condition                          | Expected handling                                |
| ---------------------------------- | ------------------------------------------------ |
| Unreadable FITS file               | Import failure                                   |
| Missing required time column       | Import failure                                   |
| Missing required flux measurements | Import failure                                   |
| Missing optional metadata          | Warning                                          |
| Missing uncertainty values         | Warning, depending on the selected measurement   |
| Non-finite observations            | Report and preserve according to approved design |
| Nonzero quality flags              | Warning; preserve flags                          |
| Unsupported structure              | Clear import failure                             |

The exact required fields and validation rules should follow the approved 2.2.1 design.

Do not introduce arbitrary validation thresholds.

## 5. Preserve the original measurements

The importer should create a usable application representation without changing the original scientific data.

Requirements:

- Never modify the original FITS file.
- Preserve the original measurements.
- Preserve relevant metadata.
- Preserve quality flags.
- Preserve missing-value information.
- Do not silently discard observations.
- Do not normalize or detrend measurements.
- Do not automatically filter quality flags.
- Do not replace missing values with invented values.

Any transformations needed for later scientific analysis belong to subsequent operations and must be separately identifiable.

## 6. Import results and error reporting

The importer should provide a clear result to the application.

Depending on the approved 2.2.1 design, this may include:

- The constructed light-curve dataset.
- Source information.
- Extracted measurement columns.
- Metadata.
- Validation results.
- Warnings.
- Import errors.

The importer should distinguish a successful import with warnings from a failed import.

The application should be able to explain why a file could not be imported rather than simply displaying a generic failure.

A user-facing file-selection dialog may be included only if it is part of the approved scope for this task. Otherwise, keep the importer independent of the UI and leave its integration to the appropriate task.

## 7. Testing requirements

Testing should cover both the actual Kepler dataset and controlled test fixtures.

| Test category       | What to verify                                            |
| ------------------- | --------------------------------------------------------- |
| FITS reading        | Correctly opens valid FITS files                          |
| HDU detection       | Identifies the correct measurement table                  |
| Column extraction   | Extracts the correct measurements                         |
| Metadata            | Preserves units and time conventions                      |
| Uncertainty         | Maintains flux/error relationships                        |
| Quality flags       | Preserves original flags                                  |
| Missing values      | Detects and handles them according to the approved design |
| Invalid files       | Produces clear errors                                     |
| Missing columns     | Reports structural problems                               |
| Unsupported formats | Fails safely                                              |
| Original data       | Remains unchanged                                         |
| Resource management | Files are closed appropriately                            |

Use temporary FITS fixtures for controlled edge cases.

The actual Kepler dataset should be used for real-data verification when available.

Do not make automated tests dependent on an absolute user-specific file path. The test suite should remain usable on another machine.

## 8. Documentation updates

Under `AGENTS.md`, documentation must remain synchronized with implementation.

Likely affected documents:

- `docs/MASTER_DEVELOPMENT_ROADMAP.md`
- `docs/development/DEVELOPMENT_LOG.md`
- Data-model documentation.
- Importer/module responsibility documentation.
- Validation documentation.
- Testing documentation.

The agent should identify the actual files during Plan mode.

Foundation documents remain read-only.

## 9. What belongs to later subtasks?

| Feature                     | Planned task |
| --------------------------- | ------------ |
| Light-curve data model      | 2.2.1        |
| FITS parsing and validation | 2.2.2        |
| Full project association    | 2.2.3        |
| Dataset persistence         | 2.2.3        |
| Data table                  | 2.3          |
| Interactive graph           | 2.3          |
| BLS analysis                | 2.4          |
| Analysis operation records  | 2.5          |

## 10. Completion checklist

## 2.2.2 expected deliverables

- Reads valid FITS files.
- Identifies the appropriate light-curve table.
- Extracts supported measurement columns.
- Preserves corresponding uncertainties.
- Extracts scientific metadata.
- Preserves quality flags.
- Detects invalid or missing information.
- Separates warnings from fatal errors.
- Produces the approved light-curve data model.
- Leaves original FITS files unchanged.
- Passes automated tests.
- Updates relevant documentation.

## Recommended division of work

I recommend keeping 2.2.2 focused on the importer itself:

1. FITS reading and HDU identification.
2. Measurement and metadata extraction.
3. Validation and warning/error reporting.
4. Testing with real and controlled FITS data.

These are proposed work areas, not necessarily separate Build tasks. The Plan-mode review should establish the appropriate implementation boundaries.

The central success criterion: The application can take a real FITS light-curve file and reliably turn it into the approved internal data model, while preserving its original scientific measurements and metadata.

Project persistence and reopening that imported dataset will be addressed in Subtask 2.2.3.