# Stage 2.3 — Data Table and Light-Curve Visualization

## 1. Overall objective

The objective of Stage 2.3 is to make imported astronomical light-curve data accessible for visual inspection and examination within a research project.

After completing Stage 2.2, the application should be able to import a light-curve dataset, associate it with a project, and preserve it. Stage 2.3 builds on that foundation by providing two connected ways to examine the data:

1. A measurement table for inspecting individual data points and their associated values.
2. A scientific light-curve plot for examining the overall behavior and structure of the measurements.

Both views must represent the same underlying dataset without modifying the original scientific measurements.

## 2. Proposed subsection breakdown

I recommend dividing Stage 2.3 into four subtasks.

### 2.3.1 — Data inspection and presentation design

Establish how imported light-curve data should be presented in the application before implementing the table or plot.

Work includes:

- Review the completed Stage 2.2 data model and importer.
- Review the existing application architecture and project interface.
- Identify which dataset information should appear in the table.
- Determine how users select between available measurements, such as `SAP_FLUX` and `PDCSAP_FLUX`.
- Establish how uncertainties, quality flags, missing values, and invalid measurements should be represented.
- Determine how measurement units and time representations should be communicated.
- Design how table selection and plot selection will correspond.
- Establish visualization boundaries so that displaying data cannot modify the underlying measurements.
- Identify any interface or architectural decisions that require approval.

Deliverable: An approved design for the data table, scientific plot, and their relationship to the imported dataset.

No table or plotting implementation should occur in this subtask.

### 2.3.2 — Measurement table implementation

Implement the tabular view of imported light-curve measurements.

Work includes:

- Display the imported measurements in a table.
- Display relevant measurement columns, such as time, flux, uncertainty, quality flags, and cadence identifiers where available.
- Preserve the distinction between different measurement types.
- Display units and relevant metadata.
- Make missing, non-finite, and invalid measurements identifiable.
- Support selecting and inspecting individual measurements.
- Handle datasets containing many measurements without making the interface impractical.
- Ensure the table reads from the imported dataset rather than creating an independent or altered copy of the scientific data.

Testing should verify that displayed values correspond to the underlying imported values.

Deliverable: A working measurement table integrated into the application.

### 2.3.3 — Scientific light-curve visualization

Implement the graphical representation of the imported measurements.

Work includes:

- Plot time against the selected flux measurement.
- Label axes using the actual time representation and measurement units.
- Display uncertainty information when available.
- Make missing or invalid measurements distinguishable without silently removing them from the underlying dataset.
- Support appropriate zooming, panning, and navigation.
- Allow users to select which measurement is plotted, particularly `SAP_FLUX` versus `PDCSAP_FLUX`.
- Ensure plot updates reflect the currently selected dataset and measurement.
- Preserve the original measurements; visualization must not silently normalize, filter, detrend, or otherwise transform them.

For Kepler-10b, `PDCSAP_FLUX` is the preferred starting point for the initial detection workflow, but `SAP_FLUX` must remain accessible for comparison and inspection.

Deliverable: A working scientific light-curve plot integrated into the application.

### 2.3.4 — Table/plot integration, testing, and completion verification

Connect the table and plot into a coherent inspection workflow and verify the completed Stage 2.3 functionality.

Work includes:

- Ensure both views display the same selected dataset.
- Connect table selection with the corresponding plotted measurement.
- Ensure switching between flux measurements updates the appropriate views.
- Verify uncertainty information is consistent between the table and plot.
- Verify missing values, invalid measurements, and quality flags are represented consistently.
- Test dataset switching and project switching.
- Verify that visualization does not modify imported measurements or persisted data.
- Test with controlled FITS fixtures and the real Kepler-10b dataset where available.
- Run the full test suite and check for regressions.
- Reconcile documentation with the actual implementation.
- Identify remaining limitations and determine whether Stage 2.3 meets its completion criteria.

Deliverable: A verified, documented table-and-plot inspection workflow.

## 3. Scientific integrity requirements

These requirements apply throughout Stage 2.3.

