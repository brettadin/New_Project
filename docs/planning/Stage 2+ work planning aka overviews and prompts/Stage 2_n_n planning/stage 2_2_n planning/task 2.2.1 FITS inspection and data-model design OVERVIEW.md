# Subtask 2.2.1 — FITS Inspection and Data-Model Design

Primary objective: Establish the internal data model that the application will use to represent astronomical light-curve datasets before implementing the FITS importer.

This task creates the foundation for Subtasks 2.2.2–2.2.4.

## 1. Inspect the existing Kepler-10b FITS dataset

Examine the actual file:

`kplr011904151-2009131105131_llc_full.fits`

Using Astropy, inspect:

- Number and purpose of HDUs.
- Relevant FITS headers.
- Available table columns.
- Column names, types, shapes, and units.
- Time reference and time system.
- Flux measurements and uncertainties.
- Quality flags and cadence identifiers.
- Missing or unusual values.

Verify previously established information about the dataset rather than assuming it is correct.

The original FITS file must remain unchanged.

## 2. Design the light-curve data model

Determine how the application should internally represent an imported dataset.

The proposed model should account for:

Source information

- Original file path and filename.
- Source identifier and archive information, where available.
- Relevant source metadata.
- File availability.

Measurement data

- Observation timestamps.
- Flux measurements.
- Measurement uncertainties.
- Cadence identifiers.
- Data-quality flags.
- Missing or invalid measurements.
- Measurement-column identities.

Scientific metadata

- Measurement units.
- Time units.
- Time reference or epoch.
- Time system or scale.
- Instrument and mission information.
- Observation cadence.
- Original column metadata.

Validation information

- Missing required information.
- Missing optional information.
- Non-finite values.
- Invalid timestamps.
- Missing uncertainties.
- Quality flags.
- Unsupported or ambiguous metadata.

The model must distinguish original measurements from future derived or transformed measurements.

## 3. Review existing application architecture

Determine how the new data model should fit into the existing application.

Inspect:

- Existing project models.
- Project services and repositories.
- Existing data-reference functionality.
- Module responsibilities.
- Existing architecture and documentation.

Establish how scientific datasets should relate to project metadata without unnecessarily coupling the two.

Identify which existing modules can be reused and whether new modules are justified.

## 4. Establish storage boundaries

Decision D6 deferred the permanent storage architecture.

Determine what information the data model needs to represent independently of storage.

Identify what must eventually survive project save and reopen, and explain the implications of referencing external files versus copying data into projects.

Do not implement a database or permanent storage architecture in this task.

## 5. Consider future compatibility

The initial implementation targets Kepler FITS data, but the general data model should avoid unnecessary Kepler-specific assumptions.

Consider future compatibility with:

- FITS light curves from other missions.
- Different measurement columns.
- Different time conventions.
- Different measurement units.
- Different uncertainty representations.
- Different quality-flag systems.

Avoid designing an unnecessarily complicated universal astronomy framework.

## 6. Produce an implementation design

The Plan-mode investigation must produce:

1. Repository and architecture findings.
2. Actual FITS inspection results.
3. Proposed data-model classes and fields.
4. Required versus optional information.
5. Validation representation.
6. Architecture integration recommendations.
7. Storage implications.
8. Decisions requiring approval.
9. Testing strategy.
10. Documentation impact assessment.
11. Recommended implementation boundaries for 2.2.2–2.2.4.

The report must distinguish verified findings, assumptions, recommendations, and unresolved decisions.

## 7. Implement the approved design

After the Plan report has been reviewed and explicitly approved:

- Implement the approved data model.
- Add the necessary automated tests.
- Preserve existing functionality.
- Maintain separation between scientific data, project metadata, and UI functionality.
- Avoid implementing FITS import prematurely.
- Update relevant documentation according to `AGENTS.md`.

## 8. Test and verify

Testing should cover:

- Valid data-model construction.
- Required and optional fields.
- Missing metadata.
- Measurement-column distinctions.
- Uncertainty representation.
- Quality-flag representation.
- Missing and non-finite values.
- Validation errors and warnings.
- Source-information preservation.
- Unknown units and time conventions.

Run targeted tests and the complete test suite.

Compare documentation against the resulting code and tests.

## 9. Explicitly excluded work

The following belongs to later tasks:

| Functionality                       | Subtask |
| ----------------------------------- | ------- |
| FITS reading and HDU identification | 2.2.2   |
| Measurement and metadata extraction | 2.2.2   |
| FITS validation                     | 2.2.2   |
| Project association                 | 2.2.3   |
| Scientific dataset persistence      | 2.2.3   |
| Data table and visualization        | 2.3     |
| BLS analysis                        | 2.4     |
| Analysis operation records          | 2.5     |

## Completion checklist

## 2.2.1 expected deliverables

- Inspect the actual Kepler FITS structure.
- Review existing application architecture.
- Design the light-curve data model.
- Define measurement and uncertainty representation.
- Define scientific metadata representation.
- Define validation and warning structures.
- Establish original-versus-derived data distinctions.
- Establish storage boundaries without redesigning persistence.
- Implement the approved data model.
- Add automated tests.
- Update relevant documentation.
- Verify the complete test suite.

Central success criterion: The application has a tested, documented internal representation for astronomical light-curve datasets that can accommodate the Kepler-10b observations and serve as the foundation for the FITS importer in Subtask 2.2.2.

Sequence: Plan review → explicit approval → Build → implementation review → completion verification.