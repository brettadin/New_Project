# Task 2.2.3 — Project integration and provisional persistence
## Working Progress Log

**Task:** 2.2.3 — Project integration and provisional persistence  
**Development Stage:** Stage 2.2 — Light-Curve Import  
**Status:** Planning
**Started:** [11/4/2026]  
**Last Updated:** [Date]

**Related Documents:**
- `task 2.2.3 Project integration and provisional persistence OVERVIEW.md`
- `task 2.2.3 Project integration and provisional persistence PROMPTING.md`
- `task 2.2.3 Project integration and provisional persistence WORKING PROGRESS LOG.md`

---

# 1. Initial Review

## ChatGPT — Initial Review of Existing Documents

No. I can read ZIP archives, Markdown documents, Python files, and source code without requiring advanced data analysis.

The archive was successfully opened, and I confirmed its contents. The failure happened when I attempted to display the extracted documents through a tool that wasn't necessary for the task.

I should have used the regular file-reading workflow instead. That was a tooling mistake, not a limitation of ChatGPT.

The renamed archive is now accessible. I've opened it, extracted the repository snapshot, and reviewed the Subtask 2.2 overview, the 2.2.3 overview, the 2.2.2 implementation record, and the relevant source files.

We can proceed without advanced data analysis. I used ordinary archive and file-reading tools.
1. Where we stand
The repository snapshot identifies the following status:
Subtask	Status	Verified implementation record
2.2.1 — FITS inspection and data model	Complete	48 focused tests; 224 full-suite tests at completion
2.2.2 — FITS import and validation	Complete	60 focused tests; 233 non-GUI tests passed
2.2.3 — Project integration and provisional persistence	Pending	Planning needed
2.2.4 — Testing and documentation verification	Pending	Follows 2.2.3

These are the recorded results, not a fresh execution of the test suite.

The important distinction is that 2.2.1 and 2.2.2 deliberately created an independent scientific data model and importer. Neither implemented project-level dataset management or persistence.

That is precisely the responsibility of 2.2.3.
2. What 2.2.3 needs to accomplish
The central objective is:

Make imported scientific datasets first-class contents of research projects, with reliable saving and recovery.

The expected workflow is:
1. Open a research project.
2. Import a FITS light curve.
3. Associate it with the active project.
4. Save the project.
5. Close the project/application.
6. Reopen the project.
7. Recover the original imported dataset, including its scientific measurements and metadata.
This must work without changing the original FITS file or prematurely deciding the application's permanent storage architecture.
3. Existing architecture: important findings
I inspected the actual implementation rather than relying solely on the planning documents.

The current architecture has three relevant layers:
Component	Existing responsibility
src/light_curve.py	Scientific dataset model and serialization
src/project_repository.py	Reading and writing project metadata
src/project_service.py	Project creation, opening, saving, closing, and active-project management

What already exists
A. Scientific data model

LightCurveDataset already has:
- A persistent dataset UUID.
- Original filename and source path.
- Optional checksum and source identifiers.
- Time measurements and time-reference metadata.
- Multiple measurement columns.
- Associated uncertainties.
- Quality flags and cadence numbers.
- Validation findings.
- Import timestamp and notes.
- to_dict() and from_dict() methods.
This is important: we should not unnecessarily redesign or duplicate the data model.

B. Project persistence

ProjectRepository currently:
- Creates project directories.
- Saves project.json.
- Loads and validates project metadata.
- Uses temporary files and atomic replacement for metadata writes.
- Supports project discovery.
C. Project lifecycle

ProjectService currently manages:
- Active project selection.
- Project creation and opening.
- Project saving.
- Project closing.
- Dirty-state tracking.
- Project switching and location handling.
However, its persistence currently concerns ProjectMetadata, not scientific datasets.
The central integration gap
There is currently no established mechanism for:
- Maintaining a collection of imported datasets within a project.
- Saving the actual measurement arrays.
- Restoring datasets when a project opens.
- Tracking dataset-specific changes in project dirty state.
These are the principal areas that 2.2.3 needs to address.
4. Technical considerations for the planning phase
I see several issues that deserve explicit investigation before approving implementation.

1. Project metadata versus scientific data

We should avoid putting hundreds or thousands of measurement values directly into project.json.

The project metadata should identify its datasets, while scientific measurements should have an appropriate persisted representation.

2. Serialization and scientific integrity

The existing to_dict() converts NumPy arrays into Python lists.

That provides a useful starting point, but the persistence design needs to consider:
- Large datasets.
- Floating-point precision.
- NaN and infinite values.
- Optional arrays.
- Integer quality flags.
- Exact reconstruction of uncertainties and metadata.
In particular, JSON serialization needs careful handling of non-finite floating-point values.

3. Dirty-state integration

Currently, ProjectMetadata.is_dirty tracks metadata changes.

Importing a dataset must also make the project dirty. Saving the project must clear that state only after the associated data and project references have been successfully persisted.

4. Atomicity and failure recovery

Saving project metadata and saving scientific datasets are potentially separate filesystem operations.

We need to consider what happens if one succeeds and the other fails.

A partially completed save must not leave the project appearing clean when its scientific data has not been saved.

5. Original source availability

The imported dataset should remain recoverable even if the original FITS file is moved or deleted.

The persisted scientific representation and the original source-file reference must be distinguishable.

6. Multiple datasets

The data model already supports independent dataset identities.

The project integration should not unnecessarily restrict projects to one light curve, even though the initial scientific workflow uses Kepler-10b.
5. Decisions and constraints that must carry into 2.2.3
There are several established boundaries we must preserve.
Item	Requirement
D6	Permanent storage architecture remains deferred
Project schema	Currently version 2
Original FITS	Must remain unchanged
Scientific measurements	Must be preserved without filtering or transformation
Quality flags	Must survive persistence
Multiple flux types	SAP and PDCSAP remain independent
Multiple datasets	Should be supported where practical
Project lifecycle	Existing Save/Discard/Cancel behavior must remain intact
Foundation	Read-only; no modifications

Relevant governing documents include:
- docs/Foundation/4.6_Data Lineage, Processing History and Traceability.md
- docs/Foundation/4.7_Data Provenance, Metadata and Source Attribution.md
- docs/Foundation/4.9_Local Data, Caching and Offline Resource Access.md
- docs/Foundation/6.4_Research Projects and Workspace Integration.md
- docs/Foundation/9.4_Data Storage and Management Infrastructure.md
- docs/Foundation/10.9_User Oversight, Approval and Communication.md
These are particularly important because this task establishes how scientific research materials become persistent project contents.
6. My recommended planning structure
I would have OpenCode investigate five areas before proposing implementation.
1. Existing architecture and integration points
   
   Inspect the project model, repository, service, application startup, importer, and existing tests.
2. Dataset ownership and association
   
   Determine how projects identify datasets, maintain dataset identity, and support multiple imported light curves.
3. Provisional persistence design
   
   Evaluate suitable local storage approaches, serialization, scientific fidelity, and compatibility with D6.
4. Project lifecycle integration
   
   Establish save, reopen, dirty-state, project switching, and failure-recovery behavior.
5. Testing and implementation boundaries
   
   Define measurable acceptance criteria, affected files, regression coverage, and any decisions requiring approval.
I would specifically require OpenCode to compare reasonable storage approaches rather than automatically selecting JSON, SQLite, or NumPy files simply because they are convenient.
7. What I want from the first Plan review
The first plan should answer these questions:
1. What is the smallest maintainable architecture that satisfies 2.2.3?
2. Should scientific datasets be stored individually or collectively?
3. How should project metadata reference persisted datasets?
4. How should dataset changes affect project dirty state?
5. How can saving multiple files avoid inconsistent project state?
6. How should missing original FITS files be handled?
7. How should corrupt or missing persisted datasets be reported?
8. Can we preserve schema v2 without unnecessary migration?
9. What existing functionality needs modification?
10. What tests demonstrate that the implementation is scientifically reliable?
The plan should also identify any conflicts with existing architecture or Foundation requirements.

8. Proposed next step
I recommend we begin with Planning Version 1, using the existing 2.2.3 overview as the scope authority.

The sequence will be:
1. I'll prepare the initial OpenCode Plan prompt.
2. You submit it to OpenCode.
3. We examine its proposed architecture and implementation plan together.
4. I'll identify weaknesses, missing tests, unnecessary complexity, and scientific-integrity concerns.
5. We revise the plan until it is implementation-ready.
6. You approve the final plan before Build mode.
One important boundary: We are not authorizing a permanent storage architecture through this task. We are authorizing a carefully limited first implementation of provisional persistence.

The existing 2.2.3 overview is a good starting specification. I don't recommend rewriting it before we've seen what the first architectural investigation discovers.



### Prompt review

 Review: 2.2.3 PROMPTING.md

The file is comprehensive and provides a sound starting point. Its PLAN prompt is appropriately investigation-focused: it requires prerequisite verification, inspection of the existing project lifecycle, evaluation of persistence options, scientific-integrity protections, failure handling, testing, and a structured report.

I would retain most of its structure. I would make several targeted changes before using it for the first planning pass.

One important distinction: the file contains both a PLAN prompt and a BUILD prompt. For the first OpenCode interaction, use only the PLAN portion (sections 1–12, ending at line 435). The BUILD prompt should remain separate from this initial investigation.

## 1. What the existing PLAN prompt already handles well

| Area                                   | Assessment                                                                                     |
| -------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Governance and Foundation requirements | Good. Explicitly read-only and approval-aware.                                                 |
| Prerequisite verification              | Good. Requires inspection of actual 2.2.1 and 2.2.2 implementations.                           |
| Existing project architecture          | Good. Covers the model, repository, service, lifecycle, and dirty state.                       |
| Dataset association                    | Good. Addresses identity, provenance, multiple datasets, and project ownership.                |
| Provisional persistence                | Good. Explicitly separates provisional storage from the deferred permanent architecture.       |
| Scientific integrity                   | Good. Protects measurements, uncertainties, units, time references, flags, and missing values. |
| Failure handling                       | Good. Includes missing/corrupt data and partial recovery.                                      |
| Testing and documentation              | Good. Requires specific test proposals and identifies documentation impact.                    |
| Approval boundaries                    | Good. Separates recommendations from approved decisions.                                       |

The required Plan report is also useful. Its sections A–M give us a consistent structure for reviewing OpenCode's findings.

## 2. Changes I recommend before the first planning prompt

These are refinements, not reasons to rewrite the whole document.

### A. Make the serialization problem explicit

This is the most important technical addition.

The existing `LightCurveDataset` model has `to_dict()` and `from_dict()` methods. Those methods convert NumPy arrays into Python lists and reconstruct the model. That does not automatically make the model suitable for reliable disk persistence.

In particular, the model intentionally preserves non-finite scientific values such as `NaN` and infinity. Standard JSON does not formally support those values, even though Python's default JSON implementation permits non-standard representations.

The planning prompt should explicitly require OpenCode to investigate:

- Whether the existing serialization methods are suitable for persistence.
- Whether the selected storage format preserves floating-point values accurately.
- How `NaN`, positive infinity, and negative infinity will survive a save/load cycle.
- Whether integer arrays, floating-point arrays, and optional arrays retain their intended types.
- Whether `None` remains distinguishable from an empty array.
- Whether the complete dataset can be reconstructed without losing metadata or validation information.

Why this matters: A dataset that successfully saves and reopens is not necessarily scientifically identical to the dataset that was imported. We need round-trip preservation, not merely successful deserialization.

I would not prescribe JSON, NumPy files, NPZ, or another format in the prompt. OpenCode should evaluate the reasonable options against the actual model and recommend one.

### B. Require a concrete save-transaction design

The current prompt mentions incomplete writes, corrupted data, and persistence failures. It should go one step further and require an explanation of how a save operation remains consistent when multiple files are involved.

For example, suppose a project has three datasets. The application saves two dataset files successfully, then fails while saving the third. What state is the project left in?

The plan should explain:

- Which file or record identifies the datasets belonging to a project.
- The order in which dataset content and project references are written.
- How temporary files and atomic replacement are used, if appropriate.
- What happens when only part of a save succeeds.
- When the project is allowed to become clean.
- How the application detects and handles orphaned or incomplete dataset files.

This is particularly important because the existing project metadata repository already uses atomic replacement for `project.json`. The new persistence mechanism should not undermine that existing guarantee.

### C. Clarify the distinction between source-file availability and dataset availability

The existing prompt handles a missing original FITS file, but I would make the expected distinction more explicit.

There are three separate things:

1. The original FITS file on disk.
2. The imported `LightCurveDataset` held by the application.
3. The persisted representation of that dataset inside the project.

The original FITS file may become unavailable after import. That should not automatically make the project's saved dataset unavailable.

Ask OpenCode to explain whether the project will rely on its persisted dataset representation for reopening, while retaining the original path and provenance as source information.

Also require it to verify what the importer actually does. Recording a source path is not the same as making a copy of the original file.

### D. Make the dirty-state design more specific

The current prompt correctly asks whether the existing dirty-state mechanism needs extending.

The planning report should distinguish:

- Project metadata changes.
- Dataset additions.
- Dataset content changes.
- Dataset removal or association changes, if those operations are included.
- Successful metadata saves versus successful dataset saves.

The key question is whether the application can accidentally mark a project as saved when its scientific data did not save successfully.

OpenCode should trace the actual save and close call paths before recommending a solution. We should avoid a broad project lifecycle rewrite.

### E. Require explicit evaluation of the existing project schema

The current project metadata uses schema version 2. The prompt asks about future schema changes, but I would explicitly require OpenCode to answer:

- Can dataset references be stored separately without changing the project metadata schema?
- Would a separate dataset manifest or index be appropriate?
- Would any proposed design require a schema version increase?
- If so, why is that change necessary now?
- How would existing projects continue to open?

My preference is to avoid a schema change unless the inspected architecture demonstrates that one is necessary. That is a recommendation for evaluation, not an approved design decision.

### F. Add a requirement to inspect the actual GUI integration boundary

The prompt reviews project lifecycle operations, but it could more clearly require tracing where an imported dataset would enter the application.

OpenCode should identify:

- Where the existing import action is initiated, if one exists.
- Which component receives the `LightCurveDataset`.
- Which component owns the active project.
- Whether project services or the main window currently coordinate lifecycle operations.
- Where a dataset collection or repository would logically belong.
- Whether 2.2.3 requires a user-facing import workflow or only the underlying project integration.

That final distinction matters. We should not accidentally expand 2.2.3 into the table interface or other 2.3 work.

### G. Add a clear implementation boundary to the Plan report

The existing prompt asks for likely files to change, which is good. I would also require a proposed minimum implementation boundary:

- Files that must change.
- Files that may need to change depending on the chosen design.
- New files that are justified.
- Existing files that should remain untouched.
- Features explicitly deferred.

This will help prevent OpenCode from turning a focused integration task into a general refactor.

## 3. Additional material to include

I recommend adding four short requirements to the PLAN prompt.

1\. Verify the current repository state

The supplied ZIP is a snapshot after 2.2.2, but OpenCode will inspect the local working repository. Its plan should be based on the actual checkout, not the ZIP or prior conversation notes.

Require it to report:

- Current branch and working-tree status.
- Whether the checkout matches the expected 2.2.2 implementation.
- Any uncommitted user changes that could affect the proposed work.
- Any differences between the repository and its documentation.

This is especially important before implementation begins.

2\. Trace the actual import-to-project workflow

Require a concise call-flow description, from the FITS import operation through the point where the resulting dataset could be associated with the active project.

The report should identify actual classes and methods, not just suggest a theoretical architecture.

3\. Evaluate persistence formats against scientific round-trip requirements

Ask for a small comparison of viable approaches, considering:

| Criterion         | What to establish                                                           |
| ----------------- | --------------------------------------------------------------------------- |
| Numeric fidelity  | Can measurement values be recovered without unintended precision loss?      |
| Non-finite values | Are `NaN` and infinities preserved?                                         |
| Data types        | Are float and integer arrays reconstructed correctly?                       |
| Metadata          | Can all model metadata and validation findings be retained?                 |
| Optional data     | Are absent arrays distinguishable from empty arrays?                        |
| Complexity        | Does the approach fit the current project without unnecessary dependencies? |
| Recovery          | Can incomplete or corrupted content be identified?                          |

The recommendation should be based on the existing implementation, not a generic preference for a particular format.

4\. Identify unresolved user decisions before implementation

Require OpenCode to identify decisions that cannot safely be made from the existing requirements.

Examples include:

- Whether duplicate imports should create separate dataset identities or be recognized as the same source.
- Whether removing a dataset from a project is part of 2.2.3.
- Whether multiple datasets should be independently recoverable.
- Whether a project should still open if one dataset is corrupted.
- Whether any storage-format or schema decision requires explicit approval.

