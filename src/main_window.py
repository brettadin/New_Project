"""Main application window for the astronomy research application.

Provides a minimal desktop shell with an active-project indicator and a
Project > New menu action for creating research projects.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget,
    QStatusBar,
    QMessageBox,
)

from src.new_project_dialog import NewProjectDialog


class MainWindow(QMainWindow):
    """Main application window.

    Shows a minimal shell with an active-project indicator that initially
    displays "No project". Provides a Project > New menu action that opens
    the New Project dialog and activates the created project.
    """

    def __init__(self, service=None, parent=None) -> None:
        super().__init__(parent)
        self._service = service
        self.setWindowTitle("Astronomy Research Application")
        self.resize(900, 600)

        central = QWidget()
        layout = QVBoxLayout(central)

        self._active_label = QLabel("No project")
        self._active_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self._active_label)
        layout.addStretch()

        self.setCentralWidget(central)

        self._status_bar: QStatusBar = self.statusBar()
        self._status_bar.showMessage("Ready")

        self._setup_menu()

    def _setup_menu(self) -> None:
        """Create the menu bar with Project > New action."""
        project_menu = self.menuBar().addMenu("&Project")
        new_action = project_menu.addAction("&New...")
        new_action.setStatusTip("Create a new research project")
        new_action.triggered.connect(self._on_new_project)

    def _on_new_project(self) -> None:
        """Handle the Project > New menu action."""
        if self._service is None:
            self._status_bar.showMessage(
                "Project service not available", 5000
            )
            return

        dialog = NewProjectDialog(
            default_location=self._service.default_location, parent=self
        )
        if dialog.exec():
            name = dialog.project_name()
            location = dialog.project_location() or None
            try:
                metadata = self._service.create_project(name, location)
                self.set_active_project(metadata.name)
                self._status_bar.showMessage(
                    f"Project '{metadata.name}' created", 5000
                )
            except Exception as exc:  # noqa: BLE001 - UI boundary: show any error
                QMessageBox.critical(
                    self, "Project Creation Failed", str(exc)
                )

    def set_active_project(self, project_name: str | None) -> None:
        """Update the active-project indicator.

        Args:
            project_name: Name of the active project, or None when no
                project is open.
        """
        if project_name:
            self._active_label.setText(f"Active project: {project_name}")
        else:
            self._active_label.setText("No project")
