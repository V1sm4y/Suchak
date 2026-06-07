"""
Nmap Scan Tool
==============
Runs a limited nmap scan without allowing arbitrary command execution.
"""

import re
import subprocess

from suchak.tools.base import Tool


class NmapScanTool(Tool):
    """
    Tool for running a constrained nmap scan.

    The tool accepts only a target and an optional top_ports flag. It does not
    accept raw command strings or arbitrary nmap arguments.
    """

    name = "nmap_scan"
    description = "Run a limited nmap scan against a target."
    timeout_seconds = 60

    _target_pattern = re.compile(r"^[A-Za-z0-9._:/-]+$")

    def execute(self, **kwargs) -> str:
        target = kwargs.get("target")
        top_ports = kwargs.get("top_ports", False)

        validation_error = self._validate_target(target)
        if validation_error:
            return validation_error

        if not isinstance(top_ports, bool):
            return "Error: 'top_ports' must be a boolean."

        command = ["nmap"]
        if top_ports:
            command.extend(["--top-ports", "100"])
        command.append(target)

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                shell=False,
                timeout=self.timeout_seconds,
                check=False,
            )
        except FileNotFoundError:
            return "Error: nmap is not installed or not available on PATH."
        except subprocess.TimeoutExpired:
            return "Error: nmap scan timed out."
        except OSError as err:
            return f"Error: could not run nmap: {err}"

        if result.stdout:
            return result.stdout

        if result.stderr:
            return result.stderr

        return f"nmap exited with status {result.returncode} and no output."

    def schema(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": [
                {
                    "name": "target",
                    "type": "str",
                    "required": True,
                    "description": "Hostname, IP address, or CIDR target to scan.",
                },
                {
                    "name": "top_ports",
                    "type": "bool",
                    "required": False,
                    "description": "Whether to scan only the top 100 ports.",
                },
            ],
        }

    def _validate_target(self, target: object) -> str | None:
        if not target or not isinstance(target, str):
            return "Error: 'target' is required and must be a string."

        if target.strip() != target:
            return "Error: target must not contain leading or trailing whitespace."

        if any(char.isspace() for char in target):
            return "Error: target must not contain whitespace."

        if "://" in target:
            return "Error: target must be a hostname, IP address, or CIDR range, not a URL."

        if not self._target_pattern.fullmatch(target):
            return "Error: target contains unsupported characters."

        return None
