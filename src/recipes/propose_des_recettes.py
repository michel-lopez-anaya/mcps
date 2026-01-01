#!/usr/bin/env python3
"""Module providing the propose_des_recettes function."""
import os
from recipes.recipe_manager import SQLiteRecipeManager
from recipes.database_manager import SQLiteDatabaseManager


def propose_des_recettes(source: str, quantite: int) -> str:
    """Propose un nombre défini de recettes à partir d'une source donnée.

    Parameters
    ----------
    source: str
        La source des recettes à rechercher.
    quantite: int
        Nombre de recettes à proposer.

    Returns
    -------
    str
        Texte contenant la description et le titre de chaque recette trouvée, ou un message si aucune n'est trouvée.
    """
    db_path = os.path.expanduser("/home/courses/.local/share/gourmand/recipes.db")
    db_manager = SQLiteDatabaseManager(db_path)
    recipe_manager = SQLiteRecipeManager(db_manager)

    if db_manager.connect():
        results = recipe_manager.search_recipes(source, quantite)
        db_manager.close()
        return "\n".join(results)
    else:
        return "Impossible de se connecter à la base de données."
