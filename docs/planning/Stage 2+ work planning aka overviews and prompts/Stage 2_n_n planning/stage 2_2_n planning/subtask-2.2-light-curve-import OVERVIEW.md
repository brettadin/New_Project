# What needs to be done


# Stage 2.2 — Light-Curve Import

Primary objective: Enable the application to import a real astronomical light-curve dataset into an existing research project, inspect its contents and metadata, and preserve its scientific integrity.

This is the next major development milestone after project lifecycle management. It establishes the data foundation needed for visualization (2.3) and BLS analysis (2.4).

The initial implementation should focus on your existing Kepler-10b FITS dataset, rather than attempting to support every astronomical data format immediately.

## 1. Dataset selection and import

Initial target identified

[Kepler - Universe Missions - NASA Jet Propulsion Laboratory | NASA Jet Propulsion Laboratory (JPL)](https://images.openai.com/static-rsc-4/dq1kC_0QMsN_QVSWJRG4Y7gqQDq3t8gA4Mx6EE82bErMctmU9KYWejlU1AzsnMWm6udnNGeGzAYXB7Sdwm9hRzXRljZ0q6fPr4H7qG8dAyhz3eVJbUNZeas9Zot7L3f6nNDE0hgSWO1t3eRnEFHa_nhV6evJyYrY7Ami-Mp6v6I?purpose=inline)

Kepler-10b light curve

Existing local dataset:

`kplr011904151-2009131105131_llc_full.fits`

FITS format, long cadence, approximately 9.7 days of observations.

The application needs to:

- Allow the user to select a FITS file through a file dialog.
- Read the file using Astropy.
- Identify the available FITS HDUs (Header/Data Units).
- Identify relevant columns and metadata.
- Extract the selected light-curve measurements.
- Associate the imported dataset with the currently active project.

The importer should not assume every FITS file has exactly the same structure. It should inspect the file and determine whether it contains the information needed for the supported import workflow.

## 2. Identify and interpret scientific data

The selected Kepler dataset contains several important fields:

| Field             | Purpose                         |
| ----------------- | ------------------------------- |
| `TIME`            | Observation timestamps          |
| `SAP_FLUX`        | Simple Aperture Photometry flux |
| `PDCSAP_FLUX`     | Pipeline-corrected flux         |
| `SAP_QUALITY`     | Data-quality flags              |
| `SAP_FLUX_ERR`    | Flux uncertainty                |
| `PDCSAP_FLUX_ERR` | Corrected flux uncertainty      |
| `CADENCENO`       | Observation cadence number      |

The importer needs to understand the distinction between these measurements.

For example:

- SAP_FLUX represents the original aperture-photometry measurement.
- PDCSAP_FLUX contains pipeline corrections.
- Their values should not be treated as interchangeable.
- Time values need their time reference and convention preserved.
- Flux values need their units and measurement context preserved.

The initial workflow should make it possible to select which flux column is used for subsequent analysis.

## 3. Validate the imported dataset

The importer needs to identify potential problems without silently altering the data.

Examples include:

- Missing required columns.
- Missing or incomplete metadata.
- NaN or infinite measurements.
- Invalid timestamps.
- Missing uncertainty values.
- Nonzero quality flags.
- Unexpected data types or incompatible column structures.

Your Kepler dataset already provides some useful validation cases:

- 476 observation rows.
- Approximately four missing flux measurements.
- 37 nonzero quality flags.

The application should report these conditions clearly.

Important: Nonzero quality flags should not automatically cause observations to be discarded. The quality-handling policy needs to be scientifically justified and recorded.

## 4. Preserve the original data and provenance

Important design area

This is one of the most important parts of Subtask 2.2.

The application needs to distinguish between:

1. The original FITS file.
2. The measurements extracted from that file.
3. Any derived or transformed measurements created later.

The import workflow should:

- Preserve the original file unchanged.
- Record the original file location.
- Record source information and relevant metadata.
- Preserve column names, units, time conventions, and measurement context.
- Record import warnings and validation results.
- Avoid silently modifying or discarding measurements.

We also need to establish how the imported dataset is associated with the project and how that association survives saving and reopening.

### Storage consideration

Decision D6 deferred the permanent storage architecture.

Therefore, Subtask 2.2 should not prematurely introduce a complete database or permanent storage redesign.

It should establish a suitable provisional approach for the first working scientific-data import while documenting its limitations and preserving the option to make a formal storage decision later.

## 5. Integrate the importer into the application

The importer must work with the existing project lifecycle.

Expected workflow:

1. Open an existing research project.
2. Select an astronomical FITS file.
3. Inspect its structure and metadata.
4. Validate its measurements and report warnings.
5. Import the selected light-curve data.
6. Associate the dataset with the active project.
7. Save and close the project.
8. Reopen the project and verify that the dataset remains available.

The interface should communicate whether the import succeeded, whether warnings were generated, and what dataset was imported.

## 6. Testing requirements

Testing should cover more than whether one FITS file can be opened.

| Test area           | What needs verification                          |
| ------------------- | ------------------------------------------------ |
| FITS reading        | Correctly reads the selected dataset             |
| HDU inspection      | Identifies the appropriate data structure        |
| Column extraction   | Retrieves the intended measurements              |
| Metadata            | Preserves units and time information             |
| Validation          | Detects missing and invalid values               |
| Quality flags       | Preserves flags and avoids unjustified filtering |
| Original file       | Remains unchanged                                |
| Project integration | Associates data with the correct project         |
| Persistence         | Dataset remains available after reopening        |
| Error handling      | Reports invalid or unsupported files clearly     |

Synthetic test FITS files can be used for controlled edge cases. They should not be presented as real scientific observations or used as substitutes for the actual Kepler dataset in the application workflow.

## 7. Documentation updates

The implementation should update relevant documentation as required by `AGENTS.md`.

Likely affected documents include:

- `docs/MASTER_DEVELOPMENT_ROADMAP.md`
- `docs/development/DEVELOPMENT_LOG.md`
- Relevant architecture or module documentation.
- Data-model documentation.
- Validation and testing documentation.
- Decision records, if implementation exposes a decision requiring formal approval.

The agent should identify the actual affected documents during Plan mode rather than assuming every document needs modification.

## What Subtask 2.2 should deliver

At completion, the application should be able to:

## 2.2 Completion checklist

- Import the existing Kepler-10b FITS dataset.
- Identify and extract the appropriate light-curve measurements.
- Preserve relevant metadata and scientific context.
- Validate data and report warnings.
- Preserve the original file unchanged.
- Associate the imported dataset with a project.
- Save and reopen the project with the dataset still available.
- Pass automated tests.
- Update relevant documentation.

## What is deliberately outside Subtask 2.2?

These belong to later tasks:

| Feature                                     | Planned task |
| ------------------------------------------- | ------------ |
| Data table for viewing measurements         | 2.3          |
| Interactive light-curve graph               | 2.3          |
| Zooming and selecting observations          | 2.3          |
| BLS period search                           | 2.4          |
| Transit period and uncertainty estimation   | 2.4          |
| Recording analysis parameters and results   | 2.5          |
| Replaying previous analyses                 | Stage 3      |
| Downloading observations from NASA archives | Stage 4      |

We should avoid turning the importer into a complete data-processing system before the subsequent tasks have been designed.

## Recommended order of work

I would divide the Plan-mode investigation into these areas, allowing the coding agent to determine whether they should be separate implementation subtasks:

1. FITS inspection and data-model design.
2. FITS import and validation.
3. Project integration and provisional persistence.
4. Automated testing and documentation verification.

These are planning areas, not four pre-approved Build tasks. The Plan-mode review should establish the actual implementation boundaries and identify any decisions requiring your approval.

The central success criterion: After Subtask 2.2, you should be able to open a project, import your real Kepler-10b observations, and retain the measurements and their scientific context when you close and reopen the project.


# plan for subtasks.


Yes. I recommend preparing one Plan prompt and one Build prompt for each implementation task. That gives us a set of ready-to-use instructions without committing us to implementation details before we've inspected the current code.

There is one important distinction: the Build prompts should be treated as drafts requiring revision after the corresponding Plan review, not unconditional authorization to implement.

## Proposed Subtask 2.2 breakdown

I'd organize it into four implementation tasks:

| Task  | Scope                                               | Plan prompt | Build prompt |
| ----- | --------------------------------------------------- | ----------- | ------------ |
| 2.2.1 | FITS inspection and data-model design               | 1           | 1            |
| 2.2.2 | FITS import and validation                          | 1           | 1            |
| 2.2.3 | Project integration and provisional persistence     | 1           | 1            |
| 2.2.4 | Testing, documentation, and completion verification | 1           | 1            |

These are proposed boundaries. The first Plan review should confirm whether they are appropriate.

## What each prompt should accomplish

Plan prompts

- Inspect the current repository and relevant Foundation requirements.
- Review existing architecture, decisions, and documentation.
- Identify dependencies and affected files.
- Identify implementation risks and unresolved decisions.
- Propose a limited implementation approach.
- Identify tests and documentation updates.
- Make no changes.

Build prompts

- Implement only the approved plan.
- Preserve existing functionality.
- Add or update tests.
- Update relevant documentation.
- Run the appropriate tests.
- Report exact changes and verification results.
- Make no commits or pushes.

## How I recommend we prepare them

## Preparation sequence

1. Prepare all four Plan prompts

   Save them as separate Markdown files.
2. Prepare all four Build prompt templates

   Save them alongside their corresponding Plan prompts, with explicit approval and scope boundaries.
3. Review Task 2.2.1 when ready

   Send its Plan prompt to the coding agent.
4. Review the agent's proposal

   We check it against the actual repository and Foundation requirements.
5. Revise and authorize its Build prompt

   Only then does implementation begin.
6. Repeat for the next task

   Later prompts can be adjusted to account for what was actually implemented.

## One additional recommendation

We should prepare the prompts for 2.2 only right now.

For 2.3, 2.4, and 2.5, I would prepare broader task outlines but wait to write detailed Build prompts. Their implementation will depend on decisions made during 2.2.

For example, the visualization task should use the actual data model and interfaces established by the importer, rather than assumptions we make today.

My recommendation: Prepare eight Markdown documents for Subtask 2.2: four Plan prompts and four corresponding Build prompts. Keep them outside the repository, as you have been doing.