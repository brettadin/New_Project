# PLAN PROMPT

# Stage 2.3.2 — Measurement Table Implementation
## PLAN Prompt

**MODE: PLAN ONLY. Do not implement anything or modify files.**

You are planning Subtask 2.3.2 of the astronomy research application.

Your task is to inspect the current repository, verify the prerequisites, review the approved 2.3.1 design, and produce a detailed implementation plan for the measurement table.

The objective is to implement a table that allows users to inspect imported astronomical light-curve measurements while preserving the underlying scientific data.

This task concerns the measurement table only. Scientific plotting and table/plot integration belong to later subtasks.

---

## 1. Project governance and required reading

Before planning, read and follow the repository's `AGENTS.md`.

Also review the relevant Foundation requirements and project documentation, including:

- Development roadmap.
- Development log.
- Architecture documentation.
- Data model documentation.
- Data flow documentation.
- Module responsibilities.
- Existing decision records.
- Testing and validation documentation.
- Project state and continuity records.
- Approved Stage 2.2 plans, implementation reports, and completion report.
- Approved Stage 2.3.1 design and implementation report.

Follow all applicable Foundation requirements.

**Important governance rules:**

- Foundation documents are read-only. Do not modify them.
- Preserve existing project decisions and architectural boundaries.
- Do not introduce unapproved architectural changes.
- Do not commit, push, reset, clean, or otherwise modify Git history.
- Do not overwrite or discard existing user work.
- Follow the repository's documentation-maintenance requirements when identifying future documentation changes.
- Distinguish verified implementation facts from historical reports, assumptions, recommendations, and unresolved questions.

If required documentation is missing, identify that fact rather than inventing its contents.

## 2. Prerequisite verification

Before planning implementation, verify the following prerequisites.

### 2.1 Stage 2.2 — Light-curve import

Inspect the actual implementation of:

- 2.2.1 — FITS inspection and data-model design.
- 2.2.2 — FITS import and validation.
- 2.2.3 — Project integration and provisional persistence.
- 2.2.4 — Testing, documentation, and completion verification.

Confirm that the application can access imported light-curve measurements and their associated metadata through the existing interfaces.

Pay particular attention to:

- Time measurements and their representation.
- SAP flux measurements.
- PDCSAP flux measurements.
- Associated uncertainty fields.
- Flux units.
- Time units, reference, and scale.
- Quality flags.
- Cadence identifiers.
- Missing and non-finite values.
- Validation warnings.
- Dataset identity and source information.
- Project association and persistence.

Do not assume every dataset contains every field.

### 2.2 Stage 2.3.1 — Approved presentation design

Review the actual 2.3.1 completion report and the user's approved decisions.

Verify the approved requirements for:

- Table structure.
- Default and optional columns.
- Units and metadata presentation.
- Missing and invalid value presentation.
- Measurement inspection.
- Row selection.
- Large-dataset handling.
- Dataset and project switching.
- Architecture and component responsibilities.
- Scientific integrity.
- Testing requirements.

The approved 2.3.1 design is the specification for this task.

Do not independently redesign it.

### 2.3 Prerequisite gate

If Stage 2.2 or 2.3.1 is incomplete, inconsistent, or does not provide the interfaces needed for the table, identify the problem and explain its impact.

Do not implement or repair earlier subtasks as part of this task.

If a prerequisite prevents reliable planning, stop and report the issue.

Otherwise, continue.

## 3. Inspect the current application architecture

Review the actual repository and determine how the measurement table should fit into the application.

Inspect:

- Main application window.
- Current navigation and layout.
- Existing project and dataset selection mechanisms.
- Light-curve data model.
- FITS importer.
- Project data-access and persistence interfaces.
- Existing table or data-display widgets.
- Existing model/view patterns, if any.
- Current dependencies and configuration.
- Testing conventions.

Determine which existing components can be reused.

Identify the smallest appropriate implementation that follows the approved 2.3.1 architecture.

The table must remain a presentation component that reads from the existing scientific data model.

Do not introduce a new storage mechanism, duplicate scientific dataset, or unnecessary architectural layer.

Do not introduce dependencies without justification and approval.

