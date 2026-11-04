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


# ------------------------------------------------------------------
# Schema version 2: owner and roles defaults
# ------------------------------------------------------------------


def test_new_metadata_owner_defaults_to_local_user():
    metadata = ProjectMetadata.create("Default Owner Test")
    assert metadata.owner == "local_user"


def test_new_metadata_has_all_required_roles():
    metadata = ProjectMetadata.create("Roles Test")
    assert set(metadata.roles.keys()) == {"view", "contribute", "manage"}


def test_each_default_role_contains_local_user():
    metadata = ProjectMetadata.create("Roles Contain Local User Test")
    for role in ("view", "contribute", "manage"):
        assert "local_user" in metadata.roles[role]


def test_new_metadata_has_schema_version_2():
    metadata = ProjectMetadata.create("Schema V2 Test")
    assert metadata.schema_version == 2
    assert metadata.schema_version == SCHEMA_VERSION


def test_new_metadata_is_clean():
    metadata = ProjectMetadata.create("Clean Test")
    assert not metadata.is_dirty


def test_independent_projects_do_not_share_roles_data():
    m1 = ProjectMetadata.create("Independent A")
    m2 = ProjectMetadata.create("Independent B")
    assert m1.roles is not m2.roles
    assert m1.roles["view"] is not m2.roles["view"]
    m1.roles["view"].append("extra_principal")
    assert "extra_principal" not in m2.roles["view"]


# ------------------------------------------------------------------
# Owner validation
# ------------------------------------------------------------------


def _metadata_with_owner(owner):
    metadata = ProjectMetadata.create("Owner Validation Test")
    metadata.owner = owner
    return metadata


def test_owner_rejects_empty_string():
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.validate(_metadata_with_owner(""))


def test_owner_rejects_whitespace_only_string():
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.validate(_metadata_with_owner("   "))
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.validate(_metadata_with_owner("\t\n"))


def test_owner_rejects_none():
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.validate(_metadata_with_owner(None))


def test_owner_rejects_integer():
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.validate(_metadata_with_owner(42))


def test_owner_rejects_list():
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.validate(_metadata_with_owner(["local_user"]))


def test_owner_rejects_dictionary():
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.validate(_metadata_with_owner({"name": "local_user"}))


def test_owner_accepts_valid_string():
    metadata = _metadata_with_owner("researcher_a")
    ProjectMetadata.validate(metadata)  # should not raise


# ------------------------------------------------------------------
# Roles validation
# ------------------------------------------------------------------


def _metadata_with_roles(roles):
    metadata = ProjectMetadata.create("Roles Validation Test")
    metadata.roles = roles
    return metadata


def test_roles_rejects_none():
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.validate(_metadata_with_roles(None))


def test_roles_rejects_list():
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.validate(_metadata_with_roles([]))


def test_roles_rejects_string_value():
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.validate(_metadata_with_roles({"view": "local_user"}))


def test_roles_rejects_missing_view():
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.validate(
            _metadata_with_roles({"contribute": ["local_user"], "manage": ["local_user"]})
        )


def test_roles_rejects_missing_contribute():
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.validate(
            _metadata_with_roles({"view": ["local_user"], "manage": ["local_user"]})
        )


def test_roles_rejects_missing_manage():
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.validate(
            _metadata_with_roles({"view": ["local_user"], "contribute": ["local_user"]})
        )


def test_roles_rejects_non_string_role_name():
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.validate(
            _metadata_with_roles({1: ["local_user"], "contribute": ["local_user"], "manage": ["local_user"]})
        )


def test_roles_rejects_non_list_role_value():
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.validate(
            _metadata_with_roles({"view": "local_user", "contribute": ["local_user"], "manage": ["local_user"]})
        )


def test_roles_rejects_non_string_principal():
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.validate(
            _metadata_with_roles({"view": [None], "contribute": ["local_user"], "manage": ["local_user"]})
        )


def test_roles_rejects_empty_principal():
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.validate(
            _metadata_with_roles({"view": [""], "contribute": ["local_user"], "manage": ["local_user"]})
        )


def test_roles_rejects_whitespace_only_principal():
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.validate(
            _metadata_with_roles({"view": ["   "], "contribute": ["local_user"], "manage": ["local_user"]})
        )


def test_roles_accepts_additional_valid_role_names():
    metadata = _metadata_with_roles(
        {
            "view": ["local_user"],
            "contribute": ["local_user"],
            "manage": ["local_user"],
            "review": ["researcher_a"],
        }
    )
    ProjectMetadata.validate(metadata)  # should not raise


# ------------------------------------------------------------------
# Serialization round trips
# ------------------------------------------------------------------


