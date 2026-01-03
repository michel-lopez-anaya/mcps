#!/usr/bin/env python3
"""Tests for the propose_des_recettes module."""
import sys
from unittest.mock import patch, MagicMock

# Add the src directory to the path so we can import the modules
sys.path.insert(0, 'src')

from mcps.recipes.propose_des_recettes import propose_des_recettes


def test_propose_des_recettes_success():
    """Test that propose_des_recettes returns the correct result when successful."""
    # Mock the database manager and recipe manager
    mock_db_manager = MagicMock()
    mock_recipe_manager = MagicMock()
    
    # Configure the mocks
    mock_db_manager.connect.return_value = True
    mock_recipe_manager.search_recipes.return_value = [
        "Recipe 1: Description 1",
        "Recipe 2: Description 2"
    ]
    
    # Patch the imports
    with patch('mcps.recipes.propose_des_recettes.SQLiteDatabaseManager', return_value=mock_db_manager), \
         patch('mcps.recipes.propose_des_recettes.SQLiteRecipeManager', return_value=mock_recipe_manager), \
         patch('mcps.recipes.propose_des_recettes.os.path.expanduser', return_value='/mock/path/recipes.db'):
        
        result = propose_des_recettes("Test Source", 2)
        
        # Check that the database manager methods were called
        mock_db_manager.connect.assert_called_once()
        mock_recipe_manager.search_recipes.assert_called_once_with("Test Source", 2)
        mock_db_manager.close.assert_called_once()
        
        # Check the result
        expected = "Recipe 1: Description 1\nRecipe 2: Description 2"
        assert result == expected


def test_propose_des_recettes_db_connection_failure():
    """Test that propose_des_recettes handles database connection failures."""
    # Mock the database manager
    mock_db_manager = MagicMock()
    
    # Configure the mock to fail connection
    mock_db_manager.connect.return_value = False
    
    # Patch the imports
    with patch('mcps.recipes.propose_des_recettes.SQLiteDatabaseManager', return_value=mock_db_manager), \
         patch('mcps.recipes.propose_des_recettes.os.path.expanduser', return_value='/mock/path/recipes.db'):
        
        result = propose_des_recettes("Test Source", 2)
        
        # Check that the database manager connect method was called
        mock_db_manager.connect.assert_called_once()
        
        # Check the result
        assert result == "Impossible de se connecter à la base de données."