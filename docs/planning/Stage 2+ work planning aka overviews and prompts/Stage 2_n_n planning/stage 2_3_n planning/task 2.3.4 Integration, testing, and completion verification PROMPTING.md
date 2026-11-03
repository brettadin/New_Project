# PLAN PROMPT

# PLAN — Stage 2.3.4: Table/Plot Integration, Testing, and Completion Verification

**Mode: PLAN ONLY — inspection, analysis, and planning. No implementation or file modifications.**

## 1. Objective

Plan the final Stage 2.3 subtask: integrate the measurement table implemented in Stage 2.3.2 with the scientific light-curve visualization implemented in Stage 2.3.3.

The goal is a cohesive inspection experience in which:

- The table and plot represent the same active scientific dataset.
- Selecting a measurement in the table identifies the corresponding observation in the plot.
- Selecting a plotted observation identifies the corresponding table row.
- Switching between SAP_FLUX and PDCSAP_FLUX keeps the table and plot consistent.
- Project and dataset changes update both components together.
- Missing or non-finite measurements remain correctly represented and mapped.
- Neither component modifies the underlying scientific measurements.

This task is an integration and verification task. It is not an opportunity to redesign the application or expand its scientific capabilities.

## 2. Mandatory prerequisite inspection

Before planning implementation, inspect the actual repository and verify the current state of:

1. Stage 2.2.1 — FITS inspection and data-model design.
2. Stage 2.2.2 — FITS import and validation.
3. Stage 2.2.3 — Project integration and provisional persistence.
4. Stage 2.2.4 — Testing, documentation, and completion verification.
5. Stage 2.3.1 — Data inspection and presentation design.
6. Stage 2.3.2 — Measurement table implementation.
7. Stage 2.3.3 — Scientific light-curve visualization.

Read the relevant roadmap, development log, approved designs, architecture documentation, data-model documentation, module documentation, testing documentation, and decision records.

Verify implementation against actual code and tests. Do not rely exclusively on completion statements in documentation or previous reports.

In particular, establish:

- Whether the table and plot both exist and function independently.
- How each component obtains its dataset.
- How each component identifies an observation.
- Whether a stable measurement or observation identifier exists.
- How plotted points map back to source observations.
- How non-finite observations are represented in the table and excluded, if appropriate, from rendering.
- How SAP_FLUX and PDCSAP_FLUX are selected.
- How uncertainty fields are associated with each flux measurement.
- How project and dataset changes are currently handled.
- Whether the existing interfaces support integration without changes to the scientific data model.

**If any prerequisite is incomplete, missing, or inconsistent, stop and report the issue. Do not plan around functionality that does not exist.** Identify the minimum prerequisite work needed before 2.3.4 can proceed.

## 3. Table-to-plot and plot-to-table synchronization

Inspect the existing selection mechanisms and plan how the two components will communicate.

The design must address both directions:

### Table to plot

When a user selects a measurement in the table:

- Identify the corresponding underlying observation.
- Highlight or otherwise identify the corresponding plotted point when that observation is plottable.
- Ensure the mapping uses the correct underlying observation identity.
- Do not rely on visible table row numbers as permanent scientific identifiers.

### Plot to table

When a user selects a plotted point:

- Identify the corresponding underlying observation.
- Select or bring the corresponding table row into view.
- Ensure the selected row represents the same observation as the selected plotted point.

### Observation identity

Explicitly inspect how the current implementation handles observation identity.

The integration must remain correct when:

- Rows are sorted or displayed differently, if supported.
- Some observations are omitted from the rendered plot because their time or flux values are non-finite.
- The table contains observations that cannot be plotted.
- The dataset contains missing values.

A plotted-point index must not be assumed to equal a table row index unless the implementation explicitly guarantees that relationship.

Recommend the smallest reliable approach consistent with the existing data model and architecture. Do not introduce a new identity system without demonstrating why it is necessary.

## 4. Measurement selection synchronization

Inspect how the table and plot currently represent the selected flux measurement.

