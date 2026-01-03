# Guide des Tests d'Intégration

Ce guide explique comment exécuter et utiliser les tests d'intégration créés pour les modules du projet MCP.

## 📋 Table des Matières

- [Vue d'ensemble](#vue-densemble)
- [Modules Testés](#modules-testés)
- [Installation](#installation)
- [Exécution des Tests](#exécution-des-tests)
- [Résultats Attendus](#résultats-attendus)
- [Dépannage](#dépannage)

## 🔍 Vue d'ensemble

Les tests d'intégration valident le fonctionnement correct des interactions entre les différents modules du projet :

```
┌─────────────────┐
│    jsonise      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────────┐
│  recipe_manager │◄───►│ database_manager │
└────────┬────────┘     └──────────────────┘
         │
         ▼
┌─────────────────┐
│    mcp_perso    │
└─────────────────┘
```

## 📦 Modules Testés

### 1. `jsonise.py`
**Responsabilité** : Conversion des emails en format JSON

**Tests d'intégration** :
- ✅ Workflow complet de traitement d'emails (multipart)
- ✅ Traitement d'emails HTML avec nettoyage
- ✅ Détection de pièces jointes
- ✅ Nettoyage du corps des emails (citations, signatures)

### 2. `recipe_manager.py`
**Responsabilité** : Gestion des opérations sur les recettes

**Tests d'intégration** :
- ✅ Workflow complet de mise à jour de recettes
- ✅ Workflow de recherche de recettes avec pagination
- ✅ Gestion des erreurs (recettes inexistantes)
- ✅ Intégration avec database_manager

### 3. `marque_recette_faite.py`
**Responsabilité** : Marquage d'une recette comme réalisée

**Tests d'intégration** :
- ✅ Marquage complet avec mise à jour de la date
- ✅ Persistance dans la base de données
- ✅ Gestion des recettes inexistantes
- ✅ Format correct de la date

### 4. `propose_des_recettes.py`
**Responsabilité** : Proposition de recettes par source

**Tests d'intégration** :
- ✅ Recherche et filtrage par source
- ✅ Limitation du nombre de résultats
- ✅ Gestion des sources inexistantes
- ✅ Format correct des résultats

### 5. `database_manager.py`
**Responsabilité** : Gestion de la connexion et des opérations DB

**Tests d'intégration** :
- ✅ Connexion et déconnexion
- ✅ Exécution de requêtes avec paramètres
- ✅ Gestion des transactions (commit)
- ✅ Gestion des erreurs de connexion

### 6. `mcp_perso.py`
**Responsabilité** : Serveur MCP JSON-RPC

**Tests d'intégration** :
- ✅ Séquence d'initialisation
- ✅ Liste des outils disponibles
- ✅ Exécution des outils (calcul, recettes)
- ✅ Communication bidirectionnelle JSON-RPC
- ✅ Gestion des erreurs

## 🚀 Installation

### Prérequis
```bash
# Python 3.8+
python --version

# Installer les dépendances de test
pip install -r test-requirements.txt
```

### Configuration
Le fichier `pytest.ini` configure automatiquement pytest.

## 🧪 Exécution des Tests

### Méthode 1 : Script dédié (Recommandé)

```bash
# Exécuter tous les tests
python run_tests.py

# Exécuter uniquement les tests d'intégration
python run_tests.py --type integration

# Exécuter uniquement les tests unitaires
python run_tests.py --type unitary

# Avec couverture de code
python run_tests.py --coverage

# Mode silencieux
python run_tests.py --quiet
```

### Méthode 2 : Pytest direct

```bash
# Tous les tests
pytest tests/ -v

# Tests d'intégration uniquement
pytest tests/test_integration.py -v

# Une classe de tests spécifique
pytest tests/test_integration.py::TestDatabaseIntegration -v

# Un test spécifique
pytest tests/test_integration.py::TestRecipeManagerIntegration::test_full_recipe_update_workflow -v

# Avec couverture de code
pytest tests/ --cov=src --cov-report=html
```

## 📊 Résultats Attendus

### Succès
```
tests/test_integration.py::TestDatabaseIntegration::test_database_connection_and_query PASSED
tests/test_integration.py::TestRecipeManagerIntegration::test_full_recipe_update_workflow PASSED
tests/test_integration.py::TestRecipeManagerIntegration::test_full_recipe_search_workflow PASSED
tests/test_integration.py::TestRecipeManagerIntegration::test_error_handling_workflow PASSED
tests/test_integration.py::TestMarqueRecetteFaiteIntegration::test_mark_recipe_as_done_integration PASSED
tests/test_integration.py::TestMarqueRecetteFaiteIntegration::test_mark_nonexistent_recipe PASSED
tests/test_integration.py::TestProposeDesRecettesIntegration::test_propose_recipes_integration PASSED
tests/test_integration.py::TestProposeDesRecettesIntegration::test_propose_recipes_with_limit PASSED
tests/test_integration.py::TestProposeDesRecettesIntegration::test_propose_recipes_no_results PASSED
tests/test_integration.py::TestMailToJSONIntegration::test_full_email_processing_workflow PASSED
tests/test_integration.py::TestMailToJSONIntegration::test_html_email_processing PASSED
tests/test_integration.py::TestMailToJSONIntegration::test_email_attachment_detection PASSED
tests/test_integration.py::TestMailToJSONIntegration::test_email_without_attachment PASSED
tests/test_integration.py::TestMCPFullIntegration::test_mcp_calcul_integration PASSED
tests/test_integration.py::TestMCPFullIntegration::test_mcp_marque_recette_faite_integration PASSED
tests/test_integration.py::TestMCPFullIntegration::test_mcp_propose_des_recettes_integration PASSED
tests/test_integration.py::TestMCPFullIntegration::test_mcp_initialization_sequence PASSED
tests/test_integration.py::TestEndToEndWorkflow::test_complete_recipe_lifecycle PASSED
tests/test_integration.py::TestEndToEndWorkflow::test_mcp_server_full_workflow PASSED

======================== 19 passed in 1.72s =========================
```

### Couverture de Code
```
Name                                             Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------
src/email_processing/jsonise.py                      89      0   100%
src/recipes/database_manager.py                      22      0   100%
src/recipes/recipe_manager.py                        32      0   100%
src/recipes/marque_recette_faite.py                  17      0   100%
src/recipes/propose_des_recettes.py                  17      0   100%
src/mcp_server/mcp_perso.py                          85      0   100%
------------------------------------------------------------------------------
TOTAL                                                262      0   100%
```

## 🔧 Dépannage

### Erreur : ModuleNotFoundError
```bash
# Solution : Ajoutez le répertoire src au PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
# ou
python run_tests.py  # Le script gère cela automatiquement
```

### Erreur : Permission denied pour la base de données
```bash
# Solution : Vérifiez les permissions du répertoire temporaire
chmod +x tests/
```

### Tests lents
```bash
# Solution : Exécutez uniquement les tests nécessaires
pytest tests/test_integration.py::TestDatabaseIntegration -v
```

### Problèmes de nettoyage
```bash
# Solution : Nettoyez manuellement les fichiers temporaires
find /tmp -name "*.db" -user $(whoami) -delete
```

## 📝 Structure d'un Test d'Intégration

```python
class TestExempleIntegration:
    """Tests d'intégration pour le module Exemple."""
    
    def setup_method(self):
        """Configuration avant chaque test."""
        # Créer les ressources nécessaires (DB, fichiers, etc.)
        pass
    
    def teardown_method(self):
        """Nettoyage après chaque test."""
        # Supprimer les ressources temporaires
        pass
    
    def test_workflow_complet(self):
        """Test le workflow complet."""
        # 1. Préparation
        # 2. Exécution
        # 3. Vérification
        assert True
```

## 🎯 Bonnes Pratiques

1. **Isolation** : Chaque test est indépendant
2. **Automatisation** : Nettoyage automatique des ressources
3. **Clarté** : Noms de tests descriptifs
4. **Vitesse** : Tests rapides tout en étant complets
5. **Maintenance** : Code facile à comprendre et modifier

## 📚 Ressources Supplémentaires

- [Documentation Pytest](https://docs.pytest.org/)
- [Tests d'intégration vs Tests Unitaires](https://martinfowler.com/bliki/UnitTest.html)
- [Meilleures pratiques de testing](https://testing-python.com/)

---

**Dernière mise à jour** : 2026-01-03
