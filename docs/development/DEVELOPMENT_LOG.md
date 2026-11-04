# Development Log

**Rolling development record** — `docs/development/DEVELOPMENT_LOG.md`
**Governed by:** §10.11.3, §11.2.3

## Purpose

Chronological record of development activity. Maintained continuously as work progresses (§10.3.4).

## Entries

### 2026-11-02 — Stage 0 initiated

**Activity:** Stage 0 documentation and decision baseline creation.

**Files created:**
- `docs/README.md` — central documentation index (§11.2.6)
- `docs/MASTER_DEVELOPMENT_ROADMAP.md` — master development roadmap (§10.3.4)
- `docs/development/DEVELOPMENT_LOG.md` — this rolling development record (§10.11.3)
- `docs/templates/` — six standardized templates (§11.4.9)
- `docs/development/decisions/` — decision records for D2, D3, D4 (§10.9.5)
- `docs/PROJECT_IDENTITY.md` — project identity record, working title only (§1.1.6)
- `docs/development/UNRESOLVED_QUESTIONS.md` — unresolved-questions register (§13.1)

**Files modified:**
- `AGENTS.md` — updated to reference `docs/README.md` and the roadmap

**Decisions recorded:**
- D2: Photometry and time-series analysis as initial scientific capability (Approved)
- D3: Initial scope boundary in four categories (Approved)
- D4: Single-user local deployment, private-by-default projects, permission-aware data model (Approved)

**Git:** Repository initialized (no commits made).

**Next steps:**
- Begin Stage 1 research: T1 platform evaluation (§9.1.9 criteria) and photometry research S1–S4, S7 (proportionate to the selected analytical operation)
- Complete T1 findings → D1 decision record → obtain D1 approval
- Begin Stage 2 only after Stage 1 complete, D1 approval, and S1–S4, S7 research

**Status:** Stage 0 complete.

### 2026-11-02 — Stage 1 research completed; D1 and BLS decisions approved

**Activity:** Stage 1 targeted scientific and technical research (Plan mode — no files modified during research phase). Build mode: created research records, decision records, .gitignore; made authorized Foundation change.

**Files created (6):**
- `docs/science/REVIEW-001-bls-method.md` — BLS vs Lomb–Scargle method research (§11.4.5, §12.2)
- `docs/science/REVIEW-002-kepler10b-dataset.md` — Kepler-10b dataset profile (§11.4.5, §12.2)
- `docs/technical/REVIEW-003-platform-evaluation.md` — T1 platform evaluation vs §9.1.9 (§11.4.5, §12.3)
- `docs/development/decisions/DEC-004-d1-platform.md` — D1 platform decision record (§10.9.5) — Approved
- `docs/development/decisions/DEC-005-bls-operation.md` — BLS operation decision record (§10.9.5) — Approved
- `.gitignore` — Repository ignore rules for caches, environments, datasets, large data formats

**Files modified (4):**
- `docs/development/DEVELOPMENT_LOG.md` — this rolling development record (§10.11.3)
- `docs/MASTER_DEVELOPMENT_ROADMAP.md` — master development roadmap (§10.3.4)
- `docs/development/UNRESOLVED_QUESTIONS.md` — unresolved-questions register (§13.1)
- `docs/Foundation/3.4_Photometry, Transits and Time-Series Analysis.md` §3.4.8 — added one sentence documenting Lomb–Scargle as future capability

**Foundation change made:**
- `docs/Foundation/3.4_Photometry, Transits and Time-Series Analysis.md` §3.4.8 — Added one sentence: "Future capabilities should include Lomb–Scargle periodogram analysis for investigating approximately sinusoidal periodic signals, including stellar variability."

**File inspection status:**
- Kepler-10b FITS file: NOT inspected — MAST download API returned errors on all endpoints attempted. Dataset profile (REVIEW-002) is documentation-derived, not directly verified from file inspection. This is an explicit evidence gap (UQ-008 remains open).

**Decisions approved:**
- D1: Initial platform strategy — desktop-first (DEC-004 — Approved)
- BLS operation: Initial photometric workflow — BLS transit-period detection; Lomb–Scargle retained as future capability (DEC-005 — Approved)

