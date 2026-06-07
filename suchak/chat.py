"""
Chat Loop
=========
Runs the interactive prompt-response loop in the terminal.
"""

from pathlib import Path
import shlex

from suchak.config import APP_NAME, APP_VERSION, DEFAULT_MODEL, WORKSPACE_DIR
from suchak import client
from suchak.tools import create_registry
from suchak.tools.registry import ToolRegistry


def handle_tool_command(
    command: str,
    tool_registry: ToolRegistry,
    model: str = DEFAULT_MODEL,
) -> str:
    """
    Execute a direct CLI tool command without sending it to the LLM.
    """
    try:
        parts = shlex.split(command)
    except ValueError as err:
        return f"Error: could not parse command: {err}"

    if not parts:
        return "Error: empty command."

    name = parts[0]
    args = parts[1:]

    if name == "/tools":
        tools = tool_registry.list_tools()
        if not tools:
            return "No tools available."
        return "\n".join(f"{tool['name']}: {tool['description']}" for tool in tools)

    if name == "/list_files":
        return _handle_list_files(args, tool_registry)

    if name == "/read_file":
        return _handle_read_file(args, tool_registry)

    if name == "/summarize":
        return _handle_summarize(args, tool_registry, model)

    return f"Error: unknown command: {name}"


def _handle_list_files(args: list[str], tool_registry: ToolRegistry) -> str:
    path = "."
    recursive = False
    paths = []

    for arg in args:
        if arg in ("-r", "--recursive"):
            recursive = True
        elif arg.startswith("-"):
            return f"Error: unknown option for /list_files: {arg}"
        else:
            paths.append(arg)

    if len(paths) > 1:
        return "Error: /list_files accepts at most one path."

    if paths:
        path = paths[0]

    return tool_registry.execute("list_files", path=path, recursive=recursive)


def _handle_read_file(args: list[str], tool_registry: ToolRegistry) -> str:
    if len(args) != 1:
        return "Usage: /read_file <path>"

    return tool_registry.execute("read_file", path=args[0])


def _handle_summarize(
    args: list[str],
    tool_registry: ToolRegistry,
    model: str,
) -> str:
    if len(args) != 1:
        return "Usage: /summarize <path>"

    path = args[0]
    contents = tool_registry.execute("read_file", path=path)
    if contents.startswith("Error:"):
        return contents

    prompt = (
        "Summarize this file clearly and concisely.\n\n"
        f"File: {path}\n\n"
        "Content:\n"
        f"{contents}"
    )
    return client.generate(prompt, model=model)


def start(model: str = DEFAULT_MODEL, workspace_dir: str | Path = WORKSPACE_DIR) -> None:
    """
    Launch the interactive chat session.

    Args:
        model: The Ollama model to use for generation.
        workspace_dir: Directory that sandboxed tools are allowed to access.
    """
    workspace_path = Path(workspace_dir).resolve()
    workspace_path.mkdir(parents=True, exist_ok=True)
    tool_registry = create_registry(workspace_path)

    print(f"\n  {APP_NAME} v{APP_VERSION}")
    print(f"  Model: {model}")
    print(f"  Workspace: {workspace_path}")
    print("  Tools:")
    for tool in tool_registry.list_tools():
        print(f"    - {tool['name']}: {tool['description']}")
    print("  Type 'exit' or 'quit' to end the session.\n")
    print("-" * 50)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("\nGoodbye!")
            break

        if user_input.startswith("/"):
            result = handle_tool_command(user_input, tool_registry, model=model)
            print(f"\n{APP_NAME}: {result}")
            continue

        try:
            response = client.generate(user_input, model=model)
            print(f"\n{APP_NAME}: {response}")
        except ConnectionError as err:
            print(f"\n[Connection Error] {err}")
        except RuntimeError as err:
            print(f"\n[Error] {err}")