Plan a consistent approach for:

- SAP_FLUX.
- PDCSAP_FLUX.

The integration must preserve the distinction between these measurements.

The plot must continue to use the correct uncertainty field:

- SAP_FLUX → SAP_FLUX_ERR.
- PDCSAP_FLUX → PDCSAP_FLUX_ERR.

Address:

- Where the shared measurement selection should live.
- How changes are communicated between the table and plot.
- How the components avoid conflicting or duplicated selection state.
- What happens when a dataset does not contain the selected measurement.
- How the interface communicates unavailable measurements.
- Whether the default measurement remains consistent with the existing approved design and decisions.

Do not change the underlying scientific data or overwrite one measurement with another.

## 5. Project and dataset lifecycle integration

Inspect existing project and dataset lifecycle behavior.

Plan how both components will respond to:

- Opening a project.
- Closing a project.
- Switching between projects.
- Selecting another dataset within a project.
- Importing an additional dataset, if supported.
- Datasets with different available columns or metadata.
- Empty datasets.
- Missing or unavailable datasets.
- Dataset-loading or display errors.

The table and plot must never display different active datasets simultaneously.

Address:

- How selection state is reset or restored.
- How stale plotted points and table selections are prevented.
- How the components respond when a selected observation no longer exists in the active dataset.
- How measurement selection behaves when switching datasets.
- Whether existing project lifecycle signals or interfaces can be reused.

Do not redesign project management or persistence.

## 6. Missing values, non-finite measurements, and quality flags

Inspect actual table and plot behavior for these cases.

The integration must preserve the following scientific distinctions:

- Missing values are not zero.
- Missing uncertainty values are not zero uncertainty.
- NaN and infinite values remain identifiable in the underlying dataset.
- An observation omitted from the rendered plot must remain available in the table.
- Selecting an observation that cannot be plotted must still produce a meaningful table selection.
- Nonzero quality flags must not automatically remove observations.
- Quality flags must remain accessible through the existing inspection interface.

Plan tests for selection mapping when observations are missing or non-finite.

Do not introduce automatic filtering, quality-based exclusion, normalization, or other scientific transformations.

## 7. Cohesive interface and interaction design

Inspect the current application layout and the independent table and plot interfaces.

Plan only the layout and interaction changes necessary to make the two components work together.

Consider:

- How the table and plot are arranged.
- Resizing and available screen space.
- Whether both components remain accessible.
- Measurement selection controls.
- Selection and highlighting feedback.
- Empty and unavailable states.
- Consistent dataset and measurement labels.
- Whether the interface makes the relationship between a selected table row and plotted point clear.

Avoid a whole-application redesign.

Follow the approved Stage 2.3.1 presentation design unless the actual implementation reveals a concrete incompatibility. Clearly identify any proposed deviation and explain why it is necessary.

## 8. Architecture and implementation boundaries

Inspect the existing module structure and identify the smallest appropriate integration points.

Determine:

- Which existing components should own or coordinate shared selection state.
- Whether existing signals, slots, callbacks, or controller mechanisms can be reused.
- Whether a small integration controller or shared state object is justified.
- How dataset identity and observation identity will be passed between components.
- How lifecycle changes will invalidate or refresh both views.
- Whether any existing interfaces need narrow changes.

Prefer reuse of existing architecture over introducing new abstractions.

Do not add dependencies or introduce a new plotting, table, or application framework.

Do not modify the scientific data model, FITS importer, or persistence architecture as part of this task unless an actual blocking defect is discovered. If one is discovered, document it separately and request approval before expanding scope.

## 9. Performance considerations

Inspect the current table and plot implementations for data duplication and performance concerns.

Plan how integration will avoid:

- Unnecessary copies of full measurement arrays.
- Repeated expensive conversions.
- Rebuilding the entire plot for simple selection changes when avoidable.
- Excessive signal emissions or selection feedback loops.
- Unresponsive behavior on larger datasets.

Determine whether the current implementation is sufficient or whether a narrow optimization is necessary.

