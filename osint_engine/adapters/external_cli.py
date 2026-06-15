from __future__ import annotations

import shutil
import subprocess


class ExternalToolUnavailable(RuntimeError):
    """Raised when an optional CLI tool is not installed."""


def run_external(command: list[str], timeout: float) -> str:
    executable = shutil.which(command[0])
    if executable is None:
        raise ExternalToolUnavailable(f"{command[0]} is not installed or not in PATH.")

    completed = subprocess.run(
        [executable, *command[1:]],
        capture_output=True,
        check=False,
        text=True,
        timeout=timeout,
    )
    output = "\n".join(part for part in (completed.stdout, completed.stderr) if part)
    if completed.returncode != 0:
        raise RuntimeError(f"{command[0]} exited with {completed.returncode}: {output[:500]}")
    return output
