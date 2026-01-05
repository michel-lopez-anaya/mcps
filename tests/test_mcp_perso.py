#!/usr/bin/env python3
"""Tests for the mcp_perso module."""
import json
import sys
from io import StringIO
from unittest.mock import patch, MagicMock

# Add the src directory to the path so we can import the modules
sys.path.insert(0, 'src')

from mcps.mcp_server.mcp_perso import handle_initialize, handle_list_tools, handle_call_tool


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
    expected_tools = {"calcul", "resume_emails", "marque_recette_faite", "propose_des_recettes", "prepare_synthese", "gourmandise_recette"}
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
    assert len(response["result"]["tools"]) == 6
    
    # Check that each tool has the required fields
    tool_names = {tool["name"] for tool in response["result"]["tools"]}
    expected_tools = {"calcul", "resume_emails", "marque_recette_faite", "propose_des_recettes", "prepare_synthese", "gourmandise_recette"}
    assert tool_names == expected_tools
    
    # Check specific tool details
    calcul_tool = next(tool for tool in response["result"]["tools"] if tool["name"] == "calcul")
    assert "inputSchema" in calcul_tool
    assert "properties" in calcul_tool["inputSchema"]
    assert "a" in calcul_tool["inputSchema"]["properties"]
    assert "b" in calcul_tool["inputSchema"]["properties"]


def test_handle_call_tool_calcul():
    """Test handle_call_tool for the calcul tool."""
    captured_output = StringIO()
    with patch('sys.stdout', captured_output):
        handle_call_tool("789", {"name": "calcul", "arguments": {"a": 5, "b": 3}})

    output = captured_output.getvalue().strip()
    response = json.loads(output)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == "789"
    assert "result" in response
    assert response["result"]["content"][0]["type"] == "text"
    assert "Le résultat de 5 + 3 = 8" in response["result"]["content"][0]["text"]


@patch('mcps.mcp_server.mcp_perso.run_jsonise')
def test_handle_call_tool_resume_emails(mock_run_jsonise):
    """Test handle_call_tool for the resume_emails tool."""
    mock_run_jsonise.return_value = {"output": "Résumé des emails"}

    captured_output = StringIO()
    with patch('sys.stdout', captured_output):
        handle_call_tool("101", {"name": "resume_emails", "arguments": {}})

    output = captured_output.getvalue().strip()
    response = json.loads(output)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == "101"
    assert response["result"]["content"][0]["text"] == "Résumé des emails"
    mock_run_jsonise.assert_called_once()


@patch('mcps.mcp_server.mcp_perso.marque_recette_faite')
def test_handle_call_tool_marque_recette_faite(mock_marque_recette_faite):
    """Test handle_call_tool for the marque_recette_faite tool with valid titre."""
    mock_marque_recette_faite.return_value = "Recette marquée comme faite"

    captured_output = StringIO()
    with patch('sys.stdout', captured_output):
        handle_call_tool("102", {"name": "marque_recette_faite", "arguments": {"titre": "Pasta"}})

    output = captured_output.getvalue().strip()
    response = json.loads(output)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == "102"
    assert response["result"]["content"][0]["text"] == "Recette marquée comme faite"
    mock_marque_recette_faite.assert_called_once_with("Pasta")


def test_handle_call_tool_marque_recette_faite_missing_titre():
    """Test handle_call_tool for the marque_recette_faite tool without titre."""
    captured_output = StringIO()
    with patch('sys.stdout', captured_output):
        handle_call_tool("103", {"name": "marque_recette_faite", "arguments": {}})

    output = captured_output.getvalue().strip()
    response = json.loads(output)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == "103"
    assert response["result"]["content"][0]["text"] == "Veuillez spécifier le titre de la recette."


@patch('mcps.mcp_server.mcp_perso.propose_des_recettes')
def test_handle_call_tool_propose_des_recettes(mock_propose_des_recettes):
    """Test handle_call_tool for the propose_des_recettes tool with valid params."""
    mock_propose_des_recettes.return_value = "Liste de recettes"

    captured_output = StringIO()
    with patch('sys.stdout', captured_output):
        handle_call_tool("104", {"name": "propose_des_recettes", "arguments": {"source": "internet", "quantite": 5}})

    output = captured_output.getvalue().strip()
    response = json.loads(output)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == "104"
    assert response["result"]["content"][0]["text"] == "Liste de recettes"
    mock_propose_des_recettes.assert_called_once_with("internet", 5)


def test_handle_call_tool_propose_des_recettes_missing_params():
    """Test handle_call_tool for the propose_des_recettes tool with missing params."""
    captured_output = StringIO()
    with patch('sys.stdout', captured_output):
        handle_call_tool("105", {"name": "propose_des_recettes", "arguments": {}})

    output = captured_output.getvalue().strip()
    response = json.loads(output)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == "105"
    assert response["result"]["content"][0]["text"] == "Veuillez spécifier la source et la quantité de recettes."


@patch('mcps.mcp_server.mcp_perso.recuperer_texte_du_presse_papier')
def test_handle_call_tool_prepare_synthese(mock_recuperer):
    """Test handle_call_tool for the prepare_synthese tool."""
    mock_recuperer.return_value = "Texte synthétisé"

    captured_output = StringIO()
    with patch('sys.stdout', captured_output):
        handle_call_tool("106", {"name": "prepare_synthese", "arguments": {}})

    output = captured_output.getvalue().strip()
    response = json.loads(output)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == "106"
    assert response["result"]["content"][0]["text"] == "Texte synthétisé"
    mock_recuperer.assert_called_once()


@patch('mcps.mcp_server.mcp_perso.recuperer_texte_du_presse_papier')
def test_handle_call_tool_gourmandise_recette(mock_recuperer):
    """Test handle_call_tool for the gourmandise_recette tool."""
    mock_recuperer.return_value = "Recette gourmande"

    captured_output = StringIO()
    with patch('sys.stdout', captured_output):
        handle_call_tool("107", {"name": "gourmandise_recette", "arguments": {}})

    output = captured_output.getvalue().strip()
    response = json.loads(output)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == "107"
    assert response["result"]["content"][0]["text"] == "Recette gourmande"
    mock_recuperer.assert_called_once()


def test_handle_call_tool_unknown_tool():
    """Test handle_call_tool for an unknown tool."""
    captured_output = StringIO()
    with patch('sys.stdout', captured_output):
        handle_call_tool("108", {"name": "unknown_tool", "arguments": {}})

    output = captured_output.getvalue().strip()
    response = json.loads(output)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == "108"
    assert "error" in response
    assert response["error"]["code"] == -32601
    assert "Outil inconnu: unknown_tool" in response["error"]["message"]
