"""
Read File Tool
==============
Reads files from a configured workspace directory only.
"""

from pathlib import Path

from suchak.tools.base import Tool


class ReadFileTool(Tool):
    """
    Tool for reading text files inside a workspace directory.

    The tool rejects absolute paths and traversal attempts that would escape
    the workspace.
    """

    name = "read_file"
    description = "Read a text file from the configured workspace directory."

    def __init__(self, workspace_dir: str | Path) -> None:
        self.workspace_dir = Path(workspace_dir).resolve()

    def execute(self, **kwargs) -> str:
        path = kwargs.get("path")
        if not path or not isinstance(path, str):
            return "Error: 'path' is required and must be a string."

        requested_path = Path(path)
        if requested_path.is_absolute():
            return "Error: absolute paths are not allowed."

        resolved_path = (self.workspace_dir / requested_path).resolve()
        if not self._is_inside_workspace(resolved_path):
            return "Error: path is outside the workspace."

        if not resolved_path.exists():
            return f"Error: file not found: {path}"

        if not resolved_path.is_file():
            return f"Error: path is not a file: {path}"

        try:
            return resolved_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return f"Error: file is not valid UTF-8 text: {path}"
        except OSError as err:
            return f"Error: could not read file: {err}"

    def schema(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": [
                {
                    "name": "path",
                    "type": "str",
                    "required": True,
                    "description": "Relative path to a file inside the workspace.",
                }
            ],
        }

    def _is_inside_workspace(self, path: Path) -> bool:
        return path == self.workspace_dir or self.workspace_dir in path.parents