The plan should make recommendations, but it must not treat those recommendations as approved decisions.

## 4. Proposed additions to the existing prompt

I would add the following material rather than replace the existing sections.

### Additional investigation requirements for Subtask 2.2.3

#### A. Repository state and implementation baseline

Inspect the actual local repository before making recommendations.

Report:

- Current Git branch and working-tree status.
- Whether the current implementation contains the completed 2.2.1 and 2.2.2 work.
- Whether the repository matches the relevant development documentation.
- Any uncommitted user changes or discrepancies that could affect the proposed implementation.

Treat the actual repository as the implementation source of truth. Do not assume that a supplied archive, previous report, or documentation statement necessarily matches the current working tree.

#### B. Import-to-project integration path

Trace the actual application workflow from FITS import to the point where the resulting `LightCurveDataset` could become associated with the active project.

Identify:

- Where import is initiated.
- Which component receives the imported dataset.
- How the active project is identified and accessed.
- Which existing service or repository should coordinate dataset ownership and persistence.
- Whether any user-facing workflow is required for 2.2.3 or whether the work should remain limited to underlying project integration.

Identify actual classes, methods, and call paths. Do not propose a theoretical integration without first examining the existing implementation.

Keep the boundary between 2.2.3 and the later 2.3 interface work explicit.

#### C. Serialization and scientific round-trip verification

Inspect `LightCurveDataset.to_dict()` and `LightCurveDataset.from_dict()` and determine whether they are appropriate for persistent storage.

Evaluate reasonable persistence formats against:

- Floating-point precision and measurement-value preservation.
- Preservation of `NaN`, positive infinity, and negative infinity.
- Preservation of integer and floating-point array types.
- Preservation of `None` versus empty arrays.
- Preservation of uncertainties and their associations with measurements.
- Preservation of all dataset metadata, source information, and validation findings.
- Ability to reconstruct a valid dataset after application restart.
- Complexity, portability, and dependency impact.

Do not assume that successful serialization or deserialization proves scientific equivalence. The proposed test strategy must verify that a dataset survives a complete save/load round trip without unintended loss or alteration.

Do not select a storage format solely on preference. Explain the trade-offs and recommend the smallest maintainable approach that satisfies the requirements.

#### D. Save consistency and recovery strategy

If the proposed design requires multiple files or records to persist a project and its datasets, explain how the save operation remains consistent when an individual write fails.

Address:

- The order in which dataset content and project references are written.
- Temporary files and atomic replacement where appropriate.
- How incomplete writes are detected.
- How partially completed saves are handled.
- When the project may safely be marked as clean.
- How orphaned or unreferenced dataset files are handled.
- Whether one corrupted dataset can be isolated from other recoverable datasets.

Compare the proposed behavior with the existing atomic project-metadata save implementation. Do not weaken existing guarantees.

#### E. Project schema compatibility

The current project metadata implementation uses schema version 2. Determine whether the proposed dataset association can be implemented without changing that schema.

Evaluate whether a separate dataset manifest or index is appropriate.

If a project metadata schema change is proposed, explain:

- Why it is necessary.
- What existing projects would require.
- How compatibility with existing projects would be preserved.
- Why the change cannot reasonably be deferred.

Do not introduce a schema migration or version increase without identifying it as an explicit approval decision.

#### F. Dataset lifecycle boundaries

Identify which dataset operations are actually required for the 2.2.3 vertical slice.

Distinguish between:

- Importing and associating a dataset.
- Saving and recovering a dataset.
- Listing or retrieving project datasets.
- Replacing or re-importing a dataset.
- Removing a dataset association or deleting persisted content.

Do not assume that every operation is required. Identify optional operations and recommend whether they belong in 2.2.3 or should be deferred.

#### G. Minimum implementation boundary

In addition to listing likely files to change, identify:

- Files that must change.
- Files that may change depending on the approved design.
- New files that are justified.
- Existing files that should remain untouched.
- Existing interfaces that should remain unchanged.
- Functionality explicitly deferred to later subtasks.

Keep the proposed implementation focused on project integration and provisional persistence. Avoid unrelated refactoring.

#### H. Explicit approval decisions

Clearly distinguish verified facts, assumptions, recommendations, and decisions requiring user approval.

Do not treat a recommended storage format, project-dataset relationship, schema change, duplicate-import policy, or deletion policy as approved merely because it appears in the Plan report.

Stop short of implementing or committing to any consequential architectural decision that is not already authorized.

## 5. How I would structure the first planning interaction

I would use the existing PLAN prompt with the additions above. I would not yet rewrite the entire prompting document or its BUILD section.

The first planning pass should have five practical goals:

1. Verify the baseline. Confirm 2.2.1 and 2.2.2 are genuinely complete in the local repository and identify the exact interfaces available.
2. Understand project integration. Trace the actual project lifecycle and determine where datasets should belong.
3. Evaluate persistence. Compare reasonable storage approaches, especially their ability to preserve scientific values and metadata.
4. Design lifecycle safety. Establish how save, close, reopen, dirty-state, partial failures, and recovery should work.
5. Produce an implementation proposal. Identify the minimum files, tests, sequence, risks, and decisions requiring our approval.

## 6. What I want back from OpenCode

The existing A–M report structure is suitable. I would retain it, with particular attention to these deliverables:

- A verified architecture map of the existing project and dataset components.
- An import-to-project call-flow explanation.
- A recommended project-to-dataset relationship.
- A comparison and recommendation for provisional persistence.
- A concrete save-consistency and recovery strategy.
- A dirty-state integration proposal.
- A proposed test matrix, including scientific round-trip tests.
- A minimum implementation boundary and file-impact list.
- A list of decisions that require our approval.

My recommendation: Make these additions, then run the first PLAN pass. Do not decide the persistence format or project-dataset architecture in advance. Those are the central questions this planning exercise needs to answer.

Once OpenCode returns its report, we can review the technical reasoning against the actual code, identify weak assumptions, and refine the plan before authorizing any implementation.

---

# 2. Planning Phase

## Planning Version 1

### ChatGPT — OpenCode Planning Prompt #
---
PLAN — Subtask 2.2.3: Project Integration and Provisional Persistence

We are beginning planning for **Subtask 2.2.3 — Project Integration and Provisional Persistence** within Stage 2, Task 2.2 of ECAS.

You are operating in **PLAN mode only**.

Your responsibility is to inspect the existing implementation, understand the architecture, evaluate design options, identify risks, and produce a detailed implementation plan.

**Do not implement anything. Do not modify files. Do not create, delete, or overwrite files. Do not commit or push changes.**

The purpose of this first planning pass is to establish an accurate understanding of the current application and determine the smallest maintainable approach for integrating imported light-curve datasets into existing research projects with provisional persistence.


### 1. Project context

ECAS is a desktop application for exoplanetary characterization and astrochemical research.

The current development effort is building the first useful scientific vertical slice: importing a real astronomical light-curve dataset into a research project, preserving its scientific information, and making that dataset available after the project is closed and reopened.

The current task sequence is:

- **2.2.1 — FITS inspection and data-model design:** Complete.
- **2.2.2 — FITS import and validation:** Complete.
- **2.2.3 — Project integration and provisional persistence:** Pending.
- **2.2.4 — Testing, documentation, and completion verification:** Pending.

The intended initial dataset is a Kepler-10b long-cadence FITS light curve.

The scientific data model and FITS importer have already been implemented. This task must build on those implementations rather than redesigning or duplicating them.

The central success criterion for 2.2.3 is:

**A real imported light-curve dataset can be associated with a research project, saved, recovered after closing and reopening the project, and reconstructed with its scientific measurements and associated metadata intact.**

---

### 2. Required project instructions and documentation

Before making recommendations, inspect and follow:

- `AGENTS.md`
- `docs/MASTER_DEVELOPMENT_ROADMAP.md`
- `docs/development/DEVELOPMENT_LOG.md`
- Relevant project architecture and data-model documentation.
- The existing 2.2.1 and 2.2.2 overview, prompting, and working-progress documents.
- `task 2.2.n work to keep track of for documenting.md`.

The Stage 2.2 planning documents are located under:

`docs/planning/Stage 2+ work planning aka overviews and prompts/Stage 2_n_n planning/stage 2_2_n planning/`

Review the relevant 2.2.3 overview and prompting document as well.

#### Foundation documentation

The Foundation documentation is authoritative and read-only.

Read:

- `docs/Foundation/0_index.md`
- Relevant sections covering data lineage, provenance, research projects, local storage, data ownership, architecture decisions, testing, user approval, and scientific integrity.
- In particular, inspect the relevant detailed subsections associated with:
  - 4.6 — Data Lineage, Processing History and Traceability.
  - 4.7 — Data Provenance, Metadata and Source Attribution.
  - 4.9 — Local Storage and Offline Operation.
  - 6.4 — Research Projects and Workspace Integration.
  - 9.4 — Data Storage and Management Infrastructure.
  - 9.7 — Portability and Data Ownership.
  - 10.4 — Technical and Architecture Decision-Making.
  - 10.6 — Testing.
  - 10.9 — User Oversight, Approval and Communication.
  - 10.10 — Development Integrity and Accountability.
  - 11.3 — Authoritative Records and Sources of Truth.

Read the actual relevant documents and subsections rather than relying only on the index or summaries.

**Do not modify any files under `docs/Foundation/`.**

---

### 3. Verify the current repository state

Before analyzing the design, inspect the actual local repository.

Report:

- Current Git branch.
- Working-tree status.
- Whether the current checkout contains the completed 2.2.1 and 2.2.2 implementations.
- Whether the implementation agrees with the relevant development documentation.
- Any uncommitted user changes that could affect the proposed implementation.
- Any discrepancies between the repository and its documentation.

Treat the actual repository as the implementation source of truth. Do not assume that an archive, previous report, or documentation statement necessarily matches the current working tree.

Do not overwrite, discard, or modify uncommitted user work.

---

### 4. Review the existing implementation

Inspect the actual source code and tests associated with the following areas.

#### A. Light-curve data model

Review:

- `src/light_curve.py`
- `tests/test_light_curve.py`

Understand the existing `LightCurveDataset` implementation, including:

- Dataset identity.
- Dataset name.
- Original source information.
- Time metadata.
- Measurement series and measurement columns.
- Uncertainties.
- Quality flags.
- Cadence numbers.
- Validation findings.
- Import timestamp.
- Notes.
- `to_dict()` and `from_dict()`.

Determine exactly what information is already represented and what the model does not currently handle.

Do not redesign the model unless a specific integration requirement demonstrates that a change is necessary.

#### B. FITS importer

Review:

- `src/fits_importer.py`
- `tests/test_fits_importer.py`

Understand:

- The public import interface.
- How the importer identifies a suitable FITS table.
- How it extracts supported measurements.
- How it preserves SAP and PDCSAP measurements separately.
- How it handles uncertainties.
- How it preserves time metadata.
- How it handles quality flags and cadence numbers.
- How it records validation findings.
- How it handles missing and non-finite values.
- How source information is recorded.

Identify any limitations relevant to project integration.

Do not redesign or duplicate the importer.

#### C. Project architecture

Review:

- `src/project_model.py`
- `src/project_repository.py`
- `src/project_service.py`
- `src/main_window.py`
- Other directly relevant project and GUI modules.
- Associated project and lifecycle tests.

Understand the actual implementation of:

- Project metadata.
- Project identity.
- Project directory structure.
- Project creation.
- Project opening.
- Project saving.
- Project closing.
- Active-project management.
- Project discovery.
- Dirty-state tracking.
- Save, Discard, and Cancel behavior.
- Existing persistence and atomic-write patterns.
- Custom project locations, if supported.

Identify where the light-curve dataset should logically integrate with this architecture.

Do not assume the main window should own scientific data or that project metadata should contain the measurements.

---

### 5. Repository and import-to-project integration path

Trace the actual workflow from FITS import to the point where the resulting `LightCurveDataset` could become associated with the active project.

Identify:

- Where FITS import is initiated.
- Which component receives the imported dataset.
- How the active project is identified and accessed.
- Which existing service or repository should coordinate dataset ownership and persistence.
- Where a project-level dataset collection or registry would logically belong.
- Whether a user-facing import workflow is required for 2.2.3 or whether this task should remain limited to the underlying project integration.

Identify actual classes, methods, and call paths.

Do not propose a theoretical architecture without examining the existing implementation first.

Keep the boundary between 2.2.3 and later interface work explicit. In particular, do not expand this task into the table interface or visualization work planned for 2.3.

---

### 6. Dataset association and project ownership

Determine the most appropriate way to associate one or more `LightCurveDataset` objects with an existing research project.

Evaluate:

- How dataset identity should be maintained.
- Whether datasets should be individually identifiable within a project.
- How the original source filename and path should be retained.
- How provenance and scientific metadata should remain associated with the correct measurements.
- Whether multiple datasets should be supported within one project.
- Whether a dataset can be associated with more than one project, or whether project ownership should be exclusive.
- How project switching and closing should affect datasets.
- How dataset references should be stored without placing large scientific arrays directly into project metadata.

Consider the existing project architecture and the dataset model's existing identity fields.

Recommend the smallest maintainable design.

Do not introduce unnecessary abstractions or a broad project-system redesign.

---

### 7. Provisional persistence design

The project needs to save and recover imported light-curve datasets.

However, the permanent storage architecture has deliberately been deferred.

The current development roadmap permits a provisional local-file approach for the first scientific vertical slice, provided its limitations are documented and original data is preserved.

**Do not treat this task as approval to establish the permanent ECAS storage architecture or finalize the deferred D6 decision.**

Investigate reasonable persistence approaches and recommend one based on the actual implementation.

Evaluate:

- Where persisted dataset content should live.
- How dataset identity and project association should be represented.
- How dataset metadata and scientific arrays should be stored.
- How the application should locate persisted datasets when reopening a project.
- How the design handles multiple datasets.
- How the design supports future migration to a more permanent storage architecture.
- Whether any new dependencies are actually necessary.

Do not assume a particular file format or database is already approved.

#### Serialization and scientific round-trip verification

Inspect `LightCurveDataset.to_dict()` and `LightCurveDataset.from_dict()`.

Determine whether they are appropriate for persistent storage.

Evaluate candidate approaches against:

- Floating-point precision and measurement-value preservation.
- Preservation of `NaN`, positive infinity, and negative infinity.
- Preservation of integer and floating-point array types.
- Preservation of `None` versus empty arrays.
- Preservation of uncertainties and their associations with measurements.
- Preservation of all dataset metadata, source information, and validation findings.
- Ability to reconstruct a valid dataset after application restart.
- Complexity, portability, and dependency impact.

The model intentionally preserves non-finite scientific values. Account for the fact that standard JSON does not formally support NaN or infinity, even though Python's default JSON implementation permits non-standard representations.

Do not assume successful serialization or deserialization proves scientific equivalence.

The proposed test strategy must verify that a dataset survives a complete save/load round trip without unintended loss or alteration.

Provide a comparison of reasonable formats and explain the trade-offs. Do not select a format solely on preference.

---

### 8. Save consistency, atomicity, and recovery

If the proposed design requires multiple files or records to persist a project and its datasets, explain how the save operation remains consistent when an individual write fails.

For example, consider a project with three datasets where the first two save successfully but the third fails.

Address:

- The order in which dataset content and project references are written.
- Temporary files and atomic replacement where appropriate.
- How incomplete writes are detected.
- How partially completed saves are handled.
- When the project may safely be marked as clean.
- How orphaned or unreferenced dataset files are handled.
- Whether one corrupted dataset can be isolated from other recoverable datasets.
- Whether existing project metadata remains valid if dataset persistence fails.

Compare the proposed behavior with the existing atomic project-metadata save implementation.

Do not weaken existing guarantees.

The application must not report a successful save or clear the dirty state when required scientific data has not been saved successfully.

---

### 9. Original source-file availability

Keep three separate concepts distinct:

1. The original FITS file on disk.
2. The imported `LightCurveDataset` held by the application.
3. The persisted representation of that dataset inside the project.

The original FITS file may become unavailable after import.

Determine whether the project can still reopen and recover its persisted dataset when the original source file has been moved, renamed, or deleted.

Retain the original source path and provenance information.

Verify what the current importer actually does. Recording a source path is not equivalent to copying or preserving the original file.

Do not modify or overwrite the original FITS file.

The persisted representation must be distinguishable from the original source and from any future derived data.

---

### 10. Project dirty-state and lifecycle integration

Determine how dataset changes should interact with the existing project dirty-state mechanism.

Distinguish between:

- Project metadata changes.
- Dataset additions.
- Dataset content changes.
- Dataset removal or association changes, if included in scope.
- Successful metadata saves.
- Successful dataset saves.

