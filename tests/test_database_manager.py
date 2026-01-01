#!/usr/bin/env python3
"""Tests for the database_manager module."""
import sys
from unittest.mock import patch, MagicMock

# Add the src directory to the path so we can import the modules
sys.path.insert(0, 'src')

from recipes.database_manager import SQLiteDatabaseManager


def test_sqlite_database_manager_connect_success():
    """Test that SQLiteDatabaseManager can connect successfully."""
    # Mock sqlite3 connection
    mock_conn = MagicMock()
    
    with patch('recipes.database_manager.sqlite3.connect', return_value=mock_conn):
        db_manager = SQLiteDatabaseManager('/mock/path/database.db')
        result = db_manager.connect()
        
        # Check that connect returns True
        assert result is True
        # Check that the connection is stored
        assert db_manager.conn == mock_conn


def test_sqlite_database_manager_execute_query():
    """Test that SQLiteDatabaseManager can execute queries."""
    # Mock sqlite3 connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [('test', 'data')]
    
    db_manager = SQLiteDatabaseManager('/mock/path/database.db')
    db_manager.conn = mock_conn
    
    result = db_manager.execute_query("SELECT * FROM test", ('param1', 'param2'))
    
    # Check that the query was executed with correct parameters
    mock_cursor.execute.assert_called_once_with("SELECT * FROM test", ('param1', 'param2'))
    mock_cursor.fetchall.assert_called_once()
    
    # Check the result
    assert result == [('test', 'data')]