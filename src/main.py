"""Application entry point for the astronomy research application."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from src.config_provider import ConfigProvider
from src.main_window import MainWindow
from src.project_repository import ProjectRepository
from src.project_service import ProjectService


def main() -> int:
    """Launch the application and return the Qt exit code."""
    app = QApplication(sys.argv)

    config_provider = ConfigProvider()
    repository = ProjectRepository(config_provider.get_projects_root())
    service = ProjectService(config_provider, repository)

    window = MainWindow(service=service)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
