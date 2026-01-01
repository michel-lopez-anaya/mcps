#!/usr/bin/env python3
"""Tests for the run_jsonise module."""
import sys
from unittest.mock import patch, MagicMock

# Add the src directory to the path so we can import the modules
sys.path.insert(0, 'src')

from email_processing.run_jsonise import _run_jsonise


def test_run_jsonise_success():
    """Test that _run_jsonise returns the correct result when the script executes successfully."""
    # Mock the subprocess result
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "Email 1 content\nEmail 2 content"
    mock_result.stderr = ""
    
    # Patch the imports
    with patch('email_processing.run_jsonise.subprocess.run', return_value=mock_result), \
         patch('email_processing.run_jsonise.os.path.isfile', return_value=True), \
         patch('email_processing.run_jsonise.os.path.abspath', return_value='/mock/path'), \
         patch('email_processing.run_jsonise.os.path.expanduser', return_value='/mock/path'):
        
        result = _run_jsonise()
        
        # Check the result
        assert "output" in result
        assert "error" not in result
        assert result["output"].startswith("écrit un résumé de 80 mots pour chacun des emails qui suivent :")
        assert "Email 1 content" in result["output"]
        assert "Email 2 content" in result["output"]


def test_run_jsonise_script_not_found():
    """Test that _run_jsonise handles the case when the script is not found."""
    # Patch the imports to simulate script not found
    with patch('email_processing.run_jsonise.os.path.isfile', return_value=False), \
         patch('email_processing.run_jsonise.os.path.abspath', return_value='/mock/path'), \
         patch('email_processing.run_jsonise.os.path.expanduser', return_value='/mock/path'):
        
        result = _run_jsonise()
        
        # Check the result
        assert "error" in result
        assert "script not found" in result["error"]
        assert "output" not in result