"""Tests for the project metadata model (Subtask 2.1.1).

Covers project creation, metadata validation, project ID generation,
schema versioning, serialization round-trips, and dirty-state tracking.
"""

from __future__ import annotations

import uuid

import pytest

from src.project_model import (
    ProjectMetadata,
    ProjectValidationError,
    SCHEMA_VERSION,
    VALID_STATUSES,
)


def test_create_project_metadata_with_valid_name():
    metadata = ProjectMetadata.create("My Research Project")
    assert metadata.name == "My Research Project"
    assert metadata.status == "Active"
    assert metadata.schema_version == SCHEMA_VERSION
    assert metadata.project_id
    uuid.UUID(metadata.project_id)  # raises if not a valid UUID
    assert metadata.created_at
    assert not metadata.is_dirty


def test_create_project_metadata_generates_unique_ids():
    m1 = ProjectMetadata.create("Project A")
    m2 = ProjectMetadata.create("Project B")
    assert m1.project_id != m2.project_id


def test_empty_name_rejected():
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.create("")
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.create("   ")


def test_invalid_name_characters_rejected():
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.create("bad/name")


def test_name_too_long_rejected():
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.create("x" * 101)


def test_validate_accepts_valid_metadata():
    metadata = ProjectMetadata.create("Valid Project")
    ProjectMetadata.validate(metadata)  # should not raise


def test_validate_rejects_invalid_status():
    metadata = ProjectMetadata.create("Test")
    metadata.status = "InvalidStatus"
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.validate(metadata)


def test_validate_rejects_invalid_uuid():
    metadata = ProjectMetadata.create("Test")
    metadata.project_id = "not-a-uuid"
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.validate(metadata)


def test_dirty_state_tracking():
    metadata = ProjectMetadata.create("Dirty Test")
    assert not metadata.is_dirty
    metadata.mark_dirty()
    assert metadata.is_dirty
    metadata.mark_clean()
    assert not metadata.is_dirty


def test_to_dict_and_from_dict_roundtrip():
    metadata = ProjectMetadata.create("Roundtrip")
    data = metadata.to_dict()
    restored = ProjectMetadata.from_dict(data)
    assert restored.project_id == metadata.project_id
    assert restored.name == metadata.name
    assert restored.status == metadata.status
    assert restored.schema_version == metadata.schema_version
    assert not restored.is_dirty


def test_schema_version_default():
    metadata = ProjectMetadata.create("Schema Test")
    assert metadata.schema_version == SCHEMA_VERSION


def test_valid_statuses_accepted():
    for status in VALID_STATUSES:
        metadata = ProjectMetadata.create("Status Test")
        metadata.status = status
        ProjectMetadata.validate(metadata)  # should not raise
