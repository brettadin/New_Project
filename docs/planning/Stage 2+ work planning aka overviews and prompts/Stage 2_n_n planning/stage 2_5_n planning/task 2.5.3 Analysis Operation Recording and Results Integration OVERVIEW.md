# Task 2.5.3 — Analysis Operation Recording and Results Integration

Stage 2.5: Operation Records

## 1. Purpose

Task 2.5.3 connects the operation-record model and persistence system implemented in Task 2.5.2 to the application's actual scientific analysis workflow.

The goal is for the application to automatically create and save an operation record whenever a user performs a BLS analysis.

Currently, an analysis can produce results, but those results need to become part of the project's persistent scientific history. The application should retain not just the latest displayed result, but also the information describing how that result was produced.

This task establishes that connection.

## 2. Scope of implementation

The work should focus on integrating operation recording into the existing BLS analysis workflow.

It should not redesign the BLS algorithm, change the scientific methodology, or introduce additional analysis methods.

### A. Connect BLS analysis to the operation-record system

The existing BLS workflow should interact with the operation-record model and persistence interfaces created in Task 2.5.2.

When a user initiates an analysis, the application should:

1. Identify the active research project.
2. Identify the dataset being analyzed.
3. Capture the selected measurement and associated uncertainty information.
4. Capture the BLS configuration and parameters.
5. Create an operation record.
6. Execute the analysis.
7. Associate the resulting output with that operation record.
8. Persist the completed record.

The integration should use the established interfaces rather than bypassing the operation-record system.

### B. Record the actual analysis inputs

The operation record must describe the data that the BLS analysis actually used.

Relevant information includes:

- Source dataset identity.
- Selected flux measurement, such as `PDCSAP_FLUX` or `SAP_FLUX`.
- Associated uncertainty column.
- Time column and time reference.
- Measurement units, where available.
- Data selection or exclusions, if any.
- Any preprocessing or quality filtering actually applied.
- Relevant warnings or missing metadata.

It is important to distinguish between the original imported dataset and the specific data supplied to the analysis.

The record must not imply that preprocessing occurred when it did not.

### C. Record BLS configuration and parameters

The application should retain the actual configuration used for each analysis.

This includes the BLS parameters established by the existing implementation, such as:

- Period search range.
- Period-grid resolution or frequency factor.
- Transit duration search configuration.
- Number of periods or other search settings, where applicable.
- Other parameters that influence the calculation.

The precise fields should follow the existing BLS implementation and the approved operation-record design.

The application should record the values actually passed to the analysis, not merely display default values or values that were available in the interface.

### D. Integrate BLS results into operation records

The results produced by BLS should be associated with the corresponding operation record.

Relevant results include the information already produced by the application's BLS implementation, such as:

- Best-fit period.
- Transit epoch.
- Transit duration.
- Transit depth.
- BLS power.
- Periodogram information.
- Phase-folded light-curve information.
- Transit model information.
- Associated uncertainty estimates.
- Detection assessment and relevant warnings.

The implementation should preserve the distinction between numerical results, uncertainty estimates, and scientific interpretation.

For example:

- A candidate detection is not a confirmed planet.
- Parameter uncertainty is not the same as detection significance.
- A false-alarm probability is conditional on its specified noise-only null model; it is not the probability that a detected period is correct.

The record should retain the assessment and limitations produced by the existing analysis workflow without overstating what the results establish.

### E. Handle incomplete and failed analyses

Operation recording should account for analyses that do not complete successfully.

The integration should handle situations such as:

- Invalid analysis configuration.
- Insufficient usable measurements.
- Missing required data.
- Numerical or computational errors.
- Analysis interrupted before completion.
- Results generated with warnings or limitations.

Where the approved record model supports it, the application should retain an appropriately classified operation record rather than silently losing the attempt.

A failed or incomplete analysis must never be represented as a successful completed analysis.

The record should preserve relevant error and warning information.

### F. Preserve the relationship between analysis and project

Each BLS operation record must remain associated with the correct research project and input dataset.

The system should support multiple analyses of the same dataset.

For example, a user might analyze the same light curve using different period ranges or transit-duration configurations. Each execution should produce its own identifiable operation record.

The records must not overwrite one another simply because they analyzed the same dataset.

This is important for comparing different analysis attempts and preserving research history.

## 3. Integration with the existing application

The implementation should connect the existing BLS workflow to operation recording without unnecessarily changing the user interface.

The existing analysis behavior should remain intact.

The integration should ensure that:

- Starting an analysis triggers the appropriate recording process.
- The correct project and dataset are identified.
- The actual analysis inputs are captured.
- The results are associated with the correct operation.
- The operation record is saved through the established persistence system.
- Persistence failures are handled clearly.
- The existing result-display workflow continues to function.

Any changes to the user interface should be limited to what is necessary for correct integration.

