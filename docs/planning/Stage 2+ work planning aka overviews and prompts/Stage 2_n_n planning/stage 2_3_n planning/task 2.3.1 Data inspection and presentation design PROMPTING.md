# PLAN PROMPT

# Stage 2.3.1 — Data Inspection and Presentation Design
## PLAN Prompt

**MODE: PLAN ONLY. Do not implement anything or modify files.**

You are planning Subtask 2.3.1 of the astronomy research application.

Your task is to inspect the current repository, verify the existing Stage 2.2 implementation, and produce a detailed design for the measurement table and scientific light-curve visualization that will be implemented in later subtasks.

This is a design and repository-review task only. You must not make code changes.

---

## 1. Project governance and required reading

Before planning, read and follow the repository's `AGENTS.md`.

Also review the relevant Foundation requirements and project documentation, including:

- The development roadmap.
- The development log.
- Architecture documentation.
- Data model documentation.
- Data flow documentation.
- Module responsibilities.
- Existing decision records.
- Testing and validation documentation.
- Project state and continuity records.
- The approved Stage 2.2 plans, implementation reports, and completion report, if present.

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

## 2. Prerequisite verification: Stage 2.2

Stage 2.3 depends on the light-curve import and project-persistence functionality established in Stage 2.2.

Before designing the presentation layer, verify the actual implementation of:

- **2.2.1 — FITS inspection and data-model design**
- **2.2.2 — FITS import and validation**
- **2.2.3 — Project integration and provisional persistence**
- **2.2.4 — Testing, documentation, and completion verification**

Inspect the current source code, tests, documentation, and available completion reports.

Determine:

1. Whether each subtask was actually implemented.
2. Whether its tests exist and what they verify.
3. Whether its documentation accurately describes the implementation.
4. Whether the data model and importer expose the information required for presentation.
5. Whether project persistence preserves the measurements and metadata needed by the table and plot.
6. Whether any known limitations affect Stage 2.3.

Do not assume that a previous plan or report proves that functionality exists.

**Prerequisite gate:**

If Stage 2.2 is incomplete, materially inconsistent, or missing essential interfaces, identify the issue and explain how it affects 2.3.1.

Do not silently design around missing functionality. Do not implement or repair Stage 2.2 as part of this task. Stop and report any issue that prevents a reliable design.

If Stage 2.2 is sufficiently complete, continue with the planning task.

## 3. Inspect the current application architecture

Review the actual application structure and determine how the new presentation functionality should fit into it.

Inspect:

- Main application window and current navigation.
- Existing widgets and layouts.
- Project and dataset selection mechanisms.
- Current data-access patterns.
- Light-curve data model and importer interfaces.
- Existing plotting or visualization components, if any.
- Existing dependencies and their configuration.
- Current testing conventions.

Identify which existing modules should be reused and which new components may be appropriate.

Do not assume that a new module or framework is necessary.

Prefer the smallest design that fits the existing architecture while maintaining appropriate separation between:

- Scientific data.
- Data access and project integration.
- Presentation and visualization.
- User interaction.

Do not introduce a new plotting library, dependency, storage system, or major architectural redesign without a clear justification and explicit approval.

## 4. Design the measurement table

Determine how imported light-curve measurements should be presented.

Use the actual Stage 2.2 data model and importer as the basis for the design.

Consider the available information, including where supported:

- Observation time.
- Time units and reference information.
- Time scale.
- SAP flux measurements.
- SAP flux uncertainties.
- PDCSAP flux measurements.
- PDCSAP flux uncertainties.
- Quality flags.
- Cadence identifiers.
- Measurement units.
- Missing and non-finite values.
- Validation warnings.
- Relevant dataset metadata.

Do not assume every dataset will contain every field.

Your design must address:

### 4.1 Table structure

- Which columns should be visible by default?
- Should all imported measurement columns be available?
- Should users be able to hide or show columns?
- How should units be communicated?
- Where should dataset-level metadata be displayed?
- How should missing or invalid values appear?
- How should quality flags be represented?
- How should large datasets be handled efficiently?

Distinguish essential initial functionality from optional enhancements.

### 4.2 Measurement inspection

Determine how users should inspect individual measurements.

Consider:

- Selecting a row.
- Identifying the selected observation.
- Displaying associated uncertainties.
- Accessing quality flags and cadence information.
- Inspecting missing or invalid measurements.
- Communicating additional measurement details.

Define the expected behavior without implementing it.

## 5. Design the scientific light-curve plot

Determine how the imported measurements should be visualized.

The initial scientific plot should represent time against a selected flux measurement.

Address the following:

### 5.1 Plot data

- Which imported measurement is plotted?
- How is the selected measurement identified?
- How are uncertainties represented when available?
- How are missing and non-finite measurements handled?
- How are quality flags communicated, if appropriate?
- How does the plot respond to a dataset with incomplete or unavailable information?

For Kepler-10b, the application must preserve the distinction between `SAP_FLUX` and `PDCSAP_FLUX`.

`PDCSAP_FLUX` is the preferred starting point for the initial exoplanet detection workflow, but `SAP_FLUX` must remain available for inspection and comparison.

Do not silently substitute one measurement for another.

### 5.2 Axis labels and metadata

Determine how the plot will communicate:

- Time representation.
- Time units.
- Time reference or offset.
- Time scale.
- Flux measurement identity.
- Flux units.

Axis labels must be based on actual available metadata.

Do not invent units, time references, or conversions when the imported information does not support them.

If metadata is unavailable, determine how that uncertainty should be communicated.

### 5.3 Plot navigation

Determine the appropriate initial navigation functionality.

Consider:

- Zooming.
- Panning.
- Returning to the full dataset view.
- Inspecting individual plotted measurements.
- Handling large datasets.

Separate essential initial capabilities from optional future enhancements.

Do not expand this into a general-purpose plotting system.

## 6. Design table/plot interaction

The table and plot should provide complementary views of the same underlying dataset.

Design how they will work together.

### 6.1 Shared dataset

Determine:

- How both views receive the selected dataset.
- How dataset switching updates both views.
- How project switching updates both views.
- How stale data or stale selections are prevented.
- How empty or unavailable datasets are handled.

### 6.2 Selection synchronization

Determine how selection should work between the views.

Consider the following interaction:

1. A user selects a measurement in the table.
2. The corresponding observation is identified in the plot.
3. A user selects a plotted observation.
4. The corresponding table row is identified.

Decide whether both directions are necessary for the initial implementation and explain the recommendation.

### 6.3 Measurement selection

Determine how users select between available flux measurements.

For example, the table might display both SAP and PDCSAP measurements while the plot displays one selected measurement at a time.

Establish how the selected measurement and its associated uncertainty remain correctly linked.

Do not treat SAP and PDCSAP as interchangeable.

## 7. Scientific integrity requirements

The presentation layer must not modify the original scientific measurements or the imported dataset.

Establish explicit design boundaries for:

- Original source data.
- Imported measurements.
- Displayed values.
- Future derived data.

The initial table and plot are inspection tools, not scientific processing tools.

The design must ensure:

- Original measurements remain unchanged.
- Missing values remain represented in the underlying dataset.
- Non-finite values remain identifiable.
- Quality flags remain accessible.
- Uncertainties remain associated with the correct measurements.
- Known units and time references are preserved.
- Unknown metadata is not invented.
- Visualization does not silently normalize measurements.
- Visualization does not filter measurements out of the underlying dataset.
- Visualization does not detrend measurements.
- Plot rendering does not mutate data.

A plotting library may require non-finite values to be omitted from a rendered line. If so, explain how this presentation limitation will be handled without altering the underlying data.

Also identify whether any proposed display behavior could be mistaken for a scientific transformation.

## 8. Architecture and interface design

Produce a concrete design for how the table and plot will fit into the current application.

Identify:

- Proposed widgets or components.
- Their responsibilities.
- Existing modules they depend on.
- How they receive the selected dataset.
- How measurement selection is communicated.
- How table and plot selections are synchronized.
- How dataset and project changes propagate.
- How the presentation layer accesses data without modifying it.

Where useful, propose interface signatures or data-flow descriptions.

Do not write implementation code.

Do not change the existing data model simply to make the presentation layer easier. If a change appears necessary, explain why, identify the affected interfaces, and request approval rather than assuming authorization.

## 9. Testing strategy

Develop a testing plan for the later implementation subtasks.

Address:

### 9.1 Table tests

