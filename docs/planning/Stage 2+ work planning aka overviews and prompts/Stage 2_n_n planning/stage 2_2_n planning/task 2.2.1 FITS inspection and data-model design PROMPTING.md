# *REVISED* PLAN MODE PROMPT

The existing PLAN prompt has a good foundation. I would revise and tighten it rather than replace its overall structure.

I found several things that need correcting before sending it to OpenCode.

## What needs to change

| Area                    | Required adjustment                                                                                                  |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Test baseline           | The prompt references 135 passing tests. The latest reported result is now 176 passing tests.                        |
| Repository instructions | Add `docs/README.md` and explicitly require checking the current roadmap, development log, and unresolved questions. |
| D4 implementation       | Account for the completed schema version 2 and permission-aware project metadata.                                    |
| D6 storage decision     | Explicitly preserve the deferred permanent storage decision and provisional local-file direction.                    |
| FITS inspection         | Distinguish read-only inspection of the actual FITS file from implementing a reusable FITS importer.                 |
| Data model              | Require a concrete proposed model, including field types, ownership, relationships, and validation responsibilities. |
| Scientific integrity    | Give more attention to time conventions, units, uncertainties, quality flags, and preserving original measurements.  |
| Subtask boundaries      | Make sure 2.2.1 does not absorb implementation work assigned to 2.2.2 or 2.2.3.                                      |

There is also an important distinction in the existing documents:

- 2.2.1 must inspect the actual FITS file to understand what the data model needs to represent.
- 2.2.2 implements the reusable FITS-reading and extraction functionality.

Those are different responsibilities. The revised prompt will make that explicit.

## Revised PLAN prompt

The following replaces only the PLAN section at the top of `PROMPTING.md`.

The existing BUILD section remains untouched. We will revisit it after reviewing OpenCode's findings and approving the design.

# PLAN MODE PROMPT

# Subtask 2.2.1 — FITS Inspection and Data-Model Design

## Mode: PLAN ONLY

Inspect the actual repository, examine the selected astronomical FITS dataset, and develop a technically and scientifically justified design for the application's internal light-curve data model.

**Do not implement anything. Do not modify, create, delete, or overwrite files.**

This task establishes the scientific data representation that will support the remaining Subtask 2.2 work.

The objective is to determine what the application needs to represent, how that representation should fit into the existing architecture, and what implementation should be authorized in the subsequent BUILD task.

FITS import implementation, project integration, and scientific dataset persistence belong to later subtasks.

---

## 1. Project Context

**Repository:**

`C:\Code\New_Project`

**GitHub:**

`https://github.com/brettadin/New_Project`

The application is a local desktop astronomy research application.

The approved technology stack is documented in `DEC-006` and includes:

- Python 3.13
- PySide6
- NumPy
- SciPy
- Astropy
- Matplotlib (QtAgg)
- pytest

Verify the actual environment and current implementation rather than assuming every listed dependency or capability is already present.

### 1.1 Existing application functionality

The application has completed Stage 2, Task 2.1, covering:

- Project creation.
- Project discovery and opening.
- Project saving and closing.
- Unsaved-change tracking.
- Project lifecycle statuses.
- Project metadata persistence.
- Permission-aware project metadata under DEC-003.

The D4 / DEC-003 implementation is complete.

The project metadata schema is now version 2 and includes:

- `owner`
- `roles`
- Existing project metadata and lifecycle information.

The latest reported full test-suite result is:

**176 passed, 0 failed.**

Environment reported:

- Python 3.13.9
- pytest 9.2.0
- Existing project `.venv`

These are the latest reported results, not a substitute for inspecting the actual current repository.

The working tree may contain uncommitted D4 changes. Preserve all existing modifications. Do not reset, revert, stash, overwrite, or discard them.

### 1.2 Current development objective

The next objective is:

**Stage 2.2 — Light-Curve Dataset Import**

The overall objective is to establish a workflow that can import real astronomical light-curve observations, preserve their scientific context and provenance, and make them available for subsequent visualization and analysis.

Subtask 2.2.1 establishes the data-model foundation for that workflow.

---

## 2. Governing Instructions and Required Reading

Before beginning the investigation:

### 2.1 Project instructions

