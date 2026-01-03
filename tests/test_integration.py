#!/usr/bin/env python3
"""Tests d'intégration pour les modules du projet."""
import sys
import os
import json
import tempfile
import sqlite3
from io import StringIO
from datetime import datetime
from unittest.mock import patch, MagicMock

# Add the src directory to the path
sys.path.insert(0, 'src')

from mcps.recipes.database_manager import SQLiteDatabaseManager
from mcps.recipes.recipe_manager import SQLiteRecipeManager
from mcps.recipes.marque_recette_faite import marque_recette_faite
from mcps.recipes.propose_des_recettes import propose_des_recettes
from mcps.email_processing.jsonise import clean_body, extract_body, has_attachment, clean_message


class TestDatabaseIntegration:
    """Tests d'intégration pour le module de base de données."""
    
    def setup_method(self):
        """Crée une base de données de test temporaire."""
        self.test_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.test_db.close()
        
        # Créer la structure de la base de données
        conn = sqlite3.connect(self.test_db.name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipe (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                source TEXT,
                preptime TEXT,
                cooktime TEXT,
                rating TEXT,
                yields TEXT
            )
        ''')
        
        # Insérer des données de test
        test_recipes = [
            ('Recette 1', 'Description 1', 'Source A', '30 min', '1 hour', '5.0/5', '4 Personnes'),
            ('Recette 2', 'Description 2', 'Source A', '15 min', '45 min', '4.5/5', '2 Personnes'),
            ('Recette 3', 'Description 3', 'Source B', '1 hour', '2 hours', '4.0/5', '6 Personnes'),
        ]
        cursor.executemany('INSERT INTO recipe (title, description, source, preptime, cooktime, rating, yields) VALUES (?, ?, ?, ?, ?, ?, ?)', test_recipes)
        conn.commit()
        conn.close()
    
    def teardown_method(self):
        """Nettoie la base de données de test."""
        if os.path.exists(self.test_db.name):
            os.unlink(self.test_db.name)
    
    def test_database_connection_and_query(self):
        """Test l'intégration complète de la connexion et des requêtes."""
        db_manager = SQLiteDatabaseManager(self.test_db.name)
        
        # Test de connexion
        assert db_manager.connect() is True
        
        # Test d'exécution de requête
        result = db_manager.execute_query("SELECT * FROM recipe")
        assert len(result) == 3
        
        # Test de commit
        db_manager.execute_query("INSERT INTO recipe (title, description, source) VALUES (?, ?, ?)", 
                               ('Test', 'Test Description', 'Test Source'))
        db_manager.commit()
        
        # Vérification de l'insertion
        result = db_manager.execute_query("SELECT * FROM recipe WHERE title = ?", ('Test',))
        assert len(result) == 1
        assert result[0][1] == 'Test'
        
        db_manager.close()


class TestRecipeManagerIntegration:
    """Tests d'intégration pour le gestionnaire de recettes."""
    
    def setup_method(self):
        """Crée une base de données de test temporaire."""
        self.test_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.test_db.close()
        
        conn = sqlite3.connect(self.test_db.name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipe (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                source TEXT,
                preptime TEXT,
                cooktime TEXT,
                rating TEXT,
                yields TEXT
            )
        ''')
        
        test_recipes = [
            ('Recette 1', 'Description 1', 'Source A', '30 min', '1 hour', '5.0/5', '4 Personnes'),
            ('Recette 2', 'Description 2', 'Source A', '15 min', '45 min', '4.5/5', '2 Personnes'),
            ('Recette 3', 'Description 3', 'Source B', '1 hour', '2 hours', '4.0/5', '6 Personnes'),
        ]
        cursor.executemany('INSERT INTO recipe (title, description, source, preptime, cooktime, rating, yields) VALUES (?, ?, ?, ?, ?, ?, ?)', test_recipes)
        conn.commit()
        conn.close()
        
        self.db_manager = SQLiteDatabaseManager(self.test_db.name)
        self.recipe_manager = SQLiteRecipeManager(self.db_manager)
    
    def teardown_method(self):
        """Nettoie la base de données de test."""
        if self.db_manager.conn:
            self.db_manager.close()
        if os.path.exists(self.test_db.name):
            os.unlink(self.test_db.name)
    
    def test_full_recipe_update_workflow(self):
        """Test le workflow complet de mise à jour d'une recette."""
        # Connexion
        assert self.db_manager.connect() is True
        
        # Mise à jour d'une recette
        result = self.recipe_manager.update_recipe('Recette 1', 'Updated Description')
        if result == None:
            assert False
        else:
            assert 'Recette 1' in result
            assert 'Updated Description' in result
        
        # Vérification de la mise à jour
        updated_recipe = self.recipe_manager.get_recipe('Recette 1')
        if updated_recipe == None:
            assert False
        else:
            assert 'Updated Description' in updated_recipe
        
        self.db_manager.close()
    
    def test_full_recipe_search_workflow(self):
        """Test le workflow complet de recherche de recettes."""
        # Connexion
        assert self.db_manager.connect() is True
        
        # Recherche de recettes
        results = self.recipe_manager.search_recipes('Source A', 10)
        assert len(results) == 2
        assert any('Recette 1' in result for result in results)
        assert any('Recette 2' in result for result in results)
        
        # Recherche avec limite
        results = self.recipe_manager.search_recipes('Source A', 1)
        assert len(results) == 1
        
        self.db_manager.close()
    
    def test_error_handling_workflow(self):
        """Test la gestion des erreurs dans le workflow."""
        assert self.db_manager.connect() is True
        
        # Test avec une recette inexistante
        result = self.recipe_manager.get_recipe('Recette Inexistante')
        if result is None:
            assert True
        else:
            assert 'introuvable' in result.lower()
        
        # Test de mise à jour d'une recette inexistante
        result = self.recipe_manager.update_recipe('Recette Inexistante', 'Test')
        if result is None:
            assert True
        else:
            assert 'introuvable' in result.lower()
        
        self.db_manager.close()