## 4. Plan measurement table implementation

Use the approved 2.3.1 design to establish exactly how the table will be implemented.

### 4.1 Table structure

Determine:

- Which columns will be displayed by default.
- Which additional columns will be available.
- How columns map to actual fields in the data model.
- How column headers identify their measurements.
- How units are communicated.
- How time metadata is presented.
- How dataset-level metadata is made accessible.
- Whether column visibility or ordering is required.
- How the table handles datasets with different available fields.

For Kepler-10b, consider the available measurements:

- `TIME`
- `SAP_FLUX`
- `SAP_FLUX_ERR`
- `PDCSAP_FLUX`
- `PDCSAP_FLUX_ERR`
- `SAP_QUALITY`
- `CADENCENO`

Verify actual field names and availability against the current implementation.

Do not hardcode assumptions that every dataset contains these columns.

### 4.2 Measurement identity and uncertainty associations

Determine how the table will preserve the distinction between measurement types.

In particular:

- `SAP_FLUX` and `PDCSAP_FLUX` must remain separately identifiable.
- Their uncertainties must remain associated with the correct flux measurement.
- Missing uncertainty fields must be handled appropriately.
- Switching or displaying measurement types must not cause values or uncertainties to become mismatched.

`PDCSAP_FLUX` is the preferred starting point for the initial detection workflow, but `SAP_FLUX` must remain available for inspection and comparison.

Do not silently substitute one for the other.

### 4.3 Missing and invalid values

Determine how the table will represent:

- Missing values.
- NaN values.
- Positive and negative infinity.
- Invalid measurements.
- Unavailable fields.
- Nonzero quality flags.
- Relevant validation warnings.

The display must distinguish missing information from actual measured values.

A missing measurement must not be displayed as zero.

A nonzero quality flag must not automatically cause its associated observation to disappear.

Determine how the approved design will communicate these conditions to the user.

### 4.4 Measurement inspection and selection

Plan the approved measurement inspection behavior.

Determine:

- How users select a row.
- How the selected observation is identified.
- What additional measurement information is available.
- How uncertainties and quality information can be inspected.
- How missing or invalid values are communicated.
- How selection is represented internally.
- How the selection can later be communicated to the plot implementation in 2.3.3 and 2.3.4.

Do not implement plot selection or table/plot synchronization.

The table should nevertheless be designed so later integration does not require unnecessary redesign.

## 5. Plan large-dataset handling

Astronomical light curves may contain thousands or substantially more observations.

Review the expected dataset sizes and determine an appropriate implementation approach.

Consider:

- Whether the existing application can display the expected number of rows efficiently.
- Whether a model/view approach is appropriate.
- Whether data should be accessed lazily or loaded into a table model.
- Avoiding unnecessary duplication of measurement arrays.
- Avoiding expensive operations during scrolling or row selection.
- Efficient formatting of displayed values.
- Scrolling and navigation.
- Memory use.

Pagination, sorting, filtering, and column customization should only be included if required by the approved design or justified by actual usability needs.

Distinguish essential initial functionality from optional enhancements.

Do not overengineer the table.

## 6. Plan application integration

Determine how the measurement table will integrate with the existing application.

Address:

### 6.1 Dataset access

- How the table receives the selected dataset.
- Which existing service or interface provides access.
- How it avoids creating an independent copy of the scientific dataset.
- How it handles unavailable or invalid dataset access.

### 6.2 Dataset switching

Determine how the table responds when:

- A different dataset is selected.
- A dataset is added to the active project.
- A dataset becomes unavailable.
- A dataset fails to load.

Ensure that the table cannot continue displaying stale measurements as though they belong to the newly selected dataset.

### 6.3 Project switching

Determine how the table responds when:

- A project is opened.
- A project is closed.
- A different project becomes active.
- The active project contains no imported light-curve dataset.

Preserve existing project lifecycle behavior.

Do not modify project persistence or project lifecycle architecture as part of this task unless a specific issue is identified and separately approved.

### 6.4 Empty and unavailable states

Plan how the table behaves when:

- No project is active.
- No dataset is selected.
- The selected project has no light-curve data.
- The dataset is empty.
- The dataset cannot be accessed.
- Required display information is unavailable.

The interface should communicate these states clearly rather than displaying misleading or stale data.

## 7. Scientific integrity requirements

The table is an inspection interface, not a scientific processing system.

The implementation must preserve the distinction between:

1. Original source data.
2. Imported measurements.
3. Displayed values.
4. Future derived data.

Establish how the implementation will guarantee:

- Original FITS files are not modified.
- Imported measurements remain unchanged.
- SAP and PDCSAP measurements remain distinct.
- Uncertainties remain associated with the correct measurements.
- Missing values remain represented.
- Non-finite values remain identifiable.
- Quality flags remain accessible.
- Known units and time references are preserved.
- Unknown metadata is not invented.
- Display formatting does not change stored measurements.
- Row selection does not modify scientific data.
- Dataset switching does not alter persisted measurements.

Do not implement:

- Normalization.
- Filtering.
- Detrending.
- Outlier removal.
- Quality-based observation removal.
- Unit conversion that changes the underlying measurements.
- Any other scientific transformation.

If a display-only conversion or formatting operation is proposed, explain how it will remain separate from the stored scientific values.

## 8. Testing strategy

Develop a detailed testing plan for the measurement table.

### 8.1 Table structure and displayed values

Plan tests for:

- Correct columns.
- Correct row count.
- Correct values.
- Correct measurement identities.
- Correct uncertainty associations.
- Correct units and metadata.
- Datasets with optional or missing fields.
- Large datasets.

### 8.2 Missing and invalid values

Plan tests for:

- Missing values.
- NaN values.
- Positive and negative infinity.
- Unavailable fields.
- Nonzero quality flags.
- Validation warnings.
- Ensuring missing measurements are not displayed as zero.
- Ensuring observations are not silently removed.

### 8.3 Selection and inspection

Plan tests for:

- Row selection.
- Selected observation identity.
- Associated uncertainty access.
- Quality flag access.
- Selection behavior with missing values.
- Selection behavior after dataset changes.

### 8.4 Application integration

Plan tests for:

- Initial table display.
- Dataset switching.
- Project switching.
- Project opening and closing.
- Empty projects.
- Empty datasets.
- Unavailable datasets.
- Failed dataset access.
- Prevention of stale data display.

### 8.5 Scientific integrity

Plan tests verifying that:

- Displaying the table does not modify measurements.
- Selecting rows does not modify measurements.
- Formatting values does not modify stored values.
- Switching datasets does not modify persisted measurements.
- Original source files remain unchanged.

### 8.6 Test data and portability

Routine tests must use controlled fixtures and temporary data.

The standard test suite must not depend on the user's permanent Kepler-10b FITS file or its absolute local path.

The real dataset may be used for optional manual verification.

Do not weaken existing tests to accommodate the implementation.

## 9. Dependencies and implementation approach

Determine whether the existing technology stack is sufficient.

The current approved stack includes:

- Python 3.13.
- PySide6.
- NumPy.
- SciPy.
- Astropy.
- Matplotlib.
- pytest.

Do not assume a new dependency is required.

If an additional library or significant architectural change appears necessary:

1. Explain the problem it solves.
2. Identify alternatives using existing dependencies.
3. Explain the maintenance and architectural consequences.
4. Request approval before including it in the implementation.

Provide a proposed implementation sequence with clear milestones.

For each milestone, identify:

- Files or modules expected to change.
- Responsibilities.
- Relevant tests.
- Documentation updates.
- Dependencies on earlier milestones.

Do not write implementation code.

## 10. Documentation impact assessment

Identify the documents that will need updates during implementation.

Consider:

- Development roadmap.
- Development log.
- Architecture documentation.
- Data model documentation, only if necessary.
- Data flow documentation.
- Module responsibilities.
- Decision records.
- Testing and validation documentation.
- Project state and continuity records.

Use the actual repository structure.

For each affected document, explain what needs to change and why.

Follow `AGENTS.md` documentation-maintenance requirements.

Do not modify documentation during this planning task.

## 11. Scope boundaries

This task concerns planning the measurement table implementation only.

