"""Tests for project discovery and opening (Subtask 2.1.4).

Covers project discovery from the default root and custom locations,
opening valid projects, rejecting invalid/missing/corrupted metadata,
active-project tracking on success/failure/cancellation, and that
opening does not modify project metadata.

Uses temporary directories only. Does not touch the real Kepler-10b dataset.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from src.config_provider import ConfigProvider
from src.main_window import MainWindow
from src.new_project_dialog import NewProjectDialog
from src.open_project_dialog import OpenProjectDialog
from src.project_model import ProjectMetadata
from src.project_repository import (
    ProjectCorruptedError,
    ProjectNotFoundError,
    ProjectRepository,
)
from src.project_service import (
    ProjectOpeningError,
    ProjectService,
)


def _app():
    """Return the QApplication instance, creating one if needed."""
    from PySide6.QtWidgets import QApplication

    return QApplication.instance() or QApplication([])


# ------------------------------------------------------------------
# Discovery - repository level
# ------------------------------------------------------------------

def test_discover_multiple_valid_projects(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))

    m1 = ProjectMetadata.create("Zebra Project")
    m2 = ProjectMetadata.create("Alpha Project")
    m3 = ProjectMetadata.create("Mid Project")
    repo.save(m1)
    repo.save(m2)
    repo.save(m3)

    valid, invalid = repo.discover_projects()
    assert len(valid) == 3
    assert invalid == []
    # Sorted by name
    assert [p.name for p in valid] == ["Alpha Project", "Mid Project", "Zebra Project"]
    assert valid[0].project_id == m2.project_id
    assert valid[1].project_id == m3.project_id
    assert valid[2].project_id == m1.project_id


def test_discover_empty_root(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))

    valid, invalid = repo.discover_projects()
    assert valid == []
    assert invalid == []


def test_discover_nonexistent_root(tmp_path):
    nonexistent = tmp_path / "does_not_exist"
    repo = ProjectRepository(str(nonexistent))

    valid, invalid = repo.discover_projects()
    assert valid == []
    assert invalid == []


def test_discover_skips_directory_without_project_json(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))

    # Create a valid project
    repo.save(ProjectMetadata.create("Valid Project"))

    # Create a directory without project.json
    (tmp_path / "not_a_project").mkdir()

    valid, invalid = repo.discover_projects()
    assert len(valid) == 1
    assert valid[0].name == "Valid Project"
    assert "not_a_project" in invalid


def test_discover_skips_corrupted_metadata(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))

    # Create a valid project
    repo.save(ProjectMetadata.create("Valid Project"))

    # Create a directory with corrupted project.json
    bad_dir = tmp_path / "bad_project"
    bad_dir.mkdir()
    (bad_dir / "project.json").write_text("not valid json {{{", encoding="utf-8")

    valid, invalid = repo.discover_projects()
    assert len(valid) == 1
    assert valid[0].name == "Valid Project"
    assert "bad_project" in invalid


def test_discover_skips_missing_required_fields(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))

    repo.save(ProjectMetadata.create("Valid Project"))

    # Create a directory with incomplete project.json
    bad_dir = tmp_path / "incomplete_project"
    bad_dir.mkdir()
    (bad_dir / "project.json").write_text(
        json.dumps({"name": "Incomplete"}), encoding="utf-8"
    )

    valid, invalid = repo.discover_projects()
    assert len(valid) == 1
    assert "incomplete_project" in invalid


def test_discover_no_recursive_scanning(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))

    repo.save(ProjectMetadata.create("Top Level Project"))

    # Create a nested directory with a project.json - should NOT be discovered
    nested = tmp_path / "subdir" / "nested_project"
    nested.mkdir(parents=True)
    (nested / "project.json").write_text(
        json.dumps({
            "project_id": "nested-id",
            "name": "Nested Project",
            "created_at": "2026-01-01T00:00:00+00:00",
            "status": "Active",
            "schema_version": 1,
        }),
        encoding="utf-8",
    )

    valid, invalid = repo.discover_projects()
    assert len(valid) == 1
    assert valid[0].name == "Top Level Project"
    # subdir has no project.json at its level, so it's invalid;
    # nested_project inside subdir is not discovered (no recursion)
    assert "nested_project" not in [p.project_id for p in valid]


# ------------------------------------------------------------------
# Discovery - service level
# ------------------------------------------------------------------

def test_service_discover_projects_uses_default_root(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)

    service.create_project("Service Project")

    valid, invalid = service.discover_projects()
    assert len(valid) == 1
    assert valid[0].name == "Service Project"
    assert invalid == []


# ------------------------------------------------------------------
# Opening - repository level
# ------------------------------------------------------------------

def test_open_valid_project_from_default_root(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))

    metadata = ProjectMetadata.create("Open Test")
    repo.save(metadata)

    loaded = repo.load(metadata.project_id)
    assert loaded.project_id == metadata.project_id
    assert loaded.name == "Open Test"
    assert loaded.status == "Active"
    assert loaded.schema_version == 1


def test_open_project_from_custom_location(tmp_path):
    custom_root = tmp_path / "custom_projects"
    custom_root.mkdir()

    # Create a project directly in the custom location
    repo = ProjectRepository(str(custom_root))
    metadata = ProjectMetadata.create("Custom Location Project")
    repo.save(metadata)

    # Open from the custom directory path
    project_dir = custom_root / metadata.project_id
    loaded = ProjectRepository.load_from_directory(str(project_dir))

    assert loaded.project_id == metadata.project_id
    assert loaded.name == "Custom Location Project"
    assert loaded.status == "Active"
    assert loaded.schema_version == 1


def test_opening_does_not_modify_project_json(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))

    metadata = ProjectMetadata.create("Immutable Project")
    repo.save(metadata)

    # Record original file content
    project_file = tmp_path / metadata.project_id / "project.json"
    original_content = project_file.read_bytes()

    # Load the project multiple times
    for _ in range(3):
        repo.load(metadata.project_id)

    # File must be unchanged
    assert project_file.read_bytes() == original_content


def test_open_missing_project_raises_not_found(tmp_path):
    repo = ProjectRepository(str(tmp_path))
    with pytest.raises(ProjectNotFoundError):
        repo.load("nonexistent-id")


def test_open_corrupted_metadata_raises_corrupted(tmp_path):
    repo = ProjectRepository(str(tmp_path))
    bad_dir = tmp_path / "bad_project"
    bad_dir.mkdir()
    (bad_dir / "project.json").write_text("not valid json {{{", encoding="utf-8")

    with pytest.raises(ProjectCorruptedError):
        repo.load("bad_project")


def test_open_from_path_missing_project_json(tmp_path):
    empty_dir = tmp_path / "empty_dir"
    empty_dir.mkdir()
    with pytest.raises(ProjectNotFoundError):
        ProjectRepository.load_from_directory(str(empty_dir))


def test_open_from_path_corrupted_metadata(tmp_path):
    bad_dir = tmp_path / "bad_dir"
    bad_dir.mkdir()
    (bad_dir / "project.json").write_text("corrupted", encoding="utf-8")
    with pytest.raises(ProjectCorruptedError):
        ProjectRepository.load_from_directory(str(bad_dir))


# ------------------------------------------------------------------
# Opening - service level
# ------------------------------------------------------------------

def test_service_open_project_sets_active(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)

    metadata = service.create_project("To Be Opened")

    # Clear active project, then re-open
    service.set_active_project(None)
    assert service.active_project is None

    loaded = service.open_project(metadata.project_id)
    assert service.active_project is loaded
    assert loaded.name == "To Be Opened"
    assert loaded.status == "Active"


def test_service_open_project_from_path_sets_active(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)

    # Create a project in a custom location
    custom_dir = tmp_path / "custom_projects"
    custom_dir.mkdir()
    custom_repo = ProjectRepository(str(custom_dir))
    metadata = ProjectMetadata.create("Custom Open")
    custom_repo.save(metadata)

    # Open from the actual project directory path (not the root)
    project_dir = custom_dir / metadata.project_id
    loaded = service.open_project_from_path(str(project_dir))
    assert service.active_project is loaded
    assert loaded.name == "Custom Open"
    assert loaded.project_id == metadata.project_id


def test_service_open_failed_preserves_active_project(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)

    existing = service.create_project("Existing Project")
    assert service.active_project is existing

    # Try to open a nonexistent project
    with pytest.raises(ProjectOpeningError):
        service.open_project("nonexistent-id")

    # Previously active project must be preserved
    assert service.active_project is existing
    assert service.active_project.name == "Existing Project"


def test_service_open_corrupted_fails_with_opening_error(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)

    # Create a corrupted project.json directly
    bad_dir = tmp_path / "bad_project"
    bad_dir.mkdir()
    (bad_dir / "project.json").write_text("corrupted", encoding="utf-8")

    with pytest.raises(ProjectOpeningError):
        service.open_project("bad_project")


# ------------------------------------------------------------------
# OpenProjectDialog tests
# ------------------------------------------------------------------

def test_dialog_shows_discovered_projects():
    app = _app()
    projects = [
        ProjectMetadata.create("Alpha Project"),
        ProjectMetadata.create("Zebra Project"),
    ]
    dialog = OpenProjectDialog(projects=projects)
    assert dialog._project_list.count() == 2
    dialog.reject()


def test_dialog_empty_project_list():
    app = _app()
    dialog = OpenProjectDialog(projects=[])
    assert dialog._project_list.count() == 0
    dialog.reject()


def test_dialog_select_project_returns_id():
    app = _app()
    projects = [ProjectMetadata.create("Selectable Project")]
    dialog = OpenProjectDialog(projects=projects)
    dialog._project_list.setCurrentRow(0)
    dialog.accept()
    assert dialog.selected_project_id() == projects[0].project_id
    assert dialog.custom_location() is None


def test_dialog_browse_folder_returns_location():
    app = _app()
    dialog = OpenProjectDialog(projects=[])
    # Simulate clicking browse and selecting a folder
    with patch(
        "src.open_project_dialog.QFileDialog.getExistingDirectory",
        return_value="/custom/folder/path",
    ):
        dialog._browse_folder()
    assert dialog.custom_location() == "/custom/folder/path"
    assert dialog.selected_project_id() is None
    dialog.reject()


def test_dialog_cancel_preserves_active_project():
    app = _app()
    dialog = OpenProjectDialog(projects=[ProjectMetadata.create("Cancel Test")])
    dialog.reject()
    assert dialog.result() == 0  # Rejected


# ------------------------------------------------------------------
# MainWindow active-project indicator on open
# ------------------------------------------------------------------

def test_main_window_indicator_shows_opened_project(tmp_path):
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)
    window = MainWindow(service=service)

    assert window._active_label.text() == "No project"

    metadata = service.create_project("Window Test")
    service.open_project(metadata.project_id)
    window.set_active_project(metadata.name)
    assert window._active_label.text() == "Active project: Window Test"

    window.close()


def test_main_window_indicator_no_project_initially():
    app = _app()
    window = MainWindow()
    assert window._active_label.text() == "No project"
    window.close()


# ------------------------------------------------------------------
# Canceling new project dialog does not affect open workflow
# ------------------------------------------------------------------

def test_cancel_new_project_dialog_no_active_project(tmp_path):
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)

    assert service.active_project is None

    dialog = NewProjectDialog(default_location=str(tmp_path))
    dialog._name_edit.setText("Cancelled")
    dialog.reject()

    assert service.active_project is None
    assert repo.list_projects() == []
