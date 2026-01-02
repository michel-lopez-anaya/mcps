#!/usr/bin/env python3
"""Module providing the propose_des_recettes function."""
import os
from pathlib import Path
from mcps.recipes.recipe_manager import SQLiteRecipeManager
from mcps.recipes.database_manager import SQLiteDatabaseManager
try:
    import yaml
except Exception:
    yaml = None


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
        results = recipe_manager.search_recipes(source, quantite)
        db_manager.close()
        return "\n".join(results)
    else:
        return "Impossible de se connecter à la base de données."
