# Stage 2.5 — Record Analysis Operations and Parameters

Objective: Establish a persistent record of the scientific operations performed within a research project, including the datasets, measurements, parameters, methods, and results associated with each operation.

Stage 2.4 establishes the BLS analysis workflow. Stage 2.5 builds on that functionality by ensuring the application remembers what analysis was performed, how it was configured, and what it produced.

The application should no longer depend on displaying only the most recent analysis result. Instead, users should be able to return to a project, inspect previously performed operations, and understand the context in which their results were generated.

This stage establishes the foundation for later reproducibility and analysis-history capabilities. It does not implement a complete analysis-replay engine.

# Stage 2.5 — Record Analysis Operations and Parameters

## Objective

Implement a persistent operation-recording system that documents the scientific analyses performed within a research project.

The application must remember what it did, not merely display the most recent result.

When an analysis is performed, the application should create a record containing the relevant information needed to identify, inspect, and understand that operation after the project is closed and reopened.

This stage builds on the completed Stage 2.4 BLS workflow and establishes the foundation for future reproducibility capabilities.

## 1. Operation Records

The application should create a record for each supported scientific analysis operation.

Each record should identify:

- The operation performed.
- The date and time the operation was performed.
- The research project associated with the operation.
- The dataset analyzed.
- The specific measurements and input columns used.
- The selected flux measurement and associated uncertainty field, where applicable.
- The analysis method and relevant software information.
- The parameters and configuration used.
- Any preprocessing or quality-filtering steps applied.
- The results produced by the operation.
- Relevant uncertainty estimates.
- Warnings, limitations, and assessment information.
- Other provenance information necessary to understand the operation.

The exact record structure should be established during the design and planning task.

Do not assume every future analysis operation will have identical parameters or result structures.

## 2. BLS Analysis Recording

The initial implementation should support recording the BLS workflow established in Stage 2.4.

A BLS operation record should retain the relevant information needed to identify and understand the analysis, including:

- Source dataset identity.
- Selected flux measurement.
- Associated measurement uncertainties.
- Search configuration.
- Period range and duration configuration.
- Other BLS parameters.
- Data-preparation information.
- Candidate results.
- Period, epoch, duration, and depth estimates.
- BLS power and relevant candidate information.
- Parameter uncertainties and their estimation method.
- Detection-assessment results and null-model information, where available.
- Warnings and limitations.
- Relevant software and method information.

The record should preserve the distinction between the original BLS results, uncertainty estimates, and detection-assessment results.

Do not discard relevant results merely because another part of the analysis was unsuccessful or inconclusive.

## 3. Project Association and Persistence

Every operation record must be associated with the research project in which the operation was performed.

The application should preserve operation records when:

- An analysis is completed.
- The project is saved.
- The project is closed.
- The project is reopened.
- The user returns to the project at a later time.

Records should remain associated with the correct datasets and analysis results.

The implementation should account for missing datasets, unavailable source files, incomplete records, and persistence failures.

Follow the existing approved project architecture and storage decisions.

Do not use this stage as an opportunity to redesign the permanent storage architecture.

## 4. Operation History Inspection

Users should be able to inspect previously recorded operations within their research projects.

The application should provide an appropriate way to:

- View recorded operations.
- Identify the operation type.
- Identify when it was performed.
- Identify the dataset and measurements used.
- Inspect relevant parameters.
- Inspect recorded results.
- Review uncertainty and detection-assessment information.
- Review warnings and limitations.

The exact interface and level of detail should be established during planning.

The application must distinguish historical operation records from the currently displayed or newly generated analysis results.

## 5. Provenance and Reproducibility Foundation

Operation records should provide enough information to support later scientific traceability and reproducibility.

A user should be able to determine:

- What data was analyzed.
- Which measurements were selected.
- Which method was used.
- Which parameters were supplied.
- What preparation was applied.
- What results were produced.
- What uncertainties and limitations were reported.
- Which relevant software and method versions were involved.

Records should accurately represent what actually happened.

Do not invent missing metadata or assume that an operation used a particular preprocessing step when it did not.

Distinguish between:

- Original scientific measurements.
- Analysis inputs.
- Derived or prepared data.
- Analysis configuration.
- Generated results.
- Operation metadata.

## 6. Future Compatibility

Although the initial implementation focuses on BLS, the operation-recording design should avoid unnecessarily tying the entire system to BLS-specific fields.

Future operations may include other scientific analyses with different inputs, parameters, outputs, and provenance requirements.

The design should therefore consider how different operation types can be recorded without creating an unnecessarily complicated universal framework.

Do not implement support for unrelated future analysis methods in this stage.

## 7. Testing and Verification

Testing should establish that:

