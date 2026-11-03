# 2.3.2 — Measurement Table Implementation

## 1. Objective

The purpose of 2.3.2 is to implement the measurement table designed and approved in 2.3.1.

The table will allow users to inspect the individual measurements contained in an imported astronomical light-curve dataset.

It should provide access to the actual scientific values and associated information without modifying the underlying dataset.

The table should integrate into the existing application and work with the project and dataset management functionality established in Stage 2.2.

The focus of this subtask is the table itself. Scientific plotting and table/plot synchronization belong to later subtasks.

## 2. Review the approved design and existing implementation

Before implementation, review:

- The completed 2.3.1 design and approval report.
- The Stage 2.2 data model.
- The FITS importer and validation behavior.
- Project integration and persistence.
- Existing application architecture and interface conventions.
- Relevant testing and documentation.

Verify that the approved design still matches the actual repository.

Determine how the table will access the imported measurements and how it will respond to dataset and project changes.

Do not redesign the table or introduce new requirements without approval.

## 3. Implement the measurement table

### 3.1 Display imported measurements

Implement the table according to the approved design.

For the Kepler-10b dataset, relevant fields may include:

| Field           | Information                       |
| --------------- | --------------------------------- |
| TIME            | Observation time                  |
| SAP_FLUX        | Original aperture photometry flux |
| SAP_FLUX_ERR    | Associated uncertainty            |
| PDCSAP_FLUX     | Pipeline-corrected flux           |
| PDCSAP_FLUX_ERR | Associated uncertainty            |
| SAP_QUALITY     | Pipeline quality flags            |
| CADENCENO       | Observation cadence identifier    |

The actual columns must follow the approved design and available data model.

The table should display the imported values accurately, without silently changing their precision or scientific meaning.

### 3.2 Measurement types

Preserve the distinction between different flux measurements.

In particular:

- `SAP_FLUX` and `PDCSAP_FLUX` must remain separately identifiable.
- Their corresponding uncertainties must remain correctly associated.
- Users must be able to inspect both measurements.
- The table must not silently substitute one measurement for another.

The table should provide a clear way to understand which measurement a particular value represents.

### 3.3 Units and metadata

Display relevant information about the measurements.

Consider:

- Time units.
- Time reference and scale.
- Flux units.
- Measurement identity.
- Dataset-level metadata.
- Relevant validation warnings.

Units and metadata must come from the imported dataset.

Unknown information must remain unknown rather than being inferred or invented.

The approved 2.3.1 design should determine whether this information appears in column headers, table information areas, metadata panels, or another arrangement.

## 4. Handle missing and invalid measurements

The table must represent incomplete or invalid measurements in a scientifically understandable way.

This includes:

- Missing values.
- NaN values.
- Infinite values.
- Invalid or unavailable measurements.
- Quality flags.
- Import validation warnings, where relevant.

The design should make these conditions distinguishable from actual measured values.

For example, a missing measurement should not be displayed as zero.

Quality flags should remain accessible. A nonzero quality flag must not automatically cause its associated measurement to disappear.

The table must not silently remove observations because they contain missing values or quality flags.

## 5. Implement measurement inspection

Implement the approved method for inspecting individual observations.

Depending on the approved design, this may include:

- Selecting a table row.
- Identifying the selected observation.
- Viewing its associated measurements.
- Inspecting its uncertainties.
- Accessing its quality flags and cadence identifier.
- Understanding whether any values are missing or invalid.

The table should make it possible to examine individual observations without requiring users to interpret the entire dataset at once.

Selection behavior should be designed with future plot integration in mind, but full table/plot synchronization is not part of this subtask.

## 6. Handle large datasets

Astronomical light curves can contain many observations.

The table should remain usable when displaying larger datasets.

Planning and implementation should consider:

- Avoiding unnecessary duplication of measurement arrays.
- Avoiding expensive operations every time a row is selected.
- Efficiently accessing displayed values.
- Appropriate scrolling and navigation.
- Whether pagination, model/view architecture, or another approach is justified by the approved design.

Do not introduce unnecessary complexity.

The implementation should be appropriate for the current application and expected initial datasets.

## 7. Integrate the table into the application

The measurement table must become accessible through the existing application interface.

Work includes:

- Integrating the table into the approved application layout.
- Displaying the selected project's imported dataset.
- Handling projects with no imported dataset.
- Updating the table when the selected dataset changes.
- Updating the table when the active project changes.
- Clearing or refreshing stale data when appropriate.
- Handling unavailable or failed dataset access.

The table should not maintain an independent scientific dataset that can diverge from the project's imported measurements.

The table is a presentation component that reads from the existing data model.

## 8. Scientific integrity requirements