Trace the actual save and close call paths before recommending a solution.

Address:

- Importing a dataset into an active project.
- Saving the project.
- Closing the project.
- Reopening the project.
- Recovering datasets.
- Switching between projects.
- Handling unsaved dataset changes.
- Handling missing or corrupted persisted datasets.
- Handling failed persistence operations.

Preserve the existing Save, Discard, and Cancel behavior.

Do not introduce a broad rewrite of the project lifecycle merely to support datasets.

The plan must explain how a project can avoid being incorrectly marked as clean when its scientific data has not been persisted.

---

### 11. Project schema compatibility

The existing project metadata implementation currently uses schema version 2.

Determine whether dataset association can be implemented without changing that schema.

Evaluate whether a separate dataset manifest or index is appropriate.

If a project metadata schema change is proposed, explain:

- Why it is necessary.
- What existing projects would require.
- How compatibility with existing projects would be preserved.
- Why the change cannot reasonably be deferred.

Prefer avoiding an unnecessary schema change, but base the recommendation on the inspected architecture.

Do not introduce a schema migration or version increase without identifying it as an explicit decision requiring approval.

---

### 12. Dataset lifecycle boundaries

Identify which dataset operations are actually required for the 2.2.3 vertical slice.

Distinguish between:

- Importing and associating a dataset.
- Saving and recovering a dataset.
- Listing or retrieving project datasets.
- Replacing or re-importing a dataset.
- Removing a dataset association.
- Deleting persisted dataset content.

Do not assume that every operation is required.

Identify optional operations and recommend whether they belong in 2.2.3 or should be deferred.

In particular, distinguish removing a dataset from a project from permanently deleting its stored scientific data.

---

### 13. Scientific integrity requirements

The following requirements are non-negotiable.

The implementation must preserve:

- Original imported scientific measurements.
- SAP_FLUX and PDCSAP_FLUX as distinct measurement series.
- Associated uncertainties.
- Original time values and time metadata.
- Quality flags.
- Cadence numbers.
- Source information.
- Units.
- Validation findings.
- Missing values.
- Non-finite values.

The implementation must not automatically:

- Normalize measurements.
- Detrend measurements.
- Filter observations.
- Remove nonzero quality flags.
- Discard NaN or infinite values.
- Convert time values.
- Convert measurement units.
- Modify the original FITS file.
- Replace original measurements with derived values.

Do not introduce assumptions when metadata is unknown or unavailable.

Original measurements and any future derived measurements must remain distinguishable.

---

### 14. Testing strategy

Review the existing tests and propose the tests needed for 2.2.3.

The proposed test strategy should cover:

#### Dataset association

- Associating a dataset with the correct project.
- Maintaining dataset identity.
- Supporting multiple datasets where appropriate.
- Retrieving the correct dataset from the correct project.
- Preventing accidental cross-project contamination.

#### Persistence

- Saving a dataset.
- Loading a saved dataset.
- Reopening a project and recovering its datasets.
- Preserving all measurements and metadata.
- Preserving uncertainties, flags, and cadence numbers.
- Preserving missing and non-finite values.
- Preserving optional fields and array types.
- Verifying scientific round-trip equivalence.

#### Failure and recovery

- Missing original FITS source file.
- Missing persisted dataset content.
- Corrupted persisted content.
- Incomplete writes.
- Failed dataset saves.
- Failed project saves.
- Invalid dataset references.
- Unsupported or outdated data-model versions.
- One corrupted dataset alongside other valid datasets.

#### Project lifecycle

- Creating a project and importing a dataset.
- Saving and closing.
- Reopening and recovering.
- Switching projects.
- Unsaved dataset changes.
- Save, Discard, and Cancel behavior.
- Dirty-state correctness after successful and failed saves.

Use temporary project directories and controlled test datasets.

Do not use mock data in the actual application workflow. Synthetic fixtures are acceptable for isolated automated tests.

Do not weaken, remove, or bypass existing tests to make implementation easier.

Identify which tests can run without a GUI and which require a GUI environment.

Do not prioritize investigating or eliminating the existing automated-test popup behavior during this subtask unless it directly prevents required verification. That broader issue is deferred to the later 2.2.n review.

---

### 15. Documentation impact

Identify which documentation should be updated during 2.2.3 and which should be deferred to 2.2.4.

Consider:

- `docs/MASTER_DEVELOPMENT_ROADMAP.md`
- `docs/development/DEVELOPMENT_LOG.md`
- Architecture documentation.
- Data-model documentation.
- Data-flow documentation.
- Module responsibilities.
- Storage and persistence documentation.
- Testing and validation documentation.
- Project state and decision records.
- `task 2.2.n work to keep track of for documenting.md`.

The running implementation record must capture verified details, including:

- Actual implementation decisions.
- Files changed.
- New files or dependencies.
- Actual behavior.
- Test results.
- Deviations from the approved plan.
- Limitations.
- Deferred work.

Do not invent implementation results during planning.

Do not modify Foundation documentation.

---

### 16. Minimum implementation boundary

Identify:

- Files that must change.
- Files that may change depending on the selected design.
- New files that are justified.
- Existing files that should remain untouched.
- Existing interfaces that should remain unchanged.
- Functionality explicitly deferred to later subtasks.

Keep the proposed implementation focused on project integration and provisional persistence.

Avoid unrelated refactoring.

Do not expand the task into:

- Light-curve table UI or visualization (2.3).
- Transit detection or BLS analysis (2.4).
- Analysis operation records (2.5).
- Permanent storage architecture redesign.
- Archive download integration planned for Stage 4.

---

### 17. Required planning report

Return a structured report with the following sections.

**A. Repository state and verification**

- Branch and working-tree status.
- Verified 2.2.1 and 2.2.2 implementation state.
- Discrepancies or uncommitted changes.

**B. Existing architecture**

- Relevant models, services, repositories, and GUI components.
- Their actual responsibilities.
- Current project lifecycle and persistence behavior.

**C. Import-to-project workflow**

- Actual call path.
- Current integration gap.
- Recommended integration point.

**D. Dataset association**

- Recommended ownership and identity model.
- Multiple-dataset support.
- Project-to-dataset relationship.

**E. Persistence alternatives**

- Reasonable approaches considered.
- Comparison of trade-offs.
- Recommended provisional approach.
- Scientific round-trip considerations.

**F. Save consistency and recovery**

- Proposed save sequence.
- Atomicity and partial-failure behavior.
- Corruption and recovery strategy.

**G. Source-file handling**

- Original FITS availability.
- Persisted dataset independence.
- Provenance retention.

**H. Project lifecycle and dirty state**

- Import, save, close, reopen, and switching behavior.
- Save, Discard, and Cancel integration.
- Dirty-state strategy.

**I. Project schema compatibility**

- Whether schema version 2 can remain unchanged.
- Whether a separate manifest or index is appropriate.
- Any required migration and justification.

**J. Testing plan**

- Specific test cases.
- Existing tests to extend.
- New test files, if necessary.
- GUI versus non-GUI verification.

**K. Documentation impact**

- Files requiring updates.
- Information to record now versus consolidate in 2.2.4.

**L. Implementation sequence and scope**

- Recommended implementation phases.
- Files likely to change.
- Dependencies between phases.
- Explicitly deferred work.

**M. Risks, assumptions, and approval decisions**

- Technical risks.
- Unverified assumptions.
- Recommended decisions.
- Decisions requiring explicit user approval.

For every important conclusion, distinguish between:

- **Verified fact:** Directly established from source code, tests, or authoritative documentation.
- **Assumption:** Not yet established.
- **Recommendation:** Your proposed approach.
- **Approval required:** A consequential decision that must be approved before implementation.

Reference actual files, classes, methods, and tests wherever possible.

---

### 18. Planning boundaries and final instructions

This is an investigation and planning exercise only.

Do not:
- Modify source code.
- Modify tests.
- Modify documentation.
- Create implementation files.
- Run commands that alter the repository.
- Install dependencies.
- Commit or push changes.
- Make permanent architectural decisions on the user's behalf.
- Treat recommendations as approved decisions.

Read-only inspection and non-destructive testing or analysis may be performed when useful. Clearly report any commands that were run and their effects.

If an important requirement is ambiguous, identify it in the report rather than silently choosing an interpretation.

The goal is a practical, technically justified implementation plan that fits the existing ECAS architecture and the intended scope of 2.2.3.

**Stop after presenting the planning report. Wait for review and explicit approval before making any changes or beginning implementation.**

---


# OpenCode — Planning Response (Version 1)

All 233 non-GUI tests pass. I now have a complete, verified picture of the repository. Here is my planning report for Subtask 2.2.3.
 PLAN REPORT — Subtask 2.2.3: Project Integration and Provisional Persistence

**Mode:** PLAN ONLY. No files were modified, created, or deleted. Only read-only inspection and a read-only test execution were performed.

## A. Repository state and verification

**Verified facts:**
- Current Git branch: `master`. Last commit: `3cbe6f5 subtask 2.2.2 done`.
- Working tree is clean of source changes; there are 7 modified `WORKING PROGRESS LOG.md` files under `docs/planning/...` (pre-existing user changes — I have not touched them).
- 2.2.1 and 2.2.2 implementations are present and complete:
  - `src/light_curve.py` — `LightCurveDataset` model with `to_dict()`/`from_dict()`.
  - `src/fits_importer.py` — `import_light_curve(file_path) -> LightCurveDataset`.
  - `tests/test_light_curve.py` (48 tests) and `tests/test_fits_importer.py` (60 tests).
- Project lifecycle (Task 2.1) is complete: `src/project_model.py`, `src/project_repository.py`, `src/project_service.py`, `src/main_window.py`, `src/main.py`, `src/config_provider.py`.
- Project metadata schema version is **2** (`SCHEMA_VERSION = 2` in `project_model.py`), with `owner`/`roles` fields (DEC-003/D4, implemented 2026-11-04).
- Read-only test execution: `python -m pytest tests/test_light_curve.py tests/test_fits_importer.py tests/test_project_model.py tests/test_project_repository.py tests/test_project_service.py tests/test_project_discovery.py tests/test_project_status.py -q` → **233 passed, 0 failed** (Python 3.13.9, `.venv`). This matches the development log.
- GUI test files (`test_new_project_dialog.py`, `test_project_save_close.py`) hang in this headless environment due to PySide6 display/QPA requirements — a pre-existing limitation documented in the dev log; not part of this task.

**Assumptions:** None needed for the baseline; state was verified directly from code and test execution.

**Discrepancies:** None between repository and documentation for the areas inspected. The working tree's modified working-progress logs are user-held notes, not source changes.

---

## B. Existing architecture

**Verified facts from source inspection:**

| Module | Class | Responsibility |
|---|---|---|
| `src/project_model.py` | `ProjectMetadata` | Project metadata: `project_id` (UUID), `name`, `created_at`, `status`, `schema_version=2`, `external_data_references: list`, `owner`, `roles`, `is_dirty`. Validation, `set_name()`, `set_status()`, `to_dict()`/`from_dict()`, v1→v2 in-memory migration. Dirty-state via `mark_dirty()`/`mark_clean()`; only `set_name()`/`set_status()` mark dirty. |
| `src/project_repository.py` | `ProjectRepository` | JSON persistence: one `project.json` per project directory named by `project_id`. Atomic writes (temp file + `os.replace` + `fsync`). `load`, `save`, `load_from_directory`, `discover_projects`, `list_projects`. Error classes: `ProjectNotFoundError`, `ProjectCorruptedError`, `ProjectRepositoryError`. |
| `src/project_service.py` | `ProjectService` | Lifecycle orchestration: `create_project`, `open_project`, `open_project_from_path`, `save_project`, `close_project`, `discover_projects`, `change_status`, `set_active_project`. Tracks `_active_project` and `_active_location` (runtime only). Repository selection for save prefers injected default repo when roots match. |
| `src/main_window.py` | `MainWindow` | PySide6 shell: Project > New/Save/Close/Open, Status submenu, dirty asterisk indicator, Save/Discard/Cancel prompts on close/switch, menu state gated by dirty state. |
| `src/light_curve.py` | `LightCurveDataset` | Scientific dataset: `dataset_id` (UUID), `name`, `source` (DatasetSource: filename, path, archive, source_id, mission, instrument, target, checksum), `time` (TimeInfo), `measurements` (MeasurementSeries of MeasurementColumn: values, unit, uncertainties, description), `quality_flags`, `cadence_numbers`, `validation` (ValidationReport), `imported_at`, `notes`. Arrays copied on construction; `to_dict()`→lists, `from_dict()` reconstructs and validates. |
| `src/fits_importer.py` | `import_light_curve` | Reads FITS read-only, structural HDU identification, extracts TIME/SAP_FLUX/PDCSAP_FLUX + uncertainties/quality/cadence, records validation findings, builds `LightCurveDataset`. Records `original_filename`/`original_file_path` in `DatasetSource`. Never modifies the FITS file. No project or GUI imports. |
| `src/main.py` | `main()` | Wires `ConfigProvider` → `ProjectRepository` → `ProjectService` → `MainWindow`. |

**Current project lifecycle and persistence behavior (verified):**
- Project metadata is saved atomically to `<projects_root>/<project_id>/project.json`.
- `save_project()` marks metadata clean only on success; failure preserves dirty state and the active project.
- `close_project()` clears the active project; the caller (MainWindow) handles Save/Discard/Cancel before closing.
- Dirty state reflects metadata changes only (name, status). There is **no** concept of dataset changes in dirty state today.
- Save disabled when no project or clean; close disabled when no project.
- No import menu/action exists anywhere in the GUI. `import_light_curve` is a standalone library function with no project awareness.

---

## C. Import-to-project workflow

**Verified facts:**
- `import_light_curve(file_path)` returns a standalone `LightCurveDataset`. Nothing in the current codebase receives it or associates it with a project.
- `MainWindow` has no import action. The active project is held by `ProjectService._active_project` and exposed via `active_project` property; `MainWindow` accesses it through `self._service`.

**Current integration gap (verified):**
- No project-level dataset collection or registry exists.
- No mechanism to persist measurement arrays or recover them on reopen.
- `ProjectMetadata.external_data_references` (a plain `list`, already serialized) is the only existing project field that could carry lightweight dataset references; it currently holds nothing dataset-specific.

**Recommended integration point (recommendation):**
- `ProjectService` should own the active dataset collection (runtime `dict[str, LightCurveDataset]` keyed by `dataset_id`) and coordinate dataset persistence via `ProjectRepository` for project metadata plus a dataset-file persistence layer for the scientific content. `MainWindow` would later (2.3+) add an import action calling service methods. For 2.2.3 the integration is service-level and testable without a GUI.

---

## D. Dataset association

**Recommended ownership and identity model (recommendation):**
- **Dataset identity:** Reuse `LightCurveDataset.dataset_id` (UUID, already generated and serialized) as the stable, project-scoped dataset identity. No change to the data model.
- **Project-to-dataset relationship:** Exclusive ownership within a project for the vertical slice. A dataset belongs to one project; associating the same imported dataset with multiple projects is deferred (not required for 2.2.3). Foundation §6.4.3 (shared data across projects) and §4.6.6 (independent processing of shared data) describe future sharing; exclusive ownership is the simplest starting point and does not conflict with them.
- **Multiple datasets:** Supported. A project can hold multiple datasets, each individually identifiable by `dataset_id` and name.
- **Dataset references in project metadata:** Store lightweight references in the existing `ProjectMetadata.external_data_references` list as dicts:
  ```json
  {"kind": "light_curve_dataset", "dataset_id": "<uuid>", "name": "<dataset name>",
   "dataset_file": "datasets/<dataset_id>.json", "source": {...summary...}, "imported_at": "..."}
  ```
  This avoids a schema change: `external_data_references` is already a `list` field with no enforced element schema, and `to_dict()`/`from_dict()` round-trips it unchanged.
- **Scientific content separate from metadata:** Measurement arrays live in per-dataset files (`<project_dir>/datasets/<dataset_id>.json`), never inside `project.json`. This preserves the separation between project metadata and scientific data, consistent with Foundation §9.4.2 (large scientific files separate from structured records) and the existing `external_data_references` design.
- **Original source retention:** `DatasetSource.original_file_path` and `original_filename` are serialized into each dataset file, so provenance survives source-file moves/deletions.
- **Project switching/closing:** Datasets are runtime state of the active project only. Closing clears the active project (and its in-memory datasets); persisted datasets are recovered on reopen. Switching projects does not transfer datasets (exclusive ownership).

**Assumptions:** Dataset content changes after association (e.g., user edits values) are out of scope for 2.2.3; only association/dirty-state on *addition* is required. No removal or re-import UI is required for the slice (see §L).