Do not introduce speculative caching, downsampling, or complex performance infrastructure.

## 10. Testing plan

Develop a concrete test plan based on the actual implementation and existing test conventions.

Use controlled FITS fixtures and temporary project data for routine tests.

The standard test suite must not depend on the user's permanent Kepler FITS file or its absolute local path.

Include tests for:

### A. Table-to-plot selection

- Selecting a table observation identifies the corresponding plotted point.
- Selecting a different row updates the highlighted point.
- Selection remains correct for observations whose visible row position differs from their underlying identity.

### B. Plot-to-table selection

- Selecting a plotted point selects the corresponding table observation.
- The correct row is brought into view when appropriate.
- Selection maps to the correct original observation.

### C. Non-finite and missing observations

- A table observation with non-finite time or flux remains in the table.
- An observation omitted from the plot does not break point-to-row mapping.
- Selecting an unplottable observation in the table remains meaningful.
- Missing values are never substituted with zero.

### D. Measurement switching

- Switching between SAP_FLUX and PDCSAP_FLUX updates the plot correctly.
- The corresponding uncertainty field is used.
- Table values remain associated with the correct measurement.
- Missing or unavailable measurements are handled clearly.
- No measurement data is overwritten.

### E. Project and dataset switching

- Both components update when the active dataset changes.
- Both components update when the active project changes.
- Stale selection and plot state are cleared or restored according to the approved design.
- Empty and unavailable states are consistent.
- Different dataset column configurations are handled.

### F. Scientific integrity

- The table and plot reference the same underlying dataset.
- Original measurement values remain unchanged.
- SAP and PDCSAP remain separate.
- Uncertainties remain correctly associated.
- Missing and non-finite values remain identifiable.
- Quality flags remain accessible.
- Units and time metadata remain accurate.
- No normalization, detrending, filtering, or other transformations occur.
- The original source FITS file remains unchanged.

### G. Integration and regression

- Selection synchronization does not create infinite signal loops.
- Existing table tests continue to pass.
- Existing plot tests continue to pass.
- Existing project lifecycle tests continue to pass.
- The full test suite passes.

Identify appropriate test files and any necessary new tests. Do not weaken or remove existing tests to make the integration pass.

## 11. Documentation plan

Follow the documentation-maintenance requirements in the repository's `AGENTS.md`.

Identify which existing documents need updates based on the actual implementation and repository structure.

Consider:

- Stage roadmap and task status.
- Development log.
- Architecture documentation.
- Data-flow documentation.
- Module responsibilities.
- Data-model documentation, only if necessary.
- Testing and validation documentation.
- Project state and continuity records.
- Decision records, only if a genuine new decision is required.

Documentation must describe implemented behavior accurately, not planned behavior as though it already exists.

Do not modify Foundation documents.

Do not create duplicate documentation when an existing document is the appropriate location.

## 12. Explicit scope exclusions

This task does not include:

- BLS transit search or uncertainty calculations (Stage 2.4).
- Transit fitting or parameter estimation.
- Detrending, normalization, filtering, or other scientific transformations.
- Automatic quality-flag filtering.
- Archive integration or remote data retrieval.
- Permanent storage architecture redesign.
- FITS importer redesign.
- New scientific analysis operations.
- General-purpose plotting framework development.
- Unrelated application redesign or refactoring.
- Unapproved dependencies or architectural changes.

If an issue outside this scope is discovered, report it separately rather than silently expanding the task.

## 13. Required PLAN report

Provide the final plan in the following sections:

**A. Repository and implementation state**
- Current branch and working-tree state, if available.
- Relevant modules and files inspected.
- Actual implementation state of 2.2 and 2.3.1–2.3.3.
- Distinguish verified facts from documentation claims.

**B. Prerequisite assessment**
- Which prerequisites are complete.
- Which are incomplete or inconsistent.
- Whether 2.3.4 can proceed.

**C. Current table implementation**
- Data access.
- Observation identity.
- Selection behavior.
- Measurement selection.
- Missing/non-finite handling.

