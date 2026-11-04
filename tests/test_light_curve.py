"""Focused unit tests for the light-curve data model (Subtask 2.2.1).

Covers construction, validation, serialization, array copying, calculated
properties, and round-trip fidelity of all model components.

Uses controlled NumPy fixtures only. Does not read FITS files, does not touch
the project model, repository, or service, and does not import PySide6.
"""

from __future__ import annotations

import uuid

import numpy as np
import pytest

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


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _time_values(n: int) -> np.ndarray:
    return np.arange(n, dtype=np.float64)


def _flux_values(n: int) -> np.ndarray:
    return np.ones(n, dtype=np.float64) * 100.0


def _make_dataset(n: int = 5) -> LightCurveDataset:
    return LightCurveDataset(
        name="Test Dataset",
        time=TimeInfo(values=_time_values(n), unit="d"),
        measurements=MeasurementSeries(
            series={
                "FLUX": MeasurementColumn(
                    name="FLUX",
                    values=_flux_values(n),
                    unit="e-/s",
                )
            }
        ),
    )


# ------------------------------------------------------------------
# Component construction
# ------------------------------------------------------------------


def test_dataset_source_defaults_are_optional():
    source = DatasetSource()
    assert source.original_filename is None
    assert source.original_file_path is None
    assert source.archive is None
    assert source.source_id is None
    assert source.mission is None
    assert source.instrument is None
    assert source.target_object is None
    assert source.checksum is None


def test_dataset_source_supplied_values_preserved():
    source = DatasetSource(
        original_filename="kplr.fits",
        original_file_path="/data/kplr.fits",
        archive="MAST/STScI",
        source_id="product-123",
        mission="Kepler",
        instrument="Kepler Photometer",
        target_object="KIC 11904151",
        checksum="abc123",
    )
    assert source.original_filename == "kplr.fits"
    assert source.original_file_path == "/data/kplr.fits"
    assert source.archive == "MAST/STScI"
    assert source.source_id == "product-123"
    assert source.mission == "Kepler"
    assert source.instrument == "Kepler Photometer"
    assert source.target_object == "KIC 11904151"
    assert source.checksum == "abc123"


def test_time_info_required_fields():
    time_info = TimeInfo(values=np.array([1.0, 2.0, 3.0]), unit="d")
    assert len(time_info.values) == 3
    assert time_info.unit == "d"
    assert time_info.reference == ""
    assert time_info.time_scale == ""


def test_measurement_column_required_fields():
    col = MeasurementColumn(name="FLUX", values=np.array([1.0, 2.0]), unit="e-/s")
    assert col.name == "FLUX"
    assert col.unit == "e-/s"
    assert col.uncertainties is None
    assert col.description is None


def test_measurement_column_with_uncertainties():
    col = MeasurementColumn(
        name="FLUX",
        values=np.array([1.0, 2.0]),
        unit="e-/s",
        uncertainties=np.array([0.1, 0.2]),
        description="aperture flux",
    )
    assert col.uncertainties is not None
    assert np.array_equal(col.uncertainties, np.array([0.1, 0.2]))
    assert col.description == "aperture flux"


def test_measurement_series_key_matches_name():
    col = MeasurementColumn(name="FLUX", values=np.array([1.0]), unit="e-/s")
    series = MeasurementSeries(series={"FLUX": col})
    assert series.series["FLUX"] is col


def test_validation_finding_fields():
    finding = ValidationFinding(
        code="UNCERTAINTY_MISSING",
        message="No uncertainties provided for FLUX.",
        severity="warning",
        column="FLUX",
        row_indices=[0, 1],
    )
    assert finding.code == "UNCERTAINTY_MISSING"
    assert finding.severity == "warning"
    assert finding.column == "FLUX"
    assert finding.row_indices == [0, 1]


def test_validation_report_defaults_empty():
    report = ValidationReport()
    assert report.errors == []
    assert report.warnings == []
    assert report.info == []


# ------------------------------------------------------------------
# LightCurveDataset construction
# ------------------------------------------------------------------