1. Read the root `AGENTS.md` completely.
2. Read `docs/README.md`.
3. Read `docs/MASTER_DEVELOPMENT_ROADMAP.md`.
4. Read `docs/development/DEVELOPMENT_LOG.md`.
5. Read `docs/development/UNRESOLVED_QUESTIONS.md`.
6. Inspect relevant decision records in `docs/development/decisions/`.
7. Read the complete parent document:

   `subtask-2.2-light-curve-import OVERVIEW.md`
8. Read the complete task overview:

   `task 2.2.1 FITS inspection and data-model design OVERVIEW.md`
9. Inspect the existing planning and BUILD prompts for consistency with the approved task boundaries.

Follow the repository's actual instructions and approval requirements.

Do not assume that the supplied repository snapshot or previous conversational reports represent the current working tree.

### 2.2 Relevant approved decisions

Pay particular attention to:

- DEC-001 — Initial photometry and time-series capability.
- DEC-002 — Initial application scope.
- DEC-003 — Single-user local deployment and permission-aware project metadata.
- DEC-005 — Initial BLS analytical operation.
- DEC-006 — Approved technology stack.

Also investigate the current documented position of **D6 — Data Storage Model**.

The existing development records describe D6 as follows:

- Permanent storage architecture is deferred.
- A provisional local-file approach is permitted for the first working scientific vertical slice.
- The data model should not be unnecessarily coupled to a particular permanent storage architecture.

Verify the current authoritative records rather than assuming that this description has not changed.

### 2.3 Foundation requirements

Read:

`docs/Foundation/0_index.md`

Then consult the relevant section overviews and detailed documents.

Prioritize:

**Scientific capabilities**

- Section 3.0 — Core Scientific Capabilities and Research Workflows.
- Section 3.2 — Observational Data Examination and Preparation.
- Section 3.4 — Photometry, Transits and Time-Series Analysis.

**Scientific data and provenance**

- Section 4.0 — Data Discovery, Databases and External Resources.
- Section 4.4 — Scientific Data Types, Formats and Standards.
- Section 4.5 — Data Retrieval, Import and Acquisition.
- Section 4.6 — Data Lineage, Processing History and Traceability.
- Section 4.7 — Data Provenance, Metadata and Source Attribution.
- Section 4.8 — Data Quality, Reliability and Availability.

**Scientific integrity**

- Section 5.0 — Scientific Integrity, Automation and Analysis Control.
- Section 5.1 — Scientific Integrity and Reliability.
- Section 5.3 — Data Processing and Transformation Safeguards.
- Section 5.4 — Scientific Interpretation and Uncertainty.
- Section 5.6 — Validation, Error Detection and Quality Control.

**Architecture and storage**

- Section 9.0 — Platform, Architecture, Portability and Offline Use.
- Section 9.2 — System Architecture and Technical Structure.
- Section 9.4 — Data Storage and Management Infrastructure.
- Section 9.7 — Portability, Interoperability and Data Ownership.

**Development and approval**

- Section 10.0 — AI Development Partner Responsibilities and Autonomy.
- Section 10.4 — Technical and Architectural Decision-Making.
- Section 10.6 — Testing, Verification and Quality Assurance.
- Section 10.9 — User Oversight, Approval and Communication.
- Section 11.0 — Knowledge Management, Project Records and Continuity.
- Section 11.3 — Authoritative Records and Sources of Truth.
- Section 11.5 — Documentation Maintenance and Change Management.
- Section 12.0 — Initial Research Phase, Planning and Implementation Boundaries.
- Section 12.6 — Development Planning and Implementation Readiness.
- Section 12.7 — Transition from Research to Implementation.

Consult additional detailed documents where the index or initial investigation identifies a relevant requirement.

Foundation documents are authoritative and read-only.

Cite the original relative document paths and relevant headings when relying on Foundation requirements.

Do not modify Foundation documents.

---

## 3. Selected Scientific Dataset

The initial target is the existing Kepler-10b FITS dataset.

**Local path:**

`C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits`

**Filename:**

`kplr011904151-2009131105131_llc_full.fits`

The file is outside the repository and is intended to remain outside the repository.

It must be treated as read-only.

Do not move, rename, overwrite, modify, or delete it.

Previously established information includes:

- FITS format.
- Kepler long-cadence photometry.
- Approximately 9.7 days of observations.
- Approximately 476 observation rows.
- `TIME` values using the BKJD time reference and TDB time system.
- `SAP_FLUX` and `PDCSAP_FLUX` measurement columns.
- Corresponding uncertainty columns.
- `SAP_QUALITY` quality flags.
- `CADENCENO` cadence identifiers.
- Approximately four missing flux measurements.
- Approximately 37 observations with nonzero quality flags.

These are prior findings, not verified facts for this investigation.

Verify them against the actual file.

If the file cannot be accessed:

- Report the limitation.
- Identify which aspects of the investigation cannot be completed.
- Do not substitute another dataset.
- Do not use synthetic data as a replacement for actual dataset inspection.

### Important distinction

This task permits **read-only exploratory inspection** of the actual FITS file using Astropy.

It does not authorize implementing a reusable FITS reader, importer, extraction workflow, or import interface.

The distinction is:

- 2.2.1: Inspect the file to understand the scientific structure and design the model.
- 2.2.2: Implement the functionality that reads FITS files and extracts measurements into the approved model.

---

## 4. Investigation A — Actual FITS Structure

Inspect the actual Kepler-10b FITS file using Astropy.

Determine and report:

1. Number of HDUs.
2. Purpose of each HDU.
3. Which HDU contains the relevant light-curve measurements.
4. Table structure and available columns.
5. Column names, data types, dimensions, and shapes.
6. Column units.
7. Relevant primary and extension header metadata.
8. Time reference and time system.
9. Time units and relevant timing keywords.
10. Available uncertainty information.
11. Available data-quality information.
12. Observation identifiers and cadence information.
13. Missing, non-finite, or unusual values.
14. Any relationships between columns that affect scientific interpretation.

Pay particular attention to:

- `TIME`
- `SAP_FLUX`
- `PDCSAP_FLUX`
- `SAP_FLUX_ERR`
- `PDCSAP_FLUX_ERR`
- `SAP_QUALITY`
- `CADENCENO`

Explain the distinction between the two flux measurement types.

Do not treat `SAP_FLUX` and `PDCSAP_FLUX` as interchangeable.

Identify which properties are specific to the Kepler dataset and which represent more general astronomical light-curve concepts.

Do not perform transit detection, BLS analysis, normalization, detrending, or other scientific processing.

The objective is understanding the data, not interpreting its astronomical signals.

---

## 5. Investigation B — Proposed Light-Curve Data Model

Examine the existing application architecture and develop a concrete proposed internal data model.

The model should represent astronomical light-curve observations without unnecessarily depending on the structure of the initial Kepler file.

Do not immediately jump to implementation.

First establish what information the application needs to preserve and how the information relates to other parts of the application.

### A. Dataset identity and source information

Determine how the model should represent:

- Dataset identity.
- Original filename.
- Original source-file path.
- Source identifier, if available.
- Archive or originating resource.
- Target object or observation identifier, where available.
- Instrument and mission information.
- Import date/time.
- Relevant source metadata.
- Source-file availability.

Consider whether a file checksum or another source-identification mechanism would provide useful provenance.

Distinguish source-file identification from complete scientific provenance.

Consider whether source-file availability should be stored as metadata or determined dynamically when needed.

### B. Measurement representation

Determine how the model should represent:

- Observation timestamps.
- Flux measurements.
- Flux uncertainties.
- Cadence numbers or other observation identifiers.
- Data-quality flags.
- Missing measurements.
- Invalid or non-finite values.
- Measurement-column identities.
- The selected measurement series for subsequent analysis.

Consider whether measurements should be represented as:

- Separate aligned arrays.
- A structured measurement-series object.
- A table-like representation.
- Another justified structure.

Evaluate the advantages and disadvantages of the alternatives against the existing application architecture and scientific requirements.

For the initial Kepler dataset, `SAP_FLUX` and `PDCSAP_FLUX` must remain independently identifiable and accessible.

Consider how the corresponding uncertainty columns should remain associated with their respective measurement columns.

Do not assume that every astronomical dataset contains flux measurements or uses the same column names.

### C. Time representation

Give particular attention to time representation.

The model must not reduce timestamps to generic floating-point values without preserving their interpretation.

Determine how to represent:

