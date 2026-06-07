"""
Ollama API Client
=================
Handles communication with the local Ollama instance.
Sends prompts and returns generated text responses.
"""

import json

import requests

from suchak.config import OLLAMA_API_ENDPOINT, DEFAULT_MODEL, SYSTEM_PROMPT


def generate(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """
    Send a prompt to the Ollama API and return the full generated response.

    Args:
        prompt: The user's input text.
        model:  The model name to use (defaults to config.DEFAULT_MODEL).

    Returns:
        The complete generated text as a single string.

    Raises:
        ConnectionError: If Ollama is not reachable.
        RuntimeError:    If the API returns a non-200 status or an error payload.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "system": SYSTEM_PROMPT,
        "stream": False,
    }

    try:
        response = requests.post(OLLAMA_API_ENDPOINT, json=payload, timeout=120)
    except requests.ConnectionError:
        raise ConnectionError(
            "Could not connect to Ollama. "
            "Make sure it is running at http://localhost:11434"
        )
    except requests.Timeout:
        raise RuntimeError("Request to Ollama timed out. Try a shorter prompt or check the server.")

    if response.status_code != 200:
        raise RuntimeError(
            f"Ollama returned HTTP {response.status_code}: {response.text}"
        )

    data = response.json()

    if "error" in data:
        raise RuntimeError(f"Ollama error: {data['error']}")

    return data.get("response", "")