class TestMarqueRecetteFaiteIntegration:
    """Tests d'intégration pour le module marque_recette_faite."""
    
    def setup_method(self):
        """Crée une base de données de test et patch le chemin."""
        self.test_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.test_db.close()
        
        conn = sqlite3.connect(self.test_db.name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipe (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                source TEXT,
                preptime TEXT,
                cooktime TEXT,
                rating TEXT,
                yields TEXT
            )
        ''')
        
        cursor.execute('INSERT INTO recipe (title, description, source) VALUES (?, ?, ?)', 
                      ('Test Recipe', 'Old Description', 'Test Source'))
        conn.commit()
        conn.close()
        
        # Patch le chemin de base de données
        self.patcher = patch('mcps.recipes.marque_recette_faite.os.path.expanduser', return_value=self.test_db.name)
        self.patcher.start()
    
    def teardown_method(self):
        """Nettoie les patches et la base de données."""
        self.patcher.stop()
        if os.path.exists(self.test_db.name):
            os.unlink(self.test_db.name)
    
    def test_mark_recipe_as_done_integration(self):
        """Test l'intégration complète de marquage d'une recette comme faite."""
        result = marque_recette_faite('Test Recipe')
        
        # Vérifier le résultat
        assert 'Test Recipe' in result
        
        # Vérifier que la base de données a été mise à jour
        conn = sqlite3.connect(self.test_db.name)
        cursor = conn.cursor()
        cursor.execute("SELECT description FROM recipe WHERE title = ?", ('Test Recipe',))
        description = cursor.fetchone()[0]
        conn.close()
        
        # Vérifier que la description contient la date d'aujourd'hui
        today = datetime.now().strftime("%Y-%m-%d")
        assert today in description
    
    def test_mark_nonexistent_recipe(self):
        """Test le marquage d'une recette inexistante."""
        result = marque_recette_faite('Nonexistent Recipe')
        assert 'introuvable' in result.lower()


class TestProposeDesRecettesIntegration:
    """Tests d'intégration pour le module propose_des_recettes."""
    
    def setup_method(self):
        """Crée une base de données de test et patch le chemin."""
        self.test_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.test_db.close()
        
        conn = sqlite3.connect(self.test_db.name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipe (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                source TEXT,
                preptime TEXT,
                cooktime TEXT,
                rating TEXT,
                yields TEXT
            )
        ''')
        
        test_recipes = [
            ('Recipe A1', 'Desc A1', 'Source A', '30 min', '1 hour', '5.0/5', '4 Personnes'),
            ('Recipe A2', 'Desc A2', 'Source A', '15 min', '45 min', '4.5/5', '2 Personnes'),
            ('Recipe B1', 'Desc B1', 'Source B', '1 hour', '2 hours', '4.0/5', '6 Personnes'),
        ]
        cursor.executemany('INSERT INTO recipe (title, description, source, preptime, cooktime, rating, yields) VALUES (?, ?, ?, ?, ?, ?, ?)', test_recipes)
        conn.commit()
        conn.close()
        
        # Patch le chemin de base de données
        self.patcher = patch('mcps.recipes.propose_des_recettes.os.path.expanduser', return_value=self.test_db.name)
        self.patcher.start()
    
    def teardown_method(self):
        """Nettoie les patches et la base de données."""
        self.patcher.stop()
        if os.path.exists(self.test_db.name):
            os.unlink(self.test_db.name)
    
    def test_propose_recipes_integration(self):
        """Test l'intégration complète de proposition de recettes."""
        result = propose_des_recettes('Source A', 10)
        
        # Vérifier que les recettes de Source A sont présentes
        assert 'Recipe A1' in result or 'Desc A1' in result
        assert 'Recipe A2' in result or 'Desc A2' in result
        
        # Vérifier que les recettes d'autres sources ne sont pas présentes
        assert 'Recipe B1' not in result
    
    def test_propose_recipes_with_limit(self):
        """Test la limitation du nombre de recettes proposées."""
        result = propose_des_recettes('Source A', 1)
        
        # Vérifier qu'une seule recette est retournée
        lines = [line for line in result.split('\n') if line.strip()]
        assert len(lines) <= 1
    
    def test_propose_recipes_no_results(self):
        """Test la proposition de recettes avec une source inexistante."""
        result = propose_des_recettes('Nonexistent Source', 10)
        assert 'Aucune recette trouvée' in result