- Original timestamp values.
- Time units.
- Time reference or epoch.
- Time system or scale.
- Relevant offsets and reference conventions.
- Any additional timing metadata required to interpret observations correctly.

Consider the distinction between:

- A numerical time value.
- The unit associated with that value.
- Its reference epoch.
- Its time scale.

Investigate whether Astropy time-related structures are appropriate for the model or whether another representation is preferable.

Consider the consequences for later BLS analysis and other time-series operations.

Do not silently convert time values or assume a time convention when metadata is missing.

### D. Scientific units and measurement metadata

Determine how to represent:

- Measurement units.
- Uncertainty units.
- Time units.
- Original FITS column names.
- Column descriptions.
- Instrument and mission metadata.
- Observation cadence.
- Relevant header metadata.
- Relationships between measurement and uncertainty columns.

Consider whether Astropy `Quantity` objects, unit strings, or another representation is appropriate.

Evaluate the implications for:

- Serialization.
- Future persistence.
- Numerical computation.
- Interoperability.
- Unknown or missing units.

Do not introduce assumptions about units that are not supported by the source data.

### E. Validation and warnings

Determine how the model should represent validation findings.

Consider:

- Missing required information.
- Missing optional information.
- Non-finite measurements.
- Invalid timestamps.
- Missing uncertainties.
- Nonzero quality flags.
- Unsupported metadata.
- Ambiguous units or time conventions.
- Unexpected measurement structures.
- Inconsistent array lengths.

Distinguish between:

1. Conditions that should prevent a dataset from being accepted.
2. Conditions that permit representation but generate warnings.
3. Conditions that should be preserved without modifying the original measurements.

Consider how validation findings should be structured so that later import functionality can report them consistently.

Distinguish model-level structural validation from FITS-file inspection and import validation.

Do not design the model so that constructing it automatically removes observations or performs scientific processing.

In particular, nonzero quality flags must remain available.

Do not assume all nonzero quality flags should cause observations to be discarded.

### F. Original and derived measurements

Establish how the model should distinguish:

1. Original source measurements.
2. Imported representations of source measurements.
3. Future derived or transformed measurements.

Consider what relationships or metadata will eventually be required to trace derived measurements back to their source.

Normalization, filtering, detrending, quality filtering, interpolation, and other processing operations must not silently overwrite original measurements.

Do not implement processing functionality.

---

## 6. Investigation C — Existing Architecture and Integration

Inspect the actual application architecture.

At minimum, examine:

- `src/project_model.py`
- `src/project_repository.py`
- `src/project_service.py`
- Existing UI modules relevant to project lifecycle.
- Existing data-related modules.
- Existing model and service tests.
- Existing architecture and data-model documentation.

Identify any existing dataset, file-reference, or project-association mechanisms.

Determine:

1. Which existing modules could reasonably own the scientific dataset model.
2. Whether a new module is justified.
3. Whether separate structures are needed for dataset identity, measurements, metadata, and validation.
4. How scientific datasets should relate to projects.
5. Whether the current project model provides an appropriate relationship mechanism.
6. Which existing interfaces should be reused.
7. Whether the proposed model creates unnecessary coupling.
8. Whether any existing architecture should be extended rather than replaced.

### Important architectural boundaries

Preserve the conceptual distinction between:

- Project metadata.
- Scientific datasets.
- Measurement data.
- Source-file references.
- Scientific metadata.
- Validation findings.
- Future analysis results.

The project metadata model already has its own responsibilities, including the schema version 2 and DEC-003 ownership/roles fields.

Do not propose placing large scientific measurement arrays directly into `ProjectMetadata` without a compelling architectural justification.

Do not duplicate project ownership or permission metadata inside the scientific dataset model.

The application remains a single-user local deployment under DEC-003.

Do not introduce authentication, collaboration, or multi-user infrastructure.

Explain how the proposed design fits the existing module-responsibility boundaries.

---

## 7. Investigation D — Storage and Persistence Boundaries

D6 deferred the permanent storage architecture.

The current approved direction permits provisional local-file persistence for the first scientific vertical slice without establishing a permanent storage architecture.

For this task, determine:

1. What information the scientific data model needs to represent independently of storage.
2. Which information must eventually survive project save and reopen.
3. What the next task will need from the model to support provisional persistence.
4. The implications of referencing an external source file.
5. The implications of copying scientific data into a project.
6. The risks of relying on external file paths.
7. Whether the proposed data model can be serialized without losing scientific meaning.
8. Which aspects of persistence should remain outside the model.