These requirements apply throughout implementation.

| Concern               | Required behavior                |
| --------------------- | -------------------------------- |
| Original FITS file    | Must not be modified             |
| Imported measurements | Must remain unchanged            |
| SAP and PDCSAP        | Remain separate                  |
| Uncertainties         | Remain correctly associated      |
| Missing values        | Remain represented               |
| Non-finite values     | Remain identifiable              |
| Quality flags         | Remain accessible                |
| Units                 | Use actual available metadata    |
| Time representation   | Preserve original interpretation |
| Normalization         | Not performed                    |
| Filtering             | Not performed                    |
| Detrending            | Not performed                    |
| Table display         | Must not modify scientific data  |

Displaying a value differently from how it is stored may be necessary for readability, but the displayed representation must not alter the underlying measurement.

For example, formatting a timestamp for display must not change the stored timestamp.

## 9. Testing strategy

Testing should verify both table functionality and scientific correctness.

### Table functionality

- Correct columns and values.
- Correct measurement identities.
- Correct uncertainty associations.
- Correct units and metadata.
- Row selection and inspection.
- Dataset switching.
- Project switching.
- Empty dataset behavior.
- Large dataset behavior.

### Missing and invalid values

- Missing values display correctly.
- NaN and infinite values remain identifiable.
- Quality flags are preserved.
- Invalid measurements are not silently removed.
- Missing measurements are not represented as zero.

### Scientific integrity

- Displaying measurements does not modify the underlying data.
- Selecting rows does not modify the underlying data.
- Changing datasets does not alter persisted measurements.
- Original source files remain unchanged.

### Test data

Use controlled fixtures and temporary datasets for routine automated tests.

The standard test suite must not depend on the user's permanent Kepler-10b FITS file or its absolute local path.

The real dataset can be used for optional manual verification.

## 10. Documentation requirements

Update the appropriate documentation as implementation progresses.

Likely affected documents include:

- Development roadmap.
- Development log.
- Architecture documentation.
- Data flow documentation.
- Module responsibilities.
- Testing and validation documentation.
- Project state and continuity records.

The data model documentation should only change if an approved interface or model change is actually necessary.

Record the implemented table behavior accurately.

Do not describe future plot functionality as already implemented.

## 11. Scope boundaries

2.3.2 is specifically about implementing the measurement table.

It does not include:

- Scientific light-curve plotting (2.3.3).
- Table/plot synchronization (2.3.4).
- Zooming or panning.
- Plot measurement selection.
- Normalization.
- Filtering.
- Detrending.
- BLS analysis (2.4).
- Analysis operation records (2.5).
- External archive integration.
- Permanent storage architecture redesign.
- Unrelated application refactoring.

If the table implementation reveals that another capability is necessary, document the dependency and request approval rather than expanding scope automatically.

## 12. Expected deliverables

By the end of 2.3.2, the following should exist:

1. A functioning measurement table integrated into the application.
2. Accurate presentation of imported light-curve measurements.
3. Clear distinction between available measurement types.
4. Correct association of measurements and uncertainties.
5. Appropriate display of units and metadata.
6. Understandable representation of missing and invalid values.
7. Access to quality flags and cadence identifiers where available.
8. Approved measurement inspection and row-selection behavior.
9. Correct behavior when datasets or projects change.
10. Automated tests covering functionality and scientific integrity.
11. Updated project documentation.
12. A completion report identifying any remaining limitations.

## 13. Completion criteria

2.3.2 is complete when:

- The measurement table follows the approved 2.3.1 design.
- Imported measurements display correctly.
- SAP and PDCSAP measurements remain distinguishable.
- Uncertainties remain correctly associated.
- Units and time metadata are presented accurately.
- Missing and invalid measurements remain identifiable.
- Quality flags remain accessible.
- Users can inspect individual observations.
- Dataset and project changes update the table correctly.
- The table does not modify imported or persisted scientific measurements.
- Automated tests pass without regressions.
- Documentation reflects the actual implementation.

## 14. Relationship to the remaining Stage 2.3 work

1. 2.3.1 — Data inspection and presentation design

   Design prerequisite

   Establishes the approved requirements and architecture.
2. 2.3.2 — Measurement table implementation

   Current subtask

   Implements the tabular inspection interface.
3. 2.3.3 — Scientific light-curve visualization

   Implements the graphical inspection interface using the approved design.
4. 2.3.4 — Integration and completion verification

   Connects the table and plot, verifies their interaction, and assesses Stage 2.3 completion.

Important: The table should be implemented in a way that makes later plot integration straightforward, but 2.3.2 should remain independently testable and should not attempt to implement the later visualization functionality.