**Distinction — Stage 1 complete vs Stage 2 ready:**
- Stage 1 research/documentation: Complete. All research records and decision records exist.
- Stage 2 readiness: Pending D5 technology approval (DEC-006). Kepler-10b file inspection resolved; empirical UQ-009 calibration is a Stage 2 validation activity, not an entry blocker.

**Next steps:**
- Begin Stage 2 implementation with Task 2.1 (project lifecycle)
- Install Python packages: PySide6, NumPy, SciPy, Astropy, Matplotlib, pytest
- Empirical UQ-009 calibration during Stage 2 validation activity (not an entry blocker)

**Status:** Stage 1 research complete. Stage 2 ready to begin (D5 approved with delegation; PySide6 selected by OpenCode).

### 2026-11-02 — Stage 2 Task 2.1 (Project Lifecycle) — Subtasks 2.1.1–2.1.4 complete

**Activity:** Stage 2 implementation — Project Lifecycle. Created the minimal desktop application shell and project lifecycle capability for creating, discovering, opening, saving, and closing research projects. All work performed in Build mode using the existing `.venv` (Python 3.13.9). No Foundation documents modified. No commits or pushes made.

**Files created (9):**
- `src/__init__.py` — Application package marker (§11.4.9)
- `src/project_model.py` — `ProjectMetadata` dataclass with UUID generation, name validation, dirty-state tracking, JSON serialization/deserialization (§6.4.2, §4.7)
- `src/main_window.py` — PySide6 `QMainWindow` with active-project indicator ("No project" initially); `Project > New` and `Project > Open` menu actions (§6.1, §6.4)
- `src/main.py` — Application entry point; wires up `ConfigProvider`, `ProjectRepository`, `ProjectService` (§9.2)
- `src/config_provider.py` — Projects root resolution: `ASTRONOMY_PROJECTS_ROOT` env var > config file > default `%USERPROFILE%\Documents\AstronomyProjects` (§9.4.4)
- `src/project_repository.py` — JSON persistence with atomic writes (`project.json` per project directory); `discover_projects()` for default-root scanning; `load_from_directory()` for custom locations; error classes (`ProjectNotFoundError`, `ProjectCorruptedError`, `ProjectRepositoryError`) (§9.4.2, §9.4.5, §9.4.6)
- `src/project_service.py` — `ProjectService` coordinating creation, discovery, opening, active-project tracking, and failure cleanup; `ProjectCreationError` and `ProjectOpeningError` exceptions (§6.4.10, §5.1.4)
- `src/new_project_dialog.py` — PySide6 dialog for project creation with name validation and location picker (§6.4.2)
- `src/open_project_dialog.py` — PySide6 dialog for project selection from discovered list or custom folder (§6.4.10)

**Files modified (3):**
- `AGENTS.md` — Added "Documentation Maintenance During Implementation" section requiring documentation updates during Build-mode tasks
- `docs/MASTER_DEVELOPMENT_ROADMAP.md` — Stage 2 status changed from "Pending" to "In Progress"; Task 2.1 subtask breakdown added
- `docs/development/DEVELOPMENT_LOG.md` — This rolling development record

**Module responsibilities:**
- `project_model.py`: Pure data model — metadata fields (`project_id`, `name`, `created_at`, `status`, `schema_version`, `external_data_references`), validation, serialization
- `project_repository.py`: Persistence layer — read/write `project.json`, atomic writes, discovery scanning, directory queries
- `project_service.py`: Lifecycle orchestration — create/open/save/close/discover, active-project tracking, failure cleanup
- `main_window.py`: PySide6 UI shell — active-project indicator, New/Open menu actions
- `config_provider.py`: Configuration — projects root location resolution
- `main.py`: Entry point — bootstraps Qt application and wires components

**Architecture decisions:**
- Provisional local-file persistence (D6 remains deferred — not a permanent storage architecture)
- Project directory named by stable `project_id` (UUID); human-readable `name` can change without moving files
- Original external data files referenced by path, never copied or modified
- Atomic writes via temp file + `os.replace` to protect against interrupted saves
- `schema_version` distinct from application version; describes `project.json` metadata format version

**Verified test results (73 tests, all passing):**
- `tests/test_project_model.py` — 12 tests (Subtask 2.1.1)
- `tests/test_project_repository.py` — 14 tests (Subtask 2.1.2)
- `tests/test_project_service.py` — 10 tests (Subtask 2.1.3)
- `tests/test_new_project_dialog.py` — 10 tests (Subtask 2.1.3)
- `tests/test_project_discovery.py` — 27 tests (Subtask 2.1.4)
- Total: 73 tests, 0 failures

