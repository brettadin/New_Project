# PLAN PROMPT

# Stage 2.3.3 — Scientific Light-Curve Visualization
## PLAN Prompt

**MODE: PLAN ONLY — INSPECT, ANALYZE, AND DESIGN. DO NOT IMPLEMENT.**

You are working on Stage 2.3.3 of the astronomy research application.

Your task is to inspect the existing repository and prepare an implementation plan for the scientific light-curve visualization.

The objective is to allow users to visualize and inspect actual imported astronomical light-curve measurements through a scientific plot integrated into the existing application.

The plot must use the existing imported dataset and preserve the integrity of the underlying scientific measurements.

This task is planning only. Do not modify source code, tests, documentation, dependencies, project data, or Git state.

---

## 1. Required preparation

Before planning, inspect and follow:

- Repository `AGENTS.md`.
- Relevant Foundation requirements.
- Development roadmap.
- Development log.
- Architecture documentation.
- Data model documentation.
- Data flow documentation.
- Module responsibilities.
- Existing decision records.
- Testing and validation documentation.
- Project state and continuity records.
- Stage 2.2 plans, implementation reports, and completion verification.
- Approved Stage 2.3.1 design and implementation report.
- Stage 2.3.2 Plan report and approval decisions.
- Stage 2.3.2 implementation and completion report, if completed.

Follow all applicable Foundation requirements.

**Governance requirements:**

- Foundation documents are read-only.
- Do not modify Foundation requirements.
- Preserve approved architectural and scientific decisions.
- Do not assume a previous report accurately describes the current repository without verification.
- Distinguish verified facts, assumptions, recommendations, and unresolved decisions.
- Do not commit, push, reset, clean, or modify Git history.

---

## 2. Verify prerequisites

Inspect the actual repository and verify that the prerequisites for 2.3.3 are complete.

In particular, verify:

1. Stage 2.2 provides an imported light-curve data model and importer.
2. Imported measurements are associated with projects and persisted as approved.
3. The 2.3.1 design establishes the intended table and plot architecture.
4. Stage 2.3.2 has implemented the measurement table.
5. The table and project/data-access layers expose the information needed by the plot.
6. The existing application provides a suitable location for the visualization.
7. Existing dependencies support the intended plotting approach.

Inspect actual source files, interfaces, tests, and documentation.

Do not rely solely on previous implementation reports.

**Stop conditions:**

If Stage 2.2 or 2.3.2 is incomplete, identify the missing prerequisite and explain its impact.

If the 2.3.1 design or its approved decisions conflict with the current implementation, identify the discrepancy.

If a required interface or data field is unavailable, do not invent an alternative implementation.

Do not begin implementation planning that depends on an unresolved architectural decision without identifying it.

---

## 3. Inspect the actual light-curve data

Examine the current data model and imported dataset representation.

Verify the actual availability and meaning of:

- Observation timestamps.
- Time units.
- Time reference.
- Time scale.
- SAP_FLUX.
- SAP_FLUX_ERR.
- PDCSAP_FLUX.
- PDCSAP_FLUX_ERR.
- Flux units.
- Quality flags.
- Cadence identifiers.
- Missing and non-finite values.
- Dataset metadata.
- Source and provenance information.

Determine how these fields are exposed to the application.

Do not assume every imported dataset contains all Kepler-specific fields.

The initial target is the existing Kepler-10b dataset, but the design should avoid unnecessary coupling to Kepler-specific column names or conventions.

The visualization must use the existing data model rather than introducing an independent scientific dataset.

---

## 4. Review the existing plotting architecture

Inspect:

- Current plotting dependencies.
- Existing visualization modules.
- Existing PySide6 widgets and layouts.
- Application window integration.
- Data-access patterns.
- Project and dataset selection mechanisms.
- Existing signal/slot conventions.
- Existing testing patterns for UI and plotting code.

Determine whether the approved technology stack already provides everything needed.

The current approved stack includes:

- Python 3.13.
- PySide6.
- NumPy.
- SciPy.
- Astropy.
- Matplotlib.
- pytest.

Do not recommend a new dependency unless there is a specific technical reason.

If a new dependency or significant architectural change appears necessary, explain why and identify alternatives. Do not treat it as approved.

---

## 5. Design the scientific plot

Prepare a concrete design for the initial light-curve visualization.

The expected initial representation is:

- X-axis: observation time.
- Y-axis: selected flux measurement.
- Plotted values: actual imported observations.

