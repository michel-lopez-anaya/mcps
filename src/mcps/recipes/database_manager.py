#!/usr/bin/env python3
"""Module providing the DatabaseManager interface and its implementation."""
from typing import List, Optional, Any
import sqlite3


class DatabaseManager:
    """Interface pour la gestion de la base de données."""

    def connect(self) -> bool:
        """Établit une connexion à la base de données."""
        pass

    def execute_query(self, query: str, params: tuple = None) -> List[Any]:
        """Exécute une requête SQL et retourne les résultats."""
        pass

    def commit(self) -> None:
        """Valide les changements dans la base de données."""
        pass

    def close(self) -> None:
        """Fermer la connexion à la base de données."""
        pass


class SQLiteDatabaseManager(DatabaseManager):
    """Implémentation de DatabaseManager pour SQLite."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None

    def connect(self) -> bool:
        """Établit une connexion à la base de données."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            return True
        except Exception as e:
            print(f"Erreur lors de la connexion à la base de données: {e}")
            return False

    def execute_query(self, query: str, params: tuple = None) -> List[Any]:
        """Exécute une requête SQL et retourne les résultats."""
        if not self.conn:
            raise Exception("Aucune connexion à la base de données.")
        cursor = self.conn.cursor()
        cursor.execute(query, params or ())
        return cursor.fetchall()

    def commit(self) -> None:
        """Valide les changements dans la base de données."""
        if self.conn:
            self.conn.commit()

    def close(self) -> None:
        """Fermer la connexion à la base de données."""
        if self.conn:
            self.conn.close()
            self.conn = None
