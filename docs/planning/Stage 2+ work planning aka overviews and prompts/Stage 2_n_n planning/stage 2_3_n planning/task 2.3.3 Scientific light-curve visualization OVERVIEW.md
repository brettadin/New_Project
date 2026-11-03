# Stage 2.3.3 — Scientific Light-Curve Visualization

Objective: Implement a scientific plot that allows users to visualize and inspect the light-curve measurements already imported into a project and displayed in the 2.3.2 measurement table.

The plot and table should provide two ways of examining the same underlying dataset. The plot must accurately represent the measurements without modifying the original scientific data.

This subtask focuses on the visualization itself. The final integration and verification of table/plot interactions belong to 2.3.4.

## 1. Review the existing implementation

Before designing or implementing the plot, the coding agent should inspect:

- Completed Stage 2.2 data model, importer, and persistence.
- Approved 2.3.1 design.
- Completed 2.3.2 measurement table implementation.
- Existing application architecture and UI.
- Existing plotting dependencies and conventions.
- Current project and dataset access mechanisms.

The plot must use the existing imported data rather than creating its own independent copy or interpretation of the scientific dataset.

The agent should verify the actual available measurement fields and metadata rather than assuming every dataset has the same structure.

## 2. Design the scientific light-curve plot

[Using Kepler Space Telescope Data to Identify an Exoplanet | Science Project](https://images.openai.com/static-rsc-4/igOecwNaI2Ie4P98AgGICdLG_dD-8U_M68I-cLPvY0rUiK2FJ-c3TuyorutD61I5fsO-Exp_s7NMjEHErxufRUDKlJ0C5fmy2-gU7pswuixHSwByYu5WENpxSeYb53CYpU4MSvH1ERVUietXF2rOn3kn7VfsgLbdKhZUY3qFU5g?purpose=inline)

[Time Series (astropy.timeseries) — Astropy v7.2.0](https://images.openai.com/static-rsc-4/snwDbsX4_gau_UTid95X_NcqFTd_sNWioUvyCzcIAUMvrMRuixPT4jc0JpyyyuWXkxAYGBQGdaCt6CgRzU5zAMZdOUcYgq-tVhR_fDN-bEevD8zWbenL06_ph5ZRv2hADMhd6qaPekzSHTmpwUG3p0ebGqSsUT0a4RXoMzYcg9E?purpose=inline)

[Research | Michelle Kunimoto](https://images.openai.com/static-rsc-4/H0-4Y_CwfGkGuShE-r0rOp5sG5BFjqA8yDPe5yY1lCqBmfFlXUBhQ44RCyMgHQt6KC7bINJekqS9xND10-5qq89E9f-eL3D-4MK39_dwrdFLGbxOaeUg8XkTrVIGaD66QEGwm4gK9P-3OtJ-Df4lU4Ws50hXVZJXyN1WYR_90g8?purpose=inline)

9

The initial visualization should be a conventional scientific light-curve plot.

For the initial Kepler photometry workflow:

- X-axis: Observation time.
- Y-axis: Selected flux measurement.
- Data: Actual imported observations.
- Optional uncertainty representation: Measurement error bars, if supported by the approved design and available data.

The plot should make it possible to recognize the overall behavior of a light curve and inspect variations in brightness over time.

The initial implementation should not attempt to identify or fit transits. That belongs to the later BLS analysis work in Stage 2.4.

## 3. Measurement selection

The plot should support the measurement choices established in the data model and table design.

For the Kepler-10b dataset, the important distinction is:

| Measurement | Meaning                               |
| ----------- | ------------------------------------- |
| SAP_FLUX    | Simple Aperture Photometry flux       |
| PDCSAP_FLUX | Pre-search Data Conditioning SAP flux |

Users should be able to select which measurement is plotted, according to the approved design.

Important requirements:

- SAP and PDCSAP must remain separate.
- The correct uncertainty field must accompany the selected measurement.
- Switching measurements must not overwrite or transform the underlying data.
- If a measurement or its uncertainty is unavailable, the interface must communicate that accurately.

The initial default measurement should follow the decision already established for the detection workflow: PDCSAP_FLUX.

## 4. Axis labels, units, and metadata

The plot must use the actual metadata supplied by the imported dataset.

For example:

- Time axis should reflect the dataset's time representation.
- Time units should be displayed when known.
- Time reference and scale should be communicated appropriately.
- Flux axis should display the actual flux unit when available.

Do not assume every dataset uses BKJD, BJD, or the same time scale.

Unknown metadata must remain unknown. Do not invent labels or units to make the plot appear complete.

The labels should update when the selected dataset changes.

## 5. Measurement uncertainties

Where valid uncertainty measurements are available, the plot should be capable of displaying them.

For the initial dataset:

- SAP_FLUX uses SAP_FLUX_ERR.
- PDCSAP_FLUX uses PDCSAP_FLUX_ERR.

The visualization must preserve these associations.

The agent should determine the appropriate display behavior during planning, including:

- Error bars on individual measurements.
- Whether error bars should be enabled by default.
- How missing or invalid uncertainties are handled.
- Whether displaying error bars for large datasets affects responsiveness.

If uncertainty data is unavailable, the plot should still display valid flux measurements without implying that uncertainties are zero.

## 6. Missing values and quality flags

The plot must handle incomplete or invalid observations without changing the underlying dataset.

Requirements:

- NaN and infinite values must not produce misleading plotted points.
- Missing observations must not be converted to zero.
- Non-finite values may be omitted from the rendered line where necessary.
- The original observations must remain available in the dataset and table.
- Nonzero quality flags must not automatically remove observations.
- The visualization should preserve the ability to distinguish actual observations from excluded or unavailable plotted values.

The approved design should determine whether quality flags are represented through visual styling, a separate display option, or inspection through the table.

Do not introduce automatic quality filtering.

## 7. Plot interaction

The plot should provide the basic interactions approved during 2.3.1.

Potential functionality includes:

- Zooming.
- Panning.
- Returning to the full dataset view.
- Inspecting individual observations.
- Displaying measurement values and associated information.
- Identifying the selected measurement.

The exact interaction behavior should be established in the approved 2.3.1 design and 2.3.3 Plan.

Avoid adding unnecessary plotting features.

For example, scientific fitting, transit detection, detrending, normalization, and period analysis are not part of this task.

## 8. Application integration

The plot must integrate into the existing application.

It should respond appropriately to:

- Opening a project.
- Closing a project.
- Switching projects.
- Selecting another dataset.
- Switching between SAP and PDCSAP.
- Missing or unavailable data.
- Empty datasets.
- Missing optional measurements.

The plot must not continue showing measurements from a previous dataset after the active dataset changes.

The visualization should obtain its data through the established project/data-access interfaces.

## 9. Scientific integrity

This is a particularly important part of the task.

The plot is a visualization of imported measurements, not a data-processing operation.

| Operation                             | Allowed in 2.3.3?                    |
| ------------------------------------- | ------------------------------------ |
| Plot original measurements            | Yes                                  |
| Display measurement uncertainties     | Yes                                  |
| Omit non-finite points from rendering | Yes, if underlying data is preserved |
| Zoom and pan                          | Yes                                  |
| Switch SAP/PDCSAP                     | Yes                                  |
| Display metadata and units            | Yes                                  |
| Normalize flux                        | No                                   |
| Detrend flux                          | No                                   |
| Remove outliers                       | No                                   |
| Automatically filter quality flags    | No                                   |
| Perform transit fitting               | No                                   |
| Run BLS                               | No                                   |
| Modify imported measurements          | No                                   |

Any future scientific transformation must be implemented separately and recorded as derived data rather than silently changing the original measurements.

## 10. Performance and large datasets

The visualization should handle the expected initial datasets without unnecessary overhead.

The Plan should consider:

- Efficient access to measurement arrays.
- Avoiding unnecessary copies.
- Rendering performance.
- Error-bar rendering costs.
- Zooming and panning responsiveness.
- Appropriate handling of non-finite values.

Do not introduce a general-purpose plotting framework or additional dependency without approval.

Use the existing approved plotting technology and application conventions.

## 11. Testing

Tests should verify:

- Correct X-axis data.
- Correct Y-axis measurement.
- Correct measurement selection.
- Correct SAP/PDCSAP distinction.
- Correct uncertainty association.
- Correct units and axis labels.
- Missing and non-finite value handling.
- Quality-flag preservation.
- Empty and unavailable states.
- Dataset switching.
- Project switching.
- Zoom/pan/full-view behavior, where applicable.
- No modification of underlying scientific measurements.
- No regression in project lifecycle or table functionality.

Use controlled test fixtures and temporary data.

The standard test suite must not depend on the permanent Kepler-10b FITS file or its absolute path. The real dataset can be used for optional manual verification.

## 12. Documentation

Update relevant documentation in accordance with `AGENTS.md`.

Likely affected documents include:

- Development roadmap.
- Development log.
- Architecture documentation.
- Data flow documentation.
- Module responsibilities.
- Testing and validation documentation.
- Project state and continuity records.

Document the actual plotting implementation, interfaces, limitations, and deferred features.

Do not modify Foundation documents.

## 13. What 2.3.3 does not include

Keep the boundaries clear:

- 2.3.2: Measurement table.
- 2.3.3: Scientific light-curve visualization.
- 2.3.4: Table/plot integration, testing, and completion verification.

Therefore, 2.3.3 does not authorize:

- Table/plot synchronization.
- Shared selection behavior between table and plot.
- BLS or transit detection.
- Transit fitting.
- Detrending or normalization.
- Scientific filtering.
- Archive integration.
- Permanent storage redesign.
- Changes to the existing importer or data model without separate approval.

# 14. Completion criteria

2.3.3 should be considered complete when:

1. The application can plot actual imported light-curve measurements.
2. The correct time and flux fields are used.
3. SAP and PDCSAP can be selected independently.
4. The correct uncertainty field accompanies the selected measurement.
5. Axis labels and units reflect available metadata.
6. Missing and non-finite values are handled correctly.
7. Quality flags are not automatically used to discard observations.
8. Basic plot interactions work as approved.
9. Project and dataset changes update the visualization correctly.
10. Large datasets are handled appropriately.
11. The underlying scientific measurements remain unchanged.
12. Automated tests pass.
13. The full existing test suite passes.
14. Documentation reflects the implemented functionality.

## Proposed subtask workflow

| Step    | Work                                                |
| ------- | --------------------------------------------------- |
| 2.3.3.1 | Scientific plot design and implementation planning  |
| 2.3.3.2 | Plot implementation                                 |
| 2.3.3.3 | Testing, documentation, and completion verification |

This is a proposed breakdown, not a change to the approved roadmap. The existing roadmap should be checked before adopting it.

Recommended next step: Begin with a Plan-only review of the completed 2.3.2 table and the approved 2.3.1 design. Establish the exact plotting architecture, interfaces, interactions, and test strategy before implementing the visualization.