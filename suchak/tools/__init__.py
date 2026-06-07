"""
Suchak Tools
============
Factory helpers for creating a registry of built-in tools.
"""

from pathlib import Path

from suchak.tools.list_files import ListFilesTool
from suchak.tools.read_file import ReadFileTool
from suchak.tools.registry import ToolRegistry


def create_registry(workspace_dir: str | Path) -> ToolRegistry:
    """
    Create a tool registry with all built-in tools registered.

    Args:
        workspace_dir: Directory that filesystem tools are allowed to access.

    Returns:
        A ToolRegistry containing Suchak's built-in tools.
    """
    registry = ToolRegistry()
    registry.register(ListFilesTool(workspace_dir))
    registry.register(ReadFileTool(workspace_dir))
    return registry


__all__ = ["ToolRegistry", "create_registry"]
