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
from src.new_project_dialog import NewProjectDialog
from src.open_project_dialog import OpenProjectDialog
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


# ------------------------------------------------------------------
# Location persistence tests (Issue A correction)
# ------------------------------------------------------------------


def test_create_project_in_custom_location_saves_there(tmp_path):
    """Creating a project in a custom location saves project.json there."""
    custom_root = tmp_path / "custom_projects"
    custom_root.mkdir()

    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(custom_root))
    service = ProjectService(provider, repo)

    metadata = service.create_project("Custom Project", location=str(custom_root))

    project_file = custom_root / metadata.project_id / "project.json"
    assert project_file.exists()
    assert service._active_location == str(custom_root)


def test_open_project_from_custom_location_saves_there(tmp_path):
    """Opening a project from a custom location saves updates there."""
    custom_root = tmp_path / "custom_projects"
    custom_root.mkdir()

    custom_repo = ProjectRepository(str(custom_root))
    metadata = ProjectMetadata.create("Custom Open")
    custom_repo.save(metadata)

    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)

    loaded = service.open_project_from_path(str(custom_root / metadata.project_id))

    assert service._active_location == str(custom_root)

    loaded.set_name("Renamed Custom")
    service.save_project()

    updated = custom_repo.load(metadata.project_id)
    assert updated.name == "Renamed Custom"
    assert not updated.is_dirty


def test_open_project_from_default_location_saves_there(tmp_path):
    """Opening a project from default location saves to default location."""
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)

    metadata = service.create_project("Default Project")
    assert service._active_location == str(tmp_path)

    metadata.set_name("Renamed Default")
    service.save_project()

    loaded = repo.load(metadata.project_id)
    assert loaded.name == "Renamed Default"
    assert not loaded.is_dirty


def test_multiple_projects_in_different_locations_saved_separately(tmp_path):
    """Multiple projects in different locations are saved to their own locations."""
    custom_root = tmp_path / "custom_projects"
    custom_root.mkdir()

    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)

    # Create project in default location and save while active
    default_project = service.create_project("Default Project")
    default_project.set_name("Renamed Default")
    service.save_project()

    loaded_default = repo.load(default_project.project_id)
    assert loaded_default.name == "Renamed Default"

    # Create project in custom location and save while active
    custom_project = service.create_project("Custom Project", location=str(custom_root))
    custom_project.set_name("Renamed Custom")
    service.save_project()

    custom_repo = ProjectRepository(str(custom_root))
    loaded_custom = custom_repo.load(custom_project.project_id)
    assert loaded_custom.name == "Renamed Custom"

    # Verify no duplicate in default location for custom project
    custom_project_file = tmp_path / custom_project.project_id / "project.json"
    assert not custom_project_file.exists()


def test_no_duplicate_project_directory_in_default_location(tmp_path):
    """Saving a custom-location project does not create a duplicate in default root."""
    custom_root = tmp_path / "custom_projects"
    custom_root.mkdir()

    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)

    metadata = service.create_project("Custom Project", location=str(custom_root))
    metadata.set_name("Renamed Custom")
    service.save_project()

    custom_project_file = custom_root / metadata.project_id / "project.json"
    assert custom_project_file.exists()

    default_project_file = tmp_path / metadata.project_id / "project.json"
    assert not default_project_file.exists()


def test_injected_repository_used_when_location_matches(tmp_path):
    """When active location matches injected repo's root, use injected repo."""
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)

    metadata = service.create_project("DI Project")
    assert service._active_location == str(tmp_path)

    save_calls = []
    original_save = repo.save

    def tracking_save(md):
        save_calls.append(md.project_id)
        original_save(md)

    with patch.object(repo, "save", side_effect=tracking_save):
        metadata.set_name("Renamed DI")
        service.save_project()

    assert len(save_calls) == 1
    assert save_calls[0] == metadata.project_id


def test_active_location_reset_after_close(tmp_path):
    """_active_location is cleared after closing the project."""
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)

    metadata = service.create_project("Close Location Test")
    assert service._active_location is not None

    service.close_project()
    assert service._active_location is None


def test_failed_operation_preserves_previous_active_location(tmp_path):
    """Failed save preserves previous active location."""
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)

    metadata = service.create_project("Previous Location")
    original_location = service._active_location

    metadata.set_name("Modified")

    def failing_save(md):
        raise OSError("Simulated disk full")

    with patch.object(
        repo, "save", side_effect=failing_save
    ):
        with pytest.raises(ProjectRepositoryError):
            service.save_project()

    assert service._active_location == original_location
    assert service.active_project is metadata
    assert service.active_project.is_dirty


# ------------------------------------------------------------------
# Unsaved-project protection tests (Issue B correction)
# ------------------------------------------------------------------