- Correct measurement values.
- Correct columns.
- Correct units and metadata.
- Missing and non-finite values.
- Quality flags.
- Measurement selection.
- Large datasets.

### 9.2 Plot tests

- Correct plotted time and flux values.
- Correct axis labels and units.
- Correct uncertainty association.
- Missing and invalid measurements.
- Measurement switching.
- Plot navigation.
- Empty or incomplete datasets.

### 9.3 Integration tests

- Table and plot use the same selected dataset.
- Table selection identifies the correct plotted observation.
- Plot selection identifies the correct table row, if supported.
- Switching measurements updates the plot correctly.
- Switching datasets updates both views.
- Switching projects does not display stale data.
- The underlying dataset remains unchanged.

### 9.4 Test data

Use controlled test fixtures and temporary data.

The standard test suite must not depend on the user's permanent Kepler-10b FITS file or its absolute local path.

The real dataset may be used for optional manual or integration verification where available.

Do not weaken existing tests to accommodate the new functionality.

## 10. Documentation impact assessment

Identify which existing documents will need updates during 2.3.2, 2.3.3, and 2.3.4.

Consider:

- Development roadmap.
- Development log.
- Architecture documentation.
- Data model documentation, if interfaces change.
- Data flow documentation.
- Module responsibilities.
- Decision records.
- Testing and validation documentation.
- Project state and continuity records.

Use the actual repository documentation structure.

For each affected document, explain what will need to change and why.

Do not modify documentation during this planning task.

## 11. Scope boundaries

This subtask is design and planning only.

It does not authorize:

- Implementing the measurement table.
- Implementing the scientific plot.
- Adding visualization dependencies.
- Adding navigation controls.
- Implementing table/plot synchronization.
- Modifying the light-curve data model.
- Changing project persistence.
- Normalizing measurements.
- Filtering measurements.
- Detrending measurements.
- Implementing BLS or other scientific analysis.
- Recording analysis operations.
- Integrating external astronomical archives.
- Redesigning the storage architecture.
- Performing unrelated refactoring.

These are either later subtasks or require separate approval.

## 12. Required report structure

Produce a detailed planning report with the following sections:

### A. Repository and project-state findings
- Current branch and Git working-tree status.
- Relevant source files and modules.
- Relevant documentation.
- Existing architecture and conventions.
- Distinguish local repository findings from historical reports.

### B. Stage 2.2 prerequisite verification
For each of 2.2.1–2.2.4:
- What was inspected.
- What is implemented.
- What tests exist.
- What documentation exists.
- Known limitations.
- Whether it is sufficient for Stage 2.3.

### C. Actual light-curve data capabilities
- Available fields.
- Measurement representations.
- Uncertainties.
- Time metadata.
- Units.
- Quality flags.
- Missing and invalid values.
- Relevant limitations.

### D. Measurement table design
- Proposed columns.
- Default presentation.
- Optional columns.
- Metadata display.
- Missing-value presentation.
- Measurement inspection behavior.
- Large-dataset considerations.

### E. Scientific plot design
- Plotted measurement.
- Measurement selection.
- Axis labels and metadata.
- Uncertainty representation.
- Missing-value behavior.
- Quality information.
- Navigation capabilities.

### F. Table/plot interaction design
- Shared dataset behavior.
- Selection synchronization.
- Measurement switching.
- Dataset and project switching.
- Empty and unavailable data behavior.

### G. Scientific integrity assessment
- How original and imported measurements remain unchanged.
- How display-only handling is separated from scientific processing.
- Potential integrity risks and mitigations.

### H. Architecture and interface proposal
- Proposed components.
- Responsibilities.
- Data flow.
- Interfaces.
- Existing modules to reuse.
- Any proposed changes requiring approval.

### I. Testing strategy
- Unit tests.
- Integration tests.
- Test fixtures.
- Regression tests.
- Optional real-dataset verification.

### J. Documentation impact
- Exact documents affected.
- Proposed updates.
- Any missing or inconsistent documentation.

### K. Risks, limitations, and unresolved questions
Classify findings as:
- Verified issue.
- Potential issue.
- Assumption.
- Recommendation.
- Approval required.
- Deferred enhancement.

### L. Implementation breakdown
Define the approved boundaries and expected work for:
- 2.3.2 — Measurement table implementation.
- 2.3.3 — Scientific light-curve visualization.
- 2.3.4 — Table/plot integration, testing, and completion verification.