---

## E. Persistence alternatives

**Reasonable approaches considered (comparison):**

| Criterion | (1) Per-dataset JSON files in project dir + refs in external_data_references | (2) One collective JSON for all datasets | (3) NumPy .npy/.npz sidecars + JSON metadata | (4) SQLite in project dir |
|---|---|---|---|---|
| Reuses existing code | Yes (`to_dict`/`from_dict`, atomic-write pattern) | Yes | Partial | No |
| New dependencies | No | No | No | sqlite3 is stdlib, but new query layer |
| Human-portable/inspectable | Yes | Yes | Partial (binary arrays) | No |
| NaN/Inf handling | Python json writes `NaN`/`Infinity`/`-Infinity` (non-standard RFC 8259, but round-trips exactly in Python's `json`) | Same | Native, robust | Native |
| Float64 precision | Exact via `float.__repr__` shortest round-trip | Same | Exact | Exact |
| None vs empty array distinguished | Yes (null vs []) | Yes | Needs convention | Yes |
| Multiple datasets | Natural (one file each) | Awkward (single blob) | Natural | Natural |
| Partial-failure isolation | Good (per-file atomic writes) | Poor (one file = all or nothing) | Good | Transactional |
| Migration path to permanent D6 | Straightforward (files are independent dataset records) | Straightforward | Straightforward | Requires DB migration |

**Recommended provisional approach (recommendation):** Option 1 — one JSON file per dataset at `<project_dir>/datasets/<dataset_id>.json`, serialized via `LightCurveDataset.to_dict()`/`from_dict()`, with project metadata holding lightweight references in `external_data_references`. This is the smallest maintainable approach, requires zero new dependencies, reuses the existing serialization and atomic-write patterns, and cleanly separates concerns.

**Scientific round-trip considerations (recommendation + caveat requiring approval):**
- Float64 measurement values: `tolist()` → JSON decimal → `float()` round-trips exactly (Python uses shortest repr that round-trips). ✅ Verified property of Python's json; safe for scientific preservation.
- `NaN`, `+Infinity`, `-Infinity`: Python's `json.dump` (default `allow_nan=True`) emits the non-standard literals `NaN`, `Infinity`, `-Infinity`. Python's `json.load` reads them back exactly. **This is NOT valid strict JSON (RFC 8259).** It round-trips perfectly within Python, but a strict JSON parser or external tool would reject the file. For a provisional local-file slice this is acceptable and must be documented as a known limitation. Using `allow_nan=False` would raise on non-finite values — unacceptable since preserving NaN/Inf is non-negotiable (§13).
- Integer arrays: `tolist()` → Python ints; `from_dict` reconstructs with explicit `dtype=np.int64` (quality/cadence) and `np.float64` (time/measurements/uncertainties), so types are preserved. None vs empty arrays distinguished by `is None` checks in `from_dict`.
- Uncertainties: `None` ↔ absent column preserved; zero arrays ↔ None distinguished.
- All metadata/source/validation fields are strings or primitives, fully round-tripped.
- `from_dict` re-runs structural validation (`LightCurveValidationError`), so corrupted/truncated files are detectable on load.
- **Scientific equivalence is not proven by successful deserialization** — the test strategy must assert value-level equality (including NaN positions, inf signs, dtype kinds) after round-trip.

**Decision requiring user approval:** Adopting per-dataset JSON with Python's default JSON (non-standard NaN/Infinity literals) as the provisional persistence format. This touches data storage (D6 deferred; §10.4.2 lists "major changes to data storage, persistence or project structures" as requiring approval). I recommend it but it is not approved.

---

## F. Save consistency and recovery

**Proposed save sequence (recommendation):**
1. Require an active project; otherwise error (no silent no-op).
2. For each dataset in the active project's collection: serialize and atomically write `<project_dir>/datasets/<dataset_id>.json` (temp file + `os.replace`, same directory, matching the existing `_write_json_atomic` pattern).
3. Only after **all** dataset files succeed: update `external_data_references` in `ProjectMetadata` and atomically save `project.json`.
4. Mark the project clean **only** after both dataset files and project metadata are saved successfully.

**Partial-failure behavior (example: 3 datasets, third fails):**
- Datasets 1 and 2 are written; dataset 3 write raises. Abort **before** touching `project.json`. Project metadata remains the previous valid version (atomic). Project stays **dirty**; user is not told the save succeeded. Error surfaced via existing UI error conventions (QMessageBox.critical, as in `_on_save_project`).
- The newly written dataset files for datasets 1 and 2 are unreferenced orphans until a successful save. On a subsequent successful save, remove any `datasets/*.json` whose `dataset_id` is not in the current reference set (orphan cleanup), keeping the project directory consistent. Orphan cleanup is best-effort and never removes referenced files.

**Incomplete-write detection:** Atomic temp+replace means `project.json` and each dataset file are either fully the previous valid version or fully the new version — never partially written. On load, `json.load` failure → `ProjectCorruptedError`; `from_dict` validation failure → treated as corrupted dataset.

**Corruption and recovery strategy:**
- Loading a project: load `project.json` first. If that fails → `ProjectOpeningError` (project cannot open; matches existing behavior).
- For each dataset reference: attempt to load and reconstruct the dataset file. If **one** dataset file is missing or corrupted: isolate it — skip that dataset, record a recoverable error, continue loading the project and the other datasets. Surface a clear message identifying which dataset failed. One bad dataset must not invalidate the whole project (Foundation §4.6.8, §9.4.6; task §8).
- Missing original FITS file after import: not a recovery blocker. The dataset file is self-contained; `original_file_path` is retained as provenance only. The project reopens and recovers the dataset without the original file (task §9).
- The application must **not** report a successful save or clear the dirty state when any required dataset failed to persist. ✅ Enforced by the sequence above.

**Comparison with existing atomic metadata save:** The proposed design extends the existing atomic-write pattern to dataset files and adds an ordering rule (datasets before metadata, clean only after all succeed). It does not weaken `project.json`'s existing guarantees.

---

## G. Source-file handling

**Verified facts:**
- `_build_source_metadata` in `fits_importer.py` sets `original_filename=path.name` and `original_file_path=str(path)`; opens the file `mode="readonly"` and never writes, moves, or copies it.
- The importer records a path reference only; it does not preserve the original file contents.

**Three concepts kept distinct (recommendation):**
1. Original FITS file on disk — untouched, may become unavailable after import.
2. Imported `LightCurveDataset` in memory.
3. Persisted dataset representation (`datasets/<dataset_id>.json`) inside the project — self-contained, independent of #1.

**Provenance retention:** `original_file_path`, `original_filename`, plus `mission`/`instrument`/`target_object`/`source_id` from the FITS headers are serialized into the dataset file. The persisted representation is distinguishable from the original source (different path, JSON format, application-owned) and from future derived data (no derivation is performed in 2.2.3; derived-data relationships belong to 2.4/2.5 per Foundation §4.6).

**Recovery without original file:** Yes — reopening loads the dataset JSON; the missing original file does not prevent dataset recovery. A warning/info indication that the source file is no longer available is appropriate UI-level feedback (deferred to GUI work).

---

## H. Project lifecycle and dirty state

**Dirty-state strategy (recommendation):**
- Dataset **association** into an active project → `ProjectMetadata.mark_dirty()`. (New trigger; currently only name/status changes mark dirty. This is a minimal, scoped extension of the existing mechanism.)
- Successful project save (metadata + all datasets) → `mark_clean()`.
- Failed save → dirty preserved, active project preserved (existing behavior).
- Import + save + close + reopen: dataset persists in `datasets/`, reference in `external_data_references`, recovered on `open_project`, project loads clean.
- Switching projects: existing `_prompt_save_before_switch()` already handles dirty metadata; dataset addition now contributes to dirty, so the prompt fires correctly. No lifecycle rewrite needed.
- Save/Discard/Cancel: preserved unchanged.

**Call paths to integrate (recommendation):**
- `ProjectService.associate_dataset(dataset)` (or `add_dataset`): appends to runtime collection, marks dirty.
- `ProjectService.save_project()`: extended to persist datasets before metadata (as in §F).
- `ProjectService.open_project()` / `open_project_from_path()`: extended to load referenced dataset files after metadata load.
- `ProjectService.close_project()`: unchanged (clears runtime state; datasets are recoverable from disk).

**Scope note:** A user-facing import workflow (menu item, file dialog) is **not** part of 2.2.3. The integration is at the service layer, driven by tests and later by a GUI import action (2.3+). This keeps the boundary with 2.3 interface work explicit.

---

## I. Project schema compatibility

**Verified fact:** Project metadata schema version is 2 and `ProjectMetadata.to_dict()`/`from_dict()` serialize `external_data_references` as-is (a `list`).

**Recommendation:** Schema version 2 can remain unchanged. Dataset references use the existing `external_data_references` list field; no new fields, no version bump, no migration. A separate manifest file is not necessary — the per-dataset files plus references in `external_data_references` constitute the index.

**Approval note:** If the user prefers a dedicated field (e.g., `datasets`) on `ProjectMetadata`, that would require a schema change to version 3 — an explicit approval decision under §10.4.2. I recommend avoiding it.

---

## J. Testing plan

**Tests that run without a GUI (pytest, tmp_path; verified runnable):**

New test module `tests/test_dataset_repository.py` (recommended):
- Save a dataset to a project directory; load it back; value-level equality for time, SAP_FLUX, PDCSAP_FLUX, uncertainties, quality_flags, cadence_numbers.
- Round-trip preserves `NaN`, `+Inf`, `-Inf` (positions and signs), float64 precision, int64 types.
- `None` uncertainties vs zero-valued uncertainties distinguished; empty vs None arrays distinguished.
- All source/provenance fields and validation findings preserved.
- Multiple datasets in one project; each recoverable by `dataset_id`; no cross-project contamination (separate project dirs).
- Missing dataset file → recoverable error, other datasets load, project still opens.
- Corrupted dataset JSON (truncated/invalid) → isolated failure, other datasets load.
- Unsupported dataset schema/structure (from_dict validation) → isolated failure.
- Atomic write: interrupted/failing write leaves no corrupted file (simulate by monkeypatching or read-only dir).
- Orphan cleanup: unreferenced dataset files removed on successful save.

New/extended service-level tests (extend `tests/test_project_service.py` or new module):
- Associate dataset with active project; `is_dirty` becomes True.
- Save persists dataset file + reference; project clean after success.
- Reopen (`open_project`) recovers dataset with all measurements/metadata.
- Save failure (e.g., read-only project dir) leaves project dirty and active; `project.json` unchanged.
- `list_datasets()`/`get_dataset()` return correct dataset per project.
- Two separate service instances/projects do not leak datasets.

Existing tests to extend/regression:
- `tests/test_project_model.py` — unchanged (schema v2 untouched).
- `tests/test_project_save_close.py` — dirty-state Save/Discard/Cancel behavior still valid; add case where dataset addition makes save enabled.
- Run full non-GUI suite as regression.

**GUI vs non-GUI:** All proposed tests are non-GUI. GUI integration (an import menu action) requires a display and is deferred; GUI test execution limitation is pre-existing and deferred to 2.2.n review per the task.

**Fixtures:** Synthetic `LightCurveDataset` objects built with NumPy arrays (including NaN/Inf) under `tmp_path`. Do not depend on the user's real Kepler-10b path (it may not even be present; per dev log it was never independently imported).

---

## K. Documentation impact

**To update during 2.2.3 (Build mode):**
- `docs/MASTER_DEVELOPMENT_ROADMAP.md` — mark Task 2.2.3 Complete; status reflects verified progress. (Authoritative source for development status per §11.3.3.)
- `docs/development/DEVELOPMENT_LOG.md` — record implementation: files changed, new files, decisions, test results, limitations, deferred work (per §10.11, §11.3).
- `docs/planning/.../task 2.2.n work to keep track of for documenting.md` — update the running 2.2 record with verified 2.2.3 details (files, behavior, decisions).
- Document the provisional persistence approach and its limitations (non-standard JSON NaN/Infinity literals, D6 deferred) so they are not mistaken for permanent architecture.

**Defer to 2.2.4:** Broader architecture/data-model documentation consolidation, data-flow docs, and final documentation reconciliation — per the existing plan, 2.2.4 owns the consolidated documentation pass.

**Do not modify:** `docs/Foundation/` (read-only). No decision records need creation unless an approval decision (format, schema) is taken — then a decision record under `docs/development/decisions/` would be appropriate (§10.9.5).

---

## L. Implementation sequence and scope

**Recommended phases:**

| Phase | Objective | Likely modules | Tests | Depends on |
|---|---|---|---|---|
| 1 | Dataset file persistence: save/load one `LightCurveDataset` as JSON in `<project>/datasets/<id>.json`, atomic writes, validation on load | New module (e.g. `src/dataset_repository.py`) or repository extension | `test_dataset_repository.py` round-trip, NaN/Inf, types, corruption, atomicity | Approval of format (E) |
| 2 | ProjectService dataset association: add/get/list datasets, dirty marking, integrate dataset save into `save_project()`, dataset load into `open_project()` | `src/project_service.py` | `test_project_service.py` association, dirty, save/recover, failure, multiple datasets | Phase 1 |
| 3 | Serialization round-trip verification & edge cases (None vs empty, dtype preservation, orphan cleanup, missing source file) | Phase 1 + 2 code | Edge-case tests in Phase 1/2 modules | Phase 1–2 |
| 4 | Documentation updates (roadmap, log, tracking file) | docs only | n/a | Implementation complete |

**Files likely to change:**
- `src/project_service.py` (extend: dataset collection + save/load integration)
- New: `src/dataset_repository.py` (or equivalent) — dataset file persistence
- Possibly `src/project_repository.py` (helper for dataset dir paths) — may change depending on design
- Tests: new `tests/test_dataset_repository.py`; extend `tests/test_project_service.py`
- Docs: roadmap, dev log, tracking file

**Files that should remain untouched:**
- `src/light_curve.py`, `src/fits_importer.py` (do not redesign or duplicate 2.2.1/2.2.2)
- `src/project_model.py` (no schema change recommended)
- `src/main_window.py` (no GUI import workflow in 2.2.3)
- `docs/Foundation/*` (read-only)

**Functionality explicitly deferred:**
- User-facing import menu/workflow (GUI; 2.3+ boundary)
- Dataset removal, replacement, re-import, deletion of persisted content
- Permanent storage architecture (D6 remains deferred)
- Table UI, visualization (2.3), BLS/transit analysis (2.4), operation records (2.5), archive integration (Stage 4)

---

## M. Risks, assumptions, and approval decisions

**Technical risks:**
- Non-standard JSON (NaN/Infinity literals) — round-trips in Python but rejected by strict JSON parsers. Mitigation: document limitation; acceptable for provisional slice.
- Orphan dataset files after partial saves — mitigated by best-effort cleanup on successful save.
- Dataset load failure isolation — must be implemented carefully so one bad dataset doesn't block project open.
- No UI import path in 2.2.3 means end-to-end user verification requires GUI work later; service-level tests cover the logic.

**Unverified assumptions:**
- That storing dataset references in `external_data_references` (a generic list) is acceptable semantically — no schema enforcement exists today, but it's a repurposing of the field.
- That the real Kepler-10b file may not be available in this environment; tests use synthetic fixtures (per existing convention).

**Recommended decisions (for user approval):**
1. **Provisional persistence format:** per-dataset JSON files using `LightCurveDataset.to_dict()`/`from_dict()` with Python's default JSON (non-standard NaN/Infinity literals), one file per dataset in `<project_dir>/datasets/`. (Requires approval — data storage decision, §10.4.2, D6 deferred.)
2. **Dataset references stored in existing `external_data_references` list without schema change.** (Minor; flagging for awareness.)
3. **No GUI import workflow in 2.2.3** — service-level integration only; tests drive it.
4. **Dataset association marks project dirty** — scoped extension of existing dirty-state mechanism.

**Decisions requiring explicit user approval before implementation:** #1 above (and any decision to instead change the schema version or add a dedicated `datasets` field to `ProjectMetadata`). Everything else is within ordinary implementation scope per §10.4.1.

---

## Readiness assessment

**Ready for implementation planning and approval.** The prerequisites (2.2.1 and 2.2.2) are verified complete (233 tests passing). The interfaces are established: `import_light_curve(file_path) -> LightCurveDataset`, `LightCurveDataset.to_dict()`/`from_dict()`, `ProjectService` lifecycle, `ProjectRepository` atomic JSON persistence. No blockers remain for planning.

I am waiting for your review and explicit approval of the recommendations (especially the persistence format in section E and the approval items in section M) before any implementation begins, per Plan mode and §10.9/§10.4.

# ChatGPT — Plan Review (Version 1)

Review of OpenCode's 2.2.3 planning report

Overall assessment: strong report, but I would not approve implementation yet.

OpenCode has correctly identified the main integration gap and proposed a relatively small architecture:

- A dataset persistence component.
- A project-level dataset collection managed by `ProjectService`.
- Individual persisted dataset files.
- Dataset references in project metadata.
- Dataset-aware dirty-state and save/reopen behavior.

That is a reasonable direction. The report also correctly keeps the GUI import workflow, visualization, permanent storage architecture, and later analysis features outside 2.2.3.

However, there are several design details that need to be resolved before we authorize the implementation. The most important concerns are where dataset references belong, how persistence remains consistent after partial failures, and whether the proposed JSON representation is sufficiently robust for scientific data.

The 233 passing tests establish a good baseline. They do not yet verify any of the proposed dataset-persistence behavior.

## 1. Issues that need resolution

### Issue 1 — `external_data_references` is the wrong place for internal dataset references

Needs revision

This is the clearest problem in the proposed design.

OpenCode recommends using `ProjectMetadata.external_data_references` to store references to the application's own persisted dataset files.

However, the existing model explicitly describes this field as:

> References to external data files used by the project.

I checked the existing tests as well. `tests/test_project_repository.py` and `tests/test_project_status.py` already use it for external file references, including FITS paths and availability information.

The distinction matters:

- An external reference identifies data that exists outside the project.
- A persisted project dataset identifies scientific data that the project itself manages.

These are related concepts, but they are not interchangeable.

My recommendation: Keep `external_data_references` for external source references. Investigate a separate dataset manifest, such as:

```
project/
├── project.json
└── datasets/
    ├── manifest.json
    ├── <dataset-id>.json
    └── <dataset-id>.json
```

This would let us:

- Keep project metadata schema version 2.
- Avoid adding scientific data to `project.json`.
- Avoid repurposing an existing field.
- Maintain a dedicated index of project-owned datasets.
- Give the dataset persistence layer responsibility for its own records.

The manifest could have its own format version without requiring a project metadata schema migration.

This is my preferred direction for further investigation, not an approved architecture decision.

### Issue 2 — The save transaction needs more work

Needs revision

OpenCode's proposed sequence is:

1. Write all dataset files.
2. Update dataset references.
3. Save `project.json`.
4. Mark the project clean.

That sequence has a useful property: a failure while writing dataset files leaves the existing project metadata untouched.

However, the proposed report does not fully establish how the complete operation behaves under every failure condition.

Consider this situation:

- A user imports a dataset.
- They also rename the project.
- The dataset file saves successfully.
- The dataset references save successfully.
- The project metadata save fails.

The application reports a failed save, but the dataset association may already exist on disk.

What happens if the user subsequently chooses Discard?

The application must have a defined answer. Otherwise, Save/Discard/Cancel no longer has predictable behavior.

The plan needs to establish whether it will:

- Roll back already-committed dataset changes when a later save step fails.
- Use staging and a commit mechanism.
- Or explicitly define a different, carefully controlled save contract.

I would not accept simply saying that the project remains dirty. Dirty-state tracking alone does not undo partially persisted changes.

### Issue 3 — Automatic orphan cleanup is unnecessarily risky

Revise scope

The report proposes deleting dataset files that are not referenced after a successful save.

I would defer that behavior.

An unreferenced file might be:

- A leftover from a failed save.
- A dataset awaiting recovery.
- A manually retained backup.
- A file from a newer storage format.
- An artifact that the application does not yet understand.

Automatically deleting files during an ordinary project save introduces unnecessary data-loss risk.

For 2.2.3, I recommend:

- Detect unreferenced files if useful.
- Report them or leave them untouched.
- Do not automatically delete them.
- Defer cleanup and garbage collection to a later, explicitly designed operation.

Storage is cheap compared with losing scientific data.

### Issue 4 — Dataset files need their own format version

Needs clarification

The report proposes testing unsupported dataset schema versions, but its proposed JSON structure does not actually define a dataset persistence version.

The existing `LightCurveDataset` model has its own structure, but that is not the same thing as a versioned on-disk format.

I recommend investigating a simple storage envelope:

```
{
  "storage_format_version": 1,
  "dataset": {
    "...": "serialized LightCurveDataset"
  }
}
```

This would let future versions of ECAS identify which persistence format a dataset uses.

It would also give us a clear place to handle compatibility and future migration without confusing the dataset file format with project metadata schema version 2.

No need to build a general migration framework now. Just establish a version identifier and a defined response to unsupported versions.

### Issue 5 — JSON and non-finite values need a more complete comparison

Needs clarification

OpenCode's explanation is technically reasonable:

- Python's default JSON encoder permits `NaN` and infinity.
- Python's default decoder can read those values back.
- Finite Python floating-point values can round-trip through JSON without ordinary decimal precision loss.

However, those non-finite representations are not compliant with strict JSON.

The report acknowledges this, but it moves fairly quickly to accepting the limitation.

I want the revised plan to compare two additional possibilities:

1. JSON with an explicit, standards-compliant representation for non-finite values.
2. A hybrid format with JSON metadata and binary NumPy arrays.

The objective is not to force a more complicated format. It is to establish whether the simplest option is still the best option after considering portability and scientific preservation.

For whichever approach is recommended, the tests must cover:

- `NaN` positions.
- Positive and negative infinity.
- Float64 precision.
- Integer array types.
- Empty versus absent arrays.
- Uncertainties.
- All source and validation metadata.

## 2. What I agree with

These recommendations are sound and should be retained unless the revised analysis uncovers a concrete reason to change them.

| Recommendation                                  | My assessment |
| ----------------------------------------------- | ------------- |
| `ProjectService` coordinates dataset lifecycle  | Agree         |
| Multiple datasets per project                   | Agree         |
| Reuse existing `dataset_id`                     | Agree         |
| Keep scientific arrays out of `project.json`    | Agree         |
| Keep the original FITS file untouched           | Agree         |
| Recover datasets without the original FITS file | Agree         |
| Preserve SAP and PDCSAP independently           | Agree         |
| Preserve non-finite values and quality flags    | Agree         |
| Dataset additions mark the project dirty        | Agree         |
| Keep schema v2 if practical                     | Agree         |
| No GUI import workflow in 2.2.3                 | Agree         |
| Service-level tests for integration             | Agree         |
| Defer permanent storage architecture            | Agree         |
| Defer dataset deletion and replacement          | Agree         |

One additional point: I agree with keeping the dataset collection in `ProjectService` for now. It gives us a clear place to coordinate project lifecycle operations without introducing a large new application architecture.

## 3. Proposed architecture direction

This is the direction I would ask OpenCode to investigate further:

## Provisional project structure

Project directory

Existing project metadata remains separate.

`project.json`

Schema v2

datasets/

`manifest.json`

Dataset index

`<dataset-id-1>.json`

`<dataset-id-2>.json`

Each dataset is independently stored and identified.

Runtime coordination

ProjectService

Active project and dataset collection

Dataset persistence component

Save, load, validate and recover

This is a proposed direction, not a final design. The save transaction still needs to be worked out, particularly how dataset changes and metadata changes behave together when a save partially fails.

## 4. What I want OpenCode to revise

I don't think we need another complete investigation. The first report already did most of the necessary work.

I recommend a focused follow-up PLAN request covering these five points:

1. Reevaluate the use of `external_data_references` and compare it with a separate dataset manifest.
2. Design the complete save transaction, including failure and Discard behavior.
3. Remove automatic orphan-file deletion from the proposed 2.2.3 scope.
4. Add explicit dataset storage-format versioning.
5. Reevaluate JSON serialization against a standards-compliant non-finite-value representation and a hybrid binary-array option.

Ask OpenCode to return revised sections D, E, F, H, I, J, L, and M, rather than repeat the entire report.

## 5. Current approval status

2.2.3 architecture

Not approved

| Decision                                         | Status                              |
| ------------------------------------------------ | ----------------------------------- |
| Service-level dataset integration                | Provisionally accepted              |
| Multiple datasets per project                    | Provisionally accepted              |
| Dataset identity via UUID                        | Provisionally accepted              |
| Separate dataset persistence                     | Direction accepted                  |
| Per-dataset JSON format                          | Awaiting revision                   |
| `external_data_references` for internal datasets | Not accepted                        |
| Dataset manifest                                 | Preferred alternative; needs review |
| Save transaction design                          | Not resolved                        |
| Automatic orphan cleanup                         | Deferred                            |
| Project schema v2                                | Preferred, subject to design        |
| Permanent D6 storage architecture                | Still deferred                      |

Conclusion: OpenCode's report is a good first planning pass. I would retain its overall architecture direction but resolve the five issues above before approving the final implementation plan.

The next step is a focused planning revision, not BUILD.

---

# Planning Version 2

ChatGPT — OpenCode Revision Prompt

SUBTASK 2.2.3 — PLAN REVISION: DATASET PERSISTENCE AND PROJECT INTEGRATION

## MODE: PLAN ONLY — INSPECT, ANALYZE, AND REVISE THE PROPOSED DESIGN

We have completed the initial planning investigation for Subtask 2.2.3. Your previous report identified a workable direction, but several architectural and data-integrity questions need to be resolved before implementation can be approved.

Your task is to **revise and strengthen the 2.2.3 implementation plan** in response to the review points below.

This remains a planning task.

### 1. Mandatory operating restrictions

- Do not implement anything.
- Do not modify source code, tests, configuration, or documentation.
- Do not create, delete, rename, or move files.
- Do not run commands that modify the repository.
- Do not commit or push anything.
- Do not modify the Foundation documentation.
- Do not begin BUILD or implementation work.
- Preserve all existing user changes.
- You may inspect source files, tests, documentation, and repository history as needed.
- Clearly distinguish verified facts, design proposals, assumptions, and unresolved decisions.

The user retains final authority over architectural decisions. A revised plan is not implementation approval.

### 2. Preserve the existing investigation

Do not repeat the entire original investigation unnecessarily.

Use your previous report as the starting point. Revisit the relevant source files and tests where necessary to verify the design, especially:

- `src/project_model.py`
- `src/project_repository.py`
- `src/project_service.py`
- `src/light_curve.py`
- `src/fits_importer.py`
- Existing project and dataset-related tests
- Relevant Foundation documentation and architecture decisions

Confirm that your revised recommendations remain compatible with the actual repository.

### 3. Resolve the internal dataset reference design

Your previous recommendation was to store internal dataset references in:

`ProjectMetadata.external_data_references`

The review identified a semantic conflict.

That field is currently documented and tested as a place for references to external data files and their provenance. It is used for information such as original FITS source paths and availability.

An internally persisted, project-owned dataset is not the same thing as an external source file.

Reconsider this design.

Evaluate a separate dataset manifest/index, for example:

```text
project/
    project.json
    datasets/
        manifest.json
        <dataset-id>.json
```

The example is a proposal, not an approved requirement.

Address:

1. Whether a separate manifest is the cleanest design.
2. Whether it should contain dataset IDs, relative storage paths, names, and other minimal identifying information.
3. Whether `external_data_references` should remain reserved for external source references.
4. Whether the existing project metadata schema version 2 can remain unchanged.
5. Whether the dataset manifest and individual dataset files need their own format versions.
6. How projects created before dataset persistence was introduced should behave.
7. Whether a project with no manifest should simply be interpreted as having zero persisted datasets.

Compare alternatives if you believe a separate manifest is not appropriate. Explain the tradeoffs rather than assuming the proposed structure is automatically correct.

### 4. Define the save transaction and failure behavior

This is a major unresolved issue.

Your previous plan proposed:

1. Write dataset files.
2. Update project references.
3. Save `project.json`.
4. Mark the project clean.

However, this does not fully define what happens when a failure occurs partway through the operation.

For example:

- Dataset A is written successfully.
- Dataset B is written successfully.
- Updating or saving the manifest fails.
- The user later chooses Discard when closing the project.

What has actually been saved? What does Discard mean in this situation?

Develop a clear persistence and save-consistency design.

Evaluate how to coordinate:

- Individual dataset file writes.
- Dataset manifest updates.
- Existing project metadata saves.
- The project's dirty state.
- Save failure handling.
- Retrying a failed save.
- Save/Discard/Cancel behavior when closing or switching projects.

Consider staging files, atomic replacement, rollback, transaction journals, or another proportionate approach.

You do not need to build a complex database-style transaction system if a simpler design can meet the requirements. However, the plan must explicitly identify the consistency guarantees and limitations.

Answer these questions directly:

1. What is the commit point for a dataset addition?
2. Can a partially completed save leave a dataset visible after reopening?
3. Can a failed save leave a dataset file that is not referenced by the project?
4. If so, how is that condition detected and handled?
5. Does choosing Discard guarantee that unsaved dataset additions are not present after reopening?
6. Does the proposed design preserve the existing atomic-save behavior of `ProjectRepository`?
7. When is the project marked clean?

Do not claim that the existing dirty-state mechanism automatically provides rollback. It currently tracks project metadata changes; it is not itself a transactional persistence mechanism.

### 5. Do not automatically delete orphaned dataset files

Your previous plan proposed deleting unreferenced dataset files during a later successful save.

Do not include automatic orphan deletion in the 2.2.3 implementation scope.

An unreferenced file might be:

- The result of an interrupted save.
- A leftover from a failed operation.
- A backup or recovery artifact.
- A file from a newer or partially recognized storage format.

For this subtask, prefer a conservative policy:

- Detect or identify unreferenced dataset files where practical.
- Report or preserve them.
- Do not silently delete them during ordinary save operations.

Explain whether orphan detection belongs in 2.2.3 or should be deferred. Any future cleanup mechanism should be a separately designed operation.

### 6. Define dataset storage format versioning

The proposed individual dataset JSON files need an explicit storage-format version.

Evaluate a wrapper such as:

```json
{
  "storage_format_version": 1,
  "dataset": {
    "...": "..."
  }
}
```

The exact structure is not mandatory, but the design must distinguish:

- Project metadata schema version.
- Dataset manifest format version.
- Individual dataset storage format version.
- The in-memory `LightCurveDataset` model.

Explain how unsupported future versions should be handled. Do not introduce a general migration framework unless the requirements genuinely justify it.

### 7. Reconsider non-finite values and scientific data fidelity

Your previous report recommended using Python's default JSON behavior.

Python's standard `json` module can serialize `NaN`, `Infinity`, and `-Infinity` by default. Python can read these values back, but they are not compliant with strict JSON specifications.

This matters because the imported scientific data intentionally preserves non-finite measurements.

Compare these three options:

**Option A — Default Python JSON behavior**
- Use the existing `to_dict()` representation.
- Allow Python's default non-standard `NaN` and infinity tokens.
- Reconstruct using `from_dict()`.

**Option B — Standards-compliant tagged representation**
- Encode non-finite values using an explicit JSON-compatible representation.
- Decode those representations when reconstructing the dataset.
- Preserve the distinction between NaN, positive infinity, and negative infinity.

**Option C — Hybrid metadata and binary arrays**
- Store metadata in JSON.
- Store numerical arrays in a suitable binary representation such as NumPy `.npz`.
- Reconstruct the model from both components.

For each option, assess:

- Implementation complexity.
- Scientific fidelity.
- Readability and inspectability.
- Dependencies.
- File size and performance.
- Error handling.
- Compatibility with the existing `LightCurveDataset.to_dict()` and `from_dict()` methods.

Recommend one approach for this initial vertical slice and explain why.

Whichever approach you recommend, explicitly plan tests for:

- NaN preservation.
- Positive and negative infinity preservation.
- Finite float64 precision.
- Integer dtype preservation.
- `None` versus empty-array distinctions.
- Uncertainty arrays.
- Quality flags and cadence numbers.
- Time information and units.
- Source metadata.
- Validation findings.

Do not silently filter, normalize, convert, or discard scientific values to make serialization easier.

### 8. Validate IDs and storage paths

Define how dataset IDs and storage paths will be validated.

The design must prevent:

- Path traversal.
- Absolute paths escaping the project directory.
- Dataset references pointing outside the project.
- Duplicate dataset IDs.
- Duplicate manifest entries.
- Malformed or unsupported storage paths.

Prefer storing project-relative paths rather than absolute paths for internal dataset storage.

Explain how paths will be resolved and checked to ensure they remain inside the project's dataset storage directory.

Preserve the original source-file path as provenance metadata; do not confuse it with the internal persisted dataset path.

### 9. Define missing and corrupted data behavior

Distinguish these cases:

**A. Missing manifest**
- What should happen when opening a project that has no dataset manifest?

**B. Corrupted manifest**
- Should the project still open?
- How should the application communicate that dataset associations could not be loaded?
- How do we avoid silently treating a corrupted manifest as an empty dataset collection and thereby losing the user's ability to recover associations?

**C. Missing individual dataset file**
- Should the remaining valid datasets still load?
- How should the missing dataset be reported?

**D. Corrupted individual dataset file**
- Can one invalid dataset be isolated without preventing other valid datasets from loading?

**E. Unsupported format version**
- How should an unsupported manifest or dataset version be handled?

Recommend proportionate behavior for this subtask. Prioritize preservation and clear error reporting over silent recovery or deletion.

### 10. Refine the ProjectService integration

Retain the general direction of using `ProjectService` as the coordinator for the active project's datasets, unless the repository evidence indicates otherwise.

Define the proposed service responsibilities:

- Holding the active project's dataset collection.
- Associating a newly imported `LightCurveDataset` with the active project.
- Supporting multiple datasets in one project.
- Loading persisted datasets when opening a project.
- Persisting datasets when saving a project.
- Clearing runtime dataset state when closing or switching projects.
- Marking the project dirty when a dataset is added.
- Preventing accidental cross-project dataset association.

Clarify which responsibilities belong in a dedicated dataset repository versus `ProjectService`.

Keep `LightCurveDataset` independent of project persistence and GUI code unless there is a compelling, evidence-based reason to change that boundary.

### 11. Maintain the existing scope boundaries

The intended 2.2.3 scope remains project integration and provisional persistence.

Do not expand this subtask into:

- A GUI import workflow or import menu.
- New GUI screens or dialogs.
- Dataset deletion, replacement, or editing.
- Re-import workflows.
- Multi-project dataset sharing.
- Permanent storage architecture decisions under D6.
- BLS or transit analysis.
- Operation records or analysis history.
- Stage 4 archive downloading.
- Broad GUI test infrastructure repairs.

The FITS importer remains a separate import function. The service layer should be capable of accepting an already imported `LightCurveDataset`.

The original FITS file must remain untouched. Persisting a dataset must not modify, move, or overwrite its source file.

### 12. Revise the test plan

Provide a focused test plan that covers the revised design.

Include, where applicable:

**Dataset repository**
- Save and load one dataset.
- Save and load multiple datasets.
- Dataset storage format version.
- Manifest format version.
- Missing manifest behavior.
- Corrupted manifest behavior.
- Missing dataset file.
- Corrupted dataset file.
- Unsupported versions.
- Duplicate IDs and entries.
- Invalid paths and path traversal attempts.
- Atomic writes.
- Failed writes and retry behavior.
- Orphan detection without deletion.

**Scientific fidelity**
- NaN and both infinity signs.
- Finite float64 precision.
- Integer dtypes.
- None versus empty arrays.
- Uncertainties.
- Quality flags.
- Cadence numbers.
- Time metadata.
- Source metadata.
- Validation findings.
- SAP and PDCSAP measurements remaining distinct.

**ProjectService**
- Add a dataset to an active project.
- Multiple datasets in one project.
- Adding a dataset marks the project dirty.
- Save and reopen preserves datasets.
- Closing clears active runtime state.
- Switching projects does not leak datasets between projects.
- Failed save behavior.
- Discard behavior.
- Project with no datasets continues to work.

Avoid redundant tests that merely repeat existing `LightCurveDataset` or FITS importer tests without exercising persistence or integration.

### 13. Revise the implementation sequence and file boundaries

Provide a proposed implementation sequence with dependencies between phases.

Identify:

- New files.
- Existing files likely to change.
- Existing files that should remain untouched.
- Tests to add or modify.
- Documentation updates that belong in 2.2.3.
- Documentation consolidation that remains deferred to 2.2.4.

Keep the implementation boundary as small as reasonably possible.

In particular, reconsider whether `project_model.py`, `project_repository.py`, `light_curve.py`, or `fits_importer.py` actually need modifications.

Do not modify any files during this planning task.

### 14. Required final report

Return a revised plan with the following sections:

**A. Executive summary**
- Recommended architecture.
- Main changes from your previous proposal.
- Remaining risks.

**B. Verified existing architecture**
- Relevant current classes, responsibilities, and persistence behavior.
- Cite actual file paths and methods.

**C. Revised storage design**
- Directory structure.
- Manifest responsibilities.
- Individual dataset file structure.
- Versioning.
- Path validation.

**D. Save consistency and failure semantics**
- Save sequence.
- Commit point.
- Atomicity guarantees.
- Failure and retry behavior.
- Discard behavior.
- Dirty-state handling.

**E. Scientific data fidelity**
- Serialization approach comparison.
- Recommendation.
- Preservation guarantees and limitations.

**F. Missing/corrupt data behavior**
- Explicit behavior for every case in Section 9.

**G. ProjectService integration**
- Responsibilities and method-level proposals.
- Runtime lifecycle.
- Project isolation.

**H. Test plan**
- Grouped tests and the behavior each group verifies.

**I. Implementation sequence**
- Phases, dependencies, and likely files.

**J. Scope exclusions**
- Explicitly identify deferred work.

**K. Documentation plan**
- What gets recorded during 2.2.3.
- What remains for 2.2.4.
- Confirm Foundation documentation remains untouched.

**L. Risks and unresolved decisions**
- Identify any decisions that still require user approval.
- Do not hide uncertainty behind a single recommendation.

**M. Approval checklist**
- List each consequential design decision separately.
- Explain the practical consequence of approving or rejecting it.
- Clearly identify your recommended choice.
- Do not treat silence as approval.

### 15. Final instruction

The goal is a technically coherent, conservative, testable plan that preserves scientific data and existing project behavior.

Do not begin implementation after producing the report. Wait for the user to review the revised plan and explicitly authorize the next step.

# OpenCode — Revised Plan (Version 2)

I now have all verified facts needed. Here is the revised plan.

---

 REVISED PLAN REPORT — Subtask 2.2.3: Dataset Persistence and Project Integration

**Mode:** PLAN ONLY. No files inspected were modified. No commands that alter the repository were run beyond read-only inspection already performed.

## A. Executive summary

**Recommended architecture:**
- A project's persisted datasets live in a `<project_dir>/datasets/` directory containing:
  - `manifest.json` — a minimal index of dataset associations (dataset_id, relative path, name, imported_at, source summary).
  - One `<dataset_id>.json` per dataset — the full serialized `LightCurveDataset`.
- `ProjectMetadata.external_data_references` remains reserved for external source references (original FITS paths, etc.) and is **not** used for internal dataset references.
- Project metadata schema version 2 remains unchanged.
- `ProjectService` coordinates the active project's runtime dataset collection, dirty marking on dataset addition, and dataset save/load integrated into project save/open/close.
- Atomic writes (temp file + `os.replace`) for every dataset file, the manifest, and `project.json`.

**Main changes from previous proposal:**
- Replaced `external_data_references` for dataset references with a separate manifest (resolves the semantic conflict).
- Removed automatic orphan-file deletion (conservative preserve-and-report policy).
- Added explicit storage-format versioning for manifest and dataset files.
- Defined a concrete commit point and failure semantics for the save transaction.
- Selected Option A (default Python JSON) for serialization after comparing three options.

**Remaining risks:**
- Non-standard JSON (`NaN`/`Infinity` tokens) from Python's default JSON — documented provisional limitation, acceptable for the first vertical slice under deferred D6.
- Orphan dataset files can accumulate after failed saves; cleanup is deliberately deferred to a separate operation.
- No GUI import workflow in this subtask; end-to-end user verification requires later GUI work.

---

## B. Verified existing architecture

**Confirmed from source inspection:**

| Module | Class / method | Responsibility |
|---|---|---|
| `src/project_model.py` | `ProjectMetadata` (dataclass) | Project metadata: `project_id` (UUID), `name`, `created_at`, `status`, `schema_version=2`, `external_data_references: list`, `owner`, `roles`, `is_dirty`. Docstring on `external_data_references`: "References to external data files used by the project (paths, provenance). Preserved even when the referenced file is not currently accessible." `SCHEMA_VERSION = 2`. `to_dict()`/`from_dict()` round-trip all fields including `external_data_references`. v1→v2 in-memory migration. |
| `src/project_model.py` | `ProjectMetadata.validate()` | Rejects schema versions > 2; validates owner/roles/name/project_id/status. |
| `src/project_repository.py` | `ProjectRepository.save(metadata)` | Validates, creates `<projects_root>/<project_id>/`, writes `project.json` atomically via `_write_json_atomic` (temp file + `os.replace` + `fsync`), then `metadata.mark_clean()`. |
| `src/project_repository.py` | `ProjectRepository._write_json_atomic(path, data)` | Existing atomic-write pattern: `tempfile.mkstemp` in target dir, write+flush+fsync, `os.replace`, cleanup temp on failure. |
| `src/project_repository.py` | `ProjectRepository.load(project_id)` / `load_from_directory(directory)` | Reads `project.json`; `JSONDecodeError` → `ProjectCorruptedError`; validation failure → `ProjectCorruptedError`. |
| `src/project_service.py` | `ProjectService` | Holds `_active_project` and `_active_location`. `save_project()` saves metadata via repository, marks clean on success, preserves dirty on failure. `open_project()`/`open_project_from_path()` load metadata and set active. `close_project()` clears active state. `change_status()`, `discover_projects()`. No dataset awareness today. |
| `src/main_window.py` | `MainWindow` | PySide6 shell; Save/Discard/Cancel prompts; dirty asterisk; menu state gated by `is_dirty`. No import action exists. |
| `src/light_curve.py` | `LightCurveDataset` | `dataset_id` (UUID, auto-generated), `name`, `source` (DatasetSource), `time` (TimeInfo), `measurements` (MeasurementSeries of MeasurementColumn), `quality_flags`, `cadence_numbers`, `validation` (ValidationReport), `imported_at`, `notes`. `to_dict()` → JSON-compatible dict (arrays → lists); `from_dict()` reconstructs and re-validates. Arrays copied on construction. Independent of project/persistence/GUI. |
| `src/fits_importer.py` | `import_light_curve(file_path)` | Returns `LightCurveDataset`. Reads FITS read-only, never modifies source. Records `original_filename`/`original_file_path` in `DatasetSource`. No project/GUI/persistence imports. |

**Verified test state:** 233 non-GUI tests pass (`test_light_curve.py`, `test_fits_importer.py`, `test_project_model.py`, `test_project_repository.py`, `test_project_service.py`, `test_project_discovery.py`, `test_project_status.py`). GUI tests hang in this headless environment (pre-existing).

---

## C. Revised storage design

### Directory structure
```
<projects_root>/<project_id>/
    project.json              # existing project metadata (schema v2, unchanged)
    datasets/
        manifest.json         # dataset association index
        <dataset-uuid>.json   # one file per persisted LightCurveDataset
```

### Manifest responsibilities
`manifest.json` is the authoritative index of which datasets belong to the project. Each entry is minimal identifying information:
- `dataset_id` (string UUID)
- `dataset_file` (project-relative path, e.g. `datasets/<uuid>.json`)
- `name` (dataset display name)
- `imported_at` (ISO timestamp)
- `source` (summary: `original_filename`, `original_file_path` as provenance)

The manifest does **not** contain measurement arrays — those live in the individual dataset files. This keeps the manifest small and fast to read, and lets a corrupted individual dataset file be isolated.

### Individual dataset file structure
Each `<dataset_id>.json` contains a versioned wrapper:
```json
{
  "storage_format_version": 1,
  "dataset": { ... LightCurveDataset.to_dict() output ... }
}
```
The `dataset` payload is exactly the existing `to_dict()` output, so no changes to `light_curve.py` are needed.

### Versioning (three distinct versions, kept separate)
1. **Project metadata schema version** — `schema_version = 2` in `project.json`. Unchanged by this subtask.
2. **Dataset manifest format version** — `manifest_format_version` in `manifest.json`, starting at 1.
3. **Individual dataset storage format version** — `storage_format_version` in each `<dataset_id>.json`, starting at 1.
4. **In-memory `LightCurveDataset` model** — has no version field of its own; its structure is defined by `to_dict()`/`from_dict()`.

### Path validation
- All internal dataset paths are **project-relative** (e.g. `datasets/<uuid>.json`), never absolute.
- On write, the target path is resolved as `<project_dir>/<relative_path>` and verified to be within the project's `datasets/` directory (prevents path traversal / escape).
- Dataset IDs are UUIDs (validated by `LightCurveDataset` construction and manifest load).
- Duplicate dataset IDs are rejected at manifest load; duplicate manifest entries rejected on save.
- Original source-file path (`DatasetSource.original_file_path`) is preserved as provenance inside the dataset file and is distinct from the internal persisted path.

### Why `external_data_references` is not reused
Verified in `project_model.py`: its documented purpose is "References to external data files used by the project (paths, provenance)." An internally owned, project-persisted dataset is not an external source file. Using it for internal dataset references would conflate two distinct concepts and violate the field's documented contract. A separate manifest keeps the separation clean.

### Schema compatibility
Schema version 2 remains unchanged. No new fields on `ProjectMetadata`. Pre-existing projects with no `datasets/` directory or no `manifest.json` are interpreted as having zero persisted datasets — fully backward compatible. `ProjectMetadata.from_dict` is untouched.

---

## D. Save consistency and failure semantics

### Save sequence (recommended)
For `ProjectService.save_project()` when datasets are associated:

1. **Require active project**; error if none (existing behavior).
2. **Serialize all associated datasets** in memory first (validate `to_dict()` output can be built). Fail fast before any disk write if serialization fails.
3. **Write each dataset file atomically** to `datasets/<dataset_id>.json` using the existing temp-file + `os.replace` pattern (same directory, so `os.replace` is atomic). Writes are idempotent (same dataset_id → same filename).
4. **Write the manifest atomically** to `datasets/manifest.json`.
5. **Save `project.json`** via the existing `ProjectRepository.save()` (atomic, marks clean).
6. **Mark the project clean** only after steps 3–5 all succeed.

### Commit point
The commit point for the overall project save is the **successful write of `project.json`** (step 5). Until then, the project remains dirty. Individual dataset files and the manifest may exist on disk from steps 3–4 even if step 5 fails, but they are **unreferenced by a successful project save** until `project.json` is written.

### Atomicity guarantees
- Each file (dataset JSON, manifest, project.json) is written via temp-file + `os.replace`, matching the existing `_write_json_atomic` guarantee: a file is either the previous valid version or the new version, never partially written.
- The operation as a whole is **not** a single atomic transaction across multiple files (no journal/rollback). This is a deliberate, proportionate choice for the provisional slice.
- Existing `ProjectRepository` atomic-save behavior is preserved unchanged.

### Failure behavior (the 3-dataset example)
- Dataset A written → Dataset B written → manifest write fails.
  - A and B exist on disk as files. Manifest not updated. `project.json` not touched (previous valid version intact). Project stays **dirty**. User sees save error.
  - On reopen: manifest is absent/unchanged → A and B are **not referenced** → not loaded → effectively invisible. They are orphaned files on disk, preserved (not auto-deleted).
- `project.json` write fails after manifest written:
  - Dataset files + manifest exist on disk. `project.json` retains previous version. Project stays dirty.
  - On reopen: `project.json` loads fine (previous version). If service consults manifest at open, A and B might be referenced but `project.json` doesn't know about them... 

Wait — I need to resolve this carefully. How does the project know to consult the manifest on open?

**Resolution:** The manifest is consulted at open time by checking for the fixed relative path `datasets/manifest.json` inside the project directory. `project.json` does **not** reference the manifest (no schema change). So on open:
1. Load `project.json` (metadata).
2. Check `<project_dir>/datasets/manifest.json`. If it exists, load it and resolve each entry to a dataset file. If absent → zero datasets.

This means if manifest was written but `project.json` save failed, on reopen the manifest exists and A/B would be loaded — even though the user's save "failed." Is that a problem? The project is still dirty (project.json wasn't re-saved), but the datasets are recoverable. This is actually **conservative in favor of data preservation** (don't lose the user's data). The dirty state correctly tells the user "there's unsaved work" even though some data is on disk. On a successful re-save, everything is reconciled.