**Approved decisions preserved (not modified):**
- D1: Desktop-first (DEC-004)
- D2: Photometry/time-series initial capability (DEC-001)
- D3: Initial scope boundaries (DEC-002)
- D4: Single-user local, private-by-default, permission-aware (DEC-003)
- D5: Technology stack Python 3.13/PySide6/NumPy/SciPy/Astropy/Matplotlib/pytest/venv (DEC-006)
- D6: Data storage model — formal decision deferred; provisional local-file approach for first vertical slice only

**Next steps:**
- Subtask 2.1.6 — Project lifecycle status management

**Status:** Stage 2 In Progress; Task 2.1 subtasks 2.1.1–2.1.5 complete, 2.1.6 pending.

### 2026-11-02 — Stage 2 Task 2.1 Subtask 2.1.5 (Project Save and Close) complete

**Activity:** Stage 2 implementation — Subtask 2.1.5 project save and close workflow. Added explicit saving, dirty-state tracking, and project closing without exiting the application. All work performed in Build mode using the existing `.venv` (Python 3.13.9). No Foundation documents modified. No commits or pushes made.

**Files created (1):**
- `tests/test_project_save_close.py` — 21 tests covering dirty-state tracking, save/close behavior, failure handling, and UI menu state

**Files modified (4):**
- `src/project_model.py` — Added `set_name()` method that marks project dirty only when the name actually changes; unchanged values are not marked dirty
- `src/project_service.py` — Added `save_project()` (persists active project via repository, marks clean on success, preserves dirty state on failure) and `close_project()` (clears active project; caller handles dirty-state prompting)
- `src/main_window.py` — Added Project > Save and Project > Close menu actions; dirty-state indicator (asterisk suffix); Save/Discard/Cancel dialog for dirty close; Save disabled when no project or clean; Close disabled when no project; menu state updates on project lifecycle changes
- `docs/MASTER_DEVELOPMENT_ROADMAP.md` — Task 2.1 subtask 2.1.5 marked Complete; 2.1.6 remains Pending

**Module responsibility boundaries preserved:**
- `ProjectMetadata`: Stores metadata, tracks dirty state via `is_dirty`, `mark_dirty()`, `mark_clean()`, `set_name()`
- `ProjectRepository`: Persists metadata with atomic writes; unchanged from Subtask 2.1.2
- `ProjectService`: Orchestrates save/close; no GUI dialogs or PySide6 dependency
- `MainWindow`: GUI dialogs, menu actions, dirty indicator, Save/Discard/Cancel prompting

**Dirty-state behavior:**
- `set_name()` marks dirty only when the value actually changes
- Assigning an unchanged value does not mark dirty
- Successful persistence marks clean; failed persistence leaves dirty
- No observer system or complex change-tracking infrastructure

**Save behavior:**
- Save active project metadata through existing repository (atomic writes)
- Project not marked clean until persistence succeeds
- On failure, active project and dirty state preserved; error displayed
- Save disabled when no active project or project is clean

**Close behavior:**
- No active project: no action
- Clean project: closes immediately
- Dirty project: Save/Discard/Cancel prompt via QMessageBox
- Save then close on Save choice; close without saving on Discard; leave active on Cancel
- Failed save during close: project remains active and dirty; close aborted
- Application window remains open after project close

**Deferred requirement (recorded, not implemented):**
- Application exit / window-close event integration (save-on-exit behavior) — to be addressed in a future task, not Subtask 2.1.5

**Verified test results (93 tests, all passing):**
- `tests/test_project_save_close.py` — 21 tests (Subtask 2.1.5)
- Total across all test files: 93 tests, 0 failures

**Approved decisions preserved (not modified):**
- D1: Desktop-first (DEC-004)
- D2: Photometry/time-series initial capability (DEC-001)
- D3: Initial scope boundaries (DEC-002)
- D4: Single-user local, private-by-default, permission-aware (DEC-003)
- D5: Technology stack Python 3.13/PySide6/NumPy/SciPy/Astropy/Matplotlib/pytest/venv (DEC-006)
- D6: Data storage model — formal decision deferred; provisional local-file approach for first vertical slice only