- Operations are recorded correctly.
- The correct project and dataset are associated with each record.
- Input measurements and parameters are represented accurately.
- Results, uncertainties, and warnings are retained.
- Multiple operations can be recorded without overwriting one another.
- Records survive project save, close, and reopen.
- Historical records remain associated with their original datasets.
- Missing or unavailable data is handled appropriately.
- Incomplete or failed operations are represented accurately.
- Existing project and Stage 2.4 functionality remains intact.

Use portable test fixtures and temporary project data.

The standard test suite must not depend on the user's permanent Kepler-10b FITS file.

## 8. Scope Exclusions

Stage 2.5 does not implement:

- Complete analysis replay.
- Automatic reconstruction of every previous analysis.
- Automatic rerunning of historical operations.
- General-purpose workflow automation.
- Full scientific notebook functionality.
- New scientific analysis methods.
- New BLS algorithms or uncertainty methods.
- Archive integration.
- Permanent storage architecture redesign.
- Unrelated application redesign.

These capabilities may be considered in later stages.

## 9. Expected Outcome

At the completion of Stage 2.5, the application should retain a persistent history of supported scientific analysis operations within each research project.

A user should be able to reopen a project and inspect what analyses were performed, which datasets and measurements were used, which parameters were supplied, and what results and limitations were recorded.

This establishes the foundation for later reproducibility, traceability, and analysis-replay capabilities without attempting to implement the complete replay system prematurely.

## Suggested task breakdown and filenames

I recommend dividing Stage 2.5 into five tasks. This separates the record design, underlying record structure, actual recording behavior, user-facing inspection, and final verification.

| Task  | Name                                                 | Primary responsibility                                                          |
| ----- | ---------------------------------------------------- | ------------------------------------------------------------------------------- |
| 2.5.1 | Operation Record Design and Implementation Planning  | Inspect the existing architecture and design the operation-recording system.    |
| 2.5.2 | Operation Record Model and Persistence               | Implement the record structure and its project-level persistence.               |
| 2.5.3 | Analysis Operation Recording and Results Integration | Capture actual BLS operations, parameters, results, and provenance.             |
| 2.5.4 | Operation History Inspection and Project Integration | Allow users to view and inspect historical records within projects.             |
| 2.5.5 | Testing, Documentation, and Completion Verification  | Verify recording, persistence, inspection, integrity, and Stage 2.5 completion. |

### Suggested filenames

Use these names consistently for each task's overview and prompting document:

Task 2.5.1 — Operation Record Design and Implementation Planning

Design the structure, requirements, interfaces, and implementation boundaries.

`task 2.5.1 Operation Record Design and Implementation Planning OVERVIEW.md`

`task 2.5.1 Operation Record Design and Implementation Planning PROMPTING.md`

Task 2.5.2 — Operation Record Model and Persistence

Implement the operation-record data structure and save/reopen behavior.

`task 2.5.2 Operation Record Model and Persistence OVERVIEW.md`

`task 2.5.2 Operation Record Model and Persistence PROMPTING.md`

Task 2.5.3 — Analysis Operation Recording and Results Integration

Connect the existing BLS workflow to the recording system.

`task 2.5.3 Analysis Operation Recording and Results Integration OVERVIEW.md`

`task 2.5.3 Analysis Operation Recording and Results Integration PROMPTING.md`

Task 2.5.4 — Operation History Inspection and Project Integration

Provide the interface for viewing and inspecting historical operations.

`task 2.5.4 Operation History Inspection and Project Integration OVERVIEW.md`

`task 2.5.4 Operation History Inspection and Project Integration PROMPTING.md`

Task 2.5.5 — Testing, Documentation, and Completion Verification

Verify the complete operation-recording workflow and assess Stage 2.5 completion.

`task 2.5.5 Testing, Documentation, and Completion Verification OVERVIEW.md`

`task 2.5.5 Testing, Documentation, and Completion Verification PROMPTING.md`

## Important design boundary

There is one architectural distinction worth preserving throughout Stage 2.5:

Recording an operation is not the same as being able to replay it.

For example, an operation record might retain:

- The dataset identity.
- The selected PDCSAP_FLUX measurement.
- The BLS period range and duration settings.
- The uncertainty method and its settings.
- The candidate results.
- The detection assessment.
- The relevant software and method information.

That would allow the user to inspect what happened and understand the result later.

Replaying the operation would require additional capabilities: retrieving the original inputs, reconstructing the analysis environment, restoring all required settings, and executing the analysis again. That is deliberately outside this stage.

Recommended sequence: Complete 2.5.1 planning first, review and approve its design, then proceed through the implementation tasks. In particular, Task 2.5.1 should inspect the actual Stage 2.4 results and the existing provisional project-persistence architecture before deciding how operation records should be stored.