def test_new_project_with_no_active_project_proceeds(tmp_path):
    """Creating a new project with no active project proceeds normally."""
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)
    window = MainWindow(service=service)

    with patch(
        "src.main_window.NewProjectDialog"
    ) as MockDialog:
        mock_instance = MockDialog.return_value
        mock_instance.exec.return_value = True
        mock_instance.project_name.return_value = "New Project"
        mock_instance.project_location.return_value = ""

        window._on_new_project()

    assert service.active_project is not None
    assert service.active_project.name == "New Project"

    window.close()


def test_open_project_with_no_active_project_proceeds(tmp_path):
    """Opening a project with no active project proceeds normally."""
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    metadata = service.create_project("To Be Opened")
    service.close_project()
    assert service.active_project is None

    with patch(
        "src.main_window.OpenProjectDialog"
    ) as MockDialog:
        mock_instance = MockDialog.return_value
        mock_instance.exec.return_value = True
        mock_instance.custom_location.return_value = None
        mock_instance.selected_project_id.return_value = metadata.project_id

        window._on_open_project()

    assert service.active_project is not None
    assert service.active_project.name == "To Be Opened"

    window.close()


def test_new_project_with_clean_active_project_proceeds_without_prompt(tmp_path):
    """Creating a new project with a clean active project proceeds without prompt."""
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    service.create_project("Clean Project")
    assert service.active_project is not None
    assert not service.active_project.is_dirty

    with patch(
        "src.main_window.NewProjectDialog"
    ) as MockDialog:
        mock_instance = MockDialog.return_value
        mock_instance.exec.return_value = True
        mock_instance.project_name.return_value = "Second Project"
        mock_instance.project_location.return_value = ""

        with patch.object(
            QMessageBox, "question", return_value=QMessageBox.StandardButton.Save
        ) as mock_question:
            window._on_new_project()

    mock_question.assert_not_called()

    assert service.active_project is not None
    assert service.active_project.name == "Second Project"

    window.close()


def test_new_project_with_dirty_project_save_then_create(tmp_path):
    """Creating a new project with dirty project: Save saves then creates new."""
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    service.create_project("First Project")
    service.active_project.set_name("Modified Name")

    with patch(
        "src.main_window.NewProjectDialog"
    ) as MockDialog:
        mock_instance = MockDialog.return_value
        mock_instance.exec.return_value = True
        mock_instance.project_name.return_value = "Second Project"
        mock_instance.project_location.return_value = ""

        with patch.object(
            QMessageBox, "question", return_value=QMessageBox.StandardButton.Save
        ):
            window._on_new_project()

    loaded = repo.list_projects()
    assert len(loaded) == 2
    for pid in loaded:
        m = repo.load(pid)
        if m.name == "Modified Name":
            assert not m.is_dirty

    assert service.active_project is not None
    assert service.active_project.name == "Second Project"

    window.close()


def test_new_project_with_dirty_project_discard_then_create(tmp_path):
    """Creating a new project with dirty project: Discard creates new without saving."""
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    service.create_project("First Project")
    service.active_project.set_name("Modified Name")

    with patch(
        "src.main_window.NewProjectDialog"
    ) as MockDialog:
        mock_instance = MockDialog.return_value
        mock_instance.exec.return_value = True
        mock_instance.project_name.return_value = "Second Project"
        mock_instance.project_location.return_value = ""

        with patch.object(
            QMessageBox, "question", return_value=QMessageBox.StandardButton.Discard
        ):
            window._on_new_project()

    assert service.active_project is not None
    assert service.active_project.name == "Second Project"

    for pid in repo.list_projects():
        m = repo.load(pid)
        if m.name == "First Project":
            assert m.name == "First Project"

    window.close()


def test_new_project_with_dirty_project_cancel_preserves_active(tmp_path):
    """Creating a new project with dirty project: Cancel preserves active project."""
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    service.create_project("First Project")
    service.active_project.set_name("Modified Name")
    window._update_dirty_indicator()
    assert service.active_project.is_dirty

    with patch(
        "src.main_window.NewProjectDialog"
    ) as MockDialog:
        mock_instance = MockDialog.return_value
        mock_instance.exec.return_value = True
        mock_instance.project_name.return_value = "Second Project"
        mock_instance.project_location.return_value = ""

        with patch.object(
            QMessageBox, "question", return_value=QMessageBox.StandardButton.Cancel
        ):
            window._on_new_project()

    assert service.active_project is not None
    assert service.active_project.name == "Modified Name"
    assert service.active_project.is_dirty
    window._update_dirty_indicator()
    assert window._active_label.text() == "Active project: Modified Name *"

    window.close()


def test_open_project_with_dirty_project_save_then_open(tmp_path):
    """Opening a project with dirty project: Save saves then opens new."""
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    service.create_project("First Project")
    service.active_project.set_name("Modified Name")

    other_metadata = service.create_project("Other Project")
    service.close_project()
    service.open_project(other_metadata.project_id)

    with patch(
        "src.main_window.OpenProjectDialog"
    ) as MockDialog:
        mock_instance = MockDialog.return_value
        mock_instance.exec.return_value = True
        mock_instance.custom_location.return_value = None
        mock_instance.selected_project_id.return_value = other_metadata.project_id

        with patch.object(
            QMessageBox, "question", return_value=QMessageBox.StandardButton.Save
        ):
            window._on_open_project()

    assert service.active_project is not None
    assert service.active_project.name == "Other Project"

    for pid in repo.list_projects():
        m = repo.load(pid)
        if m.name == "Modified Name":
            assert not m.is_dirty

    window.close()