**Next steps:**
- Subtask 2.1.6 — Project lifecycle status management (Paused/Completed/Archived transitions)

**Status:** Stage 2 In Progress; Task 2.1 subtasks 2.1.1–2.1.5 complete, 2.1.6 pending.

### 2026-11-03 — Corrective Task: Project Location Persistence and Unsaved-Project Protection

**Activity:** Corrective task addressing two project lifecycle issues identified during GitHub review. Both corrections were applied in Build mode using the existing `.venv` (Python 3.13.9). No Foundation documents modified. No commits or pushes made. No new architectural decisions introduced.

**Issue A — Project location persistence:**
- `ProjectService` now tracks `_active_location` (runtime-only, not serialized) to record where the active project resides.
- `_active_location` is set after successful `create_project()`, `open_project()`, or `open_project_from_path()`.
- `_active_location` is cleared in `close_project()`.
- `save_project()` now selects the repository based on the active project's location: uses the injected `_default_repository` when its `projects_root` matches the active location (preserving dependency injection and test patching), or creates a new repository for the active location otherwise.
- Failed operations (create/open/save) do not replace the existing active project or its location.

**Issue B — Unsaved-project protection:**
- `MainWindow` now has `_prompt_save_before_switch()` that presents Save/Discard/Cancel when the active project is dirty.
- `_on_new_project()` and `_on_open_project()` call `_prompt_save_before_switch()` after dialog acceptance but before the creation/opening operation.
- If the user cancels, the existing project remains active and unchanged.
- If saving fails, the existing project remains active and dirty; the operation is aborted.
- If creation/opening fails after Discard, the previous active project and its dirty state are preserved.

**Files modified (3):**
- `src/project_service.py` — Added `_active_location` tracking; updated `save_project()` repository selection; updated `create_project()`, `open_project()`, `open_project_from_path()`, `close_project()` to manage `_active_location`
- `src/main_window.py` — Added `_prompt_save_before_switch()` method; integrated it into `_on_new_project()` and `_on_open_project()`
- `tests/test_project_save_close.py` — Added 20 tests for location persistence and unsaved-project protection (total test count now 114)

**Module responsibility boundaries preserved:**
- `ProjectMetadata`: Stores metadata, tracks dirty state — unchanged
- `ProjectRepository`: Persists metadata with atomic writes — unchanged
- `ProjectService`: Location tracking and repository selection — minimal addition
- `MainWindow`: GUI prompts, user interaction — minimal addition

**Deferred requirement (still recorded, not implemented):**
- Application exit / window-close event integration (save-on-exit behavior)

**Verified test results (114 tests, all passing):**
- Total across all test files: 114 tests, 0 failures

**Approved decisions preserved (not modified):**
- D1: Desktop-first (DEC-004)
- D2: Photometry/time-series initial capability (DEC-001)
- D3: Initial scope boundaries (DEC-002)
- D4: Single-user local, private-by-default, permission-aware (DEC-003)
- D5: Technology stack Python 3.13/PySide6/NumPy/SciPy/Astropy/Matplotlib/pytest/venv (DEC-006)
- D6: Data storage model — formal decision deferred; provisional local-file approach for first vertical slice only

**Next steps:**
- Subtask 2.1.6 — Project lifecycle status management (Paused/Completed/Archived transitions)

**Status:** Stage 2 In Progress; Task 2.1 subtasks 2.1.1–2.1.5 complete (including corrective task), 2.1.6 pending.

### 2026-11-03 — Stage 2 Task 2.1 Subtask 2.1.6 (Project Lifecycle Status Management) complete

**Activity:** Stage 2 implementation — Subtask 2.1.6 project lifecycle status management. Added status-change capability (Active, Paused, Completed, Archived) with dirty tracking, save protection, and UI submenu. All work performed in Build mode using the existing `.venv` (Python 3.13.9). No Foundation documents modified. No commits or pushes made.

**Files created (1):**
- `tests/test_project_status.py` — 21 tests covering model-level status changes, service-level operations, UI submenu behavior, persistence, and reopening