**D. Current plot implementation**
- Data access.
- Observation-to-point mapping.
- Selection behavior.
- Measurement and uncertainty handling.
- Missing/non-finite handling.

**E. Integration design**
- Table-to-plot synchronization.
- Plot-to-table synchronization.
- Stable observation mapping.
- Shared measurement selection.
- Handling of unplottable observations.

**F. Project and dataset lifecycle**
- Required event handling.
- Stale-state prevention.
- Empty, unavailable, and error states.

**G. Interface design**
- Proposed layout and interaction changes.
- Alignment with approved 2.3.1 design.
- Any necessary deviations.

**H. Architecture and implementation breakdown**
- Actual modules/files expected to change.
- Proposed signals, interfaces, or state coordination.
- Smallest reasonable implementation approach.
- Any unresolved architecture questions.

**I. Performance assessment**
- Existing performance characteristics.
- Data duplication risks.
- Necessary optimizations, if any.

**J. Scientific integrity**
- How each scientific integrity requirement will be preserved.
- Any existing risks or defects.

**K. Testing plan**
- Existing tests to extend.
- New tests required.
- Fixture strategy.
- Regression and full-suite verification.

**L. Documentation plan**
- Exact existing documents expected to change.
- Purpose of each proposed update.
- Documents intentionally left unchanged and why.

**M. Risks and unresolved questions**
- Technical risks.
- Missing prerequisites.
- Ambiguous design decisions.
- Any issue requiring user approval.

**N. Implementation sequence**
- A clear, ordered implementation sequence.
- Dependencies between steps.
- Expected verification after each meaningful step.
- Keep the sequence focused on 2.3.4.

**O. Readiness recommendation**
- Ready to proceed to Build, or not ready.
- Any conditions that must be met first.
- Explicit confirmation that the proposed work remains within Stage 2.3.4 scope.

## 14. PLAN restrictions

During this task:

- Do not modify source code.
- Do not modify tests.
- Do not modify documentation.
- Do not create or delete files.
- Do not install or update dependencies.
- Do not modify project data or the original FITS file.
- Do not run implementation or migration scripts.
- Do not commit, push, reset, clean, or otherwise alter Git history.
- Do not begin Build.
- Do not assume approval for unresolved architecture or scope decisions.

Read-only inspection and appropriate existing test execution may be used to verify the current state, provided they do not modify project files or data. If a verification command could modify files, explain that limitation and do not run it.

**Stop after presenting the PLAN report. Wait for review and explicit approval before any implementation.**


# BUILD PROMPT

# BUILD — Stage 2.3.4: Table/Plot Integration, Testing, and Completion Verification

**Mode: BUILD — implement the approved 2.3.4 plan only.**

## 1. Objective

Implement the approved integration between the Stage 2.3.2 measurement table and Stage 2.3.3 scientific light-curve visualization.

The objective is to provide a cohesive inspection experience in which:

- The table and plot always represent the same active scientific dataset.
- Selecting an observation in the table identifies the corresponding plotted observation.
- Selecting a plotted observation identifies the corresponding table row.
- SAP_FLUX and PDCSAP_FLUX selection remains consistent across both components.
- The correct uncertainty field remains associated with each selected flux measurement.
- Project and dataset changes update both components together.
- Missing and non-finite observations remain correctly represented and mapped.
- The underlying scientific measurements remain unchanged.

Follow the reviewed and approved 2.3.4 PLAN report.

**The approved PLAN is the implementation authority.** If this prompt conflicts with the approved plan, follow the approved plan within its authorized scope. If the plan contains unresolved decisions, incomplete prerequisites, or proposed changes requiring additional approval, stop and report them rather than guessing.

## 2. Mandatory pre-implementation verification

Before editing anything:

1. Re-read the approved 2.3.4 PLAN report.
2. Inspect the relevant current repository files.
3. Verify the implementation state of Stage 2.2 and Stage 2.3.1–2.3.3.
4. Confirm that the prerequisites identified in the PLAN are satisfied.
5. Confirm the approved implementation sequence and file-change list.
6. Confirm the existing working-tree state.