| Requirement                  | Expected behavior                                       |
| ---------------------------- | ------------------------------------------------------- |
| Original measurements        | Remain unchanged                                        |
| `SAP_FLUX` and `PDCSAP_FLUX` | Remain separately identifiable                          |
| Uncertainties                | Retained and displayed when available                   |
| Time representation          | Preserve the original time reference and scale          |
| Units                        | Display actual known units; do not invent missing units |
| Quality flags                | Remain accessible and identifiable                      |
| Missing values               | Remain represented in the underlying data               |
| Invalid measurements         | Made identifiable rather than silently discarded        |
| Normalization                | Not performed automatically                             |
| Filtering                    | Not performed automatically                             |
| Detrending                   | Not performed automatically                             |
| Visualization                | Must not modify the underlying dataset                  |

A distinction is important here: a plot may need to omit a non-finite value from the rendered line because it cannot be plotted meaningfully. That does not authorize removing the corresponding measurement from the dataset or table. The application should make such exclusions understandable to the user.

## 4. Testing strategy

Testing should cover both individual components and their integration.

Table testing

- Correct values and columns.
- Correct units and metadata.
- Missing and invalid values.
- Measurement selection.
- Large datasets.

Plot testing

- Correct time and flux values.
- Correct axis labels and units.
- Uncertainty representation.
- Missing and invalid measurements.
- Zooming and navigation.
- Switching between flux measurements.

Integration testing

- Table and plot use the same dataset.
- Selecting a measurement in one view updates the other as designed.
- Switching datasets updates both views.
- Switching projects does not display stale data.
- Viewing or navigating data does not modify the underlying measurements.

Use temporary test datasets and controlled FITS fixtures for routine tests. The real Kepler-10b file can provide an additional verification case, but the standard test suite must not depend on its absolute local path.

## 5. Documentation expectations

Documentation should be updated as implementation progresses, following the project's existing `AGENTS.md` requirements.

Likely affected documentation includes:

- Development roadmap.
- Development log.
- Architecture documentation.
- Data model documentation.
- Data flow documentation.
- Module responsibilities.
- Decisions and design records.
- Testing and validation documentation.
- Project state and continuity records.

The exact documents to update should be determined during each subtask's planning process, based on the actual repository.

## 6. Scope boundaries

Stage 2.3 should remain focused on inspecting imported light-curve data.

It does not include:

- BLS transit detection or uncertainty calculations (Stage 2.4).
- Recording analysis operations and parameters (Stage 2.5).
- Normalization, detrending, filtering, or other scientific transformations.
- External archive integration.
- A permanent redesign of the application's storage architecture.
- General-purpose plotting infrastructure for every possible astronomical data type.
- Expanding the application into a full scientific analysis environment before the planned analysis stages.

If implementation reveals that one of these capabilities is necessary, it should be documented as a dependency or future decision rather than added without approval.

## 7. Stage 2.3 completion criteria

Stage 2.3 can be considered complete when:

1. Imported light-curve measurements can be inspected in a table.
2. The same dataset can be examined in a scientific light-curve plot.
3. Users can select and inspect the available measurement types.
4. Uncertainties, units, time references, quality flags, and missing values are represented appropriately.
5. Table and plot remain synchronized.
6. Dataset and project switching work correctly.
7. The visualization workflow does not modify the original scientific measurements or persisted data.
8. Automated tests verify the functionality and its integration.
9. Documentation accurately reflects the implementation.
10. The full existing test suite passes without regressions.

## 8. Recommended implementation sequence

1. 2.3.1 — Data inspection and presentation design

   Review the completed 2.2 implementation and establish the table/plot design.
2. 2.3.2 — Measurement table implementation

   Build and test the tabular inspection interface.
3. 2.3.3 — Scientific light-curve visualization

   Build and test the plotting interface.
4. 2.3.4 — Integration, testing, and completion verification

   Connect the views, verify scientific integrity, reconcile documentation, and assess completion.

Important prerequisite: Before beginning 2.3.1, Stage 2.2 should be verified as complete against its actual implementation and completion report. Stage 2.3 depends on the data model, importer, and project persistence established there.

This gives you four separate subsection records. We can use the same process as Stage 2.2 for each: subsection overview first, then its Plan prompt, then a Build prompt revised after the Plan has been reviewed and approved.