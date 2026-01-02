#!/usr/bin/env python3
"""Module providing the _run_jsonise function used by the MCP server.
"""

from typing import Dict
from mcps.email_processing.jsonise import run_jsonise
 
def _run_jsonise() -> Dict:
    """Execute ``jsonise.sh`` and return its output prefixed by a static prompt.

    Returns
    -------
    dict
        ``{"output": <text>, "error": <msg>}`` – the ``error`` key is only present on failure.
    """
    
    # Call the function and return its result
    return run_jsonise()
