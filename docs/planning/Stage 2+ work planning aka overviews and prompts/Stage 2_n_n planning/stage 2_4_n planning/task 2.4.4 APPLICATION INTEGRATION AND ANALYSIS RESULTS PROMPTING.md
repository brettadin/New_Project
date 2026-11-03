# PLAN MODE PROMPT

# PLAN — Task 2.4.4: Application Integration and Analysis Results

**Stage:** 2.4 — BLS Analysis and Uncertainty  
**Task:** 2.4.4 — Application Integration and Analysis Results  
**Mode: PLAN ONLY — Inspect, evaluate, and design. Do not implement.**

## 1. Objective

Inspect the actual application and completed scientific analysis functionality, then develop a detailed implementation plan for integrating BLS transit searches, uncertainty estimates, and detection-assessment results into the existing application interface.

The planned workflow should allow a user to:

1. Select a project and imported light-curve dataset.
2. Select the flux measurement to analyze.
3. Configure and execute a BLS search.
4. Inspect detected candidate signals.
5. Review transit parameters and uncertainties.
6. Review detection-assessment results and limitations.
7. Inspect relevant scientific visualizations.
8. Understand how an analysis was configured and which dataset produced its results.

The integration must use the existing scientific implementations from Tasks 2.4.2 and 2.4.3.

**Do not reimplement BLS, uncertainty estimation, or detection assessment.**

The purpose of this planning task is to establish how those capabilities should be integrated into the application, what interfaces are needed, how results should be presented, and how the complete workflow will be tested.

## 2. Mandatory Repository and Documentation Inspection

Before designing the integration, inspect the actual repository.

Read and follow:

- `AGENTS.md`.
- The current Stage 2 roadmap.
- The development log.
- Relevant architecture documentation.
- Relevant data-flow documentation.
- Relevant data-model documentation.
- Module responsibility documentation.
- Existing testing and validation documentation.
- Relevant decision records.
- Current project state and continuity documentation.

Inspect the actual implementation of:

- Task 2.2 — Light-Curve Import.
- Task 2.3 — Data Table and Light-Curve Visualization.
- Task 2.4.1 — BLS Analysis Design.
- Task 2.4.2 — BLS Transit Search.
- Task 2.4.3 — Transit Parameter Uncertainty and Detection Assessment.

Verify the actual implementation status of each prerequisite.

Do not assume that an earlier plan was implemented exactly as written.

### Inspect the existing application

Identify:

- Main application entry point.
- Main window and application layout.
- Project navigation and project selection.
- Dataset selection and management.
- Existing light-curve table.
- Existing light-curve visualization.
- Existing plotting infrastructure.
- Existing UI controls and interaction patterns.
- Existing error and warning presentation.
- Existing background-task or asynchronous execution approach.
- Existing project lifecycle behavior.
- Existing scientific data access interfaces.

### Inspect the scientific analysis implementation

Identify:

- BLS public interfaces.
- BLS input requirements.
- BLS search configuration.
- BLS result structures.
- Candidate representation.
- Periodogram representation.
- Phase-folding capabilities, if implemented.
- Transit model availability, if implemented.
- Uncertainty estimation interfaces.
- Uncertainty result structures.
- Calibration information.
- Detection-assessment interfaces.
- Noise-only null-model information.
- FAP or alternative detection statistics.
- Warning and inconclusive-result handling.
- Reproducibility information.
- Dataset and measurement associations.

Record actual file paths, class names, function names, and relevant interfaces.

Do not invent interfaces or assume capabilities exist without verifying them.

## 3. Prerequisite Completion and Integration Readiness

Assess whether the completed work provides everything needed for Task 2.4.4.

Evaluate:

- Whether BLS can be invoked independently of the GUI.
- Whether the BLS result structure is suitable for application presentation.
- Whether uncertainty assessment can consume the existing BLS results.
- Whether detection assessment can consume the existing BLS results.
- Whether analysis results retain dataset identity.
- Whether selected flux measurements are represented clearly.
- Whether associated uncertainty measurements are identifiable.
- Whether time references and units are available.
- Whether warnings and limitations are represented.
- Whether candidate information supports visualization.
- Whether analysis configurations are retained.

Identify any missing interface, metadata, or result information required for integration.

Distinguish between:

1. A genuine prerequisite defect.
2. A missing application-integration interface.
3. A presentation requirement.
4. A requirement that belongs to Task 2.5.
5. A requirement that is outside Task 2.4.4.

Do not silently redesign Tasks 2.2, 2.3, 2.4.2, or 2.4.3.

If a prerequisite defect prevents integration, describe it and recommend whether it requires a separate correction or approval.

## 4. Application Workflow Design

Design the complete user-facing workflow.

Consider the appropriate sequence for:

1. Selecting a project.
2. Selecting an imported dataset.
3. Selecting a flux measurement.
4. Reviewing the associated uncertainty measurement.
5. Configuring the BLS search.
6. Validating the configuration.
7. Starting the analysis.
8. Presenting progress and execution status.
9. Displaying candidate results.
10. Selecting and inspecting candidates.
11. Reviewing uncertainty results.
12. Reviewing detection-assessment results.
13. Inspecting visualizations.
14. Switching between candidates or datasets.

Determine where this workflow belongs in the existing application.

Evaluate whether it should use:

- Existing application panels.
- A dedicated analysis panel.
- A separate analysis view.
- A dialog or other existing UI pattern.

Base the recommendation on the actual application architecture.

Do not redesign the entire application.

Identify the necessary user actions, UI states, and transitions.

## 5. Dataset and Flux Measurement Selection

Design how the application will select and validate analysis inputs.

The initial workflow must support:

- PDCSAP_FLUX as the default measurement.
- SAP_FLUX as a separately selectable measurement.
- Correct uncertainty association.

| Selected measurement | Required associated uncertainty |
|---|---|
| PDCSAP_FLUX | PDCSAP_FLUX_ERR |
| SAP_FLUX | SAP_FLUX_ERR |

Verify how the existing dataset model represents these fields.

Plan how the interface will handle:

- Missing flux measurements.
- Missing associated uncertainties.
- Non-finite observations.
- Quality flags.
- Missing time metadata.
- Unsupported or incomplete datasets.
- Dataset switching.
- Empty project or dataset states.

Do not automatically remove nonzero quality flags.

Do not silently switch flux measurements or substitute an unrelated uncertainty field.

Do not introduce automatic normalization, detrending, filtering, or other scientific transformations.

Identify which validation belongs to the existing scientific analysis layer and which validation belongs to the UI.

## 6. BLS Search Configuration and Execution

Design the user-facing configuration interface using the parameters actually supported by the existing BLS implementation.

For each configuration option, document:

- Name.
- Purpose.
- Accepted values or range.
- Default, if established.
- Units.
- Validation requirements.
- Whether it must be user-configurable.

Do not invent new search parameters.

Do not change the approved BLS methodology.

Evaluate how the application should:

- Validate user inputs.
- Present configuration errors.
- Initiate the existing BLS search.
- Report progress.
- Handle long-running calculations.
- Prevent inappropriate duplicate execution.
- Handle cancellation if supported by the existing architecture.
- Report successful completion or failure.

Inspect the existing threading or background-task infrastructure before recommending a new approach.

Consider interface responsiveness without introducing unnecessary complexity.

Identify the precise interfaces between the UI and BLS analysis layer.

## 7. Candidate Results Presentation

Design how BLS results should be presented.

Inspect the actual candidate result structures before proposing UI fields.

Consider presentation of:

- Period.
- Transit epoch.
- Transit duration.
- Transit depth.
- BLS power.
- Relevant units.
- Time reference.
- Search configuration.
- Candidate warnings.

Determine how multiple candidates should be displayed and selected.

Consider how the interface should distinguish:

- Highest-power candidate.
- Other candidate peaks.
- Competing candidates.
- Potential aliases and harmonics.
- Candidates with inconclusive assessments.

Do not automatically describe the strongest peak as the correct planetary period.

Do not present a BLS candidate as a confirmed planet.

Specify what information belongs in:

- Candidate lists or tables.
- Detailed candidate views.
- Supporting metadata.
- Warning and limitation displays.

## 8. Uncertainty Results Presentation

Inspect the actual Task 2.4.3 uncertainty result structures.

Design how the application will display:

- Period uncertainty.
- Epoch uncertainty.
- Duration uncertainty.
- Depth uncertainty.
- Uncertainty method.
- Calibration information.
- Reliability information.
- Assumptions and limitations.

Specify how the interface should distinguish:

- Parameter estimate.
- Uncertainty estimate.
- Unavailable uncertainty.
- Unreliable uncertainty.
- Inconclusive assessment.

Do not assume all parameters have valid uncertainty estimates.

Do not substitute zero or arbitrary values when an estimate is unavailable.

Do not calculate uncertainty in the GUI.

The interface must consume the existing uncertainty-assessment outputs.

## 9. Detection Assessment Presentation

Inspect the actual Task 2.4.3 detection-assessment implementation.

Design how the application should display available results, such as:

- Detection statistics.
- FAP, if implemented.
- Null-model information.
- Simulation configuration.
- Assessment outcome.
- Relevant assumptions.
- Warnings and limitations.

Determine how much statistical detail should be immediately visible and what should be available through expanded details or explanatory text.

Preserve the distinction between:

1. A BLS candidate being detected.
2. Statistical distinguishability from the specified noise-only model.
3. Confirmation that the signal represents a planet.

If FAP is presented, its interpretation must remain conditional on the specified null model.

It must not be described as the probability that the candidate is a planet or that the candidate period is correct.

Do not invent confidence classifications or thresholds.

If detection assessment is incomplete or inconclusive, design an appropriate presentation rather than hiding the result.

## 10. Scientific Visualization Integration

Inspect the existing Task 2.3 plotting implementation and the actual analysis outputs.

Design how the application will integrate available analysis visualizations.

### Periodogram

Determine how the existing BLS periodogram can be displayed.

Consider:

- Period axis and units.
- BLS power axis.
- Candidate peaks.
- Selected-candidate indication.
- Search boundaries.
- Interaction with candidate selection.

### Phase-folded light curve

Determine whether the existing implementation provides the necessary data and functionality.

If supported, design:

- Phase or folded-time axis.
- Flux axis and units.
- Selected candidate period.
- Observation points.
- Relevant uncertainty representation.
- Transit model overlay, if available.

### Transit model

Determine whether the existing BLS implementation exposes a model suitable for presentation.

If so, design how it should be distinguished from actual observations.

Do not invent a model or implement full transit fitting.