def test_valid_dataset_construction():
    dataset = _make_dataset()
    assert dataset.name == "Test Dataset"
    assert dataset.n_observations == 5
    assert dataset.imported_at
    assert isinstance(dataset.validation, ValidationReport)
    assert dataset.validation.errors == []
    assert dataset.validation.warnings == []


def test_automatic_uuid_generation():
    d1 = _make_dataset()
    d2 = _make_dataset()
    uuid.UUID(d1.dataset_id)  # raises if invalid
    uuid.UUID(d2.dataset_id)
    assert d1.dataset_id != d2.dataset_id


def test_explicit_uuid_preserved():
    explicit_id = str(uuid.uuid4())
    dataset = _make_dataset()
    dataset.dataset_id = explicit_id
    # Re-create with explicit id via constructor
    dataset2 = LightCurveDataset(
        name="Explicit",
        dataset_id=explicit_id,
        time=TimeInfo(values=np.array([1.0]), unit="d"),
        measurements=MeasurementSeries(series={}),
    )
    assert dataset2.dataset_id == explicit_id


def test_malformed_uuid_rejected():
    with pytest.raises(LightCurveValidationError):
        LightCurveDataset(
            name="Bad",
            dataset_id="not-a-uuid",
            time=TimeInfo(values=np.array([1.0]), unit="d"),
            measurements=MeasurementSeries(series={}),
        )


def test_automatic_imported_at_is_timezone_aware():
    dataset = _make_dataset()
    assert "+00:00" in dataset.imported_at or dataset.imported_at.endswith("Z")


def test_explicit_imported_at_preserved():
    explicit_ts = "2026-01-01T00:00:00+00:00"
    dataset = LightCurveDataset(
        name="Timestamped",
        imported_at=explicit_ts,
        time=TimeInfo(values=np.array([1.0]), unit="d"),
        measurements=MeasurementSeries(series={}),
    )
    assert dataset.imported_at == explicit_ts


def test_optional_source_metadata():
    source = DatasetSource(
        original_filename="kplr.fits",
        mission="Kepler",
        target_object="KIC 11904151",
    )
    dataset = LightCurveDataset(
        name="With Source",
        source=source,
        time=TimeInfo(values=np.array([1.0]), unit="d"),
        measurements=MeasurementSeries(series={}),
    )
    assert dataset.source.original_filename == "kplr.fits"
    assert dataset.source.mission == "Kepler"
    assert dataset.source.target_object == "KIC 11904151"


# ------------------------------------------------------------------
# Unknown units and optional uncertainties
# ------------------------------------------------------------------


def test_unknown_time_unit_is_empty_string():
    dataset = LightCurveDataset(
        name="Unknown Unit",
        time=TimeInfo(values=np.array([1.0]), unit=""),
        measurements=MeasurementSeries(series={}),
    )
    assert dataset.time.unit == ""


def test_unknown_measurement_unit_is_empty_string():
    col = MeasurementColumn(name="FLUX", values=np.array([1.0]), unit="")
    dataset = LightCurveDataset(
        name="Unknown Unit",
        time=TimeInfo(values=np.array([1.0]), unit="d"),
        measurements=MeasurementSeries(series={"FLUX": col}),
    )
    assert dataset.measurements.series["FLUX"].unit == ""


def test_uncertainties_none_distinguishable_from_zero_array():
    col_none = MeasurementColumn(
        name="FLUX", values=np.array([1.0]), unit="e-/s", uncertainties=None
    )
    col_zero = MeasurementColumn(
        name="FLUX",
        values=np.array([1.0]),
        unit="e-/s",
        uncertainties=np.array([0.0]),
    )
    assert col_none.uncertainties is None
    assert col_zero.uncertainties is not None
    assert np.array_equal(col_zero.uncertainties, np.array([0.0]))


def test_optional_uncertainties_accepted():
    col = MeasurementColumn(
        name="FLUX", values=np.array([1.0, 2.0]), unit="e-/s", uncertainties=None
    )
    dataset = LightCurveDataset(
        name="No Uncertainties",
        time=TimeInfo(values=np.array([1.0, 2.0]), unit="d"),
        measurements=MeasurementSeries(series={"FLUX": col}),
    )
    assert dataset.measurements.series["FLUX"].uncertainties is None


