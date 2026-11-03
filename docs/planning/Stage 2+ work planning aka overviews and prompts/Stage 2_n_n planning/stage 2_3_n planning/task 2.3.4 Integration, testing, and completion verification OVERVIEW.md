# Stage 2.3.4 — Table/Plot Integration, Testing, and Completion Verification

Objective: Bring the measurement table (2.3.2) and scientific light-curve plot (2.3.3) together into one cohesive data-inspection experience.

Subtasks 2.3.2 and 2.3.3 establish the two individual visualization components. Subtask 2.3.4 ensures they work together, remain synchronized, correctly represent the same scientific dataset, and behave reliably throughout project and dataset changes.

This is the final subtask of Stage 2.3.

## 1. Review the completed implementations

Before integration, inspect the actual implementations of:

- Stage 2.2: Importer, data model, and persistence.
- Stage 2.3.1: Approved table and plot design.
- Stage 2.3.2: Measurement table.
- Stage 2.3.3: Scientific light-curve plot.

Verify their actual interfaces and behavior.

Identify:

- How the table accesses the active dataset.
- How the plot accesses the active dataset.
- How table row selection is represented.
- How plotted points map to original observations.
- How measurement selection works.
- How project and dataset switching are handled.
- Whether either component currently duplicates scientific data.

The integration must use the existing implementations rather than creating another independent data-handling system.

## 2. Implement table/plot synchronization