Alternatively, the manifest could only be written as part of the project.json save — but they're separate files, so true atomicity across both isn't possible without a journal. I'll accept the preserve-data lean: datasets written to disk are recoverable on reopen even if the metadata save failed, and the project remains dirty until a clean save completes.

### Retry behavior
A failed save can be retried. Retrying re-writes dataset files (idempotent, same filenames), rewrites the manifest, and re-saves `project.json`. Orphan files from a prior failed attempt with the same dataset_id are overwritten. New orphan files (different dataset_id) may accumulate but remain unreferenced.

### Discard behavior
- **Discard on close/switch** clears in-memory runtime state (active project + dataset collection). It does **not** delete files already on disk.
- If no save was ever attempted: no dataset files exist → clean discard, nothing persists. ✅
- If a save partially wrote dataset files then failed, and user Discards: orphan files remain on disk but unreferenced → not loaded on reopen → the dataset addition is effectively not visible. This satisfies "unsaved dataset additions are not present after reopening" from the user's perspective, while preserving the files (per section 5's no-auto-delete policy).
- Discard does **not** roll back already-written files; that is a documented limitation, not a bug.

### When is the project marked clean?
Only after all dataset files, the manifest, and `project.json` are written successfully. Any failure → dirty preserved, active project preserved, error surfaced.

