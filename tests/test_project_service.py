"""Tests for the project lifecycle service (Subtask 2.1.3).

Covers project creation, metadata validation, default and custom locations,
duplicate identification handling, failure cleanup, active-project tracking,
and existing-project preservation.

Uses temporary directories only. Does not touch the real Kepler-10b dataset.
"""

from __future__ import annotations

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
    assert metadata.schema_version == 1
    assert metadata.external_data_references == []
    assert metadata.project_id
    uuid.UUID(metadata.project_id)


def test_project_metadata_initial_values(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)

    metadata = service.create_project("Initial Values")

    assert metadata.name == "Initial Values"
    assert metadata.status == "Active"
    assert metadata.schema_version == 1
    assert metadata.external_data_references == []
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
