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
- Subtask 2.1.5 — Project saving and closing workflow
- Subtask 2.1.6 — Project lifecycle status management

**Status:** Stage 2 In Progress; Task 2.1 subtasks 2.1.1–2.1.4 complete, 2.1.5–2.1.6 pending.
