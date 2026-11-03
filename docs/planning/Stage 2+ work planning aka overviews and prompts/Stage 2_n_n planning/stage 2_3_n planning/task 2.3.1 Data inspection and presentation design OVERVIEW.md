# 2.3.1 — Data Inspection and Presentation Design

## 1. Objective

The purpose of 2.3.1 is to establish how imported astronomical light-curve data will be presented and inspected in the application before implementing the measurement table or scientific plot.

This subtask is primarily about reviewing the existing implementation, identifying presentation requirements, and designing how the two views will work together.

The goal is to make sure the table and plot are based on the actual scientific data model established in Stage 2.2, rather than designing interfaces around assumptions about what the data contains.

By the end of this subtask, there should be an approved design that can guide implementation in 2.3.2 and 2.3.3.

## 2. Review the existing implementation

Before making design decisions, inspect the completed Stage 2.2 implementation.

This should include:

- The light-curve data model established in 2.2.1.
- The FITS importer and validation behavior established in 2.2.2.
- Project integration and persistence established in 2.2.3.
- The Stage 2.2 completion and testing results from 2.2.4.
- Existing application windows, widgets, layouts, and navigation.
- Existing architecture, data-flow, and module-responsibility documentation.
- Current tests and established coding conventions.

The purpose is to understand what information is actually available and how the application currently accesses it.

For example, the design should establish whether the imported dataset exposes separate measurement arrays for `SAP_FLUX` and `PDCSAP_FLUX`, how their uncertainties are associated with them, and how missing values and quality flags are represented.

Important: Do not assume that the current implementation matches the original plans. Verify the actual code and tests.

## 3. Design the measurement table

Establish what information users should be able to inspect in the table.

### 3.1 Table contents

Determine which fields should be displayed, considering the information available in the imported dataset.

Potential columns include:

| Field           | Purpose                           |
| --------------- | --------------------------------- |
| Time            | Observation timestamp             |
| SAP_FLUX        | Original aperture photometry flux |
| SAP_FLUX_ERR    | Associated uncertainty            |
| PDCSAP_FLUX     | Pipeline-corrected flux           |
| PDCSAP_FLUX_ERR | Associated uncertainty            |
| SAP_QUALITY     | Pipeline quality flags            |
| CADENCENO       | Observation cadence identifier    |

The final selection should depend on the actual data model and the design of the table.

The design should also consider:

- Whether all available columns should be visible by default.
- Whether users can hide or show columns.
- How units are communicated.
- Whether metadata belongs in the table, a separate information area, or both.
- How missing or invalid values are displayed.
- How large datasets will be handled without making the interface impractical.

The goal is to provide useful scientific information without overcrowding the interface.

### 3.2 Measurement inspection

Determine how users will inspect individual measurements.

For example:

- Selecting a row.
- Identifying the selected measurement.
- Displaying additional information about that measurement.
- Making missing or invalid values understandable.
- Showing associated uncertainty and quality information.

The design should establish what happens when a user selects a measurement and how that selection will relate to the plot.

## 4. Design the scientific plot

Establish how the imported light curve should be represented graphically.

### 4.1 Plot contents

The initial plot should represent:

- Time on the horizontal axis.
- A selected flux measurement on the vertical axis.
- Uncertainty information when available.
- Missing or invalid measurements in an understandable way.

The design should establish:

- How axis labels are generated.
- How known units are displayed.
- How the time reference and time scale are communicated.
- How the selected flux measurement is identified.
- How missing or invalid values affect the rendered line.
- Whether quality information should be represented visually or remain available through the table and metadata.

Axis labels must reflect the actual imported data. The application must not invent units or time conventions when metadata is unavailable.

### 4.2 Measurement selection

A particularly important design decision concerns the ability to switch between measurement types.

For Kepler-10b, the user should be able to inspect both:

- `SAP_FLUX`
- `PDCSAP_FLUX`

These must remain distinguishable as separate measurements.

The design should determine how users select which measurement is plotted and how its associated uncertainty is selected.

`PDCSAP_FLUX` is the preferred starting point for the initial detection workflow, but that does not mean the application should hide or discard `SAP_FLUX`.

### 4.3 Plot navigation

Determine what navigation capabilities are appropriate for the initial implementation.

Consider:

- Zooming into a region of the light curve.
- Panning across the time range.
- Returning to the full dataset view.
- Inspecting individual plotted measurements.
- Handling datasets with many observations.

The objective is to provide practical scientific inspection tools without introducing unnecessary plotting features.

## 5. Establish how the table and plot work together

This is one of the most important parts of 2.3.1.

The table and plot should not behave like two unrelated displays. They should provide complementary ways to examine the same underlying measurements.

The design should establish:

### 5.1 Shared dataset

- Both views use the same selected dataset.
- Switching datasets updates both views.
- Switching projects does not leave stale measurements visible.
- Neither view maintains an independently modified scientific dataset.

### 5.2 Measurement selection

Determine how selections relate between the two views.

For example:

1. A user selects a row in the table.
2. The corresponding observation is identified on the plot.
3. A user selects a plotted observation.
4. The corresponding table row is identified.

The exact interaction can be decided during planning. The important point is that the relationship is designed before implementation.

### 5.3 Measurement type selection

Determine how switching between `SAP_FLUX` and `PDCSAP_FLUX` affects the table and plot.

For example, the application might display both measurements in the table while allowing the user to choose which one is plotted.

This is a design question, not a predetermined implementation requirement.