---

## E. Scientific data fidelity

### Option comparison

| Criterion | Option A — Default Python JSON | Option B — Standards-compliant tagged representation | Option C — Hybrid JSON + binary arrays (.npz) |
|---|---|---|---|
| Reuses existing `to_dict()`/`from_dict()` | Yes, zero changes | No — requires custom encode/decode | Partial — metadata in JSON, arrays elsewhere |
| NaN / ±Inf preservation | Exact round-trip in Python (`allow_nan=True`) | Exact via explicit tags | Exact in binary arrays |
| Strict JSON (RFC 8259) compliant | No — emits non-standard `NaN`/`Infinity` tokens | Yes | Metadata JSON yes; binary payload not JSON |
| Float64 precision | Exact (Python shortest-repr round-trip) | Exact | Exact |
| Integer dtype preservation | Yes (explicit dtype in `from_dict`) | Yes | Yes |
| None vs empty array distinguished | Yes | Yes | Yes |
| Implementation complexity | Minimal | Moderate | Highest (two-file format, pairing logic) |
| Readability / inspectability | High (single JSON file) | High (JSON) | Low (binary arrays) |
| New dependencies | None | None | None (npz is NumPy, already a dep) |
| Error handling | `from_dict` re-validates on load | Custom decode errors | Binary read errors + JSON errors |

