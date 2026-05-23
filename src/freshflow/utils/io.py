"""Configuration loading and path resolution from configs/config.yaml."""

from pathlib import Path
from typing import Any


def load_config(config_path: Path | None = None) -> dict[str, Any]:
    """Load project configuration from YAML.

    Args:
        config_path: Path to config.yaml. If None, resolves to project configs/.

    Returns:
        Parsed configuration dictionary.
    """
    raise NotImplementedError("load_config is not yet implemented")


def resolve_path(key: str, config: dict[str, Any] | None = None) -> Path:
    """Resolve a data or output path from config paths section.

    Args:
        key: Key under paths (e.g., 'raw', 'processed', 'reports_figures').
        config: Optional pre-loaded config; loads from file if None.

    Returns:
        Absolute or project-relative Path.
    """
    raise NotImplementedError("resolve_path is not yet implemented")


def ensure_dir(path: Path) -> Path:
    """Create directory if missing and return the path.

    Args:
        path: Directory to create.

    Returns:
        The same path after creation.
    """
    raise NotImplementedError("ensure_dir is not yet implemented")