Do not:

- Make a permanent storage architecture decision.
- Introduce a database.
- Design a complete persistence subsystem.
- Implement file copying.
- Modify the existing project repository.
- Expand the scope into project integration.

Identify any storage-related decision that requires further approval.

The data model should remain appropriately independent of its eventual storage mechanism.

---

## 8. Investigation E — Future Compatibility

The initial implementation targets the selected Kepler FITS dataset.

The general scientific data model should not become unnecessarily dependent on Kepler-specific assumptions.

Consider future compatibility with:

- FITS light curves from other missions.
- Different measurement columns.
- Different time conventions.
- Different flux, intensity, or other measurement units.
- Different uncertainty representations.
- Different data-quality systems.
- Additional photometric datasets.
- Different observation cadences.

Explain which elements should be generic and which can reasonably remain specific to the initial Kepler implementation.

Consider future compatibility with later visualization and BLS analysis.

In particular, the model should preserve the information needed for subsequent time-series analysis without implementing those operations now.

Avoid designing a universal astronomy data framework.

The objective is an appropriately extensible first scientific data model, not an abstract framework for every possible astronomical observation.

---

## 9. Required Deliverable — Proposed Design

Produce a structured planning report.

### 1. Repository and architecture findings

Include:

- Actual repository state.
- Relevant files inspected.
- Existing models and interfaces.
- Existing functionality that can be reused.
- Relevant architectural boundaries.
- Existing documentation.
- Missing or incomplete documentation.
- Current Git working-tree state.
- Verified test baseline, if established.

Distinguish current implementation from documented future requirements.

### 2. Actual FITS inspection results

Include:

- HDU structure.
- Relevant headers.
- Column names.
- Column data types and shapes.
- Units.
- Time conventions.
- Uncertainty information.
- Quality flags.
- Missing or unusual measurements.
- Differences from previously recorded dataset information.

Identify which findings were directly verified against the actual file.

### 3. Proposed data model

Provide a concrete model proposal.

For each proposed class or structure, specify:

- Name.
- Responsibility.
- Proposed fields.
- Suggested field types.
- Required versus optional fields.
- Relationships with other structures.
- Validation responsibilities.
- Scientific purpose.

Explain how measurement columns and their uncertainties remain associated.

Explain how timestamps and their interpretation are preserved.

Include a conceptual example or pseudocode if useful.

Do not provide implementation-ready code that implies authorization to modify the repository.

### 4. Data integrity and validation design

Explain:

- Required versus optional scientific information.
- Model-level validation.
- Import-level validation.
- Errors versus warnings.
- Missing and non-finite values.
- Quality-flag preservation.
- Original versus derived measurements.
- Handling of unknown units and time conventions.

### 5. Architecture integration proposal

Identify:

- Proposed module responsibilities.
- Existing modules to reuse.
- Any new modules that are justified.
- Relationship between datasets and projects.
- Separation between scientific data and project metadata.
- Dependencies and coupling concerns.
- Compatibility with the existing project lifecycle.

### 6. Storage implications

Explain what the proposed model requires from future persistence.

Remain within D6's approved boundaries.

Do not select or implement a permanent storage architecture.

### 7. Future compatibility

Explain how the proposed design accommodates future astronomical datasets without unnecessary abstraction.

Identify any Kepler-specific assumptions that should remain in the initial importer rather than the general model.

### 8. Decisions requiring approval

Separate findings into:

- Existing approved decisions.
- Recommendations within existing architectural authority.
- New scientific or architectural decisions requiring my approval.
- Questions that can safely remain deferred.

Do not present recommendations as approved decisions.

### 9. Proposed implementation breakdown

Review the proposed remaining Subtask 2.2 organization:

| Subtask | Intended responsibility                             |
| ------- | --------------------------------------------------- |
| 2.2.2   | FITS import and validation                          |
| 2.2.3   | Project integration and provisional persistence     |
| 2.2.4   | Testing, documentation, and completion verification |

Determine whether these boundaries remain appropriate after examining the actual architecture.

Identify:

