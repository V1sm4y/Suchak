"""
Suchak Configuration
====================
Central configuration constants for the Suchak CLI application.
Modify values here to change the default model, API endpoint, or app behavior.
"""

from pathlib import Path

# Ollama API settings
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_API_ENDPOINT = f"{OLLAMA_BASE_URL}/api/generate"

# Default model to use for text generation
DEFAULT_MODEL = "mistral"

# Application metadata
APP_NAME = "Suchak"
APP_VERSION = "1.0.0"

# Default workspace for sandboxed tools
WORKSPACE_DIR = Path("./workspace")

# System prompt — defines Suchak's persona and capabilities
SYSTEM_PROMPT = (
    "You are Suchak.\n\n"
    "You are an AI security assistant.\n\n"
    "Your purpose is to help with:\n"
    "- reconnaissance\n"
    "- attack surface analysis\n"
    "- security workflows\n"
    "- cloud security\n"
    "- penetration testing assistance\n\n"
    "You refer to yourself as Suchak.\n\n"
    "Be concise and practical."
)
