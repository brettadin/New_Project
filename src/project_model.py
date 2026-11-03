"""Project metadata model for the astronomy research application.

Defines the minimal project metadata schema, validation rules, project ID
generation, and dirty-state tracking for Subtask 2.1.1.

The model is intentionally free of UI and persistence concerns so it can be
unit-tested independently of PySide6 and the file system.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

SCHEMA_VERSION = 1
VALID_STATUSES = ("Active", "Paused", "Completed", "Archived")

# Characters not allowed in project names (filesystem-safe).
_INVALID_NAME_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
_MAX_NAME_LENGTH = 100


class ProjectValidationError(ValueError):
    """Raised when project metadata fails validation."""


@dataclass
class ProjectMetadata:
    """Metadata describing a research project.

    Fields:
        project_id: Stable unique identifier (UUID). Used as the project
            directory name; never changes for the life of the project.
        name: User-visible project name. May be renamed without changing
            project_id.
        created_at: ISO-8601 timestamp of project creation.
        status: Lifecycle status. Defaults to "Active".
        schema_version: Version of the project.json metadata format.
            Distinct from the application version; incremented when the
            metadata structure changes.
        external_data_references: References to external data files used
            by the project (paths, provenance). Preserved even when the
            referenced file is not currently accessible.
        is_dirty: True if in-memory metadata has changed since last save.
    """

    project_id: str
    name: str
    created_at: str
    status: str = "Active"
    schema_version: int = SCHEMA_VERSION
    external_data_references: list = field(default_factory=list)
    is_dirty: bool = False

    @classmethod
    def create(cls, name: str) -> "ProjectMetadata":
        """Create a new project metadata instance with generated fields."""
        cls.validate_name(name)
        now = datetime.now(timezone.utc).isoformat()
        return cls(
            project_id=str(uuid.uuid4()),
            name=name,
            created_at=now,
            status="Active",
            schema_version=SCHEMA_VERSION,
            external_data_references=[],
            is_dirty=False,
        )

    @classmethod
    def validate_name(cls, name: str) -> None:
        """Validate a project name."""
        if not name or not name.strip():
            raise ProjectValidationError("Project name must not be empty.")
        if _INVALID_NAME_CHARS.search(name):
            raise ProjectValidationError(
                "Project name contains invalid characters."
            )
        if len(name.strip()) > _MAX_NAME_LENGTH:
            raise ProjectValidationError(
                f"Project name must not exceed {_MAX_NAME_LENGTH} characters."
            )

    @classmethod
    def validate(cls, metadata: "ProjectMetadata") -> None:
        """Validate all fields of a ProjectMetadata instance."""
        cls.validate_name(metadata.name)
        if not metadata.project_id:
            raise ProjectValidationError("Project ID must not be empty.")
        try:
            uuid.UUID(metadata.project_id)
        except ValueError:
            raise ProjectValidationError("Project ID must be a valid UUID.")
        if metadata.status not in VALID_STATUSES:
            raise ProjectValidationError(
                f"Status must be one of: {', '.join(VALID_STATUSES)}"
            )
        if not isinstance(metadata.schema_version, int) or metadata.schema_version < 1:
            raise ProjectValidationError("Schema version must be a positive integer.")

    def mark_dirty(self) -> None:
        """Mark the metadata as having unsaved changes."""
        self.is_dirty = True

    def mark_clean(self) -> None:
        """Mark the metadata as saved (no unsaved changes)."""
        self.is_dirty = False

    def to_dict(self) -> dict:
        """Serialize metadata to a JSON-compatible dictionary."""
        return {
            "project_id": self.project_id,
            "name": self.name,
            "created_at": self.created_at,
            "status": self.status,
            "schema_version": self.schema_version,
            "external_data_references": self.external_data_references,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ProjectMetadata":
        """Deserialize metadata from a dictionary.

        A freshly loaded instance is clean (not dirty).
        """
        return cls(
            project_id=data["project_id"],
            name=data["name"],
            created_at=data["created_at"],
            status=data.get("status", "Active"),
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            external_data_references=data.get("external_data_references", []),
            is_dirty=False,
        )
