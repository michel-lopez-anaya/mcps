#!/usr/bin/env python3
"""Module providing the _run_jsonise function used by the MCP server.
"""
import os
from pathlib import Path
import subprocess
from typing import Dict

SCRIPT_PATH = Path(f"{os.path.dirname(os.path.abspath(__file__))}")
SCRIPT_PATH = SCRIPT_PATH.parent.parent.parent
SCRIPT_PATH = SCRIPT_PATH / "scripts"
 
def _run_jsonise() -> Dict:
    """Execute ``jsonise.sh`` and return its output prefixed by a static prompt.

    Returns
    -------
    dict
        ``{"output": <text>, "error": <msg>}`` – the ``error`` key is only present on failure.
    """
    # Resolve the script location
    script_path = f"{SCRIPT_PATH}"
    script = os.path.join(script_path, "jsonise.sh")

    if not os.path.isfile(script):
        return {"error": f"script not found at {script}"}

    try:
        result = subprocess.run(
            [script],
            cwd=script_path,
            capture_output=True,
            text=True,
        )
    except Exception as exc:
        return {"error": f"script execution failed: {exc}"}

    if result.returncode != 0:
        err_msg = result.stderr.strip() or "unknown error"
        return {"error": f"script exited with code {result.returncode}: {err_msg}"}

    prompt = "écrit un résumé de 80 mots pour chacun des emails qui suivent : "
    script_stdout = result.stdout.strip()
    combined = f"{prompt}\n{script_stdout}" if script_stdout else prompt
    return {"output": combined}