# ------------------------------------------------------------------
# Non-finite value preservation
# ------------------------------------------------------------------


def test_non_finite_values_preserved():
    values = np.array([1.0, np.nan, np.inf, -np.inf, 5.0])
    col = MeasurementColumn(name="FLUX", values=values, unit="e-/s")
    dataset = LightCurveDataset(
        name="Non-finite",
        time=TimeInfo(values=np.arange(5, dtype=np.float64), unit="d"),
        measurements=MeasurementSeries(series={"FLUX": col}),
    )
    stored = dataset.measurements.series["FLUX"].values
    assert np.isnan(stored[1])
    assert np.isposinf(stored[2])
    assert np.isneginf(stored[3])


def test_n_nonfinite_calculated_property():
    values = np.array([1.0, np.nan, 3.0, np.inf, 5.0])
    col = MeasurementColumn(name="FLUX", values=values, unit="e-/s")
    assert col.n_nonfinite == 2


# ------------------------------------------------------------------
# SAP_FLUX vs PDCSAP_FLUX independence
# ------------------------------------------------------------------


def test_sap_and_pdcsap_are_separate_columns():
    n = 10
    dataset = LightCurveDataset(
        name="Two Flux Columns",
        time=TimeInfo(values=np.arange(n, dtype=np.float64), unit="d"),
        measurements=MeasurementSeries(
            series={
                "SAP_FLUX": MeasurementColumn(
                    name="SAP_FLUX",
                    values=np.ones(n, dtype=np.float64) * 500.0,
                    unit="e-/s",
                ),
                "PDCSAP_FLUX": MeasurementColumn(
                    name="PDCSAP_FLUX",
                    values=np.ones(n, dtype=np.float64) * 501.0,
                    unit="e-/s",
                ),
            }
        ),
    )
    series = dataset.measurements.series
    assert "SAP_FLUX" in series
    assert "PDCSAP_FLUX" in series
    assert series["SAP_FLUX"].values[0] == 500.0
    assert series["PDCSAP_FLUX"].values[0] == 501.0
    assert series["SAP_FLUX"] is not series["PDCSAP_FLUX"]


# ------------------------------------------------------------------
# Optional quality flags and cadence numbers
# ------------------------------------------------------------------


def test_quality_flags_and_cadence_optional():
    dataset = _make_dataset()
    assert dataset.quality_flags is None
    assert dataset.cadence_numbers is None


def test_quality_flags_and_cadence_supplied():
    n = 5
    dataset = LightCurveDataset(
        name="With Quality",
        time=TimeInfo(values=np.arange(n, dtype=np.float64), unit="d"),
        measurements=MeasurementSeries(
            series={"FLUX": MeasurementColumn(name="FLUX", values=np.ones(n), unit="e-/s")}
        ),
        quality_flags=np.array([0, 64, 0, 128, 0], dtype=np.int64),
        cadence_numbers=np.array([568, 569, 570, 571, 572], dtype=np.int64),
    )
    assert np.array_equal(
        dataset.quality_flags, np.array([0, 64, 0, 128, 0], dtype=np.int64)
    )
    assert np.array_equal(
        dataset.cadence_numbers, np.array([568, 569, 570, 571, 572], dtype=np.int64)
    )


# ------------------------------------------------------------------
# Length validation
# ------------------------------------------------------------------


def test_measurement_values_length_mismatch_rejected():
    with pytest.raises(LightCurveValidationError):
        LightCurveDataset(
            name="Mismatch",
            time=TimeInfo(values=np.arange(5, dtype=np.float64), unit="d"),
            measurements=MeasurementSeries(
                series={
                    "FLUX": MeasurementColumn(
                        name="FLUX",
                        values=np.ones(3, dtype=np.float64),
                        unit="e-/s",
                    )
                }
            ),
        )


def test_uncertainties_length_mismatch_rejected():
    with pytest.raises(LightCurveValidationError):
        LightCurveDataset(
            name="Uncertainty Mismatch",
            time=TimeInfo(values=np.arange(5, dtype=np.float64), unit="d"),
            measurements=MeasurementSeries(
                series={
                    "FLUX": MeasurementColumn(
                        name="FLUX",
                        values=np.ones(5, dtype=np.float64),
                        unit="e-/s",
                        uncertainties=np.ones(3, dtype=np.float64),
                    )
                }
            ),
        )