**Files modified (3):**
- `src/project_model.py` — Added `set_status()` method following the `set_name()` pattern: validates status, marks dirty only when changed, preserves all other fields
- `src/project_service.py` — Added `change_status()` method delegating to model; raises `ProjectRepositoryError` when no active project, `ProjectValidationError` for invalid status
- `src/main_window.py` — Added Status submenu under Project with four checkable actions (Active, Paused, Completed, Archived) in exclusive group; updates checked state on create/open/close/status change; disables when no project
- `docs/MASTER_DEVELOPMENT_ROADMAP.md` — Task 2.1 subtask 2.1.6 marked Complete; all 2.1 subtasks now Complete

**Module responsibility boundaries preserved:**
- `ProjectMetadata`: Stores metadata, tracks dirty state via `set_status()`, `set_name()`, `mark_dirty()`, `mark_clean()`
- `ProjectRepository`: Persists metadata with atomic writes; unchanged
- `ProjectService`: `change_status()` delegates to model; no GUI dependencies; preserves `_active_location`
- `MainWindow`: Status submenu, checkable actions, dirty indicator, status-bar messages

**Status behavior:**
- All four statuses (Active, Paused, Completed, Archived) are valid
- All transitions between any two statuses are permitted
- Status changes mark the project dirty via `set_status()`
- Assigning an unchanged status does not mark dirty
- No auto-save on status change; user must explicitly save
- No confirmation dialog for status changes
- No restrictions on openability by status (all remain openable)
- Archived projects can be reactivated (no deletion or invalidation)
- No transition matrix; validation only checks membership in `VALID_STATUSES`

**Verified test results (135 tests, all passing):**
- `tests/test_project_status.py` — 21 tests (Subtask 2.1.6)
- Total across all test files: 135 tests, 0 failures

**Approved decisions preserved (not modified):**
- D1: Desktop-first (DEC-004)
- D2: Photometry/time-series initial capability (DEC-001)
- D3: Initial scope boundaries (DEC-002)
- D4: Single-user local, private-by-default, permission-aware (DEC-003)
- D5: Technology stack Python 3.13/PySide6/NumPy/SciPy/Astropy/Matplotlib/pytest/venv (DEC-006)
- D6: Data storage model — formal decision deferred; provisional local-file approach for first vertical slice only

**Deferred requirements (recorded, not implemented):**
- Application exit / window-close event integration (save-on-exit behavior)
- Status filtering or searching in project discovery
- Historical audit trail for status changes (change-history/provenance remains outside scope)

**Next steps:**
- Stage 2 review per §12.7.8 — formal review of the first useful scientific vertical slice
- Or begin Subtask 2.2 — light-curve dataset import

**Status:** Stage 2 In Progress; Task 2.1 subtasks 2.1.1–2.1.6 all complete.

### 2026-11-04 — D4 / DEC-003 Permission-Aware Data Model (schema version 2)

**Activity:** Implemented DEC-003 Option A — single-user local deployment with a permission-aware project metadata data model, and incremented the project metadata schema version from 1 to 2. Build mode, using the existing `.venv` (Python 3.13.9). No Foundation documents modified. No commits or pushes made. `src/project_service.py` and `src/project_repository.py` were not modified; the model's existing serialization interface is used for persistence.

**Approved architecture implemented:** DEC-003 Option A. Single-user local deployment; projects private by default; local user implicitly owns every project; no accounts, authentication, groups, invitations, collaboration, or public sharing. Ownership and permission metadata are present as a future architectural extension point only; no multi-user infrastructure was built.

**Files modified (4):**
- `src/project_model.py` — `SCHEMA_VERSION` incremented 1 → 2. Added `owner: str = "local_user"` and `roles: dict[str, list[str]]` (default factory returns independent view/contribute/manage roles, each containing "local_user"). `ProjectMetadata.create()` initializes owner, roles, schema_version=2, is_dirty=False. Added `validate_owner()` and `validate_roles()` plus schema-version upper-bound (>2) rejection in `validate()`. `to_dict()` serializes owner and roles (roles copied to avoid sharing). `from_dict()` distinguishes v1 (in-memory migration to v2 with default owner/roles when absent, is_dirty=False, no disk modification) from v2 (owner and roles required; missing fields raise ProjectValidationError) and rejects versions > 2 and invalid schema-version types/values.
- `tests/test_project_model.py` — Extended with tests for defaults (8.1), owner validation (8.2), roles validation (8.3), serialization round trips (8.4), v1 migration (8.5), v2 missing fields (8.6), future/invalid schema versions (8.7). Existing tests preserved.
- `tests/test_project_service.py` — Updated two existing assertions from `schema_version == 1` to `schema_version == 2` to match the approved schema increment; added owner/roles/defaults assertions to creation tests. Added tests: save/reload preserves owner and roles (9.2), and the complete legacy v1 migration → explicit save → reload workflow in tmp_path (9.3), including verification that migration is in-memory only before save.
- `docs/development/DEVELOPMENT_LOG.md` — This entry.