### Integration with existing light-curve visualization

Determine whether the original light curve should remain available alongside the analysis visualizations.

Consider:

- Switching between original and derived views.
- Candidate selection updating the appropriate visualizations.
- Measurement selection.
- Dataset switching.
- Missing and non-finite observations.
- Plot labels and units.
- Avoiding unnecessary duplication of scientific data.

Do not modify original observations.

If a planned visualization is not supported by the existing scientific implementation, report the missing capability and identify whether it belongs to this task or requires separate approval.

## 11. Analysis Configuration and Reproducibility

Design how the application will expose or retain the information needed to understand an analysis.

Inspect the actual result structures and determine how the interface can present:

- Dataset identity.
- Selected flux measurement.
- Associated uncertainty measurement.
- BLS configuration.
- Data-preparation information.
- Uncertainty-estimation configuration.
- Detection-assessment configuration.
- Random seeds and simulation settings, where applicable.
- Relevant method or software information.
- Warnings and limitations.

Ensure that analyses using different datasets, measurements, or configurations can be distinguished.

Clarify the boundary between:

- Displaying analysis configuration and provenance in Task 2.4.4.
- Persisting and recording analysis operations in Task 2.5.

Do not implement a complete operation-history system.

Do not redesign permanent storage.

## 12. Error Handling and Application States

Design how the application handles the following states:

- No active project.
- No dataset selected.
- No dataset available.
- Dataset unavailable or corrupt.
- Required measurement missing.
- Associated uncertainty unavailable.
- Invalid search configuration.
- Analysis running.
- Analysis completed successfully.
- Analysis completed with warnings.
- BLS search failed.
- Uncertainty estimation failed.
- Detection assessment failed.
- Candidate assessment inconclusive.
- Visualization unavailable.
- Project or dataset switched during analysis.

Determine whether partial results should remain available when a later assessment stage fails.

For example, a valid BLS candidate should not automatically be discarded because uncertainty estimation or detection assessment failed.

Design how stale results are prevented from being displayed as though they belong to the currently selected dataset.

Identify any application-level state management required.

## 13. Project and Dataset Lifecycle Integration

Inspect existing project lifecycle behavior.

Design how analysis results and UI state behave when the user:

- Opens another project.
- Closes the active project.
- Switches datasets.
- Selects another flux measurement.
- Runs another search.
- Returns to a previously inspected analysis result.

Determine which information should be cleared, retained, or reloaded.

Maintain clear associations between results and their source dataset and configuration.

Do not assume that analysis persistence has been implemented unless the repository proves it.

Do not implement permanent persistence or complete operation-history functionality as part of this task unless explicitly approved.

## 14. Architecture and Module Responsibilities

Develop a concrete integration architecture based on the existing repository.

Identify:

- Existing modules to reuse.
- Existing modules that need modification.
- New modules or classes genuinely required.
- UI-to-analysis interfaces.
- Result-presentation interfaces.
- Visualization interfaces.
- State-management responsibilities.
- Error-handling responsibilities.
- Background-execution responsibilities.

For each proposed file change, specify:

- File path.
- Current responsibility.
- Proposed change.
- Reason for change.
- Dependencies.
- Relevant tests.

Avoid:

- Duplicate scientific logic.
- Duplicated data models.
- GUI code containing scientific calculations.
- Unnecessary abstraction layers.
- Unapproved dependencies.
- Unrelated refactoring.

Do not create new architectural layers unless justified by the actual codebase.

## 15. Testing and Integration Validation Plan

Develop a detailed test plan for the integrated workflow.

Use portable synthetic datasets and temporary project data for routine automated tests.

The standard test suite must not depend on the permanent Kepler-10b FITS file or an absolute local path.

Include appropriate tests for:

### Dataset and input selection

- Correct dataset selection.
- Correct flux measurement selection.
- PDCSAP and SAP separation.
- Correct uncertainty association.
- Missing required measurements.
- Dataset switching.

### BLS execution

- Correct configuration passed to the existing BLS implementation.
- Input validation.
- Successful execution.
- Execution failure.
- Invalid configuration.
- Interface responsiveness.
- Background execution, where applicable.

### Results presentation

- Candidate parameters.
- Units and time references.
- Multiple candidates.
- Candidate selection.
- Uncertainty estimates.
- Unavailable or unreliable uncertainties.
- Detection-assessment results.
- FAP interpretation, if applicable.
- Warnings and limitations.

### Visualization

- Periodogram.
- Candidate peak selection.
- Phase-folded light curve, if supported.
- Transit model overlay, if supported.
- Candidate switching.
- Dataset switching.
- Measurement switching.
- Missing and non-finite observations.

### Lifecycle and state management

- Project opening and closing.
- Dataset switching.
- Analysis execution during state changes.
- Stale-result prevention.
- Empty and unavailable states.
- Partial results following assessment failure.

### Scientific integrity

Verify that:

- Original observations remain unchanged.
- SAP and PDCSAP remain distinct.
- Correct uncertainty fields are used.
- Quality flags are not silently filtered.
- Missing values are not substituted with zero.
- Units and time references are preserved.
- Derived visualizations are distinguishable from original measurements.

### Integration testing

Plan at least one end-to-end test covering:

1. Opening a project.
2. Selecting a dataset.
3. Selecting a flux measurement.
4. Configuring a BLS search.
5. Running the search.
6. Inspecting candidate results.
7. Reviewing uncertainty and detection assessment.
8. Inspecting available visualizations.

