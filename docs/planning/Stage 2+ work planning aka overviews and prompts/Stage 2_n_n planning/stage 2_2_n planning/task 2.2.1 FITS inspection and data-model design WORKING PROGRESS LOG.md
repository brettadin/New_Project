# INITIAL PLAN

I now have all verified information needed. Let me compile the complete structured planning report.

---

# PLAN REPORT — Subtask 2.2.1: FITS Inspection and Light-Curve Data-Model Design

**Mode:** PLAN ONLY. No files were created, modified, deleted, or overwritten. No implementation was performed.

---

## 1. Repository and Architecture Findings

### Actual repository state

The repository is at `C:\Code\New_Project`. Git working tree contains uncommitted changes from the completed D4 / DEC-003 implementation (schema version 2, owner/roles metadata, model/service/tests updated) plus the D4 discovery-test compatibility cleanup. No commits or pushes have been made. All existing modifications are preserved.

### Verified test baseline

The most recent full test-suite result reported: **176 passed, 0 failed**, using Python 3.13.9 (`.venv`) and pytest 9.2.0. This baseline includes the D4 changes and the discovery-test fix.

### Relevant files inspected

| File | Responsibility |
|---|---|
| `src/project_model.py` | `ProjectMetadata` dataclass: metadata fields, validation (`ProjectValidationError`), serialization (`to_dict`/`from_dict`), dirty-state tracking, `create()`, `set_name()`, `set_status()`. Schema version 2. |
| `src/project_repository.py` | JSON persistence (`project.json` per project directory), atomic writes, discovery scanning, `load`/`load_from_directory`/`save`, error classes. |
| `src/project_service.py` | Lifecycle orchestration: create/open/save/close/discover, active-project tracking, failure cleanup. |
| `src/config_provider.py` | Projects-root resolution (`ASTRONOMY_PROJECTS_ROOT` env var > config file > default). |
| `src/main.py` | Application entry point; wires `ConfigProvider`, `ProjectRepository`, `ProjectService`. |
| `src/main_window.py` | PySide6 `QMainWindow` shell; project lifecycle menus; dirty indicator. |
| `src/new_project_dialog.py`, `src/open_project_dialog.py` | PySide6 dialogs for creation/opening. |
| `tests/test_project_*.py` | Existing test suite (model, service, repository, save/close, status, discovery, dialogs). |

### Existing functionality reusable

- Project create/open/save/close lifecycle via `ProjectService` + `ProjectRepository`.
- Atomic JSON writes; `project.json` per project directory keyed by stable `project_id` (UUID).
- Dirty-state tracking (`is_dirty`, `mark_dirty`, `mark_clean`) on `ProjectMetadata`.
- `external_data_references` field already exists on `ProjectMetadata` — a natural place to record source-file references.
- Schema-version mechanism already in place (`SCHEMA_VERSION` = 2).

### Architectural boundaries (to preserve)

Per the task instructions and DEC-003:
- Project metadata (`ProjectMetadata`) must not hold large scientific measurement arrays.
- Do not duplicate ownership/permission metadata inside the scientific dataset model.
- Single-user local deployment; no authentication/collaboration/multi-user infrastructure.
- D6 (data storage model) remains deferred; provisional local-file persistence only for the first vertical slice.

### Missing/incomplete documentation

- No dedicated architecture or data-model documentation exists yet for scientific datasets (the `docs/architecture/` directory is referenced by `docs/README.md` but was not found to contain dataset-model docs). The Foundation index points to `docs/architecture/` for "System architecture, component responsibilities, data models, internal interfaces."
- UQ-003 (data model for objects/observations/datasets/derived products) remains open (D6 formal deferred).

---

## 2. Actual FITS Inspection Results

**File (read-only, outside repository):** `C:\Code\AstronomyData\Kepler\Kepler-10b\kplr011904151-2009131105131_llc_full.fits`  
**Tool:** `astropy.io.fits` (astropy 8.0.2), opened `mode='readonly'`. All findings below were directly verified against the actual file.

### HDU structure

| HDU | Type | Name | Purpose |
|---|---|---|---|
| 0 | `PrimaryHDU` | PRIMARY | Global mission/target metadata; no table data |
| 1 | `BinTableHDU` | LIGHTCURVE | Light-curve measurements (476 rows × 20 columns) — **the relevant light-curve HDU** |
| 2 | `ImageHDU` | APERTURE | 12×10 pixel aperture mask image with WCS |

The `INHERIT = True` keyword on extensions 1 and 2 means they inherit primary-header keywords.

### LIGHTCURVE table structure (verified)

- **Rows:** 476
- **Columns:** 20

| Column | Format | Unit | Notes |
|---|---|---|---|
| `TIME` | f8 (64-bit float) | `BJD - 2454833` (days) | Time stamps; **0 non-finite**; range 120.539–130.245 |
| `TIMECORR` | f32 | `d` | Barycenter–timeslice correction; 0 non-finite |
| `CADENCENO` | i32 | (none) | Unique cadence number; range 568–1043; spacing exactly 1 |
| `SAP_FLUX` | f32 | `e-/s` | Aperture-photometry flux; **4 non-finite** (cadences 703, 848, 950, 972) |
| `SAP_FLUX_ERR` | f32 | `e-/s` (1-sigma) | SAP flux uncertainty; 4 non-finite (same rows as SAP_FLUX) |
| `SAP_BKG` | f32 | `e-/s` | Background flux; 4 non-finite |
| `SAP_BKG_ERR` | f32 | `e-/s` | Background error; 4 non-finite |
| `PDCSAP_FLUX` | f32 | `e-/s` | PDC-corrected flux; **7 non-finite** (cadences 703, 790, 848, 914, 915, 950, 972) |
| `PDCSAP_FLUX_ERR` | f32 | `e-/s` | PDCSAP flux uncertainty; 7 non-finite |
| `SAP_QUALITY` | i32 | (none) | Quality bitmask; values {0, 64, 128, 8192, 8320, 12352, 32800}; **37 of 476 rows nonzero** |
| `PSF_CENTR1/2`, `*_ERR` | f8/f32 | `pixel` | PSF centroids; **all 476 rows non-finite** (column entirely empty) |
| `MOM_CENTR1/2`, `*_ERR` | f8/f32 | `pixel` | Moment centroids; 4 non-finite |
| `POS_CORR1/2` | f32 | `pixels` | Position corrections; 7 non-finite |

### Header metadata (verified, from LIGHTCURVE extension)

| Keyword | Value | Meaning |
|---|---|---|
| `TELESCOP` | `Kepler` | Telescope |
| `INSTRUME` | `Kepler Photometer` | Instrument |
| `OBJECT` | `KIC 11904151` | Target identifier |
| `KEPLERID` | 11904151 | Unique Kepler target ID |
| `MISSION` | `Kepler` | Mission name |
| `ORIGIN` | `NASA/Ames` | Creating institution |
| `CREATOR` | `793551 FluxExporter2PipelineModule` | Pipeline module |
| `DATE` | `2015-08-26` | File creation date |
| `OBSMODE` | `long cadence` | Observing mode |
| `QUARTER` | 0 | Observing quarter |
| `TIMEREF` | `SOLARSYSTEM` | Barycentric correction applied |
| `TIMESYS` | `TDB` | Time system (barycentric JD) |
| `BJDREFI` | 2454833 | Integer part of BJD reference date |
| `BJDREFF` | 0.0 | Fraction of BJD reference date |
| `TIMEUNIT` | `d` | Time unit for TIME/TSTART/TSTOP |
| `TSTART` | 120.52892942 | Observation start (BJD - BJDREF) |
| `TSTOP` | 130.25561236 | Observation stop |
| `DATE-OBS` | `2009-05-02T00:40:13.639Z` | TSTART as UTC |
| `DATE-END` | `2009-05-11T18:06:13.939Z` | TSTOP as UTC |
| `TIMEDEL` | 0.02043359821692 | Time resolution (long cadence ≈ 29.4 min) |
| `INT_TIME` | 6.0198 s | Photon accumulation per frame |
| `FRAMETIM` | 6.5388 s | Frame time |

### Primary header (verified)

`TELESCOP`/`INSTRUME`/`OBJECT`/`KEPLERID`/`MISSION`/`RADESYS`/`RA_OBJ`/`DEC_OBJ`/`TEFF`/`LOGG`/`FEH`/`KEPMAG` etc. Stellar parameters present (Teff=5627 K, Kp mag=10.961).

### SAP_FLUX vs PDCSAP_FLUX distinction (verified, not interchangeable)

- `SAP_FLUX`: Simple aperture photometry flux — raw flux within the optimal aperture (background-subtracted).
- `PDCSAP_FLUX`: PDC (Pre-search Data Conditioning) corrected flux — systematic effects removed; better for transit detection.
- They have **different non-finite patterns** (4 vs 7 rows) and different value ranges (SAP ≈ 532355–532944 e-/s; PDCSAP ≈ 501346–501747 e-/s). Must remain independently identifiable.

### Deviations from prior (unverified) findings

Prior log stated "~476 rows" (verified: exactly 476), "~9.7 days" (verified: TSTOP−TSTART = 9.7267 days), "~4 missing flux measurements" (verified: exactly 4 for SAP_FLUX, 7 for PDCSAP_FLUX), "~37 nonzero quality flags" (verified: exactly 37). UQ-008 ("Can a Kepler-10b FITS file be obtained and inspected?") is now resolved — the file is present and directly inspected.

### Important observation for model design

`PSF_CENTR1`/`PSF_CENTR2` are **entirely non-finite** (all 476 rows). This confirms the model must handle measurement columns that may be fully absent/invalid — not every column contains usable data, and column availability is per-column, not per-row. Missingness is column-specific (SAP vs PDCSAP differ).

---

## 3. Proposed Data Model

### Guiding principles

