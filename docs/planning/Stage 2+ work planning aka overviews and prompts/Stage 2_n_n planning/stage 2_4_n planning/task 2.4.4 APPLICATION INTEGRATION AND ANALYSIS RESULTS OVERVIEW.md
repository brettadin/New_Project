# Task 2.4.4 — Application Integration and Analysis Results Overview

Stage: 2.4 — BLS Analysis and Uncertainty\
Task: 2.4.4 — Application Integration and Analysis Results

## 1. Objective

Integrate the completed BLS search functionality from Task 2.4.2 and the uncertainty and detection-assessment functionality from Task 2.4.3 into the application's existing interface.

The objective is to allow a user to run a transit search on an imported light-curve dataset, inspect the resulting analysis, and understand the candidate parameters, uncertainties, and statistical assessment.

This task connects the scientific analysis functionality to the application workflow. It should not reimplement the underlying scientific algorithms.

The application should provide a usable workflow for:

1. Selecting a project and imported light-curve dataset.
2. Selecting the flux measurement to analyze.
3. Configuring and running a BLS search.
4. Reviewing detected candidate signals.
5. Inspecting transit parameters and their uncertainties.
6. Reviewing detection-assessment results and limitations.
7. Visualizing the analysis results.
8. Retaining the relationship between results and their original dataset and analysis configuration.

## 2. Review Existing Implementation and Architecture

Before implementation, inspect the completed work from:

- Task 2.2 — Light-Curve Import.
- Task 2.3 — Data Table and Light-Curve Visualization.
- Task 2.4.1 — BLS Analysis Design and Implementation Planning.
- Task 2.4.2 — BLS Transit Search Implementation.
- Task 2.4.3 — Transit Parameter Uncertainty and Detection Assessment.

Review the actual implementation rather than assuming that the original plans were followed exactly.

Identify:

- Existing project and dataset selection interfaces.
- Current table and light-curve visualization components.
- BLS search interfaces and result structures.
- Uncertainty and detection-assessment result structures.
- Existing application navigation and layout.
- How scientific operations are initiated and reported.
- How errors and warnings are currently displayed.
- Which documentation and tests need updating.

The integration should follow the existing architecture and avoid unnecessary redesign.

## 3. BLS Analysis Workflow Integration

Integrate the BLS analysis workflow into the application.

The user should be able to initiate a transit search using an imported light-curve dataset.

### Dataset and measurement selection

The workflow should:

- Use the dataset associated with the active project.
- Allow selection of the appropriate imported dataset.
- Support the available flux measurements.
- Default to PDCSAP_FLUX, consistent with the existing detection-workflow decision.
- Allow SAP_FLUX to be analyzed separately.
- Associate the correct uncertainty measurement with each flux type.

| Flux measurement | Associated uncertainty |
| ---------------- | ---------------------- |
| PDCSAP_FLUX      | PDCSAP_FLUX_ERR        |
| SAP_FLUX         | SAP_FLUX_ERR           |

The application must not silently switch measurements or mix their uncertainties.

### Search configuration

Expose the BLS search parameters established in Task 2.4.1 and implemented in Task 2.4.2.

The interface should make it possible to configure the approved search settings without requiring the user to modify source code.

Include appropriate validation and explanations for configuration inputs.

Do not introduce new search parameters or change the underlying search methodology without approval.

### Running the analysis

The application should:

- Validate the selected dataset and configuration.
- Run the existing BLS implementation.
- Handle invalid inputs and execution failures.
- Provide appropriate feedback while analysis is running.
- Present successful results and relevant warnings.
- Avoid freezing the interface during computationally expensive work, using an approach consistent with the existing architecture.

## 4. Analysis Results Presentation

Create an application interface for inspecting BLS analysis results.

The presentation should make the scientific meaning of the results understandable without obscuring important technical details.

### Candidate parameters

Display the available parameters for each detected candidate:

- Period.
- Transit epoch.
- Transit duration.
- Transit depth.
- BLS power.

Include actual units and time references.

For example:

- Period: days.
- Epoch: the dataset's applicable time reference, such as BKJD.
- Duration: the appropriate time unit.
- Depth: the applicable flux or relative-depth representation.

Do not invent units or assume a time reference when metadata is unavailable.

### Parameter uncertainties

Display the uncertainty results produced by Task 2.4.3.

