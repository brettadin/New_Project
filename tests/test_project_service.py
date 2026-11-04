"""Tests for the project lifecycle service (Subtask 2.1.3).

Covers project creation, metadata validation, default and custom locations,
duplicate identification handling, failure cleanup, active-project tracking,
and existing-project preservation.

Uses temporary directories only. Does not touch the real Kepler-10b dataset.
"""

from __future__ import annotations

import json
import uuid
from unittest.mock import patch

import pytest

from src.config_provider import ConfigProvider
from src.project_model import ProjectMetadata, ProjectValidationError
from src.project_repository import ProjectRepository
from src.project_service import ProjectCreationError, ProjectService


# ------------------------------------------------------------------
# Successful creation
# ------------------------------------------------------------------

def test_successful_project_creation(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)

    metadata = service.create_project("My Research Project")

    assert metadata.name == "My Research Project"
    assert metadata.status == "Active"
    assert metadata.schema_version == 2
    assert metadata.external_data_references == []
    assert metadata.owner == "local_user"
    assert set(metadata.roles.keys()) == {"view", "contribute", "manage"}
    for role in ("view", "contribute", "manage"):
        assert metadata.roles[role] == ["local_user"]
    assert metadata.project_id
    uuid.UUID(metadata.project_id)
    assert not metadata.is_dirty


def test_project_metadata_initial_values(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)

    metadata = service.create_project("Initial Values")

    assert metadata.name == "Initial Values"
    assert metadata.status == "Active"
    assert metadata.schema_version == 2
    assert metadata.external_data_references == []
    assert metadata.owner == "local_user"
    assert set(metadata.roles.keys()) == {"view", "contribute", "manage"}
    for role in ("view", "contribute", "manage"):
        assert metadata.roles[role] == ["local_user"]
    assert metadata.created_at
    assert not metadata.is_dirty


# ------------------------------------------------------------------
# Default and custom locations
# ------------------------------------------------------------------

def test_project_saved_under_default_root(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)

    metadata = service.create_project("Default Location")

    project_file = tmp_path / metadata.project_id / "project.json"
    assert project_file.exists()
    assert repo.project_exists(metadata.project_id)


def test_custom_project_location(tmp_path):
    custom_root = tmp_path / "custom_projects"
    custom_root.mkdir()

    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)

    metadata = service.create_project("Custom Location", location=str(custom_root))

    project_file = custom_root / metadata.project_id / "project.json"
    assert project_file.exists()
    # Verify via direct load from the custom location
    custom_repo = ProjectRepository(str(custom_root))
    loaded = custom_repo.load(metadata.project_id)
    assert loaded.name == "Custom Location"
    assert loaded.project_id == metadata.project_id


# ------------------------------------------------------------------
# Invalid names
# ------------------------------------------------------------------

def test_invalid_names_rejected(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)

    with pytest.raises(ProjectValidationError):
        service.create_project("")
    with pytest.raises(ProjectValidationError):
        service.create_project("   ")
    with pytest.raises(ProjectValidationError):
        service.create_project("bad/name")
    with pytest.raises(ProjectValidationError):
        service.create_project("x" * 101)


# ------------------------------------------------------------------
# Duplicate project identifier handling
# ------------------------------------------------------------------

def test_duplicate_project_identifier_handled_safely(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)

    # Create first project
    metadata1 = service.create_project("First Project")
    assert service.active_project is metadata1

    # Patch ProjectMetadata.create to return a duplicate with the same project_id
    duplicate_metadata = ProjectMetadata.create("Duplicate")
    duplicate_metadata.project_id = metadata1.project_id

    with patch(
        "src.project_model.ProjectMetadata.create",
        return_value=duplicate_metadata,
    ):
        with pytest.raises(ProjectCreationError):
            service.create_project("Duplicate Name")

    # First project must be untouched - no overwrite, no deletion
    loaded = repo.load(metadata1.project_id)
    assert loaded.name == "First Project"
    assert loaded.status == "Active"


# ------------------------------------------------------------------
# Failure cleanup
# ------------------------------------------------------------------

def test_creation_failure_cleans_up_incomplete_directory(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)

    # Patch save at the class level so the service's internal repository
    # instance is affected. The mock creates the directory but fails to write.
    def failing_save(self, metadata):
        self.project_dir(metadata.project_id).mkdir(parents=True, exist_ok=True)
        raise OSError("Simulated disk full")

    with patch(
        "src.project_repository.ProjectRepository.save", side_effect=failing_save
    ):
        with pytest.raises(ProjectCreationError):
            service.create_project("Failed Project")

    # No incomplete directory should remain
    project_dirs = [d for d in tmp_path.iterdir() if d.is_dir()]
    assert project_dirs == []