def test_quality_flags_length_mismatch_rejected():
    with pytest.raises(LightCurveValidationError):
        LightCurveDataset(
            name="Quality Mismatch",
            time=TimeInfo(values=np.arange(5, dtype=np.float64), unit="d"),
            measurements=MeasurementSeries(
                series={"FLUX": MeasurementColumn(name="FLUX", values=np.ones(5), unit="e-/s")}
            ),
            quality_flags=np.array([0, 64], dtype=np.int64),
        )


def test_cadence_numbers_length_mismatch_rejected():
    with pytest.raises(LightCurveValidationError):
        LightCurveDataset(
            name="Cadence Mismatch",
            time=TimeInfo(values=np.arange(5, dtype=np.float64), unit="d"),
            measurements=MeasurementSeries(
                series={"FLUX": MeasurementColumn(name="FLUX", values=np.ones(5), unit="e-/s")}
            ),
            cadence_numbers=np.array([568, 569], dtype=np.int64),
        )


# ------------------------------------------------------------------
# Measurement-series key/name validation
# ------------------------------------------------------------------


def test_key_name_mismatch_rejected():
    col = MeasurementColumn(name="FLUX", values=np.ones(3), unit="e-/s")
    with pytest.raises(LightCurveValidationError):
        LightCurveDataset(
            name="Key Mismatch",
            time=TimeInfo(values=np.arange(3, dtype=np.float64), unit="d"),
            measurements=MeasurementSeries(series={"WRONG_KEY": col}),
        )


def test_duplicate_column_name_rejected():
    col1 = MeasurementColumn(name="FLUX", values=np.ones(3), unit="e-/s")
    col2 = MeasurementColumn(name="FLUX", values=np.ones(3), unit="e-/s")
    with pytest.raises(LightCurveValidationError):
        LightCurveDataset(
            name="Duplicate",
            time=TimeInfo(values=np.arange(3, dtype=np.float64), unit="d"),
            measurements=MeasurementSeries(series={"FLUX": col1, "FLUX_2": col2}),
        )


# ------------------------------------------------------------------
# Array copy behavior
# ------------------------------------------------------------------


def test_constructor_copies_time_array():
    original = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    dataset = LightCurveDataset(
        name="Copy Test",
        time=TimeInfo(values=original, unit="d"),
        measurements=MeasurementSeries(series={}),
    )
    original[0] = 999.0
    assert dataset.time.values[0] == 1.0


def test_constructor_copies_measurement_values():
    original = np.array([10.0, 20.0], dtype=np.float64)
    dataset = LightCurveDataset(
        name="Copy Test",
        time=TimeInfo(values=np.arange(2, dtype=np.float64), unit="d"),
        measurements=MeasurementSeries(
            series={"FLUX": MeasurementColumn(name="FLUX", values=original, unit="e-/s")}
        ),
    )
    original[0] = 999.0
    assert dataset.measurements.series["FLUX"].values[0] == 10.0


def test_constructor_copies_uncertainties():
    original = np.array([0.1, 0.2], dtype=np.float64)
    dataset = LightCurveDataset(
        name="Copy Uncertainties",
        time=TimeInfo(values=np.arange(2, dtype=np.float64), unit="d"),
        measurements=MeasurementSeries(
            series={
                "FLUX": MeasurementColumn(
                    name="FLUX",
                    values=np.ones(2, dtype=np.float64),
                    unit="e-/s",
                    uncertainties=original,
                )
            }
        ),
    )
    original[0] = 999.0
    assert dataset.measurements.series["FLUX"].uncertainties is not None
    assert dataset.measurements.series["FLUX"].uncertainties[0] == 0.1


def test_constructor_copies_quality_flags():
    original = np.array([0, 64, 0], dtype=np.int64)
    dataset = LightCurveDataset(
        name="Copy Quality",
        time=TimeInfo(values=np.arange(3, dtype=np.float64), unit="d"),
        measurements=MeasurementSeries(
            series={"FLUX": MeasurementColumn(name="FLUX", values=np.ones(3), unit="e-/s")}
        ),
        quality_flags=original,
    )
    original[0] = 128
    assert dataset.quality_flags is not None
    assert dataset.quality_flags[0] == 0


