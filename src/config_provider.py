"""Configuration provider for the astronomy research application.

Determines the projects root location. The location is configurable without
changing application source code through:

1. The ``ASTRONOMY_PROJECTS_ROOT`` environment variable (highest priority).
2. A JSON config file at ``~/.astronomy_research_app/config.json``.
3. The built-in default: %USERPROFILE%\\Documents\\AstronomyProjects.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

ENV_VAR_NAME = "ASTRONOMY_PROJECTS_ROOT"
DEFAULT_PROJECTS_ROOT = str(Path.home() / "Documents" / "AstronomyProjects")
DEFAULT_CONFIG_PATH = Path.home() / ".astronomy_research_app" / "config.json"


class ConfigProvider:
    """Resolves and (optionally) persists the projects root directory."""

    def __init__(self, config_path: str | Path | None = None) -> None:
        self._config_path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
        self._projects_root: str | None = None

    def get_projects_root(self) -> str:
        """Return the projects root directory path.

        Resolution order:
          1. ``ASTRONOMY_PROJECTS_ROOT`` environment variable.
          2. Value previously set via :meth:`set_projects_root`.
          3. Value stored in the config file.
          4. Built-in default.
        """
        env_root = os.environ.get(ENV_VAR_NAME)
        if env_root:
            return env_root

        if self._projects_root is not None:
            return self._projects_root

        if self._config_path.exists():
            try:
                with open(self._config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                root = config.get("projects_root")
                if isinstance(root, str) and root:
                    self._projects_root = root
                    return root
            except (json.JSONDecodeError, OSError):
                # Fall through to default if config file is unreadable.
                pass

        return DEFAULT_PROJECTS_ROOT

    def set_projects_root(self, root: str) -> None:
        """Set the projects root in memory (not persisted to disk)."""
        self._projects_root = root

    def save_config(self, root: str) -> None:
        """Persist the projects root to the config file.

        Creates the config directory if needed. Does not change the
        projects root itself; call :meth:`set_projects_root` for that.
        """
        self._config_path.parent.mkdir(parents=True, exist_ok=True)
        config = {"projects_root": root}
        tmp_fd, tmp_path = None, None
        try:
            tmp_fd, tmp_path = self._atomic_write_json(self._config_path, config)
        finally:
            if tmp_fd is not None:
                try:
                    os.close(tmp_fd)
                except OSError:
                    pass
            if tmp_path is not None:
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass
        self._projects_root = root

    @staticmethod
    def _atomic_write_json(path: Path, config: dict) -> tuple[int | None, str | None]:
        """Write JSON config atomically using temp file + replace.

        Returns the temp file descriptor and path (caller is responsible
        for cleanup if this helper raises before replacing).
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = __import__("tempfile").mkstemp(
            dir=str(path.parent), suffix=".tmp"
        )
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
        return fd, tmp_path
