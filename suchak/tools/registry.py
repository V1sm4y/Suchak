"""
Tool Registry
==============
Central registry for discovering, listing, and dispatching tools.
Tools register themselves here and can be looked up by name.
"""

from suchak.tools.base import Tool


class ToolRegistry:
    """
    Manages a collection of Tool instances.

    Provides registration, lookup, listing, and execution of tools
    through a single unified interface.
    """

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """
        Register a tool instance.

        Args:
            tool: A Tool subclass instance to register.

        Raises:
            ValueError: If a tool with the same name is already registered.
        """
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered.")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        """
        Look up a tool by name.

        Args:
            name: The unique tool identifier.

        Returns:
            The Tool instance, or None if not found.
        """
        return self._tools.get(name)

    def list_tools(self) -> list[dict]:
        """
        Return a summary of all registered tools.

        Returns:
            A list of dicts, each containing 'name' and 'description'.
        """
        return [
            {"name": t.name, "description": t.description}
            for t in self._tools.values()
        ]

    def execute(self, name: str, **kwargs) -> str:
        """
        Look up a tool by name and execute it.

        Args:
            name:     The tool name to execute.
            **kwargs: Arguments passed to the tool's execute method.

        Returns:
            The string result from the tool.

        Raises:
            KeyError: If no tool with the given name is registered.
        """
        tool = self._tools.get(name)
        if tool is None:
            raise KeyError(f"Unknown tool: '{name}'")
        return tool.execute(**kwargs)
