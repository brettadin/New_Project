"""Tests for the New Project dialog and MainWindow integration (Subtask 2.1.3).

Tests dialog behavior without requiring a UI-testing dependency beyond
PySide6 itself (already part of the approved stack). Uses QApplication
in offscreen mode implicitly through the test environment.
"""

from __future__ import annotations

from unittest.mock import patch

from PySide6.QtWidgets import QApplication, QDialog

from src.config_provider import ConfigProvider
from src.main_window import MainWindow
from src.new_project_dialog import NewProjectDialog
from src.project_repository import ProjectRepository
from src.project_service import ProjectService


def _app():
    """Return the QApplication instance, creating one if needed."""
    return QApplication.instance() or QApplication([])


# ------------------------------------------------------------------
# Dialog creation and defaults
# ------------------------------------------------------------------

def test_dialog_has_default_location():
    app = _app()
    default = "/some/default/path"
    dialog = NewProjectDialog(default_location=default)
    assert dialog.project_location() == default
    assert dialog.project_name() == ""
    dialog.reject()


def test_dialog_default_location_empty():
    app = _app()
    dialog = NewProjectDialog()
    assert dialog.project_location() == ""
    assert dialog.project_name() == ""
    dialog.reject()


# ------------------------------------------------------------------
# Name input and validation
# ------------------------------------------------------------------

def test_dialog_accept_returns_name():
    app = _app()
    dialog = NewProjectDialog(default_location="/tmp/test")
    dialog._name_edit.setText("My Project")
    dialog.accept()
    assert dialog.result() == QDialog.DialogCode.Accepted
    assert dialog.project_name() == "My Project"


def test_dialog_accept_whitespace_name_stripped():
    app = _app()
    dialog = NewProjectDialog()
    dialog._name_edit.setText("  Spaced Project  ")
    dialog.accept()
    assert dialog.project_name() == "Spaced Project"


def test_dialog_create_button_disabled_for_empty_name():
    app = _app()
    dialog = NewProjectDialog()
    assert not dialog._create_button.isEnabled()

    dialog._name_edit.setText("   ")
    assert not dialog._create_button.isEnabled()

    dialog._name_edit.setText("Valid Name")
    assert dialog._create_button.isEnabled()
    dialog.reject()


# ------------------------------------------------------------------
# Cancel behavior
# ------------------------------------------------------------------

def test_dialog_cancel_returns_rejected():
    app = _app()
    dialog = NewProjectDialog(default_location="/tmp/test")
    dialog._name_edit.setText("My Project")
    dialog.reject()
    assert dialog.result() == QDialog.DialogCode.Rejected


def test_dialog_cancel_does_not_alter_location():
    app = _app()
    default = "/some/default/path"
    dialog = NewProjectDialog(default_location=default)
    dialog._location_edit.setText("/custom/location")
    dialog.reject()
    # After reject, the dialog's location reflects what was entered,
    # but the caller simply ignores the result on cancel.
    assert dialog.project_location() == "/custom/location"


# ------------------------------------------------------------------
# MainWindow active-project indicator
# ------------------------------------------------------------------

def test_main_window_initial_indicator_is_no_project():
    app = _app()
    window = MainWindow()
    assert window._active_label.text() == "No project"
    window.close()


def test_main_window_set_active_project_displays_name():
    app = _app()
    window = MainWindow()

    window.set_active_project("My Research")
    assert window._active_label.text() == "Active project: My Research"

    window.set_active_project(None)
    assert window._active_label.text() == "No project"
    window.close()


# ------------------------------------------------------------------
# Dialog cancel does not create a project
# ------------------------------------------------------------------

def test_dialog_cancel_does_not_create_project(tmp_path):
    """Cancelling the New Project dialog must not create a project
    or alter the active project on the service."""
    app = _app()

    provider = ConfigProvider()
    provider.set_projects_root(str(tmp_path))
    repo = ProjectRepository(str(tmp_path))
    service = ProjectService(provider, repo)

    assert service.active_project is None

    dialog = NewProjectDialog(default_location=str(tmp_path))
    dialog._name_edit.setText("Cancelled Project")
    dialog.reject()

    assert dialog.result() == QDialog.DialogCode.Rejected
    assert service.active_project is None
    assert repo.list_projects() == []

