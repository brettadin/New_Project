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

SCHEMA_VERSION = 2
VALID_STATUSES = ("Active", "Paused", "Completed", "Archived")

# Characters not allowed in project names (filesystem-safe).
_INVALID_NAME_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
_MAX_NAME_LENGTH = 100

# Required permission roles for schema version 2. Each role grants the local
# user by default in the single-user deployment.
_REQUIRED_ROLES = ("view", "contribute", "manage")
_DEFAULT_OWNER = "local_user"


def _default_roles() -> dict[str, list[str]]:
    """Return the default roles mapping for a new project.

    Each call returns an independent dictionary and independent lists so
    that no mutable state is shared between projects.
    """
    return {
        "view": [_DEFAULT_OWNER],
        "contribute": [_DEFAULT_OWNER],
        "manage": [_DEFAULT_OWNER],
    }


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
        owner: Identifier of the project owner. Defaults to "local_user"
            for single-user local deployment.
        roles: Mapping of role name to a list of principal IDs. Defaults
            to view/contribute/manage, each containing "local_user".
        is_dirty: True if in-memory metadata has changed since last save.
    """

    project_id: str
    name: str
    created_at: str
    status: str = "Active"
    schema_version: int = SCHEMA_VERSION
    external_data_references: list = field(default_factory=list)
    owner: str = "local_user"
    roles: dict[str, list[str]] = field(default_factory=_default_roles)
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
            owner=_DEFAULT_OWNER,
            roles=_default_roles(),
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
        if (
            not isinstance(metadata.schema_version, int)
            or isinstance(metadata.schema_version, bool)
            or metadata.schema_version < 1
        ):
            raise ProjectValidationError("Schema version must be a positive integer.")
        if metadata.schema_version > SCHEMA_VERSION:
            raise ProjectValidationError(
                f"Unsupported schema version {metadata.schema_version}. "
                f"Maximum supported version is {SCHEMA_VERSION}."
            )
        cls.validate_owner(metadata.owner)
        cls.validate_roles(metadata.roles)

    @classmethod
    def validate_owner(cls, owner: str) -> None:
        """Validate the owner field."""
        if not isinstance(owner, str):
            raise ProjectValidationError("Owner must be a string.")
        if not owner.strip():
            raise ProjectValidationError("Owner must not be empty or whitespace-only.")

    @classmethod
    def validate_roles(cls, roles: dict[str, list[str]]) -> None:
        """Validate the roles field structure and contents."""
        if not isinstance(roles, dict):
            raise ProjectValidationError("Roles must be a dictionary.")
        for role in _REQUIRED_ROLES:
            if role not in roles:
                raise ProjectValidationError(f"Roles must contain '{role}' role.")
        for role_name, principals in roles.items():
            if not isinstance(role_name, str):
                raise ProjectValidationError("Role names must be strings.")
            if not isinstance(principals, list):
                raise ProjectValidationError(
                    f"Role '{role_name}' value must be a list."
                )
            for principal in principals:
                if not isinstance(principal, str):
                    raise ProjectValidationError("Principal IDs must be strings.")
                if not principal.strip():
                    raise ProjectValidationError(
                        "Principal IDs must not be empty or whitespace-only."
                    )

    def mark_dirty(self) -> None:
        """Mark the metadata as having unsaved changes."""
        self.is_dirty = True

    def mark_clean(self) -> None:
        """Mark the metadata as saved (no unsaved changes)."""
        self.is_dirty = False

    def set_name(self, name: str) -> None:
        """Change the project name and mark the project dirty.

        Assigning an unchanged value does not mark the project dirty.
        Raises :exc:`ProjectValidationError` if the name is invalid.
        """
        stripped = name.strip()
        if stripped == self.name:
            return
        self.validate_name(stripped)
        self.name = stripped
        self.mark_dirty()

    def set_status(self, status: str) -> None:
        """Change the project status and mark the project dirty.

        Assigning an unchanged value does not mark the project dirty.
        Raises :exc:`ProjectValidationError` if the status is invalid.
        """
        if status == self.status:
            return
        if status not in VALID_STATUSES:
            raise ProjectValidationError(
                f"Status must be one of: {', '.join(VALID_STATUSES)}"
            )
        self.status = status
        self.mark_dirty()

    def to_dict(self) -> dict:
        """Serialize metadata to a JSON-compatible dictionary."""
        return {
            "project_id": self.project_id,
            "name": self.name,
            "created_at": self.created_at,
            "status": self.status,
            "schema_version": self.schema_version,
            "external_data_references": self.external_data_references,
            "owner": self.owner,
            "roles": {
                role: list(principals) for role, principals in self.roles.items()
            },
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ProjectMetadata":
        """Deserialize metadata from a dictionary.

        Schema version 1 metadata is migrated in memory to version 2:
        missing owner/roles are filled with defaults and the in-memory
        schema_version is upgraded. Migration does not modify the source
        dictionary or any file.

        Schema version 2 metadata must contain both owner and roles;
        missing fields are rejected outright. Schema versions greater than
        2 are rejected.

        A freshly loaded instance is clean (not dirty).
        """
        raw_version = data.get("schema_version")

        if raw_version is None:
            # Legacy metadata with no schema version: treat as version 1.
            schema_version = 1
        elif (
            not isinstance(raw_version, int)
            or isinstance(raw_version, bool)
            or raw_version < 1
        ):
            raise ProjectValidationError("Schema version must be a positive integer.")
        elif raw_version > SCHEMA_VERSION:
            raise ProjectValidationError(
                f"Unsupported schema version {raw_version}. "
                f"Maximum supported version is {SCHEMA_VERSION}."
            )
        else:
            schema_version = raw_version

        def _copy_roles(roles_source):
            """Return an independent copy of a roles mapping."""
            return {
                role: list(principals) for role, principals in roles_source.items()
            }

        if schema_version == 1:
            # Version 1 migration: apply defaults only when fields are absent.
            owner = data.get("owner", _DEFAULT_OWNER)
            roles_source = data.get("roles")
            roles = _default_roles() if roles_source is None else _copy_roles(roles_source)
        else:
            # Version 2: owner and roles are required; defaults must not
            # conceal missing fields.
            if "owner" not in data:
                raise ProjectValidationError(
                    "Version 2 metadata must contain 'owner'."
                )
            if "roles" not in data:
                raise ProjectValidationError(
                    "Version 2 metadata must contain 'roles'."
                )
            owner = data["owner"]
            roles = _copy_roles(data["roles"])

        metadata = cls(
            project_id=data["project_id"],
            name=data["name"],
            created_at=data["created_at"],
            status=data.get("status", "Active"),
            schema_version=SCHEMA_VERSION,
            external_data_references=data.get("external_data_references", []),
            owner=owner,
            roles=roles,
            is_dirty=False,
        )
        cls.validate(metadata)
        return metadata