- Dependencies.
- Shared interfaces.
- Potential overlap.
- Any necessary changes to task boundaries.

These are proposed boundaries, not immutable requirements.

Explain any recommended changes.

### 10. Testing strategy

Recommend the tests required for the eventual data-model implementation.

Distinguish between:

- Model construction and validation tests.
- Serialization and conversion tests, if appropriate.
- Controlled scientific-data fixtures.
- Tests involving the actual Kepler dataset.
- Future FITS importer tests.
- Project integration tests.

Identify which tests belong specifically to 2.2.1 and which belong to subsequent subtasks.

Do not introduce implementation work from later subtasks into the 2.2.1 scope.

Do not weaken or replace existing tests.

### 11. Documentation impact assessment

Identify which existing documents may require updates during implementation.

Consider:

- Data-model documentation.
- Architecture documentation.
- Module responsibilities.
- Data-flow documentation.
- Validation documentation.
- Testing documentation.
- Development log.
- Master Development Roadmap.

Identify documents that should remain unchanged.

Do not edit any documentation during this Plan task.

---

## 10. Scope Restrictions

This is strictly a PLAN task.

### Permitted

- Read repository files.
- Inspect the actual FITS dataset.
- Use Astropy for read-only exploratory inspection.
- Run read-only inspection commands.
- Examine existing source code and tests.
- Run existing tests if necessary to establish or verify the current baseline.
- Consult Foundation documents.
- Examine existing architectural decisions.
- Produce a proposed design and implementation recommendations.

### Not permitted

- Create, modify, delete, or overwrite source files.
- Create or modify tests.
- Modify documentation.
- Modify Foundation documents.
- Modify project configuration.
- Install or upgrade dependencies.
- Modify the selected FITS dataset.
- Introduce new dependencies.
- Implement a FITS importer.
- Implement project integration.
- Implement scientific dataset persistence.
- Make unapproved architectural or scientific decisions.
- Commit or push changes.

Do not modify the existing PROMPTING.md file.

Do not edit or rewrite its BUILD section.

Do not create additional planning documents.

If a necessary investigation cannot be completed, report the limitation instead of filling the gap with assumptions.

If an architectural or scientific issue requires user approval, identify it clearly.

---

## 11. Final Instruction

Complete the investigation and present the full structured planning report.

Clearly distinguish:

- Verified repository facts.
- Verified FITS inspection findings.
- Existing approved decisions.
- Assumptions.
- Recommendations.
- Unresolved questions.
- Decisions requiring my approval.

The proposed design must be specific enough that it can be reviewed and, once approved, translated into a focused BUILD task.

Do not implement anything.

Do not begin Subtask 2.2.2.

Do not proceed to another Stage 2.2 task.

**Stop after presenting the complete planning report and wait for my review and explicit authorization before any BUILD-mode work.**

## What I deliberately changed

A few decisions in this revision are particularly important:

1\. Time representation receives its own investigation. This is important because BKJD/TDB cannot safely be represented as an unexplained array of floating-point numbers. The model needs to preserve the interpretation of those values.

2\. Measurement series are treated independently. SAP and PDCSAP measurements, including their respective uncertainties, must remain distinguishable.

3\. Validation responsibilities are separated. The data model should be able to represent validation findings, but it should not become the FITS importer or perform import-time processing.

4\. D6 remains protected. We can design a scientifically complete data structure without committing to a permanent database or storage architecture.

5\. D4 is accounted for. The existing project metadata and permission model should remain separate from scientific dataset representation.

6\. The actual repository takes precedence. The latest reported test baseline is 176 passing tests, but OpenCode must verify the current working tree and test results itself.

Next action: Use this revised PLAN section with Nemotron/OpenCode. Once it produces its report, we can review the proposed classes, fields, relationships, and implementation boundaries before touching the BUILD prompt.


# BUILD MODE PROMPT


# Subtask 2.2.1 — FITS Inspection and Light-Curve Data Model

## Mode: BUILD

Implement the approved data-model design for the initial light-curve import workflow.

This Build task is authorized only after the corresponding Plan report has been reviewed and explicitly approved.

**The approved Plan report is the implementation specification. Do not independently expand, reinterpret, or replace its approved design.**

---

## 1. Project Context

Repository:

`C:\Code\New_Project`

GitHub:

https://github.com/brettadin/New_Project

