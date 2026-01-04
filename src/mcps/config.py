#!/usr/bin/env python3
"""
Module de configuration centralisée pour le projet MCP.
Permet de charger et gérer la configuration depuis différents sources.
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional

class ConfigManager:
    """Gestionnaire de configuration centralisé."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialise le gestionnaire de configuration.
        
        Parameters
        ----------
        config_path : str, optional
            Chemin vers le fichier de configuration. Si None, cherche dans les emplacements par défaut.
        """
        self.config_path = config_path or self._find_config_file()
        self.config = self._load_config()
    
    def _find_config_file(self) -> Optional[str]:
        """
        Trouve le fichier de configuration dans les emplacements par défaut.
        
        Returns
        -------
        str or None
            Chemin vers le fichier de configuration trouvé, ou None si non trouvé.
        """
        # Emplacements par défaut à chercher
        default_paths = [
            Path.cwd() / "config" / "config.yaml",
            Path.cwd() / "config.yaml",
            Path.home() / ".config" / "mcps" / "config.yaml",
            Path.home() / ".mcps" / "config.yaml",
        ]
        
        for path in default_paths:
            if path.exists():
                return str(path)
        
        return None
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Charge la configuration depuis le fichier YAML.
        
        Returns
        -------
        dict
            Configuration chargée, ou dictionnaire vide si erreur.
        """
        if not self.config_path or not Path(self.config_path).exists():
            return self._get_default_config()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"⚠️  Erreur lors du chargement de la configuration: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        Retourne la configuration par défaut.
        
        Returns
        -------
        dict
            Configuration par défaut.
        """
        return {
            "database": {
                "path": "~/.local/share/gourmand/recipes.db"
            },
            "mbox": {
                "path": "~/Mail/ia_raw.mbox"
            },
            "scripts": {
                "jsonise_script": "scripts/jsonise.sh"
            },
            "environment": {
                "DISPLAY": ":0",
                "XAUTHORITY": "~/.Xauthority",
                "PATH": "/usr/local/bin:/usr/bin:/bin",
                "NODE_PATH": "/usr/lib/node_modules"
            }
        }
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Récupère une valeur de configuration en utilisant un chemin séparé par des points.
        
        Parameters
        ----------
        key_path : str
            Chemin de la clé (ex: "database.path")
        default : any
            Valeur par défaut si la clé n'est pas trouvée
        
        Returns
        -------
        any
            Valeur de la configuration ou la valeur par défaut.
        """
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_database_path(self) -> str:
        """
        Récupère le chemin de la base de données avec expansion utilisateur.
        
        Returns
        -------
        str
            Chemin de la base de données.
        """
        db_path = self.get("database.path", "~/.local/share/gourmand/recipes.db")
        return os.path.expanduser(db_path)
    
    def get_mbox_path(self) -> str:
        """
        Récupère le chemin du fichier mbox avec expansion utilisateur.
        
        Returns
        -------
        str
            Chemin du fichier mbox.
        """
        mbox_path = self.get("mbox.path", "~/Mail/ia_raw.mbox")
        return os.path.expanduser(mbox_path)
    
    def get_environment_vars(self) -> Dict[str, str]:
        """
        Récupère les variables d'environnement configurées.
        
        Returns
        -------
        dict
            Dictionnaire des variables d'environnement.
        """
        env_vars = self.get("environment", {})
        # Étendre les variables avec expansion utilisateur
        expanded_env = {}
        for key, value in env_vars.items():
            expanded_env[key] = os.path.expanduser(str(value)) if isinstance(value, str) else str(value)
        return expanded_env

# Instance globale du gestionnaire de configuration
_config_manager: Optional[ConfigManager] = None

def get_config() -> ConfigManager:
    """
    Récupère l'instance globale du gestionnaire de configuration.
    
    Returns
    -------
    ConfigManager
        Instance du gestionnaire de configuration.
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager

def get_config_value(key_path: str, default: Any = None) -> Any:
    """
    Récupère une valeur de configuration de manière pratique.
    
    Parameters
    ----------
    key_path : str
        Chemin de la clé (ex: "database.path")
    default : any
        Valeur par défaut si la clé n'est pas trouvée
    
    Returns
    -------
    any
        Valeur de la configuration ou la valeur par défaut.
    """
    return get_config().get(key_path, default)

# Exemple d'utilisation :
# db_path = get_config_value("database.path", "~/.local/share/gourmand/recipes.db")
# env_vars = get_config().get_environment_vars()