Identify the relevant test files and proposed fixtures.

Do not weaken existing tests or claim that UI execution alone validates the scientific methods.

## 16. Documentation Plan

Identify the documentation that will need updating during implementation.

Follow `AGENTS.md` documentation-maintenance requirements.

Consider:

- Stage roadmap.
- Development log.
- Architecture documentation.
- Data-flow documentation.
- Module responsibilities.
- Data-model and result-structure documentation.
- UI and workflow documentation.
- Testing and validation documentation.
- Project state and continuity records.

For each document, explain:

- Why it needs updating.
- What implementation information it should contain.
- Whether it should remain unchanged.

Do not modify documentation during PLAN.

Do not modify Foundation documents.

Avoid creating duplicate documentation.

## 17. Task Boundaries

Define the precise boundary between Task 2.4.4 and the remaining Stage 2.4 work.

### Task 2.4.4 includes

- Application integration of existing BLS functionality.
- User-facing dataset and measurement selection.
- BLS configuration and execution controls.
- Candidate result presentation.
- Uncertainty result presentation.
- Detection-assessment presentation.
- Integration of supported analysis visualizations.
- Application-level error and state handling.
- Project and dataset lifecycle integration.
- Reproducibility information presentation.
- Integration tests and documentation.

### Task 2.4.4 excludes

- Reimplementing BLS.
- Changing BLS methodology.
- Reimplementing uncertainty estimation.
- Reimplementing detection assessment or FAP.
- Full transit fitting.
- Detailed planetary physical parameter estimation.
- Atmospheric characterization.
- Radial-velocity analysis.
- New automatic normalization or detrending.
- Automatic quality filtering.
- External archive integration.
- Permanent storage redesign.
- Complete analysis-operation history.
- Unrelated application redesign.

### Task 2.4.5 boundary

Task 2.4.5 remains responsible for final Stage 2.4 testing, scientific validation, documentation reconciliation, and completion verification.

Task 2.4.4 should perform the integration tests necessary to verify its own implementation, but must not claim final Stage 2.4 scientific validation or completion.

## 18. Implementation Breakdown

Recommend a practical sequence of implementation steps for Task 2.4.4.

For each proposed step, specify:

- Objective.
- Files or modules affected.
- Dependencies on earlier steps.
- Implementation requirements.
- Tests.
- Documentation updates.
- Completion criteria.

The sequence should minimize unnecessary changes and keep the application usable throughout development.

Identify which steps can be implemented independently and which require earlier interfaces to be completed.

Do not begin implementation.

## 19. Required PLAN Report

Return a structured report with the following sections.

### A. Prerequisite completion assessment
Actual status of Tasks 2.2, 2.3, 2.4.1, 2.4.2, and 2.4.3.

### B. Current application architecture
Relevant windows, panels, modules, interfaces, and responsibilities.

### C. Existing scientific analysis interfaces
Actual BLS, uncertainty, and detection-assessment interfaces and result structures.

### D. Integration readiness
What is ready, what is missing, and any genuine prerequisite defects.

### E. Proposed user workflow
Step-by-step user interaction and application states.

### F. Dataset and measurement selection
Proposed interface, validation, and uncertainty association.

### G. BLS configuration and execution
Actual supported configuration options and integration approach.

### H. Candidate results presentation
Proposed candidate list, details, units, and selection behavior.

### I. Uncertainty presentation
Proposed display and handling of unavailable, unreliable, or inconclusive results.

### J. Detection-assessment presentation
Proposed display, statistical interpretation, null-model details, and limitations.

### K. Scientific visualization integration
Periodogram, phase-folded light curve, transit model, and original light-curve relationships.

### L. Reproducibility and analysis metadata
Information exposed in the interface and boundary with Task 2.5.

### M. Error handling and lifecycle behavior
Failure states, partial results, project/dataset switching, and stale-result prevention.

### N. Architecture and file-change plan
Concrete existing and proposed modules, responsibilities, and interfaces.

### O. Testing and validation plan
Targeted tests, integration tests, fixtures, and scientific-integrity checks.

### P. Documentation plan
Documents to update and documents intentionally unchanged.

### Q. Implementation sequence
Practical implementation steps with dependencies and completion criteria.

### R. Scope and unresolved decisions
Confirm exclusions, identify assumptions, and list decisions requiring user approval.

### S. Overall readiness recommendation
State whether Task 2.4.4 is ready for Build, conditionally ready, or blocked.

Clearly distinguish:

- Verified repository facts.
- Recommendations.
- Assumptions.
- Unresolved decisions.
- Prerequisite defects.
- Requirements that need explicit approval.

## 20. PLAN Restrictions

This is a planning task only.

Do not:

- Modify source code.
- Modify tests.
- Modify documentation.
- Add dependencies.
- Implement UI components.
- Implement analysis integration.
- Change scientific algorithms.
- Modify research datasets.
- Modify the original Kepler-10b FITS file.
- Modify Foundation documents.
- Commit or push.
- Reset, clean, or alter Git history.
- Discard or overwrite user changes.

You may inspect files, execute read-only repository inspection commands, and run existing tests only if doing so is necessary to verify the current state. Do not modify the repository through inspection or testing.

Do not begin Task 2.4.4 implementation.