- Represent a light-curve dataset independently of the Kepler file structure (no hard-coded column names beyond what's needed for the initial importer).
- Preserve original measurements without modification; never silently drop observations.
- Preserve time semantics (value, unit, reference epoch, time scale) separately.
- Keep measurement columns and their uncertainties associated.
- Distinguish dataset identity/source metadata from measurements from validation findings.
- No coupling to permanent storage architecture (D6 deferred).

### Proposed structures

#### 3.1 `LightCurveDataset` (top-level dataset container)

**Responsibility:** Holds a single imported light-curve dataset: its identity/source metadata, measurements, time representation, units, and validation findings. One instance per imported dataset.

| Field | Type | Required? | Purpose |
|---|---|---|---|
| `dataset_id` | `str` (UUID) | Yes | Stable identifier for the dataset within a project |
| `name` | `str` | Yes | User-visible dataset name |
| `source` | `DatasetSource` | Yes | Source-file identity and provenance metadata |
| `time` | `TimeInfo` | Yes | Time representation (values, unit, reference, scale) |
| `measurements` | `MeasurementSeries` | Yes | The measurement columns (flux + uncertainty pairs) |
| `quality_flags` | `list[int]` or `numpy.ndarray` | Yes | Per-observation quality flags (preserved, not filtered) |
| `cadence_numbers` | `list[int]` | Yes | Observation identifiers |
| `n_observations` | `int` | Yes | Row count (derivable, but stored for convenience) |
| `validation` | `ValidationReport` | Yes | Import/construction validation findings |
| `imported_at` | `str` (ISO-8601) | Yes | Import timestamp |
| `notes` | `str` | No | User annotations |

**Relationships:** A `Project` may contain zero or more `LightCurveDataset` instances (association mechanism to be defined in 2.2.3, not here).

#### 3.2 `DatasetSource` (source identity & provenance)

**Responsibility:** Identifies where the dataset came from and tracks source-file availability.

| Field | Type | Required? | Purpose |
|---|---|---|---|
| `source_id` | `str` | Yes | Stable source identifier (e.g., KIC 11904151 / KeplerID) |
| `original_filename` | `str` | Yes | Original file name |
| `original_file_path` | `str` | Yes | Absolute path to source file (at import time) |
| `archive` | `str` | No | Originating archive/resource (e.g., "MAST/STScI") |
| `mission` | `str` | No | Mission (e.g., "Kepler") |
| `instrument` | `str` | No | Instrument (e.g., "Kepler Photometer") |
| `target_object` | `str` | No | Target object identifier (e.g., "KIC 11904151") |
| `checksum` | `str` | No | File checksum for source identification (optional, recommended) |
| `file_available` | `bool` | No (derived) | Cached availability flag; **determined dynamically** when needed, not trusted blindly |

**Design decision:** Source-file availability is determined dynamically at load/access time (the file may be moved/deleted after import). The stored path + checksum support re-verification. A checksum is useful provenance but is distinct from complete scientific provenance (§4.7).

#### 3.3 `TimeInfo` (time representation)

**Responsibility:** Preserve timestamps **and** their interpretation — never reduce to raw floats without context.

| Field | Type | Required? | Purpose |
|---|---|---|---|
| `values` | `numpy.ndarray` (float64) | Yes | Numerical timestamp values |
| `unit` | `str` | Yes | Time unit (e.g., "d") |
| `reference` | `str` | No | Time reference/epoch (e.g., "BJD - 2454833") |
| `reference_value` | `float` | No | Numeric reference epoch (e.g., 2454833.0) |
| `time_scale` | `str` | No | Time scale/system (e.g., "TDB") |
| `time_reference_frame` | `str` | No | Barycentric frame (e.g., "SOLARSYSTEM") |
| `start` | `float` | No | TSTART / observation start |
| `stop` | `float` | No | TSTOP / observation stop |
| `resolution` | `float` | No | TIMEDEL / time resolution |
| `format_hint` | `str` | No | e.g., "BJD" |

**Rationale:** Astropy `Time` objects are appropriate for computation but are not ideal for serialization/persistence (they carry complex internal state). The model stores primitive components (values + unit + reference + scale) so the dataset can be serialized and reconstructed without Astropy being present, and `astropy.time.Time` can be constructed on demand for computation (e.g., BLS in 2.2.4). This avoids silently converting time or assuming a convention when metadata is missing.

#### 3.4 `MeasurementSeries` (measurements + uncertainties)

**Responsibility:** Holds measurement columns with their uncertainties, keeping each measurement column associated with its uncertainty column.

**Rejected alternatives:**
- **Separate aligned arrays:** Simple but loses the column↔uncertainty association and column identity/metadata; error-prone when columns are added/removed.
- **Table-like representation (e.g., Astropy Table / DataFrame):** Powerful but introduces a heavy dependency into the core model and couples serialization to that table format.
- **Chosen:** A small container of named measurement series, each a pair (values, uncertainties) with column identity and units.

| Field | Type | Required? | Purpose |
|---|---|---|---|
| `series` | `dict[str, MeasurementColumn]` | Yes | Named measurement series (key = column identity, e.g., "SAP_FLUX") |

#### 3.5 `MeasurementColumn` (one measurement + its uncertainty)

**Responsibility:** A single measurement column and its associated uncertainty, plus column metadata.

| Field | Type | Required? | Purpose |
|---|---|---|---|
| `name` | `str` | Yes | Column identity (original FITS column name, e.g., "SAP_FLUX") |
| `values` | `numpy.ndarray` (float64) | Yes | Measurement values |
| `uncertainties` | `numpy.ndarray` (float64) | Yes | 1-sigma uncertainties (aligned, same length) |
| `unit` | `str` | Yes | Measurement unit (e.g., "e-/s") |
| `description` | `str` | No | Column description (from FITS TTYPE/TCOMM) |
| `n_nonfinite` | `int` | Yes | Count of non-finite values (validation-derived) |

**Constraint:** `len(values) == len(uncertainties) == n_observations` (validated). Non-finite values are **preserved**, not removed.

**Column identity vs. role:** The `name` preserves the original column. A separate `selected_series` reference (on `LightCurveDataset`) indicates which series is selected for subsequent analysis — this keeps SAP and PDCSAP independently accessible while marking the analysis choice.

#### 3.6 `ValidationReport` (validation findings)

**Responsibility:** Structured record of validation findings so the importer can report them consistently.

| Field | Type | Required? | Purpose |
|---|---|---|---|
| `errors` | `list[ValidationFinding]` | Yes | Conditions preventing acceptance |
| `warnings` | `list[ValidationFinding]` | Yes | Conditions permitting representation but flagged |
| `info` | `list[ValidationFinding]` | Yes | Conditions preserved without modification |

#### 3.7 `ValidationFinding`

| Field | Type | Purpose |
|---|---|---|
| `code` | `str` | Stable machine-readable code |
| `message` | `str` | Human-readable description |
| `severity` | `str` ("error"/"warning"/"info") | Severity |
| `column` | `str` | Affected column (if any) |
| `row_indices` | `list[int]` | Affected rows (if any) |

### Conceptual example (pseudocode, not implementation-ready code)

```
dataset = LightCurveDataset(
    dataset_id = uuid4(),
    name = "Kepler-10b Quarter 0",
    source = DatasetSource(
        source_id = "KIC 11904151",
        original_filename = "kplr011904151-2009131105131_llc_full.fits",
        original_file_path = r"C:\...\Kepler-10b\kplr..._llc_full.fits",
        mission = "Kepler",
        instrument = "Kepler Photometer",
        target_object = "KIC 11904151",
        archive = "MAST/STScI",
    ),
    time = TimeInfo(
        values = [...476 floats...],  # TIME column
        unit = "d",
        reference = "BJD - 2454833",
        reference_value = 2454833.0,
        time_scale = "TDB",
        time_reference_frame = "SOLARSYSTEM",
        start = 120.5289,
        stop = 130.2556,
        resolution = 0.02043,
    ),
    measurements = MeasurementSeries(series = {
        "SAP_FLUX": MeasurementColumn(name="SAP_FLUX", values=[...], uncertainties=[...], unit="e-/s", description="aperture photometry flux", n_nonfinite=4),
        "PDCSAP_FLUX": MeasurementColumn(name="PDCSAP_FLUX", values=[...], uncertainties=[...], unit="e-/s", description="PDC-corrected flux", n_nonfinite=7),
        # ... other columns as needed
    }),
    quality_flags = [0, 0, 64, ...],  # 476 entries, preserved
    cadence_numbers = [568, 569, ...],  # 476 entries
    validation = ValidationReport(errors=[], warnings=[...], info=[...]),
    imported_at = "2026-...",
)
```

**Key design points honored:**
- SAP_FLUX and PDCSAP_FLUX are independently identifiable and accessible (separate `MeasurementColumn` entries).
- Uncertainties remain associated with their measurement columns (same `MeasurementColumn`).
- Time preserves unit ("d"), reference ("BJD - 2454833"), reference value (2454833.0), and scale ("TDB") separately.
- Non-finite values preserved (n_nonfinite tracked, values not removed).
- Nonzero quality flags preserved (37 rows).
- PSF_CENTR columns (all non-finite) can be omitted or stored with n_nonfinite=476 — model does not require every column to be usable.

---

## 4. Data Integrity and Validation Design

### Required vs. optional scientific information

**Required (absence = error):** dataset identity, at least one usable measurement series, time values with unit, observation count, quality flags array aligned to observations.

**Optional (absence = warning or info):** source-file path/checksum, mission/instrument/target metadata, uncertainties for a column, centroid/position columns, archive name.

### Validation tiers

1. **Model-level validation** (constructing the model): checks internal consistency — `len(values) == len(uncertainties) == n_observations` for each series; quality flags and cadence arrays length-match `n_observations`; required fields present and typed correctly; time unit/reference/scale present when time values present. Raises `ValueError`-style model errors for structural inconsistency.

2. **Import-level validation** (FITS import, 2.2.2): checks source-data suitability — file readable, expected HDU present, required columns present, time metadata present. Produces `ValidationReport` with errors/warnings/info.

### Errors vs. warnings vs. info

| Condition | Disposition | Rationale |
|---|---|---|
| Missing required column (e.g., TIME) | Error | Cannot represent dataset |
| Array length mismatch | Error | Structural corruption |
| Non-finite measurement values | Warning (preserved) | Data quality issue; do not drop silently |
| Missing uncertainties for a column | Warning | Column usable but uncertainty unknown |
| Nonzero quality flags | Info (preserved) | 37 rows in Kepler-10b; do not discard |
| Entirely empty column (e.g., PSF_CENTR) | Info | Column present but no data |
| Unknown/missing units | Warning | Computation may be affected |
| Missing/ambiguous time convention | Warning | BLS/time ops need scale + reference |
| Source file not found at load | Warning (runtime) | File may have moved; data still in model |

### Original vs. derived measurements

Original source measurements are stored as imported. Future derived/transformed measurements (normalized, detrended, filtered) must be stored as separate `MeasurementColumn` entries with provenance metadata linking back to the source series — never overwriting originals. Processing operations (normalization, detrending, quality filtering, interpolation) are **out of scope** for this task.

### Unknown units and time conventions

- Unknown unit: stored as-is (string); computation functions must handle gracefully.
- Missing time scale/reference: warning issued; time values still stored but flagged as ambiguous. No default convention assumed.

---

## 5. Architecture Integration Proposal

### Module responsibilities

| Module | Responsibility |
|---|---|
| `project_model.py` | Project metadata only (unchanged). **Not** extended with measurement arrays. |
| `project_repository.py` | JSON persistence only (unchanged). |
| `project_service.py` | Project lifecycle only (unchanged). |
| **New module** (e.g., `src/light_curve.py` or `src/dataset/`) | Light-curve data model: `LightCurveDataset`, `DatasetSource`, `TimeInfo`, `MeasurementSeries`, `MeasurementColumn`, `ValidationReport`. No UI, no persistence, no FITS reading. |
| **Future importer** (2.2.2) | Reads FITS, constructs model, performs import-level validation. |
| **Future project integration** (2.2.3) | Associates datasets with projects, provisional persistence. |

### Dataset–project relationship

A project may contain zero or more datasets. The association mechanism (how datasets are stored/referenced relative to a project) is deliberately deferred to 2.2.3 because D6 (storage) is deferred. For 2.2.1, the model is independent of projects entirely.

### Separation of concerns preserved

- Project metadata (`ProjectMetadata`) — project-level: name, status, owner, roles, schema version.
- Scientific dataset (`LightCurveDataset`) — observation-level: measurements, time, source, validation.
- Source-file reference — in `DatasetSource.original_file_path`, **not** duplicated in project metadata.
- Validation findings — in `ValidationReport`, separate from measurements.
- Future analysis results — separate structure (deferred).

### Coupling concerns

- The dataset model imports only `numpy` (and standard library). It does **not** import PySide6, astropy.fits, or the project model. This keeps it testable and storage-independent.
- `astropy.time.Time` may be used optionally for computation but is not a required dependency of the model structure (primitive fields stored instead).

### Compatibility with existing project lifecycle

No changes to `ProjectMetadata`, `ProjectRepository`, or `ProjectService` are required in 2.2.1. Integration (associating datasets with projects, saving dataset references) happens in 2.2.3.

---

## 6. Storage Implications

Within D6's approved boundaries (provisional local-file, formal architecture deferred):

1. **Information independent of storage:** dataset identity, source metadata, measurements, time, units, quality flags, validation report — all represented without reference to a specific file format or database.
2. **Information that must survive save/reopen:** dataset identity, source path, measurements, time, validation. (Exactly which and how is a 2.2.3 question.)
3. **What 2.2.3 needs from the model:** a serializable representation (fields are primitives/numpy arrays) and a clear association to a project.
4. **External source file references:** stored as path + checksum; availability determined dynamically. Risk: file may be moved/deleted after import; data remains in model but re-verification may fail.
5. **Copying data into a project:** NOT done in this design (preserves original-file approach per DEC-002/architecture decisions: "Original external data files referenced by path, never copied or modified"). Copying is a future storage decision.
6. **Risks of external paths:** path staleness, portability across machines. Mitigated by checksum + dynamic availability check; not solved in 2.2.1.
7. **Serialization without losing scientific meaning:** achievable if units, time reference/scale, and column identities are stored as explicit strings (as proposed). Lost only if reduced to raw floats.
8. **Aspects outside the model:** where files live, atomic writes, project-file format, checksum algorithm choice — these are storage/layer concerns for 2.2.3+.

**Storage-related decision requiring approval:** None for 2.2.1 (model is storage-independent). The question of how/whether datasets are persisted with projects is deferred to 2.2.3 under D6's provisional approach.

---

## 7. Future Compatibility

### Generic elements (in the core model)

- `dataset_id`, `name`, `imported_at`, `validation`, `quality_flags`, `cadence_numbers` — generic to any time-series photometry.
- `TimeInfo` with explicit unit/reference/scale — works for any time convention (BJD, JD, MJD, Unix time, etc.).
- `MeasurementSeries`/`MeasurementColumn` keyed by column name — works for any flux/intensity/magnitude columns and any units.
- `DatasetSource` with mission/instrument/target/archive — works for Kepler, TESS, ground-based, etc.

### Kepler-specific assumptions (keep in the importer, not the model)

- Column names `SAP_FLUX`, `PDCSAP_FLUX`, `SAP_QUALITY`, `CADENCENO` — these are Kepler FITS conventions; the importer maps them to generic `MeasurementColumn` entries.
- `BJD - 2454833` reference, `TDB` scale, `SOLARSYSTEM` frame — Kepler-specific time convention; `TimeInfo` is generic.
- `e-/s` flux unit — one possible unit among many.

### Future compatibility accommodated

- FITS light curves from other missions: importer maps their columns; model unchanged.
- Different measurement columns: `MeasurementSeries` is a dict keyed by name; arbitrary columns supported.
- Different time conventions: `TimeInfo` stores unit/reference/scale as strings.
- Different flux/intensity/magnitude units: `MeasurementColumn.unit` is a string.
- Different uncertainty representations: stored as aligned array; absence = warning.
- Different quality systems: `quality_flags` is a generic int array; interpretation deferred.
- Additional photometric datasets: multiple `LightCurveDataset` instances per project (2.2.3).
- Different cadences: `cadence_numbers` generic; not required to be uniformly spaced.

### Compatibility with later visualization and BLS

- BLS needs time values, flux values, and uncertainties — all preserved with units.
- Visualization needs x (time) and y (flux) series with axis labels — available via `TimeInfo` + `MeasurementColumn.unit`/`description`.
- Normalization/detrending (future) store as new `MeasurementColumn` entries — originals untouched.

**Not attempted:** A universal astronomy data framework. The model is purpose-built for 1-D time-series photometry with associated uncertainties.

---

## 8. Decisions Requiring Approval

### Existing approved decisions (relied upon, not changed)

- DEC-001: Photometry/time-series as initial capability.
- DEC-002: Four-category scope; import of one light-curve format included; original-file preservation.
- DEC-003: Single-user local; no multi-user infrastructure in dataset model.
- DEC-005: BLS as initial operation (model must preserve time+flux+uncertainty for it).
- DEC-006: Python 3.13 + NumPy/SciPy/Astropy/Matplotlib stack (numpy available for model).
- D6 deferred: provisional local-file only; no storage architecture decision here.

### Recommendations within existing architectural authority (no new approval needed)

- New module `src/light_curve.py` (or `src/dataset/`) for the scientific dataset model — justified as a separate concern from `ProjectMetadata`.
- Model uses numpy arrays + primitive types only; no PySide6, no astropy.fits dependency.
- `TimeInfo` stores primitive time components rather than `astropy.time.Time` objects directly.

### New decisions requiring my approval

1. **Exact module name and location** for the dataset model (e.g., `src/light_curve.py` vs `src/dataset/light_curve.py`).
2. **Whether `quality_flags` and `cadence_numbers` are stored as Python lists or numpy arrays** in the model (affects serialization in 2.2.3).
3. **Whether `MeasurementColumn.uncertainties` is required or optional** at the model level (some datasets may lack uncertainties).
4. **Whether a checksum field is required or optional** in `DatasetSource`.

### Questions that can safely remain deferred

- How datasets are associated with projects (2.2.3).
- Exact persistence format/location (D6 deferred; 2.2.3 provisional).
- Whether source files are ever copied into projects (DEC-002 says referenced by path, never copied — but formal confirmation in 2.2.3).
- Analysis-record model for derived measurements (§5.5) — deferred.
- Units library choice (Astropy `Quantity` vs plain strings) — recommended plain strings for serialization simplicity.

---

## 9. Proposed Implementation Breakdown

Reviewing the proposed remaining Subtask 2.2 organization:

| Subtask | Intended responsibility | Assessment after this investigation |
|---|---|---|
| 2.2.2 | FITS import and validation | **Appropriate.** Reads the verified LIGHTCURVE HDU, maps columns to `MeasurementSeries`, builds `TimeInfo`, produces `ValidationReport`. Depends on the 2.2.1 model. |
| 2.2.3 | Project integration and provisional persistence | **Appropriate.** Associates datasets with projects; decides how dataset references survive save/reopen. Depends on D6's provisional approach. |
| 2.2.4 | Testing, documentation, and completion verification | **Appropriate.** |

### Dependencies and shared interfaces

- 2.2.2 → 2.2.1: importer constructs model instances; model must be complete before importer.
- 2.2.3 → 2.2.1: project integration needs a serializable model and a dataset–project association.
- 2.2.2 → 2.2.3: imported datasets become associated with a project.

### Potential overlap

None identified, provided 2.2.1 stays strictly a data model (no FITS reading, no project association, no persistence).

### Recommended changes to task boundaries

None required. The three-subtask breakdown remains appropriate. The 2.2.1 scope should remain limited to: FITS inspection (done here) + proposed data model + validation design. No implementation code belongs in 2.2.1.

---

## 10. Testing Strategy

Tests belonging to 2.2.1 (data model):

| Test category | What it covers | Belongs to |
|---|---|---|
| Model construction | Building `LightCurveDataset` and sub-structures with valid data | 2.2.1 |
| Model validation | `ValidationReport` generation; required-field errors; length mismatches; non-finite handling | 2.2.1 |
| Serialization/conversion | Round-trip of model to/from plain dict (primitive/numpy) without losing units/time-reference/scale | 2.2.1 |
| Controlled scientific-data fixtures | Small synthetic numpy arrays exercising edge cases (empty column, all-nonfinite column, length mismatch) | 2.2.1 |
| Time representation | Preservation of unit/reference/scale; no silent float reduction | 2.2.1 |
| SAP/PDCSAP independence | Two flux columns independently accessible; uncertainties aligned | 2.2.1 |

Tests belonging to subsequent subtasks:

| Test category | Belongs to |
|---|---|
| FITS file parsing (actual Kepler dataset) | 2.2.2 (importer) |
| Import-level validation against real FITS | 2.2.2 |
| Project association of datasets | 2.2.3 |
| Save/reopen of dataset references | 2.2.3 |
| GUI/visualization tests | Later (visualization subtask) |
| BLS analysis tests | 2.2.4 / BLS subtask |

**Do not** introduce FITS-importer or project-integration tests into 2.2.1. Do not weaken or replace existing tests.

---

## 11. Documentation Impact Assessment

Documents that may require updates during implementation (not edited now):

- `docs/architecture/` — new data-model documentation (module responsibilities, data flow). Currently not present/insubstantial; creation justified.
- `docs/development/DEVELOPMENT_LOG.md` — record 2.2.1 completion when implemented.
- `docs/MASTER_DEVELOPMENT_ROADMAP.md` — mark 2.2.1 status; update Stage 2 progress.
- `docs/development/UNRESOLVED_QUESTIONS.md` — UQ-003 (data model) may be partially addressed; UQ-008 is now resolved (file inspected).
- `docs/science/REVIEW-002-kepler10b-dataset.md` — may be updated with verified FITS findings (currently documentation-derived per the log).

Documents that should remain unchanged:
- Foundation documents (read-only).
- Decision records (DEC-001/002/003/005/006) — no change needed; this design operates within them.
- AGENTS.md — no change needed.

---

## Verification Summary

| Item | Status |
|---|---|
| Repository inspected | Verified (source, tests, decisions, log read) |
| FITS file accessed read-only | Verified (astropy 8.0.2; 3 HDUs; LIGHTCURVE 476×20) |
| Column names/types/units | Verified (all 20 columns) |
| Time convention | Verified (BJD-2454833, TDB, d, SOLARSYSTEM) |
| Quality flags | Verified (37 nonzero rows; values 0/64/128/8192/8320/12352/32800) |
| Non-finite values | Verified (SAP 4 rows; PDCSAP 7 rows; PSF_CENTR all 476) |
| SAP vs PDCSAP distinction | Verified (different non-finite patterns, different ranges) |
| Test baseline | 176 passed, 0 failed (reported, not re-run in this session) |

---

## Completion Statement

This planning report is complete. **Nothing has been implemented, created, or modified.** The proposed design (Sections 3–5) is specific enough to be reviewed and translated into a focused BUILD task for 2.2.2 (FITS import) once approved.

I am stopping here and awaiting your review and explicit authorization before any BUILD-mode work or proceeding to Subtask 2.2.2.



# REVIEW OF PLAN

# Review — Subtask 2.2.1 PLAN Report

The report is thorough and establishes a reasonable foundation for the light-curve data model. However, I would not approve it as implementation-ready without a few corrections and clarifications.

There are two separate issues:

1. The repository snapshot does not fully match the implementation state described in the report.
2. The proposed data model contains several inconsistencies that should be resolved before moving into 2.2.2.

The overall direction is sound: keep the scientific dataset independent of project metadata, preserve original measurements, retain time conventions and uncertainties, and defer project integration to 2.2.3.

## 1. Repository verification discrepancy

Snapshot does not match reported state

I inspected the attached ZIP rather than assuming it represented the current Windows working tree.

The snapshot contains:

- `SCHEMA_VERSION = 1` in `src/project_model.py`.
- No `owner` or `roles` fields in the snapshot's project model.
- A development log ending with the earlier 2.1.6 work.
- No evidence of the reported D4 implementation or the 176-test baseline.

The snapshot therefore appears to predate the D4 changes described in your report.

This does not establish that the D4 implementation is incorrect. It means I cannot independently verify the current working-tree state or the reported test results from this ZIP.

For the 2.2.1 design review, I can still assess the architectural requirements and the proposed model.

## 2. Issues in the proposed model

These are the corrections I recommend before approving the design.

### A. Uncertainties must be optional

Needs correction

The report currently defines:

```
uncertainties: np.ndarray
```

as a required field on `MeasurementColumn`.

However, its own validation design says:

- Missing uncertainties should produce a warning.
- A measurement column without uncertainties can still be usable.
- Different datasets may have different levels of available information.

These requirements contradict one another.

Recommendation: Make uncertainties optional:

```
uncertainties: np.ndarray | None = None
```

When available, uncertainty arrays must have the same length as their corresponding measurements.

This is important because the application should not reject an otherwise usable light curve simply because its source does not provide uncertainty measurements.

It also preserves the ability to distinguish an unknown uncertainty from a measured uncertainty of zero.

### B. Quality flags and cadence numbers should not be universally required

Needs correction

The proposed model requires:

```
quality_flags: list[int]cadence_numbers: list[int]
```

But these are not universal features of astronomical time-series data.

Kepler provides both. Other missions and ground-based observations may use different identifiers or provide no equivalent quality-flag column.

The report also explicitly aims to support other missions.

Recommendation:

- Make `quality_flags` optional.
- Make `cadence_numbers` optional.
- When present, require their lengths to match the observation count.
- Preserve the original values and do not interpret unknown quality systems automatically.

This avoids accidentally making a Kepler-oriented model mandatory for every future light-curve importer.

### C. Time validation contains a contradiction

The report says:

- `TimeInfo.reference` is optional.
- `TimeInfo.time_scale` is optional.
- Missing or ambiguous conventions should generate warnings.
- Model validation requires the unit/reference/scale to be present whenever time values exist.

Those statements cannot all be true.

Recommendation: Separate structural requirements from scientific completeness.

| Field           | Model requirement                                                                         |
| --------------- | ----------------------------------------------------------------------------------------- |
| Time values     | Required                                                                                  |
| Time unit       | Required as a field, but an explicitly unknown/empty value needs a defined representation |
| Reference epoch | Optional                                                                                  |
| Time scale      | Optional                                                                                  |
| Reference frame | Optional                                                                                  |
| Start/stop      | Optional                                                                                  |
| Resolution      | Optional                                                                                  |

Missing reference or scale information should be recorded as a validation warning, not automatically prevent construction.

This follows Foundation §3.4.3, which requires preservation of original timestamps and identification of ambiguous time information.

### D. Source-file availability should be calculated dynamically

The report correctly identifies that a source file may be moved or deleted.

However, it includes:

```
file_available: bool
```

as a field in `DatasetSource`.

This risks storing stale information.

Recommendation: Do not treat availability as persistent source metadata.

Determine availability when needed by checking the stored path. A property or separate availability-check function would be appropriate.

The original path and optional checksum remain useful provenance information.

### E. Observation count and non-finite counts need clearer treatment

Two fields deserve attention:

```
n_observations: intn_nonfinite: int
```

Both can be derived from the underlying arrays.

For example:

- `n_observations` can be obtained from the length of the time array.
- `n_nonfinite` can be obtained from the measurement values.

Storing derived counts creates the possibility of inconsistent metadata if the underlying arrays change.

Recommendation: Prefer calculated properties unless there is a specific reason to store them.

If they are stored, validation must ensure they always agree with the underlying arrays.

### F. Preservation of original measurements needs an explicit rule

The report repeatedly states that original measurements must not be modified.

However, NumPy arrays are mutable.

The model therefore needs a clear ownership rule:

- Does the model copy incoming arrays?
- Can external code modify the arrays after construction?
- Are arrays considered immutable once imported?
- How are derived measurements distinguished from original measurements?

I recommend that construction copy incoming arrays so that modifying the original FITS-derived arrays outside the model cannot silently alter the dataset.

The implementation should also document whether callers are allowed to modify the arrays held by the model.

This is particularly important for the future normalization and detrending operations.

Foundation §5.3 establishes the requirement to preserve original observations and distinguish derived datasets.

## 3. Additional architectural considerations

### Serialization

The report says the model will use NumPy arrays but should be serializable without requiring Astropy.

That is reasonable.

However, NumPy arrays are not directly JSON serializable.

The model should have a clearly defined conversion interface, such as:

- `to_dict()`: converts arrays into JSON-compatible lists and preserves metadata.
- `from_dict()`: reconstructs the model and its arrays.

This is not the same as implementing project persistence.

It is simply a model-level serialization contract that 2.2.3 can use later.

### Source identity

The example uses:

```
source_id = "KIC 11904151"
```

This identifies the astronomical target, not necessarily the individual source file or archive product.

A target can have many observations and many FITS files.

I recommend distinguishing:

- Dataset identity: the imported dataset's UUID.
- Target identity: the astronomical object identifier.
- Source identity: the originating archive/product identifier, when available.
- Source-file identity: filename, path and optional checksum.

This will matter when multiple quarters or observations of the same target are imported.

### Validation findings

The `ValidationReport` and `ValidationFinding` structures are useful and should remain.

One additional consideration: row indices should consistently use zero-based indexing internally, with any conversion for user-facing display handled separately.

That will avoid confusion when relating findings to NumPy arrays and Python indexing.

## 4. The four decisions requiring your approval

The report identifies four decisions. I would resolve them as follows.

| Decision                          | My recommendation      | Reason                                                                           |
| --------------------------------- | ---------------------- | -------------------------------------------------------------------------------- |
| Module location                   | `src/light_curve.py`   | Fits the existing flat `src/` structure and avoids premature package complexity. |
| Quality flags and cadence numbers | NumPy arrays, optional | Consistent numeric representation, while accommodating other missions.           |
| Measurement uncertainties         | Optional NumPy arrays  | Not every dataset supplies uncertainties.                                        |
| Checksum                          | Optional string        | Useful provenance, but not necessary for every imported file.                    |

There are two additional details I would settle:

Source path: Keep the original file path required for this initial local-file import workflow. The original file must remain externally referenced, not copied or modified. A future source type can accommodate datasets without a local source file.

Array mutability: Copy incoming arrays during model construction and document the model's mutation policy. Original imported measurements must not be silently altered.

## 5. Architecture and scope assessment

The overall separation of responsibilities is correct.

2.2.1 — Scientific data model

`LightCurveDataset`, `DatasetSource`, `TimeInfo`, `MeasurementSeries`, `MeasurementColumn`, `ValidationReport`, `ValidationFinding`

2.2.2 — FITS importer

Reads actual FITS files, identifies the appropriate HDU, extracts measurements and metadata, and constructs the data model.

2.2.3 — Project integration

Associates datasets with projects and implements provisional persistence.

2.2.4 — Testing and completion

Integration verification, documentation and end-to-end testing.

I agree with keeping these boundaries.

In particular, do not introduce FITS reading, project persistence, GUI functionality or BLS analysis into 2.2.1.

The Foundation supports this direction:

- §3.4.1 — Photometric data representation and examination.
- §3.4.3 — Time systems and temporal data handling.
- §4.4 — Scientific data formats and standards.
- §4.5 — Data retrieval and import.
- §4.6–4.8 — Provenance, metadata and data quality.
- §5.3 — Original data preservation and transformation safeguards.
- §5.6 — Validation and quality control.

One documentation consideration: the roadmap and development log should be updated when the relevant implementation work is completed. The Foundation remains read-only.

## 6. Final assessment

Overall architecture accepted in principle

| Area                      | Assessment               |
| ------------------------- | ------------------------ |
| FITS inspection           | Sufficiently detailed    |
| Scientific data model     | Sound overall structure  |
| Project separation        | Correct                  |
| Time representation       | Needs clarification      |
| Measurement uncertainties | Needs correction         |
| Quality flags/cadence     | Needs correction         |
| Source provenance         | Minor clarification      |
| Validation architecture   | Good                     |
| Serialization             | Needs explicit interface |
| Future compatibility      | Good                     |
| Subtask boundaries        | Correct                  |

My recommendation is to make these corrections in the 2.2.1 design before implementation.

There is no reason to restart the research or request another comprehensive PLAN report. The investigation has already established the necessary foundation.

The next step should be a focused revision of the existing 2.2.1 PLAN report, resolving the inconsistencies and recording the design choices.

Once that is settled, we can move directly to the 2.2.1 BUILD task.

I would keep the implementation deliberately small. The objective is a reliable, reusable scientific data model that the FITS importer can use—not a universal astronomy data framework.


# REVISION PROMPT

# TASK — Refine Subtask 2.2.1 Data-Model Design Requirements

## Mode: PLAN DOCUMENT REVISION ONLY

You are revising the existing planning documentation for:

**Subtask 2.2.1 — FITS Inspection and Data-Model Design**

The initial investigation has been completed and reviewed. A detailed PLAN report exists, and the design direction is established.

The review identified several inconsistencies in the proposed data model that must be resolved before the implementation design is approved.

Your task is to incorporate these corrections into the existing planning documentation.

**Do not restart the original investigation. Do not request another comprehensive PLAN report. Do not implement code.**

---

## 1. Files and instructions

Repository:
`C:\Code\New_Project`

Read and follow:
- `AGENTS.md`
- `docs/README.md`
- `docs/MASTER_DEVELOPMENT_ROADMAP.md`
- `docs/development/DEVELOPMENT_LOG.md`
- `docs/development/UNRESOLVED_QUESTIONS.md`

Read-only architectural references:
- `docs/Foundation/0_index.md`
- `docs/Foundation/3.4_Photometry, Transits and Time-Series Analysis.md`
- Relevant detailed Foundation sections covering data formats, import, provenance, data quality, processing safeguards, and validation.

Primary planning documents:

1. `docs/planning/Stage 2+ work planning aka overviews and prompts/Stage 2_n_n planning/stage 2_2_n planning/task 2.2.1 FITS inspection and data-model design OVERVIEW.md`

2. `docs/planning/Stage 2+ work planning aka overviews and prompts/Stage 2_n_n planning/stage 2_2_n planning/task 2.2.1 FITS inspection and data-model design PROMPTING.md`

The PROMPTING document contains two separate sections:
- PLAN MODE PROMPT
- BUILD MODE PROMPT

Pay particular attention to preserving their separation.

## 2. Scope of this revision

Modify the existing **PLAN MODE PROMPT** so that it accurately guides the final design investigation and resolves the inconsistencies identified in the review.

Review the OVERVIEW document for contradictions with the corrected design requirements.

If the OVERVIEW needs corresponding corrections to avoid contradicting the revised PLAN prompt, update only the relevant sections.

Do not rewrite either document wholesale.

Do not modify the BUILD MODE PROMPT during this task. It will be revised separately after the design has been finalized and approved.

Do not modify:
- Source code.
- Tests.
- Foundation documents.
- Decision records.
- Roadmap.
- Development log.
- Unresolved questions register.
- Subtasks 2.2.2, 2.2.3 or 2.2.4 documentation.

## 3. Required design corrections

### A. Measurement uncertainties

The current proposal treats uncertainties as mandatory despite stating that datasets without uncertainties should remain usable.

Correct this inconsistency.

Required design direction:

- Uncertainties must be optional.
- Represent absence explicitly, preferably using `None`.
- When provided, uncertainty arrays must align with their corresponding measurement arrays.
- Missing uncertainties should generate an appropriate validation warning.
- A missing uncertainty must not invalidate an otherwise usable measurement series.
- An unknown uncertainty must remain distinguishable from a measured zero uncertainty.

### B. Quality flags and cadence identifiers

These must not be universal mandatory requirements.

Required design direction:

- Both should be optional.
- NumPy arrays are the preferred representation for numeric data.
- When present, their lengths must match the observation count.
- Preserve original values without interpreting unfamiliar quality systems.
- Do not impose Kepler-specific requirements on other missions.

### C. Time representation and validation

Resolve the contradiction between optional time metadata and validation rules that currently require it.

Required design direction:

| Field | Requirement |
|---|---|
| Time values | Required |
| Time unit | Explicitly represented; unknown units must be distinguishable |
| Reference epoch | Optional |
| Time scale | Optional |
| Reference frame | Optional |
| Start | Optional |
| Stop | Optional |
| Resolution | Optional |
| Format hint | Optional |

Missing reference epochs or time scales should generate validation warnings where scientifically relevant.

Do not invent default time conventions.

The model must preserve numerical time values and their interpretation separately.

### D. Source-file availability

Do not persist `file_available` as authoritative metadata.

The availability of an external file must be determined dynamically when required.

Retain:
- Original filename.
- Original path.
- Optional checksum.
- Available source/archive metadata.

A dynamic property or separate availability-check function may be considered, but do not introduce unnecessary infrastructure.

### E. Derived counts

Review:
- `n_observations`
- `n_nonfinite`

Prefer calculated properties where values can be derived reliably from underlying arrays.

If either is stored, define how consistency is guaranteed.

Do not maintain redundant metadata without justification.

### F. Array ownership and mutation

The design must explicitly establish how original measurement arrays are protected.

Required design direction:

- Copy incoming NumPy arrays during model construction.
- External modification of the original input arrays must not silently alter the dataset.
- Document whether model-owned arrays are mutable or protected from modification.
- Preserve original imported measurements.
- Future transformations must produce separate derived measurements rather than overwrite originals.

Do not introduce a complicated immutability framework unless justified.

### G. Serialization

Establish an explicit model-level serialization interface.

Recommended interface:

- `to_dict()` converts the model into a JSON-compatible representation, including NumPy arrays.
- `from_dict()` reconstructs the model and its arrays.

Preserve:
- Measurement values.
- Uncertainties.
- Units.
- Time conventions.
- Source information.
- Quality flags and cadence identifiers.
- Validation findings.
- Original-versus-derived distinctions, where represented.

This is a model-level conversion contract only.

Do not implement persistence, database storage, project integration, or file-writing workflows.

### H. Source identity

Clearly distinguish:

1. Dataset identity — unique identity of the imported dataset.
2. Target identity — the astronomical object being observed.
3. Source identity — originating archive or archive-product identifier, where available.
4. Source-file identity — filename, path and optional checksum.

A target may have multiple datasets, observations, quarters or archive products.

Do not use an astronomical target identifier as though it uniquely identifies an imported dataset or source file.

### I. Validation findings

Retain the proposed `ValidationReport` and `ValidationFinding` structures.

Clarify:
- Stable machine-readable finding codes.
- Human-readable messages.
- Severity.
- Optional affected column.
- Optional affected row indices.

Use zero-based row indices internally.

Distinguish structural errors from scientific-data warnings and informational findings.

Preserve non-finite values rather than silently discarding observations.

## 4. Architectural boundaries

The following remain established requirements:

- The scientific dataset model is independent of `ProjectMetadata`.
- Project metadata must not contain measurement arrays.
- No ownership or permission metadata is duplicated in the scientific dataset model.
- No PySide6 dependency.
- No FITS-reading dependency in the core model.
- NumPy and standard-library types are sufficient for the model.
- Astropy `Time` may be constructed later for computation, but should not be required for basic model construction or serialization.
- No permanent storage architecture is introduced.
- No project association is implemented.
- No FITS importer is implemented.

The proposed module location remains a recommendation:

`src/light_curve.py`

Confirm that this is consistent with the actual repository structure. Do not create the module during this task.

## 5. Decisions and approval boundaries

Do not silently convert recommendations into approved decisions.

The revised design should clearly distinguish:

- Existing approved architectural decisions.
- Requirements established by the Foundation.
- Verified repository and FITS findings.
- Design recommendations.
- Decisions still requiring explicit user approval.

The following recommendations should be evaluated and presented clearly:

| Design question | Current recommendation |
|---|---|
| Module location | `src/light_curve.py` |
| Numeric arrays | NumPy arrays |
| Quality flags | Optional NumPy array |
| Cadence identifiers | Optional NumPy array |
| Uncertainties | Optional NumPy array |
| Checksum | Optional string |
| Source path | Required for the initial local-file workflow |
| Array construction | Copy incoming arrays |
| Serialization | `to_dict()` / `from_dict()` |

Do not invent additional approval requirements for routine implementation details.

If a recommendation is sufficiently supported by existing architectural authority, explain that rather than creating an unnecessary approval gate.

## 6. Preserve the original FITS investigation

The existing inspection findings must remain intact unless a specific factual discrepancy is discovered.

The verified dataset findings include:

- Three HDUs.
- LIGHTCURVE extension: 476 observations and 20 columns.
- TIME uses days relative to BJD 2454833.
- Time scale is TDB.
- Time reference frame is SOLARSYSTEM.
- SAP_FLUX has four non-finite measurements.
- PDCSAP_FLUX has seven non-finite measurements.
- SAP_FLUX and PDCSAP_FLUX remain independently identifiable.
- PSF_CENTR1 and PSF_CENTR2 are entirely non-finite.
- Thirty-seven observations have nonzero SAP_QUALITY values.

These findings demonstrate why the model must preserve missingness, column identity, and original observations.

Do not replace the real dataset with synthetic data in the actual application workflow.

## 7. Required output

After revising the planning documentation, provide a concise report containing:

1. Files inspected.
2. Files modified.
3. Exact sections revised.
4. How each of the nine design corrections was addressed.
5. Remaining decisions requiring user approval.
6. Any conflicts between the OVERVIEW and PLAN prompt that remain.
7. Confirmation that the BUILD prompt was left untouched.
8. Confirmation that no source code or tests were modified.

Do not claim implementation completion.

Do not run implementation tests because no implementation is authorized.

## 8. Completion boundary

The objective is to produce a consistent, technically sound 2.2.1 planning specification.

Once the revised PLAN documentation is ready, stop and present it for user review.

**Do not proceed to BUILD mode. Do not start Subtask 2.2.2. Do not modify the BUILD prompt until the revised design has been reviewed and explicitly approved.**



# revised plan

Both the `edit` and `write` tools are restricted in Plan mode — they cannot modify files outside the plan directory (`C:\Users\brett\.opencode\plan`). The user's task explicitly requires modifying `PROMPTING.md` and `OVERVIEW.md` in the repository, which I cannot do from Plan mode.

Per the system instructions, I need to tell the user they need to switch agents to Build mode to authorize these file modifications. However, I can provide the complete revised content here so it's ready to apply once the mode is switched.

Here is the summary of all changes needed:

---

## Changes Required to PROMPTING.md (PLAN MODE PROMPT section only)

### 1. Section 3.A — Dataset identity and source information (lines 337–356)

**Replace with:**
- Add dataset/target/source/source-file identity distinction (correction H)
- Remove "Source-file availability" as a stored field; replace with dynamic determination guidance (correction D)

### 2. Section 3.B — Measurement representation (lines 358–385)

**Replace with:**
- Mark flux uncertainties as optional with `None` representation (correction A)
- Mark cadence numbers and data-quality flags as optional (correction B)
- Add array ownership/copying requirement (correction F)

### 3. Section 3.C — Time representation (lines 387–413)

**Replace with:**
- Add time field requirement table: values required, unit explicit, reference/scale/frame/start/stop/resolution/format_hint optional (correction C)
- Warnings for missing reference/scale, no default conventions

### 4. Section 3.D — Scientific units and measurement metadata (lines 415–439)

**Add:**
- Derived counts (n_observations, n_nonfinite) should be calculated properties, not stored redundantly (correction E)

### 5. Section 3.E — Validation and warnings (lines 441–472)

**Add:**
- ValidationReport/ValidationFinding structure: stable codes, human-readable messages, severity, optional column, optional zero-based row indices (correction I)

### 6. Section 3.F — Original and derived measurements (lines 474–486)

**Add:**
- Array ownership: copy incoming arrays during construction, document mutability policy (correction F)

### 7. New Section 3.G — Serialization interface (after 3.F)

**Add:**
- `to_dict()` / `from_dict()` model-level conversion contract (correction G)

### 8. BUILD MODE PROMPT section

**Unchanged** — must be preserved exactly as-is.

---

## Changes Required to OVERVIEW.md (Section 2 only)

### Section 2 — Design the light-curve data model

**Source information** — Replace "File availability" bullet with guidance that availability is determined dynamically, not persisted.

**Measurement data** — Mark "Measurement uncertainties", "Cadence identifiers", and "Data-quality flags" as optional.

**Add source identity distinction** — Clarify that dataset identity ≠ target identity ≠ source identity ≠ source-file identity.

---

## Confirmation

- **BUILD MODE PROMPT section:** Left untouched (as required).
- **Source code, tests, Foundation documents, decision records, roadmap, development log, unresolved questions register, subtasks 2.2.2/2.2.3/2.2.4:** Not modified.
- **No commits or pushes:** None made.

Please switch to Build mode so I can apply these changes to the actual repository files. Once in Build mode, I will make the targeted edits to `PROMPTING.md` and `OVERVIEW.md` as specified above.


*** me ***

wtf why is it tryuing to edit prompting and overview...

# review

Stop. Do not switch to Build mode.

Your task is NOT to edit PROMPTING.md, OVERVIEW.md, or any other repository document.

The purpose of this exercise is to finalize the technical design for Subtask 2.2.1 based on the PLAN report and subsequent architectural review.

Use the nine corrections provided in the review to resolve the outstanding inconsistencies in the proposed light-curve data model.

Produce a consolidated, finalized technical specification directly in your response.

The specification must cover:

1. Dataset, target, source and source-file identity.
2. DatasetSource structure and source availability.
3. TimeInfo structure and time-validation requirements.
4. MeasurementSeries and MeasurementColumn structures.
5. Optional measurement uncertainties.
6. Optional quality flags and cadence identifiers.
7. Array ownership, copying and mutability.
8. Derived counts and calculated properties.
9. ValidationReport and ValidationFinding.
10. Model-level serialization through to_dict() and from_dict().
11. Preservation of original measurements and separation of future derived measurements.
12. Module location and dependency boundaries.
13. Compatibility with the subsequent 2.2.2 FITS importer and 2.2.3 project integration.

For each proposed structure, identify its fields, types, requirements and validation rules.

Distinguish established architectural requirements from recommendations and decisions still requiring my approval.

Preserve the verified Kepler-10b FITS findings and the existing 2.2.1 scope boundaries.

Do not:
- Edit or create any files.
- Modify PROMPTING.md or OVERVIEW.md.
- Generate another PLAN prompt.
- Generate a BUILD prompt yet.
- Implement source code or tests.
- Reopen previously approved architecture decisions.
- Restart the original repository or FITS investigation.

The objective is to finish the technical design review so I can approve it and we can move directly to preparing the 2.2.1 BUILD prompt.

Present the complete consolidated specification and stop for review.




## reply w/ revision


# Subtask 2.2.1 — Finalized Light-Curve Data Model Specification

This specification consolidates the PLAN report findings and resolves all nine design corrections identified in the architectural review. Nothing has been implemented or modified.

---

## 1. Scope Boundaries

**In scope:** Design of the internal light-curve data model (`src/light_curve.py` recommended), its validation, serialization contract, and its relationship to the existing project metadata model.

**Out of scope:** FITS reading/importer (2.2.2), project association/persistence (2.2.3), testing and completion verification (2.2.4), visualization (2.3), BLS analysis (2.4), analysis records (2.5).

**Preserved architectural decisions:**
- DEC-001: Photometry/time-series as initial capability.
- DEC-002: Import of one light-curve format; original-file preservation (referenced by path, never copied/modified).
- DEC-003: Single-user local; no ownership/permission metadata in the scientific dataset model.
- DEC-005: BLS as initial operation (model must preserve time+flux+uncertainty).
- DEC-006: Python 3.13 + NumPy/SciPy/Astropy/Matplotlib stack.
- D6 deferred: permanent storage architecture deferred; model must be storage-independent.
- Foundation §3.4.1, §3.4.3, §4.4–4.8, §5.3, §5.6: photometric data representation, time systems, data formats, import, provenance, quality, original-data preservation, validation.

---

## 2. Identity Model

Four distinct identities must be maintained:

| Identity | Meaning | Example |
|---|---|---|
| **Dataset identity** | UUID uniquely identifying this imported dataset instance | `dataset_id` (UUID string) |
| **Target identity** | The astronomical object being observed | `target_object`: `"KIC 11904151"` |
| **Source identity** | Originating archive or archive-product identifier | `source_id`: `"MAST/STScI"` product ID |
| **Source-file identity** | Original filename, path, and optional checksum | `original_filename`, `original_file_path`, optional `checksum` |

**Rule:** An astronomical target identifier must **not** be used as though it uniquely identifies an imported dataset or source file. A target may have multiple datasets, observations, quarters, or archive products.

---

## 3. DatasetSource Structure

**Responsibility:** Identifies where the dataset came from; retains source-file provenance; does **not** persist source-file availability as authoritative metadata.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `original_filename` | `str` | Yes | Original file name |
| `original_file_path` | `str` | Yes | Absolute path to source file at import time (local-file workflow) |
| `archive` | `str` | No | Originating archive/resource (e.g., `"MAST/STScI"`) |
| `mission` | `str` | No | Mission (e.g., `"Kepler"`) |
| `instrument` | `str` | No | Instrument (e.g., `"Kepler Photometer"`) |
| `target_object` | `str` | No | Target object identifier (e.g., `"KIC 11904151"`) |
| `checksum` | `str` | No | File checksum for source identification (optional provenance) |

**Source-file availability:** Must **not** be stored as a `file_available` boolean field. Availability is determined dynamically when required, by checking the stored path at access time. A dynamic property or separate availability-check function may be considered, but no unnecessary infrastructure.

**Validation rule:** `original_file_path` is required for the initial local-file import workflow. A future source type (external archive, API retrieval) may accommodate datasets without a local source file — that is a 2.2.2/2.2.3 consideration, not a model change.

---

## 4. TimeInfo Structure

**Responsibility:** Preserves timestamps **and** their interpretation separately; never reduces timestamps to raw floats without context.

| Field | Type | Required | Validation Rule |
|---|---|---|---|
| `values` | `numpy.ndarray` (float64) | Yes | Required. Numerical timestamp values. |
| `unit` | `str` | Yes | Required as a field. Unknown/empty units must be distinguishable; unknown units generate a validation warning. |
| `reference` | `str` | No | Time reference/epoch (e.g., `"BJD - 2454833"`). Optional; missing generates warning where scientifically relevant. |
| `reference_value` | `float` | No | Numeric reference epoch (e.g., `2454833.0`). Optional. |
| `time_scale` | `str` | No | Time scale/system (e.g., `"TDB"`). Optional; missing generates warning where scientifically relevant. |
| `time_reference_frame` | `str` | No | Barycentric frame (e.g., `"SOLARSYSTEM"`). Optional. |
| `start` | `float` | No | TSTART / observation start. Optional. |
| `stop` | `float` | No | TSTOP / observation stop. Optional. |
| `resolution` | `float` | No | TIMEDEL / time resolution. Optional. |
| `format_hint` | `str` | No | e.g., `"BJD"`. Optional. |

**Validation rules:**
- Time values are required for construction.
- Time unit must be explicitly represented; unknown units are distinguishable (not silently defaulted).
- Reference epoch and time scale are optional; missing values produce validation warnings, not construction errors.
- No default time conventions are invented.
- Numerical time values and their interpretation (unit, reference, scale, frame) are preserved separately.

**Kepler-10b verified values:** `values` range 120.539–130.245, `unit="d"`, `reference="BJD - 2454833"`, `reference_value=2454833.0`, `time_scale="TDB"`, `time_reference_frame="SOLARSYSTEM"`, `start=120.52892942`, `stop=130.25561236`, `resolution=0.02043359821692`.

---

## 5. MeasurementSeries Structure

**Responsibility:** Holds named measurement columns, each a `MeasurementColumn` pairing values with uncertainties. Keyed by original column identity.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `series` | `dict[str, MeasurementColumn]` | Yes | Named measurement series (key = column identity, e.g., `"SAP_FLUX"`). |

**Constraint:** Keys must be unique column names. Each entry independently identifies its measurement column.

---

## 6. MeasurementColumn Structure

**Responsibility:** A single measurement column paired with its associated uncertainty, plus column metadata.

| Field | Type | Required | Validation Rule |
|---|---|---|---|
| `name` | `str` | Yes | Column identity (original FITS column name, e.g., `"SAP_FLUX"`). |
| `values` | `numpy.ndarray` (float64) | Yes | Measurement values. Non-finite values preserved, not removed. |
| `uncertainties` | `numpy.ndarray` (float62) \| `None` | No (optional, `None`) | 1-sigma uncertainties aligned with `values`. If provided, `len(uncertainties) == len(values)`. Missing = validation warning, not construction error. Unknown uncertainty distinguishable from measured zero. |
| `unit` | `str` | Yes | Measurement unit (e.g., `"e-/s"`). Unknown units distinguishable. |
| `description` | `str` | No | Column description (from FITS TTYPE/TCOMM). |

**Validation rules:**
- `len(values) == len(uncertainties)` when uncertainties provided.
- Missing uncertainties do not invalidate an otherwise usable series; generate a warning.
- Unknown uncertainty (None) is distinguishable from a measured zero uncertainty (array of 0.0 values).
- Non-finite values in `values` are preserved; count tracked via calculated property.

**Kepler-10b verified values:**
- `SAP_FLUX`: unit `"e-/s"`, 4 non-finite (cadences 703, 848, 950, 972), range ≈ 532355–532944 e-/s.
- `PDCSAP_FLUX`: unit `"e-/s"`, 7 non-finite (cadences 703, 790, 848, 914, 915, 950, 972), range ≈ 501346–501747 e-/s.
- SAP and PDCSAP remain independently identifiable and accessible (separate `MeasurementColumn` entries).

---

## 7. Optional Quality Flags and Cadence Identifiers

**Responsibility:** Per-observation quality flags and observation identifiers, both optional.

| Field | Type | Required | Validation Rule |
|---|---|---|---|
| `quality_flags` | `numpy.ndarray` (int) | No (optional) | If present, `len(quality_flags) == n_observations`. Original values preserved; unknown quality systems not interpreted automatically. |
| `cadence_numbers` | `numpy.ndarray` (int) | No (optional) | If present, `len(cadence_numbers) == n_observations`. Original values preserved; not required to be uniformly spaced. |

**Rules:**
- Neither is a universal mandatory requirement.
- When present, lengths must match observation count.
- Original values preserved without interpretation of unfamiliar quality systems.
- No Kepler-specific requirements imposed on other missions.
- Nonzero quality flags remain available (37 of 476 rows nonzero in Kepler-10b; values {0, 64, 128, 8192, 8320, 12352, 32800}). Do not assume all nonzero flags should cause observations to be discarded.

---

## 8. LightCurveDataset Structure

**Responsibility:** Top-level container for a single imported light-curve dataset. One instance per imported dataset. Independent of `ProjectMetadata` and of any project association.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `dataset_id` | `str` (UUID) | Yes | Stable identifier for this imported dataset. |
| `name` | `str` | Yes | User-visible dataset name. |
| `source` | `DatasetSource` | Yes | Source-file identity and provenance metadata. |
| `time` | `TimeInfo` | Yes | Time representation (values, unit, reference, scale, frame). |
| `measurements` | `MeasurementSeries` | Yes | The measurement columns. |
| `quality_flags` | `numpy.ndarray` (int) | No | Per-observation quality flags (optional, see §7). |
| `cadence_numbers` | `numpy.ndarray` (int) | No | Observation identifiers (optional, see §7). |
| `validation` | `ValidationReport` | Yes | Import/construction validation findings. |
| `imported_at` | `str` (ISO-8601) | Yes | Import timestamp. |
| `notes` | `str` | No | User annotations. |

**Relationships:** A `Project` may contain zero or more `LightCurveDataset` instances (association mechanism deferred to 2.2.3). For 2.2.1, the model is independent of projects entirely.

**Original-versus-derived distinction:** Original source measurements are stored as imported and never overwritten. Future derived/transformed measurements (normalized, detrended, filtered) are stored as separate `MeasurementColumn` entries with provenance metadata linking back to the source series. Processing operations (normalization, detrending, quality filtering, interpolation) are out of scope for 2.2.1.

---

## 9. Array Ownership, Copying, and Mutability

**Rule:** The model copies incoming NumPy arrays during construction.

- External modification of the original input arrays (e.g., FITS-derived arrays held by the importer) must **not** silently alter the dataset.
- Model-owned arrays are mutable by design (no complicated immutability framework), but the mutability policy must be documented so callers understand whether they may modify arrays held by the model.
- Future transformations must produce separate derived `MeasurementColumn` entries rather than overwriting originals.

**Rationale:** NumPy arrays are mutable; without an explicit copy rule, external code could silently corrupt imported data. This is particularly important for future normalization and detrending operations (Foundation §5.3: original data preservation and transformation safeguards).

---

## 10. Derived Counts and Calculated Properties

**Rule:** Prefer calculated properties over stored redundant counts.

| Derived Count | Derivation | Stored? |
|---|---|---|
| `n_observations` | Length of `time.values` array | No — calculated property |
| `n_nonfinite` | Count of non-finite values in a `MeasurementColumn.values` array | No — calculated property per column |

**Justification:** Storing derived counts creates the possibility of inconsistent metadata if underlying arrays change. If either is ever stored, validation must ensure agreement with underlying arrays. For 2.2.1, both are calculated.

---

## 11. ValidationReport and ValidationFinding

**ValidationReport** — Structured record of validation findings so the importer can report them consistently.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `errors` | `list[ValidationFinding]` | Yes | Conditions preventing dataset acceptance. |
| `warnings` | `list[ValidationFinding]` | Yes | Conditions permitting representation but flagged. |
| `info` | `list[ValidationFinding]` | Yes | Conditions preserved without modification. |

**ValidationFinding**

| Field | Type | Purpose |
|---|---|---|
| `code` | `str` | Stable machine-readable finding code. |
| `message` | `str` | Human-readable description. |
| `severity` | `str` (`"error"`/`"warning"`/`"info"`) | Severity level. |
| `column` | `str` | Affected column (optional). |
| `row_indices` | `list[int]` | Affected row indices, **zero-based** internally. |

**Distinctions:**
- Structural errors (array length mismatch, missing required fields) prevent construction.
- Scientific-data warnings (missing uncertainties, nonzero quality flags, unknown units, ambiguous time conventions) permit representation but are flagged.
- Informational findings (entirely empty column, all-nonfinite column) preserve context without modification.
- Non-finite values are preserved rather than silently discarded.

**Model-level vs. import-level validation:** Model-level validation checks internal consistency (length alignment, required fields, types). Import-level validation (2.2.2) checks source-data suitability (file readable, HDU present, required columns present). These remain separate.

---

## 12. Model-Level Serialization

**Interface:** `to_dict()` and `from_dict()` on `LightCurveDataset`.

| Method | Purpose |
|---|---|
| `to_dict()` | Converts the model into a JSON-compatible representation. NumPy arrays converted to JSON-compatible form (lists). Preserves measurement values, uncertainties, units, time conventions, source information, quality flags, cadence identifiers, validation findings, original-versus-derived distinctions. |
| `from_dict()` | Reconstructs the model and its arrays from the serialized representation. |

**Rules:**
- This is a model-level conversion contract only — not project persistence, database storage, or file-writing.
- Serialization must not lose scientific meaning: units, time reference/scale, and column identities stored as explicit strings.
- NumPy arrays are not directly JSON serializable; the conversion to lists is part of this contract.
- No PySide6 dependency; no astropy.fits dependency in the core model.

---

## 13. Module Location and Dependency Boundaries

**Recommended module location:** `src/light_curve.py` — consistent with the existing flat `src/` structure, avoids premature package complexity.

**Dependencies:**
- NumPy arrays + standard library types only.
- No PySide6 dependency.
- No `astropy.fits` dependency in the core model.
- `astropy.time.Time` may be constructed later for computation (e.g., BLS in 2.2.4), but is not required for basic model construction or serialization.

**Module responsibility table:**

| Module | Responsibility |
|---|---|
| `src/project_model.py` | Project metadata only (unchanged; not extended with measurement arrays). |
| `src/project_repository.py` | JSON persistence only (unchanged). |
| `src/project_service.py` | Project lifecycle only (unchanged). |
| `src/light_curve.py` (new, recommended) | Light-curve data model: `LightCurveDataset`, `DatasetSource`, `TimeInfo`, `MeasurementSeries`, `MeasurementColumn`, `ValidationReport`, `ValidationFinding`. No UI, no persistence, no FITS reading. |

**Separation of concerns preserved:**
- Project metadata (`ProjectMetadata`) — project-level: name, status, owner, roles, schema version 2.
- Scientific dataset (`LightCurveDataset`) — observation-level: measurements, time, source, validation.
- Source-file reference — in `DatasetSource.original_file_path`, not duplicated in project metadata.
- Validation findings — in `ValidationReport`, separate from measurements.
- Future analysis results — separate structure (deferred).

No ownership or permission metadata is duplicated inside the scientific dataset model. The application remains single-user local under DEC-003.

---

## 14. Compatibility with Subsequent Subtasks

**2.2.2 (FITS Import and Validation):**
- Importer reads FITS files, identifies the LIGHTCURVE HDU, extracts measurements and metadata, constructs `LightCurveDataset` instances, performs import-level validation.
- Model must be complete before importer implementation begins.
- Column mapping (Kepler `SAP_FLUX`, `PDCSAP_FLUX`, `SAP_QUALITY`, `CADENCENO`, `TIME`, etc.) happens in the importer, not the model — these are Kepler-specific conventions kept out of the general model.
- Time convention mapping (BJD-2454833, TDB, SOLARSYSTEM) happens in the importer; `TimeInfo` stores generic components.

**2.2.3 (Project Integration and Provisional Persistence):**
- Associates datasets with projects; decides how dataset references survive save/reopen.
- Needs a serializable model (provided by `to_dict()`/`from_dict()`) and a clear dataset–project association (to be defined).
- D6 deferred: provisional local-file approach only; no permanent storage architecture decision in 2.2.1.

**Potential overlap:** None, provided 2.2.1 stays strictly a data model (no FITS reading, no project association, no persistence).

**Recommended task boundaries remain appropriate:**
| Subtask | Responsibility |
|---|---|
| 2.2.2 | FITS import and validation |
| 2.2.3 | Project integration and provisional persistence |
| 2.2.4 | Testing, documentation, and completion verification |

---

## 15. Verified Kepler-10b FITS Findings (Preserved)

All findings directly verified against the actual file using `astropy.io.fits` (astropy 8.0.2), `mode='readonly'`:

- **3 HDUs:** PRIMARY (mission/target metadata), LIGHTCURVE (476 rows × 20 columns — the relevant light-curve HDU), APERTURE (12×10 pixel aperture mask with WCS).
- **TIME:** days relative to BJD 2454833, range 120.539–130.245, 0 non-finite, `TIMESYS=TDB`, `TIMEREF=SOLARSYSTEM`, `BJDREFI=2454833`.
- **SAP_FLUX vs PDCSAP_FLUX:** Independently identifiable, different non-finite patterns (4 vs 7 rows), different value ranges. Not interchangeable.
- **SAP_FLUX:** 4 non-finite (cadences 703, 848, 950, 972).
- **PDCSAP_FLUX:** 7 non-finite (cadences 703, 790, 848, 914, 915, 950, 972).
- **SAP_QUALITY:** 37 of 476 rows nonzero; values {0, 64, 128, 8192, 8320, 12352, 32800}.
- **PSF_CENTR1/PSF_CENTR2:** Entirely non-finite (all 476 rows) — confirms the model must handle columns that may be fully absent/invalid.
- **CADENCENO:** range 568–1043, spacing exactly 1.

These findings demonstrate why the model must preserve missingness, column identity, original observations, and optional quality/cadence fields.

---

## 16. Decisions Still Requiring User Approval

The following recommendations are presented for approval before proceeding to the 2.2.1 BUILD task:

| Design Question | Recommendation | Approval Required? |
|---|---|---|
| Module location | `src/light_curve.py` | Yes |
| Quality flags / cadence identifiers | Optional NumPy arrays | Yes |
| Measurement uncertainties | Optional NumPy arrays (`None` = absent) | Yes |
| Checksum field | Optional string | Yes |
| Source path | Required for initial local-file workflow | Yes (per DEC-002 original-file preservation) |
| Array construction | Copy incoming arrays during construction | Yes |
| Serialization | `to_dict()` / `from_dict()` model-level contract | Yes |
| Derived counts | Calculated properties (not stored) | Yes |

**Approved decisions (relied upon, not changed):** DEC-001/002/003/005/006; D6 deferred.

**Questions that can safely remain deferred:**
- How datasets are associated with projects (2.2.3).
- Exact persistence format/location (D6 deferred; 2.2.3 provisional).
- Whether source files are ever copied into projects.
- Analysis-record model for derived measurements (§5.5).
- Units library choice (plain strings recommended for serialization simplicity).

---

This specification is complete and ready for review. Once approved, it can be translated directly into a focused 2.2.1 BUILD task. No files were created, modified, or deleted during this planning exercise.



# revision review, should be greenlight after this next review.

The specification is substantially complete and resolves the earlier design inconsistencies. I would approve the overall architecture, but I recommend correcting several details before treating it as the final BUILD specification.

## Required corrections

1\. Typo in uncertainty type: Section 6 says `numpy.ndarray (float62)`. This should be `numpy.ndarray (float64)`.

2\. Clarify `MeasurementSeries` identity: Section 5 says the dictionary key is the original column identity, but Section 6 also gives each column a `name`. Require `key == MeasurementColumn.name` to prevent conflicting identities.

3\. Clarify dataset ID generation: State whether `dataset_id` is generated by the model using `uuid.uuid4()` when omitted, or must be supplied by the caller. I recommend generating it by default while allowing an explicit ID during reconstruction through `from_dict()`.

4\. Clarify array mutability: Copying incoming arrays prevents external references from changing the model, but model-owned arrays remain mutable. Therefore, calculated properties such as `n_nonfinite` must calculate their results from the current array contents rather than cache them.

5\. Clarify validation ownership: The model should enforce structural consistency, but it should not require callers to manually construct a complete `ValidationReport` before constructing a dataset. I recommend a default empty report, with model-level findings added during construction or validation.

6\. Clarify `imported_at`: Generate an ISO-8601 timestamp with timezone information by default. Preserve an explicitly supplied timestamp during reconstruction.

7\. Clarify unknown units: Use a consistent representation for unknown units. I recommend an empty string (`""`) rather than `None`, since the fields are defined as required strings.

8\. Clarify serialization: Specify that `to_dict()` returns ordinary Python values suitable for `json.dumps()`, and that `from_dict()` validates and reconstructs NumPy arrays. It should preserve `None` versus arrays, including arrays containing zero values.

## One architectural consideration

The proposed `source.original_file_path` is required for the initial local-file workflow. That is reasonable under DEC-002. Keep the requirement scoped to the current workflow rather than making the model fundamentally incapable of representing a future dataset without a local source file.

## Recommendation

Approve with corrections

The overall design is appropriate:

- `src/light_curve.py` is a reasonable location.
- Optional uncertainty, quality, and cadence arrays are appropriate.
- Original measurements and non-finite values remain preserved.
- The model is independent of FITS parsing, UI, project metadata, and persistence.
- `to_dict()` / `from_dict()` provide a useful boundary for 2.2.3.
- The Kepler-specific conventions remain in the importer rather than contaminating the general model.

Do not begin 2.2.2 yet. First incorporate these corrections into the finalized 2.2.1 specification, then review and approve the BUILD prompt.

# revision prompt

# Subtask 2.2.1 — Final Specification Corrections

**Mode: PLAN ONLY. Do not implement anything.**

Review the finalized Light-Curve Data Model Specification I just provided and incorporate the following eight corrections.

### Required corrections

1. **Uncertainty type:** Correct `float62` to `float64` in `MeasurementColumn.uncertainties`.

2. **Measurement column identity:** Require each `MeasurementSeries` dictionary key to match its contained `MeasurementColumn.name`.

3. **Dataset ID generation:** Recommend generating `dataset_id` using `uuid.uuid4()` when creating a new dataset, while allowing an explicitly supplied ID during reconstruction through `from_dict()`.

4. **Array mutability:** Incoming arrays must be copied during construction. Model-owned arrays remain mutable. Calculated properties such as `n_nonfinite` must calculate their values from the current arrays rather than cache them.

5. **Validation ownership:** `LightCurveDataset` should be constructible without requiring callers to manually supply a complete `ValidationReport`. Recommend a default empty report, with structural validation performed by the model.

6. **Import timestamp:** Generate an ISO-8601 timestamp with timezone information when `imported_at` is omitted. Preserve explicitly supplied timestamps during reconstruction.

7. **Unknown units:** Use an empty string (`""`) to represent unknown units for required string fields. Do not silently substitute a physical unit.

8. **Serialization:** Specify that:
   - `to_dict()` returns ordinary Python values compatible with `json.dumps()`.
   - NumPy arrays are converted to lists.
   - `from_dict()` reconstructs NumPy arrays and validates the resulting model.
   - `None` and arrays containing zero values remain distinguishable.

### Additional clarification

Keep `DatasetSource.original_file_path` required for the initial local-file workflow under DEC-002. Do not make the current model unnecessarily dependent on local files as a permanent architectural restriction. Future source types can be considered separately.

### Instructions

- Preserve all previously established scope boundaries and architectural decisions.
- Do not introduce new features or expand the scope.
- Do not modify any repository files.
- Do not modify the original OVERVIEW or PROMPTING documents.
- Do not begin implementation.
- Do not generate the 2.2.2 importer prompt.
- Incorporate the corrections into one consolidated, revised technical specification.
- Identify any remaining ambiguities or decisions that genuinely require my approval.

**Deliverable:** Present the complete revised Subtask 2.2.1 specification directly in your response, followed by a concise list of any remaining approval decisions. Stop and wait for my review.


# PLAN REVISION 

# Subtask 2.2.1 — Revised Light-Curve Data Model Specification

This is the complete consolidated specification incorporating all eight corrections plus the additional clarification. Nothing has been implemented; no repository files were modified.

---

## 1. Scope Boundaries

**In scope:** Design of the internal light-curve data model (`src/light_curve.py` recommended), its validation, serialization contract, and its relationship to the existing project metadata model.

**Out of scope:** FITS reading/importer (2.2.2), project association/persistence (2.2.3), testing and completion verification (2.2.4), visualization (2.3), BLS analysis (2.4), analysis records (2.5).

**Preserved architectural decisions:**
- DEC-001: Photometry/time-series as initial capability.
- DEC-002: Import of one light-curve format; original-file preservation (referenced by path, never copied/modified).
- DEC-003: Single-user local; no ownership/permission metadata in the scientific dataset model.
- DEC-005: BLS as initial operation (model must preserve time+flux+uncertainty).
- DEC-006: Python 3.13 + NumPy/SciPy/Astropy/Matplotlib stack.
- D6 deferred: permanent storage architecture deferred; model must be storage-independent.
- Foundation §3.4.1, §3.4.3, §4.4–4.8, §5.3, §5.6: photometric data representation, time systems, data formats, import, provenance, quality, original-data preservation, validation.

---

## 2. Identity Model

Four distinct identities must be maintained:

| Identity | Meaning | Example |
|---|---|---|
| **Dataset identity** | UUID uniquely identifying this imported dataset instance | `dataset_id` (UUID string) |
| **Target identity** | The astronomical object being observed | `target_object`: `"KIC 11904151"` |
| **Source identity** | Originating archive or archive-product identifier | `source_id`: `"MAST/STScI"` product ID |
| **Source-file identity** | Original filename, path, and optional checksum | `original_filename`, `original_file_path`, optional `checksum` |

**Rule:** An astronomical target identifier must **not** be used as though it uniquely identifies an imported dataset or source file. A target may have multiple datasets, observations, quarters, or archive products.

---

## 3. DatasetSource Structure

**Responsibility:** Identifies where the dataset came from; retains source-file provenance; does **not** persist source-file availability as authoritative metadata.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `original_filename` | `str` | Yes | Original file name |
| `original_file_path` | `str` | Yes | Absolute path to source file at import time (initial local-file workflow under DEC-002) |
| `archive` | `str` | No | Originating archive/resource (e.g., `"MAST/STScI"`) |
| `mission` | `str` | No | Mission (e.g., `"Kepler"`) |
| `instrument` | `str` | No | Instrument (e.g., `"Kepler Photometer"`) |
| `target_object` | `str` | No | Target object identifier (e.g., `"KIC 11904151"`) |
| `checksum` | `str` | No | File checksum for source identification (optional provenance) |

**Source-file availability:** Must **not** be stored as a `file_available` boolean field. Availability is determined dynamically when required, by checking the stored path at access time. A dynamic property or separate availability-check function may be considered, but no unnecessary infrastructure.

**Clarification:** `original_file_path` is required for the initial local-file workflow under DEC-002. The model must not be unnecessarily dependent on local files as a permanent architectural restriction; future source types (external archive, API retrieval) can be considered separately without requiring changes to this model structure.

**Validation rule:** `original_file_path` is required for construction in the initial local-file import workflow.

---

## 4. TimeInfo Structure

**Responsibility:** Preserves timestamps **and** their interpretation separately; never reduces timestamps to raw floats without context.

| Field | Type | Required | Validation Rule |
|---|---|---|---|
| `values` | `numpy.ndarray` (float64) | Yes | Required. Numerical timestamp values. |
| `unit` | `str` | Yes | Required as a field. Empty string `""` represents unknown units; unknown units must be distinguishable and generate a validation warning. No physical unit is silently substituted. |
| `reference` | `str` | No | Time reference/epoch (e.g., `"BJD - 2454833"`). Optional; missing generates warning where scientifically relevant. Empty string `""` if unknown. |
| `reference_value` | `float` | No | Numeric reference epoch (e.g., `2454833.0`). Optional. |
| `time_scale` | `str` | No | Time scale/system (e.g., `"TDB"`). Optional; missing generates warning where scientifically relevant. Empty string `""` if unknown. |
| `time_reference_frame` | `str` | No | Barycentric frame (e.g., `"SOLARSYSTEM"`). Optional. Empty string `""` if unknown. |
| `start` | `float` | No | TSTART / observation start. Optional. |
| `stop` | `float` | No | TSTOP / observation stop. Optional. |
| `resolution` | `float` | No | TIMEDEL / time resolution. Optional. |
| `format_hint` | `str` | No | e.g., `"BJD"`. Optional. |

**Validation rules:**
- Time values are required for construction.
- Time unit must be explicitly represented; unknown units are represented as `""` and are distinguishable. No physical unit is silently substituted.
- Reference epoch and time scale are optional; missing/unknown values produce validation warnings, not construction errors.
- No default time conventions are invented.
- Numerical time values and their interpretation (unit, reference, scale, frame) are preserved separately.

**Kepler-10b verified values:** `values` range 120.539–130.245, `unit="d"`, `reference="BJD - 2454833"`, `reference_value=2454833.0`, `time_scale="TDB"`, `time_reference_frame="SOLARSYSTEM"`, `start=120.52892942`, `stop=130.25561236`, `resolution=0.02043359821692`.

---

## 5. MeasurementSeries Structure

**Responsibility:** Holds named measurement columns, each a `MeasurementColumn` pairing values with uncertainties. Keyed by original column identity.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `series` | `dict[str, MeasurementColumn]` | Yes | Named measurement series. **Each dictionary key must match its contained `MeasurementColumn.name`.** |

**Validation rule:** For every entry `key -> column` in `series`, `key == column.name`. Keys must be unique column names. Each entry independently identifies its measurement column.

---

## 6. MeasurementColumn Structure

**Responsibility:** A single measurement column paired with its associated uncertainty, plus column metadata.

| Field | Type | Required | Validation Rule |
|---|---|---|---|
| `name` | `str` | Yes | Column identity (original FITS column name, e.g., `"SAP_FLUX"`). Must match the `MeasurementSeries` dictionary key. |
| `values` | `numpy.ndarray` (float64) | Yes | Measurement values. Non-finite values preserved, not removed. |
| `uncertainties` | `numpy.ndarray` (float64) \| `None` | No (optional, `None`) | 1-sigma uncertainties aligned with `values`. `None` = unknown/absent. If provided, `len(uncertainties) == len(values)`. Unknown uncertainty (`None`) is distinguishable from a measured zero uncertainty (array of `0.0` values). Missing uncertainties generate a validation warning but do not invalidate an otherwise usable series. |
| `unit` | `str` | Yes | Measurement unit (e.g., `"e-/s"`). Empty string `""` represents unknown units; unknown units are distinguishable. |
| `description` | `str` | No | Column description (from FITS TTYPE/TCOMM). |

**Validation rules:**
- `len(values) == len(uncertainties)` when uncertainties are not `None`.
- Missing uncertainties (`None`) do not invalidate an otherwise usable series; generate a warning.
- Unknown uncertainty (`None`) is distinguishable from a measured zero uncertainty (array of `0.0` values).
- Non-finite values in `values` are preserved; count tracked via calculated property.
- Unknown measurement units (`""`) are distinguishable from known units; no physical unit silently substituted.

**Kepler-10b verified values:**
- `SAP_FLUX`: unit `"e-/s"`, 4 non-finite (cadences 703, 848, 950, 972), range ≈ 532355–532944 e-/s.
- `PDCSAP_FLUX`: unit `"e-/s"`, 7 non-finite (cadences 703, 790, 848, 914, 915, 950, 972), range ≈ 501346–501747 e-/s.
- SAP and PDCSAP remain independently identifiable and accessible (separate `MeasurementColumn` entries).

---

## 7. Optional Quality Flags and Cadence Identifiers

**Responsibility:** Per-observation quality flags and observation identifiers, both optional.

| Field | Type | Required | Validation Rule |
|---|---|---|---|
| `quality_flags` | `numpy.ndarray` (int) | No (optional) | If present, `len(quality_flags) == n_observations`. Original values preserved; unknown quality systems not interpreted automatically. |
| `cadence_numbers` | `numpy.ndarray` (int) | No (optional) | If present, `len(cadence_numbers) == n_observations`. Original values preserved; not required to be uniformly spaced. |

**Rules:**
- Neither is a universal mandatory requirement.
- When present, lengths must match observation count.
- Original values preserved without interpretation of unfamiliar quality systems.
- No Kepler-specific requirements imposed on other missions.
- Nonzero quality flags remain available (37 of 476 rows nonzero in Kepler-10b; values {0, 64, 128, 8192, 8320, 12352, 32800}). Do not assume all nonzero flags should cause observations to be discarded.

---

## 8. LightCurveDataset Structure

**Responsibility:** Top-level container for a single imported light-curve dataset. One instance per imported dataset. Independent of `ProjectMetadata` and of any project association.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `dataset_id` | `str` (UUID) | Yes | Stable identifier for this imported dataset. |
| `name` | `str` | Yes | User-visible dataset name. |
| `source` | `DatasetSource` | Yes | Source-file identity and provenance metadata. |
| `time` | `TimeInfo` | Yes | Time representation (values, unit, reference, scale, frame). |
| `measurements` | `MeasurementSeries` | Yes | The measurement columns. |
| `quality_flags` | `numpy.ndarray` (int) | No | Per-observation quality flags (optional). |
| `cadence_numbers` | `numpy.ndarray` (int) | No | Observation identifiers (optional). |
| `validation` | `ValidationReport` | Yes | Import/construction validation findings. Default empty report if not supplied; structural validation performed by the model. |
| `imported_at` | `str` (ISO-8601) | Yes | Import timestamp. Generated with timezone info if omitted; explicitly supplied timestamps preserved during `from_dict()` reconstruction. |
| `notes` | `str` | No | User annotations. |

**Relationships:** A `Project` may contain zero or more `LightCurveDataset` instances (association mechanism deferred to 2.2.3). For 2.2.1, the model is independent of projects entirely.

**Original-versus-derived distinction:** Original source measurements are stored as imported and never overwritten. Future derived/transformed measurements (normalized, detrended, filtered) are stored as separate `MeasurementColumn` entries with provenance metadata linking back to the source series. Processing operations (normalization, detrending, quality filtering, interpolation) are out of scope for 2.2.1.

**Validation ownership:** `LightCurveDataset` is constructible without requiring callers to manually supply a complete `ValidationReport`. A default empty `ValidationReport` is used when none is supplied. Structural validation (length alignment, required fields, types) is performed by the model during construction and by `from_dict()` during reconstruction.

---

## 9. Array Ownership, Copying, and Mutability

**Rule:** The model copies incoming NumPy arrays during construction.

- External modification of the original input arrays (e.g., FITS-derived arrays held by the importer) must **not** silently alter the dataset.
- Model-owned arrays remain mutable. No complicated immutability framework is introduced; the mutability policy is documented so callers understand whether they may modify arrays held by the model.
- Calculated properties such as `n_nonfinite` must calculate their values from the current arrays rather than cache them. They are not stored.
- Future transformations must produce separate derived `MeasurementColumn` entries rather than overwriting originals.

**Rationale:** NumPy arrays are mutable; without an explicit copy rule, external code could silently corrupt imported data. This is particularly important for future normalization and detrending operations (Foundation §5.3: original data preservation and transformation safeguards).

---

## 10. Derived Counts and Calculated Properties

**Rule:** Prefer calculated properties over stored redundant counts.

| Derived Count | Derivation | Stored? |
|---|---|---|
| `n_observations` | Length of `time.values` array | No — calculated property |
| `n_nonfinite` | Count of non-finite values in a `MeasurementColumn.values` array | No — calculated property per column, computed from current array |

**Justification:** Storing derived counts creates the possibility of inconsistent metadata if underlying arrays change. Both are calculated properties that read from the current arrays; they are never cached or stored independently.

---

## 11. ValidationReport and ValidationFinding

**ValidationReport** — Structured record of validation findings so the importer can report them consistently.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `errors` | `list[ValidationFinding]` | Yes | Conditions preventing dataset acceptance. |
| `warnings` | `list[ValidationFinding]` | Yes | Conditions permitting representation but flagged. |
| `info` | `list[ValidationFinding]` | Yes | Conditions preserved without modification. |

**ValidationFinding**

| Field | Type | Purpose |
|---|---|---|
| `code` | `str` | Stable machine-readable finding code. |
| `message` | `str` | Human-readable description. |
| `severity` | `str` (`"error"`/`"warning"`/`"info"`) | Severity level. |
| `column` | `str` | Affected column (optional). |
| `row_indices` | `list[int]` | Affected row indices, **zero-based** internally. |

**Distinctions:**
- Structural errors (array length mismatch, missing required fields, key/name mismatch in `MeasurementSeries`) prevent construction.
- Scientific-data warnings (missing uncertainties, nonzero quality flags, unknown units, ambiguous time conventions) permit representation but are flagged.
- Informational findings (entirely empty column, all-nonfinite column) preserve context without modification.
- Non-finite values are preserved rather than silently discarded.

**Model-level vs. import-level validation:** Model-level validation checks internal consistency (length alignment, required fields, types, key/name matching). Import-level validation (2.2.2) checks source-data suitability (file readable, HDU present, required columns present). These remain separate.

---

## 12. Model-Level Serialization

**Interface:** `to_dict()` and `from_dict()` on `LightCurveDataset`.

| Method | Specification |
|---|---|
| `to_dict()` | Returns ordinary Python values compatible with `json.dumps()`. NumPy arrays are converted to lists. Preserves measurement values, uncertainties, units, time conventions, source information, quality flags, cadence identifiers, validation findings, original-versus-derived distinctions. `None` uncertainties serialize as JSON `null`. Zero-value arrays serialize as arrays of zeros (distinguishable from `null`/`None`). |
| `from_dict()` | Reconstructs NumPy arrays from the serialized lists and validates the resulting model. `null` in JSON reconstructs to Python `None` for optional uncertainty fields. Arrays of zeros reconstruct to NumPy arrays containing zeros (distinguishable from `None`). Structural validation is performed on the reconstructed model. |

**Rules:**
- This is a model-level conversion contract only — not project persistence, database storage, or file-writing.
- Serialization must not lose scientific meaning: units, time reference/scale, and column identities stored as explicit strings.
- No PySide6 dependency; no `astropy.fits` dependency in the core model.

---

## 13. Module Location and Dependency Boundaries

**Recommended module location:** `src/light_curve.py` — consistent with the existing flat `src/` structure, avoids premature package complexity.

**Dependencies:**
- NumPy arrays + standard library types only.
- No PySide6 dependency.
- No `astropy.fits` dependency in the core model.
- `astropy.time.Time` may be constructed later for computation (e.g., BLS in 2.2.4), but is not required for basic model construction or serialization.

**Module responsibility table:**

| Module | Responsibility |
|---|---|
| `src/project_model.py` | Project metadata only (unchanged; not extended with measurement arrays). |
| `src/project_repository.py` | JSON persistence only (unchanged). |
| `src/project_service.py` | Project lifecycle only (unchanged). |
| `src/light_curve.py` (new, recommended) | Light-curve data model: `LightCurveDataset`, `DatasetSource`, `TimeInfo`, `MeasurementSeries`, `MeasurementColumn`, `ValidationReport`, `ValidationFinding`. No UI, no persistence, no FITS reading. |

**Separation of concerns preserved:**
- Project metadata (`ProjectMetadata`) — project-level: name, status, owner, roles, schema version 2.
- Scientific dataset (`LightCurveDataset`) — observation-level: measurements, time, source, validation.
- Source-file reference — in `DatasetSource.original_file_path`, not duplicated in project metadata.
- Validation findings — in `ValidationReport`, separate from measurements.
- Future analysis results — separate structure (deferred).

No ownership or permission metadata is duplicated inside the scientific dataset model. The application remains single-user local under DEC-003.

---

## 14. Compatibility with Subsequent Subtasks

**2.2.2 (FITS Import and Validation):**
- Importer reads FITS files, identifies the LIGHTCURVE HDU, extracts measurements and metadata, constructs `LightCurveDataset` instances, performs import-level validation.
- Model must be complete before importer implementation begins.
- Column mapping (Kepler `SAP_FLUX`, `PDCSAP_FLUX`, `SAP_QUALITY`, `CADENCENO`, `TIME`, etc.) happens in the importer, not the model — these are Kepler-specific conventions kept out of the general model.
- Time convention mapping (BJD-2454833, TDB, SOLARSYSTEM) happens in the importer; `TimeInfo` stores generic components.

**2.2.3 (Project Integration and Provisional Persistence):**
- Associates datasets with projects; decides how dataset references survive save/reopen.
- Needs a serializable model (provided by `to_dict()`/`from_dict()`) and a clear dataset–project association (to be defined).
- D6 deferred: provisional local-file approach only; no permanent storage architecture decision in 2.2.1.

**Potential overlap:** None, provided 2.2.1 stays strictly a data model (no FITS reading, no project association, no persistence).

**Recommended task boundaries remain appropriate:**
| Subtask | Responsibility |
|---|---|
| 2.2.2 | FITS import and validation |
| 2.2.3 | Project integration and provisional persistence |
| 2.2.4 | Testing, documentation, and completion verification |

---

## 15. Verified Kepler-10b FITS Findings (Preserved)

All findings directly verified against the actual file using `astropy.io.fits` (astropy 8.0.2), `mode='readonly'`:

- **3 HDUs:** PRIMARY (mission/target metadata), LIGHTCURVE (476 rows × 20 columns — the relevant light-curve HDU), APERTURE (12×10 pixel aperture mask with WCS).
- **TIME:** days relative to BJD 2454833, range 120.539–130.245, 0 non-finite, `TIMESYS=TDB`, `TIMEREF=SOLARSYSTEM`, `BJDREFI=2454833`.
- **SAP_FLUX vs PDCSAP_FLUX:** Independently identifiable, different non-finite patterns (4 vs 7 rows), different value ranges. Not interchangeable.
- **SAP_FLUX:** 4 non-finite (cadences 703, 848, 950, 972).
- **PDCSAP_FLUX:** 7 non-finite (cadences 703, 790, 848, 914, 915, 950, 972).
- **SAP_QUALITY:** 37 of 476 rows nonzero; values {0, 64, 128, 8192, 8320, 12352, 32800}.
- **PSF_CENTR1/PSF_CENTR2:** Entirely non-finite (all 476 rows) — confirms the model must handle columns that may be fully absent/invalid.
- **CADENCENO:** range 568–1043, spacing exactly 1.

These findings demonstrate why the model must preserve missingness, column identity, original observations, and optional quality/cadence fields.

---

## 16. Decisions Still Requiring User Approval

The following recommendations are presented for approval before proceeding to the 2.2.1 BUILD task:

| Design Question | Recommendation | Approval Required? |
|---|---|---|
| Module location | `src/light_curve.py` | Yes |
| Quality flags / cadence identifiers | Optional NumPy arrays | Yes |
| Measurement uncertainties | Optional NumPy arrays (`None` = absent) | Yes |
| Checksum field | Optional string | Yes |
| Source path | Required for initial local-file workflow | Yes (per DEC-002 original-file preservation) |
| Array construction | Copy incoming arrays during construction; model arrays mutable | Yes |
| Serialization | `to_dict()` / `from_dict()` model-level contract with array→list conversion | Yes |
| Derived counts | Calculated properties (not stored, not cached) | Yes |
| Dataset ID generation | `uuid.uuid4()` for new datasets; explicitly supplied ID preserved during `from_dict()` | Yes |
| Default ValidationReport | Empty default if not supplied; model performs structural validation | Yes |
| Import timestamp | ISO-8601 with timezone when omitted; explicit values preserved during reconstruction | Yes |
| Unknown units representation | Empty string `""`; no silent physical-unit substitution | Yes |

**Approved decisions (relied upon, not changed):** DEC-001/002/003/005/006; D6 deferred.

**Questions that can safely remain deferred:**
- How datasets are associated with projects (2.2.3).
- Exact persistence format/location (D6 deferred; 2.2.3 provisional).
- Whether source files are ever copied into projects.
- Analysis-record model for derived measurements (§5.5).
- Units library choice (plain strings recommended for serialization simplicity).

---

This specification is complete and ready for review. No files were created, modified, or deleted during this planning exercise. Stop and wait for your review.


# revision review


The revised specification incorporates all eight corrections. The architecture is sound, and I would approve most of it. However, there are five remaining issues worth resolving before implementation. These are more substantive than wording changes.

## Remaining issues

### 1. `source_id` is missing from `DatasetSource`

Section 2 defines source identity as a distinct identity, including an archive-product identifier. However, Section 3 does not include a `source_id` field.

Add:

| Field       | Type  | Required | Purpose                                                         |
| ----------- | ----- | -------- | --------------------------------------------------------------- |
| `source_id` | `str` | No       | Identifier assigned by the originating archive or data provider |

It should be optional because locally sourced files might not have an archive identifier.

### 2. Source path requirements need a clearer boundary

Section 3 says `original_file_path` is required for construction in the initial local-file workflow, but also says future source types should be supported without changing the model structure.

These requirements are slightly contradictory.

Recommendation: Make `original_file_path` optional in the general data model. Require the FITS importer in 2.2.2 to supply it for the initial local-file workflow.

This preserves the current requirement without unnecessarily restricting the model.

### 3. Measurement arrays must align with time arrays

The specification checks uncertainty lengths against measurement lengths, but does not explicitly state that every measurement column must have the same number of observations as `time.values`.

Add these structural requirements:

- `len(column.values) == len(time.values)` for every measurement column.
- `len(column.uncertainties) == len(column.values)` when uncertainties are present.
- Optional quality flags and cadence numbers must also match `len(time.values)`.

Any mismatch must prevent construction.

This is essential because each measurement, timestamp, quality flag, and cadence identifier represents the same observation position.

### 4. Derived measurement provenance is not represented

Section 8 says future derived measurements will have provenance metadata linking them to their original measurement series.

However, `MeasurementColumn` currently has no field for that relationship.

Since transformations are explicitly outside 2.2.1, I recommend deferring derived-measurement provenance metadata entirely rather than introducing an incomplete system now.

The specification should say that the initial model preserves imported measurements, while derived measurements and their provenance relationships will be designed alongside the future analysis-record model.

### 5. Validation responsibilities need clarification

The specification currently describes three things:

- Structural validation performed by the model.
- Scientific warnings such as unknown units or missing uncertainties.
- Import-level validation performed by 2.2.2.

It does not clearly establish which component generates each finding.

I recommend this division:

| Responsibility                                                   | Owner              |
| ---------------------------------------------------------------- | ------------------ |
| Array lengths, required fields, data types, column identity      | Core model         |
| Missing uncertainties, unknown units, ambiguous time conventions | Importer           |
| FITS readability, HDU selection, missing source columns          | Importer           |
| Preserving and exposing findings                                 | `ValidationReport` |

Structural errors should raise clear exceptions rather than produce an invalid `LightCurveDataset`. The report can retain importer findings, including errors that prevented a dataset from being accepted.

## Overall assessment

Architecture approved in principle

| Area                                  | Assessment                                |
| ------------------------------------- | ----------------------------------------- |
| Identity separation                   | One missing field                         |
| Time representation                   | Appropriate                               |
| Measurement representation            | Appropriate, with alignment clarification |
| Optional uncertainties                | Approved                                  |
| Quality flags and cadence identifiers | Approved                                  |
| Array ownership                       | Approved                                  |
| Serialization                         | Approved                                  |
| Validation architecture               | Needs clarification                       |
| Module boundaries                     | Approved                                  |
| Project integration separation        | Approved                                  |

The remaining decisions are limited. There is no reason to reopen the broader architectural design.

## Next step

Have Nemotron incorporate these five corrections into the specification, still in PLAN mode, without modifying files or implementing anything.

After that, I would consider the 2.2.1 specification ready for final approval and move directly to the BUILD prompt.


# review prompt

# Subtask 2.2.1 — Final Specification Review and Corrections

**Mode: PLAN ONLY. No implementation or repository modifications.**

Review the revised Subtask 2.2.1 Light-Curve Data Model Specification from your previous response.

Incorporate the following five final corrections into the specification.

## 1. Add the missing source identifier

Section 2 distinguishes source identity from dataset identity and source-file identity, but `DatasetSource` does not currently contain a field for the archive's identifier.

Add the following optional field to `DatasetSource`:

| Field | Type | Required | Purpose |
|---|---|---|---|
| `source_id` | `str` | No | Identifier assigned by the originating archive or data provider, such as an archive product ID. |

Do not confuse this identifier with `dataset_id`, the target identifier, or the original filename.

## 2. Clarify the source-path requirement

The general model should not be permanently restricted to datasets with local source files.

Revise the specification as follows:

- `DatasetSource.original_file_path` is optional in the general data model.
- The initial FITS importer in 2.2.2 must supply the original file path for the current local-file workflow under DEC-002.
- Preserve the original filename and other available provenance information.
- Do not introduce remote retrieval or archive-download functionality in 2.2.1.

This resolves the distinction between a general scientific data model and the requirements of the initial importer.

## 3. Explicitly require measurement/time array alignment

Add the following structural validation requirements:

- Every `MeasurementColumn.values` array must have the same length as `TimeInfo.values`.
- If `MeasurementColumn.uncertainties` is not `None`, its length must match its corresponding measurement values.
- If `quality_flags` is present, its length must match `TimeInfo.values`.
- If `cadence_numbers` is present, its length must match `TimeInfo.values`.

Any mismatch must prevent construction of a valid `LightCurveDataset`.

These arrays represent corresponding observation positions. Do not permit misaligned observations.

## 4. Defer derived-measurement provenance

Section 8 currently promises provenance metadata for future derived measurements, but the proposed `MeasurementColumn` does not define that metadata.

Do not introduce an incomplete provenance mechanism into 2.2.1.

Instead:
- The initial model represents and preserves imported measurements.
- Original imported measurements must not be overwritten.
- Derived measurements and their provenance relationships are deferred to the future analysis-record model and relevant processing subtasks.
- Do not add transformation functionality or analysis-record fields to the current model.

## 5. Clarify validation responsibilities

Establish the following division:

| Responsibility | Owner |
|---|---|
| Required fields, data types, array lengths, column identity | Core data model |
| Missing uncertainties, unknown units, ambiguous time conventions | FITS importer |
| FITS readability, HDU selection, missing source columns | FITS importer |
| Preserving and exposing validation findings | `ValidationReport` |

Additional rules:

- Structural errors must raise clear exceptions and prevent construction of an invalid `LightCurveDataset`.
- Importer-generated warnings and informational findings must be retained in `ValidationReport`.
- Importer errors that prevent dataset acceptance should be reported to the caller, even when no valid dataset can be constructed.
- Do not duplicate importer-specific validation logic inside the general model.

## Scope and execution restrictions

Preserve all previously established requirements and architectural decisions, including:

- DEC-001, DEC-002, DEC-003, DEC-005, DEC-006.
- D6 remains deferred.
- `src/light_curve.py` remains the recommended module location.
- NumPy and Python standard library only in the core model.
- No PySide6, FITS parsing, persistence, or project association in 2.2.1.
- No changes to `ProjectMetadata`, project repository, or project service.
- No changes to architecture decision records or unrelated documentation.

**Do not:**
- Switch to BUILD mode.
- Create, edit, delete, or modify repository files.
- Modify the original OVERVIEW or PROMPTING documents.
- Begin implementation.
- Generate the 2.2.2 importer prompt.
- Expand the scope of Subtask 2.2.1.

## Deliverable

Present the **complete consolidated Subtask 2.2.1 Light-Curve Data Model Specification**, incorporating all previous decisions and these five corrections.

Do not provide only a list of changes. Reproduce the complete specification so it can be reviewed as a standalone document.

At the end, provide:
1. A concise list of any genuinely unresolved design decisions.
2. Confirmation that no repository files were modified.
3. Your recommendation on whether the specification is ready for final approval and the BUILD phase.

Stop and wait for review.


# revision response

(my naming is very inconsistent... oops)

# Subtask 2.2.1 — Light-Curve Data Model Specification

**Mode: PLAN ONLY.** This is a consolidated technical specification. No repository files have been created, modified, or deleted. No implementation has been performed.

---

## 1. Scope Boundaries

**In scope:** Design of the internal light-curve data model (`src/light_curve.py` recommended), its validation, serialization contract, and its relationship to the existing project metadata model.

**Out of scope:** FITS reading/importer (2.2.2), project association/persistence (2.2.3), testing and completion verification (2.2.4), visualization (2.3), BLS analysis (2.4), analysis records (2.5).

**Preserved architectural decisions:**
- DEC-001: Photometry/time-series as initial capability.
- DEC-002: Import of one light-curve format; original-file preservation (referenced by path, never copied/modified).
- DEC-003: Single-user local; no ownership/permission metadata in the scientific dataset model.
- DEC-005: BLS as initial operation (model must preserve time+flux+uncertainty).
- DEC-006: Python 3.13 + NumPy/SciPy/Astropy/Matplotlib stack.
- D6 deferred: permanent storage architecture deferred; model must be storage-independent.
- Foundation §3.4.1, §3.4.3, §4.4–4.8, §5.3, §5.6: photometric data representation, time systems, data formats, import, provenance, quality, original-data preservation, validation.

---

## 2. Identity Model

Four distinct identities must be maintained:

| Identity | Meaning | Example |
|---|---|---|
| **Dataset identity** | UUID uniquely identifying this imported dataset instance | `dataset_id` (UUID string) |
| **Target identity** | The astronomical object being observed | `target_object`: `"KIC 11904151"` |
| **Source identity** | Originating archive or archive-product identifier | `source_id`: `"MAST/STScI"` product ID |
| **Source-file identity** | Original filename, path, and optional checksum | `original_filename`, `original_file_path`, optional `checksum` |

**Rule:** An astronomical target identifier must **not** be used as though it uniquely identifies an imported dataset or source file. A target may have multiple datasets, observations, quarters, or archive products.

Do not confuse `source_id` (archive-assigned product identifier) with `dataset_id` (dataset UUID), `target_object` (astronomical object), or `original_filename`.

---

## 3. DatasetSource Structure

**Responsibility:** Identifies where the dataset came from; retains source-file provenance; does **not** persist source-file availability as authoritative metadata.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `original_filename` | `str` | No | Original file name |
| `original_file_path` | `str` | No | Absolute path to source file at import time (optional in general model) |
| `archive` | `str` | No | Originating archive/resource (e.g., `"MAST/STScI"`) |
| `source_id` | `str` | No | Identifier assigned by the originating archive or data provider (e.g., archive product ID) |
| `mission` | `str` | No | Mission (e.g., `"Kepler"`) |
| `instrument` | `str` | No | Instrument (e.g., `"Kepler Photometer"`) |
| `target_object` | `str` | No | Target object identifier (e.g., `"KIC 11904151"`) |
| `checksum` | `str` | No | File checksum for source identification (optional provenance) |

**Source-file path requirement (clarified):**
- `DatasetSource.original_file_path` is **optional in the general data model**. The model is not permanently restricted to datasets with local source files.
- The initial FITS importer in Subtask 2.2.2 **must supply** the original file path for the current local-file workflow under DEC-002.
- Preserve the original filename and other available provenance information.
- Do not introduce remote retrieval or archive-download functionality in 2.2.1.

**Source-file availability:** Must **not** be stored as a `file_available` boolean field. Availability is determined dynamically when required, by checking the stored path at access time. A dynamic property or separate availability-check function may be considered, but no unnecessary infrastructure.

**Validation rule:** `original_file_path` is not required at the general model level. It is required at the importer level for the initial local-file workflow (Subtask 2.2.2).

---

## 4. TimeInfo Structure

**Responsibility:** Preserves timestamps **and** their interpretation separately; never reduces timestamps to raw floats without context.

| Field | Type | Required | Validation Rule |
|---|---|---|---|
| `values` | `numpy.ndarray` (float64) | Yes | Required. Numerical timestamp values. |
| `unit` | `str` | Yes | Required as a field. Empty string `""` represents unknown units; unknown units must be distinguishable and generate a validation warning. No physical unit is silently substituted. |
| `reference` | `str` | No | Time reference/epoch (e.g., `"BJD - 2454833"`). Optional; missing generates warning where scientifically relevant. Empty string `""` if unknown. |
| `reference_value` | `float` | No | Numeric reference epoch (e.g., `2454833.0`). Optional. |
| `time_scale` | `str` | No | Time scale/system (e.g., `"TDB"`). Optional; missing generates warning where scientifically relevant. Empty string `""` if unknown. |
| `time_reference_frame` | `str` | No | Barycentric frame (e.g., `"SOLARSYSTEM"`). Optional. Empty string `""` if unknown. |
| `start` | `float` | No | TSTART / observation start. Optional. |
| `stop` | `float` | No | TSTOP / observation stop. Optional. |
| `resolution` | `float` | No | TIMEDEL / time resolution. Optional. |
| `format_hint` | `str` | No | e.g., `"BJD"`. Optional. |

**Validation rules:**
- Time values are required for construction.
- Time unit must be explicitly represented; unknown units are represented as `""` and are distinguishable. No physical unit is silently substituted.
- Reference epoch and time scale are optional; missing/unknown values produce validation warnings, not construction errors.
- No default time conventions are invented.
- Numerical time values and their interpretation (unit, reference, scale, frame) are preserved separately.

**Kepler-10b verified values:** `values` range 120.539–130.245, `unit="d"`, `reference="BJD - 2454833"`, `reference_value=2454833.0`, `time_scale="TDB"`, `time_reference_frame="SOLARSYSTEM"`, `start=120.52892942`, `stop=130.25561236`, `resolution=0.02043359821692`.

---

## 5. MeasurementSeries Structure

**Responsibility:** Holds named measurement columns, each a `MeasurementColumn` pairing values with uncertainties. Keyed by original column identity.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `series` | `dict[str, MeasurementColumn]` | Yes | Named measurement series. **Each dictionary key must match its contained `MeasurementColumn.name`.** |

**Validation rule:** For every entry `key -> column` in `series`, `key == column.name`. Keys must be unique column names. Each entry independently identifies its measurement column.

---

## 6. MeasurementColumn Structure

**Responsibility:** A single measurement column paired with its associated uncertainty, plus column metadata.

| Field | Type | Required | Validation Rule |
|---|---|---|---|
| `name` | `str` | Yes | Column identity (original FITS column name, e.g., `"SAP_FLUX"`). Must match the `MeasurementSeries` dictionary key. |
| `values` | `numpy.ndarray` (float64) | Yes | Measurement values. Non-finite values preserved, not removed. |
| `uncertainties` | `numpy.ndarray` (float64) \| `None` | No (optional, `None`) | 1-sigma uncertainties aligned with `values`. `None` = unknown/absent. If provided, `len(uncertainties) == len(values)`. Unknown uncertainty (`None`) is distinguishable from a measured zero uncertainty (array of `0.0` values). Missing uncertainties generate a validation warning but do not invalidate an otherwise usable series. |
| `unit` | `str` | Yes | Measurement unit (e.g., `"e-/s"`). Empty string `""` represents unknown units; unknown units are distinguishable. |
| `description` | `str` | No | Column description (from FITS TTYPE/TCOMM). |

**Array alignment validation rules (structural):**
- Every `MeasurementColumn.values` array must have the same length as `TimeInfo.values`.
- If `MeasurementColumn.uncertainties` is not `None`, its length must match its corresponding measurement values.
- Unknown units (`""`) are distinguishable from known units; no physical unit silently substituted.
- Non-finite values in `values` are preserved; count tracked via calculated property.

**Kepler-10b verified values:**
- `SAP_FLUX`: unit `"e-/s"`, 4 non-finite (cadences 703, 848, 950, 972), range ≈ 532355–532944 e-/s.
- `PDCSAP_FLUX`: unit `"e-/s"`, 7 non-finite (cadences 703, 790, 848, 914, 915, 950, 972), range ≈ 501346–501747 e-/s.
- SAP and PDCSAP remain independently identifiable and accessible (separate `MeasurementColumn` entries).

---

## 7. Optional Quality Flags and Cadence Identifiers

**Responsibility:** Per-observation quality flags and observation identifiers, both optional.

| Field | Type | Required | Validation Rule |
|---|---|---|---|
| `quality_flags` | `numpy.ndarray` (int) | No (optional) | If present, `len(quality_flags) == len(TimeInfo.values)`. Original values preserved; unknown quality systems not interpreted automatically. |
| `cadence_numbers` | `numpy.ndarray` (int) | No (optional) | If present, `len(cadence_numbers) == len(TimeInfo.values)`. Original values preserved; not required to be uniformly spaced. |

**Array alignment validation rules (structural):**
- If `quality_flags` is present, its length must match `TimeInfo.values`.
- If `cadence_numbers` is present, its length must match `TimeInfo.values`.

**Rules:**
- Neither is a universal mandatory requirement.
- When present, lengths must match observation count (i.e., `TimeInfo.values` length).
- Original values preserved without interpretation of unfamiliar quality systems.
- No Kepler-specific requirements imposed on other missions.
- Nonzero quality flags remain available (37 of 476 rows nonzero in Kepler-10b; values {0, 64, 128, 8192, 8320, 12352, 32800}). Do not assume all nonzero flags should cause observations to be discarded.

**Any mismatch between array lengths must prevent construction of a valid `LightCurveDataset`.**

---

## 8. LightCurveDataset Structure

**Responsibility:** Top-level container for a single imported light-curve dataset. One instance per imported dataset. Independent of `ProjectMetadata` and of any project association.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `dataset_id` | `str` (UUID) | Yes | Stable identifier for this imported dataset. |
| `name` | `str` | Yes | User-visible dataset name. |
| `source` | `DatasetSource` | Yes | Source-file identity and provenance metadata. |
| `time` | `TimeInfo` | Yes | Time representation (values, unit, reference, scale, frame). |
| `measurements` | `MeasurementSeries` | Yes | The measurement columns. |
| `quality_flags` | `numpy.ndarray` (int) | No | Per-observation quality flags (optional). |
| `cadence_numbers` | `numpy.ndarray` (int) | No | Observation identifiers (optional). |
| `validation` | `ValidationReport` | Yes | Import/construction validation findings. Default empty report if not supplied; structural validation performed by the model. |
| `imported_at` | `str` (ISO-8601) | Yes | Import timestamp. Generated with timezone info if omitted; explicitly supplied timestamps preserved during `from_dict()` reconstruction. |
| `notes` | `str` | No | User annotations. |

**Relationships:** A `Project` may contain zero or more `LightCurveDataset` instances (association mechanism deferred to 2.2.3). For 2.2.1, the model is independent of projects entirely.

**Dataset ID generation:** Recommend generating `dataset_id` using `uuid.uuid4()` when creating a new dataset, while allowing an explicitly supplied ID during reconstruction through `from_dict()`.

**Validation ownership:** `LightCurveDataset` is constructible without requiring callers to manually supply a complete `ValidationReport`. A default empty `ValidationReport` is used when none is supplied. Structural validation (length alignment, required fields, types, key/name matching, array alignment) is performed by the model during construction and by `from_dict()` during reconstruction.

**Derived-measurement provenance (deferred):** The initial model represents and preserves imported measurements. Original imported measurements must not be overwritten. Derived measurements and their provenance relationships are deferred to the future analysis-record model and relevant processing subtasks. Do not add transformation functionality or analysis-record fields to the current model.

**Original-versus-derived distinction:** Original source measurements are stored as imported and never overwritten. Future derived/transformed measurements (normalized, detrended, filtered) are stored as separate `MeasurementColumn` entries with provenance metadata linking back to the source series — that provenance mechanism is deferred, not implemented in 2.2.1. Processing operations (normalization, detrending, quality filtering, interpolation) are out of scope for 2.2.1.

---

## 9. Array Ownership, Copying, and Mutability

**Rule:** The model copies incoming NumPy arrays during construction.

- External modification of the original input arrays (e.g., FITS-derived arrays held by the importer) must **not** silently alter the dataset.
- Model-owned arrays remain mutable. No complicated immutability framework is introduced; the mutability policy is documented so callers understand whether they may modify arrays held by the model.
- Calculated properties such as `n_nonfinite` must calculate their values from the current arrays rather than cache them. They are not stored.
- Future transformations must produce separate derived `MeasurementColumn` entries rather than overwriting originals.

**Rationale:** NumPy arrays are mutable; without an explicit copy rule, external code could silently corrupt imported data. This is particularly important for future normalization and detrending operations (Foundation §5.3: original data preservation and transformation safeguards).

---

## 10. Derived Counts and Calculated Properties

**Rule:** Prefer calculated properties over stored redundant counts.

| Derived Count | Derivation | Stored? |
|---|---|---|
| `n_observations` | Length of `time.values` array | No — calculated property |
| `n_nonfinite` | Count of non-finite values in a `MeasurementColumn.values` array | No — calculated property per column, computed from current array |

**Justification:** Storing derived counts creates the possibility of inconsistent metadata if underlying arrays change. Both are calculated properties that read from the current arrays; they are never cached or stored independently.

---

## 11. ValidationReport and ValidationFinding

**ValidationReport** — Structured record of validation findings so the importer can report them consistently.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `errors` | `list[ValidationFinding]` | Yes | Conditions preventing dataset acceptance. |
| `warnings` | `list[ValidationFinding]` | Yes | Conditions permitting representation but flagged. |
| `info` | `list[ValidationFinding]` | Yes | Conditions preserved without modification. |

**ValidationFinding**

| Field | Type | Purpose |
|---|---|---|
| `code` | `str` | Stable machine-readable finding code. |
| `message` | `str` | Human-readable description. |
| `severity` | `str` (`"error"`/`"warning"`/`"info"`) | Severity level. |
| `column` | `str` | Affected column (optional). |
| `row_indices` | `list[int]` | Affected row indices, **zero-based** internally. |

---

## 12. Validation Responsibilities (Division)

| Responsibility | Owner |
|---|---|
| Required fields, data types, array lengths, column identity, key/name matching | Core data model (`LightCurveDataset`, `MeasurementColumn`, `TimeInfo`, `DatasetSource`) |
| Missing uncertainties, unknown units, ambiguous time conventions | FITS importer (Subtask 2.2.2) |
| FITS readability, HDU selection, missing source columns | FITS importer (Subtask 2.2.2) |
| Preserving and exposing validation findings | `ValidationReport` |

**Additional rules:**
- Structural errors must raise clear exceptions and prevent construction of an invalid `LightCurveDataset`.
- Importer-generated warnings and informational findings must be retained in `ValidationReport`.
- Importer errors that prevent dataset acceptance should be reported to the caller, even when no valid dataset can be constructed.
- Do not duplicate importer-specific validation logic inside the general model.
- Model-level validation checks internal consistency (length alignment, required fields, types, key/name matching, array alignment between measurement/time arrays).
- Import-level validation (2.2.2) checks source-data suitability (file readable, HDU present, required columns present). These remain separate.

---

## 13. Model-Level Serialization

**Interface:** `to_dict()` and `from_dict()` on `LightCurveDataset`.

| Method | Specification |
|---|---|
| `to_dict()` | Returns ordinary Python values compatible with `json.dumps()`. NumPy arrays are converted to lists. Preserves measurement values, uncertainties, units, time conventions, source information, quality flags, cadence identifiers, validation findings, original-versus-derived distinctions. `None` uncertainties serialize as JSON `null`. Zero-value arrays serialize as arrays of zeros (distinguishable from `null`/`None`). |
| `from_dict()` | Reconstructs NumPy arrays from the serialized lists and validates the resulting model. `null` in JSON reconstructs to Python `None` for optional uncertainty fields. Arrays of zeros reconstruct to NumPy arrays containing zeros (distinguishable from `None`). Structural validation is performed on the reconstructed model. |

**Rules:**
- This is a model-level conversion contract only — not project persistence, database storage, or file-writing.
- Serialization must not lose scientific meaning: units, time reference/scale, and column identities stored as explicit strings.
- No PySide6 dependency; no `astropy.fits` dependency in the core model.
- `None` and arrays containing zero values remain distinguishable.

---

## 14. Module Location and Dependency Boundaries

**Recommended module location:** `src/light_curve.py` — consistent with the existing flat `src/` structure, avoids premature package complexity.

**Dependencies:**
- NumPy arrays + standard library types only.
- No PySide6 dependency.
- No `astropy.fits` dependency in the core model.
- `astropy.time.Time` may be constructed later for computation (e.g., BLS in 2.2.4), but is not required for basic model construction or serialization.

**Module responsibility table:**

| Module | Responsibility |
|---|---|
| `src/project_model.py` | Project metadata only (unchanged; not extended with measurement arrays). |
| `src/project_repository.py` | JSON persistence only (unchanged). |
| `src/project_service.py` | Project lifecycle only (unchanged). |
| `src/light_curve.py` (new, recommended) | Light-curve data model: `LightCurveDataset`, `DatasetSource`, `TimeInfo`, `MeasurementSeries`, `MeasurementColumn`, `ValidationReport`, `ValidationFinding`. No UI, no persistence, no FITS reading. |

**Separation of concerns preserved:**
- Project metadata (`ProjectMetadata`) — project-level: name, status, owner, roles, schema version 2.
- Scientific dataset (`LightCurveDataset`) — observation-level: measurements, time, source, validation.
- Source-file reference — in `DatasetSource.original_file_path`, not duplicated in project metadata.
- Validation findings — in `ValidationReport`, separate from measurements.
- Future analysis results — separate structure (deferred).

No ownership or permission metadata is duplicated inside the scientific dataset model. The application remains single-user local under DEC-003.

**No changes to `ProjectMetadata`, project repository, or project service.**

---

## 15. Compatibility with Subsequent Subtasks

**2.2.2 (FITS Import and Validation):**
- Importer reads FITS files, identifies the LIGHTCURVE HDU, extracts measurements and metadata, constructs `LightCurveDataset` instances, performs import-level validation.
- Model must be complete before importer implementation begins.
- Column mapping (Kepler `SAP_FLUX`, `PDCSAP_FLUX`, `SAP_QUALITY`, `CADENCENO`, `TIME`, etc.) happens in the importer, not the model — these are Kepler-specific conventions kept out of the general model.
- Time convention mapping (BJD-2454833, TDB, SOLARSYSTEM) happens in the importer; `TimeInfo` stores generic components.
- The importer must supply `original_file_path` for the initial local-file workflow under DEC-002.

**2.2.3 (Project Integration and Provisional Persistence):**
- Associates datasets with projects; decides how dataset references survive save/reopen.
- Needs a serializable model (provided by `to_dict()`/`from_dict()`) and a clear dataset–project association (to be defined).
- D6 deferred: provisional local-file approach only; no permanent storage architecture decision in 2.2.1.

**Potential overlap:** None, provided 2.2.1 stays strictly a data model (no FITS reading, no project association, no persistence).

**Recommended task boundaries remain appropriate:**
| Subtask | Responsibility |
|---|---|
| 2.2.2 | FITS import and validation |
| 2.2.3 | Project integration and provisional persistence |
| 2.2.4 | Testing, documentation, and completion verification |

---

## 16. Verified Kepler-10b FITS Findings (Preserved)

All findings directly verified against the actual file using `astropy.io.fits` (astropy 8.0.2), `mode='readonly'`:

- **3 HDUs:** PRIMARY (mission/target metadata), LIGHTCURVE (476 rows × 20 columns — the relevant light-curve HDU), APERTURE (12×10 pixel aperture mask with WCS).
- **TIME:** days relative to BJD 2454833, range 120.539–130.245, 0 non-finite, `TIMESYS=TDB`, `TIMEREF=SOLARSYSTEM`, `BJDREFI=2454833`.
- **SAP_FLUX vs PDCSAP_FLUX:** Independently identifiable, different non-finite patterns (4 vs 7 rows), different value ranges. Not interchangeable.
- **SAP_FLUX:** 4 non-finite (cadences 703, 848, 950, 972).
- **PDCSAP_FLUX:** 7 non-finite (cadences 703, 790, 848, 914, 915, 950, 972).
- **SAP_QUALITY:** 37 of 476 rows nonzero; values {0, 64, 128, 8192, 8320, 12352, 32800}.
- **PSF_CENTR1/PSF_CENTR2:** Entirely non-finite (all 476 rows) — confirms the model must handle columns that may be fully absent/invalid.
- **CADENCENO:** range 568–1043, spacing exactly 1.

These findings demonstrate why the model must preserve missingness, column identity, original observations, and optional quality/cadence fields.

---

## 17. Decisions Still Requiring User Approval

| Design Question | Recommendation | Approval Required? |
|---|---|---|
| Module location | `src/light_curve.py` | Yes |
| Quality flags / cadence identifiers | Optional NumPy arrays | Yes |
| Measurement uncertainties | Optional NumPy arrays (`None` = absent) | Yes |
| `source_id` field | Optional string in `DatasetSource` | Yes |
| `original_file_path` | Optional in general model; required by initial importer | Yes |
| Dataset ID generation | `uuid.uuid4()` for new; explicit ID preserved during `from_dict()` | Yes |
| Array construction | Copy incoming arrays during construction; model arrays mutable | Yes |
| Serialization | `to_dict()` / `from_dict()` model-level contract with array→list conversion | Yes |
| Derived counts | Calculated properties (not stored, not cached) | Yes |
| Default ValidationReport | Empty default if not supplied; model performs structural validation | Yes |
| Import timestamp | ISO-8601 with timezone when omitted; explicit values preserved during reconstruction | Yes |
| Unknown units representation | Empty string `""`; no silent physical-unit substitution | Yes |
| Validation responsibility division | Core model: structural; Importer: source-data suitability | Yes |

**Approved decisions (relied upon, not changed):** DEC-001/002/003/005/006; D6 deferred.

**Questions that can safely remain deferred:**
- How datasets are associated with projects (2.2.3).
- Exact persistence format/location (D6 deferred; 2.2.3 provisional).
- Whether source files are ever copied into projects.
- Analysis-record model for derived measurements (§5.5).
- Units library choice (plain strings recommended for serialization simplicity).

---

## Verification and Completion Status

**Confirmation:** No repository files were created, modified, or deleted during this planning exercise. No BUILD mode was entered. No implementation code or tests were written. The original OVERVIEW and PROMPTING documents were not modified.

**Recommendation:** The specification is now complete and internally consistent. All five corrections from this review have been incorporated:

1. `source_id` added to `DatasetSource` as an optional field.
2. `original_file_path` clarified as optional in the general model, required by the initial importer.
3. Measurement/time array alignment explicitly required as structural validation.
4. Derived-measurement provenance explicitly deferred; no incomplete provenance mechanism added.
5. Validation responsibilities explicitly divided between core model and FITS importer.

The specification is ready for final review and, upon approval, for preparation of the 2.2.1 BUILD prompt.

Stop and wait for review.



# final review

The specification is now approved in principle for Subtask 2.2.1 BUILD. All five architectural corrections have been incorporated, and the model boundaries are appropriate.

I found two final details worth making explicit in the BUILD prompt. Neither requires another PLAN cycle.

### 1. Dataset ID generation

Section 8 lists `dataset_id` as required, while also specifying automatic generation.

The implementation should interpret this as:

- Generate a UUID when the caller does not provide one.
- Accept an explicit UUID when supplied.
- Preserve the existing UUID during `from_dict()` reconstruction.
- Reject malformed UUIDs.

### 2. Validation report boundaries

Structural errors prevent construction of a valid dataset, so they cannot be stored in that dataset's `ValidationReport`.

The implementation should distinguish:

- Model structural errors: raise clear exceptions.
- Importer findings: warnings and informational findings can be retained in `ValidationReport`.
- Importer failures: reported to the caller separately when no valid dataset can be constructed.

This avoids an inconsistency in the validation design.

## Approval summary

Ready for BUILD

| Area                                    | Decision                    |
| --------------------------------------- | --------------------------- |
| Data model architecture                 | Approved                    |
| Module location                         | `src/light_curve.py`        |
| NumPy array handling                    | Approved                    |
| Optional uncertainties and quality data | Approved                    |
| Source identity and provenance          | Approved                    |
| Time representation                     | Approved                    |
| Serialization contract                  | Approved                    |
| Validation separation                   | Approved with clarification |
| Project integration                     | Deferred to 2.2.3           |
| Persistence architecture                | D6 remains deferred         |

Next step: Prepare the Subtask 2.2.1 BUILD prompt using this specification as the authoritative design.

No further design-planning cycle is necessary.


# build prompt


# BUILD — Subtask 2.2.1: FITS Inspection and Light-Curve Data Model

## Mode and authorization

**BUILD mode — implementation authorized.**

The design for Subtask 2.2.1 has been reviewed and approved. Implement the approved light-curve data model. Do not restart the design-planning process or broaden the scope.

The approved specification from the preceding planning/review process is authoritative. If an implementation detail is not explicitly specified, inspect existing repository conventions and choose the smallest compatible solution. Report any material conflict rather than silently changing the approved design.

## 1. Repository and baseline checks

Repository: `C:\Code\New_Project`

Before editing:

1. Inspect the current repository state and relevant existing files.
2. Confirm the active Python environment and project test configuration.
3. Run the existing test suite to establish the current baseline.
4. Record the baseline test result.
5. Inspect existing conventions for dataclasses, validation, serialization, type annotations, exceptions, and tests.

Do not assume the repository is unchanged from the previous planning session.

Do not overwrite unrelated user changes. If the working tree contains existing modifications, identify them and avoid disturbing them.

## 2. Implementation scope

Create the new module:

`src/light_curve.py`

Implement the approved scientific light-curve data model using **Python standard-library functionality and NumPy only**.

The module should contain the following model components:

- `DatasetSource`
- `TimeInfo`
- `MeasurementColumn`
- `MeasurementSeries`
- `ValidationFinding`
- `ValidationReport`
- `LightCurveDataset`

Use clear type annotations and documentation/docstrings consistent with the existing project.

### Explicit exclusions

Do not implement:

- FITS file reading or parsing.
- Astropy FITS integration.
- FITS HDU selection.
- FITS import workflows.
- Project association or project-level dataset management.
- Database or file persistence.
- Project repository/service changes.
- GUI changes or PySide6 integration.
- Plotting or visualization.
- BLS or other scientific analysis.
- Derived-measurement processing or provenance systems.
- Changes to project metadata schema or permission logic.

These belong to later subtasks.

## 3. Dataset identity and source information

### DatasetSource

Represent the origin of a dataset independently from its scientific measurements.

Include these optional fields:

- `original_filename: str | None`
- `original_file_path: str | None`
- `archive: str | None`
- `source_id: str | None`
- `mission: str | None`
- `instrument: str | None`
- `target_object: str | None`
- `checksum: str | None`

Do not add a stored `file_available` property. File availability can be checked dynamically when needed.

The general model permits an optional original file path. The later FITS importer in Subtask 2.2.2 is responsible for supplying the path for the current local-file workflow.

Keep these identities distinct:

- `dataset_id`: identifies this imported dataset.
- `target_object`: identifies the astronomical target.
- `source_id`: identifies the originating archive/provider product.
- Original filename/path/checksum: identify the source file.

Do not treat a target identifier as a dataset or file identifier.

## 4. TimeInfo

Represent the time axis independently.

Required fields:

- `values`: NumPy array of float64 values.
- `unit: str`

Optional metadata:

- `reference`
- `reference_value`
- `time_scale`
- `time_reference_frame`
- `start`
- `stop`
- `resolution`
- `format_hint`

An empty string (`""`) represents an unknown time unit. Do not invent defaults for unknown time units, reference conventions, or time scales.

Missing or unknown scientific metadata should be representable and should not automatically prevent construction.

The model must preserve the supplied time values without silently changing their meaning.

## 5. MeasurementColumn and MeasurementSeries

### MeasurementColumn

Represent each measurement column independently.

Required fields:

- `name: str`
- `values`: NumPy array of float64 values.
- `unit: str`

Optional fields:

- `uncertainties`: NumPy array of float64 values or `None`.
- `description: str | None`

Requirements:

- Preserve non-finite values (`NaN`, positive infinity, negative infinity).
- Do not silently remove, replace, or interpolate invalid values.
- An empty unit string (`""`) means unknown.
- `uncertainties=None` means uncertainties are absent or unknown.
- Do not interpret `None` as an array of zero uncertainties.
- If an uncertainty array is supplied, its length must match the measurement values.
- Measurement values must align with the time array.
- Do not merge distinct measurement columns.

In particular, SAP_FLUX and PDCSAP_FLUX must remain separate, independently identifiable measurement columns.

### MeasurementSeries

Represent measurement columns using:

`series: dict[str, MeasurementColumn]`

Requirements:

- Dictionary keys must match the corresponding `MeasurementColumn.name`.
- Column names must be unique.
- Reject invalid key/name mismatches.
- Preserve column identity.

## 6. Optional quality flags and cadence numbers

Support optional arrays:

- `quality_flags: np.ndarray[int] | None`
- `cadence_numbers: np.ndarray[int] | None`

When supplied, their lengths must match the time array.

Preserve the supplied values. Do not automatically interpret quality flags, remove observations with nonzero flags, or impose Kepler-specific assumptions.

These fields must remain optional so that the model can represent light curves from other sources.

## 7. LightCurveDataset

Create the central dataset model.

It should contain:

- `dataset_id`
- `name`
- `source`
- `time`
- `measurements`
- optional `quality_flags`
- optional `cadence_numbers`
- `validation`
- `imported_at`
- optional `notes`

Requirements:

### Dataset ID

- Use a UUID string.
- Generate a UUID using `uuid.uuid4()` when a new dataset is created without an explicit ID.
- Accept an explicit valid UUID when reconstructing a dataset.
- Preserve an explicitly supplied UUID.
- Preserve the UUID during `from_dict()` reconstruction.
- Reject malformed UUID values with a clear exception.

### Imported timestamp

- Generate an ISO-8601 timestamp with timezone information when one is not supplied.
- Preserve an explicitly supplied timestamp during reconstruction.
- Do not replace an existing timestamp when loading serialized data.

### Validation report

- Default to an empty `ValidationReport` when one is not supplied.
- Preserve a supplied report.
- Do not treat scientific warnings as construction failures.

### Dataset independence

A `LightCurveDataset` represents one imported dataset. It must not depend on or contain a `ProjectMetadata` object.

Do not add project IDs, ownership fields, roles, permissions, or access-control metadata to the scientific model.

Project association will be handled separately in Subtask 2.2.3.

## 8. Array ownership and mutation

Copy incoming NumPy arrays during construction so that subsequent changes to the caller's original input arrays cannot alter the model's arrays.

The model-owned arrays may remain mutable.

Do not introduce an unnecessary immutable-array framework.

Do not implement measurement transformations or processing operations in this subtask. The model should not provide functionality that overwrites imported measurements with processed values. Future analysis and derived-measurement provenance will be addressed separately.

## 9. Calculated properties

Implement these as calculated properties, not stored fields:

- `n_observations`: number of entries in the time array.
- `n_nonfinite` for each `MeasurementColumn`: number of non-finite measurement values.

Do not cache these counts. They must reflect the current model-owned arrays.

Do not count or store these values as independent serialized data.

## 10. Validation design

Implement the approved separation between structural validation and scientific/import validation.

### Core model structural validation

The model must reject structurally invalid data, including:

- Missing required fields.
- Invalid field types.
- Invalid UUID values.
- Invalid measurement-series keys or names.
- Measurement arrays with lengths that do not match the time array.
- Uncertainty arrays with lengths that do not match their measurement arrays.
- Quality-flag or cadence arrays with lengths that do not match the time array.

Raise clear, appropriate exceptions. Follow existing project conventions where practical.

Structural failures prevent construction of a valid dataset. They should not be represented as findings inside a dataset that was never successfully constructed.

### ValidationFinding

Include:

- `code`
- `message`
- `severity`
- optional `column`
- optional `row_indices`

Use the supported severity values:

- `error`
- `warning`
- `info`

`row_indices`, when supplied, should represent zero-based row positions.

### ValidationReport

Include separate collections for:

- `errors`
- `warnings`
- `info`

Preserve findings during serialization and reconstruction.

### Scientific and importer-level findings

Missing uncertainties, unknown units, and ambiguous time conventions should be representable as warnings rather than structural errors.

The later FITS importer is responsible for detecting FITS-specific issues and populating the dataset's validation report when a valid dataset can still be constructed.

If an importer failure prevents dataset construction, that failure must be reported separately to the caller by the importer. Do not attempt to store such a failure in a dataset validation report for a dataset that does not exist.

Do not duplicate FITS-specific validation logic in `src/light_curve.py`.

## 11. Serialization

Implement:

- `to_dict()`
- `from_dict()`

Requirements:

- `to_dict()` must return ordinary Python values compatible with `json.dumps()`.
- Convert NumPy arrays to ordinary lists.
- Preserve all relevant model fields and metadata.
- Serialize absent uncertainties and optional arrays as `None` (JSON `null`).
- Preserve actual zero-valued arrays as arrays of zeros.
- Preserve non-finite array values without silently replacing or dropping them during model conversion.
- Serialize and reconstruct validation findings and reports.
- Preserve `dataset_id` and `imported_at`.
- `from_dict()` must reconstruct NumPy arrays with the required dtypes.
- `from_dict()` must distinguish `None` from an actual array.
- `from_dict()` must validate the reconstructed model using the same structural rules as normal construction.

Serialization is a data-conversion facility only. Do not add JSON file-writing, database access, or persistence functionality.

## 12. Dependency boundaries

`src/light_curve.py` may use:

- Python standard library.
- NumPy.

Do not import:

- PySide6.
- `astropy.io.fits`.
- Other GUI or FITS-specific modules.

Do not modify the existing project model, repository, or service to integrate this dataset. That work belongs to Subtask 2.2.3.

## 13. Focused tests

Although broader testing and completion verification belong to Subtask 2.2.4, add focused unit tests needed to verify the new model itself.

Follow the repository's existing test organization and naming conventions. A focused file such as `tests/test_light_curve.py` is appropriate if consistent with the project.

Test at minimum:

1. Valid construction of each model component.
2. Automatic UUID generation.
3. Acceptance and preservation of an explicit UUID.
4. Rejection of malformed UUIDs.
5. Automatic timezone-aware `imported_at` generation.
6. Preservation of explicitly supplied timestamps.
7. Optional source metadata.
8. Unknown units represented by empty strings.
9. Measurement values aligned with time values.
10. Optional uncertainties, including the distinction between `None` and a zero array.
11. Preservation of non-finite measurement values.
12. Separate identity of SAP_FLUX and PDCSAP_FLUX.
13. Optional quality flags and cadence numbers.
14. Length validation for all aligned arrays.
15. Measurement-series key/name validation.
16. Array-copy behavior.
17. Calculated observation and non-finite counts.
18. Default and explicitly supplied validation reports.
19. Serialization and reconstruction of all supported fields.
20. Preservation of `None` versus actual arrays during round-trip conversion.
21. Rejection of invalid reconstructed data.

Tests must verify the intended behavior rather than merely mirror implementation details.

Do not weaken, remove, skip, or rewrite unrelated existing tests to make the new implementation pass.

## 14. Documentation and change control

Keep changes limited to the new model and its focused tests unless a small, necessary adjustment is required by an established repository convention.

Do not edit the Subtask 2.2.1 OVERVIEW or PROMPTING planning documents.

Do not update broader development status or mark Subtask 2.2.1 complete. Completion verification and documentation updates belong to Subtask 2.2.4.

Do not commit or push changes.

## 15. Verification

After implementation:

1. Run the focused light-curve model tests.
2. Run the complete existing test suite.
3. Compare the full-suite result against the baseline recorded before implementation.
4. Inspect the final diff for unintended changes.
5. Confirm that no FITS importer, project persistence, GUI, or analysis functionality was introduced.

If tests fail, investigate and fix implementation defects within this scope. Do not weaken tests or expand scope to work around failures.

## 16. Final report

Provide a concise implementation report containing:

- Files created or modified.
- Model components implemented.
- Validation and serialization behavior implemented.
- Focused test command and result.
- Full test command and result.
- Baseline versus final test counts.
- Any unresolved issues or deviations from the approved specification.
- Confirmation that no commit or push was performed.

Clearly distinguish verified results from assumptions.

**Stop after completing Subtask 2.2.1. Do not begin Subtask 2.2.2 or 2.2.3.**



# build report #


The implementation is complete. Only the two authorized files were created by me (`src/light_curve.py` and `tests/test_light_curve.py`). The deleted PLAN.md and untracked WORKING PROGRESS LOG.md are pre-existing from the planning session and were not touched by me. No commits or pushes were made.

---

# Subtask 2.2.1 — Implementation Report

## Files Created

| File | Purpose |
|---|---|
| `src/light_curve.py` | New light-curve data model module |
| `tests/test_light_curve.py` | Focused unit tests for the model |

No existing files were modified. No commits or pushes were made.

## Model Components Implemented

| Component | Description |
|---|---|
| `DatasetSource` | Source-file identity and provenance (all fields optional; no stored `file_available`) |
| `TimeInfo` | Time representation with required `values` + `unit`; optional reference/scale/frame metadata; empty string for unknown units |
| `MeasurementColumn` | Single measurement column with `name`, `values`, `unit`, optional `uncertainties` (`None` distinguishable from zero array), optional `description`; `n_nonfinite` calculated property |
| `MeasurementSeries` | `dict[str, MeasurementColumn]` with key/name matching validation |
| `ValidationFinding` | `code`, `message`, `severity`, optional `column`, optional zero-based `row_indices` |
| `ValidationReport` | Separate `errors`, `warnings`, `info` collections |
| `LightCurveDataset` | Central dataset model with `dataset_id`, `name`, `source`, `time`, `measurements`, optional `quality_flags`/`cadence_numbers`, `validation`, `imported_at`, optional `notes`; `n_observations` calculated property |

## Validation & Serialization Behavior

**Structural validation (raises `LightCurveValidationError`):**
- Invalid/malformed UUID for `dataset_id`
- Missing or non-array `time.values`
- Non-string `time.unit`
- Measurement-series key/name mismatch, duplicate column names
- Measurement values not aligned with time array length
- Uncertainty/quality/cadence array length mismatches
- Invalid `ValidationReport` or non-string `imported_at`

**Array ownership:** Incoming NumPy arrays are copied during `LightCurveDataset` construction. Model-owned arrays remain mutable; no immutable framework.

**Calculated properties (not cached):** `n_observations` (from `time.values` length), `n_nonfinite` per `MeasurementColumn`.

**Serialization (`to_dict()` / `from_dict()`):**
- NumPy arrays → Python lists (JSON-compatible via `json.dumps`)
- `None` uncertainties/optional arrays preserved as JSON `null`
- Zero-valued arrays preserved as arrays of zeros (distinguishable from `null`)
- Validation findings preserved through round-trip
- `dataset_id` and `imported_at` preserved
- Reconstructed models validated with same structural rules

## Test Results

| Command | Result |
|---|---|
| `pytest tests/test_light_curve.py -v` | 48 passed, 0 failed |
| `pytest` (full suite) | 224 passed, 0 failed (baseline: 176) |

## Scope Compliance

- No FITS reading, no `astropy.io.fits`, no PySide6, no persistence, no project association, no GUI, no BLS analysis, no derived-measurement provenance.
- No changes to `ProjectMetadata`, `project_repository.py`, or `project_service.py`.
- No changes to OVERVIEW or PROMPTING planning documents.

The implementation matches the approved specification. Subtask 2.2.1 is complete. Stopping here — not beginning Subtask 2.2.2 or 2.2.3.


# 2.2.1 work review


Subtask 2.2.1 is complete based on the reported implementation and test results.

The results are consistent with the approved design:

| Verification            | Result     |
| ----------------------- | ---------- |
| Focused model tests     | 48 passed  |
| Full test suite         | 224 passed |
| Previous baseline       | 176 passed |
| Net increase            | 48 tests   |
| Existing files modified | 0          |
| Commits / pushes        | None       |

The reported scope is also correct: the scientific data model is independent of project metadata, FITS parsing, and persistence.

### Two items to retain for the completion review

1. Structural validation: The report identifies several validation cases, but does not explicitly mention every type constraint from the specification (for example, float64 measurement arrays and integer quality/cadence arrays). These should be checked against the actual implementation.
2. Array ownership: The report says arrays are copied during `LightCurveDataset` construction. Check whether arrays are also copied when individual components such as `TimeInfo` and `MeasurementColumn` are constructed independently.

These are verification points, not reasons to reopen implementation automatically.

### Current status

Implementation reported complete

- Subtask 2.2.1: FITS inspection and light-curve data-model design — implemented.
- Subtask 2.2.2: FITS importer — not started.
- Subtask 2.2.3: Project association and persistence — not started.
- Subtask 2.2.4: Testing, documentation, and completion verification — remains separate.

I would preserve the reported implementation as-is and carry those two checks into the 2.2.4 review rather than expanding the current scope.