Do not overwrite, discard, or revert existing user changes.

If the actual repository differs materially from the approved PLAN, stop and report the discrepancy before proceeding.

Do not expand scope to compensate for missing prerequisite work.

## 3. Implement table-to-plot synchronization

Implement the approved mechanism for synchronizing table selection with plot selection.

When a user selects an observation in the measurement table:

- Identify the correct underlying observation.
- Identify or highlight the corresponding plotted point when it is plottable.
- Keep the table selection and plot selection consistent.
- Avoid unnecessary plot reconstruction when a selection-only update is sufficient.

The mapping must use the observation identity strategy established in the approved design.

Do not assume that a visible table row index is a permanent scientific identifier.

## 4. Implement plot-to-table synchronization

When a user selects a plotted observation:

- Identify the corresponding underlying observation.
- Select the correct table row.
- Bring the selected row into view when appropriate under the approved design.
- Ensure the selected row represents the same observation as the plotted point.

The plotted-point index must not be assumed to equal the table row index unless the existing implementation explicitly guarantees that relationship.

Ensure the implementation remains correct when some observations are omitted from the rendered plot because their time or flux values are non-finite.

## 5. Preserve observation identity

Implement the approved mapping between:

- Original dataset observations.
- Table rows.
- Rendered plot points.
- Selected observations.

The mapping must remain correct when:

- The table contains non-finite observations.
- Some observations cannot be rendered.
- The table's display order differs from the underlying data order, if supported.
- The active dataset changes.
- A selected observation is no longer available.

Do not create a new identity system unless the approved PLAN explicitly authorizes it.

Do not use visual position alone as a substitute for scientific observation identity.

## 6. Synchronize measurement selection

Implement the approved shared measurement-selection behavior.

Support the existing distinct measurement types:

- SAP_FLUX.
- PDCSAP_FLUX.

Preserve their uncertainty associations:

- SAP_FLUX → SAP_FLUX_ERR.
- PDCSAP_FLUX → PDCSAP_FLUX_ERR.

Ensure:

- The table and plot remain consistent when the selected measurement changes.
- The plot displays the selected measurement.
- The correct uncertainty field is used.
- The table continues to display the correct source measurement values.
- Missing or unavailable measurements are handled according to the approved design.
- Selection state does not become duplicated or contradictory between components.

Do not overwrite, combine, or substitute one measurement with another.

Retain the approved default measurement selection.

## 7. Integrate project and dataset lifecycle behavior

Implement the approved lifecycle handling so that both components respond consistently to:

- Opening a project.
- Closing a project.
- Switching projects.
- Selecting another dataset.
- Importing another dataset, where supported.
- Empty datasets.
- Missing or unavailable datasets.
- Dataset-loading failures.
- Datasets with different available columns or metadata.

The table and plot must never display different active datasets simultaneously.

Ensure stale selections and plotted points cannot remain visible after a dataset or project change.

Reset or restore selections according to the approved design.

Do not redesign project management, persistence, or dataset import.

## 8. Handle missing values and quality flags correctly

Preserve the existing scientific data and approved display behavior.

Ensure:

- Missing values are never replaced with zero.
- Missing uncertainties are never interpreted as zero uncertainty.
- NaN and infinite values remain identifiable in the underlying dataset.
- Observations omitted from the plot remain available in the table.
- Selecting an unplottable observation in the table remains meaningful.
- Nonzero quality flags do not automatically remove observations.
- Quality flags remain accessible through the existing inspection interface.

Do not introduce automatic quality filtering or scientific transformations.

## 9. Complete the integrated interface

Implement only the layout and interaction changes approved in the PLAN.

Ensure:

- The table and plot are accessible together.
- Their selection feedback is understandable.
- Measurement selection remains consistent.
- Dataset and measurement labels are accurate.
- Empty and unavailable states are handled coherently.
- Resizing and available screen space behave appropriately.

Do not redesign unrelated parts of the application.