**Stop after delivering the complete PLAN report and wait for explicit user approval before any Build work.**


# BUILD MODE PROMPT

# BUILD — Task 2.4.4: Application Integration and Analysis Results

**Stage:** 2.4 — BLS Analysis and Uncertainty  
**Task:** 2.4.4 — Application Integration and Analysis Results  
**Mode: BUILD — Implement the approved application integration plan only.**

## 1. Objective

Integrate the existing BLS transit-search functionality from Task 2.4.2 and the uncertainty and detection-assessment functionality from Task 2.4.3 into the application's existing user interface.

The completed workflow should allow a user to:

1. Open a project containing an imported light-curve dataset.
2. Select the dataset and flux measurement to analyze.
3. Configure and execute a BLS search.
4. Inspect detected candidate signals.
5. Review candidate transit parameters and uncertainties.
6. Review detection-assessment results and their limitations.
7. Inspect available scientific visualizations.
8. Understand which dataset, measurement, and analysis configuration produced the results.

**Do not reimplement the scientific analysis methods.** This task connects existing scientific functionality to the application.

Follow the approved Task 2.4.4 PLAN report, the actual repository architecture, and all applicable requirements in `AGENTS.md`.

## 2. Mandatory Pre-Build Verification

Before making changes:

1. Read `AGENTS.md`.
2. Read the current Stage 2 roadmap and development log.
3. Read the approved Task 2.4.4 PLAN report.
4. Review the actual implementation of Tasks 2.2, 2.3, 2.4.1, 2.4.2, and 2.4.3.
5. Inspect the current application architecture and UI.
6. Verify the actual scientific analysis interfaces and result structures.
7. Inspect the Git working tree.
8. Identify existing user changes and preserve them.
9. Identify the exact source, test, and documentation files expected to change.

Reconcile the approved PLAN against the current repository.

If the repository differs materially from the PLAN, or an essential prerequisite is missing, stop and report the discrepancy.

Do not silently redesign completed scientific functionality to make integration easier.

Do not introduce new architectural decisions, dependencies, or scope beyond the approved plan.

## 3. Application Workflow Integration

Implement the user-facing workflow established in the approved PLAN.

Integrate it into the existing application using the approved layout and navigation approach.

The workflow must support:

- Project selection through the existing project-management interface.
- Dataset selection through the existing dataset-management interface.
- Flux measurement selection.
- BLS search configuration.
- Search execution.
- Candidate selection and inspection.
- Uncertainty and detection-assessment presentation.
- Available analysis visualizations.

Use existing application components and interaction patterns where appropriate.

Avoid unnecessary redesign of the main window, project navigation, dataset management, or unrelated application functionality.

The interface should clearly communicate which project and dataset are currently being analyzed.

## 4. Dataset and Flux Measurement Selection

Integrate dataset selection with the existing scientific data model.

Support the approved initial measurement choices:

| Selected measurement | Associated uncertainty |
|---|---|
| PDCSAP_FLUX | PDCSAP_FLUX_ERR |
| SAP_FLUX | SAP_FLUX_ERR |

Requirements:

- Default to PDCSAP_FLUX.
- Allow SAP_FLUX to be selected independently.
- Preserve the distinction between the two measurements.
- Always associate the correct uncertainty measurement.
- Validate that required input fields are available.
- Display unavailable measurements appropriately.
- Do not silently substitute one measurement for another.
- Do not substitute an unrelated uncertainty field.
- Preserve actual units and time metadata.
- Preserve quality flags and missing-value information.

Do not automatically filter nonzero quality flags.

Do not introduce automatic normalization, detrending, filtering, or other scientific transformations.

Use the existing analysis input-preparation interfaces. Do not duplicate scientific preparation logic in the GUI.

## 5. BLS Search Configuration and Execution

Integrate the existing BLS implementation from Task 2.4.2.

Expose the search configuration options established in the approved design and supported by the actual implementation.

For each user-facing option:

- Display an understandable label.
- Provide an appropriate input control.
- Display units where applicable.
- Validate the entered value.
- Present useful validation feedback.
- Pass the validated configuration to the existing BLS interface.

Do not invent new BLS configuration parameters.

Do not change the underlying BLS search methodology.

### Execution behavior

Implement the approved execution approach.

The application should:

- Validate the selected dataset and measurement.
- Validate the search configuration.
- Initiate the existing BLS analysis.
- Provide execution feedback.
- Keep the interface responsive using the existing or approved background-execution approach.
- Handle analysis failures.
- Prevent inappropriate duplicate execution.
- Handle cancellation only if supported by the approved design and actual implementation.

Do not add unnecessary threading or background-task infrastructure if the existing application already provides an appropriate mechanism.

The GUI must not contain BLS calculations or duplicate the scientific analysis logic.

## 6. Candidate Results Presentation

Implement the candidate-results interface using the actual BLS result structures.

Display available candidate parameters, including where supported:

- Period.
- Transit epoch.
- Transit duration.
- Transit depth.
- BLS power.
- Units.
- Time reference.
- Relevant search configuration.
- Candidate warnings.

Allow the user to inspect multiple candidates where the existing BLS implementation provides them.

Implement the approved candidate-selection behavior.

When a candidate is selected, its corresponding details and visualizations must update consistently.

Clearly distinguish:

- Highest-power candidate.
- Other candidate peaks.
- Competing candidates.
- Possible aliases or harmonics.
- Candidates with inconclusive assessments.