Identify dependencies between these subtasks.

### M. Approval decisions
List every design or architectural decision requiring my approval.

For each decision, provide:
- The question.
- Available options.
- Your recommendation.
- The reason for the recommendation.
- Consequences of each option.

Do not make approval-dependent decisions on my behalf.

### N. Readiness assessment
Conclude whether 2.3.1 is:
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

# Stage 2.3.1 — Data Inspection and Presentation Design
## BUILD Prompt

**MODE: BUILD ONLY AFTER THE 2.3.1 PLAN REPORT HAS BEEN REVIEWED AND EXPLICITLY APPROVED.**

You are implementing the approved work for Subtask 2.3.1 of the astronomy research application.

Your task is to finalize and document the data inspection and presentation design that will guide the later implementation of:

- 2.3.2 — Measurement table implementation.
- 2.3.3 — Scientific light-curve visualization.
- 2.3.4 — Table/plot integration, testing, and completion verification.

This subtask establishes the approved design and implementation boundaries. It does not authorize implementation of the table, plot, or their interactive functionality.

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
- Approved Stage 2.2 plans and implementation reports.
- The completed 2.3.1 Plan report.
- The user's explicit approval and any decisions made during Plan review.

Inspect the current repository and compare it with the repository state described in the approved Plan report.

**Do not assume the repository is unchanged since planning.**

Verify that:

1. Stage 2.2 remains sufficiently complete to support the design.
2. The actual data model and importer match the interfaces used in the approved design.
3. Project integration and persistence still support the required data access.
4. The approved design remains compatible with the current application architecture.
5. No new discrepancies have appeared that invalidate an approved decision.

If the repository has changed materially, or the approved design no longer matches the implementation, stop and report the discrepancy before proceeding.

Do not silently redesign around unexpected changes.

## 2. Approval and scope control

Use the approved Plan report and the user's explicit approval as the implementation specification.

Apply all approved decisions exactly as authorized.

For any unresolved decision:

- Do not make an assumption merely to keep implementation moving.
- Do not select an architectural approach without authorization.
- Identify the decision and explain why it is needed.
- Stop and request clarification where it affects the design deliverable.

Do not expand the scope of 2.3.1.

---

## 3. Finalize the Stage 2.3 presentation design

Produce a coherent design specification based on the approved Plan.

The specification must explain how imported light-curve data will be presented and inspected in the application.

It should cover the following areas.

### 3.1 Measurement table design

Document the approved table design, including:

- Proposed measurement columns.
- Which columns should be visible by default.
- Optional or additional columns.
- Time representation and units.
- Flux measurement identities and units.
- Uncertainty fields and their associations.
- Quality flags.
- Cadence identifiers.
- Missing and non-finite values.
- Relevant dataset metadata.
- Individual measurement inspection behavior.
- Large-dataset considerations.

Use the actual data model and importer interfaces.

Do not document fields as available if the current implementation does not provide them.

Where future compatibility is discussed, distinguish existing functionality from anticipated support.

### 3.2 Scientific plot design

Document the approved scientific plotting behavior, including:

- Time on the horizontal axis.
- Selected flux measurement on the vertical axis.
- Axis-label generation.
- Time units and references.
- Time scale.
- Flux units.
- Uncertainty representation.
- Missing and non-finite measurement handling.
- Quality information, where applicable.
- Measurement selection.
- Plot navigation requirements.

For Kepler-10b, preserve the distinction between `SAP_FLUX` and `PDCSAP_FLUX`.

Document `PDCSAP_FLUX` as the preferred starting point for the initial detection workflow, while retaining access to `SAP_FLUX`.

Do not treat the two measurements as interchangeable.

### 3.3 Table/plot interaction design

Document the approved interaction between the two views.

Include:

- How both views obtain the selected dataset.
- How dataset switching affects both views.
- How project switching affects both views.
- How table row selection relates to plotted observations.
- How plot selection relates to table rows, if approved.
- How flux measurement selection affects the plot.
- How associated uncertainties remain correctly linked.
- How stale selections and stale data are prevented.
- How empty or unavailable datasets are handled.

Clearly distinguish required initial behavior from optional future enhancements.

### 3.4 Scientific integrity design

Document the distinction between:

1. Original source data.
2. Imported measurements.
3. Displayed values.
4. Future derived data.

The design must explicitly establish that the table and plot are inspection tools.

Document the following boundaries:

- Original source data must not be modified.
- Imported measurements must remain unchanged.
- Missing values must remain represented in the underlying dataset.
- Non-finite values must remain identifiable.
- Quality flags must remain accessible.
- Uncertainties must remain associated with the correct measurements.
- Known units and time references must be preserved.
- Unknown metadata must not be invented.
- Visualization must not silently normalize measurements.
- Visualization must not filter or remove measurements from the underlying dataset.
- Visualization must not detrend measurements.
- Plot rendering must not mutate scientific data.

If non-finite values cannot be rendered directly, document how they will be handled in the presentation layer without changing the dataset.

Do not implement scientific transformations.

---

## 4. Finalize the architecture and interface design

Document how the table and plot will fit into the existing application architecture.

Based on the approved Plan, identify:

- Components or widgets responsible for presentation.
- Responsibilities of each component.
- Existing modules that will be reused.
- How the selected dataset is supplied.
- How measurement selection is represented.
- How selections are communicated between views.
- How dataset and project changes propagate.
- How the presentation layer accesses scientific measurements without modifying them.

Where appropriate, document proposed interfaces, data-flow relationships, or method responsibilities.

Do not implement the components or their behavior.

Do not introduce a new dependency, plotting framework, storage architecture, or major architectural change unless explicitly approved.

If the approved design requires a change to the existing data model or importer, do not implement that change automatically. Report it as a dependency requiring separate authorization unless the user explicitly approved it for this subtask.

---

## 5. Finalize the testing design

Document how the later implementation subtasks will be tested.

Include the approved testing requirements for:

### Measurement table
- Correct displayed values.
- Correct columns.
- Units and metadata.
- Missing and non-finite values.
- Quality flags.
- Measurement inspection.
- Large datasets.

### Scientific plot
- Correct plotted values.
- Correct axis labels.
- Units and time references.
- Uncertainty representation.
- Missing and invalid measurements.
- Measurement switching.
- Navigation.
- Empty or incomplete datasets.

### Table/plot integration
- Shared dataset.
- Selection synchronization.
- Measurement switching.
- Dataset switching.
- Project switching.
- Stale-data prevention.
- Underlying data integrity.

### Test data and portability

Document the requirement to use controlled fixtures and temporary test data.

The standard test suite must not depend on the user's permanent Kepler-10b FITS file or its absolute local path.

The real dataset may be used for optional manual verification.

Do not create or modify tests in this subtask.

---

## 6. Define the implementation boundaries for subsequent subtasks

Document the responsibilities and exclusions of each remaining Stage 2.3 subtask.

### 2.3.2 — Measurement table implementation

Responsible for implementing the approved table design.

Expected scope includes:

- Table presentation.
- Measurement columns.
- Units and metadata presentation.
- Missing and invalid value presentation.
- Measurement inspection.
- Table-specific tests.
- Relevant documentation updates.

It must not independently expand into scientific plotting or BLS analysis.

### 2.3.3 — Scientific light-curve visualization

Responsible for implementing the approved scientific plot design.

Expected scope includes:

- Time-series plotting.
- Selected flux measurement.
- Axis labels and units.
- Uncertainty representation.
- Missing and invalid measurement presentation.
- Plot navigation.
- Plot-specific tests.
- Relevant documentation updates.

It must not independently expand into scientific transformations or BLS analysis.

### 2.3.4 — Integration, testing, and completion verification

Responsible for:

- Connecting the table and plot.
- Verifying selection synchronization.
- Verifying dataset and project switching.
- Testing scientific integrity.
- Running regression and integration tests.
- Reconciling documentation.
- Producing the Stage 2.3 completion report.

Do not implement these later subtasks now.

---

## 7. Documentation maintenance

Follow the documentation-maintenance requirements in `AGENTS.md`.

Update the appropriate project documentation to record the approved Stage 2.3 design.

Inspect the actual repository documentation structure before choosing files.

Potential documents include:

- Development roadmap.
- Development log.
- Architecture documentation.
- Data model documentation, if relevant.
- Data flow documentation.
- Module responsibilities.
- Decision records.
- Testing and validation documentation.
- Project state and continuity records.

For each document updated:

- Preserve its existing organization and conventions.
- Make only relevant changes.
- Ensure statements reflect verified implementation facts or clearly identified future designs.
- Do not claim that planned functionality has already been implemented.
- Do not duplicate information unnecessarily.
- Record important approved decisions in the established decision-record format.

If a document does not need updating, leave it unchanged.

Do not modify Foundation documents.

---

## 8. Testing and verification

Since this subtask establishes and documents a design rather than implementing functionality:

- Run relevant existing tests only if necessary to verify repository state or confirm a documented claim.
- Do not create tests for functionality that does not yet exist.
- Do not modify existing tests.
- Do not weaken test assertions.
- Do not introduce dependencies.

Verify that the documentation is internally consistent and accurately describes the approved design.

Check that:

1. Table requirements agree with the actual data model.
2. Plot requirements agree with the actual data model.
3. Measurement identities and uncertainty associations are correct.
4. Time and unit descriptions are supported by the importer.
5. Table/plot interaction requirements are consistent.
6. Scientific integrity boundaries are explicit.
7. The responsibilities of 2.3.2, 2.3.3, and 2.3.4 do not overlap ambiguously.
8. No later-stage functionality is represented as part of 2.3.1.

Report any verification commands and their exact results.

---

## 9. Explicit exclusions

This BUILD task does not authorize:

- Implementing a measurement table.
- Implementing a scientific plot.
- Creating visualization widgets.
- Adding zooming or panning controls.
- Implementing table/plot selection synchronization.
- Changing the light-curve data model.
- Changing the FITS importer.
- Changing project persistence.
- Adding dependencies.
- Normalizing measurements.
- Filtering measurements.
- Detrending measurements.
- Implementing BLS or other scientific analysis.
- Recording analysis operations.
- Integrating external astronomical archives.
- Redesigning storage architecture.
- Performing unrelated refactoring.
- Modifying Foundation documents.

If any of these appears necessary, document the dependency and request separate approval.

---

## 10. Completion criteria

Subtask 2.3.1 is complete when:

1. The actual Stage 2.2 implementation has been verified as a sufficient foundation.
2. The approved measurement table design is documented.
3. The approved scientific plot design is documented.
4. Table/plot interaction is documented.
5. Scientific integrity requirements are explicit.
6. Architecture and component responsibilities are documented.
7. Testing requirements for later subtasks are documented.
8. Implementation boundaries for 2.3.2, 2.3.3, and 2.3.4 are clear.
9. Relevant documentation has been updated.
10. Documentation has been checked against the actual code and approved design.
11. No unapproved implementation or architectural changes have been made.

---

## 11. Required final report

Provide a completion report containing:

### A. Summary
- What was completed.
- Whether 2.3.1 meets its completion criteria.

### B. Prerequisite verification
- Actual Stage 2.2 implementation reviewed.
- Any discrepancies or limitations discovered.

### C. Design finalized
- Measurement table.
- Scientific plot.
- Table/plot interaction.
- Scientific integrity.
- Architecture and interfaces.
- Testing strategy.

### D. Files changed
For every changed file:
- Path.
- Purpose of the change.
- Summary of the update.

Also list important files inspected but intentionally left unchanged where useful.

### E. Testing and verification
- Commands executed.
- Exact results.
- Documentation consistency checks.
- Any verification not performed.

### F. Scope confirmation
Explicitly confirm that:
- No table or plot functionality was implemented.
- No scientific measurements were modified.
- No unapproved data-model, importer, or persistence changes were made.
- No dependencies were added.
- No Foundation documents were modified.
- No commits or pushes were made.

### G. Outstanding issues
List unresolved decisions, dependencies, limitations, and recommendations for later subtasks.

### H. Handoff to 2.3.2
Summarize the approved design requirements that the measurement table implementation must follow.

Confirm that the next authorized task is 2.3.2, not 2.3.3 or 2.3.4.

---

## 12. Final restrictions

- Follow the approved 2.3.1 Plan and explicit user decisions.
- Preserve existing user work.
- Do not expand scope.
- Do not make unapproved architectural decisions.
- Do not commit or push.
- Leave the working tree available for user review.
- Stop after completing 2.3.1.

**This task authorizes only the approved design finalization and documentation work. It does not authorize implementation of the measurement table or scientific plot.**
