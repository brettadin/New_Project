"""Light-curve data model for the astronomy research application.

Defines the internal scientific representation of an imported astronomical
light-curve dataset, independent of file format, persistence, and project
lifecycle concerns.

The model is intentionally free of FITS-reading, PySide6, persistence, and
project-association logic so it can be unit-tested independently.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

import numpy as np


class LightCurveValidationError(ValueError):
    """Raised when light-curve dataset construction fails structural validation."""


@dataclass
class DatasetSource:
    """Source-file identity and provenance metadata for a light-curve dataset.

    All fields are optional. The general model does not require a local source
    file path; the later FITS importer (Subtask 2.2.2) is responsible for
    supplying the path for the initial local-file workflow.
    """

    original_filename: str | None = None
    original_file_path: str | None = None
    archive: str | None = None
    source_id: str | None = None
    mission: str | None = None
    instrument: str | None = None
    target_object: str | None = None
    checksum: str | None = None


@dataclass
class TimeInfo:
    """Time representation for a light-curve dataset.

    Preserves numerical timestamp values together with their interpretation
    (unit, reference epoch, time scale, reference frame). Unknown units and
    missing metadata are representable as empty strings and do not prevent
    construction.
    """

    values: np.ndarray
    unit: str = ""
    reference: str = ""
    reference_value: float | None = None
    time_scale: str = ""
    time_reference_frame: str = ""
    start: float | None = None
    stop: float | None = None
    resolution: float | None = None
    format_hint: str | None = None


@dataclass
class MeasurementColumn:
    """A single measurement column and its associated uncertainty.

    Measurement values and uncertainties are preserved as-is. Non-finite
    values are not removed, replaced, or interpolated. An empty unit string
    represents an unknown unit; None uncertainties means uncertainties are
    absent or unknown (distinguishable from a measured zero uncertainty).
    """

    name: str
    values: np.ndarray
    unit: str = ""
    uncertainties: np.ndarray | None = None
    description: str | None = None

    @property
    def n_nonfinite(self) -> int:
        """Number of non-finite measurement values in this column."""
        return int(np.sum(~np.isfinite(self.values)))


@dataclass
class MeasurementSeries:
    """Named measurement columns, keyed by original column identity.

    Dictionary keys must match the corresponding MeasurementColumn.name.
    """

    series: dict[str, MeasurementColumn]


@dataclass
class ValidationFinding:
    """A single validation finding.

    row_indices, when supplied, are zero-based row positions.
    """

    code: str
    message: str
    severity: str
    column: str | None = None
    row_indices: list[int] | None = None


@dataclass
class ValidationReport:
    """Structured record of validation findings.

    errors: conditions preventing dataset acceptance.
    warnings: conditions permitting representation but flagged.
    info: conditions preserved without modification.
    """

    errors: list[ValidationFinding] = field(default_factory=list)
    warnings: list[ValidationFinding] = field(default_factory=list)
    info: list[ValidationFinding] = field(default_factory=list)


@dataclass
class LightCurveDataset:
    """Central dataset model for a single imported light-curve dataset.

    Represents one imported dataset independently of project metadata.
    Does not depend on or contain a ProjectMetadata object.
    """

    dataset_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    source: DatasetSource = field(default_factory=DatasetSource)
    time: TimeInfo = field(default_factory=TimeInfo)
    measurements: MeasurementSeries = field(
        default_factory=lambda: MeasurementSeries(series={})
    )
    quality_flags: np.ndarray | None = None
    cadence_numbers: np.ndarray | None = None
    validation: ValidationReport = field(default_factory=ValidationReport)
    imported_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    notes: str | None = None

    @property
    def n_observations(self) -> int:
        """Number of entries in the time array."""
        return len(self.time.values)

    def __post_init__(self) -> None:
        """Validate structural requirements, then copy arrays."""
        self._validate_structural()
        self._copy_arrays()

    def _validate_structural(self) -> None:
        """Raise LightCurveValidationError for structurally invalid data."""
        # Validate dataset_id is a valid UUID string.
        try:
            uuid.UUID(self.dataset_id)
        except (ValueError, TypeError, AttributeError) as exc:
            raise LightCurveValidationError(
                f"dataset_id must be a valid UUID string, got: {self.dataset_id!r}"
            ) from exc

        # Validate time values.
        if self.time.values is None:
            raise LightCurveValidationError("TimeInfo.values is required.")
        if not isinstance(self.time.values, np.ndarray):
            raise LightCurveValidationError("TimeInfo.values must be a NumPy array.")

        # Validate time unit is a string.
        if not isinstance(self.time.unit, str):
            raise LightCurveValidationError("TimeInfo.unit must be a string.")

        # Validate measurement series container.
        if not isinstance(self.measurements, MeasurementSeries):
            raise LightCurveValidationError(
                "measurements must be a MeasurementSeries instance."
            )
        if not isinstance(self.measurements.series, dict):
            raise LightCurveValidationError(
                "MeasurementSeries.series must be a dictionary."
            )

        # Validate key/name matching and uniqueness.
        seen_names: set[str] = set()
        for key, column in self.measurements.series.items():
            if not isinstance(key, str):
                raise LightCurveValidationError(
                    "MeasurementSeries keys must be strings."
                )
            if key != column.name:
                raise LightCurveValidationError(
                    f"MeasurementSeries key '{key}' does not match "
                    f"MeasurementColumn.name '{column.name}'."
                )
            if column.name in seen_names:
                raise LightCurveValidationError(
                    f"Duplicate measurement column name: '{column.name}'."
                )
            seen_names.add(column.name)

            # Validate column field types.
            if not isinstance(column.values, np.ndarray):
                raise LightCurveValidationError(
                    f"MeasurementColumn '{column.name}' values must be a NumPy array."
                )
            if not isinstance(column.unit, str):
                raise LightCurveValidationError(
                    f"MeasurementColumn '{column.name}' unit must be a string."
                )
            if column.uncertainties is not None and not isinstance(
                column.uncertainties, np.ndarray
            ):
                raise LightCurveValidationError(
                    f"MeasurementColumn '{column.name}' uncertainties must be "
                    f"a NumPy array or None."
                )

        # Validate array alignment with the time array.
        time_len = len(self.time.values)
        for key, column in self.measurements.series.items():
            if len(column.values) != time_len:
                raise LightCurveValidationError(
                    f"MeasurementColumn '{key}' values length "
                    f"({len(column.values)}) does not match time array "
                    f"length ({time_len})."
                )
            if (
                column.uncertainties is not None
                and len(column.uncertainties) != time_len
            ):
                raise LightCurveValidationError(
                    f"MeasurementColumn '{key}' uncertainties length "
                    f"({len(column.uncertainties)}) does not match time array "
                    f"length ({time_len})."
                )

        # Validate optional arrays alignment with the time array.
        if self.quality_flags is not None and len(self.quality_flags) != time_len:
            raise LightCurveValidationError(
                f"quality_flags length ({len(self.quality_flags)}) does not "
                f"match time array length ({time_len})."
            )
        if self.cadence_numbers is not None and len(self.cadence_numbers) != time_len:
            raise LightCurveValidationError(
                f"cadence_numbers length ({len(self.cadence_numbers)}) does not "
                f"match time array length ({time_len})."
            )

        # Validate validation report.
        if not isinstance(self.validation, ValidationReport):
            raise LightCurveValidationError(
                "validation must be a ValidationReport instance."
            )

        # Validate imported_at is a string.
        if not isinstance(self.imported_at, str):
            raise LightCurveValidationError("imported_at must be a string.")

    def _copy_arrays(self) -> None:
        """Copy incoming NumPy arrays so external mutation cannot alter the model."""
        self.time.values = np.array(self.time.values, dtype=np.float64, copy=True)

        new_series: dict[str, MeasurementColumn] = {}
        for key, column in self.measurements.series.items():
            values_copy = np.array(column.values, dtype=np.float64, copy=True)
            uncertainties_copy = (
                np.array(column.uncertainties, dtype=np.float64, copy=True)
                if column.uncertainties is not None
                else None
            )
            new_series[key] = MeasurementColumn(
                name=column.name,
                values=values_copy,
                unit=column.unit,
                uncertainties=uncertainties_copy,
                description=column.description,
            )
        self.measurements = MeasurementSeries(series=new_series)

        if self.quality_flags is not None:
            self.quality_flags = np.array(
                self.quality_flags, dtype=np.int64, copy=True
            )
        if self.cadence_numbers is not None:
            self.cadence_numbers = np.array(
                self.cadence_numbers, dtype=np.int64, copy=True
            )

    def to_dict(self) -> dict:
        """Serialize the dataset to a JSON-compatible dictionary.

        NumPy arrays are converted to ordinary Python lists. None values are
        preserved as None (JSON null). Zero-valued arrays are preserved as
        arrays of zeros (distinguishable from None).
        """
        return {
            "dataset_id": self.dataset_id,
            "name": self.name,
            "source": {
                "original_filename": self.source.original_filename,
                "original_file_path": self.source.original_file_path,
                "archive": self.source.archive,
                "source_id": self.source.source_id,
                "mission": self.source.mission,
                "instrument": self.source.instrument,
                "target_object": self.source.target_object,
                "checksum": self.source.checksum,
            },
            "time": {
                "values": self.time.values.tolist(),
                "unit": self.time.unit,
                "reference": self.time.reference,
                "reference_value": self.time.reference_value,
                "time_scale": self.time.time_scale,
                "time_reference_frame": self.time.time_reference_frame,
                "start": self.time.start,
                "stop": self.time.stop,
                "resolution": self.time.resolution,
                "format_hint": self.time.format_hint,
            },
            "measurements": {
                key: {
                    "name": col.name,
                    "values": col.values.tolist(),
                    "unit": col.unit,
                    "uncertainties": (
                        col.uncertainties.tolist()
                        if col.uncertainties is not None
                        else None
                    ),
                    "description": col.description,
                }
                for key, col in self.measurements.series.items()
            },
            "quality_flags": (
                self.quality_flags.tolist()
                if self.quality_flags is not None
                else None
            ),
            "cadence_numbers": (
                self.cadence_numbers.tolist()
                if self.cadence_numbers is not None
                else None
            ),
            "validation": {
                "errors": [
                    {
                        "code": f.code,
                        "message": f.message,
                        "severity": f.severity,
                        "column": f.column,
                        "row_indices": f.row_indices,
                    }
                    for f in self.validation.errors
                ],
                "warnings": [
                    {
                        "code": f.code,
                        "message": f.message,
                        "severity": f.severity,
                        "column": f.column,
                        "row_indices": f.row_indices,
                    }
                    for f in self.validation.warnings
                ],
                "info": [
                    {
                        "code": f.code,
                        "message": f.message,
                        "severity": f.severity,
                        "column": f.column,
                        "row_indices": f.row_indices,
                    }
                    for f in self.validation.info
                ],
            },
            "imported_at": self.imported_at,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "LightCurveDataset":
        """Reconstruct a LightCurveDataset from a serialized dictionary.

        Validates the reconstructed model using the same structural rules as
        normal construction. Distinguishes None from actual arrays.
        """
        source = DatasetSource(
            original_filename=data["source"].get("original_filename"),
            original_file_path=data["source"].get("original_file_path"),
            archive=data["source"].get("archive"),
            source_id=data["source"].get("source_id"),
            mission=data["source"].get("mission"),
            instrument=data["source"].get("instrument"),
            target_object=data["source"].get("target_object"),
            checksum=data["source"].get("checksum"),
        )

        time_data = data["time"]
        time_info = TimeInfo(
            values=np.array(time_data["values"], dtype=np.float64),
            unit=time_data.get("unit", ""),
            reference=time_data.get("reference", ""),
            reference_value=time_data.get("reference_value"),
            time_scale=time_data.get("time_scale", ""),
            time_reference_frame=time_data.get("time_reference_frame", ""),
            start=time_data.get("start"),
            stop=time_data.get("stop"),
            resolution=time_data.get("resolution"),
            format_hint=time_data.get("format_hint"),
        )

        series_dict: dict[str, MeasurementColumn] = {}
        for key, col_data in data["measurements"].items():
            uncertainties = None
            if col_data.get("uncertainties") is not None:
                uncertainties = np.array(col_data["uncertainties"], dtype=np.float64)
            series_dict[key] = MeasurementColumn(
                name=col_data["name"],
                values=np.array(col_data["values"], dtype=np.float64),
                unit=col_data.get("unit", ""),
                uncertainties=uncertainties,
                description=col_data.get("description"),
            )
        measurements = MeasurementSeries(series=series_dict)

        quality_flags = None
        if data.get("quality_flags") is not None:
            quality_flags = np.array(data["quality_flags"], dtype=np.int64)

        cadence_numbers = None
        if data.get("cadence_numbers") is not None:
            cadence_numbers = np.array(data["cadence_numbers"], dtype=np.int64)

        validation_errors = []
        for f in data.get("validation", {}).get("errors", []):
            validation_errors.append(
                ValidationFinding(
                    code=f["code"],
                    message=f["message"],
                    severity=f["severity"],
                    column=f.get("column"),
                    row_indices=f.get("row_indices"),
                )
            )
        validation_warnings = []
        for f in data.get("validation", {}).get("warnings", []):
            validation_warnings.append(
                ValidationFinding(
                    code=f["code"],
                    message=f["message"],
                    severity=f["severity"],
                    column=f.get("column"),
                    row_indices=f.get("row_indices"),
                )
            )
        validation_info = []
        for f in data.get("validation", {}).get("info", []):
            validation_info.append(
                ValidationFinding(
                    code=f["code"],
                    message=f["message"],
                    severity=f["severity"],
                    column=f.get("column"),
                    row_indices=f.get("row_indices"),
                )
            )
        validation = ValidationReport(
            errors=validation_errors,
            warnings=validation_warnings,
            info=validation_info,
        )

        kwargs = {
            "dataset_id": data["dataset_id"],
            "name": data.get("name", ""),
            "source": source,
            "time": time_info,
            "measurements": measurements,
            "quality_flags": quality_flags,
            "cadence_numbers": cadence_numbers,
            "validation": validation,
            "notes": data.get("notes"),
        }
        if data.get("imported_at") is not None:
            kwargs["imported_at"] = data["imported_at"]

        return cls(**kwargs)