Do not automatically describe the highest-power candidate as the correct planetary period.

Do not describe a BLS candidate as a confirmed planet.

Do not calculate or modify candidate parameters in the GUI.

## 7. Uncertainty Results Presentation

Integrate the uncertainty results from Task 2.4.3.

Display the available uncertainty estimates alongside their corresponding parameter estimates.

Where available, present:

- Period uncertainty.
- Epoch uncertainty.
- Duration uncertainty.
- Depth uncertainty.
- Uncertainty-estimation method.
- Calibration information.
- Reliability information.
- Relevant assumptions and limitations.

Make it visually clear which values are parameter estimates and which are uncertainty estimates.

Handle the actual result states supported by Task 2.4.3, including:

- Usable uncertainty estimate.
- Uncertainty estimate with limitations.
- Unavailable uncertainty.
- Unreliable estimate.
- Inconclusive assessment.
- Failed uncertainty assessment.

Do not:

- Calculate uncertainties in the GUI.
- Substitute zero for unavailable uncertainty.
- Invent uncertainty values.
- Hide unreliable or inconclusive results.
- Present uncertainty as detection significance.

Preserve the method and calibration information returned by the scientific analysis layer.

## 8. Detection-Assessment Results Presentation

Integrate the detection-assessment results from Task 2.4.3.

Display the statistics and assessment information actually provided by the implementation.

Depending on the implemented result structure, this may include:

- Detection statistics.
- False alarm probability.
- Noise-only null-model information.
- Simulation configuration.
- Assessment outcome.
- Statistical assumptions.
- Warnings and limitations.

Clearly distinguish:

1. Detection of a BLS candidate.
2. Statistical distinguishability from the specified noise-only model.
3. Confirmation that the signal represents a planet.

These are separate conclusions.

If FAP is displayed, retain its conditional interpretation:

- It is conditional on the specified noise-only null model.
- It is not the probability that the candidate is a planet.
- It is not the probability that the candidate period is correct.
- It does not prove that aliases or systematic effects are absent.

Do not invent detection thresholds, confidence levels, or planetary classifications.

Do not recalculate FAP or other detection statistics in the GUI.

If assessment is incomplete or inconclusive, display that state accurately.

## 9. Scientific Visualization Integration

Integrate the visualizations supported by the actual scientific implementation and approved PLAN.

Reuse the existing Task 2.3 visualization infrastructure wherever possible.

### BLS periodogram

If supported by the existing BLS results, display:

- Period axis and units.
- BLS power axis.
- Candidate peaks.
- Selected-candidate indication.
- Relevant search boundaries.

Ensure the visualization corresponds to the currently selected analysis result.

### Phase-folded light curve

If supported, display the selected candidate's phase-folded observations.

Use the existing data and analysis interfaces.

Preserve:

- Actual observation values.
- Flux units.
- Measurement identity.
- Relevant uncertainty information.
- The relationship between the candidate period and folded observations.

### Transit model

If the BLS implementation exposes an appropriate model, display it as a derived representation distinct from actual observations.

Do not implement full transit fitting or introduce a new physical transit model.

### Visualization behavior

Ensure:

- Candidate selection updates the relevant visualizations.
- Dataset switching cannot leave stale plots visible.
- Measurement switching updates the displayed data appropriately.
- Labels and units reflect actual metadata.
- Missing and non-finite observations are handled consistently.
- Original observations remain unchanged.
- Derived representations are distinguishable from measured values.

If a planned visualization is not supported by the actual analysis implementation, do not fabricate it. Report the missing capability and follow the approved PLAN's resolution.

## 10. Analysis Configuration and Reproducibility

Expose or retain the analysis information established in the approved design.

Where available, make the following information accessible:

- Project identity.
- Dataset identity.
- Selected flux measurement.
- Associated uncertainty measurement.
- BLS search configuration.
- Data-preparation information.
- Uncertainty-estimation configuration.
- Detection-assessment configuration.
- Random seeds.
- Simulation settings.
- Relevant method or software information.
- Warnings and limitations.

Ensure users can distinguish results produced from different datasets, measurements, and configurations.

Maintain the relationship between each displayed result and its source analysis.

This task prepares the application for the more complete operation-recording functionality planned in Task 2.5.

Do not implement a complete analysis-operation history.

Do not redesign permanent storage.

Do not claim analysis results persist across application restarts unless that behavior is already supported and verified.

## 11. Error Handling and Partial Results

Implement the error-handling and application states established in the approved PLAN.

Handle relevant conditions, including:

- No active project.
- No dataset selected.
- No dataset available.
- Dataset unavailable or corrupt.
- Required flux measurement missing.
- Associated uncertainty unavailable.
- Invalid search configuration.
- BLS search running.
- BLS search failure.
- Uncertainty estimation failure.
- Detection-assessment failure.
- Inconclusive candidate assessment.
- Visualization unavailable.
- Project or dataset changed during analysis.

Distinguish between:

1. Analysis completed successfully.
2. Analysis completed with warnings or limitations.
3. Analysis completed with inconclusive results.
4. Analysis partially completed.
5. Analysis failed.

### Partial-result preservation

A valid BLS result must not automatically be discarded because a later uncertainty or detection-assessment step fails.

Where the actual interfaces permit it:

- Preserve successfully produced BLS results.
- Display available uncertainty results.
- Display available detection-assessment results.
- Identify incomplete assessment components.
- Explain why a component is unavailable.

Do not fabricate missing results.

Use the existing error-handling conventions.

## 12. Project and Dataset Lifecycle Integration

Integrate the workflow with existing project and dataset lifecycle behavior.

Handle:

- Opening another project.
- Closing the active project.
- Switching datasets.
- Selecting another flux measurement.
- Running a new analysis.
- Inspecting another candidate.
- Returning to a previously available analysis result, if supported.

Prevent stale analysis results from being presented as though they belong to the currently selected dataset.

Maintain explicit associations between analysis results and their source dataset and configuration.

Follow the approved PLAN regarding which UI state should be cleared, retained, or restored.

Do not independently implement permanent analysis persistence.

Do not implement the complete Task 2.5 operation-history system.

## 13. Application Architecture and Code Quality

Follow the architecture established by the approved PLAN.

Requirements:

- Reuse existing scientific analysis interfaces.
- Keep scientific calculations outside GUI components.
- Keep UI responsibilities focused on user interaction and presentation.
- Avoid duplicated data models.
- Avoid duplicated validation or scientific preparation logic.
- Avoid unnecessary abstraction layers.
- Avoid unrelated refactoring.
- Preserve existing interfaces unless a change is required and approved.
- Add no unapproved dependencies.

If an interface change is necessary, explain why and keep it as narrow as possible.

Do not change Tasks 2.2, 2.3, 2.4.2, or 2.4.3 scientific behavior merely to simplify UI integration.

If a genuine prerequisite correction is necessary, stop and request approval unless the approved PLAN explicitly authorizes that correction.

## 14. Testing and Integration Validation

Implement tests based on the approved PLAN.

Use portable synthetic datasets and temporary project data.

The standard automated test suite must not depend on the permanent Kepler-10b FITS file or an absolute local path.

### Dataset and measurement selection

Test:

- Correct dataset selection.
- PDCSAP default selection.
- SAP selection.
- Measurement separation.
- Correct uncertainty association.
- Missing measurements.
- Dataset switching.

### BLS configuration and execution

Test:

- Configuration validation.
- Correct configuration passed to the existing BLS interface.
- Successful execution.
- Invalid configuration.
- Execution failures.
- Duplicate execution prevention, where applicable.
- Background execution and interface responsiveness, where applicable.

### Candidate presentation

Test:

- Candidate parameters.
- Units and time references.
- Multiple candidate presentation.
- Candidate selection.
- Candidate switching.
- Competing candidates.
- Warnings and limitations.

### Uncertainty presentation

Test:

- Available uncertainty estimates.
- Correct parameter association.
- Method and calibration information.
- Unavailable uncertainty.
- Unreliable uncertainty.
- Inconclusive uncertainty assessment.
- Failed uncertainty assessment.

### Detection-assessment presentation

Test:

- Available detection statistics.
- FAP presentation, if implemented.
- Null-model information.
- Assessment outcome.
- Warnings and limitations.
- Inconclusive and failed assessments.
- Correct statistical interpretation.

### Visualization

Test supported visualizations:

- Periodogram display.
- Candidate peak selection.
- Phase-folded light curve.
- Transit model representation, if supported.
- Candidate switching.
- Dataset switching.
- Measurement switching.
- Missing and non-finite observations.

### Lifecycle and state management

Test:

- Project opening.
- Project closing.
- Dataset switching.
- Analysis during state changes, where supported.
- Stale-result prevention.
- Empty states.
- Unavailable datasets.
- Partial results after later assessment failures.

### Scientific integrity

Verify that:

- Original measurements remain unchanged.
- SAP and PDCSAP remain separate.
- Correct uncertainty fields are used.
- Nonzero quality flags are not silently filtered.
- Missing values are not substituted with zero.
- Actual units and time references are preserved.
- Models and derived visualizations remain distinguishable from observations.

### End-to-end integration test

Implement at least one appropriate integration test covering the complete supported workflow:

1. Open or establish a project.
2. Select an imported dataset.
3. Select a flux measurement.
4. Configure the BLS search.
5. Execute the search.
6. Inspect candidate results.
7. Review uncertainty results.
8. Review detection-assessment results.
9. Inspect available visualizations.

The test should exercise the actual integration boundaries, not merely mock every component and verify that the UI can display arbitrary values.

Do not weaken existing tests.

Do not treat successful UI execution as proof of scientific validity. Scientific-method validation remains part of Tasks 2.4.2, 2.4.3, and final verification in Task 2.4.5.

## 15. Documentation Maintenance

Follow the documentation-maintenance requirements in `AGENTS.md`.

Before implementation, identify the affected documents.

During implementation, update documentation when functionality, interfaces, architecture, testing, or project progress changes.

Review and update where appropriate:

- Stage roadmap.
- Development log.
- Architecture documentation.
- Data-flow documentation.
- Module responsibilities.
- Data-model and result-structure documentation.
- UI and workflow documentation.
- Testing and validation documentation.
- Project state and continuity records.

Documentation must describe actual implemented behavior.

Clearly distinguish:

- Implemented functionality.
- Tested functionality.
- Known limitations.
- Deferred functionality.
- Planned Task 2.5 work.

Do not mark Task 2.4.4 complete until its approved completion criteria are verified.