Where available, show:

- Period uncertainty.
- Epoch uncertainty.
- Duration uncertainty.
- Depth uncertainty.
- Uncertainty method.
- Reliability or calibration limitations.

Make it clear which values are parameter estimates and which represent uncertainty.

If an uncertainty could not be calculated, display that status rather than substituting zero or an arbitrary value.

### Detection assessment

Present the detection-assessment results separately from the candidate parameters.

Depending on what Task 2.4.3 actually implements, this may include:

- Detection statistics.
- False alarm probability.
- Noise-only null-model information.
- Simulation configuration.
- Assessment outcome.
- Warnings and limitations.

Clearly explain that statistical distinguishability from a specified noise-only model is not equivalent to planetary confirmation.

If FAP is displayed, preserve its conditional interpretation: it is not the probability that a candidate is a planet or that its period is correct.

### Candidate comparisons

Where multiple candidates are available, provide a way to inspect and compare them.

The user should be able to distinguish:

- The strongest BLS peak.
- Other candidate peaks.
- Possible aliases or harmonics.
- Candidates with ambiguous or inconclusive assessments.

Do not automatically present the strongest peak as the confirmed planetary period.

## 5. Scientific Visualization Integration

Integrate the analysis results with the existing scientific visualization components.

The goal is to make the relationship between the original light curve and the detected transit-like signal visible.

The approved design should determine the exact presentation, but relevant visualizations may include:

### BLS periodogram

Display BLS power against the searched period range.

The visualization should allow the user to inspect candidate peaks and understand where candidate periods were identified.

### Phase-folded light curve

Display the selected light curve folded at a candidate period.

The visualization should help the user inspect whether observations align with a repeating transit-like signal.

### Transit model or candidate representation

If supported by the existing BLS implementation, display the corresponding box-shaped transit representation.

Clearly distinguish the model from actual observations.

### Visualization requirements

- Preserve original observations.
- Do not modify the underlying light-curve dataset.
- Clearly distinguish measurements from models and derived representations.
- Use appropriate units and labels.
- Handle missing and non-finite observations.
- Preserve the relationship between the selected candidate and its visualizations.
- Ensure changing candidates updates the displayed analysis appropriately.

Do not introduce full transit fitting or physical transit modeling as part of this task.

## 6. Analysis Configuration and Reproducibility

The application should make it possible to understand how a particular analysis was performed.

Retain or expose the relevant information from the existing analysis result structures, including:

- Dataset identity.
- Selected flux measurement.
- Associated uncertainty measurement.
- BLS search configuration.
- Data-preparation information.
- Uncertainty-estimation configuration.
- Detection-assessment configuration.
- Random seeds and simulation settings, where applicable.
- Relevant software or method information.
- Warnings and limitations.

The user should be able to distinguish results generated using different datasets, measurements, or search configurations.

This task should prepare the application for the more complete analysis-operation recording planned in Task 2.5.

Do not independently implement the complete operation-history system here.

## 7. Error Handling and User Feedback

Integrate the scientific analysis workflow with the application's existing error-handling approach.

Account for situations such as:

- No project selected.
- No dataset imported.
- Dataset unavailable or corrupt.
- Required measurements missing.
- Unavailable uncertainty measurements.
- Invalid search configuration.
- BLS search failure.
- Uncertainty estimation failure.
- Detection assessment failure.
- Inconclusive candidate results.
- Visualization unavailable.

The application should distinguish between:

1. Analysis completed successfully.
2. Analysis completed with warnings or limitations.
3. Analysis completed but produced inconclusive results.
4. Analysis failed and could not produce usable results.

A failure in uncertainty estimation or detection assessment should not automatically erase an otherwise valid BLS search result.

Where possible, preserve and display the results that were successfully produced, while clearly identifying incomplete assessment components.

## 8. Project and Dataset Integration

Ensure the integrated workflow behaves correctly when the user changes projects or datasets.

Consider:

- Opening another project.
- Closing the active project.
- Switching datasets.
- Selecting a different flux measurement.
- Running multiple analyses with different configurations.
- Returning to a previously inspected analysis result.

Prevent stale results from being displayed as though they belong to the currently selected dataset.

Maintain clear associations between analysis results and the data from which they were produced.

Permanent persistence and full operation-history functionality remain governed by their existing architectural decisions and Task 2.5 scope. Do not independently redesign storage.

