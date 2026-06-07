"""
List Files Tool
===============
Lists files from a configured workspace directory only.
"""

from pathlib import Path

from suchak.tools.base import Tool


class ListFilesTool(Tool):
    """
    Tool for listing files inside a workspace directory.

    The tool rejects absolute paths and traversal attempts that would escape
    the workspace.
    """

    name = "list_files"
    description = "List files from the configured workspace directory."

    def __init__(self, workspace_dir: str | Path) -> None:
        self.workspace_dir = Path(workspace_dir).resolve()

    def execute(self, **kwargs) -> str:
        path = kwargs.get("path", ".")
        recursive = kwargs.get("recursive", False)

        if not isinstance(path, str):
            return "Error: 'path' must be a string."

        if not isinstance(recursive, bool):
            return "Error: 'recursive' must be a boolean."

        requested_path = Path(path)
        if requested_path.is_absolute():
            return "Error: absolute paths are not allowed."

        resolved_path = (self.workspace_dir / requested_path).resolve()
        if not self._is_inside_workspace(resolved_path):
            return "Error: path is outside the workspace."

        if not resolved_path.exists():
            return f"Error: directory not found: {path}"

        if not resolved_path.is_dir():
            return f"Error: path is not a directory: {path}"

        pattern = "**/*" if recursive else "*"
        files = sorted(
            item.relative_to(self.workspace_dir).as_posix()
            for item in resolved_path.glob(pattern)
            if item.is_file()
        )

        if not files:
            return "No files found."

        return "\n".join(files)

    def schema(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": [
                {
                    "name": "path",
                    "type": "str",
                    "required": False,
                    "description": "Relative directory path inside the workspace.",
                },
                {
                    "name": "recursive",
                    "type": "bool",
                    "required": False,
                    "description": "Whether to include files in nested directories.",
                },
            ],
        }

    def _is_inside_workspace(self, path: Path) -> bool:
        return path == self.workspace_dir or self.workspace_dir in path.parents
