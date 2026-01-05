import unittest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
import yaml

from mcps.utils.config import ConfigManager, get_config, get_config_value

class TestConfigManager(unittest.TestCase):

    def setUp(self):
        """Configuration commune pour tous les tests"""
        # Réinitialiser l'instance globale
        import mcps.utils.config
        mcps.utils.config._config_manager = None

    def test_init_with_config_path(self):
        """Test d'initialisation avec un chemin de configuration spécifié"""
        with patch('mcps.utils.config.Path') as mock_path:
            mock_path.return_value.exists.return_value = True
            with patch('builtins.open', mock_open(read_data='test: value')):
                with patch('yaml.safe_load', return_value={'test': 'value'}):
                    manager = ConfigManager('/custom/path/config.yaml')
                    self.assertEqual(manager.config_path, '/custom/path/config.yaml')
                    self.assertEqual(manager.config, {'test': 'value'})

    def test_init_without_config_path(self):
        """Test d'initialisation sans chemin spécifié (recherche automatique)"""
        with patch.object(ConfigManager, '_find_config_file', return_value='/found/config.yaml'):
            with patch.object(ConfigManager, '_load_config', return_value={'auto': 'config'}):
                manager = ConfigManager()
                self.assertEqual(manager.config_path, '/found/config.yaml')
                self.assertEqual(manager.config, {'auto': 'config'})



    def test_load_config_success(self):
        """Test du chargement réussi de la configuration"""
        config_data = {'database': {'path': '/test/db'}, 'mbox': {'path': '/test/mbox'}}
        yaml_data = yaml.dump(config_data)

        with patch('builtins.open', mock_open(read_data=yaml_data)):
            with patch('mcps.utils.config.Path') as mock_path:
                mock_path.return_value.exists.return_value = True
                manager = ConfigManager('/test/config.yaml')
                loaded_config = manager._load_config()
                self.assertEqual(loaded_config, config_data)

    def test_load_config_file_not_exists(self):
        """Test du chargement quand le fichier n'existe pas"""
        with patch('mcps.utils.config.Path') as mock_path:
            mock_path.return_value.exists.return_value = False
            manager = ConfigManager('/nonexistent/config.yaml')
            config = manager._load_config()
            # Devrait retourner la config par défaut
            self.assertIn('database', config)
            self.assertIn('mbox', config)

    def test_load_config_invalid_yaml(self):
        """Test du chargement avec YAML invalide"""
        with patch('builtins.open', mock_open(read_data='invalid: yaml: content: [')):
            with patch('mcps.utils.config.Path') as mock_path:
                mock_path.return_value.exists.return_value = True
                with patch('yaml.safe_load', side_effect=yaml.YAMLError("Invalid YAML")):
                    manager = ConfigManager('/test/config.yaml')
                    config = manager._load_config()
                    # Devrait retourner la config par défaut en cas d'erreur
                    self.assertIn('database', config)

    def test_get_default_config(self):
        """Test de récupération de la configuration par défaut"""
        manager = ConfigManager()
        default_config = manager._get_default_config()

        self.assertIn('database', default_config)
        self.assertIn('mbox', default_config)
        self.assertIn('environment', default_config)

        self.assertEqual(default_config['database']['path'], '~/.local/share/gourmand/recipes.db')
        self.assertEqual(default_config['mbox']['path'], '~/Mail')
        self.assertEqual(default_config['mbox']['SRC'], 'ia_raw_mbox')

    def test_get_simple_key(self):
        """Test de récupération d'une clé simple"""
        manager = ConfigManager()
        manager.config = {'simple_key': 'simple_value'}
        result = manager.get('simple_key')
        self.assertEqual(result, 'simple_value')

    def test_get_nested_key(self):
        """Test de récupération d'une clé imbriquée"""
        manager = ConfigManager()
        manager.config = {'database': {'path': '/test/path', 'type': 'sqlite'}}
        result = manager.get('database.path')
        self.assertEqual(result, '/test/path')

        result = manager.get('database.type')
        self.assertEqual(result, 'sqlite')

    def test_get_key_not_found(self):
        """Test de récupération d'une clé inexistante"""
        manager = ConfigManager()
        manager.config = {'existing': 'value'}
        result = manager.get('nonexistent')
        self.assertIsNone(result)

    def test_get_key_not_found_with_default(self):
        """Test de récupération d'une clé inexistante avec valeur par défaut"""
        manager = ConfigManager()
        manager.config = {'existing': 'value'}
        result = manager.get('nonexistent', 'default_value')
        self.assertEqual(result, 'default_value')

    def test_get_nested_key_not_found(self):
        """Test de récupération d'une clé imbriquée inexistante"""
        manager = ConfigManager()
        manager.config = {'database': {'path': '/test/path'}}
        result = manager.get('database.nonexistent')
        self.assertIsNone(result)

    def test_get_database_path(self):
        """Test de récupération du chemin de la base de données"""
        manager = ConfigManager()
        manager.config = {'database': {'path': '~/custom/db/path'}}
        with patch('os.path.expanduser', return_value='/home/user/custom/db/path'):
            result = manager.get_database_path()
            self.assertEqual(result, '/home/user/custom/db/path')

    def test_get_database_path_default(self):
        """Test de récupération du chemin par défaut de la base de données"""
        manager = ConfigManager()
        manager.config = {}
        with patch('os.path.expanduser', return_value='/home/user/.local/share/gourmand/recipes.db'):
            result = manager.get_database_path()
            self.assertEqual(result, '/home/user/.local/share/gourmand/recipes.db')

    def test_get_mbox_path(self):
        """Test de récupération du chemin mbox"""
        manager = ConfigManager()
        manager.config = {'mbox': {'path': '~/custom/mbox/path'}}
        with patch('os.path.expanduser', return_value='/home/user/custom/mbox/path'):
            result = manager.get_mbox_path()
            self.assertEqual(result, '/home/user/custom/mbox/path')

    def test_get_mbox_path_default(self):
        """Test de récupération du chemin par défaut mbox"""
        manager = ConfigManager()
        manager.config = {}
        with patch('os.path.expanduser', return_value='/home/user/Mail/ia_raw.mbox'):
            result = manager.get_mbox_path()
            self.assertEqual(result, '/home/user/Mail/ia_raw.mbox')

    def test_get_environment_vars(self):
        """Test de récupération des variables d'environnement"""
        manager = ConfigManager()
        manager.config = {
            'environment': {
                'DISPLAY': ':1',
                'PATH': '~/bin:/usr/bin',
                'NODE_PATH': '/usr/lib/node_modules'
            }
        }
        with patch('os.path.expanduser', side_effect=lambda x: x.replace('~', '/home/user')):
            result = manager.get_environment_vars()
            expected = {
                'DISPLAY': ':1',
                'PATH': '/home/user/bin:/usr/bin',
                'NODE_PATH': '/usr/lib/node_modules'
            }
            self.assertEqual(result, expected)

    def test_get_environment_vars_empty(self):
        """Test de récupération des variables d'environnement quand aucune n'est configurée"""
        manager = ConfigManager()
        manager.config = {}
        result = manager.get_environment_vars()
        self.assertEqual(result, {})

    def test_get_environment_vars_non_string_values(self):
        """Test de récupération des variables d'environnement avec valeurs non-string"""
        manager = ConfigManager()
        manager.config = {
            'environment': {
                'PORT': 3000,
                'DEBUG': True
            }
        }
        result = manager.get_environment_vars()
        expected = {
            'PORT': '3000',
            'DEBUG': 'True'
        }
        self.assertEqual(result, expected)

    def test_get_config_creates_instance(self):
        """Test que get_config crée une instance globale"""
        # Assurer qu'aucune instance n'existe
        import mcps.utils.config
        mcps.utils.config._config_manager = None

        with patch('mcps.utils.config.ConfigManager') as mock_manager_class:
            mock_instance = MagicMock()
            mock_manager_class.return_value = mock_instance

            result = get_config()
            self.assertEqual(result, mock_instance)
            mock_manager_class.assert_called_once_with()

    def test_get_config_returns_existing_instance(self):
        """Test que get_config retourne l'instance existante"""
        import mcps.utils.config
        mock_instance = MagicMock()
        mcps.utils.config._config_manager = mock_instance

        result = get_config()
        self.assertEqual(result, mock_instance)

    def test_get_config_value(self):
        """Test de la fonction get_config_value"""
        with patch('mcps.utils.config.get_config') as mock_get_config:
            mock_manager = MagicMock()
            mock_manager.get.return_value = 'test_value'
            mock_get_config.return_value = mock_manager

            result = get_config_value('test.key', 'default')
            self.assertEqual(result, 'test_value')
            mock_manager.get.assert_called_once_with('test.key', 'default')

if __name__ == '__main__':
    unittest.main()