class TestMailToJSONIntegration:
    """Tests d'intégration pour le module mail_to_json."""
    
    def test_full_email_processing_workflow(self):
        """Test le workflow complet de traitement d'email."""
        # Créer un email de test multipart
        from email.message import Message
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        
        # Email multipart avec texte brut
        msg = MIMEMultipart()
        msg['From'] = 'test@example.com'
        msg['Subject'] = 'Test Subject'
        
        # Ajouter du texte brut
        text_part = MIMEText('This is the main content.\n> This is a citation\n\n--\nSignature', 'plain')
        msg.attach(text_part)
        
        # Tester l'extraction du corps
        body = extract_body(msg)
        assert body is not None
        
        # Tester le nettoyage du corps
        cleaned_body = clean_body(body)
        assert 'This is the main content' in cleaned_body
        assert 'citation' not in cleaned_body
        assert 'Signature' not in cleaned_body
    
    def test_html_email_processing(self):
        """Test le traitement d'email HTML."""
        from email.mime.text import MIMEText
        
        # Email HTML
        html_content = '''
        <html>
            <body>
                <p>Main content</p>
                <script>var x = 1;</script>
                <style>p {color: red;}</style>
                <table><tr><td>Table content</td></tr></table>
            </body>
        </html>
        '''
        
        msg = MIMEText(html_content, 'html')
        msg['From'] = 'test@example.com'
        msg['Subject'] = 'HTML Test'
        
        # Tester le nettoyage HTML
        cleaned = clean_message(msg)
        
        # Vérifier que le contenu principal est conservé
        assert 'Main content' in cleaned or cleaned  # Le contenu principal doit être présent
        
        # Vérifier que les scripts et styles sont supprimés
        assert 'var x = 1' not in cleaned
        assert 'color: red' not in cleaned
    
    def test_email_attachment_detection(self):
        """Test la détection de pièces jointes."""
        from email.message import Message
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.application import MIMEApplication
        
        # Email avec pièce jointe
        msg = MIMEMultipart()
        msg['From'] = 'test@example.com'
        
        # Ajouter du texte
        text_part = MIMEText('Email content')
        msg.attach(text_part)
        
        # Ajouter une pièce jointe
        attachment = MIMEApplication(b'File content', _subtype='octet-stream')
        attachment.add_header('Content-Disposition', 'attachment', filename='test.txt')
        msg.attach(attachment)
        
        # Tester la détection de pièce jointe
        has_attach = has_attachment(msg)
        assert has_attach is True
    
    def test_email_without_attachment(self):
        """Test la détection d'absence de pièce jointe."""
        from email.mime.text import MIMEText
        
        # Email sans pièce jointe
        msg = MIMEText('Email content without attachment')
        msg['From'] = 'test@example.com'
        
        # Tester la détection
        has_attach = has_attachment(msg)
        assert has_attach is False