The design should establish:

- Plot widget and module responsibilities.
- Data supplied to the plot.
- How the plot obtains the active dataset.
- How measurements are selected.
- How axis labels are generated.
- How units and time metadata are presented.
- How uncertainties are represented.
- How missing and invalid values are handled.
- How quality flags are made accessible.
- How the plot responds to dataset changes.
- Which user interactions are supported.

Follow the approved 2.3.1 design where applicable.

Do not design a general-purpose plotting framework.

### 5.1 Measurement selection

Determine how the user selects the measurement to display.

For the initial Kepler dataset, the important choices are:

- SAP_FLUX.
- PDCSAP_FLUX.

The initial default should follow the existing decision for the detection workflow: PDCSAP_FLUX.

Establish how the selection maps to the correct measurement and uncertainty fields.

For example:

| Selected measurement | Associated uncertainty |
|---|---|
| SAP_FLUX | SAP_FLUX_ERR |
| PDCSAP_FLUX | PDCSAP_FLUX_ERR |

Determine how unavailable measurements or uncertainties are represented.

Do not silently substitute one measurement for another.

### 5.2 Axis labels and metadata

Establish how the plot will represent:

- Time values.
- Time units.
- Time reference.
- Time scale.
- Flux values.
- Flux units.

Labels must be based on actual imported metadata.

Unknown metadata must remain unknown.

Do not infer time conventions or units solely from column names unless the existing importer explicitly establishes that interpretation.

Explain how labels respond when the active dataset or selected measurement changes.

### 5.3 Uncertainty visualization

Determine how available measurement uncertainties should be represented.

Consider:

- Error bars.
- Default visibility.
- Missing uncertainty values.
- Non-finite uncertainties.
- Invalid or negative uncertainties.
- Rendering performance for large datasets.
- Whether uncertainty display should be configurable.

The correct uncertainty field must always remain associated with its measurement.

Do not interpret missing uncertainty values as zero.

### 5.4 Missing and non-finite observations

Design behavior for:

- NaN timestamps.
- Infinite timestamps.
- NaN flux measurements.
- Infinite flux measurements.
- Missing flux values.
- Missing uncertainty values.
- Invalid uncertainties.
- Gaps in the time series.

The plot may omit non-finite points from the rendered line when necessary, but the underlying dataset must remain unchanged.

Explain how visual gaps or omitted points will be handled so the plot does not imply measurements exist where they do not.

### 5.5 Quality flags

Determine how quality flags should be represented or accessed.

The design must preserve nonzero quality flags.

Do not automatically remove flagged observations.

Consider whether flags should be:

- Accessible through point inspection.
- Represented through optional visual styling.
- Made available through a separate display option.
- Inspected through the existing measurement table.

Follow the approved 2.3.1 design and avoid unnecessary visual complexity.

---

## 6. Plot interaction design

Establish the exact interactions to implement.

Consider the approved design's requirements for:

- Zooming.
- Panning.
- Returning to the full dataset view.
- Inspecting individual observations.
- Displaying measurement values.
- Displaying associated uncertainties.
- Accessing quality flags and cadence identifiers.
- Identifying the selected measurement.

For each proposed interaction, explain:

1. What the user does.
2. What the application displays or changes.
3. Which component owns the interaction state.
4. Whether the interaction requires additional interfaces.
5. How it will be tested.

Do not introduce table/plot synchronization in this subtask. That belongs to 2.3.4.

If point inspection is implemented, establish how a plotted point maps back to the correct underlying observation without relying on an unstable visual index.

---

## 7. Application integration

Determine how the plot will integrate into the existing application.

Address:

### 7.1 Dataset access

- How the plot obtains the active dataset.
- Whether existing interfaces can be reused.
- How selected measurement information is supplied.
- How unnecessary data duplication is avoided.

### 7.2 Dataset switching

Determine behavior when:

- A different dataset is selected.
- The selected dataset has different available measurements.
- A dataset becomes unavailable.
- Data access fails.
- The dataset contains no usable plotted points.

The plot must not continue displaying stale measurements from a previous dataset.

### 7.3 Project lifecycle

Determine behavior when:

- A project is opened.
- A project is closed.
- A different project becomes active.
- The active project has no imported dataset.

Preserve existing project lifecycle behavior.

Do not redesign project persistence or project lifecycle architecture.

### 7.4 Empty and unavailable states