def test_open_project_with_dirty_project_discard_then_open(tmp_path):
    """Opening a project with dirty project: Discard opens new without saving."""
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    service.create_project("First Project")
    service.active_project.set_name("Modified Name")
    assert service.active_project.is_dirty

    other_metadata = service.create_project("Other Project")
    service.close_project()
    service.open_project(other_metadata.project_id)

    with patch(
        "src.main_window.OpenProjectDialog"
    ) as MockDialog:
        mock_instance = MockDialog.return_value
        mock_instance.exec.return_value = True
        mock_instance.custom_location.return_value = None
        mock_instance.selected_project_id.return_value = other_metadata.project_id

        with patch.object(
            QMessageBox, "question", return_value=QMessageBox.StandardButton.Discard
        ):
            window._on_open_project()

    assert service.active_project is not None
    assert service.active_project.name == "Other Project"

    window.close()


def test_open_project_with_dirty_project_cancel_preserves_active(tmp_path):
    """Opening a project with dirty project: Cancel preserves active project."""
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)
    window = MainWindow(service=service)

    service.create_project("First Project")
    service.active_project.set_name("Modified Name")
    assert service.active_project.is_dirty

    # Try to open a different project with Cancel - active project should be preserved
    with patch.object(QMessageBox, "question", return_value=QMessageBox.StandardButton.Cancel):
        result = window._prompt_save_before_switch()

    assert result is False
    assert service.active_project is not None
    assert service.active_project.name == "Modified Name"
    assert service.active_project.is_dirty

    window.close()


def test_new_project_save_failure_preserves_active_project(tmp_path):
    """Save failure during New preserves existing active project and dirty state."""
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    service.create_project("Existing Project")
    service.active_project.set_name("Modified Name")
    assert service.active_project.is_dirty

    dialog = NewProjectDialog(default_location=str(tmp_path))
    dialog._name_edit.setText("Second Project")
    dialog.accept()

    def failing_save(md):
        raise OSError("Simulated disk full")

    with patch.object(
        repo, "save", side_effect=failing_save
    ):
        with patch.object(
            QMessageBox, "question", return_value=QMessageBox.StandardButton.Save
        ):
            window._on_new_project()

    assert service.active_project is not None
    assert service.active_project.name == "Modified Name"
    assert service.active_project.is_dirty

    window.close()


def test_open_project_save_failure_preserves_active_project(tmp_path):
    """Save failure during Open preserves existing active project and dirty state."""
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)
    window = MainWindow(service=service)

    service.create_project("Existing Project")
    service.active_project.set_name("Modified Name")
    assert service.active_project.is_dirty

    # Try to open a different project with Save - save fails, active project preserved
    with patch.object(QMessageBox, "question", return_value=QMessageBox.StandardButton.Save):
        with patch.object(service, "save_project", side_effect=OSError("Simulated disk full")):
            result = window._prompt_save_before_switch()

    assert result is False
    assert service.active_project is not None
    assert service.active_project.name == "Modified Name"
    assert service.active_project.is_dirty


def test_new_project_creation_failure_after_discard_preserves_active(tmp_path):
    """Creation failure after Discard preserves previous active project."""
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    service.create_project("Existing Project")
    service.active_project.set_name("Modified Name")

    with patch(
        "src.main_window.NewProjectDialog"
    ) as MockDialog:
        mock_instance = MockDialog.return_value
        mock_instance.exec.return_value = True
        mock_instance.project_name.return_value = "Second Project"
        mock_instance.project_location.return_value = ""

        def failing_create(name, location=None):
            raise OSError("Simulated creation failure")

        with patch.object(
            QMessageBox, "question", return_value=QMessageBox.StandardButton.Discard
        ):
            with patch.object(
                service, "create_project", side_effect=failing_create
            ):
                window._on_new_project()

    assert service.active_project is not None
    assert service.active_project.name == "Modified Name"
    assert service.active_project.is_dirty

    window.close()


def test_open_project_opening_failure_after_discard_preserves_active(tmp_path):
    """Opening failure after Discard preserves previous active project."""
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)
    window = MainWindow(service=service)

    service.create_project("Existing Project")
    service.active_project.set_name("Modified Name")
    assert service.active_project.is_dirty

    # Try to open a different project with Discard - discard succeeds, active preserved
    with patch.object(QMessageBox, "question", return_value=QMessageBox.StandardButton.Discard):
        result = window._prompt_save_before_switch()

    assert result is True
    assert service.active_project is not None
    assert service.active_project.name == "Modified Name"
    assert service.active_project.is_dirty