### Recommendation: Option A

For the initial vertical slice, **Option A** is the smallest maintainable approach:
- Zero changes to `light_curve.py` — `to_dict()`/`from_dict()` already round-trip all model fields.
- Non-finite values (`NaN`, `+Inf`, `-Inf`) round-trip exactly through Python's `json` (default `allow_nan=True`). Python's `json.load` reads `NaN`/`Infinity`/`-Infinity` tokens back to `nan`/`inf`/`-inf`.
- Finite float64 values preserve full precision (Python uses shortest repr that round-trips).
- Integer arrays: `tolist()` → Python ints; `from_dict` reconstructs with explicit `dtype=np.int64` (quality/cadence) and `np.float64` (time/measurements/uncertainties).
- `None` vs empty arrays distinguished by `is None` checks in `from_dict`.
- All metadata, source info, units, validation findings are strings/primitives — fully round-tripped.

**Limitation (documented):** The emitted JSON is not RFC 8259-compliant because `NaN`/`Infinity`/`-Infinity` are not valid JSON tokens. Strict JSON parsers will reject the file. This is acceptable for a provisional local-file slice under deferred D6, and must be clearly documented as a known limitation. Options B or C can be adopted later when D6 is revisited.

### Scientific fidelity tests to plan
- NaN preservation (position and count).
- Positive infinity and negative infinity preservation (signs).
- Finite float64 precision (value equality after round-trip).
- Integer dtype preservation (quality_flags/cadence as int64).
- `None` uncertainties vs zero-valued uncertainty arrays distinguished.
- Empty arrays vs None distinguished.
- Uncertainty arrays preserved and associated with correct measurement column.
- Quality flags and cadence numbers preserved.
- Time values, unit, reference, scale, frame preserved.
- Source metadata (`original_filename`, `original_file_path`, mission, instrument, target, source_id) preserved.
- Validation findings (errors/warnings/info) preserved.
- SAP_FLUX and PDCSAP_FLUX remain distinct columns.

No filtering, normalization, detrending, or discarding of non-finite values.

---

## F. Missing/corrupt data behavior

Explicit behavior for each case:

**A. Missing manifest** (`datasets/manifest.json` absent)
- Project opens normally. Zero datasets loaded. Backward compatible with pre-2.2.3 projects. No error (manifest absence is normal for projects created before dataset persistence).

**B. Corrupted manifest** (malformed JSON or invalid structure)
- Project metadata (`project.json`) still loads — project opens.
- Dataset associations fail to load. Surface a clear error identifying the manifest as corrupted/unreadable.
- Do **not** silently treat as an empty dataset collection (that would hide data loss and prevent recovery). Continue loading any other valid project content.
- Individual dataset files may still exist on disk; they are simply not referenced by a readable manifest.