The application is a local desktop astronomy research application using:

- Python 3.13
- PySide6
- NumPy
- SciPy
- Astropy
- Matplotlib (QtAgg)
- pytest

The project already has project lifecycle functionality, including project creation, discovery, opening, saving, closing, dirty-state tracking, and status management.

Stage 2.2 introduces scientific light-curve data import.

The initial scientific dataset is:

`C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits`

This file is outside the repository and must remain unchanged.

---

## 2. Required Preparation

Before implementation:

1. Read the root `AGENTS.md` completely.
2. Review the approved Subtask 2.2.1 Plan report.
3. Review the relevant Foundation requirements identified during planning.
4. Reinspect the current repository state.
5. Review the existing project lifecycle implementation and relevant tests.
6. Verify that the proposed implementation still matches the current codebase.
7. Identify the exact files expected to change.
8. Identify documentation that will need updating under the project's documentation-maintenance requirements.
9. Confirm that all implementation decisions have already been approved.

Do not rely solely on an earlier repository snapshot or the Plan report if the current code has changed.

If the approved Plan report is unavailable, or if an unresolved architectural or scientific decision prevents implementation, stop and report the issue.

Do not silently make a new decision on the user's behalf.

---

## 3. Implementation Scope

Implement only the approved light-curve data-model design.

The implementation should establish a clear representation of an imported astronomical light-curve dataset, including the approved structures for:

### A. Source information

As specified by the approved Plan, support appropriate representation of:

- Original source-file path.
- Original filename.
- Source identifier, when available.
- Source information, when available.
- Import date/time, if approved.
- Source-file availability information, if approved.

Do not claim that storing a source path provides complete scientific provenance.

### B. Measurement data

Implement the approved representation of:

- Observation timestamps.
- Flux measurements.
- Flux uncertainties.
- Observation identifiers or cadence numbers.
- Data-quality flags.
- Missing or invalid measurements.
- Measurement-column identity.

Preserve the distinction between separate measurement columns.

For the initial Kepler dataset, `SAP_FLUX` and `PDCSAP_FLUX` must remain distinguishable.

Do not merge or treat them as interchangeable.

### C. Scientific metadata

Implement the approved representation of relevant metadata, including where available:

- Measurement units.
- Time units.
- Time reference or epoch.
- Time system or scale.
- Instrument or mission information.
- Observation cadence.
- Original column names.
- Relevant source metadata.

Missing or unknown metadata must not be silently replaced with assumed values.

### D. Validation information

Implement only the validation-related structures approved in the Plan.

The data model should be capable of representing relevant validation findings, such as:

- Missing required information.
- Missing optional information.
- Non-finite values.
- Invalid timestamps.
- Missing uncertainty values.
- Nonzero quality flags.
- Unsupported or ambiguous metadata.

Maintain the distinction between errors and warnings.

Do not introduce automatic filtering or data removal unless explicitly approved.

### E. Original and derived data distinctions

Maintain the approved separation between:

1. Original source measurements.
2. Imported representations of those measurements.
3. Future derived or transformed measurements.

Do not implement normalization, filtering, detrending, quality filtering, or other scientific processing operations as part of this task.

---

## 4. Architecture Requirements

Follow the approved Plan and existing project architecture.

In particular:

- Keep scientific data structures appropriately separated from project metadata.
- Avoid placing large measurement arrays directly inside `ProjectMetadata` unless explicitly approved.
- Maintain appropriate separation between scientific data, UI functionality, and persistence.
- Reuse existing interfaces where appropriate.
- Avoid unnecessary dependencies and abstractions.
- Preserve compatibility with the existing project lifecycle.
- Avoid introducing a permanent storage architecture prematurely.

Do not introduce a database, file-copying system, or new persistence mechanism unless the approved Plan explicitly authorizes it.

Decision D6 remains authoritative unless a subsequent decision has been formally approved.

---

## 5. Data Integrity Requirements

The selected Kepler FITS file is read-only.

Do not:

- Modify the original FITS file.
- Move or rename it.
- Delete it.
- Replace it with a synthetic dataset.
- Silently discard observations.
- Silently modify measurement values.
- Treat missing metadata as known information.
- Conflate different measurement columns.

The data model must preserve the scientific distinctions identified in the approved design.