A complete operation-history interface is not part of this task.

## 4. Scientific integrity and reproducibility

This task is particularly important because it connects scientific calculations to their provenance.

The operation record should make it possible to understand:

- Which dataset was analyzed.
- Which measurement was selected.
- Which uncertainty information was used.
- Which parameters were supplied.
- Which results were produced.
- What warnings or limitations accompanied those results.
- Which software and analysis method were involved, to the extent supported by the existing design.

The application must preserve the distinction between recorded facts and scientific interpretation.

It must not silently change the underlying dataset or alter analysis results simply to make them easier to store.

This task establishes the information needed for later inspection and reproducibility work. It does not implement automatic replay or guarantee that historical analyses can be rerun identically.

## 5. Persistence requirements

Task 2.5.3 should use the operation-record persistence system implemented in Task 2.5.2.

It should not introduce a separate BLS-specific storage mechanism unless the approved design explicitly requires one.

The implementation must verify that:

- BLS records are saved to the correct project.
- Results remain associated with their original operation.
- Multiple operations can be saved independently.
- Records survive closing and reopening the project.
- Existing project and dataset information remains intact.

The provisional storage limitations established by D6 remain in effect. This task does not authorize a permanent storage architecture redesign.

## 6. Testing and verification

Testing should establish that the BLS workflow and operation-record system work together correctly.

### A. Integration tests

Verify that:

- Executing BLS creates an operation record.
- The correct project and dataset are associated with the record.
- Actual measurement and uncertainty selections are retained.
- Actual BLS parameters are retained.
- Results are associated with the correct operation.
- Warnings and limitations are retained.
- Multiple BLS executions produce separate records.

### B. Failure-handling tests

Verify that:

- Invalid configurations do not produce misleading successful records.
- Failed analyses are represented according to the approved status model.
- Partial results are not misrepresented as complete results.
- Persistence failures are handled without silently losing or misrepresenting analysis outcomes.

### C. Persistence tests

Verify that:

- BLS operation records can be saved.
- Records can be retrieved after reopening a project.
- Multiple records remain independently accessible.
- Historical results and configuration values are preserved.

### D. Regression tests

Verify that the existing functionality remains operational:

- Project lifecycle.
- Dataset import and persistence.
- Light-curve visualization.
- BLS analysis.
- Existing uncertainty and detection-assessment behavior.

Tests should use portable fixtures and temporary directories, not depend on the user's absolute Kepler-10b dataset path.

## 7. Documentation requirements

Follow the documentation-maintenance requirements in `AGENTS.md`.

Update the relevant documentation to describe:

- How BLS analysis creates operation records.
- Which inputs and parameters are captured.
- How results are associated with records.
- How incomplete and failed operations are represented.
- How BLS records are persisted.
- Any known limitations.
- Relevant integration and regression testing.

Update the roadmap and development log accurately.

Keep the distinction between functionality that is implemented and functionality reserved for later tasks.

Foundation documents must remain unchanged.

## 8. Explicit exclusions

The following are outside Task 2.5.3:

- Designing or rebuilding the operation-record model.
- Redesigning project persistence.
- Building the operation-history interface.
- Adding record-search or filtering screens.
- Automatic reconstruction or replay of historical analyses.
- Automatically rerunning previous operations.
- Adding new scientific analysis methods.
- Changing the BLS algorithm or its scientific assumptions.
- Introducing new preprocessing methods.
- Adding automated research workflows.
- Implementing a permanent database architecture.

The model and persistence foundation belong to Task 2.5.2. The user-facing history functionality belongs to Task 2.5.4.

## 9. Expected outcome

At the end of Task 2.5.3, performing a BLS analysis should automatically produce a persistent operation record containing the relevant inputs, configuration, results, uncertainty information, warnings, and project associations.

A user should be able to close and reopen a project without losing the records of previously executed BLS analyses.

The application will then have a functioning connection between its scientific analysis workflow and its operation-record system.

This provides the foundation for Task 2.5.4, where users will be able to inspect their operation history through the application interface.

## 10. Completion criteria

Task 2.5.3 can be considered complete when:

1. The existing BLS workflow is connected to the approved operation-record system.
2. Each BLS execution creates an appropriately identified operation record.
3. Actual analysis inputs and parameters are captured.
4. BLS results and relevant uncertainty information are associated with the correct record.
5. Warnings, limitations, and failures are represented accurately.
6. Multiple analyses can be recorded independently.
7. Records persist and remain retrievable after reopening a project.
8. Existing project, import, visualization, and analysis functionality continues to work.
9. Integration and regression tests pass.
10. Relevant documentation and development-status records are updated and verified.

Task 2.5.3 is not the completion of Stage 2.5. Operation-history inspection (Task 2.5.4) and final testing, documentation, and completion verification (Task 2.5.5) remain outstanding.