Establish the expected presentation for:

- No active project.
- No selected dataset.
- Empty datasets.
- Missing measurement fields.
- Unavailable data.
- No finite points available for plotting.
- Missing metadata.
- Plot rendering failures.

The application must not present stale or misleading plot content.

---

## 8. Performance and large-dataset strategy

Review the expected dataset sizes and determine an appropriate plotting approach.

Address:

- Efficient access to NumPy arrays.
- Avoiding unnecessary copies.
- Rendering performance.
- Error-bar rendering costs.
- Zoom and pan responsiveness.
- Point inspection overhead.
- Handling non-finite values.
- Whether any rendering optimization is necessary.

Do not introduce downsampling or other data reduction without explicitly identifying its scientific implications and obtaining approval.

If a display-only optimization is recommended, explain how the full-resolution underlying data remains available and how plotted points map to original observations.

Avoid premature optimization and unnecessary abstraction.

---

## 9. Scientific integrity requirements

The plot is a visualization of imported measurements, not a scientific processing system.

The design must preserve the following boundaries:

| Operation | 2.3.3 scope |
|---|---|
| Plot original measurements | Allowed |
| Display measurement uncertainties | Allowed |
| Select SAP or PDCSAP | Allowed |
| Display metadata and units | Allowed |
| Zoom and pan | Allowed |
| Inspect observations | Allowed |
| Omit non-finite points from rendering | Allowed, if underlying data is preserved |
| Normalize flux | Excluded |
| Detrend flux | Excluded |
| Remove outliers | Excluded |
| Automatically filter quality flags | Excluded |
| Transit fitting | Excluded |
| BLS | Excluded |
| Modify imported measurements | Excluded |

Explain how the implementation will ensure that:

- Original measurements remain unchanged.
- Display operations do not modify scientific values.
- Missing values remain in the underlying dataset.
- Quality flags remain accessible.
- SAP and PDCSAP remain distinct.
- Uncertainty associations remain correct.
- The original FITS file is not modified.

---

## 10. Testing strategy

Prepare a concrete testing plan.

Identify the relevant existing test modules and proposed new test modules.

Address the following areas.

### 10.1 Plot data and measurement selection

- Correct timestamps.
- Correct flux values.
- Correct SAP/PDCSAP selection.
- Correct uncertainty associations.
- Correct handling of unavailable fields.

### 10.2 Axis labels and metadata

- Correct time units.
- Correct time reference and scale.
- Correct flux units.
- Unknown metadata.
- Label updates after dataset changes.

### 10.3 Missing and invalid data

- NaN timestamps.
- Infinite timestamps.
- NaN flux values.
- Infinite flux values.
- Missing uncertainties.
- Invalid uncertainties.
- Empty datasets.
- No finite points available.

### 10.4 Quality flags

- Nonzero flags remain accessible.
- Flagged observations are not automatically removed.
- Any approved visual flag representation is correct.

### 10.5 Plot interactions

- Zoom.
- Pan.
- Full-view reset.
- Point inspection.
- Correct observation mapping.
- Measurement switching.

Only include interactions that the approved design requires.

### 10.6 Application integration

- Dataset switching.
- Project switching.
- Project opening and closing.
- Empty projects.
- Unavailable datasets.
- Rendering failures.
- Stale-plot prevention.

### 10.7 Scientific integrity

Verify that:

- Plotting does not modify imported measurements.
- Measurement switching does not modify imported measurements.
- Display formatting does not modify stored values.
- Rendering omissions do not remove underlying observations.
- The original source file remains unchanged.

### 10.8 Test portability

Use controlled fixtures and temporary data.

The standard test suite must not depend on the user's permanent Kepler-10b FITS file or its absolute local path.

The real dataset may be used for optional manual verification.

Do not weaken existing tests.

---

## 11. Documentation impact

Inspect the actual documentation structure and identify the documents that will need updating during implementation.

Follow the requirements in `AGENTS.md`.

Consider:

- Development roadmap.
- Development log.
- Architecture documentation.
- Data flow documentation.
- Module responsibilities.
- Testing and validation documentation.
- Project state and continuity records.
- Decision records, if an approved new decision is required.

For each affected document, explain what information should be updated.

Do not modify documentation during this planning task.

Foundation documents must remain unchanged.

---

## 12. Explicit scope boundaries

This subtask authorizes planning only for scientific light-curve visualization.

It does not authorize implementation or planning of:

- Table/plot synchronization.
- Shared table and plot selection.
- BLS or transit detection.
- Transit fitting.
- Detrending.
- Normalization.
- Scientific filtering.
- Outlier removal.
- Archive integration.
- Permanent storage redesign.
- Changes to the importer or data model.
- Unapproved dependencies.
- Unrelated refactoring.

Table/plot integration and synchronization remain part of 2.3.4.

BLS and associated uncertainty work remain part of Stage 2.4.

---

## 13. Required Plan report

Provide a structured report with the following sections.

### A. Repository and prerequisite verification
- Current repository and branch.
- Current working-tree state.
- Relevant files inspected.
- Stage 2.2 completion verification.
- 2.3.1 design verification.
- 2.3.2 implementation verification.
- Any discrepancies or incomplete prerequisites.

### B. Actual data capabilities
- Available measurement fields.
- Timestamp representation.
- Time metadata.
- Flux units.
- Uncertainty fields.
- Quality flags.
- Cadence identifiers.
- Missing and non-finite data handling.
- Relevant existing interfaces.

### C. Existing plotting architecture
- Current plotting dependencies.
- Existing visualization modules.
- Relevant UI integration points.
- Existing data-access patterns.
- Reusable components.
- Gaps that need to be addressed.

### D. Proposed plot architecture
- Proposed module and widget responsibilities.
- Data-access interfaces.
- Plot data representation.
- Measurement selection.
- Axis labeling.
- Uncertainty visualization.
- Missing-value handling.
- Quality-flag access.
- Plot state and lifecycle.

Identify specific existing files and proposed files.

### E. Interaction design
Describe each approved interaction and how it will work.

Include zooming, panning, full-view reset, point inspection, and measurement switching where applicable.

### F. Application integration
Explain dataset access, project switching, dataset switching, empty states, error handling, and stale-data prevention.

### G. Performance strategy
Explain array handling, rendering performance, uncertainty display costs, and any necessary optimization.

### H. Scientific integrity
Explain how the design preserves original measurements, metadata, uncertainties, quality flags, and source data.

Explicitly identify any potential risk of data modification or misleading visualization.

### I. Architecture and dependencies
Identify existing components to reuse, proposed interfaces, new files, and any dependency or architecture changes.

Separate approved existing technology from recommendations requiring authorization.

### J. Testing plan
Identify test modules, fixtures, test cases, scientific integrity checks, and optional real-dataset verification.

### K. Documentation impact
List each affected document and the intended updates.

### L. Risks and unresolved issues
Identify technical uncertainties, missing interfaces, performance concerns, and decisions that require user approval.

### M. Implementation breakdown
Provide a clear implementation sequence for 2.3.3.

Separate logically independent implementation steps and identify dependencies between them.

### N. Approval decisions
List every decision that requires user approval.

Do not treat recommendations as approved decisions.

### O. Readiness assessment
Conclude with one of:

- **Ready for Build:** Prerequisites and approved design are sufficient.
- **Conditionally ready:** Specific decisions or minor issues must be resolved first.
- **Not ready:** A prerequisite or architectural issue blocks implementation.

Explain the reasoning.

---

## 14. Final restrictions

- PLAN ONLY.
- Do not modify source code.
- Do not modify tests.
- Do not modify documentation.
- Do not install or update dependencies.
- Do not modify project data or the original FITS file.
- Do not implement the plot.
- Do not implement table/plot synchronization.
- Do not make unapproved architectural decisions.
- Do not commit or push.
- Preserve the current working tree.

Finish by presenting the Plan report and waiting for review and explicit authorization.

**The next step after this Plan is review and approval. Do not begin Build automatically.**


# BUILD PROMPT

# Stage 2.3.3 — Scientific Light-Curve Visualization
## BUILD Prompt

**MODE: BUILD ONLY AFTER THE 2.3.3 PLAN REPORT HAS BEEN REVIEWED AND EXPLICITLY APPROVED.**

You are implementing Subtask 2.3.3 of the astronomy research application.

Your task is to implement the approved scientific light-curve visualization.

The objective is to allow users to visualize and inspect actual imported astronomical light-curve measurements through a scientific plot integrated into the existing application.

The visualization must use the existing imported dataset and preserve the integrity of the underlying scientific measurements.

This subtask implements the plot itself. Table/plot integration and synchronization belong to Subtask 2.3.4.

---

## 1. Required preparation

Before making changes, read and inspect:

- Repository `AGENTS.md`.
- Relevant Foundation requirements.
- Development roadmap.
- Development log.
- Architecture documentation.
- Data model documentation.
- Data flow documentation.
- Module responsibilities.
- Existing decision records.
- Testing and validation documentation.
- Project state and continuity records.
- Stage 2.2 implementation and completion reports.
- Approved Stage 2.3.1 design.
- Stage 2.3.2 implementation and completion report.
- Completed 2.3.3 Plan report.
- User approval decisions from the Plan review.

Follow all applicable Foundation requirements.

Governance requirements:

- Foundation documents are read-only.
- Do not modify Foundation requirements.
- Preserve approved architectural and scientific decisions.
- Do not assume previous reports accurately describe the current repository without verification.
- Distinguish verified facts from assumptions and recommendations.
- Do not overwrite or discard existing user work.
- Do not commit, push, reset, clean, or modify Git history.
- Follow the repository's documentation-maintenance requirements.

## 2. Verify prerequisites and approved design

Before implementation, inspect the current repository and compare it with the approved Plan report.

Verify that:

1. Stage 2.2 provides the required imported light-curve data model, importer, and project integration.
2. Stage 2.3.1 established the approved visualization design.
3. Stage 2.3.2 provides the measurement table and the required dataset-access interfaces.
4. The current application architecture still matches the approved implementation approach.
5. The plotting dependencies and interfaces identified in the Plan remain available.
6. The approved design and user decisions are sufficiently specific to implement.

Pay particular attention to:

- Observation timestamps.
- Time units, reference, and scale.
- SAP_FLUX and SAP_FLUX_ERR.
- PDCSAP_FLUX and PDCSAP_FLUX_ERR.
- Flux units.
- Quality flags.
- Cadence identifiers.
- Missing and non-finite values.
- Dataset identity and source information.

**Stop conditions:**

If the current repository differs materially from the approved Plan, stop and report the discrepancy.

If a prerequisite is incomplete, do not silently implement an alternative.

If a required interface is unavailable, do not invent a replacement without authorization.

If implementation requires an unapproved architectural decision, data-model change, importer change, dependency, or storage change, stop and request approval.

Do not repair earlier subtasks as part of this task.

---

## 3. Follow the approved plotting architecture

Implement the visualization using the architecture, modules, interfaces, and responsibilities established in the approved Plan.

Use existing application conventions and reusable components where appropriate.

The plot must obtain its measurements through the established data-access interfaces.

Do not create an independent scientific dataset.

Do not unnecessarily duplicate large measurement arrays.

Keep responsibilities separated:

- Existing data-model and project layers own the scientific measurements.
- The visualization component owns plot presentation and plot-specific interaction state.
- The application interface owns integration and lifecycle behavior according to the approved architecture.

Do not redesign the architecture during implementation.

If the approved Plan identifies specific modules and interfaces, follow those exact decisions.

---

## 4. Implement the scientific light-curve plot

Implement the approved scientific plot.

The initial representation is:

- **X-axis:** Observation time.
- **Y-axis:** Selected flux measurement.
- **Plotted data:** Actual imported observations.

The plot must accurately represent the imported measurements.

### 4.1 Measurement selection

Implement the approved method for selecting which flux measurement is plotted.

For the initial Kepler workflow, the relevant measurements are:

- SAP_FLUX.
- PDCSAP_FLUX.

The initial default should follow the existing detection-workflow decision: PDCSAP_FLUX.

Requirements:

- SAP and PDCSAP remain separately identifiable.
- Selecting a measurement uses the correct underlying field.
- Switching measurements does not modify the underlying dataset.
- Unavailable measurements are communicated clearly.
- The plot must not silently substitute one measurement for another.

### 4.2 Uncertainty associations

Preserve the correct uncertainty association:

| Measurement | Uncertainty |
|---|---|
| SAP_FLUX | SAP_FLUX_ERR |
| PDCSAP_FLUX | PDCSAP_FLUX_ERR |

Implement the approved uncertainty visualization.

If error bars are included:

- Use the correct uncertainty field.
- Do not interpret missing uncertainties as zero.
- Handle non-finite or invalid uncertainties according to the approved design.
- Ensure uncertainty display does not modify the underlying values.

If uncertainties are unavailable, the plot should still display valid measurements where possible without implying that uncertainty is zero.

### 4.3 Axis labels and metadata

