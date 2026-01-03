#!/usr/bin/env python3
"""Tests for the marque_recette_faite module."""
import sys
from unittest.mock import patch, MagicMock

# Add the src directory to the path so we can import the modules
sys.path.insert(0, 'src')

from mcps.recipes.marque_recette_faite import marque_recette_faite


def test_marque_recette_faite_success():
    """Test that marque_recette_faite returns the correct result when successful."""
    # Mock the database manager and recipe manager
    mock_db_manager = MagicMock()
    mock_recipe_manager = MagicMock()
    
    # Configure the mocks
    mock_db_manager.connect.return_value = True
    mock_recipe_manager.update_recipe.return_value = "Test Recipe: Made on 2023-01-01"
    
    # Patch the imports and datetime
    with patch('mcps.recipes.marque_recette_faite.SQLiteDatabaseManager', return_value=mock_db_manager), \
         patch('mcps.recipes.marque_recette_faite.SQLiteRecipeManager', return_value=mock_recipe_manager), \
         patch('mcps.recipes.marque_recette_faite.os.path.expanduser', return_value='/mock/path/recipes.db'), \
         patch('mcps.recipes.marque_recette_faite.datetime') as mock_datetime:
        
        # Set up the mock datetime to return a fixed date
        mock_datetime.now.return_value.strftime.return_value = "2026-01-03"
        
        result = marque_recette_faite("Test Recipe")
        
        # Check that the database manager methods were called
        mock_db_manager.connect.assert_called_once()
        mock_recipe_manager.update_recipe.assert_called_once_with("Test Recipe", "2026-01-03")
        mock_db_manager.close.assert_called_once()
        
        # Check the result
        assert result == "Test Recipe: Made on 2023-01-01"


def test_marque_recette_faite_db_connection_failure():
    """Test that marque_recette_faite handles database connection failures."""
    # Mock the database manager
    mock_db_manager = MagicMock()
    
    # Configure the mock to fail connection
    mock_db_manager.connect.return_value = False
    
    # Patch the imports
    with patch('mcps.recipes.marque_recette_faite.SQLiteDatabaseManager', return_value=mock_db_manager), \
         patch('mcps.recipes.marque_recette_faite.os.path.expanduser', return_value='/mock/path/recipes.db'):
        
        result = marque_recette_faite("Test Recipe")
        
        # Check that the database manager connect method was called
        mock_db_manager.connect.assert_called_once()
        
        # Check the result
        assert result == "Impossible de se connecter à la base de données."
