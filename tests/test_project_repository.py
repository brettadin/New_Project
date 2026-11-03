"""Tests for the project persistence layer (Subtask 2.1.2).

Covers JSON save/load round-trips, field preservation (including
external_data_references), default and configurable projects root,
missing/malformed metadata handling, atomic write failure behavior,
and inaccessible storage handling.

Uses temporary directories only. Does not touch the real Kepler-10b dataset.
"""

from __future__ import annotations

import json
import os
from unittest.mock import patch

import pytest

from src.config_provider import ConfigProvider, DEFAULT_PROJECTS_ROOT
from src.project_model import ProjectMetadata
from src.project_repository import (
    ProjectCorruptedError,
    ProjectNotFoundError,
    ProjectRepository,
    ProjectRepositoryError,
)


# ------------------------------------------------------------------
# Save / load round-trip
# ------------------------------------------------------------------

def test_save_and_load_roundtrip_preserves_all_fields(tmp_path):
    repo = ProjectRepository(tmp_path)
    metadata = ProjectMetadata.create("Roundtrip Project")
    repo.save(metadata)

    loaded = repo.load(metadata.project_id)
    assert loaded.project_id == metadata.project_id
    assert loaded.name == metadata.name
    assert loaded.created_at == metadata.created_at
    assert loaded.status == metadata.status
    assert loaded.schema_version == metadata.schema_version
    assert loaded.external_data_references == metadata.external_data_references
    assert not loaded.is_dirty


def test_external_data_references_preserved(tmp_path):
    repo = ProjectRepository(tmp_path)
    metadata = ProjectMetadata.create("References Project")
    metadata.external_data_references = [
        {
            "path": "C:/AstronomyData/Kepler/Kepler-10b/kplr011904151-2009131105131_llc_full.fits",
            "source": "STScI",
            "available": True,
        },
        {
            "path": "/tmp/nonexistent.fits",
            "source": "Local archive",
            "available": False,
        },
    ]
    repo.save(metadata)

    loaded = repo.load(metadata.project_id)
    assert len(loaded.external_data_references) == 2
    assert loaded.external_data_references[0]["path"].endswith(".fits")
    assert loaded.external_data_references[0]["source"] == "STScI"
    assert loaded.external_data_references[1]["available"] is False


# ------------------------------------------------------------------
# Projects root resolution
# ------------------------------------------------------------------

def test_default_projects_root_contains_astronomy_projects():
    provider = ConfigProvider()
    root = provider.get_projects_root()
    assert isinstance(root, str)
    assert root == DEFAULT_PROJECTS_ROOT
    assert "AstronomyProjects" in root


def test_configurable_projects_root_via_config_file(tmp_path):
    config_file = tmp_path / "config.json"
    provider = ConfigProvider(config_path=str(config_file))
    custom_root = str(tmp_path / "custom_projects")
    provider.save_config(custom_root)
    assert provider.get_projects_root() == custom_root


def test_projects_root_from_environment_variable(tmp_path, monkeypatch):
    custom_root = str(tmp_path / "env_projects")
    monkeypatch.setenv("ASTRONOMY_PROJECTS_ROOT", custom_root)
    provider = ConfigProvider()
    assert provider.get_projects_root() == custom_root


# ------------------------------------------------------------------
# Error handling
# ------------------------------------------------------------------

def test_missing_project_metadata_raises_not_found(tmp_path):
    repo = ProjectRepository(tmp_path)
    with pytest.raises(ProjectNotFoundError):
        repo.load("nonexistent-id")


def test_malformed_json_handling(tmp_path):
    repo = ProjectRepository(tmp_path)
    project_dir = tmp_path / "bad-project"
    project_dir.mkdir(parents=True)
    (project_dir / "project.json").write_text("not valid json {{{", encoding="utf-8")
    with pytest.raises(ProjectCorruptedError):
        repo.load("bad-project")


def test_missing_required_fields_handling(tmp_path):
    repo = ProjectRepository(tmp_path)
    project_dir = tmp_path / "incomplete-project"
    project_dir.mkdir(parents=True)
    (project_dir / "project.json").write_text(
        json.dumps({"name": "Incomplete"}), encoding="utf-8"
    )
    with pytest.raises(ProjectCorruptedError):
        repo.load("incomplete-project")


def test_invalid_status_handling(tmp_path):
    repo = ProjectRepository(tmp_path)
    project_dir = tmp_path / "bad-status-project"
    project_dir.mkdir(parents=True)
    (project_dir / "project.json").write_text(
        json.dumps({
            "project_id": "bad-status-project",
            "name": "Bad Status",
            "created_at": "2026-01-01T00:00:00+00:00",
            "status": "NotARealStatus",
        }),
        encoding="utf-8",
    )
    with pytest.raises(ProjectCorruptedError):
        repo.load("bad-status-project")


# ------------------------------------------------------------------
# Atomic write behavior
# ------------------------------------------------------------------

def test_failed_write_preserves_previous_valid_metadata(tmp_path):
    repo = ProjectRepository(tmp_path)
    metadata = ProjectMetadata.create("Original Project")
    repo.save(metadata)
    original = repo.load(metadata.project_id)
    assert original.name == "Original Project"

    # Simulate a write failure by making os.replace raise.
    with patch("os.replace", side_effect=OSError("simulated write failure")):
        metadata2 = ProjectMetadata.create("Modified Project")
        metadata2.project_id = metadata.project_id
        metadata2.name = "Modified Project"
        with pytest.raises(OSError):
            repo.save(metadata2)

    # Original metadata must still be intact.
    loaded = repo.load(metadata.project_id)
    assert loaded.name == "Original Project"
    assert not loaded.is_dirty


def test_failed_creation_leaves_no_incomplete_directory(tmp_path):
    # Simulate a filesystem failure by making Path.mkdir raise.
    unreachable_root = tmp_path / "projects"
    with patch(
        "pathlib.Path.mkdir", side_effect=OSError("simulated mkdir failure")
    ):
        unreachable_repo = ProjectRepository(str(unreachable_root))
        metadata = ProjectMetadata.create("Unreachable Project")
        with pytest.raises(OSError):
            unreachable_repo.save(metadata)

    # No project directory should have been created.
    assert not unreachable_root.exists()


# ------------------------------------------------------------------
# Repository queries
# ------------------------------------------------------------------

def test_list_projects_empty_when_root_does_not_exist(tmp_path):
    nonexistent = tmp_path / "does_not_exist"
    repo = ProjectRepository(str(nonexistent))
    assert repo.list_projects() == []


def test_list_projects_returns_sorted_ids(tmp_path):
    repo = ProjectRepository(tmp_path)
    repo.save(ProjectMetadata.create("Project B"))
    repo.save(ProjectMetadata.create("Project A"))
    ids = repo.list_projects()
    assert ids == sorted(ids)
    assert len(ids) == 2


def test_project_exists_after_save(tmp_path):
    repo = ProjectRepository(tmp_path)
    metadata = ProjectMetadata.create("Exists Test")
    assert not repo.project_exists(metadata.project_id)
    repo.save(metadata)
    assert repo.project_exists(metadata.project_id)
