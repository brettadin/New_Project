"""Tests for project lifecycle status management (Subtask 2.1.6).

Covers model-level status changes, service-level status operations,
UI status submenu behavior, persistence, and reopening.

Uses temporary directories only. Does not touch the real Kepler-10b dataset.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest
from PySide6.QtWidgets import QMessageBox

from src.config_provider import ConfigProvider
from src.main_window import MainWindow
from src.project_model import ProjectMetadata, ProjectValidationError, VALID_STATUSES
from src.project_repository import ProjectRepository
from src.project_service import ProjectRepositoryError, ProjectService


def _app():
    """Return the QApplication instance, creating one if needed."""
    from PySide6.QtWidgets import QApplication

    return QApplication.instance() or QApplication([])


# ------------------------------------------------------------------
# Model-level status tests
# ------------------------------------------------------------------

def test_set_status_marks_dirty():
    metadata = ProjectMetadata.create("Test Project")
    assert not metadata.is_dirty
    assert metadata.status == "Active"

    metadata.set_status("Paused")
    assert metadata.status == "Paused"
    assert metadata.is_dirty


def test_set_status_unchanged_does_not_mark_dirty():
    metadata = ProjectMetadata.create("Test Project")
    assert not metadata.is_dirty

    metadata.set_status("Active")
    assert metadata.status == "Active"
    assert not metadata.is_dirty


def test_set_status_all_valid_transitions():
    metadata = ProjectMetadata.create("Test Project")
    for status in VALID_STATUSES:
        metadata.status = "Active"  # reset
        metadata.is_dirty = False
        metadata.set_status(status)
        assert metadata.status == status
        if status != "Active":
            assert metadata.is_dirty


def test_set_status_invalid_rejected():
    metadata = ProjectMetadata.create("Test Project")
    assert not metadata.is_dirty

    with pytest.raises(ProjectValidationError):
        metadata.set_status("InvalidStatus")

    with pytest.raises(ProjectValidationError):
        metadata.set_status("")

    assert metadata.status == "Active"
    assert not metadata.is_dirty


def test_set_status_preserves_other_fields():
    metadata = ProjectMetadata.create("Test Project")
    metadata.external_data_references = [{"path": "test.fits"}]
    original_name = metadata.name
    original_id = metadata.project_id
    original_created = metadata.created_at

    metadata.set_status("Completed")
    assert metadata.name == original_name
    assert metadata.project_id == original_id
    assert metadata.created_at == original_created
    assert metadata.external_data_references == [{"path": "test.fits"}]


# ------------------------------------------------------------------
# Service-level status tests
# ------------------------------------------------------------------

def test_change_status_with_active_project(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)

    metadata = service.create_project("Status Test")
    assert metadata.status == "Active"

    updated = service.change_status("Paused")
    assert updated.status == "Paused"
    assert service.active_project is updated
    assert service.active_project.is_dirty


def test_change_status_no_active_project(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)

    assert service.active_project is None
    with pytest.raises(ProjectRepositoryError, match="No active project"):
        service.change_status("Paused")


def test_change_status_invalid_rejected(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)

    service.create_project("Status Test")
    with pytest.raises(ProjectValidationError):
        service.change_status("NotAStatus")


def test_change_status_preserves_active_location(tmp_path):
    custom_root = tmp_path / "custom_projects"
    custom_root.mkdir()

    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    service = ProjectService(provider)

    service.create_project("Custom Status", location=str(custom_root))
    original_location = service._active_location
    service.change_status("Completed")
    assert service._active_location == original_location


def test_change_status_persisted_on_save(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)

    metadata = service.create_project("Status Persist")
    service.change_status("Completed")
    assert service.active_project.is_dirty

    service.save_project()
    assert not service.active_project.is_dirty

    loaded = repo.load(metadata.project_id)
    assert loaded.status == "Completed"
    assert not loaded.is_dirty


def test_change_status_restored_on_open(tmp_path):
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)

    metadata = service.create_project("Status Restore")
    service.change_status("Archived")
    service.save_project()

    service.close_project()
    assert service.active_project is None

    loaded = service.open_project(metadata.project_id)
    assert loaded.status == "Archived"
    assert not loaded.is_dirty


# ------------------------------------------------------------------
# UI tests
# ------------------------------------------------------------------

def test_status_menu_actions_exist():
    app = _app()
    provider = ConfigProvider()
    service = ProjectService(provider)
    window = MainWindow(service=service)

    assert window._status_menu is not None
    assert len(window._status_actions) == 4
    for status in ("Active", "Paused", "Completed", "Archived"):
        assert status in window._status_actions
        assert window._status_actions[status].isCheckable()

    window.close()


def test_status_menu_disabled_when_no_project():
    app = _app()
    provider = ConfigProvider()
    service = ProjectService(provider)
    window = MainWindow(service=service)

    assert not window._status_menu.isEnabled()
    for action in window._status_actions.values():
        assert not action.isEnabled()

    window.close()


def test_status_menu_enabled_when_project_active(tmp_path):
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    service.create_project("Status UI")
    window._update_status_menu()

    assert window._status_menu.isEnabled()
    for action in window._status_actions.values():
        assert action.isEnabled()

    window.close()


def test_correct_status_checked_after_create(tmp_path):
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    service.create_project("Status Check")
    window._update_status_menu()

    assert window._status_actions["Active"].isChecked()
    for status in ("Paused", "Completed", "Archived"):
        assert not window._status_actions[status].isChecked()

    window.close()


def test_selecting_status_updates_service_and_dirty_indicator(tmp_path):
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    service.create_project("Status Change")
    window._update_status_menu()

    assert window._status_actions["Active"].isChecked()
    assert not service.active_project.is_dirty

    # Simulate selecting "Paused"
    window._on_change_status("Paused")

    assert service.active_project.status == "Paused"
    assert service.active_project.is_dirty
    assert window._status_actions["Paused"].isChecked()
    assert not window._status_actions["Active"].isChecked()
    assert window._active_label.text() == "Active project: Status Change *"

    window.close()


def test_checked_status_updates_after_status_change(tmp_path):
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    service.create_project("Status Update")
    window._update_status_menu()

    window._on_change_status("Completed")
    window._update_status_menu()

    assert window._status_actions["Completed"].isChecked()
    for status in ("Active", "Paused", "Archived"):
        assert not window._status_actions[status].isChecked()

    window.close()


def test_status_submenu_disabled_after_close(tmp_path):
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    service.create_project("Status Close")
    window._update_status_menu()
    assert window._status_menu.isEnabled()

    window._on_close_project()
    assert not window._status_menu.isEnabled()
    for action in window._status_actions.values():
        assert not action.isEnabled()

    window.close()


def test_completed_project_openable(tmp_path):
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    metadata = service.create_project("Completed Project")
    service.change_status("Completed")
    service.save_project()

    service.close_project()
    assert service.active_project is None

    loaded = service.open_project(metadata.project_id)
    assert loaded.status == "Completed"
    assert service.active_project is loaded

    window.close()


def test_archived_project_openable(tmp_path):
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    metadata = service.create_project("Archived Project")
    service.change_status("Archived")
    service.save_project()

    service.close_project()
    assert service.active_project is None

    loaded = service.open_project(metadata.project_id)
    assert loaded.status == "Archived"
    assert service.active_project is loaded

    window.close()


def test_status_change_does_not_modify_other_fields(tmp_path):
    app = _app()
    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)
    window = MainWindow(service=service)

    metadata = service.create_project("Field Preserve")
    original_name = metadata.name
    original_id = metadata.project_id
    original_created = metadata.created_at
    metadata.external_data_references = [{"path": "test.fits"}]

    service.change_status("Paused")
    assert service.active_project.name == original_name
    assert service.active_project.project_id == original_id
    assert service.active_project.created_at == original_created
    assert service.active_project.external_data_references == [{"path": "test.fits"}]

    window.close()