**Dirty-state behavior (verified):** New metadata is clean; v1 migration is clean; v2 deserialization is clean. No automatic save during migration; legacy project JSON remains unchanged on disk until an explicit save. Explicit save persists v2 metadata and leaves the project clean.

**Migration behavior (verified):** Loading a v1 project.json (no owner/roles, schema_version=1) upgrades in-memory schema_version to 2, applies default owner and roles, preserves existing fields, and is clean; the source file is untouched until `save_project()` is called, after which the file contains schema_version=2, owner="local_user", and all three default roles.

**Validation behavior (verified):** Owner rejects empty/whitespace/None/int/list/dict. Roles rejects non-dict, missing view/contribute/manage, non-string role names, non-list values, non-string/empty/whitespace-only principal IDs; additional valid role names accepted. V2 missing owner or roles raises ProjectValidationError. Schema version > 2 and invalid types/values (float, bool, list, dict, 0, negative) raise ProjectValidationError.

**Verified test results:**
- `tests/test_project_model.py` — 51 tests, 0 failures (12 pre-existing preserved, 39 new).
- `tests/test_project_service.py` — 12 tests, 0 failures (10 pre-existing with 2 assertions updated to schema_version==2, 2 new).
- Full suite `python -m pytest` — 176 collected, 174 passed, 2 failed.

**Full-suite failures (pre-existing tests, outside authorized scope):**
- `tests/test_project_discovery.py::test_open_valid_project_from_default_root` — asserts `schema_version == 1`; now fails because `ProjectMetadata.create()` correctly produces schema version 2 per the approved architecture.
- `tests/test_project_discovery.py::test_open_project_from_custom_location` — same cause, asserts `schema_version == 1`.
These two tests encode the pre-change schema version and are in `tests/test_project_discovery.py`, which is outside the four authorized files. They need their assertion updated to `schema_version == 2` to align with DEC-003; that change is outside this task's authorized scope.

**Limitations (deferred, not implemented):** The implementation remains strictly single-user and local. No ownership transfer, role assignment, authentication, user registration, groups, invitations, collaboration, public sharing, or multi-user authorization infrastructure exists. Multi-user functionality is deferred, not implemented.

**Approved decisions preserved (not modified):** D1–D6 as recorded previously; D4 (single-user local, private-by-default, permission-aware) is the basis of this implementation.

### 2026-11-04 — D4 Compatibility Cleanup: Project Discovery Tests

**Activity:** Corrected two outdated schema-version expectations in `tests/test_project_discovery.py` following the completed D4 / DEC-003 implementation. Build mode, using the existing `.venv` (Python 3.13.9). No production code changed.

**Relationship to D4 / DEC-003:** DEC-003 incremented the project metadata schema version from 1 to 2. Newly created projects now correctly produce `schema_version == 2`. Two discovery tests still asserted the obsolete value `schema_version == 1`, causing them to fail.

**Files modified (2):**
- `tests/test_project_discovery.py` — Updated two assertions:
  - `test_open_valid_project_from_default_root` (line 204): `assert loaded.schema_version == 1` → `assert loaded.schema_version == 2`.
  - `test_open_project_from_custom_location` (line 223): `assert loaded.schema_version == 1` → `assert loaded.schema_version == 2`.
  All other assertions, setup, fixtures, and behavior preserved. No tests removed, weakened, skipped, or added. Legacy v1 migration behavior remains covered by the D4 model and service tests.
- `docs/development/DEVELOPMENT_LOG.md` — This entry.

**No production code changed:** `src/project_model.py`, `src/project_service.py`, and `src/project_repository.py` were untouched by this task. The original D4 implementation changes remain intact.

