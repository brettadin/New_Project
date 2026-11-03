"""Project repository for provisional local-file project persistence.

Each project is stored as a directory under the projects root, named by its
stable ``project_id``, containing a single ``project.json`` metadata file.

Metadata writes are atomic: the JSON is written to a temporary file in the
same directory, then atomically replaced over the target. This ensures that
a failed or interrupted write never leaves a corrupted or partially written
``project.json`` in place of the previous valid metadata.

Original external data files are never modified, moved, or copied by this
repository; only references to them are preserved in ``project.json``.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

from src.project_model import ProjectMetadata, ProjectValidationError


class ProjectRepositoryError(Exception):
    """Base exception for repository errors."""


class ProjectNotFoundError(ProjectRepositoryError):
    """Raised when a project's metadata file does not exist."""


class ProjectCorruptedError(ProjectRepositoryError):
    """Raised when a project's metadata file is missing, malformed, or invalid."""


class ProjectRepository:
    """Reads and writes project metadata to the local file system."""

    def __init__(self, projects_root: str | Path) -> None:
        self.projects_root = Path(projects_root)

    # ------------------------------------------------------------------
    # Path helpers
    # ------------------------------------------------------------------

    def project_dir(self, project_id: str) -> Path:
        """Return the directory for a project, identified by project_id."""
        return self.projects_root / project_id

    def project_path(self, project_id: str) -> Path:
        """Return the path to a project's ``project.json`` file."""
        return self.project_dir(project_id) / "project.json"

    # ------------------------------------------------------------------
    # Persistence operations
    # ------------------------------------------------------------------

    def save(self, metadata: ProjectMetadata) -> None:
        """Persist project metadata to ``project.json``.

        Validates metadata before any file system operation. Writes
        atomically so a failed write never corrupts existing metadata.
        Marks the metadata as clean after a successful save.
        """
        ProjectMetadata.validate(metadata)

        project_dir = self.project_dir(metadata.project_id)
        project_dir.mkdir(parents=True, exist_ok=True)

        project_file = self.project_path(metadata.project_id)
        self._write_json_atomic(project_file, metadata.to_dict())
        metadata.mark_clean()

    def load(self, project_id: str) -> ProjectMetadata:
        """Load and validate project metadata from ``project.json``.

        Raises:
            ProjectNotFoundError: if the metadata file does not exist.
            ProjectCorruptedError: if the file is missing, malformed JSON,
                or fails validation.
            ProjectRepositoryError: if the file cannot be read.
        """
        project_file = self.project_path(project_id)

        if not project_file.exists():
            raise ProjectNotFoundError(
                f"Project metadata not found: {project_file}"
            )

        try:
            with open(project_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as exc:
            raise ProjectCorruptedError(
                f"Malformed project metadata: {project_file}"
            ) from exc
        except OSError as exc:
            raise ProjectRepositoryError(
                f"Cannot read project metadata: {project_file}"
            ) from exc

        try:
            metadata = ProjectMetadata.from_dict(data)
            ProjectMetadata.validate(metadata)
        except (KeyError, TypeError, ValueError) as exc:
            raise ProjectCorruptedError(
                f"Invalid project metadata: {project_file}"
            ) from exc

        return metadata

    def _write_json_atomic(self, path: Path, data: dict) -> None:
        """Write JSON to a temp file in the same directory, then replace.

        The temp file is created in the target directory so that
        ``os.replace`` is atomic (same file system). If any step fails,
        the original file is left untouched.
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(
            dir=str(path.parent), suffix=".tmp"
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, path)
        except BaseException:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise

    # ------------------------------------------------------------------
    # Query operations
    # ------------------------------------------------------------------

    def project_exists(self, project_id: str) -> bool:
        """Return True if a project's metadata file exists."""
        return self.project_path(project_id).exists()

    def list_projects(self) -> list[str]:
        """Return sorted project IDs that have a ``project.json`` file.

        Returns an empty list if the projects root does not exist.
        Does not validate metadata content; corrupted projects are still
        listed (validation happens at load time).
        """
        if not self.projects_root.exists():
            return []
        project_ids = []
        for entry in self.projects_root.iterdir():
            if entry.is_dir() and (entry / "project.json").exists():
                project_ids.append(entry.name)
        return sorted(project_ids)
