# Suchak

Suchak is a minimal CLI security assistant powered by a local Ollama model.

It started as a chatbot and is now growing into an agent with a small, sandboxed
tool system.

## Current Features

- Chat with a local Ollama model.
- Register and expose tools through a central tool registry.
- Read files only from a configured workspace directory.
- List files only from a configured workspace directory.
- Summarize workspace files by chaining a tool result into the LLM.

## Requirements

- Python 3.11+
- Ollama running locally
- A local model such as `mistral`

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Make sure Ollama is running:

```bash
ollama serve
```

Pull the default model if needed:

```bash
ollama pull mistral
```

## Run

```bash
python main.py
```

Use a different model:

```bash
python main.py --model mistral
```

Use a different workspace directory:

```bash
python main.py --workspace ./workspace
```

## Workspace Sandbox

Suchak tools do not have arbitrary filesystem access.

Filesystem tools are limited to the configured workspace directory. By default:

```text
./workspace
```

Absolute paths are rejected. Path traversal attempts such as `../main.py` are
also rejected.

## Commands

Inside the Suchak CLI, regular messages are sent to the LLM.

Slash commands run direct tool workflows.

### List Tools

```text
/tools
```

Shows available tools.

### List Files

```text
/list_files
/list_files notes
/list_files --recursive
/list_files notes --recursive
```

Lists files inside the workspace.

### Read File

```text
/read_file hello.txt
/read_file notes/todo.txt
```

Reads a UTF-8 text file from the workspace.

### Summarize File

```text
/summarize hello.txt
```

Runs the first tool plus LLM workflow:

```text
read_file -> file contents -> Ollama model -> summary
```

## Tool Architecture

Tools live in:

```text
suchak/tools/
```

Current tool files:

```text
base.py        # abstract Tool interface
registry.py    # ToolRegistry for registering/listing/executing tools
read_file.py   # sandboxed file reader
list_files.py  # sandboxed file lister
__init__.py    # creates the default built-in registry
```

Every tool implements:

```python
name: str
description: str
execute(**kwargs) -> str
schema() -> dict
```

## Project Structure

```text
.
├── main.py
├── requirements.txt
├── workspace/
│   └── .gitkeep
└── suchak/
    ├── __init__.py
    ├── chat.py
    ├── client.py
    ├── config.py
    └── tools/
        ├── __init__.py
        ├── base.py
        ├── registry.py
        ├── read_file.py
        └── list_files.py
```

## Status

Suchak currently supports direct command-driven tool use and one simple
tool-plus-LLM workflow. The next milestone is letting the model choose and call
tools automatically.
