"""Focused unit tests for the FITS light-curve importer (Subtask 2.2.2).

Uses temporary FITS fixtures created under pytest tmp_path. Does not depend
on the user's external Kepler dataset or any machine-specific absolute path.

Covers FITS reading, HDU identification, measurement extraction, metadata
mapping, unit handling, validation findings, failure handling, resource
safety, and data preservation.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
from astropy.io import fits

from src.fits_importer import FITSImportError, import_light_curve
from src.light_curve import (
    DatasetSource,
    LightCurveDataset,
    ValidationFinding,
    ValidationReport,
)


# ------------------------------------------------------------------
# Helpers for creating temporary FITS files
# ------------------------------------------------------------------

def _write_fits_file(
    tmp_path: Path,
    filename: str,
    time_values: np.ndarray,
    columns: list[fits.Column],
    primary_header: dict | None = None,
    ext_header: dict | None = None,
    extname: str = "LIGHTCURVE",
    extra_hdus: list[fits.PrimaryHDU | fits.BinTableHDU] | None = None,
) -> Path:
    """Write a minimal multi-HDU FITS file with a light-curve table.

    Parameters
    ----------
    tmp_path : Path
        pytest temporary directory.
    filename : str
        Output filename.
    time_values : np.ndarray
        TIME column values (float64).
    columns : list[fits.Column]
        Additional FITS column definitions (flux, uncertainty, quality, etc.).
    primary_header : dict, optional
        Keyword values for the primary HDU header.
    ext_header : dict, optional
        Keyword values for the extension header.
    extname : str
        EXTNAME for the table HDU.
    extra_hdus : list, optional
        Additional HDUs to append (for multi-candidate tests).
    """
    time_col = fits.Column(
        name="TIME", format="D", array=np.array(time_values, dtype=np.float64)
    )
    all_columns = [time_col] + columns

    table_hdu = fits.BinTableHDU.from_columns(all_columns)
    table_hdu.header["EXTNAME"] = extname
    if ext_header:
        for key, value in ext_header.items():
            table_hdu.header[key] = value

    primary = fits.PrimaryHDU()
    if primary_header:
        for key, value in primary_header.items():
            primary.header[key] = value

    hdul = fits.HDUList([primary, table_hdu])
    if extra_hdus:
        for extra in extra_hdus:
            hdul.append(extra)

    filepath = tmp_path / filename
    hdul.writeto(filepath)
    return filepath


def _flux_col(name: str, values, unit: str | None = None) -> fits.Column:
    """Create a float32 flux-like FITS column."""
    return fits.Column(
        name=name,
        format="E",
        array=np.array(values, dtype=np.float32),
        unit=unit,
    )


def _int_col(name: str, values, unit: str | None = None, null=None) -> fits.Column:
    """Create an int32 FITS column, optionally with a TNULL sentinel."""
    return fits.Column(
        name=name,
        format="J",
        array=np.array(values, dtype=np.int32),
        unit=unit,
        null=null,
    )


# ------------------------------------------------------------------
# Valid import: SAP only
# ------------------------------------------------------------------


def test_import_sap_only(tmp_path):
    n = 5
    time_vals = np.arange(n, dtype=np.float64) + 100.0
    sap_vals = np.array([100.0, 200.0, 300.0, 400.0, 500.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "sap_only.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals, unit="e-/s")],
        primary_header={
            "MISSION": "Kepler",
            "INSTRUME": "Kepler Photometer",
            "OBJECT": "KIC 11904151",
            "KEPLERID": 11904151,
        },
        ext_header={
            "TIMEUNIT": "d",
            "TIMESYS": "TDB",
            "TIMEREF": "SOLARSYSTEM",
            "BJDREFI": 2454833,
            "BJDREFF": 0.0,
            "TSTART": 100.0,
            "TSTOP": 104.0,
        },
    )

    dataset = import_light_curve(path)

    assert isinstance(dataset, LightCurveDataset)
    assert dataset.name == "sap_only"
    assert dataset.n_observations == n
    assert dataset.source.original_filename == "sap_only.fits"
    assert dataset.source.original_file_path == str(path)
    assert dataset.source.mission == "Kepler"
    assert dataset.source.instrument == "Kepler Photometer"
    assert dataset.source.target_object == "KIC 11904151"
    assert dataset.source.source_id == "11904151"
    assert dataset.source.archive is None

    assert dataset.time.unit == "d"
    assert dataset.time.reference == ""
    assert dataset.time.time_scale == "TDB"
    assert dataset.time.time_reference_frame == "SOLARSYSTEM"
    assert dataset.time.reference_value == 2454833.0
    assert dataset.time.start == 100.0
    assert dataset.time.stop == 104.0

    assert "SAP_FLUX" in dataset.measurements.series
    assert "PDCSAP_FLUX" not in dataset.measurements.series
    sap = dataset.measurements.series["SAP_FLUX"]
    assert sap.unit == "e-/s"
    assert np.array_equal(sap.values, sap_vals.astype(np.float64))
    assert sap.uncertainties is None

    assert dataset.quality_flags is None
    assert dataset.cadence_numbers is None

    # Warning: flux column present but no uncertainty column
    warning_codes = [f.code for f in dataset.validation.warnings]
    assert "UNCERTAINTY_MISSING" in warning_codes
    assert dataset.validation.info == []
    assert dataset.validation.errors == []


# ------------------------------------------------------------------
# Valid import: PDCSAP only
# ------------------------------------------------------------------


def test_import_pdcsap_only(tmp_path):
    n = 4
    time_vals = np.arange(n, dtype=np.float64) + 50.0
    pdc_vals = np.array([10.0, 20.0, 30.0, 40.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "pdc_only.fits",
        time_vals,
        [_flux_col("PDCSAP_FLUX", pdc_vals, unit="e-/s")],
        primary_header={"MISSION": "Kepler"},
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)

    assert dataset.n_observations == n
    assert "PDCSAP_FLUX" in dataset.measurements.series
    assert "SAP_FLUX" not in dataset.measurements.series
    pdc = dataset.measurements.series["PDCSAP_FLUX"]
    assert np.array_equal(pdc.values, pdc_vals.astype(np.float64))
    assert pdc.unit == "e-/s"


# ------------------------------------------------------------------
# Valid import: both SAP and PDCSAP (independent columns)
# ------------------------------------------------------------------


def test_import_sap_and_pdcsap_independent(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64) + 1.0
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)
    pdc_vals = np.array([101.0, 201.0, 301.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "both.fits",
        time_vals,
        [
            _flux_col("SAP_FLUX", sap_vals, unit="e-/s"),
            _flux_col("PDCSAP_FLUX", pdc_vals, unit="e-/s"),
        ],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)

    assert dataset.n_observations == n
    assert "SAP_FLUX" in dataset.measurements.series
    assert "PDCSAP_FLUX" in dataset.measurements.series
    assert dataset.measurements.series["SAP_FLUX"] is not dataset.measurements.series["PDCSAP_FLUX"]
    assert np.array_equal(
        dataset.measurements.series["SAP_FLUX"].values, sap_vals.astype(np.float64)
    )
    assert np.array_equal(
        dataset.measurements.series["PDCSAP_FLUX"].values, pdc_vals.astype(np.float64)
    )


# ------------------------------------------------------------------
# Uncertainty columns paired correctly
# ------------------------------------------------------------------


def test_uncertainties_attached_to_correct_flux_column(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)
    sap_err = np.array([1.0, 2.0, 3.0], dtype=np.float32)
    pdc_vals = np.array([101.0, 201.0, 301.0], dtype=np.float32)
    pdc_err = np.array([1.1, 2.1, 3.1], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "with_errors.fits",
        time_vals,
        [
            _flux_col("SAP_FLUX", sap_vals, unit="e-/s"),
            _flux_col("SAP_FLUX_ERR", sap_err, unit="e-/s"),
            _flux_col("PDCSAP_FLUX", pdc_vals, unit="e-/s"),
            _flux_col("PDCSAP_FLUX_ERR", pdc_err, unit="e-/s"),
        ],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)

    sap = dataset.measurements.series["SAP_FLUX"]
    pdc = dataset.measurements.series["PDCSAP_FLUX"]

    assert sap.uncertainties is not None
    assert np.array_equal(sap.uncertainties, sap_err.astype(np.float64))
    assert pdc.uncertainties is not None
    assert np.array_equal(pdc.uncertainties, pdc_err.astype(np.float64))

    # SAP and PDCSAP uncertainties are distinct arrays
    assert not np.array_equal(sap.uncertainties, pdc.uncertainties)


# ------------------------------------------------------------------
# Missing uncertainty column -> unit="" and warning
# ------------------------------------------------------------------


def test_missing_uncertainty_column(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "no_err.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals)],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)

    sap = dataset.measurements.series["SAP_FLUX"]
    assert sap.uncertainties is None
    assert sap.unit == ""

    assert len(dataset.validation.warnings) == 1
    assert dataset.validation.warnings[0].code == "UNCERTAINTY_MISSING"


# ------------------------------------------------------------------
# Missing optional quality/cadence columns -> None
# ------------------------------------------------------------------


def test_missing_optional_quality_cadence(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "no_quality.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals)],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)

    assert dataset.quality_flags is None
    assert dataset.cadence_numbers is None


# ------------------------------------------------------------------
# Quality flags and cadence numbers preserved
# ------------------------------------------------------------------


def test_quality_flags_and_cadence_preserved(tmp_path):
    n = 4
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0, 400.0], dtype=np.float32)
    quality = np.array([0, 64, 0, 128], dtype=np.int32)
    cadence = np.array([568, 569, 570, 571], dtype=np.int32)

    path = _write_fits_file(
        tmp_path,
        "quality.fits",
        time_vals,
        [
            _flux_col("SAP_FLUX", sap_vals),
            _int_col("SAP_QUALITY", quality),
            _int_col("CADENCENO", cadence),
        ],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)

    assert dataset.quality_flags is not None
    assert np.array_equal(dataset.quality_flags, quality.astype(np.int64))
    assert dataset.cadence_numbers is not None
    assert np.array_equal(dataset.cadence_numbers, cadence.astype(np.int64))


# ------------------------------------------------------------------
# Nonzero quality flags -> info finding, not filtered
# ------------------------------------------------------------------


def test_nonzero_quality_flags_info(tmp_path):
    n = 4
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0, 400.0], dtype=np.float32)
    quality = np.array([0, 64, 0, 128], dtype=np.int32)

    path = _write_fits_file(
        tmp_path,
        "quality_nonzero.fits",
        time_vals,
        [
            _flux_col("SAP_FLUX", sap_vals),
            _int_col("SAP_QUALITY", quality),
        ],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)

    # All observations preserved (no filtering)
    assert dataset.n_observations == n
    assert np.array_equal(dataset.quality_flags, quality.astype(np.int64))

    # Info finding about nonzero flags
    info_codes = [f.code for f in dataset.validation.info]
    assert "NONZERO_QUALITY_FLAGS" in info_codes


# ------------------------------------------------------------------
# No structurally valid light-curve HDU -> FITSImportError
# ------------------------------------------------------------------


def test_no_valid_light_curve_table(tmp_path):
    # Image-only file (no table)
    primary = fits.PrimaryHDU()
    image = fits.ImageHDU(data=np.zeros((3, 3), dtype=np.float32))
    hdul = fits.HDUList([primary, image])
    path = tmp_path / "image_only.fits"
    hdul.writeto(path)

    with pytest.raises(FITSImportError):
        import_light_curve(path)


def test_table_without_time_column(tmp_path):
    flux_vals = np.array([100.0, 200.0], dtype=np.float32)
    path = _write_fits_file(
        tmp_path,
        "no_time.fits",
        np.array([1.0, 2.0]),  # dummy, will be replaced
        [_flux_col("SAP_FLUX", flux_vals)],
        ext_header={"TIMEUNIT": "d"},
    )

    # The helper always adds a TIME column; create one without TIME manually
    primary = fits.PrimaryHDU()
    col = fits.Column(name="SAP_FLUX", format="E", array=flux_vals)
    hdu = fits.BinTableHDU.from_columns([col])
    hdu.header["EXTNAME"] = "LIGHTCURVE"
    hdul = fits.HDUList([primary, hdu])
    path = tmp_path / "no_time2.fits"
    hdul.writeto(path)

    with pytest.raises(FITSImportError):
        import_light_curve(path)


def test_table_without_flux_columns(tmp_path):
    time_vals = np.array([1.0, 2.0], dtype=np.float64)
    primary = fits.PrimaryHDU()
    col = fits.Column(name="TIME", format="D", array=time_vals)
    hdu = fits.BinTableHDU.from_columns([col])
    hdu.header["EXTNAME"] = "LIGHTCURVE"
    hdul = fits.HDUList([primary, hdu])
    path = tmp_path / "no_flux.fits"
    hdul.writeto(path)

    with pytest.raises(FITSImportError):
        import_light_curve(path)


# ------------------------------------------------------------------
# Empty table -> FITSImportError
# ------------------------------------------------------------------


def test_empty_table_rejected(tmp_path):
    time_vals = np.array([], dtype=np.float64)
    sap_vals = np.array([], dtype=np.float32)
    path = _write_fits_file(
        tmp_path,
        "empty.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals)],
        ext_header={"TIMEUNIT": "d"},
    )

    with pytest.raises(FITSImportError):
        import_light_curve(path)


# ------------------------------------------------------------------
# Multiple candidate HDUs
# ------------------------------------------------------------------


def test_multiple_candidates_prefers_lightcurve(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)

    # First candidate: structurally valid but named "OTHER"
    other_hdu = fits.BinTableHDU.from_columns(
        [
            fits.Column(name="TIME", format="D", array=time_vals),
            fits.Column(name="SAP_FLUX", format="E", array=sap_vals),
        ]
    )
    other_hdu.header["EXTNAME"] = "OTHER"

    # Second candidate: named LIGHTCURVE (should be preferred)
    path = _write_fits_file(
        tmp_path,
        "multi.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals)],
        ext_header={"TIMEUNIT": "d"},
        extra_hdus=[other_hdu],
    )

    dataset = import_light_curve(path)

    # Should have selected LIGHTCURVE (the one written by _write_fits_file)
    assert dataset.n_observations == n
    # Info finding about ambiguity
    assert any(f.code == "MULTIPLE_LIGHT_CURVE_CANDIDATES" for f in dataset.validation.info)


def test_multiple_candidates_no_lightcurve_first_in_order(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)

    # Two candidates, neither named LIGHTCURVE; first in HDU order wins
    first_hdu = fits.BinTableHDU.from_columns(
        [
            fits.Column(name="TIME", format="D", array=time_vals),
            fits.Column(name="SAP_FLUX", format="E", array=sap_vals),
        ]
    )
    first_hdu.header["EXTNAME"] = "TABLE_A"

    path = _write_fits_file(
        tmp_path,
        "multi2.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals)],
        ext_header={"TIMEUNIT": "d", "EXTNAME": "TABLE_B"},
        extra_hdus=[first_hdu],
    )

    dataset = import_light_curve(path)
    assert dataset.n_observations == n
    assert any(f.code == "MULTIPLE_LIGHT_CURVE_CANDIDATES" for f in dataset.validation.info)


# ------------------------------------------------------------------
# Valid HDU not at index 1
# ------------------------------------------------------------------


def test_valid_hdu_not_at_index_1(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)

    # Insert an unrelated image HDU at index 1, moving LIGHTCURVE to index 2
    image_hdu = fits.ImageHDU(data=np.zeros((2, 2), dtype=np.float32))
    path = _write_fits_file(
        tmp_path,
        "not_index1.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals)],
        ext_header={"TIMEUNIT": "d"},
        extra_hdus=[image_hdu],
    )

    dataset = import_light_curve(path)
    assert dataset.n_observations == n
    assert np.array_equal(
        dataset.measurements.series["SAP_FLUX"].values, sap_vals.astype(np.float64)
    )


# ------------------------------------------------------------------
# Metadata mapping and header-source behavior
# ------------------------------------------------------------------


def test_metadata_from_primary_and_extension_headers(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "metadata.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals)],
        primary_header={
            "MISSION": "Kepler",
            "INSTRUME": "Kepler Photometer",
            "OBJECT": "KIC 11904151",
            "KEPLERID": 11904151,
        },
        ext_header={
            "TIMEUNIT": "d",
            "TIMESYS": "TDB",
            "TIMEREF": "SOLARSYSTEM",
            "BJDREFI": 2454833,
            "BJDREFF": 0.0,
            "TSTART": 10.0,
            "TSTOP": 20.0,
            # TIMEDEL is intentionally not mapped to resolution in this subtask.
        },
    )

    dataset = import_light_curve(path)

    assert dataset.source.mission == "Kepler"
    assert dataset.source.instrument == "Kepler Photometer"
    assert dataset.source.target_object == "KIC 11904151"
    assert dataset.source.source_id == "11904151"

    assert dataset.time.unit == "d"
    assert dataset.time.time_scale == "TDB"
    assert dataset.time.time_reference_frame == "SOLARSYSTEM"
    assert dataset.time.reference_value == 2454833.0
    assert dataset.time.start == 10.0
    assert dataset.time.stop == 20.0
    assert dataset.time.resolution is None


# ------------------------------------------------------------------
# ORIGIN is not treated as archive
# ------------------------------------------------------------------


def test_origin_not_used_as_archive(tmp_path):
    n = 2
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "origin.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals)],
        primary_header={"ORIGIN": "NASA/Ames"},
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)
    assert dataset.source.archive is None


# ------------------------------------------------------------------
# Dataset name is filename stem
# ------------------------------------------------------------------


def test_dataset_name_is_filename_stem(tmp_path):
    n = 2
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "kplr011904151-2009131105131_llc_full.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals)],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)
    assert dataset.name == "kplr011904151-2009131105131_llc_full"
    assert dataset.source.original_filename == "kplr011904151-2009131105131_llc_full.fits"


# ------------------------------------------------------------------
# Unit handling: compatible units
# ------------------------------------------------------------------


def test_compatible_flux_uncertainty_units(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)
    sap_err = np.array([1.0, 2.0, 3.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "compatible_units.fits",
        time_vals,
        [
            _flux_col("SAP_FLUX", sap_vals, unit="e-/s"),
            _flux_col("SAP_FLUX_ERR", sap_err, unit="e-/s"),
        ],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)
    sap = dataset.measurements.series["SAP_FLUX"]
    assert sap.unit == "e-/s"
    assert sap.uncertainties is not None


def test_both_units_blank_import_with_empty_unit(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)
    sap_err = np.array([1.0, 2.0, 3.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "blank_units.fits",
        time_vals,
        [
            _flux_col("SAP_FLUX", sap_vals, unit=None),
            _flux_col("SAP_FLUX_ERR", sap_err, unit=None),
        ],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)
    sap = dataset.measurements.series["SAP_FLUX"]
    assert sap.unit == ""
    assert sap.uncertainties is not None


# ------------------------------------------------------------------
# Unit handling: incompatible cases all raise FITSImportError
# ------------------------------------------------------------------


def test_flux_unit_present_uncertainty_unit_absent(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)
    sap_err = np.array([1.0, 2.0, 3.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "mismatch1.fits",
        time_vals,
        [
            _flux_col("SAP_FLUX", sap_vals, unit="e-/s"),
            _flux_col("SAP_FLUX_ERR", sap_err, unit=None),
        ],
        ext_header={"TIMEUNIT": "d"},
    )

    with pytest.raises(FITSImportError):
        import_light_curve(path)


def test_flux_unit_absent_uncertainty_unit_present(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)
    sap_err = np.array([1.0, 2.0, 3.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "mismatch2.fits",
        time_vals,
        [
            _flux_col("SAP_FLUX", sap_vals, unit=None),
            _flux_col("SAP_FLUX_ERR", sap_err, unit="e-/s"),
        ],
        ext_header={"TIMEUNIT": "d"},
    )

    with pytest.raises(FITSImportError):
        import_light_curve(path)


def test_flux_and_uncertainty_units_different(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)
    sap_err = np.array([1.0, 2.0, 3.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "mismatch3.fits",
        time_vals,
        [
            _flux_col("SAP_FLUX", sap_vals, unit="e-/s"),
            _flux_col("SAP_FLUX_ERR", sap_err, unit="W/m^2"),
        ],
        ext_header={"TIMEUNIT": "d"},
    )

    with pytest.raises(FITSImportError):
        import_light_curve(path)


# ------------------------------------------------------------------
# Preserve unfamiliar nonblank unit strings
# ------------------------------------------------------------------


def test_unfamiliar_unit_string_preserved(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "unfamiliar.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals, unit="Jy")],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)
    sap = dataset.measurements.series["SAP_FLUX"]
    assert sap.unit == "Jy"


def test_time_unit_preserved_unfamiliar(tmp_path):
    n = 2
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "time_unit.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals)],
        ext_header={"TIMEUNIT": "days"},
    )

    dataset = import_light_curve(path)
    assert dataset.time.unit == "days"


# ------------------------------------------------------------------
# Whitespace-only unit strings treated as blank
# ------------------------------------------------------------------


def test_whitespace_only_unit_treated_as_blank(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)
    sap_err = np.array([1.0, 2.0, 3.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "whitespace.fits",
        time_vals,
        [
            _flux_col("SAP_FLUX", sap_vals, unit="   "),
            _flux_col("SAP_FLUX_ERR", sap_err, unit="  "),
        ],
        ext_header={"TIMEUNIT": "  "},
    )

    dataset = import_light_curve(path)
    sap = dataset.measurements.series["SAP_FLUX"]
    assert sap.unit == ""
    assert dataset.time.unit == ""


# ------------------------------------------------------------------
# Flux unit stored in single MeasurementColumn.unit field
# ------------------------------------------------------------------


def test_flux_unit_in_single_unit_field(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)
    sap_err = np.array([1.0, 2.0, 3.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "single_unit.fits",
        time_vals,
        [
            _flux_col("SAP_FLUX", sap_vals, unit="e-/s"),
            _flux_col("SAP_FLUX_ERR", sap_err, unit="e-/s"),
        ],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)
    sap = dataset.measurements.series["SAP_FLUX"]

    # Single unit field holds the flux unit
    assert sap.unit == "e-/s"
    # No separate uncertainty unit field exists on the model
    assert not hasattr(sap, "uncertainty_unit")


# ------------------------------------------------------------------
# Orphan uncertainty column -> warning
# ------------------------------------------------------------------


def test_orphan_sap_err_warning(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_err = np.array([1.0, 2.0, 3.0], dtype=np.float32)
    pdc_vals = np.array([101.0, 201.0, 301.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "orphan_sap_err.fits",
        time_vals,
        [
            _flux_col("SAP_FLUX_ERR", sap_err),
            _flux_col("PDCSAP_FLUX", pdc_vals),
        ],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)

    # SAP_FLUX absent, so orphan SAP_FLUX_ERR ignored
    assert "SAP_FLUX" not in dataset.measurements.series
    assert "PDCSAP_FLUX" in dataset.measurements.series

    # Warning raised
    warning_codes = [f.code for f in dataset.validation.warnings]
    assert "ORPHAN_UNCERTAINTY" in warning_codes


def test_orphan_pdc_err_warning(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)
    pdc_err = np.array([1.0, 2.0, 3.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "orphan_pdc_err.fits",
        time_vals,
        [
            _flux_col("SAP_FLUX", sap_vals),
            _flux_col("PDCSAP_FLUX_ERR", pdc_err),
        ],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)

    assert "PDCSAP_FLUX" not in dataset.measurements.series
    assert "SAP_FLUX" in dataset.measurements.series

    warning_codes = [f.code for f in dataset.validation.warnings]
    assert "ORPHAN_UNCERTAINTY" in warning_codes


# ------------------------------------------------------------------
# Numeric type conversion and incompatible dtype rejection
# ------------------------------------------------------------------


def test_float32_converted_to_float64(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "float32.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals)],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)
    sap = dataset.measurements.series["SAP_FLUX"]
    assert sap.values.dtype == np.float64
    assert dataset.time.values.dtype == np.float64


def test_int32_quality_converted_to_int64(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)
    quality = np.array([0, 64, 0], dtype=np.int32)

    path = _write_fits_file(
        tmp_path,
        "int_quality.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals), _int_col("SAP_QUALITY", quality)],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)
    assert dataset.quality_flags is not None
    assert dataset.quality_flags.dtype == np.int64


def test_string_column_rejected(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    # Create a string column where SAP_FLUX should be
    primary = fits.PrimaryHDU()
    cols = [
        fits.Column(name="TIME", format="D", array=time_vals),
        fits.Column(name="SAP_FLUX", format="20A", array=np.array(["a", "b", "c"])),
    ]
    hdu = fits.BinTableHDU.from_columns(cols)
    hdu.header["EXTNAME"] = "LIGHTCURVE"
    hdu.header["TIMEUNIT"] = "d"
    hdul = fits.HDUList([primary, hdu])
    path = tmp_path / "string_flux.fits"
    hdul.writeto(path)

    with pytest.raises(FITSImportError):
        import_light_curve(path)


def test_float_quality_rejected(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)
    # Quality as float (would require truncation to int)
    primary = fits.PrimaryHDU()
    cols = [
        fits.Column(name="TIME", format="D", array=time_vals),
        fits.Column(name="SAP_FLUX", format="E", array=sap_vals),
        fits.Column(name="SAP_QUALITY", format="E", array=np.array([0.0, 64.0, 0.0], dtype=np.float32)),
    ]
    hdu = fits.BinTableHDU.from_columns(cols)
    hdu.header["EXTNAME"] = "LIGHTCURVE"
    hdu.header["TIMEUNIT"] = "d"
    hdul = fits.HDUList([primary, hdu])
    path = tmp_path / "float_quality.fits"
    hdul.writeto(path)

    with pytest.raises(FITSImportError):
        import_light_curve(path)


# ------------------------------------------------------------------
# Non-finite values preserved
# ------------------------------------------------------------------


def test_nonfinite_flux_preserved(tmp_path):
    n = 5
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, np.nan, 300.0, np.inf, 500.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "nonfinite.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals)],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)
    sap = dataset.measurements.series["SAP_FLUX"]

    assert np.isnan(sap.values[1])
    assert np.isposinf(sap.values[3])
    assert sap.n_nonfinite == 2

    # Warning raised
    assert any(f.code == "NONFINITE_VALUES" for f in dataset.validation.warnings)


def test_nonfinite_uncertainty_preserved(tmp_path):
    n = 4
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0, 400.0], dtype=np.float32)
    sap_err = np.array([1.0, np.nan, 3.0, 4.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "nonfinite_err.fits",
        time_vals,
        [
            _flux_col("SAP_FLUX", sap_vals),
            _flux_col("SAP_FLUX_ERR", sap_err),
        ],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)
    sap = dataset.measurements.series["SAP_FLUX"]
    assert sap.uncertainties is not None
    assert np.isnan(sap.uncertainties[1])


def test_negative_uncertainty_warning(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)
    sap_err = np.array([1.0, -2.0, 3.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "negative_err.fits",
        time_vals,
        [
            _flux_col("SAP_FLUX", sap_vals),
            _flux_col("SAP_FLUX_ERR", sap_err),
        ],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)
    sap = dataset.measurements.series["SAP_FLUX"]
    assert sap.uncertainties is not None
    assert sap.uncertainties[1] == -2.0  # Preserved, not replaced

    assert any(f.code == "NEGATIVE_UNCERTAINTY" for f in dataset.validation.warnings)


# ------------------------------------------------------------------
# Duplicate and non-monotonic times
# ------------------------------------------------------------------


def test_duplicate_times_warning(tmp_path):
    n = 4
    time_vals = np.array([100.0, 100.0, 101.0, 102.0], dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0, 400.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "dup_time.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals)],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)
    # Order preserved, not reordered
    assert np.array_equal(dataset.time.values, time_vals)

    assert any(f.code == "DUPLICATE_TIME" for f in dataset.validation.warnings)


def test_non_monotonic_times_warning(tmp_path):
    n = 4
    time_vals = np.array([100.0, 102.0, 101.0, 103.0], dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0, 400.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "nonmono_time.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals)],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)
    # Order preserved, not reordered
    assert np.array_equal(dataset.time.values, time_vals)

    assert any(f.code == "NONMONOTONIC_TIME" for f in dataset.validation.warnings)


# ------------------------------------------------------------------
# Integer TNULL sentinel handling
# ------------------------------------------------------------------


def test_tnull_sentinel_declared_but_unused(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)
    # TNULL=-999 declared but no value equals -999
    quality = np.array([0, 64, 0], dtype=np.int32)

    path = _write_fits_file(
        tmp_path,
        "tnull_unused.fits",
        time_vals,
        [
            _flux_col("SAP_FLUX", sap_vals),
            _int_col("SAP_QUALITY", quality, null=-999),
        ],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)
    assert dataset.quality_flags is not None
    assert np.array_equal(dataset.quality_flags, quality.astype(np.int64))


def test_tnull_sentinel_present_in_data(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)
    # TNULL=-999 and value -999 is present
    quality = np.array([0, -999, 0], dtype=np.int32)

    path = _write_fits_file(
        tmp_path,
        "tnull_present.fits",
        time_vals,
        [
            _flux_col("SAP_FLUX", sap_vals),
            _int_col("SAP_QUALITY", quality, null=-999),
        ],
        ext_header={"TIMEUNIT": "d"},
    )

    with pytest.raises(FITSImportError):
        import_light_curve(path)


# ------------------------------------------------------------------
# Unit comparison: whitespace handling
# ------------------------------------------------------------------


def test_unit_comparison_trims_whitespace(tmp_path):
    """Flux unit "e-/s" and uncertainty unit " e-/s " are equivalent after trimming."""
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)
    sap_err = np.array([1.0, 2.0, 3.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "whitespace_units.fits",
        time_vals,
        [
            _flux_col("SAP_FLUX", sap_vals, unit="e-/s"),
            _flux_col("SAP_FLUX_ERR", sap_err, unit=" e-/s "),
        ],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)
    sap = dataset.measurements.series["SAP_FLUX"]
    # Original nonblank flux unit string is preserved, not the trimmed version.
    assert sap.unit == "e-/s"
    assert sap.uncertainties is not None


def test_unit_comparison_different_after_trim(tmp_path):
    """Flux unit "e-/s" and uncertainty unit "electron/s" are incompatible."""
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)
    sap_err = np.array([1.0, 2.0, 3.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "diff_units.fits",
        time_vals,
        [
            _flux_col("SAP_FLUX", sap_vals, unit="e-/s"),
            _flux_col("SAP_FLUX_ERR", sap_err, unit="electron/s"),
        ],
        ext_header={"TIMEUNIT": "d"},
    )

    with pytest.raises(FITSImportError):
        import_light_curve(path)


# ------------------------------------------------------------------
# Numeric dtype: numeric-looking strings rejected
# ------------------------------------------------------------------


def test_numeric_string_column_rejected(tmp_path):
    """A string column whose contents parse as numbers is still rejected."""
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    primary = fits.PrimaryHDU()
    cols = [
        fits.Column(name="TIME", format="D", array=time_vals),
        fits.Column(
            name="SAP_FLUX",
            format="20A",
            array=np.array(["1.0", "2.0", "3.0"]),
        ),
    ]
    hdu = fits.BinTableHDU.from_columns(cols)
    hdu.header["EXTNAME"] = "LIGHTCURVE"
    hdu.header["TIMEUNIT"] = "d"
    hdul = fits.HDUList([primary, hdu])
    path = tmp_path / "numeric_string_flux.fits"
    hdul.writeto(path)

    with pytest.raises(FITSImportError):
        import_light_curve(path)


# ------------------------------------------------------------------
# Integer overflow protection (unsigned 64-bit via TZERO)
# ------------------------------------------------------------------


def _write_uint64_fits_file(
    tmp_path: Path,
    filename: str,
    time_values: np.ndarray,
    cadence_values: np.ndarray,
    tzero: int | None = None,
) -> Path:
    """Write a FITS file with a 64-bit integer CADENCENO column.

    Uses format K (signed 64-bit) with optional TZERO = 2**63 to represent
    unsigned 64-bit values per the FITS unsigned-integer convention.
    """
    ph = fits.PrimaryHDU()
    ph.header["SIMPLE"] = True
    ph.header["BITPIX"] = 8
    ph.header["NAXIS"] = 0
    ph.header["EXTEND"] = True

    th = fits.Header()
    th["XTENSION"] = ("BINTABLE", "binary table extension")
    th["BITPIX"] = (8, "array data type")
    th["NAXIS"] = (2, "number of array dimensions")
    th["NAXIS1"] = (16, "length of first array dimension")
    th["NAXIS2"] = (len(time_values), "length of second array dimension")
    th["PCOUNT"] = (0, "group parameter count")
    th["GCOUNT"] = (1, "group count")
    th["TFIELDS"] = (2, "number of table fields")
    th["TTYPE1"] = ("TIME", "column title")
    th["TFORM1"] = ("1D", "column format")
    th["TTYPE2"] = ("CADENCENO", "column title")
    th["TFORM2"] = ("1K", "column format")
    if tzero is not None:
        th["TZERO2"] = (tzero, "unsigned integer offset")

    primary_bytes = ph.header.tostring().encode("ascii")
    primary_padded = primary_bytes + b" " * (2880 - len(primary_bytes))

    table_header_bytes = th.tostring().encode("ascii")
    table_header_padded = table_header_bytes + b" " * (2880 - len(table_header_bytes))

    import struct as _struct

    rows = b""
    for t, c in zip(time_values, cadence_values):
        rows += _struct.pack("<d", t) + _struct.pack("<q", c)
    data_bytes = rows
    data_padded = data_bytes + b"\x00" * (2880 - len(data_bytes))

    full_file = primary_padded + table_header_padded + data_padded

    from io import BytesIO as _BytesIO

    buf = _BytesIO(full_file)
    with fits.open(buf) as hdul:
        # Re-write to a proper file via astropy
        tmp_hdul = fits.HDUList([fits.PrimaryHDU(), hdul[1].copy()])
        filepath = tmp_path / filename
        tmp_hdul.writeto(filepath)
    return filepath


def test_int64_max_accepted(tmp_path):
    """The largest valid int64 value is accepted."""
    n = 2
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0], dtype=np.float32)
    max_i64 = np.iinfo(np.int64).max
    cadence = np.array([max_i64, max_i64 - 1], dtype=np.int64)

    primary = fits.PrimaryHDU()
    cols = [
        fits.Column(name="TIME", format="D", array=time_vals),
        fits.Column(name="SAP_FLUX", format="E", array=sap_vals),
        fits.Column(name="CADENCENO", format="K", array=cadence),
    ]
    hdu = fits.BinTableHDU.from_columns(cols)
    hdu.header["EXTNAME"] = "LIGHTCURVE"
    hdu.header["TIMEUNIT"] = "d"
    hdul = fits.HDUList([primary, hdu])
    path = tmp_path / "int64_max.fits"
    hdul.writeto(path)

    dataset = import_light_curve(path)
    assert dataset.cadence_numbers is not None
    assert dataset.cadence_numbers[0] == max_i64


def test_unsigned_int64_overflow_rejected(tmp_path):
    """An unsigned 64-bit value above int64 max (via TZERO=2**63) is rejected."""
    n = 2
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0], dtype=np.float32)
    # Raw value 0 with TZERO=2**63 represents unsigned 2**63, which exceeds int64 max.
    cadence_raw = np.array([0, 0], dtype=np.int64)

    path = _write_uint64_fits_file(
        tmp_path,
        "uint64_overflow.fits",
        time_vals,
        cadence_raw,
        tzero=2**63,
    )

    with pytest.raises(FITSImportError):
        import_light_curve(path)


# ------------------------------------------------------------------
# Duplicate supported column names (raw FITS fixture)
# ------------------------------------------------------------------


def test_duplicate_supported_column_names_rejected(tmp_path):
    """A table with duplicate TTYPE for a supported column is rejected."""
    import struct as _struct

    ph = fits.PrimaryHDU()
    ph.header["SIMPLE"] = True
    ph.header["BITPIX"] = 8
    ph.header["NAXIS"] = 0
    ph.header["EXTEND"] = True

    th = fits.Header()
    th["XTENSION"] = ("BINTABLE", "binary table extension")
    th["BITPIX"] = (8, "array data type")
    th["NAXIS"] = (2, "number of array dimensions")
    th["NAXIS1"] = (16, "length of first array dimension")
    th["NAXIS2"] = (2, "length of second array dimension")
    th["PCOUNT"] = (0, "group parameter count")
    th["GCOUNT"] = (1, "group count")
    th["TFIELDS"] = (3, "number of table fields")
    th["TTYPE1"] = ("TIME", "column title")
    th["TFORM1"] = ("1D", "column format")
    th["TTYPE2"] = ("SAP_FLUX", "column title")
    th["TFORM2"] = ("1E", "column format")
    th["TTYPE3"] = ("SAP_FLUX", "column title duplicate")
    th["TFORM3"] = ("1E", "column format")

    primary_bytes = ph.header.tostring().encode("ascii")
    primary_padded = primary_bytes + b" " * (2880 - len(primary_bytes))

    table_header_bytes = th.tostring().encode("ascii")
    table_header_padded = table_header_bytes + b" " * (2880 - len(table_header_bytes))

    row1 = _struct.pack("<d", 1.0) + _struct.pack("<f", 100.0) + _struct.pack("<f", 200.0)
    row2 = _struct.pack("<d", 2.0) + _struct.pack("<f", 300.0) + _struct.pack("<f", 400.0)
    data_bytes = row1 + row2
    data_padded = data_bytes + b"\x00" * (2880 - len(data_bytes))

    full_file = primary_padded + table_header_padded + data_padded

    filepath = tmp_path / "duplicate_columns.fits"
    filepath.write_bytes(full_file)

    with pytest.raises(FITSImportError):
        import_light_curve(filepath)


# ------------------------------------------------------------------
# Column-position independence
# ------------------------------------------------------------------


def test_column_position_independence(tmp_path):
    """Units and measurements are mapped by column name, not position."""
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)
    sap_err = np.array([1.0, 2.0, 3.0], dtype=np.float32)
    pdc_vals = np.array([101.0, 201.0, 301.0], dtype=np.float32)
    pdc_err = np.array([1.1, 2.1, 3.1], dtype=np.float32)

    # PDCSAP columns come before SAP columns (different order than Kepler).
    path = _write_fits_file(
        tmp_path,
        "reordered.fits",
        time_vals,
        [
            _flux_col("PDCSAP_FLUX", pdc_vals, unit="e-/s"),
            _flux_col("PDCSAP_FLUX_ERR", pdc_err, unit="e-/s"),
            _flux_col("SAP_FLUX", sap_vals, unit="e-/s"),
            _flux_col("SAP_FLUX_ERR", sap_err, unit="e-/s"),
        ],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)
    assert "SAP_FLUX" in dataset.measurements.series
    assert "PDCSAP_FLUX" in dataset.measurements.series
    assert np.array_equal(
        dataset.measurements.series["SAP_FLUX"].values, sap_vals.astype(np.float64)
    )
    assert np.array_equal(
        dataset.measurements.series["PDCSAP_FLUX"].values, pdc_vals.astype(np.float64)
    )
    assert np.array_equal(
        dataset.measurements.series["SAP_FLUX"].uncertainties, sap_err.astype(np.float64)
    )
    assert np.array_equal(
        dataset.measurements.series["PDCSAP_FLUX"].uncertainties, pdc_err.astype(np.float64)
    )
    assert dataset.measurements.series["SAP_FLUX"].unit == "e-/s"
    assert dataset.measurements.series["PDCSAP_FLUX"].unit == "e-/s"


# ------------------------------------------------------------------
# TNULL at non-index-1 HDU
# ------------------------------------------------------------------


def test_tnull_at_non_index_1_hdu(tmp_path):
    """TNULL sentinel in an integer column at HDU index 2 is rejected."""
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)
    quality = np.array([0, -999, 0], dtype=np.int32)  # -999 is the TNULL sentinel

    # Insert an unrelated image HDU at index 1
    image_hdu = fits.ImageHDU(data=np.zeros((2, 2), dtype=np.float32))

    # Build table HDU with TNULL sentinel on SAP_QUALITY using fits.Column
    cols = [
        fits.Column(name="TIME", format="D", array=time_vals),
        fits.Column(name="SAP_FLUX", format="E", array=sap_vals),
        fits.Column(name="SAP_QUALITY", format="J", array=quality, null=-999),
    ]
    table_hdu = fits.BinTableHDU.from_columns(cols)
    table_hdu.header["EXTNAME"] = "LIGHTCURVE"
    table_hdu.header["TIMEUNIT"] = "d"

    # Write primary + table, then insert image at index 1
    ph = fits.PrimaryHDU()
    hdul = fits.HDUList([ph, table_hdu])
    filepath_raw = tmp_path / "tnull_raw.fits"
    hdul.writeto(filepath_raw)

    filepath = tmp_path / "tnull_not_index1.fits"
    with fits.open(filepath_raw) as hdul2:
        hdul2.insert(1, image_hdu)
        hdul2.writeto(filepath)

    with pytest.raises(FITSImportError):
        import_light_curve(filepath)


# ------------------------------------------------------------------
# Partial BJD reference metadata
# ------------------------------------------------------------------


def test_bjdref_both_components(tmp_path):
    n = 2
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "bjd_both.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals)],
        ext_header={"TIMEUNIT": "d", "BJDREFI": 2454833, "BJDREFF": 0.5},
    )

    dataset = import_light_curve(path)
    assert dataset.time.reference_value == 2454833.5


def test_bjdref_only_fifi(tmp_path):
    """Only BJDREFI present: missing BJDREFF treated as zero."""
    n = 2
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "bjd_only_fifi.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals)],
        ext_header={"TIMEUNIT": "d", "BJDREFI": 2454833},
    )

    dataset = import_light_curve(path)
    assert dataset.time.reference_value == 2454833.0


def test_bjdref_only_ffif(tmp_path):
    """Only BJDREFF present: missing BJDREFI treated as zero."""
    n = 2
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "bjd_only_ffif.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals)],
        ext_header={"TIMEUNIT": "d", "BJDREFF": 0.5},
    )

    dataset = import_light_curve(path)
    assert dataset.time.reference_value == 0.5


def test_bjdref_neither(tmp_path):
    """Neither BJDREFI nor BJDREFF present: reference_value is None."""
    n = 2
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "bjd_neither.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals)],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)
    assert dataset.time.reference_value is None


# ------------------------------------------------------------------
# Duplicate vs non-monotonic timestamps
# ------------------------------------------------------------------


def test_duplicate_times_non_adjacent(tmp_path):
    """Duplicate timestamps at non-adjacent positions: duplicate warning plus
    non-monotonic warning because 100 at index 2 is less than 101 at index 1."""
    n = 5
    time_vals = np.array([100.0, 101.0, 100.0, 102.0, 103.0], dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0, 400.0, 500.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "dup_nonadj.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals)],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)
    assert np.array_equal(dataset.time.values, time_vals)

    warning_codes = [f.code for f in dataset.validation.warnings]
    assert "DUPLICATE_TIME" in warning_codes
    assert "NONMONOTONIC_TIME" in warning_codes


def test_duplicates_and_decreasing_times(tmp_path):
    """Both duplicate and decreasing timestamps produce both warnings."""
    n = 5
    time_vals = np.array([100.0, 100.0, 99.0, 101.0, 102.0], dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0, 400.0, 500.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "dup_and_decreasing.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals)],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)
    assert np.array_equal(dataset.time.values, time_vals)

    warning_codes = [f.code for f in dataset.validation.warnings]
    assert "DUPLICATE_TIME" in warning_codes
    assert "NONMONOTONIC_TIME" in warning_codes


# ------------------------------------------------------------------
# Missing metadata -> unknown, not fabricated
# ------------------------------------------------------------------


def test_missing_metadata_unknown(tmp_path):
    n = 2
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "no_meta.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals)],
    )

    dataset = import_light_curve(path)

    assert dataset.source.mission is None
    assert dataset.source.instrument is None
    assert dataset.source.target_object is None
    assert dataset.source.source_id is None
    assert dataset.source.archive is None

    assert dataset.time.unit == ""
    assert dataset.time.reference == ""
    assert dataset.time.time_scale == ""
    assert dataset.time.time_reference_frame == ""

    # Info finding for missing time unit
    assert any(f.code == "MISSING_TIME_UNIT" for f in dataset.validation.info)


# ------------------------------------------------------------------
# Data preservation: observation count and values
# ------------------------------------------------------------------


def test_observation_count_and_values_preserved(tmp_path):
    n = 7
    time_vals = np.linspace(100.0, 110.0, n)
    sap_vals = np.array([500.0 + i for i in range(n)], dtype=np.float32)
    pdc_vals = np.array([501.0 + i for i in range(n)], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "preserve.fits",
        time_vals,
        [
            _flux_col("SAP_FLUX", sap_vals),
            _flux_col("PDCSAP_FLUX", pdc_vals),
        ],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)
    assert dataset.n_observations == n
    assert np.array_equal(dataset.time.values, time_vals)
    assert np.array_equal(
        dataset.measurements.series["SAP_FLUX"].values, sap_vals.astype(np.float64)
    )
    assert np.array_equal(
        dataset.measurements.series["PDCSAP_FLUX"].values, pdc_vals.astype(np.float64)
    )


# ------------------------------------------------------------------
# Resource safety: data usable after file closed
# ------------------------------------------------------------------


def test_data_usable_after_file_closed(tmp_path):
    n = 3
    time_vals = np.arange(n, dtype=np.float64)
    sap_vals = np.array([100.0, 200.0, 300.0], dtype=np.float32)

    path = _write_fits_file(
        tmp_path,
        "resource.fits",
        time_vals,
        [_flux_col("SAP_FLUX", sap_vals)],
        ext_header={"TIMEUNIT": "d"},
    )

    dataset = import_light_curve(path)

    # File is closed inside import_light_curve; accessing data here
    # proves arrays are independently owned copies.
    assert dataset.n_observations == n
    assert np.array_equal(dataset.time.values, time_vals)
    assert np.array_equal(
        dataset.measurements.series["SAP_FLUX"].values, sap_vals.astype(np.float64)
    )


# ------------------------------------------------------------------
# Serialization round-trip
# ------------------------------------------------------------------


def test_serialization_round_trip(tmp_path):
    n = 4
    time_vals = np.arange(n, dtype=np.float64) + 10.0
    sap_vals = np.array([100.0, 200.0, 300.0, 400.0], dtype=np.float32)
    sap_err = np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float32)
    quality = np.array([0, 64, 0, 128], dtype=np.int32)
    cadence = np.array([568, 569, 570, 571], dtype=np.int32)

    path = _write_fits_file(
        tmp_path,
        "roundtrip.fits",
        time_vals,
        [
            _flux_col("SAP_FLUX", sap_vals, unit="e-/s"),
            _flux_col("SAP_FLUX_ERR", sap_err, unit="e-/s"),
            _int_col("SAP_QUALITY", quality),
            _int_col("CADENCENO", cadence),
        ],
        primary_header={"MISSION": "Kepler", "OBJECT": "KIC 11904151"},
        ext_header={"TIMEUNIT": "d", "TIMESYS": "TDB"},
    )

    dataset = import_light_curve(path)
    data = dataset.to_dict()
    restored = LightCurveDataset.from_dict(data)

    assert restored.dataset_id == dataset.dataset_id
    assert restored.name == dataset.name
    assert restored.n_observations == n
    assert np.array_equal(restored.time.values, dataset.time.values)
    assert restored.time.unit == dataset.time.unit
    assert restored.time.time_scale == dataset.time.time_scale
    assert np.array_equal(
        restored.measurements.series["SAP_FLUX"].values,
        dataset.measurements.series["SAP_FLUX"].values,
    )
    assert restored.measurements.series["SAP_FLUX"].unit == "e-/s"
    assert restored.measurements.series["SAP_FLUX"].uncertainties is not None
    assert np.array_equal(
        restored.measurements.series["SAP_FLUX"].uncertainties,
        dataset.measurements.series["SAP_FLUX"].uncertainties,
    )
    assert restored.quality_flags is not None
    assert np.array_equal(restored.quality_flags, dataset.quality_flags)
    assert restored.cadence_numbers is not None
    assert np.array_equal(restored.cadence_numbers, dataset.cadence_numbers)
    assert restored.source.mission == "Kepler"
    assert restored.source.target_object == "KIC 11904151"


# ------------------------------------------------------------------
# Unreadable / missing file -> FITSImportError
# ------------------------------------------------------------------


def test_missing_file_raises(tmp_path):
    missing = tmp_path / "does_not_exist.fits"
    with pytest.raises(FITSImportError):
        import_light_curve(missing)


# ------------------------------------------------------------------
# Corrupted file -> FITSImportError
# ------------------------------------------------------------------


def test_corrupted_file_raises(tmp_path):
    path = tmp_path / "corrupt.fits"
    path.write_bytes(b"not a fits file at all")
    with pytest.raises(FITSImportError):
        import_light_curve(path)