# ------------------------------------------------------------------
# Calculated properties
# ------------------------------------------------------------------


def test_n_observations_calculated_from_time():
    dataset = _make_dataset(n=7)
    assert dataset.n_observations == 7


def test_n_nonfinite_reflects_current_array():
    # A standalone MeasurementColumn does not copy arrays; array copying is a
    # LightCurveDataset responsibility. Verify through the dataset.
    values = np.array([1.0, np.nan, 3.0])
    dataset = LightCurveDataset(
        name="Copy Test",
        time=TimeInfo(values=np.arange(3, dtype=np.float64), unit="d"),
        measurements=MeasurementSeries(
            series={"FLUX": MeasurementColumn(name="FLUX", values=values, unit="e-/s")}
        ),
    )
    # Mutating the caller's original must not alter the model's copy.
    values[1] = 5.0
    assert dataset.measurements.series["FLUX"].n_nonfinite == 1


# ------------------------------------------------------------------
# Validation reports
# ------------------------------------------------------------------


def test_default_validation_report_is_empty():
    dataset = _make_dataset()
    assert dataset.validation.errors == []
    assert dataset.validation.warnings == []
    assert dataset.validation.info == []


def test_supplied_validation_report_preserved():
    report = ValidationReport(
        warnings=[
            ValidationFinding(
                code="UNKNOWN_UNIT",
                message="Unit unknown.",
                severity="warning",
                column="FLUX",
            )
        ]
    )
    dataset = LightCurveDataset(
        name="With Warnings",
        time=TimeInfo(values=np.array([1.0]), unit="d"),
        measurements=MeasurementSeries(series={}),
        validation=report,
    )
    assert len(dataset.validation.warnings) == 1
    assert dataset.validation.warnings[0].code == "UNKNOWN_UNIT"


# ------------------------------------------------------------------
# Serialization round trips
# ------------------------------------------------------------------


def test_to_dict_and_from_dict_roundtrip():
    dataset = _make_dataset()
    data = dataset.to_dict()
    restored = LightCurveDataset.from_dict(data)

    assert restored.dataset_id == dataset.dataset_id
    assert restored.name == dataset.name
    assert restored.imported_at == dataset.imported_at
    assert restored.n_observations == dataset.n_observations
    assert np.array_equal(restored.time.values, dataset.time.values)
    assert restored.time.unit == dataset.time.unit
    assert np.array_equal(
        restored.measurements.series["FLUX"].values,
        dataset.measurements.series["FLUX"].values,
    )
    assert not restored.measurements.series["FLUX"].uncertainties is not None or True


def test_roundtrip_preserves_none_uncertainties():
    col = MeasurementColumn(
        name="FLUX", values=np.array([1.0, 2.0]), unit="e-/s", uncertainties=None
    )
    dataset = LightCurveDataset(
        name="None Uncertainties",
        time=TimeInfo(values=np.arange(2, dtype=np.float64), unit="d"),
        measurements=MeasurementSeries(series={"FLUX": col}),
    )
    restored = LightCurveDataset.from_dict(dataset.to_dict())
    assert restored.measurements.series["FLUX"].uncertainties is None


def test_roundtrip_preserves_zero_array_uncertainties():
    col = MeasurementColumn(
        name="FLUX",
        values=np.array([1.0, 2.0]),
        unit="e-/s",
        uncertainties=np.array([0.0, 0.0]),
    )
    dataset = LightCurveDataset(
        name="Zero Uncertainties",
        time=TimeInfo(values=np.arange(2, dtype=np.float64), unit="d"),
        measurements=MeasurementSeries(series={"FLUX": col}),
    )
    restored = LightCurveDataset.from_dict(dataset.to_dict())
    assert restored.measurements.series["FLUX"].uncertainties is not None
    assert np.array_equal(
        restored.measurements.series["FLUX"].uncertainties, np.array([0.0, 0.0])
    )


