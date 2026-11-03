"""Tests for project save and close (Subtask 2.1.5).

Covers dirty-state tracking, successful saving, failed saving,
clean/dirty project closing, Save/Discard/Cancel handling, and
UI menu state and dirty indicator behavior.

Uses temporary directories only. Does not touch the real Kepler-10b dataset.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest
from PySide6.QtWidgets import QMessageBox

from src.config_provider import ConfigProvider
from src.main_window import MainWindow
from src.project_model import ProjectMetadata, ProjectValidationError
from src.project_repository import ProjectRepository
from src.project_service import (
    ProjectOpeningError,
    ProjectRepositoryError,
    ProjectService,
)


def _app():
    """Return the QApplication instance, creating one if needed."""
    from PySide6.QtWidgets import QApplication

    return QApplication.instance() or QApplication([])


# ------------------------------------------------------------------
# Dirty-state tracking (model level)
# ------------------------------------------------------------------

def test_set_name_marks_dirty():
    metadata = ProjectMetadata.create("Original Name")
    assert not metadata.is_dirty

    metadata.set_name("New Name")
    assert metadata.name == "New Name"
    assert metadata.is_dirty


def test_set_name_unchanged_does_not_mark_dirty():
    metadata = ProjectMetadata.create("Original Name")
    assert not metadata.is_dirty

    metadata.set_name("Original Name")
    assert metadata.name == "Original Name"
    assert not metadata.is_dirty


def test_set_name_whitespace_unchanged_does_not_mark_dirty():
    metadata = ProjectMetadata.create("Original Name")
    assert not metadata.is_dirty

    metadata.set_name("  Original Name  ")
    assert metadata.name == "Original Name"
    assert not metadata.is_dirty


def test_set_name_invalid_rejected():
    metadata = ProjectMetadata.create("Original Name")
    assert not metadata.is_dirty

    with pytest.raises(ProjectValidationError):
        metadata.set_name("")

    with pytest.raises(ProjectValidationError):
        metadata.set_name("bad/name")

    assert metadata.name == "Original Name"
    assert not metadata.is_dirty


# ------------------------------------------------------------------
# Service-level save
# ------------------------------------------------------------------

def test_save_project_marks_clean(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)

    metadata = service.create_project("Save Test")
    metadata.set_name("Renamed Project")
    assert metadata.is_dirty

    saved = service.save_project()
    assert not saved.is_dirty

    loaded = repo.load(metadata.project_id)
    assert loaded.name == "Renamed Project"


def test_save_project_no_active_project(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)

    with pytest.raises(ProjectRepositoryError, match="No active project"):
        service.save_project()


def test_save_failed_keeps_dirty(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)

    metadata = service.create_project("Save Fail Test")
    metadata.set_name("Modified")

    def failing_save(md):
        raise OSError("Simulated disk full")

    with patch.object(
        repo, "save", side_effect=failing_save
    ):
        with pytest.raises(ProjectRepositoryError):
            service.save_project()

    # Project must remain dirty and active
    assert service.active_project is metadata
    assert service.active_project.is_dirty

    # Original project.json must be unchanged
    loaded = repo.load(metadata.project_id)
    assert loaded.name == "Save Fail Test"
    assert not loaded.is_dirty


# ------------------------------------------------------------------
# Service-level close
# ------------------------------------------------------------------

def test_close_clean_project_clears_active(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)

    metadata = service.create_project("Clean Close")
    assert service.active_project is metadata

    service.close_project()
    assert service.active_project is None


def test_close_dirty_project_without_prompt_clears(tmp_path):
    """close_project() itself does not prompt; caller handles prompting."""
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)

    metadata = service.create_project("Dirty Close")
    metadata.set_name("Modified")
    assert service.active_project is metadata
    assert service.active_project.is_dirty

    service.close_project()
    assert service.active_project is None


def test_close_with_no_active_project_is_noop(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)

    assert service.active_project is None

    # Should not raise
    service.close_project()
    assert service.active_project is None


# ------------------------------------------------------------------
# UI-level tests
# ------------------------------------------------------------------

def test_save_and_close_menu_actions_exist():
    app = _app()
    provider = ConfigProvider()
    service = ProjectService(provider)
    window = MainWindow(service=service)

    assert window._save_action is not None
    assert window._close_action is not None
    assert not window._save_action.isEnabled()
    assert not window._close_action.isEnabled()

    window.close()


def test_save_enabled_when_dirty(tmp_path):
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    assert not window._save_action.isEnabled()

    service.create_project("Dirty Project")
    assert not window._save_action.isEnabled()  # clean after creation

    service.active_project.set_name("Modified")
    window._update_dirty_indicator()  # Refresh UI after model change
    assert window._save_action.isEnabled()  # dirty -> enabled

    window.close()


def test_close_enabled_when_project_active(tmp_path):
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    assert not window._close_action.isEnabled()

    service.create_project("Close Test")
    window._update_menu_state()  # Refresh UI after model change
    assert window._close_action.isEnabled()

    window.close()


def test_dirty_indicator_shows_asterisk(tmp_path):
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    assert window._active_label.text() == "No project"

    service.create_project("Indicator Test")
    window._update_dirty_indicator()
    assert window._active_label.text() == "Active project: Indicator Test"

    service.active_project.set_name("Modified")
    window._update_dirty_indicator()
    assert window._active_label.text() == "Active project: Modified *"

    service.save_project()
    window._update_dirty_indicator()
    assert window._active_label.text() == "Active project: Modified"

    window.close()


def test_close_clean_project_via_ui(tmp_path):
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    service.create_project("Clean UI Close")
    assert service.active_project is not None

    window._on_close_project()
    assert service.active_project is None
    assert window._active_label.text() == "No project"
    assert not window._save_action.isEnabled()
    assert not window._close_action.isEnabled()

    window.close()


def test_close_dirty_project_save_via_ui(tmp_path):
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    service.create_project("Dirty UI Close")
    service.active_project.set_name("Modified")

    # Simulate user clicking Save in the close dialog
    with patch.object(
        QMessageBox, "question", return_value=QMessageBox.StandardButton.Save
    ):
        window._on_close_project()

    assert service.active_project is None
    loaded = repo.list_projects()
    assert len(loaded) == 1

    window.close()


def test_close_dirty_project_discard_via_ui(tmp_path):
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    service.create_project("Dirty Discard")
    service.active_project.set_name("Modified")

    # Simulate user clicking Discard in the close dialog
    with patch.object(
        QMessageBox, "question", return_value=QMessageBox.StandardButton.Discard
    ):
        window._on_close_project()

    assert service.active_project is None
    # Project was saved during creation; discard only skips the rename
    loaded = repo.list_projects()
    assert len(loaded) == 1
    loaded_metadata = repo.load(loaded[0])
    assert loaded_metadata.name == "Dirty Discard"  # Original name preserved

    window.close()


def test_close_dirty_project_cancel_via_ui(tmp_path):
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    service.create_project("Dirty Cancel")
    service.active_project.set_name("Modified")
    window._update_dirty_indicator()
    assert service.active_project is not None
    assert service.active_project.is_dirty

    # Simulate user clicking Cancel in the close dialog.
    # Patch at the module level where QMessageBox is referenced.
    with patch(
        "src.main_window.QMessageBox.question",
        return_value=QMessageBox.StandardButton.Cancel,
    ):
        window._on_close_project()

    # Cancel leaves project active with the modified name
    assert service.active_project is not None
    assert service.active_project.name == "Modified"
    assert service.active_project.is_dirty
    assert window._active_label.text() == "Active project: Modified *"

    window.close()


def test_close_dirty_project_save_fails_via_ui(tmp_path):
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    service.create_project("Save Fail UI")
    service.active_project.set_name("Modified")
    window._update_dirty_indicator()

    def failing_save(md):
        raise OSError("Simulated disk full")

    with patch.object(
        repo, "save", side_effect=failing_save
    ):
        with patch(
            "src.main_window.QMessageBox.question",
            return_value=QMessageBox.StandardButton.Save,
        ):
            window._on_close_project()

    # Save failed, project must remain active and dirty (with modified name)
    assert service.active_project is not None
    assert service.active_project.name == "Modified"
    assert service.active_project.is_dirty
    assert window._active_label.text() == "Active project: Modified *"

    window.close()


def test_close_no_active_project_is_noop_ui():
    app = _app()
    provider = ConfigProvider()
    service = ProjectService(provider)
    window = MainWindow(service=service)

    assert service.active_project is None

    window._on_close_project()
    assert service.active_project is None
    assert window._active_label.text() == "No project"

    window.close()
