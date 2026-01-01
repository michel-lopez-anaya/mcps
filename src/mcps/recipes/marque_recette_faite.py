#!/usr/bin/env python3
"""Module providing the marque_recette_faite function."""
import os
from datetime import datetime

from mcps.recipes.recipe_manager import SQLiteRecipeManager
from mcps.recipes.database_manager import SQLiteDatabaseManager


def marque_recette_faite(titre: str) -> str:
    """Met à jour la date de réalisation d'une recette et renvoie le résultat.

    Parameters
    ----------
    titre: str
        Le titre de la recette à marquer comme faite.

    Returns
    -------
    str
        Chaîne contenant le titre et la nouvelle valeur de la colonne `description`.
    """
    db_path = os.path.expanduser("/home/courses/.local/share/gourmand/recipes.db")
    db_manager = SQLiteDatabaseManager(db_path)
    recipe_manager = SQLiteRecipeManager(db_manager)

    if db_manager.connect():
        date_today = datetime.now().strftime("%Y-%m-%d")
        result = recipe_manager.update_recipe(titre, date_today)
        db_manager.close()
        return result
    else:
        return "Impossible de se connecter à la base de données."