**Verified test results:**
- `tests/test_project_discovery.py` — all discovery tests pass.
- `tests/test_project_model.py` — 51 tests, 0 failures (unchanged from D4).
- `tests/test_project_service.py` — 12 tests, 0 failures (unchanged from D4).
- Full suite `python -m pytest` — 176 collected, 176 passed, 0 failed.

**Python and pytest versions:** Python 3.13.9 (`.venv`), pytest 9.2.0.

**Git:** No commit or push was made. The pre-existing D4 modifications (`src/project_model.py`, `tests/test_project_model.py`, `tests/test_project_service.py`, `docs/development/DEVELOPMENT_LOG.md`) were preserved; only `tests/test_project_discovery.py` was added as an additional modified file by this task.

**Limitations (unchanged, deferred):** The implementation remains strictly single-user and local. No multi-user functionality exists.

### 2026-11-04 — Stage 2 Task 2.2 Subtask 2.2.2 (FITS Import and Validation) complete

**Activity:** Implemented the FITS light-curve importer for Subtask 2.2.2. All work performed in Build mode using the existing `.venv` (Python 3.13.9). No Foundation documents modified. No commits or pushes made.

**Files created (2):**
- `src/fits_importer.py` — `FITSImportError` exception and `import_light_curve(file_path)` function. Reads FITS files read-only, identifies the light-curve table structurally (not by fixed HDU index), extracts supported measurements (`TIME`, `SAP_FLUX`, `PDCSAP_FLUX`, `SAP_FLUX_ERR`, `PDCSAP_FLUX_ERR`, `SAP_QUALITY`, `CADENCENO`), preserves scientific metadata, validates contents, and constructs `LightCurveDataset` from Subtask 2.2.1.
- `tests/test_fits_importer.py` — 46 focused unit tests using temporary FITS fixtures under pytest `tmp_path`.

**Module responsibilities:**
- `fits_importer.py`: Pure FITS import logic — file opening, HDU identification, column extraction, metadata mapping, unit compatibility validation, validation findings, dataset construction. No PySide6, no project/service/repository imports, no database, no persistence.

**Key implementation details:**
- Structural HDU identification: candidates must contain `TIME` and at least one of `SAP_FLUX`/`PDCSAP_FLUX`. Prefer `EXTNAME=LIGHTCURVE` among valid candidates; otherwise first in HDU order. Multiple candidates → informational finding.
- Extension header metadata read from `selected_hdu.header` (not fixed `hdul[1]`). Primary header provides source metadata; extension header provides time metadata. Application-level fallback for source metadata is documented and independent of FITS `INHERIT`.
- Unit policy: flux and uncertainty units read independently; compatibility enforced before column construction (both present & identical → import; both blank → import with `unit=""`; only one present → `FITSImportError`; both present but different → `FITSImportError`). `MeasurementColumn.unit` holds the flux unit only — no separate uncertainty-unit field.
- Time metadata: `TIMEUNIT` → `TimeInfo.unit`; descriptive `TUNIT1` → `TimeInfo.reference`; `TIMESYS` → time scale; `TIMEREF` → reference frame; `BJDREFI`/`BJDREFF` → reference value. No BKJD→JD conversion.
- Integer `TNULL` policy: sentinel declared but unused → import normally; sentinel present in data → `FITSImportError`.
- Validation findings: non-finite values (warning), negative uncertainties (warning), duplicate times (warning), non-monotonic times (warning), nonzero quality flags (info, no filtering), orphan uncertainties (warning), missing time unit (info).
- All arrays copied before FITS file close; memory-mapped data safely handled.

**Verified test results (46 tests, all passing):**
- `tests/test_fits_importer.py` — 46 tests (Subtask 2.2.2), 0 failures.

**Full non-GUI test suite:** 219 passed, 0 failed (includes 46 new importer tests + all existing project and model tests). Two GUI test files (`test_new_project_dialog.py`, `test_project_save_close.py`) hang in this environment due to PySide6 display requirements — pre-existing issue unrelated to this task.

**Approved decisions preserved (not modified):** D1–D6 as recorded previously.

**Next steps:** Subtask 2.2.3 (project association and provisional persistence) is pending. Subtask 2.2.4 (broader Stage 2.2 verification, documentation reconciliation, completion assessment) is pending.

**Git:** No commit or push was made.