Do not mark Task 2.4.5 or Stage 2.4 complete.

Do not modify Foundation documents.

Do not create duplicate documentation where existing documents are appropriate.

## 16. Explicit Scope Exclusions

Do not:

- Reimplement BLS.
- Change the approved BLS methodology.
- Reimplement uncertainty estimation.
- Reimplement detection assessment or FAP.
- Introduce new statistical thresholds.
- Implement full transit fitting.
- Perform detailed planetary physical parameter estimation.
- Implement atmospheric characterization.
- Implement radial-velocity analysis.
- Expand multi-planet functionality beyond the existing approved capability.
- Introduce automatic detrending or normalization.
- Introduce automatic quality filtering.
- Integrate external archives.
- Redesign permanent storage.
- Implement complete analysis-operation history.
- Redesign unrelated application components.
- Perform unrelated refactoring.

These responsibilities are outside Task 2.4.4 or belong to other approved tasks.

If an implementation requirement crosses these boundaries, stop and report it.

## 17. Final Verification

After implementation:

1. Run targeted application-integration tests.
2. Run targeted candidate-presentation tests.
3. Run uncertainty and detection-assessment presentation tests.
4. Run visualization integration tests.
5. Run lifecycle and state-management tests.
6. Run relevant regression tests.
7. Run the full test suite.
8. Record exact commands and results.
9. Investigate failures rather than suppressing them.
10. Review the complete working-tree diff.
11. Verify that scientific calculations remain in their existing analysis layer.
12. Verify that displayed results correspond to the correct dataset and analysis configuration.
13. Verify that partial results are handled correctly.
14. Verify that original measurements remain unchanged.
15. Compare implementation against the approved PLAN.
16. Reconcile documentation against actual code and test evidence.

Do not claim that tests passed unless they were actually executed successfully.

Do not claim scientific validation beyond the evidence established by the earlier scientific tasks.

Do not claim that analysis persistence or operation history exists unless it is actually implemented and verified.

## 18. Required Final Report

Provide a structured report with the following sections.

### A. Implementation summary
- Functionality integrated.
- Overall completion status.
- Relationship to the approved PLAN.

### B. User workflow
- Dataset selection.
- Flux measurement selection.
- Search configuration.
- Search execution.
- Candidate inspection.
- Uncertainty and detection-assessment review.
- Visualization workflow.

### C. BLS integration
- Existing interfaces used.
- Configuration controls.
- Execution approach.
- Error and progress handling.

### D. Candidate results presentation
- Displayed parameters.
- Units and time references.
- Multiple-candidate behavior.
- Candidate selection.
- Warnings and limitations.

### E. Uncertainty presentation
- Results displayed.
- Method and calibration information.
- Unavailable or unreliable result handling.

### F. Detection-assessment presentation
- Statistics displayed.
- Null-model information.
- FAP presentation, if implemented.
- Statistical interpretation.
- Warnings and limitations.

### G. Scientific visualization
- Periodogram.
- Phase-folded light curve.
- Transit model, if supported.
- Integration with the original light-curve visualization.

### H. Reproducibility and metadata
- Dataset and measurement associations.
- Search configuration.
- Uncertainty and detection configuration.
- Simulation information.
- Known persistence limitations.

### I. Error handling and lifecycle
- Failure states.
- Partial results.
- Project and dataset switching.
- Stale-result prevention.

### J. Files changed
For every changed file, explain:
- File path.
- What changed.
- Why it changed.
- Which approved PLAN requirement it addresses.

Separate source-code, test, and documentation changes.

### K. Test results
Include:
- Exact commands executed.
- Targeted test results.
- Integration test results.
- Regression test results.
- Full suite results.
- Failed or skipped tests.
- Remaining limitations.

### L. Scientific integrity verification
Explicitly report whether:

- Original measurements remain unchanged.
- SAP and PDCSAP remain separate.
- Correct uncertainty fields are associated.
- Quality flags remain accessible.
- Missing values are not replaced with zero.
- Units and time references are preserved.
- Derived representations are distinguished from actual observations.
- GUI code contains no duplicated scientific calculations.

### M. Documentation reconciliation
Identify:
- Documents updated.
- Documents inspected but intentionally unchanged.
- Remaining documentation gaps.

### N. Scope verification
Confirm whether:

- Existing BLS functionality was reused.
- Existing uncertainty functionality was reused.
- Existing detection-assessment functionality was reused.
- Application integration was completed.
- Supported visualizations were integrated.
- No unapproved scientific methods were introduced.
- No unapproved dependencies were added.
- Task 2.5 responsibilities were left outside scope.
- Task 2.4.5 remains outstanding.
- No Foundation documents were modified.

### O. Remaining issues and handoff
List:

- Incomplete requirements.
- Known limitations.
- Unresolved decisions.
- Any prerequisite defects.
- Information needed by Task 2.4.5.
- Recommended next steps.

Recommend whether Task 2.4.4 is complete.

Do not begin Task 2.4.5.

## 19. Git and User-Work Protections

- Do not commit.
- Do not push.
- Do not reset, clean, or alter Git history.
- Do not discard or overwrite user changes.
- Do not modify the original Kepler-10b FITS file.
- Do not modify Foundation documents.
- Do not perform destructive cleanup.

Leave all changes in the working tree for user review.

**Stop after presenting the complete final report. Wait for separate user approval before beginning Task 2.4.5.**