Implement axis labels using actual imported metadata.

The visualization should accurately communicate:

- Time values.
- Time units.
- Time reference.
- Time scale.
- Flux values.
- Flux units.
- Selected measurement identity.

Unknown metadata must remain unknown.

Do not invent units, time conventions, or reference systems.

Do not infer metadata from column names alone unless the existing importer explicitly establishes that interpretation.

Labels must update when the selected dataset or measurement changes.

### 4.4 Missing and non-finite observations

Handle:

- NaN timestamps.
- Infinite timestamps.
- NaN flux measurements.
- Infinite flux measurements.
- Missing flux values.
- Missing uncertainty values.
- Invalid uncertainties.
- Gaps in the time series.

Requirements:

- Non-finite points must not produce misleading plotted values.
- Missing measurements must not be converted to zero.
- Rendering may omit non-finite points where necessary.
- The underlying dataset must retain the original observations.
- Visual gaps must not imply measurements exist where they do not.

Do not silently remove observations from the dataset.

### 4.5 Quality flags

Implement the approved quality-flag presentation or inspection behavior.

Requirements:

- Preserve all original quality flags.
- Nonzero quality flags must not automatically remove observations.
- If quality flags are visually represented, use the approved styling.
- If flags are exposed through point inspection, map them to the correct underlying observation.

Do not introduce automatic quality filtering.

---

## 5. Implement approved plot interactions

Implement only the interactions included in the approved Plan.

These may include:

- Zooming.
- Panning.
- Returning to the full dataset view.
- Inspecting individual observations.
- Displaying measurement values.
- Displaying associated uncertainties.
- Accessing quality flags and cadence identifiers.
- Identifying the selected measurement.

For each interaction:

- Follow the approved behavior.
- Keep plot-specific state separate from scientific measurements.
- Preserve the mapping between displayed points and original observations.
- Avoid unnecessary data processing.
- Handle unavailable or invalid values appropriately.

If individual points can be inspected, ensure that the selected plotted point maps to the correct underlying observation.

Do not rely on a visual row number or unstable array position as a permanent scientific identity unless that is explicitly how the existing data model defines observation identity.

Do not add unapproved plotting features.

---

## 6. Integrate the plot into the application

Implement the approved application integration.

### 6.1 Dataset access

The plot must obtain data through the established project and dataset interfaces.

Do not create an independent dataset.

Avoid unnecessary copies of measurement arrays.

Use the approved approach for passing selected measurement information to the visualization.

### 6.2 Dataset switching

Implement the approved behavior when:

- A different dataset is selected.
- The selected dataset contains different measurement fields.
- A measurement becomes unavailable.
- Dataset access fails.
- The dataset contains no usable plotted points.

The plot must update correctly.

Prevent stale measurements from remaining visible as though they belong to the newly selected dataset.

### 6.3 Project lifecycle

Implement the approved behavior when:

- A project is opened.
- A project is closed.
- A different project becomes active.
- The active project has no imported dataset.

Preserve existing project lifecycle behavior.

Do not redesign project persistence or lifecycle architecture.

### 6.4 Empty and unavailable states

Implement the approved presentation for:

- No active project.
- No selected dataset.
- Empty datasets.
- Missing measurement fields.
- Unavailable data.
- No finite points available for plotting.
- Missing metadata.
- Plot rendering failures.

Do not leave stale or misleading plot content visible.

---

## 7. Performance and large-dataset handling

Follow the approved performance strategy.

Address:

- Efficient access to measurement arrays.
- Avoiding unnecessary data copies.
- Rendering performance.
- Error-bar rendering costs.
- Zoom and pan responsiveness.
- Point inspection overhead.
- Non-finite value handling.

Do not introduce downsampling or data reduction unless explicitly approved.

If a display-only optimization was approved:

- Preserve full-resolution underlying data.
- Maintain the mapping between rendered points and original observations.
- Document the behavior.
- Test that the optimization does not modify scientific measurements or misrepresent the data.

Avoid unnecessary abstraction and premature optimization.

---

## 8. Scientific integrity requirements

The visualization is a presentation of imported measurements, not a scientific processing system.

The implementation must preserve the following boundaries:

| Concern | Required behavior |
|---|---|
| Original FITS file | Must not be modified |
| Imported measurements | Must remain unchanged |
| SAP and PDCSAP | Remain separate |
| Uncertainties | Remain correctly associated |
| Missing values | Remain represented in underlying data |
| Non-finite values | Must not produce misleading plotted points |
| Quality flags | Must remain accessible |
| Units | Use actual available metadata |
| Time representation | Preserve original interpretation |
| Display formatting | Must not alter stored values |
| Plot interaction | Must not modify scientific measurements |
| Normalization | Not performed |
| Filtering | Not performed |
| Detrending | Not performed |
| Outlier removal | Not performed |
| Quality-based removal | Not performed |

The implementation must distinguish:

1. Original source data.
2. Imported measurements.
3. Displayed values.
4. Future derived data.

Do not silently transform, remove, replace, or reinterpret imported measurements.

---

## 9. Testing requirements

Implement tests alongside the visualization.

Follow existing testing conventions and the approved testing strategy.

### 9.1 Plot data

Test:

- Correct timestamp data.
- Correct selected flux values.
- Correct SAP/PDCSAP distinction.
- Correct uncertainty associations.
- Correct handling of unavailable measurements.
- Correct mapping between rendered points and source observations.

### 9.2 Axis labels and metadata

Test:

- Correct time units.
- Correct time reference and scale.
- Correct flux units.
- Unknown metadata.
- Label updates after dataset changes.
- Label updates after measurement switching.

### 9.3 Missing and invalid values

Test:

- NaN timestamps.
- Infinite timestamps.
- NaN flux values.
- Infinite flux values.
- Missing uncertainties.
- Non-finite uncertainties.
- Invalid uncertainties.
- Empty datasets.
- No finite points available.

Verify that rendering omissions do not remove or modify underlying observations.

### 9.4 Quality flags

Test:

- Nonzero flags remain accessible.
- Flagged observations are not automatically removed.
- Any approved visual flag representation is correct.
- Inspected flags correspond to the correct observation.

### 9.5 Plot interactions

Test the interactions required by the approved design:

- Zoom.
- Pan.
- Full-view reset.
- Point inspection.
- Observation mapping.
- Measurement switching.

### 9.6 Application integration

Test:

- Initial plot display.
- Dataset switching.
- Project switching.
- Project opening and closing.
- Empty projects.
- Empty datasets.
- Unavailable datasets.
- Rendering failures.
- Stale-plot prevention.

### 9.7 Scientific integrity

Verify that:

- Plotting does not modify imported measurements.
- Measurement switching does not modify imported measurements.
- Display formatting does not modify stored values.
- Rendering omissions do not remove underlying observations.
- Plot interactions do not modify scientific measurements.
- The original FITS file remains unchanged.

### 9.8 Test portability

Use controlled fixtures and temporary data.

The standard test suite must not depend on the user's permanent Kepler-10b FITS file or its absolute local path.

The real dataset may be used for optional manual verification.

Do not weaken existing tests or remove meaningful assertions to make the implementation pass.

Run targeted tests during implementation and the full existing test suite before completion.

Report exact commands and results.

---

## 10. Dependencies and architecture

Use the existing approved technology stack:

- Python 3.13.
- PySide6.
- NumPy.
- SciPy.
- Astropy.
- Matplotlib.
- pytest.

Follow the approved plotting-library choice in the Plan report.

Do not install additional packages unless explicitly approved.

If implementation reveals that an additional dependency, significant interface change, data-model change, importer change, or architectural redesign is necessary:

1. Stop the affected work.
2. Explain the technical reason.
3. Identify alternatives.
4. Describe the consequences.
5. Request approval.

Do not silently make the change.

---

## 11. Documentation maintenance

Follow the documentation-maintenance requirements in `AGENTS.md`.

Update relevant project documentation during implementation.

Potential documents include:

- Development roadmap.
- Development log.
- Architecture documentation.
- Data flow documentation.
- Module responsibilities.
- Testing and validation documentation.
- Project state and continuity records.
- Decision records, if a new approved decision is made.

Inspect the actual repository structure before selecting documents.

For every updated document:

- Preserve its existing structure and conventions.
- Make only relevant changes.
- Ensure descriptions match the implemented behavior.
- Distinguish implemented functionality from future planned functionality.
- Do not claim that table/plot synchronization has been completed.
- Do not claim BLS or transit detection has been implemented.
- Avoid unnecessary duplication.

Do not modify Foundation documents.

---

## 12. Explicit exclusions

This BUILD task does not authorize:

- Table/plot synchronization.
- Shared selection behavior between the table and plot.
- Table row highlighting based on plot selection.
- Plot selection highlighting in the table.
- BLS or transit detection.
- Transit fitting.
- Detrending.
- Normalization.
- Scientific filtering.
- Outlier removal.
- Automatic quality-based removal.
- Archive integration.
- Permanent storage redesign.
- Changes to the existing data model.
- Changes to the FITS importer.
- Changes to project persistence.
- Unapproved dependencies.
- Unrelated refactoring.

Table/plot integration and synchronization belong to Subtask 2.3.4.

BLS and associated uncertainty work belong to Stage 2.4.

If any excluded functionality appears necessary, document the dependency and request separate approval.

---

## 13. Completion criteria

Subtask 2.3.3 is complete when:

1. The application can plot actual imported light-curve measurements.
2. The correct timestamp and flux fields are used.
3. SAP and PDCSAP can be selected independently.
4. The correct uncertainty field accompanies the selected measurement.
5. Axis labels and units reflect available metadata.
6. Missing and non-finite values are handled correctly.
7. Quality flags remain accessible and do not automatically remove observations.
8. Approved plot interactions work correctly.
9. Project and dataset changes update the visualization correctly.
10. Empty and unavailable states are handled appropriately.
11. Large datasets are handled according to the approved strategy.
12. The underlying scientific measurements remain unchanged.
13. Automated tests cover the visualization and scientific integrity.
14. The full existing test suite passes without regressions.
15. Documentation accurately reflects the implementation.

---

## 14. Required final report

Provide a completion report containing:

### A. Summary
- What was implemented.
- Whether 2.3.3 meets its completion criteria.

### B. Prerequisite verification
- Stage 2.2 implementation reviewed.
- Approved 2.3.1 design reviewed.
- Stage 2.3.2 implementation reviewed.
- Approved 2.3.3 Plan followed.
- Any discrepancies discovered.

### C. Plot implementation
- Plot architecture and modules.
- Data-access interfaces.
- X-axis and Y-axis representation.
- Measurement selection.
- SAP/PDCSAP handling.
- Uncertainty visualization.
- Axis labels and metadata.
- Missing and non-finite value handling.
- Quality-flag handling.
- Point inspection and interactions.

### D. Application integration
- Dataset access.
- Dataset switching.
- Project switching.
- Empty and unavailable states.
- Stale-plot prevention.

### E. Performance
- Array handling.
- Rendering approach.
- Error-bar handling.
- Any optimization implemented.
- Any remaining performance limitations.

### F. Scientific integrity
- How imported measurements remain unchanged.
- How missing values and quality flags are preserved.
- How uncertainty associations are maintained.
- How display formatting is separated from stored values.
- Whether the original FITS file remained unchanged.

### G. Files changed
For every changed file:
- Path.
- Purpose.
- Summary of changes.

Also list important files inspected but intentionally left unchanged where useful.

### H. Testing and verification
- Exact test commands.
- Targeted test results.
- Full test-suite results.
- Scientific integrity test results.
- Any tests not performed and why.

### I. Documentation updates
- Documents changed.
- Summary of updates.
- Documents intentionally left unchanged.

### J. Outstanding issues
- Known limitations.
- Deferred enhancements.
- Unresolved decisions.
- Incomplete requirements.

### K. Scope confirmation

Explicitly confirm that:

- Table/plot synchronization was not implemented.
- BLS and transit detection were not implemented.
- No scientific transformations were introduced.
- No unapproved data-model, importer, persistence, or architecture changes were made.
- No unapproved dependencies were added.
- Foundation documents were not modified.
- No commits or pushes were made.

### L. Handoff to 2.3.4

Summarize:

- Plot components and interfaces implemented.
- How the active dataset is accessed.
- How measurement selection is represented.
- How plotted points map to underlying observations.
- How plot interaction state is managed.
- How the measurement table could interact with the plot.
- Any constraints the next subtask must preserve.

Confirm that the next authorized task is 2.3.4, not Stage 2.4.

---

## 15. Final restrictions

- Follow the approved 2.3.1 design and 2.3.3 Plan.
- Follow the user's explicit approval decisions.
- Preserve existing user work.
- Do not expand scope.
- Do not make unapproved architectural decisions.
- Do not commit or push.
- Leave the working tree available for user review.
- Stop after completing 2.3.3.

**This task authorizes only the approved scientific light-curve visualization. Table/plot integration and synchronization remain separate work in Subtask 2.3.4.**