def test_existing_project_untouched_after_failed_creation(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)

    # Create an existing project
    existing = service.create_project("Existing Project")

    # Now try to create a project that will fail at save time
    def failing_save(self, metadata):
        raise OSError("Simulated failure")

    with patch(
        "src.project_repository.ProjectRepository.save", side_effect=failing_save
    ):
        with pytest.raises(ProjectCreationError):
            service.create_project("Failed Project")

    # Existing project must be completely untouched
    repo = ProjectRepository(str(tmp_path))
    loaded = repo.load(existing.project_id)
    assert loaded.name == "Existing Project"
    assert loaded.status == "Active"


# ------------------------------------------------------------------
# Active project tracking
# ------------------------------------------------------------------

def test_successful_creation_sets_active_project(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)

    assert service.active_project is None

    metadata = service.create_project("New Project")

    assert service.active_project is metadata
    assert service.active_project.name == "New Project"


# ------------------------------------------------------------------
# Default location resolution
# ------------------------------------------------------------------

def test_default_location_from_config_provider(tmp_path):
    custom_root = str(tmp_path / "default_projects")
    provider = ConfigProvider()
    provider.set_projects_root(custom_root)
    repo = ProjectRepository(custom_root)
    service = ProjectService(provider, repo)

    assert service.default_location == custom_root

    metadata = service.create_project("Default Root Test")
    loaded = repo.load(metadata.project_id)
    assert loaded.name == "Default Root Test"


# ------------------------------------------------------------------
# Schema version 2: owner and roles persistence
# ------------------------------------------------------------------


def test_save_and_reload_preserves_owner_and_roles(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)

    metadata = service.create_project("Owner Roles Test")

    # Direct fixture assignment of valid non-default values.
    metadata.owner = "researcher_a"
    metadata.roles = {
        "view": ["researcher_a", "researcher_b"],
        "contribute": ["researcher_a"],
        "manage": ["researcher_a"],
    }

    service.save_project()

    reloaded = repo.load(metadata.project_id)
    assert reloaded.owner == "researcher_a"
    assert reloaded.roles["view"] == ["researcher_a", "researcher_b"]
    assert reloaded.roles["contribute"] == ["researcher_a"]
    assert reloaded.roles["manage"] == ["researcher_a"]
    assert reloaded.schema_version == 2
    assert not reloaded.is_dirty


def test_legacy_v1_migration_save_and_reload_workflow(tmp_path):
    """Complete legacy migration: in-memory only until explicit save."""
    project_id = str(uuid.uuid4())
    project_dir = tmp_path / project_id
    project_dir.mkdir()

    v1_metadata = {
        "project_id": project_id,
        "name": "Legacy Project",
        "created_at": "2026-01-01T00:00:00+00:00",
        "status": "Active",
        "schema_version": 1,
        "external_data_references": [],
    }
    project_file = project_dir / "project.json"
    project_file.write_text(json.dumps(v1_metadata, indent=2), encoding="utf-8")

    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)

    # Step 1 — Load through the existing service/repository path.
    loaded = service.open_project(project_id, location=str(tmp_path))

    # Step 2 — Verify in-memory migration.
    assert loaded.schema_version == 2
    assert loaded.owner == "local_user"
    assert loaded.roles["view"] == ["local_user"]
    assert loaded.roles["contribute"] == ["local_user"]
    assert loaded.roles["manage"] == ["local_user"]
    assert not loaded.is_dirty

    # Step 3 — Verify no automatic disk migration before saving.
    disk_data = json.loads(project_file.read_text(encoding="utf-8"))
    assert disk_data["schema_version"] == 1
    assert "owner" not in disk_data
    assert "roles" not in disk_data

    # Step 4 — Explicit save through the service.
    service.save_project()

    # Step 5 — Inspect persisted JSON.
    persisted = json.loads(project_file.read_text(encoding="utf-8"))
    assert persisted["schema_version"] == 2
    assert persisted["owner"] == "local_user"
    assert persisted["roles"]["view"] == ["local_user"]
    assert persisted["roles"]["contribute"] == ["local_user"]
    assert persisted["roles"]["manage"] == ["local_user"]

    # Step 6 — Reload and verify migrated metadata is preserved and clean.
    reloaded = service.open_project(project_id, location=str(tmp_path))
    assert reloaded.schema_version == 2
    assert reloaded.owner == "local_user"
    assert reloaded.roles["view"] == ["local_user"]
    assert reloaded.roles["contribute"] == ["local_user"]
    assert reloaded.roles["manage"] == ["local_user"]
    assert not reloaded.is_dirty
