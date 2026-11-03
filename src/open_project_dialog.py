"""Open Project dialog for selecting and opening existing projects.

Displays discovered projects with name and status, and provides a
folder-picker for opening projects from custom locations.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QFileDialog,
    QMessageBox,
)

from src.project_model import ProjectMetadata


class OpenProjectDialog(QDialog):
    """Dialog for selecting and opening an existing project.

    Shows a list of discovered projects with their name and status.
    The user can select a project and click Open, choose a custom
    folder via "Open from Folder...", or Cancel.

    After acceptance, call :meth:`selected_project_id` for a project
    selected from the list, or :meth:`custom_location` for a folder
    chosen via "Open from Folder...".
    """

    def __init__(
        self,
        projects: list[ProjectMetadata] | None = None,
        invalid_dirs: list[str] | None = None,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Open Project")
        self.resize(600, 400)

        layout = QVBoxLayout(self)

        # Project list
        layout.addWidget(QLabel("Available projects:"))
        self._project_list = QListWidget()
        self._project_list.itemSelectionChanged.connect(
            self._on_selection_changed
        )
        for project in projects or []:
            item = QListWidgetItem(f"{project.name} ({project.status})")
            item.setData(Qt.ItemDataRole.UserRole, project.project_id)
            self._project_list.addItem(item)
        layout.addWidget(self._project_list)

        # Show warning about invalid directories if any
        if invalid_dirs:
            names = ", ".join(invalid_dirs)
            QMessageBox.warning(
                self,
                "Invalid project directories skipped",
                (
                    "The following directories could not be opened as "
                    f"projects (missing or invalid project.json): {names}"
                ),
            )

        # Buttons
        button_layout = QHBoxLayout()
        self._open_button = QPushButton("Open")
        self._open_button.setEnabled(False)
        self._open_button.clicked.connect(self.accept)
        self._browse_button = QPushButton("Open from Folder...")
        self._browse_button.clicked.connect(self._browse_folder)
        self._cancel_button = QPushButton("Cancel")
        self._cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self._open_button)
        button_layout.addWidget(self._browse_button)
        button_layout.addStretch()
        button_layout.addWidget(self._cancel_button)
        layout.addLayout(button_layout)

        self._selected_project_id: str | None = None
        self._custom_location: str | None = None

    def _on_selection_changed(self) -> None:
        items = self._project_list.selectedItems()
        self._open_button.setEnabled(bool(items))
        if items:
            self._selected_project_id = items[0].data(
                Qt.ItemDataRole.UserRole
            )
        else:
            self._selected_project_id = None

    def _browse_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(
            self, "Select Project Folder", str(Path.home())
        )
        if folder:
            self._custom_location = folder
            self.accept()

    def selected_project_id(self) -> str | None:
        """Return the selected project ID, or None if none selected."""
        return self._selected_project_id

    def custom_location(self) -> str | None:
        """Return the custom folder path, or None if none chosen."""
        return self._custom_location