def test_to_dict_and_from_dict_preserve_owner_and_roles():
    metadata = ProjectMetadata.create("Roundtrip Owner Roles")
    metadata.owner = "researcher_a"
    metadata.roles = {
        "view": ["researcher_a", "researcher_b"],
        "contribute": ["researcher_a"],
        "manage": ["researcher_a"],
    }
    data = metadata.to_dict()
    restored = ProjectMetadata.from_dict(data)
    assert restored.owner == metadata.owner
    assert restored.roles == metadata.roles
    assert restored.project_id == metadata.project_id
    assert restored.name == metadata.name
    assert restored.created_at == metadata.created_at
    assert restored.status == metadata.status
    assert restored.schema_version == metadata.schema_version
    assert restored.external_data_references == metadata.external_data_references
    assert not restored.is_dirty


def test_roundtrip_roles_are_independent_copies():
    metadata = ProjectMetadata.create("Independent Roundtrip")
    data = metadata.to_dict()
    restored1 = ProjectMetadata.from_dict(data)
    restored2 = ProjectMetadata.from_dict(data)
    assert restored1.roles is not restored2.roles
    assert restored1.roles["view"] is not restored2.roles["view"]
    restored1.roles["view"].append("extra")
    assert "extra" not in restored2.roles["view"]


# ------------------------------------------------------------------
# Version 1 migration
# ------------------------------------------------------------------


def _v1_metadata_dict(project_id, name="Legacy Project"):
    return {
        "project_id": project_id,
        "name": name,
        "created_at": "2026-01-01T00:00:00+00:00",
        "status": "Active",
        "schema_version": 1,
        "external_data_references": [],
    }


def test_v1_migration_applies_default_owner_and_roles():
    metadata = ProjectMetadata.from_dict(_v1_metadata_dict(str(uuid.uuid4())))
    assert metadata.owner == "local_user"
    assert metadata.roles["view"] == ["local_user"]
    assert metadata.roles["contribute"] == ["local_user"]
    assert metadata.roles["manage"] == ["local_user"]


def test_v1_migration_upgrades_schema_version_to_2():
    metadata = ProjectMetadata.from_dict(_v1_metadata_dict(str(uuid.uuid4())))
    assert metadata.schema_version == 2


def test_v1_migration_preserves_existing_fields():
    project_id = str(uuid.uuid4())
    metadata = ProjectMetadata.from_dict(_v1_metadata_dict(project_id))
    assert metadata.project_id == project_id
    assert metadata.name == "Legacy Project"
    assert metadata.created_at == "2026-01-01T00:00:00+00:00"
    assert metadata.status == "Active"
    assert metadata.external_data_references == []


def test_v1_migration_is_clean():
    metadata = ProjectMetadata.from_dict(_v1_metadata_dict(str(uuid.uuid4())))
    assert not metadata.is_dirty


def test_v1_migration_preserves_valid_owner_and_roles_when_present():
    project_id = str(uuid.uuid4())
    data = _v1_metadata_dict(project_id)
    data["owner"] = "legacy_owner"
    data["roles"] = {"view": ["legacy_owner"], "contribute": ["legacy_owner"], "manage": ["legacy_owner"]}
    metadata = ProjectMetadata.from_dict(data)
    assert metadata.owner == "legacy_owner"
    assert metadata.roles["view"] == ["legacy_owner"]
    assert metadata.schema_version == 2


# ------------------------------------------------------------------
# Version 2 missing required fields
# ------------------------------------------------------------------


def _v2_metadata_dict(project_id, owner="local_user", roles=None):
    if roles is None:
        roles = {"view": ["local_user"], "contribute": ["local_user"], "manage": ["local_user"]}
    return {
        "project_id": project_id,
        "name": "V2 Project",
        "created_at": "2026-01-01T00:00:00+00:00",
        "status": "Active",
        "schema_version": 2,
        "external_data_references": [],
        "owner": owner,
        "roles": roles,
    }


def test_v2_missing_owner_raises():
    data = _v2_metadata_dict(str(uuid.uuid4()), owner=None)
    del data["owner"]
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.from_dict(data)


def test_v2_missing_roles_raises():
    data = _v2_metadata_dict(str(uuid.uuid4()))
    del data["roles"]
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.from_dict(data)


# ------------------------------------------------------------------
# Future schema versions
# ------------------------------------------------------------------


def test_future_schema_version_rejected():
    data = _v2_metadata_dict(str(uuid.uuid4()))
    data["schema_version"] = 3
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.from_dict(data)


def test_future_schema_version_rejected_via_validate():
    metadata = ProjectMetadata.create("Future Test")
    metadata.schema_version = 99
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.validate(metadata)


def test_invalid_schema_version_types_rejected():
    for bad_version in ("2", 2.5, True, [2], {"v": 2}):
        data = _v2_metadata_dict(str(uuid.uuid4()))
        data["schema_version"] = bad_version
        with pytest.raises(ProjectValidationError):
            ProjectMetadata.from_dict(data)


def test_schema_version_zero_rejected():
    data = _v2_metadata_dict(str(uuid.uuid4()))
    data["schema_version"] = 0
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.from_dict(data)


def test_schema_version_negative_rejected():
    data = _v2_metadata_dict(str(uuid.uuid4()))
    data["schema_version"] = -1
    with pytest.raises(ProjectValidationError):
        ProjectMetadata.from_dict(data)
