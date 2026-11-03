"""New Project dialog for creating research projects.

Collects a project name and optional location, then returns them when the
user accepts. Does not perform creation itself; the caller (typically a
ProjectService) handles persistence.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QDialogButtonBox,
    QFileDialog,
)


class NewProjectDialog(QDialog):
    """Dialog for creating a new research project.

    The caller is responsible for calling :meth:`project_name` and
    :meth:`project_location` after :meth:`exec` returns ``Accepted``.
    """

    def __init__(
        self,
        default_location: str = "",
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("New Project")
        self.resize(520, 220)

        layout = QVBoxLayout(self)

        # Project name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Project name:"))
        self._name_edit = QLineEdit()
        self._name_edit.setPlaceholderText("Enter project name")
        name_layout.addWidget(self._name_edit)
        layout.addLayout(name_layout)

        # Location
        location_layout = QHBoxLayout()
        location_layout.addWidget(QLabel("Location:"))
        self._location_edit = QLineEdit(default_location)
        self._location_edit.setReadOnly(True)
        self._browse_button = QPushButton("Browse...")
        self._browse_button.clicked.connect(self._browse_location)
        location_layout.addWidget(self._location_edit)
        location_layout.addWidget(self._browse_button)
        layout.addLayout(location_layout)

        # Buttons
        self._button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        self._button_box.accepted.connect(self.accept)
        self._button_box.rejected.connect(self.reject)
        layout.addWidget(self._button_box)

        self._create_button = self._button_box.button(
            QDialogButtonBox.StandardButton.Ok
        )
        self._create_button.setText("Create")
        self._create_button.setEnabled(False)
        self._name_edit.textChanged.connect(self._validate_name)

    def _validate_name(self, text: str) -> None:
        """Enable the Create button only when the name is non-empty."""
        self._create_button.setEnabled(bool(text.strip()))

    def _browse_location(self) -> None:
        """Open a folder picker to choose the project location."""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Project Location",
            self._location_edit.text() or "",
        )
        if folder:
            self._location_edit.setText(folder)

    def project_name(self) -> str:
        """Return the entered project name (stripped)."""
        return self._name_edit.text().strip()

    def project_location(self) -> str:
        """Return the selected location, or empty string for default."""
        return self._location_edit.text().strip()
