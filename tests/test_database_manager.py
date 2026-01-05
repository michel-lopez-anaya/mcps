#!/usr/bin/env python3
"""Tests for the database_manager module."""
import sys
from unittest.mock import patch, MagicMock

# Add the src directory to the path so we can import the modules
sys.path.insert(0, 'src')

from mcps.recipes.database_manager import SQLiteDatabaseManager


def test_sqlite_database_manager_connect_success():
    """Test that SQLiteDatabaseManager can connect successfully."""
    # Mock sqlite3 connection
    mock_conn = MagicMock()
    
    with patch('mcps.recipes.database_manager.sqlite3.connect', return_value=mock_conn):
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


def test_sqlite_database_manager_commit():
    """Test that SQLiteDatabaseManager can commit changes."""
    # Mock sqlite3 connection
    mock_conn = MagicMock()

    db_manager = SQLiteDatabaseManager('/mock/path/database.db')
    db_manager.conn = mock_conn

    db_manager.commit()

    # Check that commit was called on the connection
    mock_conn.commit.assert_called_once()


def test_sqlite_database_manager_close():
    """Test that SQLiteDatabaseManager can close the connection."""
    # Mock sqlite3 connection
    mock_conn = MagicMock()

    db_manager = SQLiteDatabaseManager('/mock/path/database.db')
    db_manager.conn = mock_conn

    db_manager.close()

    # Check that close was called on the connection and conn is set to None
    mock_conn.close.assert_called_once()
    assert db_manager.conn is None


def test_sqlite_database_manager_connect_failure():
    """Test that SQLiteDatabaseManager handles connection failure."""
    with patch('mcps.recipes.database_manager.sqlite3.connect', side_effect=Exception('Connection failed')):
        db_manager = SQLiteDatabaseManager('/mock/path/database.db')
        result = db_manager.connect()

        # Check that connect returns False on failure
        assert result is False
        # Check that no connection is stored
        assert db_manager.conn is None


def test_sqlite_database_manager_execute_query_no_connection():
    """Test that SQLiteDatabaseManager raises exception when no connection."""
    db_manager = SQLiteDatabaseManager('/mock/path/database.db')
    # Don't set db_manager.conn to simulate no connection

    try:
        db_manager.execute_query("SELECT * FROM test")
        assert False, "Expected exception was not raised"
    except Exception as e:
        assert str(e) == "Aucune connexion à la base de données."


def test_sqlite_database_manager_commit_no_connection():
    """Test that SQLiteDatabaseManager handles commit with no connection."""
    db_manager = SQLiteDatabaseManager('/mock/path/database.db')
    # Don't set db_manager.conn to simulate no connection

    # This should not raise an exception, just do nothing
    db_manager.commit()
    # No assertions needed, just ensure no exception is raised


def test_sqlite_database_manager_close_no_connection():
    """Test that SQLiteDatabaseManager handles close with no connection."""
    db_manager = SQLiteDatabaseManager('/mock/path/database.db')
    # Don't set db_manager.conn to simulate no connection

    # This should not raise an exception, just do nothing
    db_manager.close()
    # No assertions needed, just ensure no exception is raised