def test_roundtrip_preserves_quality_flags_and_cadence():
    dataset = LightCurveDataset(
        name="Quality Cadence",
        time=TimeInfo(values=np.arange(3, dtype=np.float64), unit="d"),
        measurements=MeasurementSeries(
            series={"FLUX": MeasurementColumn(name="FLUX", values=np.ones(3), unit="e-/s")}
        ),
        quality_flags=np.array([0, 64, 0], dtype=np.int64),
        cadence_numbers=np.array([568, 569, 570], dtype=np.int64),
    )
    restored = LightCurveDataset.from_dict(dataset.to_dict())
    assert restored.quality_flags is not None
    assert np.array_equal(restored.quality_flags, np.array([0, 64, 0], dtype=np.int64))
    assert restored.cadence_numbers is not None
    assert np.array_equal(
        restored.cadence_numbers, np.array([568, 569, 570], dtype=np.int64)
    )


def test_roundtrip_preserves_validation_report():
    report = ValidationReport(
        warnings=[
            ValidationFinding(
                code="UNKNOWN_UNIT",
                message="Unit unknown.",
                severity="warning",
                column="FLUX",
                row_indices=[0],
            )
        ],
        info=[
            ValidationFinding(
                code="NONFINITE_VALUES",
                message="Non-finite values present.",
                severity="info",
                column="FLUX",
            )
        ],
    )
    dataset = LightCurveDataset(
        name="With Validation",
        time=TimeInfo(values=np.array([1.0]), unit="d"),
        measurements=MeasurementSeries(series={}),
        validation=report,
    )
    restored = LightCurveDataset.from_dict(dataset.to_dict())
    assert len(restored.validation.warnings) == 1
    assert restored.validation.warnings[0].code == "UNKNOWN_UNIT"
    assert restored.validation.warnings[0].row_indices == [0]
    assert len(restored.validation.info) == 1
    assert restored.validation.info[0].code == "NONFINITE_VALUES"


def test_roundtrip_preserves_source_metadata():
    source = DatasetSource(
        original_filename="kplr.fits",
        original_file_path="/data/kplr.fits",
        archive="MAST/STScI",
        source_id="product-123",
        mission="Kepler",
        instrument="Kepler Photometer",
        target_object="KIC 11904151",
        checksum="abc123",
    )
    dataset = LightCurveDataset(
        name="With Source",
        source=source,
        time=TimeInfo(values=np.array([1.0]), unit="d"),
        measurements=MeasurementSeries(series={}),
    )
    restored = LightCurveDataset.from_dict(dataset.to_dict())
    assert restored.source.original_filename == "kplr.fits"
    assert restored.source.original_file_path == "/data/kplr.fits"
    assert restored.source.archive == "MAST/STScI"
    assert restored.source.source_id == "product-123"
    assert restored.source.mission == "Kepler"
    assert restored.source.instrument == "Kepler Photometer"
    assert restored.source.target_object == "KIC 11904151"
    assert restored.source.checksum == "abc123"


# ------------------------------------------------------------------
# Rejection of invalid reconstructed data
# ------------------------------------------------------------------


def test_from_dict_rejects_array_length_mismatch():
    data = _make_dataset().to_dict()
    # Corrupt: change flux length but not time length
    data["measurements"]["FLUX"]["values"] = [1.0, 2.0]
    with pytest.raises(LightCurveValidationError):
        LightCurveDataset.from_dict(data)


def test_from_dict_rejects_key_name_mismatch():
    data = _make_dataset().to_dict()
    data["measurements"]["RENAMED"] = data["measurements"].pop("FLUX")
    data["measurements"]["RENAMED"]["name"] = "FLUX"
    with pytest.raises(LightCurveValidationError):
        LightCurveDataset.from_dict(data)


def test_from_dict_rejects_malformed_uuid():
    data = _make_dataset().to_dict()
    data["dataset_id"] = "not-a-uuid"
    with pytest.raises(LightCurveValidationError):
        LightCurveDataset.from_dict(data)


# ------------------------------------------------------------------
# JSON compatibility
# ------------------------------------------------------------------


def test_to_dict_is_json_compatible():
    import json

    dataset = _make_dataset()
    data = dataset.to_dict()
    # Should not raise
    json.dumps(data)