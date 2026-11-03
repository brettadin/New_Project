"""Main application window for the astronomy research application.

Provides a minimal desktop shell with an active-project indicator.
Project creation and opening dialogs are wired up in later subtasks.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget,
    QStatusBar,
)


class MainWindow(QMainWindow):
    """Main application window.

    Shows a minimal shell with an active-project indicator that initially
    displays "No project".
    """

    def __init__(self) -> None:
        super().__init__()
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
