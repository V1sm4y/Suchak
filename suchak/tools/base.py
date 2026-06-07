"""
Base Tool Interface
===================
Abstract base class that all Suchak tools must implement.
Enforces a consistent contract: every tool has a name, description,
parameter schema, and an execute method.
"""

from abc import ABC, abstractmethod


class Tool(ABC):
    """
    Abstract base for all tools in the Suchak agent.

    Subclasses must set `name` and `description` as class attributes
    and implement the `execute` method.
    """

    name: str = ""
    description: str = ""

    @abstractmethod
    def execute(self, **kwargs) -> str:
        """
        Run the tool with the given keyword arguments.

        Args:
            **kwargs: Tool-specific parameters.

        Returns:
            A string containing the tool's output or error message.
        """

    def schema(self) -> dict:
        """
        Return a dictionary describing the tool's expected parameters.

        Returns:
            A dict with keys:
                - name: The tool's name.
                - description: What the tool does.
                - parameters: A list of dicts, each with:
                    - name: Parameter name.
                    - type: Parameter type (e.g. "str", "int").
                    - required: Whether the parameter is required.
                    - description: What the parameter is for.
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": [],
        }