It does not authorize:

- Implementing the measurement table.
- Implementing scientific plotting.
- Implementing table/plot synchronization.
- Adding plot navigation.
- Changing the light-curve data model.
- Changing the FITS importer.
- Changing project persistence.
- Implementing scientific transformations.
- Normalizing measurements.
- Filtering measurements.
- Detrending measurements.
- Implementing BLS or other scientific analysis.
- Recording analysis operations.
- Integrating external astronomical archives.
- Redesigning storage architecture.
- Unrelated application refactoring.

These activities belong to later subtasks or require separate approval.

## 12. Required report structure

Produce a detailed planning report with the following sections:

### A. Repository and project-state findings
- Current branch and Git working-tree status.
- Relevant source files and modules.
- Relevant documentation.
- Existing table and data-access architecture.
- Distinguish local repository findings from historical reports.

### B. Prerequisite verification
- Stage 2.2 implementation status.
- Stage 2.3.1 design and approval status.
- Actual interfaces available.
- Any discrepancies or limitations.

### C. Data model and table requirements
- Available fields.
- Measurement representations.
- Uncertainty associations.
- Time metadata.
- Units.
- Quality flags.
- Missing and non-finite values.
- Dataset metadata.

### D. Table implementation design
- Proposed table architecture.
- Columns and headers.
- Default and optional visibility.
- Units and metadata presentation.
- Missing and invalid value handling.
- Measurement inspection.
- Selection behavior.

### E. Large-dataset strategy
- Expected data volume.
- Proposed model/view or other approach.
- Memory considerations.
- Performance considerations.
- Any justified optional features.

### F. Application integration
- Dataset access.
- Project integration.
- Dataset switching.
- Project switching.
- Empty and unavailable states.
- Stale-data prevention.

### G. Scientific integrity assessment
- How imported measurements remain unchanged.
- How display formatting is separated from stored values.
- How uncertainties and measurement identities are preserved.
- Potential integrity risks and mitigations.

### H. Architecture and dependencies
- Proposed modules and components.
- Existing modules to reuse.
- Interfaces and data flow.
- Dependencies.
- Any proposed changes requiring approval.

### I. Testing strategy
- Unit tests.
- Integration tests.
- Test fixtures.
- Regression tests.
- Scientific integrity tests.
- Large-dataset tests.
- Optional real-dataset verification.

### J. Documentation impact
- Exact documents affected.
- Proposed updates.
- Missing or inconsistent documentation.

### K. Risks, limitations, and unresolved questions
Classify findings as:
- Verified issue.
- Potential issue.
- Assumption.
- Recommendation.
- Approval required.
- Deferred enhancement.

### L. Implementation breakdown
Provide an ordered implementation sequence.

For each milestone, specify:
- Objective.
- Expected files or modules.
- Functionality.
- Tests.
- Documentation.
- Completion criteria.

### M. Approval decisions
List every design, interface, dependency, or architectural decision requiring my approval.

For each decision, provide:
- The question.
- Available options.
- Your recommendation.
- Reasoning.
- Consequences of each option.

Do not make approval-dependent decisions on my behalf.

### N. Readiness assessment
Conclude whether 2.3.2 is:
- Ready for approval.
- Ready with identified conditions.
- Blocked by prerequisite or architectural issues.

Explain what must happen before implementation can begin.

---

## 13. Final restrictions

This is PLAN ONLY.

- Do not create or modify source files.
- Do not create or modify tests.
- Do not modify documentation.
- Do not install dependencies.
- Do not modify project configuration.
- Do not modify scientific data or the original FITS file.
- Do not implement any part of 2.3.2, 2.3.3, or 2.3.4.
- Do not modify Foundation documents.
- Do not commit or push.
- Do not make unapproved architectural decisions.

You may inspect files, inspect the repository, and run existing tests if doing so is useful and safe. If you run tests, report the exact commands and results. Clearly distinguish tests actually executed from tests merely inspected.

**Stop after producing the planning report. Wait for review and explicit approval before making any changes.**


# BUILD PROMPT

# Stage 2.3.2 — Measurement Table Implementation
## BUILD Prompt