## 10. Architecture and implementation discipline

Follow the existing architecture and approved integration design.

Requirements:

- Reuse existing signals, slots, interfaces, and state mechanisms where appropriate.
- Keep changes limited to the approved modules and files.
- Avoid unnecessary new abstractions.
- Avoid duplicated scientific measurement data.
- Avoid unnecessary copies of full arrays.
- Prevent signal feedback loops and repeated selection events.
- Avoid unrelated refactoring.
- Do not add dependencies unless explicitly approved.

Do not change the FITS importer, scientific data model, or persistence architecture unless the approved PLAN explicitly authorizes a narrowly scoped change.

If an unexpected defect makes an approved implementation impossible, stop and report it. Do not silently expand scope.

## 11. Testing requirements

Implement and run the tests identified in the approved PLAN.

Use portable fixtures and temporary project data. The standard test suite must not depend on the user's permanent Kepler FITS file or its absolute path.

### A. Table-to-plot selection

Verify:

- Selecting a table row identifies the correct plotted observation.
- Changing table selection updates the plot selection.
- Mapping remains correct when display positions differ from underlying observation identities.

### B. Plot-to-table selection

Verify:

- Selecting a plotted point selects the correct table row.
- The selected row is brought into view when appropriate.
- The selected table observation matches the plotted observation.

### C. Missing and non-finite observations

Verify:

- Non-finite observations remain available in the table.
- Omitted plot points do not break observation mapping.
- Selecting an unplottable observation remains meaningful.
- Missing values are not substituted with zero.

### D. Measurement selection

Verify:

- SAP_FLUX and PDCSAP_FLUX selection remains consistent.
- The correct uncertainty field is used for each measurement.
- Missing or unavailable measurements are handled correctly.
- No measurement values are overwritten or mixed.

### E. Project and dataset lifecycle

Verify:

- Both components update when the active dataset changes.
- Both components update when the active project changes.
- Stale selections and plotted points are cleared or restored correctly.
- Empty, unavailable, and error states remain consistent.
- Different dataset configurations are handled correctly.

### F. Scientific integrity

Verify:

- Both components reference the same underlying dataset.
- Original measurement values remain unchanged.
- SAP and PDCSAP remain distinct.
- Uncertainties remain correctly associated.
- Missing and non-finite values remain identifiable.
- Quality flags remain accessible.
- Units and time metadata remain accurate.
- No normalization, detrending, filtering, or other transformations occur.
- The original source FITS file remains unchanged.

### G. Regression and full-suite testing

- Run relevant existing table tests.
- Run relevant existing plot tests.
- Run relevant project and dataset lifecycle tests.
- Run all newly added integration tests.
- Run the complete test suite.

Do not weaken, delete, skip, or rewrite existing tests merely to obtain passing results.

If a test fails:

1. Identify the cause.
2. Determine whether it is an implementation defect, an existing defect, or an incorrect test assumption.
3. Make only corrections within the approved scope.
4. Preserve test coverage and scientific integrity.
5. Report unresolved failures accurately.

Do not claim tests passed unless they were actually executed and passed.

## 12. Documentation maintenance

Follow the repository's `AGENTS.md` documentation-maintenance requirements.

Update existing documentation as needed to reflect the actual implemented behavior.

Review the documents identified in the approved PLAN, including applicable:

- Stage roadmap.
- Development log.
- Architecture documentation.
- Data-flow documentation.
- Module responsibilities.
- Data-model documentation, if necessary.
- Testing and validation documentation.
- Project state and continuity records.
- Decision records, only where a genuine new decision is required.

Documentation must accurately distinguish:

- Implemented functionality.
- Tested functionality.
- Known limitations.
- Deferred work.
- Unresolved issues.

Update task status only when the corresponding implementation and verification criteria have actually been met.

Do not modify Foundation documents.

Do not create duplicate documentation where an existing document is the appropriate location.

## 13. Explicit exclusions

Do not implement or begin:

- BLS transit search or uncertainty calculations (Stage 2.4).
- Transit fitting or parameter estimation.
- Detrending, normalization, filtering, or other scientific transformations.
- Automatic quality-flag filtering.
- Archive integration or remote data retrieval.
- Permanent storage architecture redesign.
- FITS importer redesign.
- New scientific analysis operations.
- General-purpose plotting framework development.
- Unrelated application redesign or refactoring.
- Unapproved dependencies or architectural changes.

If an issue outside this scope is discovered, document it and report it separately.

## 14. Final verification and report

After implementation, testing, and documentation updates, compare the actual repository state against:

1. The approved 2.3.4 PLAN.
2. The Stage 2.3 overall objective.
3. The original scientific integrity requirements.
4. The applicable Foundation requirements.
5. The repository's `AGENTS.md`.

Provide a final report containing:

### A. Implementation summary
- What was implemented.
- How table/plot synchronization works.
- How observation identity is preserved.
- How measurement selection is synchronized.
- How project and dataset changes are handled.

### B. Files changed
For each changed file, explain:
- What changed.
- Why the change was necessary.
- Which approved PLAN item it addresses.

Separate source-code changes, test changes, and documentation changes.

### C. Testing results
Report:
- Exact test commands executed.
- Targeted test results.
- Full test-suite results.
- Any failures, skips, or limitations.
- Whether the tests use portable fixtures.

### D. Scientific integrity verification
Explicitly report the verification status of:

- Original measurements unchanged.
- SAP_FLUX and PDCSAP_FLUX kept distinct.
- Correct uncertainty associations.
- Missing and non-finite values preserved.
- Quality flags accessible.
- Accurate units and time metadata.
- Correct table/plot observation mapping.
- No unapproved scientific transformations.
- Original source FITS file unchanged.

Distinguish directly tested properties from properties only reviewed through code inspection.

### E. Documentation reconciliation
List:
- Documents updated.
- Documents inspected but intentionally unchanged, with reasons.
- Any documentation gaps that remain.

### F. Known limitations and deferred work
Identify remaining defects, limitations, unresolved decisions, or work intentionally deferred to later stages.

Do not describe deferred work as completed.

### G. Stage 2.3 completion assessment
Evaluate whether the overall Stage 2.3 objective has been met:

- 2.3.1 design completed and reflected in implementation.
- 2.3.2 measurement table implemented and verified.
- 2.3.3 scientific light-curve plot implemented and verified.
- 2.3.4 table/plot integration implemented and verified.
- Both components represent the same active dataset.
- Two-way observation selection works.
- Measurement selection is consistent.
- Missing/non-finite observations map correctly.
- Project and dataset changes update both components.
- Empty and unavailable states are handled.
- Scientific integrity requirements are satisfied.
- Relevant tests and full regression suite pass.
- Documentation reflects actual implementation.

Recommend one of:

- **Stage 2.3 Complete** — all required criteria verified.
- **Stage 2.3 Complete with documented limitations** — only if remaining limitations are explicitly acceptable under the approved scope and do not violate required criteria.
- **Stage 2.3 Incomplete** — one or more required criteria remain unmet.

Do not mark Stage 2.3 complete simply because the implementation work is finished.

### H. Handoff to Stage 2.4

If Stage 2.3 is complete, provide a concise handoff describing:

- What the application can now do.
- The relevant modules and interfaces.
- How the selected light-curve measurement is accessed.
- How the selected dataset and observation identity are represented.
- Any relevant constraints for the upcoming BLS implementation.
- Known limitations that Stage 2.4 must respect.

Do not begin Stage 2.4.

## 15. Git and user-work protections

- Do not commit.
- Do not push.
- Do not reset, clean, or alter Git history.
- Do not discard or overwrite unrelated user changes.
- Do not modify the original research FITS file.
- Do not modify Foundation documents.
- Do not perform destructive cleanup.
- Do not make unapproved scope or architecture changes.

Leave all changes in the working tree for user review.

**Stop after presenting the final report. Do not begin Stage 2.4 or any additional work without a separate request and approval.**