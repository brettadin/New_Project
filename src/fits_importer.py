"""FITS light-curve importer for the astronomy research application.

Reads astronomical FITS light-curve files, identifies the appropriate
light-curve table structurally (not by a fixed HDU index), extracts
supported measurements and their uncertainties, preserves scientific
metadata, validates the imported contents, and constructs the existing
LightCurveDataset model from Subtask 2.2.1.

The importer is intentionally free of PySide6, persistence, and
project-association logic so it can be unit-tested independently.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import numpy as np
from astropy.io import fits

from src.light_curve import (
    DatasetSource,
    LightCurveDataset,
    LightCurveValidationError,
    MeasurementColumn,
    MeasurementSeries,
    TimeInfo,
    ValidationFinding,
    ValidationReport,
)


class FITSImportError(Exception):
    """Raised when a file-level condition prevents FITS light-curve import."""


# Mapping of each supported flux column to its corresponding uncertainty column.
_FLUX_COLUMNS = ("SAP_FLUX", "PDCSAP_FLUX")
_UNCERTAINTY_FOR_FLUX = {
    "SAP_FLUX": "SAP_FLUX_ERR",
    "PDCSAP_FLUX": "PDCSAP_FLUX_ERR",
}

# Numeric dtype kinds accepted for time, flux, and uncertainty columns.
_NUMERIC_KINDS = frozenset({"f", "i", "u"})

# Numeric dtype kinds accepted for integer-valued quality/cadence columns.
_INTEGER_KINDS = frozenset({"i", "u"})


def import_light_curve(file_path: str | os.PathLike[str]) -> LightCurveDataset:
    """Read a FITS light-curve file and return a LightCurveDataset.

    Reads the file read-only, identifies the light-curve table structurally,
    extracts supported measurements and metadata, validates the contents,
    and constructs a LightCurveDataset.

    Parameters
    ----------
    file_path : str or os.PathLike
        Path to the FITS file to import.

    Returns
    -------
    LightCurveDataset
        The constructed and validated dataset.

    Raises
    ------
    FITSImportError
        If the file cannot be opened, contains no usable light-curve table,
        is missing required columns, has incompatible data types, contains
        integer null sentinels in data, or fails model construction.
    """
    path = Path(file_path)

    try:
        hdul = fits.open(path, mode="readonly")
    except FileNotFoundError as exc:
        raise FITSImportError(f"FITS file not found: '{path}'") from exc
    except PermissionError as exc:
        raise FITSImportError(
            f"Permission denied reading FITS file: '{path}'"
        ) from exc
    except Exception as exc:  # astropy.FITSError, OSError, etc.
        raise FITSImportError(
            f"Cannot open FITS file '{path}': {exc}"
        ) from exc

    try:
        return _import_from_hdul(hdul, path)
    finally:
        hdul.close()


def _import_from_hdul(hdul: fits.HDUList, path: Path) -> LightCurveDataset:
    """Import a light-curve dataset from an already-open HDU list."""

    # Step 1: Identify candidate light-curve HDUs structurally.
    candidates = _find_light_curve_candidates(hdul)
    if not candidates:
        raise FITSImportError(
            f"No usable light-curve table found in '{path}': no binary-table "
            "HDU contains a TIME column and at least one supported flux "
            "column (SAP_FLUX or PDCSAP_FLUX)."
        )

    # Step 2: Select the HDU using the multiple-candidate policy.
    selected_hdu, ambiguity_finding = _select_hdu(candidates, path)

    # Step 2.5: Reject duplicate supported column names before any
    # name-based data or metadata lookup.
    _check_duplicate_columns(selected_hdu, path)

    # Step 3: Get references to headers and table data.
    table_data = selected_hdu.data
    ext_header = selected_hdu.header
    primary_header = hdul[0].header

    # Step 4: Extract time values and time metadata.
    time_values, time_info, time_findings = _extract_time(
        selected_hdu, table_data, ext_header, path
    )

    # Reject empty tables (zero observations).
    if len(time_values) == 0:
        raise FITSImportError(
            f"The light-curve table in '{path}' contains zero observations; "
            "an empty table cannot provide a usable light-curve dataset."
        )

    n_time = len(time_values)

    # Step 8: Extract measurement columns (flux + uncertainties).
    measurements, measurement_findings = _extract_measurements(
        selected_hdu, table_data, time_values, n_time, path
    )

    # Step 9: Extract optional quality flags and cadence numbers.
    quality_flags, cadence_numbers, optional_findings = _extract_optional_arrays(
        selected_hdu, table_data, n_time, path
    )

    # Step 10: Build the validation report from all findings.
    validation = _build_validation_report(
        time_findings, measurement_findings, optional_findings, ambiguity_finding
    )

    # Step 11: Build source metadata.
    source = _build_source_metadata(primary_header, ext_header, path)

    # Step 12: Construct the dataset (model performs structural validation).
    try:
        dataset = LightCurveDataset(
            name=path.stem,
            source=source,
            time=time_info,
            measurements=MeasurementSeries(series=measurements),
            quality_flags=quality_flags,
            cadence_numbers=cadence_numbers,
            validation=validation,
        )
    except LightCurveValidationError as exc:
        raise FITSImportError(
            f"Failed to construct light-curve dataset from '{path}': {exc}"
        ) from exc

    return dataset


def _find_light_curve_candidates(hdul: fits.HDUList) -> list[tuple[int, Any]]:
    """Find all table HDUs containing TIME and at least one supported flux column.

    Returns a list of (hdu_index, hdu) tuples in HDU order.
    """
    candidates: list[tuple[int, Any]] = []
    for idx, hdu in enumerate(hdul):
        if not isinstance(hdu, (fits.BinTableHDU, fits.TableHDU)):
            continue
        col_names = hdu.columns.names
        if col_names is None:
            continue
        col_set = set(col_names)
        if "TIME" in col_set and (
            "SAP_FLUX" in col_set or "PDCSAP_FLUX" in col_set
        ):
            candidates.append((idx, hdu))
    return candidates


def _select_hdu(
    candidates: list[tuple[int, Any]], path: Path
) -> tuple[Any, ValidationFinding | None]:
    """Select one HDU from candidates using the multiple-candidate policy.

    Policy:
      1. Exactly one valid candidate -> select it (no ambiguity finding).
      2. Multiple valid candidates with one or more EXTNAME=LIGHTCURVE
         -> prefer a LIGHTCURVE candidate.
      3. Same preference -> select the first in HDU order.
      4. Multiple valid candidates -> record an informational finding.

    Returns (selected_hdu, ambiguity_finding_or_None).
    """
    if len(candidates) == 1:
        return candidates[0][1], None

    # Multiple candidates: prefer EXTNAME=LIGHTCURVE if structurally valid
    # (all candidates are already structurally valid by construction).
    lightcurve_candidates = [
        (idx, hdu)
        for idx, hdu in candidates
        if _get_extname(hdu) == "LIGHTCURVE"
    ]

    if lightcurve_candidates:
        selected_idx, selected_hdu = lightcurve_candidates[0]
    else:
        selected_idx, selected_hdu = candidates[0]  # First in HDU order

    ambiguity_finding = ValidationFinding(
        code="MULTIPLE_LIGHT_CURVE_CANDIDATES",
        message=(
            f"Multiple usable light-curve tables found ({len(candidates)}) "
            f"in '{path}'. Selected HDU index {selected_idx} "
            f"({_get_extname(selected_hdu) or 'unnamed'})."
        ),
        severity="info",
        column=None,
    )
    return selected_hdu, ambiguity_finding


def _get_extname(hdu: Any) -> str | None:
    """Get the EXTNAME value from an HDU header, or None if absent."""
    value = hdu.header.get("EXTNAME")
    if value is None:
        return None
    return str(value)


def _check_duplicate_columns(hdu: Any, path: Path) -> None:
    """Reject duplicate supported column names before name-based lookup.

    Inspects ``selected_hdu.columns.names`` which preserves the original
    FITS ``TTYPE`` definitions including duplicates. Accessing
    ``table_data.dtype.names`` or ``table_data[name]`` with duplicate
    column names raises ``ValueError`` from Astropy, so the duplicate
    check must happen first using ``columns.names``.
    """
    supported = {
        "TIME",
        "SAP_FLUX",
        "PDCSAP_FLUX",
        "SAP_FLUX_ERR",
        "PDCSAP_FLUX_ERR",
        "SAP_QUALITY",
        "CADENCENO",
    }
    col_names = list(hdu.columns.names)
    seen: set[str] = set()
    for name in col_names:
        if name in supported:
            if name in seen:
                raise FITSImportError(
                    f"Duplicate supported column name '{name}' in '{path}'. "
                    "Duplicate column definitions prevent unambiguous "
                    "data extraction."
                )
            seen.add(name)


def _get_header_string(header: fits.Header, keyword: str, default: str = "") -> str:
    """Get a string value from a FITS header, or default if absent/undefined."""
    value = header.get(keyword)
    if value is None:
        return default
    return str(value)


def _get_column_unit_str(hdu: Any, col_name: str) -> str:
    """Get the TUNITn string for a column, or '' if absent/blank/whitespace-only.

    Preserves the original nonblank unit string exactly as supplied.
    Whitespace-only metadata is treated as blank.
    """
    for col in hdu.columns:
        if col.name == col_name:
            unit = col.unit
            if unit is None:
                return ""
            unit_str = str(unit)
            if not unit_str.strip():
                return ""
            return unit_str
    return ""


def _extract_time(
    selected_hdu: Any,
    table_data: Any,
    ext_header: fits.Header,
    path: Path,
) -> tuple[np.ndarray, TimeInfo, dict[str, list[ValidationFinding]]]:
    """Extract TIME values and time metadata from the selected table HDU.

    Returns (time_values, time_info, findings).
    findings has keys "warnings" and "info".
    """
    findings: dict[str, list[ValidationFinding]] = {"warnings": [], "info": []}

    if "TIME" not in selected_hdu.columns.names:
        raise FITSImportError(
            f"Required column 'TIME' is absent from the light-curve table in "
            f"'{path}'."
        )

    time_raw = table_data["TIME"]
    kind = time_raw.dtype.kind
    if kind not in _NUMERIC_KINDS:
        raise FITSImportError(
            f"Column 'TIME' in '{path}' has incompatible type "
            f"'{time_raw.dtype}'; expected a numeric type."
        )

    time_values = np.array(time_raw, dtype=np.float64, copy=True)

    # Report non-finite timestamps as a warning; preserve values.
    nonfinite_rows = np.where(~np.isfinite(time_values))[0]
    if len(nonfinite_rows) > 0:
        findings["warnings"].append(
            ValidationFinding(
                code="NONFINITE_TIME",
                message=(
                    f"TIME column contains {len(nonfinite_rows)} non-finite "
                    f"value(s) at zero-based row index(es) "
                    f"{list(map(int, nonfinite_rows))}."
                ),
                severity="warning",
                column="TIME",
                row_indices=list(map(int, nonfinite_rows)),
            )
        )

    # Report duplicate timestamps as a warning; preserve order.
    if len(time_values) > 1:
        unique_values, counts = np.unique(time_values, return_counts=True)
        dup_values = unique_values[counts > 1]
        if len(dup_values) > 0:
            duplicate_rows = np.where(np.isin(time_values, dup_values))[0]
            findings["warnings"].append(
                ValidationFinding(
                    code="DUPLICATE_TIME",
                    message=(
                        f"TIME column contains duplicate timestamp(s) at "
                        f"zero-based row index(es) "
                        f"{list(map(int, duplicate_rows))}."
                    ),
                    severity="warning",
                    column="TIME",
                    row_indices=list(map(int, duplicate_rows)),
                )
            )

    # Report non-monotonic timestamps as a warning; preserve order.
    if len(time_values) > 1:
        diffs = np.diff(time_values)
        non_monotonic_rows = np.where(diffs < 0)[0] + 1
        if len(non_monotonic_rows) > 0:
            findings["warnings"].append(
                ValidationFinding(
                    code="NONMONOTONIC_TIME",
                    message=(
                        f"TIME column is non-monotonic at zero-based row "
                        f"index(es) {list(map(int, non_monotonic_rows))}."
                    ),
                    severity="warning",
                    column="TIME",
                    row_indices=list(map(int, non_monotonic_rows)),
                )
            )

    # --- Time metadata from the selected extension header ---
    time_unit = _get_header_string(ext_header, "TIMEUNIT", "")

    # Descriptive time convention from the TIME column's TUNIT1.
    time_reference = _get_column_unit_str(selected_hdu, "TIME")

    time_scale = _get_header_string(ext_header, "TIMESYS", "")
    time_frame = _get_header_string(ext_header, "TIMEREF", "")

    # Numeric reference offset from BJDREFI and BJDREFF.
    # A missing component is treated as zero (per the approved plan).
    reference_value: float | None = None
    bjdref_i = ext_header.get("BJDREFI")
    bjdref_f = ext_header.get("BJDREFF")
    if bjdref_i is not None or bjdref_f is not None:
        try:
            ref_i = float(bjdref_i) if bjdref_i is not None else 0.0
            ref_f = float(bjdref_f) if bjdref_f is not None else 0.0
            reference_value = ref_i + ref_f
        except (TypeError, ValueError):
            reference_value = None

    start: float | None = None
    if ext_header.get("TSTART") is not None:
        try:
            start = float(ext_header["TSTART"])
        except (TypeError, ValueError):
            start = None

    stop: float | None = None
    if ext_header.get("TSTOP") is not None:
        try:
            stop = float(ext_header["TSTOP"])
        except (TypeError, ValueError):
            stop = None

    # TIMEDEL is intentionally not mapped to resolution in this subtask.
    resolution: float | None = None

    if not time_unit:
        findings["info"].append(
            ValidationFinding(
                code="MISSING_TIME_UNIT",
                message=(
                    "Time unit is not specified in the FITS header (TIMEUNIT)."
                ),
                severity="info",
                column="TIME",
            )
        )

    time_info = TimeInfo(
        values=time_values,
        unit=time_unit,
        reference=time_reference,
        reference_value=reference_value,
        time_scale=time_scale,
        time_reference_frame=time_frame,
        start=start,
        stop=stop,
        resolution=resolution,
    )

    return time_values, time_info, findings


def _to_float64(data: np.ndarray, col_name: str, path: Path) -> np.ndarray:
    """Convert column data to float64, rejecting incompatible types."""
    kind = data.dtype.kind
    if kind not in _NUMERIC_KINDS:
        raise FITSImportError(
            f"Column '{col_name}' in '{path}' has incompatible type "
            f"'{data.dtype}'; expected a numeric type."
        )
    return np.array(data, dtype=np.float64, copy=True)


def _to_int64(data: np.ndarray, col_name: str, path: Path) -> np.ndarray:
    """Convert column data to int64, rejecting float types (would truncate).

    Before conversion, verifies all values fit within the int64 range to
    prevent overflow or wraparound when converting unsigned 64-bit values.
    """
    kind = data.dtype.kind
    if kind not in _INTEGER_KINDS:
        raise FITSImportError(
            f"Column '{col_name}' in '{path}' has incompatible type "
            f"'{data.dtype}'; expected an integer type."
        )
    int64_info = np.iinfo(np.int64)
    if np.any(data < int64_info.min) or np.any(data > int64_info.max):
        raise FITSImportError(
            f"Column '{col_name}' in '{path}' contains integer values "
            f"outside the int64 range "
            f"[{int64_info.min}, {int64_info.max}]. Conversion would "
            "overflow or wrap around."
        )
    return np.array(data, dtype=np.int64, copy=True)


def _check_tnull_sentinel_present(hdu: Any, col_name: str) -> bool:
    """Check whether a declared TNULL sentinel occurs in an integer column's data.

    Returns True if the sentinel is declared and at least one data value equals
    it (import should fail). Returns False if the sentinel is declared but
    unused, or not declared at all.
    """
    for col in hdu.columns:
        if col.name == col_name:
            null_value = col.null
            if null_value is None:
                return False
            data = hdu.data[col_name]
            return bool(np.any(data == null_value))
    return False


def _check_unit_compatibility(
    flux_col: str,
    flux_unit: str,
    err_col: str,
    uncertainty_unit: str | None,
    path: Path,
) -> None:
    """Apply the flux/uncertainty unit compatibility policy.

    Raises FITSImportError if the units are incompatible per Section 7.2:
      - Both present and identical: OK.
      - Both blank/absent: OK (unit = "").
      - Only one present: FITSImportError.
      - Both present but different: FITSImportError.
    """
    flux_present = bool(flux_unit and flux_unit.strip())
    err_present = bool(uncertainty_unit and uncertainty_unit.strip())

    if not flux_present and not err_present:
        return  # Both blank/absent -> OK

    if flux_present and not err_present:
        raise FITSImportError(
            f"Flux column '{flux_col}' has unit '{flux_unit}' but its "
            f"uncertainty column '{err_col}' has no unit in '{path}'. "
            "Flux and uncertainty units must match."
        )

    if not flux_present and err_present:
        raise FITSImportError(
            f"Uncertainty column '{err_col}' has unit '{uncertainty_unit}' "
            f"but its flux column '{flux_col}' has no unit in '{path}'. "
            "Flux and uncertainty units must match."
        )

    # Both present: must be identical (after trimming whitespace).
    if flux_unit.strip() != uncertainty_unit.strip():
        raise FITSImportError(
            f"Flux column '{flux_col}' has unit '{flux_unit}' but its "
            f"uncertainty column '{err_col}' has unit '{uncertainty_unit}' "
            f"in '{path}'. Flux and uncertainty units must match."
        )


def _extract_measurements(
    selected_hdu: Any,
    table_data: Any,
    time_values: np.ndarray,
    n_time: int,
    path: Path,
) -> tuple[dict[str, MeasurementColumn], dict[str, list[ValidationFinding]]]:
    """Extract measurement columns and their uncertainties.

    Returns (measurements_dict, findings).
    findings has keys "warnings" and "info".
    """
    findings: dict[str, list[ValidationFinding]] = {"warnings": [], "info": []}
    measurements: dict[str, MeasurementColumn] = {}

    # Check for orphan uncertainty columns first.
    for flux_col, err_col in _UNCERTAINTY_FOR_FLUX.items():
        if err_col in table_data.dtype.names and flux_col not in table_data.dtype.names:
            findings["warnings"].append(
                ValidationFinding(
                    code="ORPHAN_UNCERTAINTY",
                    message=(
                        f"Uncertainty column '{err_col}' is present but its "
                        f"corresponding flux column '{flux_col}' is absent. "
                        "The orphan uncertainty column is ignored."
                    ),
                    severity="warning",
                    column=err_col,
                )
            )

    for flux_col in _FLUX_COLUMNS:
        err_col = _UNCERTAINTY_FOR_FLUX[flux_col]

        if flux_col not in table_data.dtype.names:
            continue  # This flux column not present in the table.

        # Extract flux values.
        flux_raw = table_data[flux_col]
        flux_values = _to_float64(flux_raw, flux_col, path)

        if len(flux_values) != n_time:
            raise FITSImportError(
                f"Column '{flux_col}' length ({len(flux_values)}) does not "
                f"match TIME length ({n_time}) in '{path}'."
            )

        # Report non-finite flux values as a warning; preserve values.
        nonfinite_rows = np.where(~np.isfinite(flux_values))[0]
        if len(nonfinite_rows) > 0:
            findings["warnings"].append(
                ValidationFinding(
                    code="NONFINITE_VALUES",
                    message=(
                        f"Column '{flux_col}' contains {len(nonfinite_rows)} "
                        f"non-finite value(s) at zero-based row index(es) "
                        f"{list(map(int, nonfinite_rows))}."
                    ),
                    severity="warning",
                    column=flux_col,
                    row_indices=list(map(int, nonfinite_rows)),
                )
            )

        # Get flux unit from column metadata.
        flux_unit = _get_column_unit_str(selected_hdu, flux_col)

        # Extract uncertainties if present.
        uncertainties: np.ndarray | None = None
        uncertainty_unit: str | None = None

        if err_col in table_data.dtype.names:
            err_raw = table_data[err_col]
            uncertainties = _to_float64(err_raw, err_col, path)

            if len(uncertainties) != n_time:
                raise FITSImportError(
                    f"Column '{err_col}' length ({len(uncertainties)}) does "
                    f"not match TIME length ({n_time}) in '{path}'."
                )

            # Report non-finite uncertainties as a warning; preserve values.
            err_nonfinite = np.where(~np.isfinite(uncertainties))[0]
            if len(err_nonfinite) > 0:
                findings["warnings"].append(
                    ValidationFinding(
                        code="NONFINITE_UNCERTAINTY",
                        message=(
                            f"Column '{err_col}' contains {len(err_nonfinite)} "
                            f"non-finite value(s) at zero-based row index(es) "
                            f"{list(map(int, err_nonfinite))}."
                        ),
                        severity="warning",
                        column=err_col,
                        row_indices=list(map(int, err_nonfinite)),
                    )
                )

            # Report negative uncertainties as a warning; preserve values.
            negative_rows = np.where(uncertainties < 0)[0]
            if len(negative_rows) > 0:
                findings["warnings"].append(
                    ValidationFinding(
                        code="NEGATIVE_UNCERTAINTY",
                        message=(
                            f"Column '{err_col}' contains {len(negative_rows)} "
                            f"negative value(s) at zero-based row index(es) "
                            f"{list(map(int, negative_rows))}."
                        ),
                        severity="warning",
                        column=err_col,
                        row_indices=list(map(int, negative_rows)),
                    )
                )

            uncertainty_unit = _get_column_unit_str(selected_hdu, err_col)

            # Apply unit compatibility policy only when both columns exist.
            _check_unit_compatibility(
                flux_col, flux_unit, err_col, uncertainty_unit, path
            )
        else:
            # Uncertainty column absent entirely: warning, uncertainties=None.
            findings["warnings"].append(
                ValidationFinding(
                    code="UNCERTAINTY_MISSING",
                    message=(
                        f"No uncertainty column '{err_col}' found for flux "
                        f"column '{flux_col}'. Uncertainties are absent."
                    ),
                    severity="warning",
                    column=flux_col,
                )
            )

        # MeasurementColumn.unit receives the flux unit string. The uncertainty
        # array shares this unit by the existing model design; no separate
        # uncertainty-unit field exists.
        measurements[flux_col] = MeasurementColumn(
            name=flux_col,
            values=flux_values,
            unit=flux_unit,
            uncertainties=uncertainties,
            description=None,
        )

    # At least one supported flux column must be present.
    if not measurements:
        raise FITSImportError(
            f"No supported flux column found in '{path}': expected "
            "SAP_FLUX and/or PDCSAP_FLUX."
        )

    return measurements, findings


def _extract_optional_arrays(
    selected_hdu: Any,
    table_data: Any,
    n_time: int,
    path: Path,
) -> tuple[np.ndarray | None, np.ndarray | None, dict[str, list[ValidationFinding]]]:
    """Extract optional quality flags and cadence numbers.

    Returns (quality_flags, cadence_numbers, findings).
    findings has keys "warnings" and "info".
    """
    findings: dict[str, list[ValidationFinding]] = {"warnings": [], "info": []}

    quality_flags: np.ndarray | None = None
    if "SAP_QUALITY" in table_data.dtype.names:
        # TNULL policy: reject if sentinel occurs in data.
        if _check_tnull_sentinel_present(selected_hdu, "SAP_QUALITY"):
            raise FITSImportError(
                f"Column 'SAP_QUALITY' in '{path}' declares a FITS null "
                "sentinel (TNULL) that occurs in the data. The current model "
                "cannot represent per-row missing integer values."
            )
        quality_raw = table_data["SAP_QUALITY"]
        quality_flags = _to_int64(quality_raw, "SAP_QUALITY", path)
        if len(quality_flags) != n_time:
            raise FITSImportError(
                f"Column 'SAP_QUALITY' length ({len(quality_flags)}) does "
                f"not match TIME length ({n_time}) in '{path}'."
            )

        # Report nonzero quality flags as an info finding; do not filter.
        nonzero_rows = np.where(quality_flags != 0)[0]
        if len(nonzero_rows) > 0:
            findings["info"].append(
                ValidationFinding(
                    code="NONZERO_QUALITY_FLAGS",
                    message=(
                        f"SAP_QUALITY contains {len(nonzero_rows)} nonzero "
                        f"value(s) at zero-based row index(es) "
                        f"{list(map(int, nonzero_rows))}."
                    ),
                    severity="info",
                    column="SAP_QUALITY",
                    row_indices=list(map(int, nonzero_rows)),
                )
            )

    cadence_numbers: np.ndarray | None = None
    if "CADENCENO" in table_data.dtype.names:
        # TNULL policy: reject if sentinel occurs in data.
        if _check_tnull_sentinel_present(selected_hdu, "CADENCENO"):
            raise FITSImportError(
                f"Column 'CADENCENO' in '{path}' declares a FITS null "
                "sentinel (TNULL) that occurs in the data. The current model "
                "cannot represent per-row missing integer values."
            )
        cadence_raw = table_data["CADENCENO"]
        cadence_numbers = _to_int64(cadence_raw, "CADENCENO", path)
        if len(cadence_numbers) != n_time:
            raise FITSImportError(
                f"Column 'CADENCENO' length ({len(cadence_numbers)}) does "
                f"not match TIME length ({n_time}) in '{path}'."
            )

    return quality_flags, cadence_numbers, findings


def _build_validation_report(
    time_findings: dict[str, list[ValidationFinding]],
    measurement_findings: dict[str, list[ValidationFinding]],
    optional_findings: dict[str, list[ValidationFinding]],
    ambiguity_finding: ValidationFinding | None,
) -> ValidationReport:
    """Assemble a ValidationReport from all extraction findings."""
    errors: list[ValidationFinding] = []
    warnings: list[ValidationFinding] = []
    info: list[ValidationFinding] = []

    warnings.extend(time_findings["warnings"])
    info.extend(time_findings["info"])
    warnings.extend(measurement_findings["warnings"])
    info.extend(measurement_findings["info"])
    warnings.extend(optional_findings["warnings"])
    info.extend(optional_findings["info"])
    if ambiguity_finding is not None:
        info.append(ambiguity_finding)

    return ValidationReport(errors=errors, warnings=warnings, info=info)


def _build_source_metadata(
    primary_header: fits.Header,
    ext_header: fits.Header,
    path: Path,
) -> DatasetSource:
    """Build DatasetSource from primary header (preferred) with extension fallback.

    Source metadata (mission, instrument, target, source_id) is taken from the
    primary header first; if absent, the selected extension header is consulted
    as a documented application-level fallback. This fallback is independent of
    FITS header inheritance (the INHERIT keyword).

    ORIGIN is not automatically treated as the archive.
    """
    return DatasetSource(
        original_filename=path.name,
        original_file_path=str(path),
        archive=None,
        source_id=_get_source_value(primary_header, ext_header, "KEPLERID"),
        mission=_get_source_value(primary_header, ext_header, "MISSION"),
        instrument=_get_source_value(primary_header, ext_header, "INSTRUME"),
        target_object=_get_source_value(primary_header, ext_header, "OBJECT"),
        checksum=None,
    )


def _get_source_value(
    primary_header: fits.Header,
    ext_header: fits.Header,
    keyword: str,
) -> str | None:
    """Get a source-metadata value: primary header preferred, extension fallback."""
    value = _get_header_string(primary_header, keyword, "")
    if value:
        return value
    return _get_header_string(ext_header, keyword, "") or None
