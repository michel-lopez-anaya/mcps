#!/usr/bin/env python3
"""Module providing the RecipeManager interface and its implementation."""
from typing import List, Optional
from abc import ABC, abstractmethod
from mcps.recipes.database_manager import DatabaseManager


class RecipeManager:
    """Interface pour la gestion des recettes."""
    @abstractmethod
    def update_recipe(self, titre: str, description: str) -> str:
        """Met à jour la description d'une recette."""
        pass

    @abstractmethod
    def get_recipe(self, titre: str) -> str:
        """Récupère une recette par son titre."""
        pass

    @abstractmethod
    def search_recipes(self, source: str, quantite: int) -> List[str]:
        """Recherche des recettes par source et retourne une liste de résultats."""
        pass


class SQLiteRecipeManager(RecipeManager):
    """Implémentation de RecipeManager pour SQLite."""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def update_recipe(self, titre: str, description: str) -> str:
        """Met à jour la description d'une recette."""
        try:
            self.db_manager.execute_query(
                "UPDATE recipe SET description = ? WHERE title = ?",
                (description, titre)
            )
            self.db_manager.commit()
            row = self.db_manager.execute_query(
                "SELECT title, description FROM recipe WHERE title = ?",
                (titre,)
            )
            if row:
                return f"{row[0][0]}: {row[0][1]}"
            else:
                return f"Recette '{titre}' introuvable."
        except Exception as e:
            return f"Erreur lors de la mise à jour: {e}"

    def get_recipe(self, titre: str) -> str:
        """Récupère une recette par son titre."""
        try:
            row = self.db_manager.execute_query(
                "SELECT title, description FROM recipe WHERE title = ?",
                (titre,)
            )
            if row:
                return f"{row[0][0]}: {row[0][1]}"
            else:
                return f"Recette '{titre}' introuvable."
        except Exception as e:
            return f"Erreur glors de la récupération: {e}"

    def search_recipes(self, source: str, quantite: int) -> List[str]:
        """Recherche des recettes par source et retourne une liste de résultats."""
        try:
            rows = self.db_manager.execute_query(
                "SELECT description, title FROM recipe WHERE source = ? ORDER BY description LIMIT ?",
                (source, quantite)
            )
            if rows:
                return [f"{desc}: {title}" for desc, title in rows]
            else:
                return [f"Aucune recette trouvée pour la source '{source}'."]
        except Exception as e:
            return [f"Erreur lors de la recherche: {e}"]