Do not claim that the implementation provides complete data provenance or reproducibility if those capabilities have not yet been implemented.

---

## 6. Testing Requirements

Create or update automated tests according to the approved Plan.

Testing should cover the implemented data model and its validation behavior.

Where applicable, test:

- Valid data-model construction.
- Required and optional fields.
- Missing metadata.
- Measurement-column distinctions.
- Uncertainty representation.
- Quality-flag representation.
- Missing and non-finite values.
- Validation errors and warnings.
- Preservation of source information.
- Appropriate handling of unknown units and time conventions.
- Any approved serialization or conversion behavior.

Use controlled test fixtures where appropriate.

Do not weaken existing tests, remove assertions, or substitute synthetic data for real scientific observations in the application workflow.

Do not introduce tests for functionality that belongs to later subtasks merely to make this task appear more complete.

Run the relevant targeted tests and the complete test suite.

Report actual results, including failures.

---

## 7. Documentation Requirements

Follow the documentation-maintenance requirements in `AGENTS.md`.

Update relevant documentation when the implementation changes:

- Data models.
- Module responsibilities.
- Interfaces.
- Architecture.
- Validation behavior.
- Testing strategy.
- Development progress.

Likely affected documentation should have been identified during Plan mode.

Do not modify Foundation documents.

Do not make unrelated roadmap or documentation changes.

Before completion, compare the final documentation against the actual source code and tests.

Report:

- Documents changed.
- Documents reviewed but intentionally unchanged.
- Any documentation gaps that remain.

---

## 8. Explicitly Excluded Work

The following work belongs to later subtasks and is not authorized here:

### Subtask 2.2.2 — FITS Import and Validation

Do not implement:

- A complete FITS file importer.
- File-selection UI.
- FITS parsing workflows.
- Import dialogs.
- Full dataset extraction from the selected file.
- User-facing import workflows.

### Subtask 2.2.3 — Project Integration and Provisional Persistence

Do not implement:

- Full project association workflows.
- Dataset persistence.
- Database changes.
- Project save/reopen integration for scientific datasets.
- Permanent storage architecture.

### Subtask 2.2.4 — Testing and Completion Verification

Do not attempt to complete the entire Stage 2.2 testing and verification milestone here.

Only create and run tests necessary for the approved data-model implementation.

### Later stages

Do not implement:

- Data tables.
- Light-curve visualization.
- BLS analysis.
- Scientific processing operations.
- Analysis history.
- Analysis replay.
- External archive integration.

---

## 9. Scope and Change Control

Implement only the approved design.

If implementation reveals:

- An architectural conflict.
- An inconsistency with Foundation requirements.
- An unsupported assumption.
- A need for an additional dependency.
- A new scientific or data-model decision.
- A significant change to the approved scope.

Stop the affected work and report the issue.

Do not silently expand the implementation or make unapproved architectural decisions.

Preserve all existing functionality.

Do not perform unrelated refactoring.

Do not commit, push, reset, clean, or otherwise modify Git history.

---

## 10. Final Verification and Report

After implementation:

1. Review every modified source file.
2. Review every modified test.
3. Run the relevant targeted tests.
4. Run the complete test suite.
5. Report actual test results.
6. Confirm that the original Kepler FITS file remains unchanged.
7. Confirm that no excluded functionality was implemented.
8. Compare documentation against the resulting implementation.
9. Identify any unresolved issues or deferred work.

Provide a final report containing:

### A. Implementation summary
What was implemented and why.

### B. Files changed
List every created, modified, or deleted file and explain its purpose.

### C. Data-model summary
Explain the resulting model and its major fields and relationships.

### D. Testing results
Provide actual commands and results.

### E. Data-integrity verification
Explain how original measurements and scientific metadata are represented and protected.

### F. Documentation updates
Identify changed and intentionally unchanged documents.

### G. Scope compliance
Confirm whether implementation remained within the approved Plan.

### H. Remaining work
Identify anything intentionally deferred to Subtasks 2.2.2–2.2.4.

---

## 11. Completion Boundary

This task is complete when the approved light-curve data model has been implemented, tested, and documented.

Do not begin Subtask 2.2.2.

Do not proceed to another Stage 2.2 task without separate review and explicit authorization.

Stop after providing the final implementation report.