[08.3. How to plot a light curve — Vera C. Rubin Observatory Documentation for Data Preview 0.2](https://images.openai.com/static-rsc-4/sl7Dd_6eeZL3YCQSqKuyVo3YX9FhizmcE6ebapD7IRF4YBiMR5lZ0yy260jDcjP46PI2MqlN5Blc8WSteKlnKN4Lt7rbb-tuAJm4rrXxPuUkfEOAXOmbKksrzxJmRnSGxtq8Ik0WBU88fLWWSJ-U1Ks5PufFrB_0qDUmFopxrFg?purpose=inline)

[Help Online - Origin Help - Data Highlighter: Selecting Points in both Graph and Source Worksheet](https://images.openai.com/static-rsc-4/f2psW7NnkGFue6QwUV35IhLCjQhah687WbC4AwxtVxEQHTDINgYLecGbZExVspzBKdHXx7GF-VXz6RQ3KhjOXzUPVwlUzfkjvBvlI45zyMsvLk4zaSOZN0INjBqZvDZEStnkXyjqu7SYSnVVVe2JZK0fedSyuB3NQzVq8Ues4T4?purpose=inline)

[Data table cell | Observable documentation](https://images.openai.com/static-rsc-4/BpGdl397-ctR6pXJJ6YKs4W2OjMHmnnWI7GKai79uN4rMSRPKUXGBDytiS7uuT37rehC2l8w6he22l3T80VaVgSPAK7DBnpBec0nrcrtx60jRQJGHGDYbHDLX7D-H5VvQIbiWRB-smPteYl7VefmIE0V6bszxCO5zajfFppnuK4?purpose=inline)

7

This is the central task of 2.3.4.

The table and plot should represent the same underlying observations.

The expected interaction is:

1. A user selects an observation in the measurement table.
2. The corresponding observation is identified in the plot.
3. The plot visually indicates the selected observation.
4. A user selects or inspects a plotted observation.
5. The corresponding observation can be identified in the table.

The exact behavior should follow the approved design.

Important requirements:

- Selection must identify the correct underlying observation.
- Synchronization must work even when some observations cannot be rendered because of non-finite values.
- Visual row positions must not be mistaken for permanent scientific identities.
- Selection must not modify scientific measurements.
- Both components must remain connected to the same active dataset.

## 3. Synchronize measurement selection

The table and plot must remain consistent when the user switches between available measurements.

For example:

- SAP_FLUX.
- PDCSAP_FLUX.

The integration should establish how measurement selection is shared or communicated.

Requirements:

- The selected measurement must be clearly identifiable.
- The plot must display the correct flux field.
- The correct uncertainty field must accompany it.
- The table must continue presenting the underlying measurements accurately.
- Switching measurements must not overwrite data.
- Missing measurement fields must be handled appropriately.

The implementation should avoid unnecessary duplicated state or conflicting selections between components.

## 4. Handle project and dataset changes

Both components must respond consistently when the application state changes.

Test and implement behavior for:

- Opening a project.
- Closing a project.
- Switching projects.
- Selecting another dataset.
- Importing another dataset.
- Selecting a dataset with different available fields.
- Selecting an empty dataset.
- Encountering unavailable or corrupted data.

The table and plot must never display measurements from different datasets simultaneously.

If a dataset changes, the selection should be reset or restored according to the approved design.

Stale selections must not remain associated with the wrong dataset.

## 5. Handle missing and non-finite observations

The table and plot do not necessarily display every observation identically.

For example, a table can display a row containing a NaN flux value, while the plot may omit that point.

The integration must preserve the correspondence between them.

Requirements:

- Table rows remain available for inspection.
- Non-finite values are not converted into zero.
- Omitted plot points do not cause incorrect row-to-point mappings.
- Quality flags remain accessible.
- Nonzero quality flags do not automatically remove observations.
- Missing uncertainties do not become zero.
- Selecting an observation that cannot be plotted must still produce a meaningful table selection.

## 6. Ensure a cohesive interface

Review the combined layout and usability of the table and plot.

Consider:

- Available screen space.
- Table and plot placement.
- Resizing behavior.
- Visibility of important information.
- Measurement selection controls.
- Selection feedback.
- Empty and unavailable states.
- Consistent labeling and presentation.

The objective is a cohesive scientific inspection workspace, not a redesign of the entire application.

Only make layout changes necessary to support the approved integrated experience.

## 7. Test the complete workflow

This subtask needs broader testing than the individual table and plot implementations.

The goal is to verify the combined experience.

### Table/plot interaction

Test:

- Selecting a table row highlights the corresponding plot observation.
- Selecting a plotted observation identifies the corresponding table row.
- Selection remains correct when non-finite points are omitted from rendering.
- Selection changes correctly when the measurement changes.
- Invalid or unavailable observations remain inspectable through the table.
- Selection does not modify scientific measurements.

### Dataset and project behavior

Test:

- Switching datasets updates both components.
- Switching projects updates both components.
- Closing a project clears or resets both components correctly.
- Empty projects are handled.
- Empty datasets are handled.
- Unavailable datasets do not leave stale data visible.
- Failed data access does not leave inconsistent component states.

### Scientific integrity

Verify:

- Both components use the same underlying dataset.
- SAP and PDCSAP remain distinct.
- Uncertainties remain correctly associated.
- Missing values remain preserved.
- Quality flags remain accessible.
- Units and time metadata remain accurate.
- No transformations are introduced.
- Original source files remain unchanged.

### Regression testing

Run:

- New integration tests.
- Existing table tests.
- Existing plot tests.
- Relevant project lifecycle tests.
- The complete test suite.

Use controlled fixtures and temporary directories. The standard suite must not depend on the permanent Kepler-10b FITS file or its absolute path.

## 8. Documentation and completion verification

Update relevant documentation according to `AGENTS.md`.

Potential documents:

- Development roadmap.
- Development log.
- Architecture documentation.
- Data flow documentation.
- Module responsibilities.
- Data model documentation, if genuinely necessary.
- Testing and validation documentation.
- Project state and continuity records.

Verify that documentation accurately describes:

- The measurement table.
- The scientific plot.
- Their synchronization behavior.
- Selection mapping.
- Dataset and project switching.
- Known limitations.
- Deferred functionality.

Then review the completed Stage 2.3 implementation against its original objectives and Foundation requirements.

## 9. Scientific integrity requirements

The integration must preserve the existing scientific boundaries.

| Requirement             | Expected behavior               |
| ----------------------- | ------------------------------- |
| Original measurements   | Unchanged                       |
| SAP and PDCSAP          | Remain separate                 |
| Uncertainties           | Correctly associated            |
| Missing values          | Preserved                       |
| Non-finite values       | Remain identifiable             |
| Quality flags           | Accessible                      |
| Units and time metadata | Accurate                        |
| Table/plot selection    | References correct observations |
| Plot omissions          | Do not remove underlying data   |
| Normalization           | Not introduced                  |
| Detrending              | Not introduced                  |
| Filtering               | Not introduced                  |
| BLS                     | Not introduced                  |

The table and plot are inspection tools. They must not silently process or modify scientific measurements.

## 10. Explicit exclusions

2.3.4 does not authorize:

- BLS implementation.
- Transit detection.
- Transit fitting.
- Detrending.
- Normalization.
- Outlier removal.
- Quality-based filtering.
- Archive integration.
- Permanent storage redesign.
- Changes to the FITS importer.
- Unrelated application redesign.
- Unapproved architectural changes.

These belong to other stages or require separate approval.

## 11. Completion criteria

Stage 2.3 completion target

Stage 2.3.4 is complete when:

1. The measurement table and scientific plot operate together.
2. Both represent the same active dataset.
3. Table-to-plot selection synchronization works.
4. Plot-to-table selection synchronization works.
5. Measurement switching remains consistent.
6. Missing and non-finite observations are mapped correctly.
7. Project and dataset switching update both components.
8. Empty and unavailable states are handled consistently.
9. The integrated interface is usable.
10. Scientific measurements remain unchanged.
11. Automated integration and regression tests pass.
12. Documentation reflects the completed implementation.
13. The full test suite passes.
14. Stage 2.3's completion status is accurately assessed and recorded.

## Proposed Stage 2.3 workflow recap

| Subtask | Responsibility                                    | Status                                 |
| ------- | ------------------------------------------------- | -------------------------------------- |
| 2.3.1   | Data inspection and presentation design           | Completed when approved and documented |
| 2.3.2   | Measurement table implementation                  | Pending verification                   |
| 2.3.3   | Scientific light-curve visualization              | Pending verification                   |
| 2.3.4   | Integration, testing, and completion verification | Next                                   |

The statuses of 2.3.2 and 2.3.3 should be confirmed from their actual implementation reports and repository state.

## What comes after Stage 2.3?

The next major stage is Stage 2.4 — BLS Transit Search with Uncertainty.

That moves the application beyond inspecting astronomical measurements and into scientific analysis:

- Applying Box Least Squares to imported light curves.
- Searching for periodic transit-like signals.
- Estimating transit periods and related parameters.
- Assessing uncertainty.
- Evaluating candidate detections.
- Testing against appropriate positive and negative controls.

Stage 2.3 should establish a reliable data-inspection foundation before those analysis capabilities are introduced.