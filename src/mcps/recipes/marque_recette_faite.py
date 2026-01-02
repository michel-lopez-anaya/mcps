#!/usr/bin/env python3
"""Module providing the marque_recette_faite function."""
import os
from datetime import datetime
from pathlib import Path

from mcps.recipes.recipe_manager import SQLiteRecipeManager
from mcps.recipes.database_manager import SQLiteDatabaseManager
try:
    import yaml
except Exception:
    yaml = None


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
    # Load database path from YAML config if available, otherwise fallback
    config_path = Path(__file__).resolve().parents[3] / "config" / "config.yaml"
    db_path = None
    if config_path.exists():
        try:
            if yaml:
                with open(config_path, "r") as f:
                    cfg = yaml.safe_load(f)
                    db_path = cfg.get("database", {}).get("path")
            else:
                # minimal fallback parser for the simple YAML structure
                with open(config_path, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("path:"):
                            db_path = line.split(":", 1)[1].strip().strip('"').strip("'")
                            break
        except Exception:
            db_path = None

    if not db_path:
        db_path = "/home/courses/.local/share/gourmand/recipes.db"

    db_path = os.path.expanduser(db_path)
    db_manager = SQLiteDatabaseManager(db_path)
    recipe_manager = SQLiteRecipeManager(db_manager)

    if db_manager.connect():
        date_today = datetime.now().strftime("%Y-%m-%d")
        result = recipe_manager.update_recipe(titre, date_today)
        db_manager.close()
        if result is None:
            return f"Aucune recette trouvée avec le titre '{titre}'."
        return result
    else:
        return "Impossible de se connecter à la base de données."
