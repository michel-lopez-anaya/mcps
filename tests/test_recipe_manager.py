#!/usr/bin/env python3
"""Tests for the recipe_manager module."""
import sys
from unittest.mock import patch, MagicMock

# Add the src directory to the path so we can import the modules
sys.path.insert(0, 'src')

from mcps.recipes.recipe_manager import SQLiteRecipeManager


def test_sqlite_recipe_manager_update_recipe():
    """Test that SQLiteRecipeManager can update a recipe."""
    # Mock the database manager
    mock_db_manager = MagicMock()
    mock_db_manager.execute_query.return_value = [('Test Recipe', 'Made today')]
    
    recipe_manager = SQLiteRecipeManager(mock_db_manager)
    result = recipe_manager.update_recipe('Test Recipe', 'Made today')
    
    # Check that the database methods were called
    assert mock_db_manager.execute_query.call_count == 2
    mock_db_manager.commit.assert_called_once()
    
    # Check the result
    assert result == "Test Recipe: Made today"


def test_sqlite_recipe_manager_search_recipes():
    """Test that SQLiteRecipeManager can search for recipes."""
    # Mock the database manager
    mock_db_manager = MagicMock()
    mock_db_manager.execute_query.return_value = [
        ('Description 1', 'Recipe 1'),
        ('Description 2', 'Recipe 2')
    ]

    recipe_manager = SQLiteRecipeManager(mock_db_manager)
    result = recipe_manager.search_recipes('Test Source', 2)

    # Check that the database method was called with correct parameters
    mock_db_manager.execute_query.assert_called_once_with(
        "SELECT description, title FROM recipe WHERE source = ? ORDER BY description LIMIT ?",
        ('Test Source', 2)
    )

    # Check the result
    assert result == ["Description 1: Recipe 1", "Description 2: Recipe 2"]


def test_sqlite_recipe_manager_get_recipe():
    """Test that SQLiteRecipeManager can get a recipe."""
    # Mock the database manager
    mock_db_manager = MagicMock()
    mock_db_manager.execute_query.return_value = [('Test Recipe', 'Made today')]

    recipe_manager = SQLiteRecipeManager(mock_db_manager)
    result = recipe_manager.get_recipe('Test Recipe')

    # Check that the database method was called with correct parameters
    mock_db_manager.execute_query.assert_called_once_with(
        "SELECT title, description FROM recipe WHERE title = ?",
        ('Test Recipe',)
    )

    # Check the result
    assert result == "Test Recipe: Made today"


def test_sqlite_recipe_manager_get_recipe_not_found():
    """Test that SQLiteRecipeManager handles recipe not found."""
    # Mock the database manager
    mock_db_manager = MagicMock()
    mock_db_manager.execute_query.return_value = []

    recipe_manager = SQLiteRecipeManager(mock_db_manager)
    result = recipe_manager.get_recipe('Nonexistent Recipe')

    # Check that the database method was called
    mock_db_manager.execute_query.assert_called_once_with(
        "SELECT title, description FROM recipe WHERE title = ?",
        ('Nonexistent Recipe',)
    )

    # Check the result
    assert result == "Recette 'Nonexistent Recipe' introuvable."


def test_sqlite_recipe_manager_update_recipe_not_found():
    """Test that SQLiteRecipeManager handles update when recipe not found."""
    # Mock the database manager
    mock_db_manager = MagicMock()
    mock_db_manager.execute_query.return_value = []

    recipe_manager = SQLiteRecipeManager(mock_db_manager)
    result = recipe_manager.update_recipe('Nonexistent Recipe', 'New description')

    # Check that the database methods were called
    assert mock_db_manager.execute_query.call_count == 2
    mock_db_manager.commit.assert_called_once()

    # Check the result
    assert result == "Recette 'Nonexistent Recipe' introuvable."


def test_sqlite_recipe_manager_search_recipes_no_results():
    """Test that SQLiteRecipeManager handles search with no results."""
    # Mock the database manager
    mock_db_manager = MagicMock()
    mock_db_manager.execute_query.return_value = []

    recipe_manager = SQLiteRecipeManager(mock_db_manager)
    result = recipe_manager.search_recipes('Empty Source', 5)

    # Check that the database method was called
    mock_db_manager.execute_query.assert_called_once_with(
        "SELECT description, title FROM recipe WHERE source = ? ORDER BY description LIMIT ?",
        ('Empty Source', 5)
    )

    # Check the result
    assert result == ["Aucune recette trouvée pour la source 'Empty Source'."]