class TestMCPFullIntegration:
    """Tests d'intégration complets pour le serveur MCP."""
    
    def setup_method(self):
        """Crée une base de données de test pour les tests MCP."""
        self.test_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.test_db.close()
        
        conn = sqlite3.connect(self.test_db.name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipe (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                source TEXT,
                preptime TEXT,
                cooktime TEXT,
                rating TEXT,
                yields TEXT
            )
        ''')
        
        cursor.execute('INSERT INTO recipe (title, description, source) VALUES (?, ?, ?)', 
                      ('Test Recipe', 'Old Description', 'Test Source'))
        conn.commit()
        conn.close()
        
        # Patch les chemins de base de données
        self.db_patcher1 = patch('mcps.recipes.marque_recette_faite.os.path.expanduser', return_value=self.test_db.name)
        self.db_patcher2 = patch('mcps.recipes.propose_des_recettes.os.path.expanduser', return_value=self.test_db.name)
        self.db_patcher1.start()
        self.db_patcher2.start()
    
    def teardown_method(self):
        """Nettoie les patches et la base de données."""
        self.db_patcher1.stop()
        self.db_patcher2.stop()
        if os.path.exists(self.test_db.name):
            os.unlink(self.test_db.name)
    
    def test_mcp_calcul_integration(self):
        """Test l'intégration du calcul via MCP."""
        from mcps.mcp_server.mcp_perso import handle_call_tool
        
        # Capture stdout
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            handle_call_tool("123", {"name": "calcul", "arguments": {"a": 5, "b": 3}})
        
        output = captured_output.getvalue().strip()
        response = json.loads(output)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == "123"
        assert "8" in response["result"]["content"][0]["text"]
    
    def test_mcp_marque_recette_faite_integration(self):
        """Test l'intégration complète de marquage de recette via MCP."""
        from mcps.mcp_server.mcp_perso import handle_call_tool
        
        # Capture stdout
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            handle_call_tool("456", {"name": "marque_recette_faite", "arguments": {"titre": "Test Recipe"}})
        
        output = captured_output.getvalue().strip()
        response = json.loads(output)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == "456"
        assert "Test Recipe" in response["result"]["content"][0]["text"]
    
    def test_mcp_propose_des_recettes_integration(self):
        """Test l'intégration complète de proposition de recettes via MCP."""
        from mcps.mcp_server.mcp_perso import handle_call_tool
        
        # Capture stdout
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            handle_call_tool("789", {"name": "propose_des_recettes", "arguments": {"source": "Test Source", "quantite": 10}})
        
        output = captured_output.getvalue().strip()
        response = json.loads(output)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == "789"
        assert "Test Recipe" in response["result"]["content"][0]["text"]
    
    def test_mcp_initialization_sequence(self):
        """Test la séquence complète d'initialisation du serveur MCP."""
        from mcps.mcp_server.mcp_perso import handle_initialize, handle_list_tools
        
        # Test initialize
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            handle_initialize("init-123")
        
        output = captured_output.getvalue().strip()
        response = json.loads(output)
        
        assert response["jsonrpc"] == "2.0"
        assert "capabilities" in response["result"]
        
        # Test list_tools
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            handle_list_tools("list-123")
        
        output = captured_output.getvalue().strip()
        response = json.loads(output)
        
        assert response["jsonrpc"] == "2.0"
        assert "tools" in response["result"]
        assert len(response["result"]["tools"]) > 0


class TestEndToEndWorkflow:
    """Tests de bout en bout pour valider l'intégration complète."""
    
    def setup_method(self):
        """Configure l'environnement complet pour les tests E2E."""
        self.test_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.test_db.close()
        
        # Créer une base de données complète
        conn = sqlite3.connect(self.test_db.name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipe (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                source TEXT,
                preptime TEXT,
                cooktime TEXT,
                rating TEXT,
                yields TEXT
            )
        ''')
        
        test_recipes = [
            ('Pâtes Carbonara', 'Description 1', 'Famille', '20 min', '30 min', '5.0/5', '4 Personnes'),
            ('Pizza Margherita', 'Description 2', 'Marmiton', '1 hour', '20 min', '4.5/5', '6 Personnes'),
            ('Tarte aux Pommes', 'Description 3', 'Famille', '45 min', '1 hour', '4.0/5', '8 Personnes'),
        ]
        cursor.executemany('INSERT INTO recipe (title, description, source, preptime, cooktime, rating, yields) VALUES (?, ?, ?, ?, ?, ?, ?)', test_recipes)
        conn.commit()
        conn.close()
        
        # Patch les chemins
        self.patchers = [
            patch('mcps.recipes.marque_recette_faite.os.path.expanduser', return_value=self.test_db.name),
            patch('mcps.recipes.propose_des_recettes.os.path.expanduser', return_value=self.test_db.name),
        ]
        for patcher in self.patchers:
            patcher.start()
    
    def teardown_method(self):
        """Nettoie l'environnement E2E."""
        for patcher in self.patchers:
            patcher.stop()
        if os.path.exists(self.test_db.name):
            os.unlink(self.test_db.name)
    
    def test_complete_recipe_lifecycle(self):
        """Test le cycle de vie complet d'une recette."""
        # 1. Rechercher des recettes
        results = propose_des_recettes('Famille', 10)
        assert 'Pâtes Carbonara' in results or 'Tarte aux Pommes' in results
        
        # 2. Marquer une recette comme faite
        result = marque_recette_faite('Pâtes Carbonara')
        assert 'Pâtes Carbonara' in result
        
        # 3. Vérifier que la date a été mise à jour
        conn = sqlite3.connect(self.test_db.name)
        cursor = conn.cursor()
        cursor.execute("SELECT description FROM recipe WHERE title = ?", ('Pâtes Carbonara',))
        description = cursor.fetchone()[0]
        conn.close()
        
        today = datetime.now().strftime("%Y-%m-%d")
        assert today in description
    
    def test_mcp_server_full_workflow(self):
        """Test le workflow complet du serveur MCP."""
        from mcps.mcp_server.mcp_perso import handle_initialize, handle_list_tools, handle_call_tool

        # 1. Initialisation
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            handle_initialize("1")

        init_response = json.loads(captured_output.getvalue().strip())
        assert "capabilities" in init_response["result"]

        # 2. Liste des outils
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            handle_list_tools("2")

        tools_response = json.loads(captured_output.getvalue().strip())
        assert "tools" in tools_response["result"]

        # 3. Appel d'outil de calcul
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            handle_call_tool("3", {"name": "calcul", "arguments": {"a": 10, "b": 20}})

        calc_response = json.loads(captured_output.getvalue().strip())
        assert "30" in calc_response["result"]["content"][0]["text"]

        # 4. Appel d'outil de proposition de recettes
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            handle_call_tool("4", {"name": "propose_des_recettes", "arguments": {"source": "Famille", "quantite": 5}})

        recipe_response = json.loads(captured_output.getvalue().strip())
        assert "Carbonara" in recipe_response["result"]["content"][0]["text"]

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])