**MODE: BUILD ONLY AFTER THE 2.3.2 PLAN REPORT HAS BEEN REVIEWED AND EXPLICITLY APPROVED.**

You are implementing Subtask 2.3.2 of the astronomy research application.

Your task is to implement the approved measurement table design, integrating it into the existing application so users can inspect imported astronomical light-curve measurements.

The table must present the actual imported scientific measurements without modifying the underlying dataset.

This subtask covers the measurement table only. Scientific plotting and table/plot integration belong to later subtasks.

---

## 1. Required preparation

Before making changes, read:

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
- Stage 2.2 plans, implementation reports, and completion report.
- Approved 2.3.1 design and implementation report.
- Completed 2.3.2 Plan report.
- The user's explicit approval and any decisions made during Plan review.

Follow all applicable Foundation requirements.

**Important governance rules:**

- Foundation documents are read-only. Do not modify them.
- Preserve existing project decisions and architectural boundaries.
- Do not introduce unapproved architectural changes.
- Do not commit, push, reset, clean, or otherwise modify Git history.
- Do not overwrite or discard existing user work.
- Follow the repository's documentation-maintenance requirements.
- Distinguish verified implementation facts from historical reports, assumptions, recommendations, and unresolved questions.

## 2. Verify prerequisites and approved design

Before implementation, inspect the current repository and compare it with the approved Plan report.

Verify that:

1. Stage 2.2 is sufficiently complete.
2. The light-curve data model and importer provide the information required by the table.
3. Project integration and persistence expose the imported measurements through the expected interfaces.
4. The 2.3.1 design has been completed and approved.
5. The 2.3.2 Plan report accurately describes the current repository.
6. The approved implementation approach remains compatible with the actual code.

Pay particular attention to:

- Time measurements and metadata.
- `SAP_FLUX`.
- `SAP_FLUX_ERR`.
- `PDCSAP_FLUX`.
- `PDCSAP_FLUX_ERR`.
- Flux units.
- Time units, reference, and scale.
- Quality flags.
- Cadence identifiers.
- Missing and non-finite values.
- Dataset identity and source information.
- Project association and persistence.

Do not assume every dataset contains every field.

**Stop conditions:**

If the current repository differs materially from the approved Plan, stop and report the discrepancy.

If a required interface is missing or a prerequisite is incomplete, do not silently implement an alternative.

If implementation requires a new architectural decision, data-model change, importer change, dependency, or storage change that was not explicitly approved, stop and request authorization.

Do not repair earlier subtasks as part of this task.

---

## 3. Follow the approved implementation design

Use the approved 2.3.1 design and 2.3.2 Plan report as the implementation specification.

Implement the table using the approved architecture, components, interfaces, and presentation behavior.

Prefer existing application components and established conventions.

Keep the responsibilities separated:

- Scientific data remains owned by the existing data model and project/data-access layers.
- The table is responsible for presentation and user inspection.
- User selection is an interaction state, not a modification to scientific measurements.

Do not create an independent scientific dataset or unnecessary duplicate measurement arrays.

Do not redesign the approved architecture without authorization.

---

## 4. Implement the measurement table

### 4.1 Table structure and columns

Implement the approved table structure.

Use the actual fields provided by the current data model.

For the Kepler-10b dataset, relevant fields may include:

- `TIME`
- `SAP_FLUX`
- `SAP_FLUX_ERR`
- `PDCSAP_FLUX`
- `PDCSAP_FLUX_ERR`
- `SAP_QUALITY`
- `CADENCENO`

The actual columns, default visibility, and optional columns must follow the approved design.

Requirements:

- Display the correct measurement values.
- Use clear column headers.
- Preserve the identity of each measurement.
- Display units and metadata as approved.
- Handle datasets with optional or unavailable fields.
- Do not assume all datasets contain Kepler-specific columns.
- Do not invent values or metadata.
- Do not silently substitute one measurement for another.

If column visibility, ordering, or customization was approved, implement only the approved behavior.

### 4.2 Measurement identity and uncertainty associations

Preserve the distinction between measurement types.

In particular:

- `SAP_FLUX` and `PDCSAP_FLUX` must remain separately identifiable.
- `SAP_FLUX_ERR` must remain associated with `SAP_FLUX`.
- `PDCSAP_FLUX_ERR` must remain associated with `PDCSAP_FLUX`.
- Missing uncertainty fields must be handled honestly.
- Displaying or selecting one measurement must not cause its uncertainty to become associated with another measurement.

`PDCSAP_FLUX` is the preferred starting point for the initial detection workflow, but `SAP_FLUX` must remain accessible for inspection and comparison.

Do not silently substitute one measurement for another.

### 4.3 Units and metadata

Implement the approved presentation of:

- Time units.
- Time reference and scale.
- Flux units.
- Measurement identity.
- Dataset-level metadata.
- Relevant validation warnings.

Use actual metadata supplied by the imported dataset.

Unknown information must remain unknown.

Do not infer units, time conventions, or metadata from column names alone unless the existing importer explicitly establishes that interpretation.

Do not perform scientific unit conversions as part of table presentation unless an exact display-only conversion was explicitly approved.

---

## 5. Handle missing and invalid measurements

Implement the approved presentation for:

- Missing values.
- NaN values.
- Positive and negative infinity.
- Invalid measurements.
- Unavailable fields.
- Nonzero quality flags.
- Relevant validation warnings.

Requirements:

- Missing measurements must not be displayed as zero.
- Missing, invalid, and unavailable information must be distinguishable from valid measured values.
- Non-finite values must remain identifiable.
- Nonzero quality flags must remain accessible.
- A nonzero quality flag must not automatically cause an observation to disappear.
- Rows must not be silently removed because they contain missing values or quality flags.

Use clear and consistent display conventions.

If formatting is necessary, it must affect only the displayed representation and not the underlying values.

---

## 6. Implement measurement inspection and selection

Implement the approved method for inspecting individual observations.

Depending on the approved design, this may include:

- Selecting a table row.
- Identifying the selected observation.
- Accessing associated measurements.
- Inspecting uncertainties.
- Accessing quality flags and cadence identifiers.
- Understanding whether values are missing or invalid.

Selection must be based on the actual observation identity or stable row mapping established by the approved design.

Do not assume that a visual row number is a permanent scientific observation identifier.

Selection must not modify scientific measurements.

### Future plot integration

The table should be implemented in a way that allows later integration with the scientific plot.

Follow the approved selection-state and interface design so that 2.3.3 and 2.3.4 can use it.

However, do not implement:

- Scientific plotting.
- Plot selection.
- Table/plot synchronization.
- Plot navigation.
- Plot-specific interaction.

These belong to later subtasks.

---

## 7. Implement large-dataset handling

Follow the approved approach for displaying larger light curves.

Consider the approved design's requirements for:

- Efficient row access.
- Memory usage.
- Avoiding unnecessary duplication of measurement arrays.
- Scrolling and navigation.
- Display formatting.
- Avoiding expensive operations during row selection.
- Appropriate model/view usage, if approved.

Do not add pagination, sorting, filtering, or column customization unless explicitly included in the approved design.

Do not introduce unnecessary complexity.

The table must remain usable for the expected initial datasets without compromising scientific data integrity.

---

## 8. Integrate the table into the application

Implement the approved integration with the existing application interface.

### 8.1 Dataset access

The table must obtain measurements through the approved existing data-access interfaces.

It must not create an independent scientific dataset that can diverge from the project's imported measurements.

Avoid unnecessary copies of large measurement arrays.

### 8.2 Dataset switching

Implement the approved behavior when:

- A different dataset is selected.
- A dataset is added to the active project.
- A dataset becomes unavailable.
- Dataset access fails.

Ensure the table updates correctly.

Prevent stale measurements from remaining visible as though they belong to the newly selected dataset.

### 8.3 Project switching

Implement the approved behavior when:

- A project is opened.
- A project is closed.
- A different project becomes active.
- The active project contains no imported light-curve dataset.

Preserve existing project lifecycle behavior.

Do not modify project persistence or project lifecycle architecture as part of this task unless a specific change was explicitly approved.

### 8.4 Empty and unavailable states

Implement the approved presentation for:

- No active project.
- No selected dataset.
- No light-curve data.
- Empty datasets.
- Unavailable datasets.
- Failed dataset access.
- Missing display information.

The interface must communicate these states clearly.

Do not leave stale or misleading measurement information visible.

---

## 9. Scientific integrity requirements

The measurement table is an inspection interface, not a scientific processing system.

The implementation must preserve the distinction between:

1. Original source data.
2. Imported measurements.
3. Displayed values.
4. Future derived data.

The following requirements are mandatory:

| Concern | Required behavior |
|---|---|
| Original FITS file | Must not be modified |
| Imported measurements | Must remain unchanged |
| SAP and PDCSAP | Remain separate |
| Uncertainties | Remain correctly associated |
| Missing values | Remain represented |
| Non-finite values | Remain identifiable |
| Quality flags | Remain accessible |
| Units | Use actual available metadata |
| Time representation | Preserve original interpretation |
| Display formatting | Must not alter stored values |
| Row selection | Must not modify scientific data |
| Normalization | Not performed |
| Filtering | Not performed |
| Detrending | Not performed |
| Outlier removal | Not performed |
| Quality-based removal | Not performed |

Do not silently transform, remove, replace, or reinterpret imported measurements.

If a display-only conversion or formatting operation is approved, keep it separate from the stored scientific values and test that the original values remain unchanged.

---

## 10. Testing requirements

Implement tests alongside the table functionality.

Use the existing testing conventions and approved test strategy.

### 10.1 Table structure and values

Test:

- Correct columns.
- Correct row count.
- Correct displayed values.
- Correct measurement identities.
- Correct uncertainty associations.
- Correct units and metadata.
- Datasets with optional or missing fields.
- Large datasets.

### 10.2 Missing and invalid values

Test:

- Missing values.
- NaN values.
- Positive and negative infinity.
- Unavailable fields.
- Nonzero quality flags.
- Validation warnings.
- Missing measurements are not displayed as zero.
- Observations are not silently removed.

### 10.3 Selection and inspection

Test:

- Row selection.
- Selected observation identity.
- Associated uncertainty access.
- Quality flag access.
- Selection behavior with missing values.
- Selection behavior after dataset changes.
- Selection does not modify scientific measurements.

### 10.4 Application integration

Test:

- Initial table display.
- Dataset switching.
- Project switching.
- Project opening and closing.
- Empty projects.
- Empty datasets.
- Unavailable datasets.
- Failed dataset access.
- Stale-data prevention.

### 10.5 Scientific integrity

Verify that:

- Displaying the table does not modify imported measurements.
- Selecting rows does not modify imported measurements.
- Formatting values does not modify stored values.
- Dataset switching does not modify persisted measurements.
- Original source files remain unchanged.

### 10.6 Test data and portability

Use controlled fixtures and temporary directories.

The standard test suite must not depend on the user's permanent Kepler-10b FITS file or its absolute local path.

The real dataset may be used for optional manual verification if available.

Do not weaken existing tests or remove meaningful assertions to make the implementation pass.

Run relevant targeted tests during implementation and the full existing test suite before completion.

Report exact commands and results.

---

## 11. Dependencies and architecture

Use the existing approved technology stack:

- Python 3.13.
- PySide6.
- NumPy.
- SciPy.
- Astropy.
- Matplotlib.
- pytest.

Do not assume a new dependency is necessary.

Do not install additional packages unless explicitly approved.

If implementation reveals that an additional dependency, significant interface change, data-model change, importer change, or architectural redesign is necessary:

1. Stop the affected work.
2. Explain the technical reason.
3. Identify alternatives.
4. Describe the consequences.
5. Request approval.

Do not silently make the change.

---

## 12. Documentation maintenance

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
- Data model documentation, only if an approved change makes it necessary.
- Decision records, if a new approved decision is made.

Inspect the actual repository structure before selecting files.

For every updated document:

- Preserve its existing structure and conventions.
- Make only relevant changes.
- Ensure descriptions match the implemented behavior.
- Distinguish implemented functionality from future planned functionality.
- Do not claim that plotting or table/plot synchronization has been completed.
- Avoid unnecessary duplication.