**C. Missing individual dataset file** (manifest references a file that doesn't exist)
- Remaining valid datasets still load.
- The missing dataset is reported (identify by `dataset_id`/name). Project opens. Other datasets unaffected.

**D. Corrupted individual dataset file** (invalid JSON or fails `from_dict` validation)
- Isolated: one invalid dataset does not prevent other valid datasets from loading.
- Report which dataset failed. Project opens with the subset of valid datasets.

**E. Unsupported format version** (manifest version or dataset storage version not recognized)
- Report the unsupported version. Do not load that manifest/dataset. Other valid datasets still load. Do not silently skip or downgrade.

**General principle:** Preserve the project and all recoverable datasets; report failures per-dataset; never silently delete or fabricate data; one bad dataset must not invalidate the whole project (consistent with Foundation §4.6.8, §9.4.6 and the task's recovery requirements).

---

## G. ProjectService integration

`ProjectService` remains the coordinator for the active project's datasets. A dedicated dataset repository (new module) handles file I/O; `ProjectService` manages runtime state and lifecycle coordination.

### Proposed `ProjectService` responsibilities and method-level proposals

| Responsibility | Proposed method / behavior |
|---|---|
| Hold active project's dataset collection | Runtime `dict[str, LightCurveDataset]` keyed by `dataset_id`, private to service. |
| Associate an imported dataset | `add_dataset(dataset: LightCurveDataset)` → validates no duplicate `dataset_id`, stores in collection, calls `metadata.mark_dirty()`. Returns `dataset_id`. |
| Retrieve a dataset | `get_dataset(dataset_id) -> LightCurveDataset | None`. |
| List datasets | `list_datasets() -> list[LightCurveDataset]` (or summaries). |
| Load persisted datasets on open | After `repo.load()` in `open_project()`/`open_project_from_path()`, call dataset repository to load manifest + dataset files into the runtime collection. Errors isolated per dataset (section F). |
| Persist datasets on save | In `save_project()`, before `repo.save(metadata)`: persist all runtime datasets via dataset repository (dataset files + manifest). Only if all succeed, proceed to `repo.save()`. Mark clean only on full success. |
| Clear runtime state on close/switch | `close_project()` also clears the dataset collection. On project switch, previous project's datasets are cleared before the new project's are loaded (project isolation). |
| Dirty marking on dataset addition | `add_dataset()` marks `metadata.is_dirty = True` (scoped extension of existing mechanism; no new infrastructure). |
| Prevent cross-project leakage | Datasets are keyed by `dataset_id` within one project's runtime collection; cleared on close/switch; loaded per-project from that project's own `datasets/` directory. |

### Separation of concerns
- **Dataset repository** (new module, e.g. `src/dataset_repository.py`): file I/O — atomic writes/reads of dataset files and manifest, path validation, version checks, corruption detection. No knowledge of `ProjectMetadata` dirty state or GUI.
- **`ProjectService`**: lifecycle coordination — when to save/load/clear, dirty marking, active-project gating, error translation to existing exception types (`ProjectRepositoryError`, etc.).
- **`LightCurveDataset`**: untouched — remains independent of persistence and GUI.

---

## H. Test plan

All tests non-GUI, using `pytest tmp_path`, synthetic `LightCurveDataset` fixtures (including NaN/Inf). No dependence on the user's real Kepler-10b path.

### Dataset repository (`tests/test_dataset_repository.py` — new)
- Save and load one dataset; verify value-level equality of all fields.
- Save and load multiple datasets in one project; each recoverable by `dataset_id`.
- Manifest format version written and read.
- Dataset storage format version written and read.
- Missing manifest → zero datasets, no error.
- Corrupted manifest → clear error, project metadata still usable.
- Missing individual dataset file → other datasets load, missing one reported.
- Corrupted individual dataset file → isolated failure, other datasets load.
- Unsupported manifest/dataset version → error, not silently skipped.
- Duplicate dataset IDs rejected.
- Duplicate manifest entries rejected.
- Invalid paths / path traversal attempts rejected (relative paths only, confined to `datasets/`).
- Atomic writes: simulate write failure → no corrupted file left in place.
- Failed write → project/repository state unchanged (no partial corruption visible).
- Retry after failed save succeeds.
- Orphan detection: unreferenced dataset files are **not** deleted (preserve-and-report).
- Orphan files are identifiable/listable but not loaded.

### Scientific fidelity (within dataset repository tests)
- NaN preserved (position, count, `np.isnan`).
- `+Inf` and `-Inf` preserved (signs, `np.isposinf`/`np.isneginf`).
- Finite float64 precision (exact equality after round-trip).
- `quality_flags`/`cadence_numbers` reconstructed as `np.int64`.
- Time/measurements/uncertainties reconstructed as `np.float64`.
- `None` uncertainties vs zero-valued uncertainty arrays distinguished.
- Empty arrays vs None distinguished.
- SAP_FLUX and PDCSAP_FLUX remain distinct columns with distinct values.
- Units, time metadata, source metadata, validation findings preserved.

### ProjectService (extend `tests/test_project_service.py` or new module)
- Add dataset to active project → `is_dirty` becomes True.
- Multiple datasets in one project; `list_datasets()` returns all.
- `get_dataset()` returns correct dataset; wrong ID returns None.
- Save persists datasets; reopen (`open_project`) recovers them with all measurements/metadata.
- Closing clears runtime dataset collection.
- Switching projects does not leak datasets between projects.
- Failed save (e.g., read-only directory) → project stays dirty and active; `project.json` unchanged; error raised.
- Project with no datasets continues to work (save/open unaffected).
- No cross-project contamination: dataset added to project A is not visible in project B.

### Regression
- Run existing project lifecycle tests (`test_project_model.py`, `test_project_repository.py`, `test_project_service.py`, `test_project_discovery.py`, `test_project_status.py`, `test_project_save_close.py`).
- Run existing 2.2.1/2.2.2 tests (`test_light_curve.py`, `test_fits_importer.py`).

---

## I. Implementation sequence

### Phase 1 — Dataset repository (new file)
**Objective:** File I/O for dataset files + manifest; atomic writes; versioning; path validation; corruption/isolation handling.
**Likely new file:** `src/dataset_repository.py`
**Tests:** `tests/test_dataset_repository.py`
**Depends on:** Approval of storage design (C), serialization option (E), no-orphan-deletion policy.
**Files changed:** None existing (new file only).

### Phase 2 — ProjectService integration
**Objective:** Runtime dataset collection; `add_dataset`/`get_dataset`/`list_datasets`; integrate dataset save into `save_project()` and dataset load into `open_project()`/`open_project_from_path()`; dirty marking; clear on close/switch.
**Likely changed:** `src/project_service.py`
**Tests:** Extend `tests/test_project_service.py`
**Depends on:** Phase 1.

### Phase 3 — Tests + documentation
**Objective:** Complete test coverage; run full regression suite; record implementation in dev log + roadmap + tracking file.
**Files changed:** `tests/`, `docs/MASTER_DEVELOPMENT_ROADMAP.md`, `docs/development/DEVELOPMENT_LOG.md`, `docs/planning/.../task 2.2.n work to keep track of for documenting.md`.
**Depends on:** Phases 1–2 complete.

---

## J. Scope exclusions (explicitly deferred)

- GUI import workflow / import menu / new dialogs (2.3+ boundary).
- Dataset deletion, replacement, editing, re-import.
- Multi-project dataset sharing.
- Automatic orphan-file cleanup (separately designed operation).
- Permanent storage architecture (D6 remains deferred).
- BLS / transit analysis (2.4); operation records (2.5); Stage 4 archive downloading.
- Broad GUI test infrastructure repairs.
- Changes to `light_curve.py`, `fits_importer.py`, `project_model.py`, `main_window.py`.

### Files that should remain untouched
- `src/light_curve.py` — no redesign; reuse `to_dict()`/`from_dict()` as-is.
- `src/fits_importer.py` — no duplication; importer stays standalone.
- `src/project_model.py` — no schema change; `external_data_references` contract unchanged.
- `src/main_window.py` — no GUI import in this subtask.
- `docs/Foundation/*` — read-only.

---

## K. Documentation plan

### Update during 2.2.3
- `docs/MASTER_DEVELOPMENT_ROADMAP.md` — mark Task 2.2.3 status and progress (authoritative development status per §11.3.3).
- `docs/development/DEVELOPMENT_LOG.md` — record implementation decisions, files changed, test results, limitations, deferred work (§10.11, §11.3).
- `docs/planning/.../task 2.2.n work to keep track of for documenting.md` — update the running 2.2 record with verified 2.2.3 details.

### Defer to 2.2.4
- Broader architecture/data-model documentation consolidation; data-flow docs; final documentation reconciliation (per existing plan, 2.2.4 owns the consolidated pass).

### Confirm
- Foundation documentation remains untouched (read-only).

---

## L. Risks and unresolved decisions

| Risk | Assessment |
|---|---|
| Non-standard JSON (`NaN`/`Infinity` tokens) | Documented limitation; round-trips in Python; rejected by strict JSON parsers. Acceptable for provisional slice; revisit at D6. |
| Orphan file accumulation after failed saves | Preserve-and-report; no auto-delete; cleanup deferred. Acceptable for slice. |
| Save not a single cross-file atomic transaction | Per-file atomicity preserved; project stays dirty on partial failure. Documented limitation. |
| No GUI import path in 2.2.3 | End-to-end user verification deferred to GUI work; service-level tests cover logic. |
| `external_data_references` not reused for datasets | Resolves semantic conflict; separate manifest is cleaner. |

### Unresolved decisions requiring user approval (Section M details these):
1. Separate manifest + per-dataset file design (vs alternative).
2. Serialization Option A (default Python JSON with non-standard NaN/Inf).
3. Manifest at fixed relative path `datasets/manifest.json` (no schema change).
4. No automatic orphan deletion.
5. Commit point = successful `project.json` write; project clean only after full success.

---

## M. Approval checklist

Each decision below requires explicit user approval before implementation. Silence is not approval.

### 1. Storage design: separate manifest + per-dataset files
**Decision required:** Approve the `<project_dir>/datasets/` directory with `manifest.json` + one `<dataset_id>.json` per dataset, instead of reusing `external_data_references`.
**Context:** `external_data_references` is documented for external source files (original FITS paths). Internal project-owned datasets are a different concept; a separate manifest avoids semantic conflict and keeps schema v2 unchanged.
**Options:**
- (a) Separate manifest + per-dataset files (recommended).
- (b) Store dataset references in `external_data_references` (rejected — semantic conflict with documented purpose).
- (c) Add a new field to `ProjectMetadata` → requires schema version change to 3 (explicit approval needed; not recommended for this slice).
**Recommendation:** (a).
**Consequence of approving (a):** No schema change; backward compatible; clean separation of external vs internal references. Consequence of (c): schema migration, version bump, existing project handling — more work, not justified for the slice.
**Approval requested:** Yes — option (a).

### 2. Serialization format: Option A (default Python JSON)
**Decision required:** Approve using Python's default `json` (emits non-standard `NaN`/`Infinity`/`-Infinity` tokens) for dataset file serialization via existing `to_dict()`/`from_dict()`.
**Context:** Scientific data intentionally preserves non-finite values. Strict JSON (RFC 8259) doesn't support them, but Python's `json` round-trips them exactly.
**Options:**
- (a) Option A — default Python JSON (recommended for slice).
- (b) Option B — tagged standards-compliant representation (more complex, deferred).
- (c) Option C — hybrid JSON + binary `.npz` (most complex, deferred).
**Recommendation:** (a) for the initial vertical slice; document the non-compliant-JSON limitation.
**Consequence of approving (a):** Smallest change, zero new code, exact scientific round-trip within Python, documented limitation. Files not readable by strict JSON parsers (acceptable for provisional local storage).
**Approval requested:** Yes — option (a).

### 3. Manifest location: fixed relative path `datasets/manifest.json`
**Decision required:** Approve consulting the manifest at fixed relative path `datasets/manifest.json` on project open, without referencing it from `project.json` (no schema change).
**Context:** Keeps schema v2 unchanged and backward compatible; pre-existing projects (no manifest) = zero datasets.
**Options:**
- (a) Fixed relative path manifest consulted on open (recommended).
- (b) Manifest path stored in `project.json` → requires schema change.
**Recommendation:** (a).
**Approval requested:** Yes — option (a).

### 4. No automatic orphan-file deletion
**Decision required:** Approve conservative policy: detect/identify but do not silently delete unreferenced dataset files during ordinary saves; cleanup is a separately designed future operation.
**Context:** Orphan files may be interrupted-save results, backups, or newer-format artifacts; silent deletion risks data loss.
**Options:**
- (a) Preserve-and-report, no auto-delete (recommended).
- (b) Auto-delete unreferenced files on successful save (rejected for this slice).
**Recommendation:** (a).
**Approval requested:** Yes — option (a).

### 5. Commit point and dirty-state rule
**Decision required:** Approve that the project is marked clean only after all dataset files, manifest, and `project.json` are written successfully; any failure preserves dirty state and active project.
**Options:**
- (a) Commit at `project.json` write; clean only on full success (recommended).
- (b) Mark clean after dataset files written, before manifest/project.json (rejected — risks reporting success when data isn't durably associated).
**Recommendation:** (a).
**Approval requested:** Yes — option (a).

---

## Final instruction

This is a revised plan only. I am waiting for your review and explicit approval of the decisions in Section M before any implementation begins. No files have been or will be modified until you authorize BUILD mode.

# ChatGPT — Plan Review (Version 2)

The revised plan is substantially better. The storage architecture is now coherent, the separation between external source references and internally persisted datasets is correct, and the scientific-data preservation requirements are appropriately explicit.

However, I would not approve BUILD yet. There is one significant unresolved architectural contradiction in Section D, plus a few implementation details that need tightening.
1. Critical issue: the actual commit point is not project.json
The plan establishes that:
- datasets/manifest.json is the authoritative index of persisted datasets.
- The manifest is loaded whenever a project is opened.
- project.json does not reference the manifest.
- Dataset files and the manifest are written before project.json.
Those decisions have an important consequence.

The successful atomic replacement of manifest.json is the actual commit point for dataset additions.

Consider this sequence:
Operation	Result
Dataset A written	Success
Dataset B written	Success
Manifest written	Success
project.json written	Failure

When the project is reopened, the service finds the manifest and loads A and B.

The datasets have therefore persisted, even though the overall save operation reported failure.

The report recognizes this behavior, but then continues to describe project.json as the overall commit point. Those two statements cannot both be true.

There is a second problem: the proposed Discard behavior.

Suppose the user attempts to save, encounters an error, and chooses Discard when closing the project. The report says that Discard clears runtime state but does not remove persisted files. Because the manifest already references the datasets, they reappear on the next opening.

That means Discard does not actually discard those dataset additions.

This is not necessarily an unacceptable design, but it must be an intentional and clearly defined behavior. I would not silently introduce it into an application that already has Save/Discard/Cancel semantics.
Two reasonable approaches
Preferred
Option A — Make dataset association transactional

Stage the new dataset files and manifest separately. Do not make the new manifest authoritative until the complete save operation has succeeded.

If the metadata save fails, the previous manifest remains authoritative. The staged files can be preserved for recovery without being loaded as associated datasets.

This requires careful coordination with the existing ProjectRepository save operation, particularly its automatic dirty-state clearing.

Benefit: Save and Discard have predictable behavior. An unsuccessful save does not make new datasets appear in the project after reopening.

Option B — Accept partial persistence

Treat the manifest replacement as the dataset commit point. If it succeeds, the dataset additions are persisted, even if the subsequent metadata save fails.

The application must explicitly communicate that partial persistence occurred. Discard cannot promise to undo those additions.

Benefit: Simpler implementation and fewer transaction-management mechanisms.

Cost: Save/Discard behavior becomes less intuitive, and the user must understand that a failed save can still persist some changes.

I recommend Option A. It better preserves the behavior users reasonably expect from the existing project lifecycle.
2. Additional details to resolve
These are smaller than the transaction issue, but should be included in the final implementation plan.
Area	Remaining concern	Recommendation
Dirty state	ProjectRepository.save() already marks metadata clean internally.	Ensure the service can defer that operation until the entire coordinated save succeeds, without duplicating or weakening existing persistence guarantees.
Manifest errors	The plan says the project opens while reporting a corrupted manifest.	Define how the service exposes those errors to its caller. A structured load result or explicit dataset-loading diagnostics would be preferable to silently swallowing exceptions.
Partial dataset loading	Missing or corrupt datasets should not prevent valid datasets from loading.	Define how individual failures are collected and returned alongside successfully loaded datasets.
Path validation	Resolving paths and checking containment is appropriate.	Include symlink considerations so a path inside datasets/ cannot resolve outside the project directory.
Orphan detection	The plan proposes identifying orphan files.	Keep this optional and non-destructive. Do not let orphan scanning become a prerequisite for ordinary project opening or saving.
Test plan	Failed writes are tested, but the important cross-file failure sequence is not fully specified.	Test failures at each save stage, including manifest success followed by metadata-save failure, and verify reopening and Discard behavior.

3. Decisions that look ready
These recommendations are sound and I see no reason to reopen them:
Decision	Assessment
Separate manifest and per-dataset files	Approve
Keep external_data_references for external sources	Approve
Keep project schema v2	Approve
Fixed datasets/manifest.json location	Approve
Individual dataset storage version	Approve
Default Python JSON serialization	Approve provisionally
No automatic orphan deletion	Approve
ProjectService coordinates runtime datasets	Approve
Multiple datasets per project	Approve
No GUI import workflow in 2.2.3	Approve

A note on JSON serialization
Option A is reasonable for this provisional, local-only storage implementation.

The important distinction is that Python can round-trip NaN and infinity using its default JSON behavior, but the resulting files are not strict RFC 8259 JSON. That limitation should be recorded in the development log and revisited when D6 is formally considered.

I would not introduce a more complicated serialization mechanism just to solve a future compatibility concern at this stage.
4. Next step: one focused PLAN revision
I recommend sending OpenCode a short follow-up prompt to resolve the transaction semantics without reopening the entire architectural investigation.
SUBTASK 2.2.3 — FINAL PLAN CLARIFICATION: SAVE TRANSACTION SEMANTICS
MODE: PLAN ONLY
The revised 2.2.3 plan is substantially accepted as an architectural direction. Before BUILD approval, one remaining issue must be resolved: coordinated save semantics between dataset files, the dataset manifest, and project metadata.

Do not implement anything. Do not modify files, tests, or documentation. Do not commit or push.
1. Correct the commit-point inconsistency
The current plan identifies datasets/manifest.json as the authoritative dataset index, loaded directly when a project opens.

However, it also identifies successful project.json replacement as the overall commit point.

These statements conflict.

Because the manifest is independently discovered and loaded, successfully replacing it makes its dataset associations visible on the next project opening, regardless of whether project.json was successfully saved.

Revise the design so that the actual commit point and reopening behavior are unambiguous.
2. Prefer transactional dataset association
Evaluate a staged-save approach:
1. Serialize and validate the datasets.
2. Write new or updated dataset files to temporary/staging locations.
3. Prepare a new manifest without replacing the currently authoritative manifest.
4. Save project metadata without prematurely marking the project clean.
5. Once all required writes succeed, atomically replace the authoritative manifest with the prepared manifest.
6. Mark the project clean only after the coordinated save succeeds.
This is a proposed sequence, not a requirement to implement it exactly.

Check whether it can work with the existing ProjectRepository implementation and its atomic-write behavior.

In particular, inspect how ProjectRepository.save() currently marks metadata clean. Determine the smallest change or coordination mechanism necessary to defer that state transition until the full save succeeds.

Do not weaken existing atomic-write guarantees.
3. Define failure and Discard behavior
Explicitly address these cases:
- Dataset staging fails.
- Manifest preparation fails.
- Project metadata save fails.
- Final manifest replacement fails.
- The application closes after a failed save.
- The user chooses Discard after a failed save.
- The user retries the save.
For every case, explain:
- Which files may exist on disk.
- Which manifest is authoritative.
- Which datasets load when the project is reopened.
- Whether the project remains dirty.
- Whether Discard actually prevents unsaved dataset additions from reappearing.
The intended user-facing behavior should be:

A failed save must not silently make unsaved dataset additions appear as committed project data after reopening.

Orphaned staging files may remain for preservation and later inspection. Do not automatically delete them as part of ordinary saving.

If this guarantee cannot be achieved with a proportionate design, explain why and propose the least risky alternative.
4. Clarify load diagnostics
The previous plan says that corrupted manifests and individual dataset failures should be reported while allowing the project to open.

Define how ProjectService communicates these conditions to its caller.

Consider a structured result containing successfully loaded datasets and a collection of load warnings/errors, or another suitable design compatible with the existing codebase.

Do not silently convert a corrupted manifest into an empty dataset collection.

Also clarify how a caller can distinguish:
- A project with no datasets.
- A project with a missing manifest.
- A project whose manifest is corrupted.
- A project with some successfully loaded datasets and some failed datasets.
5. Tighten path validation
Confirm that path validation accounts for resolved paths and symbolic links, not merely string prefixes.

All internal dataset files must remain confined to the project's dataset storage directory.

Original source-file paths remain provenance metadata and must not be subjected to internal storage-path rules.
6. Add transaction-focused tests
Expand the proposed tests to cover:
- Failure during dataset staging.
- Failure during manifest preparation.
- Failure during project metadata save.
- Failure during final manifest replacement.
- Previous manifest remains authoritative when the coordinated save fails.
- Reopening after a failed save.
- Discard after a failed save.
- Retry after a failed save.
- Dirty state remains correct throughout.
- No uncommitted dataset association becomes visible after reopening.
Use failure injection or mocks where appropriate rather than relying on operating-system permission behavior alone.
7. Required output
Return only the revised sections relevant to:

A. Save consistency and commit point.
B. Failure, retry, and Discard semantics.
C. ProjectService dirty-state coordination.
D. Load diagnostics.
E. Path validation.
F. Additional tests.
G. Remaining risks or approval decisions.

Do not repeat the entire previous report.

Do not begin implementation. Wait for explicit user authorization.




5. Current approval status
My assessment is that the architecture is ready, but the save transaction is not.

I would keep the following distinction:
- Architectural direction: Accepted.
- Serialization choice: Accepted provisionally.
- Implementation authorization: Pending the final transaction clarification.
Once OpenCode returns that clarification, we can review the save lifecycle one last time and produce a precise BUILD approval with a bounded implementation scope.
---

# Planning Version [3]

# ChatGPT — OpenCode Revision Prompt

## SUBTASK 2.2.3 — FINAL PLAN CLARIFICATION: SAVE TRANSACTION SEMANTICS

## MODE: PLAN ONLY

The revised 2.2.3 plan is substantially accepted as an architectural direction. Before BUILD approval, one remaining issue must be resolved: coordinated save semantics between dataset files, the dataset manifest, and project metadata.

Do not implement anything. Do not modify files, tests, or documentation. Do not commit or push.

### 1. Correct the commit-point inconsistency

The current plan identifies `datasets/manifest.json` as the authoritative dataset index, loaded directly when a project opens.

However, it also identifies successful `project.json` replacement as the overall commit point.

These statements conflict.

Because the manifest is independently discovered and loaded, successfully replacing it makes its dataset associations visible on the next project opening, regardless of whether `project.json` was successfully saved.

Revise the design so that the actual commit point and reopening behavior are unambiguous.

### 2. Prefer transactional dataset association

Evaluate a staged-save approach:

1. Serialize and validate the datasets.
2. Write new or updated dataset files to temporary/staging locations.
3. Prepare a new manifest without replacing the currently authoritative manifest.
4. Save project metadata without prematurely marking the project clean.
5. Once all required writes succeed, atomically replace the authoritative manifest with the prepared manifest.
6. Mark the project clean only after the coordinated save succeeds.

This is a proposed sequence, not a requirement to implement it exactly.

Check whether it can work with the existing `ProjectRepository` implementation and its atomic-write behavior.

In particular, inspect how `ProjectRepository.save()` currently marks metadata clean. Determine the smallest change or coordination mechanism necessary to defer that state transition until the full save succeeds.

Do not weaken existing atomic-write guarantees.

### 3. Define failure and Discard behavior

Explicitly address these cases:

- Dataset staging fails.
- Manifest preparation fails.
- Project metadata save fails.
- Final manifest replacement fails.
- The application closes after a failed save.
- The user chooses Discard after a failed save.
- The user retries the save.

For every case, explain:

- Which files may exist on disk.
- Which manifest is authoritative.
- Which datasets load when the project is reopened.
- Whether the project remains dirty.
- Whether Discard actually prevents unsaved dataset additions from reappearing.

The intended user-facing behavior should be:

**A failed save must not silently make unsaved dataset additions appear as committed project data after reopening.**

Orphaned staging files may remain for preservation and later inspection. Do not automatically delete them as part of ordinary saving.

If this guarantee cannot be achieved with a proportionate design, explain why and propose the least risky alternative.

### 4. Clarify load diagnostics

The previous plan says that corrupted manifests and individual dataset failures should be reported while allowing the project to open.

Define how `ProjectService` communicates these conditions to its caller.

Consider a structured result containing successfully loaded datasets and a collection of load warnings/errors, or another suitable design compatible with the existing codebase.

Do not silently convert a corrupted manifest into an empty dataset collection.

Also clarify how a caller can distinguish:
- A project with no datasets.
- A project with a missing manifest.
- A project whose manifest is corrupted.
- A project with some successfully loaded datasets and some failed datasets.

### 5. Tighten path validation

Confirm that path validation accounts for resolved paths and symbolic links, not merely string prefixes.

All internal dataset files must remain confined to the project's dataset storage directory.

Original source-file paths remain provenance metadata and must not be subjected to internal storage-path rules.

### 6. Add transaction-focused tests

Expand the proposed tests to cover:

- Failure during dataset staging.
- Failure during manifest preparation.
- Failure during project metadata save.
- Failure during final manifest replacement.
- Previous manifest remains authoritative when the coordinated save fails.
- Reopening after a failed save.
- Discard after a failed save.
- Retry after a failed save.
- Dirty state remains correct throughout.
- No uncommitted dataset association becomes visible after reopening.

Use failure injection or mocks where appropriate rather than relying on operating-system permission behavior alone.

### 7. Required output

Return only the revised sections relevant to:

A. Save consistency and commit point.  
B. Failure, retry, and Discard semantics.  
C. ProjectService dirty-state coordination.  
D. Load diagnostics.  
E. Path validation.  
F. Additional tests.  
G. Remaining risks or approval decisions.

Do not repeat the entire previous report.

Do not begin implementation. Wait for explicit user authorization.

# OpenCode — Revised Plan (Version 3)

[Paste complete OpenCode response.]

# ChatGPT — Plan Review (Version 3)

[Paste complete ChatGPT review.]

---

# Planning Version [N]

# ChatGPT — OpenCode Revision Prompt

[Paste complete ChatGPT prompt.]

# OpenCode — Revised Plan (Version N)

[Paste complete OpenCode response.]

# ChatGPT — Plan Review (Version N)

[Paste complete ChatGPT review.]

---

# Planning Version [N]

# ChatGPT — OpenCode Revision Prompt

[Paste complete ChatGPT prompt.]

# OpenCode — Revised Plan (Version N)

[Paste complete OpenCode response.]

# ChatGPT — Plan Review (Version N)

[Paste complete ChatGPT review.]

---

# Planning Version [N]

# ChatGPT — OpenCode Revision Prompt

[Paste complete ChatGPT prompt.]

# OpenCode — Revised Plan (Version N)

[Paste complete OpenCode response.]

# ChatGPT — Plan Review (Version N)

[Paste complete ChatGPT review.]

---


# 3. Build Phase

# Build 1

# ChatGPT — OpenCode Build Prompt

[Paste complete ChatGPT prompt.]

# OpenCode — Build Response (Build 1)

[Paste complete OpenCode response.]

# ChatGPT — Build Review (Build 1)

[Paste complete ChatGPT review.]

---

# Build [N]

# ChatGPT — OpenCode Build Prompt

[Paste complete ChatGPT prompt.]

# OpenCode — Build Response (Build N)

[Paste complete OpenCode response.]

# ChatGPT — Build Review (Build N)

[Paste complete ChatGPT review.]

---

# 4. Additional Discussions

# Discussion 1

# ChatGPT

[Paste complete message.]

# OpenCode

[Paste complete response, if applicable.]

---

# Discussion [N]

# ChatGPT

[Paste complete message.]

# OpenCode

[Paste complete response, if applicable.]

---

# 5. Final Review

# ChatGPT — Final Task Review

[Paste complete final review.]

---