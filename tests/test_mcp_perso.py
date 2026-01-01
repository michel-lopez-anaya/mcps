#!/usr/bin/env python3
"""Tests for the mcp_perso module."""
import json
import sys
from io import StringIO
from unittest.mock import patch, MagicMock

# Add the src directory to the path so we can import the modules
sys.path.insert(0, 'src')

from mcp_server.mcp_perso import handle_initialize, handle_list_tools, handle_call_tool


def test_handle_initialize():
    """Test that handle_initialize sends the correct initialization response."""
    # Capture stdout
    captured_output = StringIO()
    with patch('sys.stdout', captured_output):
        handle_initialize("123")
    
    # Parse the JSON output
    output = captured_output.getvalue().strip()
    response = json.loads(output)
    
    # Check the response structure
    assert response["jsonrpc"] == "2.0"
    assert response["id"] == "123"
    assert "result" in response
    assert "protocolVersion" in response["result"]
    assert "serverInfo" in response["result"]
    assert "capabilities" in response["result"]
    
    # Check that all expected tools are listed
    expected_tools = {"calcul", "resume_emails", "marque_recette_faite", "propose_des_recettes"}
    actual_tools = set(response["result"]["capabilities"]["tools"].keys())
    assert actual_tools == expected_tools


def test_handle_list_tools():
    """Test that handle_list_tools returns the correct tool descriptions."""
    # Capture stdout
    captured_output = StringIO()
    with patch('sys.stdout', captured_output):
        handle_list_tools("456")
    
    # Parse the JSON output
    output = captured_output.getvalue().strip()
    response = json.loads(output)
    
    # Check the response structure
    assert response["jsonrpc"] == "2.0"
    assert response["id"] == "456"
    assert "result" in response
    assert "tools" in response["result"]
    
    # Check that we have the expected number of tools
    assert len(response["result"]["tools"]) == 4
    
    # Check that each tool has the required fields
    tool_names = {tool["name"] for tool in response["result"]["tools"]}
    expected_tools = {"calcul", "resume_emails", "marque_recette_faite", "propose_des_recettes"}
    assert tool_names == expected_tools
    
    # Check specific tool details
    calcul_tool = next(tool for tool in response["result"]["tools"] if tool["name"] == "calcul")
    assert "inputSchema" in calcul_tool
    assert "properties" in calcul_tool["inputSchema"]
    assert "a" in calcul_tool["inputSchema"]["properties"]
    assert "b" in calcul_tool["inputSchema"]["properties"]