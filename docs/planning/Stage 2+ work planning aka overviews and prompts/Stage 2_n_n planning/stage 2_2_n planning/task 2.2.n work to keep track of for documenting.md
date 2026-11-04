**# PROGRESS TRACKING. UPDATE AS WE GO**

We'll maintain a running implementation record for Subtask 2.2, then use it as the source material for the consolidated documentation update in 2.2.4.

The important thing is to record verified implementation details, not just a summary saying a task is complete.

**### Running record — Subtask 2.2**

**2.2.1 — FITS inspection and data-model design**

<badge color="success">Complete</badge>

Implemented

- Created `src/light_curve.py`.
- Created `tests/test_light_curve.py`.
- Implemented the seven model components, structural validation, array ownership, calculated properties, and serialization.
- Focused tests: 48 passed.
- Full suite at completion: 224 passed (baseline 176).
- No existing files modified; no commits or pushes.
- No FITS importer, persistence, or project integration implemented in this subtask.

Important implementation details

- Scientific data model is independent of project metadata and persistence.
- Time and measurement arrays use float64; quality flags and cadence numbers use integer arrays.
- Non-finite scientific values are preserved rather than automatically filtered.
- Incoming arrays are copied during dataset construction.
- `to_dict()` and `from_dict()` provide JSON-compatible conversion and reconstruction, but do not perform persistence.

**2.2.2 — FITS importer**

<badge color="success">Complete</badge>

Implemented

- Implemented `src/fits_importer.py` using Astropy, NumPy, and the existing light-curve model.
- Expanded `tests/test_fits_importer.py`.
- Modified only:
  - `src/fits_importer.py`
  - `tests/test_fits_importer.py`
  - `docs/development/DEVELOPMENT_LOG.md`
- No changes to `src/light_curve.py`.
- No new dependencies were introduced.
- No GUI, persistence, project, or database integration was added.
- No commits or pushes.

Important implementation details

- Public interface: `import_light_curve(file_path) -> LightCurveDataset`.
- FITS files are opened read-only and handled through a context manager.
- The importer searches HDUs for a suitable light-curve table rather than assuming a fixed HDU index.
- A suitable table must contain `TIME` and at least one supported flux column: `SAP_FLUX` or `PDCSAP_FLUX`.
- A `LIGHTCURVE` HDU is preferred when multiple candidates exist; ambiguity is reported.
- Duplicate supported column names are detected using the original FITS column definitions before name-based data access.
- Column metadata is resolved by column name rather than hardcoded column positions.
- Both `SAP_FLUX` and `PDCSAP_FLUX` are preserved independently when present.
- Matching uncertainty columns are imported when available. Flux and uncertainty units must be compatible under the approved unit rules.
- Source metadata is taken from the primary header when available, with selected-extension fallback. `ORIGIN` is not treated as an archive identifier.
- Time metadata is mapped from the selected extension header:
  - `TIMEUNIT` → time unit.
  - TIME column `TUNITn` → descriptive time reference.
  - `TIMESYS` → time scale.
  - `TIMEREF` → time reference frame.
  - `BJDREFI` and `BJDREFF` → combined reference value.
  - `TSTART` and `TSTOP` → start and stop.
  - `TIMEDEL` is not currently mapped.
- No time-system or time-coordinate conversion is performed.
- Floating-point scientific data is converted to float64. Integer quality and cadence data is converted to int64 after validation.
- Integer overflow is checked before conversion.
- Non-finite values are preserved. They are reported through validation findings rather than silently removed.
- Nonzero quality flags are preserved and reported as informational findings.
- Missing metadata, missing uncertainty columns, orphan uncertainty columns, and limited available flux types are handled according to the approved warning/information rules.
- No observations are automatically filtered or reordered.

Testing and verification

- FITS importer tests: 60 passed.
- Combined non-GUI test run:
  `python -m pytest tests/test_light_curve.py tests/test_fits_importer.py tests/test_project_model.py tests/test_project_repository.py tests/test_project_service.py tests/test_project_discovery.py tests/test_project_status.py -q`
- Result: **233 passed, 0 failed**.
- Total collected tests: 284.
- The remaining 51 tests are GUI tests that cannot run in the current headless environment because of PySide6 display/QPA requirements. This limitation existed before 2.2.2; those tests were not modified.
- Controlled temporary FITS fixtures were used for importer verification.
- The real Kepler FITS file was not independently imported during this subtask because real-file verification was gated on file availability.

Known limitations and deferred work

- `TIMEDEL` mapping remains deferred.
- Project association and persistence are not part of the importer and remain assigned to 2.2.3.
- Broader documentation consolidation remains assigned to 2.2.4.
- GUI test execution in a headless/background environment remains a broader testing issue for later review.

**2.2.3 — Project association and persistence**

<badge color="warning">Pending</badge>

Record:

- How datasets associate with projects.
- Where data is stored under the provisional storage approach.
- How dataset identity and project ownership are represented.
- Save, close, reopen, and reload behavior.
- Source-file references and provenance.
- Compatibility with project metadata schema v2.
- How existing project functionality interacts with imported light-curve datasets.
- Error handling for missing, moved, or unavailable source files.
- Tests and actual test results.
- Any changes to existing project models, repositories, services, or database structures.

Do not assume the final D6 storage architecture is being established by this subtask.

**2.2.4 — Testing, documentation, and completion**

<badge color="warning">Pending</badge>

Consolidate implementation records, verify all three subtasks, run regression tests, update the relevant documentation, and report remaining limitations.

Include:

- Review of the 2.2.1, 2.2.2, and 2.2.3 implementation records.
- Verification that the implementation matches the approved designs.
- Review of tests and test coverage, including the GUI test execution limitation.
- Review of unresolved questions and deferred work.
- Consolidation of relevant development documentation.
- Confirmation that provisional storage decisions are not documented as permanent D6 architecture.

**### How we'll maintain it**

At the end of each implementation task, we'll capture:

1. Files created, modified, or deleted.
2. Actual functionality implemented.
3. Important technical decisions and their reasoning.
4. Test commands and exact results.
5. Deviations from the approved plan.
6. Known limitations and unresolved questions.
7. Explicitly deferred work.

I'll also distinguish verified facts from assumptions so we don't accidentally document intended behavior as implemented behavior.

One important constraint will remain visible throughout: D6's permanent storage architecture is deferred. We should document any provisional storage decisions without accidentally presenting them as final architecture.

We can carry this record forward through 2.2.3, then use it for the consolidated documentation pass in 2.2.4.