Do not modify Foundation documents.

---

## 13. Explicit exclusions

This BUILD task does not authorize:

- Implementing scientific plotting.
- Implementing table/plot synchronization.
- Adding plot navigation.
- Implementing plot measurement selection.
- Changing the light-curve data model.
- Changing the FITS importer.
- Changing project persistence.
- Normalizing measurements.
- Filtering measurements.
- Detrending measurements.
- Removing outliers.
- Removing observations based on quality flags.
- Implementing BLS or other scientific analysis.
- Recording analysis operations.
- Integrating external astronomical archives.
- Redesigning storage architecture.
- Adding unapproved dependencies.
- Performing unrelated refactoring.

If any of these appears necessary, document the dependency and request separate approval.

---

## 14. Completion criteria

Subtask 2.3.2 is complete when:

1. The measurement table follows the approved 2.3.1 design.
2. Imported measurements display accurately.
3. SAP and PDCSAP remain separately identifiable.
4. Uncertainties remain correctly associated.
5. Units and time metadata are presented accurately.
6. Missing and invalid measurements remain identifiable.
7. Quality flags and cadence identifiers remain accessible where available.
8. Users can inspect individual observations according to the approved design.
9. Dataset and project changes update the table correctly.
10. Empty and unavailable states are handled appropriately.
11. Large datasets are handled according to the approved design.
12. The table does not modify imported or persisted scientific measurements.
13. Automated tests cover functionality and scientific integrity.
14. The full existing test suite passes without regressions.
15. Documentation accurately reflects the implementation.

---

## 15. Required final report

Provide a completion report containing:

### A. Summary
- What was implemented.
- Whether 2.3.2 meets its completion criteria.

### B. Prerequisite verification
- Stage 2.2 implementation reviewed.
- Approved 2.3.1 design reviewed.
- Approved 2.3.2 Plan followed.
- Any discrepancies discovered.

### C. Table implementation
- Table structure.
- Columns and metadata.
- Measurement identity handling.
- Uncertainty associations.
- Missing and invalid value presentation.
- Measurement inspection and selection.
- Large-dataset handling.

### D. Application integration
- Dataset access.
- Dataset switching.
- Project switching.
- Empty and unavailable states.
- Stale-data prevention.

### E. Scientific integrity
- How measurements remain unchanged.
- How missing values and quality flags are preserved.
- How display formatting is separated from stored values.
- Whether the original FITS file remained unchanged.

### F. Files changed
For every changed file:
- Path.
- Purpose.
- Summary of changes.

Also list important files inspected but intentionally left unchanged where useful.

### G. Testing and verification
- Exact test commands.
- Targeted test results.
- Full test-suite results.
- Scientific integrity test results.
- Any tests not performed and why.

### H. Documentation updates
- Documents changed.
- Summary of updates.
- Documents intentionally left unchanged.

### I. Outstanding issues
- Known limitations.
- Deferred enhancements.
- Unresolved decisions.
- Any incomplete requirements.

### J. Scope confirmation
Explicitly confirm that:
- Scientific plotting was not implemented.
- Table/plot synchronization was not implemented.
- No scientific transformations were introduced.
- No unapproved data-model, importer, persistence, or architecture changes were made.
- No unapproved dependencies were added.
- Foundation documents were not modified.
- No commits or pushes were made.

### K. Handoff to 2.3.3
Summarize:
- The table components and interfaces implemented.
- How the selected dataset is accessed.
- How measurement identity is represented.
- How row selection is represented.
- Any interfaces the plot implementation should use.
- Any constraints the next subtask must preserve.

Confirm that the next authorized task is 2.3.3, not 2.3.4.

---

## 16. Final restrictions

- Follow the approved 2.3.1 design and 2.3.2 Plan.
- Follow the user's explicit approval decisions.
- Preserve existing user work.
- Do not expand scope.
- Do not make unapproved architectural decisions.
- Do not commit or push.
- Leave the working tree available for user review.
- Stop after completing 2.3.2.

**This task authorizes only the approved measurement table implementation. Scientific plotting and table/plot integration remain separate future subtasks.**