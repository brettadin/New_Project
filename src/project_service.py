"""Project lifecycle service for the astronomy research application.

Orchestrates project creation by coordinating the project model, repository,
and configuration provider. Keeps UI and persistence concerns separate so the
service layer can be tested without PySide6.
"""

from __future__ import annotations

from unittest.mock import patch

from src.config_provider import ConfigProvider
from src.project_model import ProjectMetadata, ProjectValidationError
from src.project_repository import ProjectRepository


class ProjectCreationError(Exception):
    """Raised when a project cannot be created."""


class ProjectService:
    """Coordinates project creation and lifecycle operations.

    Responsibilities:
    - Validate project names before any filesystem operation
    - Create ProjectMetadata instances with generated UUIDs
    - Persist projects through the repository
    - Track the currently active project
    - Clean up only the incomplete directory created by a failed save
    """

    def __init__(
        self,
        config_provider: ConfigProvider,
        repository: ProjectRepository | None = None,
    ) -> None:
        self.config_provider = config_provider
        self._default_repository = repository
        self._active_project: ProjectMetadata | None = None

    @property
    def active_project(self) -> ProjectMetadata | None:
        """The currently active project, or None if no project is open."""
        return self._active_project

    @property
    def default_location(self) -> str:
        """The default projects root from the configuration provider."""
        return self.config_provider.get_projects_root()

    def _repository_for(self, location: str) -> ProjectRepository:
        """Return a repository scoped to the given location."""
        return ProjectRepository(location)

    def create_project(
        self, name: str, location: str | None = None
    ) -> ProjectMetadata:
        """Create a new research project.

        Args:
            name: User-visible project name.
            location: Optional projects root directory. If omitted or empty,
                the default location from the configuration provider is used.

        Returns:
            The created and saved ProjectMetadata.

        Raises:
            ProjectValidationError: if the name is invalid.
            ProjectCreationError: if creation fails or the project directory
                already exists.
        """
        # Validate name before any filesystem operation.
        ProjectMetadata.validate_name(name)

        root = location or self.default_location

        # Generate metadata with a fresh UUID.
        metadata = ProjectMetadata.create(name)

        # Defensive: never overwrite an existing project directory.
        repo = self._repository_for(root)
        if repo.project_exists(metadata.project_id):
            raise ProjectCreationError(
                f"Project directory already exists: {metadata.project_id}"
            )

        try:
            repo.save(metadata)
        except Exception as exc:
            # Clean up only the incomplete directory created by this operation.
            self._cleanup_incomplete_directory(repo, metadata.project_id)
            raise ProjectCreationError(
                f"Failed to create project '{name}': {exc}"
            ) from exc

        self._active_project = metadata
        return metadata

    @staticmethod
    def _cleanup_incomplete_directory(
        repo: ProjectRepository, project_id: str
    ) -> None:
        """Remove the incomplete project directory created by a failed save.

        Only removes artifacts created by this operation. Never touches
        existing projects or their files.
        """
        project_dir = repo.project_dir(project_id)
        project_file = repo.project_path(project_id)

        # Remove the metadata file if it was partially written.
        if project_file.exists():
            try:
                project_file.unlink()
            except OSError:
                pass

        # Remove the directory only if it is empty.
        if project_dir.exists() and project_dir.is_dir():
            try:
                project_dir.rmdir()
            except OSError:
                pass

    def set_active_project(self, metadata: ProjectMetadata | None) -> None:
        """Set the active project (called by the UI layer)."""
        self._active_project = metadata