## 6. Establish scientific integrity boundaries

The visualization system must not alter the imported scientific measurements.

The design should explicitly establish the distinction between:

1. Original source data: The information contained in the original FITS file.
2. Imported data: The application's representation of those measurements.
3. Displayed data: How the measurements are presented in the table and plot.
4. Derived data: Measurements or values produced by future scientific operations.

For this subtask, the table and plot should only inspect and present the imported data.

The design must account for the following:

| Concern               | Required behavior                               |
| --------------------- | ----------------------------------------------- |
| Original measurements | Remain unchanged                                |
| Missing values        | Remain represented in the dataset               |
| Non-finite values     | Remain identifiable                             |
| Quality flags         | Remain accessible                               |
| Uncertainties         | Remain associated with the correct measurements |
| Units                 | Use actual available metadata                   |
| Time references       | Preserve original interpretation                |
| Normalization         | Not performed automatically                     |
| Filtering             | Not performed automatically                     |
| Detrending            | Not performed automatically                     |
| Plot rendering        | Must not modify underlying measurements         |

A plot may need to skip a non-finite value when rendering a line. That is a presentation limitation, not permission to remove the value from the imported dataset.

The design should explain how these situations will be communicated to the user.

## 7. Review architecture and implementation boundaries

Before implementation, determine how the new functionality should fit into the existing application.

Consider:

- Whether the table and plot should be separate widgets or components within a shared interface.
- Which modules should own presentation responsibilities.
- How the views receive access to the selected dataset.
- How dataset selection is communicated.
- How table and plot selection are synchronized.
- How measurement selection is represented.
- How the application avoids duplicating or modifying scientific data.
- Whether existing dependencies and visualization tools are sufficient.

The design should follow the existing architecture where practical.

It should not introduce a new plotting framework, dependency, data-storage system, or major architectural redesign without justification and approval.

## 8. Establish the testing strategy

Although implementation happens in later subtasks, the design should identify how the functionality will be tested.

Potential testing areas include:

Data presentation

- Displayed values match the imported dataset.
- Units and time representations are correct.
- Missing and invalid values are represented appropriately.
- Uncertainties remain associated with the correct measurements.

Selection behavior

- Selecting a table row identifies the corresponding plot measurement.
- Selecting a plot measurement identifies the corresponding table row.
- Switching measurement types updates the plot correctly.

Dataset and project behavior

- Switching datasets updates both views.
- Switching projects does not display stale data.
- Empty or unavailable datasets are handled appropriately.

Scientific integrity

- Displaying data does not modify the underlying measurements.
- Plot navigation does not modify the dataset.
- Missing values and quality flags are not silently removed.

The test design should use controlled datasets and fixtures rather than depending on the user's permanent Kepler-10b file.

## 9. Documentation requirements

The planning process should identify which existing documents will need updates during later implementation.

Likely affected documentation includes:

- `docs/ECAS_development_plan.md` or the current development roadmap.
- Development log.
- Architecture documentation.
- Data model documentation, if presentation interfaces affect it.
- Data flow documentation.
- Module responsibilities.
- Decisions and design records.
- Testing and validation documentation.
- Project state and continuity records.

The actual files should be identified by inspecting the repository.

Any new architectural or interface decisions should be recorded in the project's established decision documentation.

## 10. Explicit exclusions

Subtask 2.3.1 is a design and planning task.

It does not include:

- Implementing the measurement table.
- Implementing the scientific plot.
- Adding plot navigation controls.
- Implementing table/plot synchronization.
- Changing the light-curve data model without approval.
- Modifying imported measurements.
- Implementing normalization, filtering, or detrending.
- Implementing BLS or other scientific analysis.
- Recording analysis operations.
- Changing permanent storage architecture.
- Integrating external astronomical archives.

Those activities belong to later subtasks or stages.

## 11. Expected deliverables

By the end of 2.3.1, the planning and approval process should produce:

1. Repository review: Verified understanding of the completed Stage 2.2 implementation and existing application architecture.
2. Table design: Defined presentation requirements, columns, metadata, and measurement inspection behavior.
3. Plot design: Defined plotted measurements, axis labels, uncertainties, missing-value behavior, and navigation requirements.
4. Selection design: Defined how table selection, plot selection, and measurement-type selection should interact.
5. Scientific integrity requirements: Explicit boundaries preventing visualization from altering imported data.
6. Architecture design: Identified components, interfaces, and responsibilities needed for implementation.
7. Testing plan: Defined how the table, plot, and their interaction will be verified.
8. Documentation plan: Identified the documents that will require updates.
9. Approval decisions: Identified any unresolved design choices requiring your authorization.
10. Implementation boundaries: Clear separation between 2.3.2, 2.3.3, and 2.3.4.

## 12. Completion criteria

Subtask 2.3.1 is complete when:

- The actual Stage 2.2 implementation has been reviewed.
- The table and plot requirements are defined.
- Measurement selection and table/plot interaction are designed.
- Scientific integrity requirements are explicit.
- The proposed architecture fits the existing application.
- Testing and documentation requirements are established.
- Unresolved decisions have been identified and approved where necessary.
- A sufficiently detailed implementation design exists for 2.3.2 and 2.3.3.

Planning complete when design is approved

No implementation should occur during 2.3.1. The next step will be to prepare a Plan prompt that instructs the coding agent to inspect the repository, verify the Stage 2.2 foundation, and produce this design based on the actual code rather than assumptions.