## 9. Testing and Validation

Test the integrated application workflow, not just the individual scientific functions.

Use portable synthetic datasets and temporary project data for routine automated tests.

The standard test suite must not depend on the permanent Kepler-10b FITS file or an absolute local path.

Testing should cover:

| Area                    | What needs verification                                     |
| ----------------------- | ----------------------------------------------------------- |
| Dataset selection       | Correct dataset reaches the analysis workflow               |
| Flux selection          | PDCSAP and SAP remain separate                              |
| Uncertainty association | Correct uncertainty field is used                           |
| Search configuration    | Inputs are validated and passed correctly                   |
| BLS execution           | Existing BLS implementation is invoked correctly            |
| Candidate results       | Parameters and units are displayed correctly                |
| Uncertainty results     | Estimates and limitations are represented correctly         |
| Detection assessment    | Statistical results and assumptions are presented correctly |
| Periodogram             | Correct search results are visualized                       |
| Phase folding           | Selected candidate controls the folded light curve          |
| Candidate switching     | Results and visualizations update together                  |
| Project switching       | No stale or mismatched results remain                       |
| Error handling          | Failures and incomplete assessments are handled clearly     |
| Scientific integrity    | Original measurements remain unchanged                      |

Include integration tests that exercise the complete workflow from dataset selection through result presentation.

Optional manual verification using the real Kepler-10b dataset can supplement the automated tests.

Do not treat successful interface execution as proof of scientific validity. The underlying methods and calibration evidence remain the responsibility of Tasks 2.4.2 and 2.4.3.

## 10. Documentation Maintenance

Follow the documentation requirements in `AGENTS.md`.

Update appropriate documentation to reflect:

- The integrated analysis workflow.
- User-facing configuration options.
- Analysis result presentation.
- Visualization behavior.
- Error and warning handling.
- Reproducibility information.
- Architecture and module responsibilities.
- Integration testing.
- Current Stage 2.4 progress.

Reconcile documentation against actual implementation.

Clearly distinguish functionality that is implemented from functionality that remains planned.

Do not modify Foundation documents.

## 11. Explicit Scope Exclusions

Task 2.4.4 does not include:

- Reimplementing BLS.
- Changing the approved BLS search methodology.
- Reimplementing uncertainty calculations.
- Reimplementing detection assessment or FAP.
- Full transit fitting.
- Detailed planetary physical parameter estimation.
- Atmospheric characterization.
- Radial-velocity analysis.
- Multi-planet modeling beyond the existing approved candidate-search capability.
- Automatic detrending or normalization.
- Automatic quality filtering.
- External archive integration.
- Permanent storage redesign.
- Complete analysis-operation history.
- Unrelated application redesign or refactoring.

These responsibilities belong to other tasks or require separate approval.

## 12. Expected Outcome

At completion, the application should provide a coherent user-facing BLS analysis workflow.

A user should be able to:

1. Open a project containing an imported light-curve dataset.
2. Select the dataset and flux measurement.
3. Configure and execute a BLS transit search.
4. Inspect candidate transit parameters.
5. Review parameter uncertainties.
6. Review detection-assessment results and limitations.
7. Inspect the periodogram and phase-folded light curve.
8. Switch between candidates and inspect their corresponding results.
9. Understand how the analysis was configured and what its limitations are.

The original light-curve measurements must remain unchanged throughout this process.

Completion of Task 2.4.4 should establish the integrated application workflow, while final scientific validation and Stage 2.4 completion verification remain for Task 2.4.5.

## 13. What comes after 2.4.4?

The remaining task is 2.4.5 — Testing, Scientific Validation, and Completion Verification.

That task will assess the entire Stage 2.4 workflow rather than just individual components.

It should verify:

- BLS search correctness.
- Parameter uncertainty and UQ-009 calibration evidence.
- Detection-assessment behavior.
- Noise-only controls and injected-signal validation.
- Alias and competing-candidate handling.
- Application integration.
- Visualization and result presentation.
- Scientific integrity and reproducibility.
- Documentation accuracy.
- Regression testing across the existing application.

The distinction: 2.4.4 makes the analysis usable through the application. 2.4.5 establishes whether the complete analysis workflow is sufficiently tested, validated, and documented to consider Stage 2.4 complete.