# Tests Unitaires et d'Intégration

Ce répertoire contient les tests pour l'application MCP Personnelle.

## Structure des Tests

### Tests Unitaires (33 tests)
- `test_jsonise.py` - Tests unitaires pour le traitement des emails (20 tests)
  - Utilise unittest.TestCase avec des méthodes de test complètes
  - Couvre le nettoyage HTML, l'extraction de corps, la détection de pièces jointes, etc.

- `test_database_manager.py` - Tests unitaires pour le gestionnaire de base de données (2 tests)
  - Tests de connexion et d'exécution de requêtes

- `test_recipe_manager.py` - Tests unitaires pour le gestionnaire de recettes (2 tests)
  - Tests de mise à jour et de recherche de recettes

- `test_marque_recette_faite.py` - Tests unitaires pour le marquage de recettes (2 tests)
  - Tests de succès et de gestion des erreurs de connexion

- `test_propose_des_recettes.py` - Tests unitaires pour la proposition de recettes (2 tests)
  - Tests de succès et de gestion des erreurs de connexion

- `test_mcp_perso.py` - Tests unitaires pour le serveur MCP (2 tests)
  - Tests d'initialisation et de liste des outils

### Tests d'Intégration (19 tests)
- `test_integration.py` - Tests d'intégration complets couvrant :

#### Classes de Test

1. **TestDatabaseIntegration**
   - Connexion et opérations de base de données
   - Insertion et récupération de données
   - Gestion des transactions

2. **TestRecipeManagerIntegration**
   - Workflow complet de mise à jour de recettes
   - Workflow de recherche de recettes
   - Gestion des erreurs

3. **TestMarqueRecetteFaiteIntegration**
   - Marquage de recettes comme faites
   - Mise à jour des dates dans la base de données
   - Gestion des recettes inexistantes

4. **TestProposeDesRecettesIntegration**
   - Proposition de recettes par source
   - Limitation du nombre de résultats
   - Gestion des sources inexistantes

5. **TestMailToJSONIntegration**
   - Workflow complet de traitement d'emails
   - Traitement d'emails HTML
   - Détection de pièces jointes
   - Nettoyage du corps des emails

6. **TestMCPFullIntegration**
   - Intégration du calcul via MCP
   - Intégration du marquage de recettes via MCP
   - Intégration de la proposition de recettes via MCP
   - Séquence d'initialisation du serveur MCP

7. **TestEndToEndWorkflow**
   - Cycle de vie complet des recettes
   - Workflow complet du serveur MCP
   - Tests de bout en bout

## Exécution des Tests

### Exécuter tous les tests
```bash
pytest tests/ -v
```

### Exécuter uniquement les tests d'intégration
```bash
pytest tests/test_integration.py -v
```

### Exécuter une classe de tests spécifique
```bash
pytest tests/test_integration.py::TestDatabaseIntegration -v
```

### Exécuter un test spécifique
```bash
pytest tests/test_integration.py::TestRecipeManagerIntegration::test_full_recipe_update_workflow -v
```

### Exécuter avec couverture de code
```bash
pytest tests/ --cov=src --cov-report=html
```

## Dépendances de Test

Les tests nécessitent les packages suivants (voir `test-requirements.txt`) :
- pytest
- pytest-cov
- pytest-mock

## Caractéristiques des Tests d'Intégration

### Bases de Données Temporaires
- Chaque test utilise une base de données SQLite temporaire
- Les données sont nettoyées automatiquement après chaque test
- Pas de risque de pollution des données de production

### Patching Intelligent
- Les chemins de fichiers sont patchés pour utiliser les bases de données temporaires
- Les entrées/sorties standard sont capturées pour tester les communications MCP

### Scénarios Réels
- Les tests simulent des scénarios d'utilisation réels
- Les workflows complets sont testés de bout en bout
- La gestion des erreurs est validée

## Bonnes Pratiques

1. **Isolation** : Chaque test est indépendant et ne modifie pas les autres
2. **Nettoyage** : Les ressources sont libérées automatiquement
3. **Clarté** : Les noms de tests décrivent clairement ce qui est testé
4. **Couverture** : Les tests couvrent les cas nominaux et les cas d'erreur
5. **Vitesse** : Les tests sont conçus pour être rapides tout en étant complets

## Résultats Attendus

### Tests Unitaires
```
tests/test_database_manager.py::test_sqlite_database_manager_connect_success PASSED
tests/test_database_manager.py::test_sqlite_database_manager_execute_query PASSED
tests/test_jsonise.py::TestEmailProcessing::test_clean_body_collapses_blank_lines PASSED
tests/test_jsonise.py::TestEmailProcessing::test_clean_body_empty_string PASSED
tests/test_jsonise.py::TestEmailProcessing::test_clean_body_only_quotes PASSED
tests/test_jsonise.py::TestEmailProcessing::test_clean_body_only_signature PASSED
tests/test_jsonise.py::TestEmailProcessing::test_clean_body_removes_quotes PASSED
tests/test_jsonise.py::TestEmailProcessing::test_clean_body_removes_signature PASSED
tests/test_jsonise.py::TestEmailProcessing::test_clean_message_with_encoding_issues PASSED
tests/test_jsonise.py::TestEmailProcessing::test_clean_message_with_invalid_html PASSED
tests/test_jsonise.py::TestEmailProcessing::test_clean_message_with_valid_html PASSED
tests/test_jsonise.py::TestEmailProcessing::test_extract_body_html_text PASSED
tests/test_jsonise.py::TestEmailProcessing::test_extract_body_multipart PASSED
tests/test_jsonise.py::TestEmailProcessing::test_extract_body_plain_text PASSED
tests/test_jsonise.py::TestEmailProcessing::test_has_attachment_with_attachment PASSED
tests/test_jsonise.py::TestEmailProcessing::test_has_attachment_without_attachment PASSED
tests/test_jsonise.py::TestEmailProcessing::test_load_config_not_found PASSED
tests/test_jsonise.py::TestEmailProcessing::test_load_config_success PASSED
tests/test_jsonise.py::TestEmailProcessing::test_process_email_basic PASSED
tests/test_jsonise.py::TestEmailProcessing::test_process_email_with_long_words PASSED
tests/test_jsonise.py::TestEmailProcessing::test_process_mbox PASSED
tests/test_jsonise.py::TestEmailProcessing::test_process_mbox_not_found PASSED
tests/test_jsonise.py::TestEmailProcessing::test_run_jsonise_config_error PASSED
tests/test_jsonise.py::TestEmailProcessing::test_run_jsonise_missing_config_values PASSED
tests/test_jsonise.py::TestEmailProcessing::test_run_jsonise_success PASSED
tests/test_marque_recette_faite.py::test_marque_recette_faite_success PASSED
tests/test_marque_recette_faite.py::test_marque_recette_faite_db_connection_failure PASSED
tests/test_mcp_perso.py::test_handle_initialize PASSED
tests/test_mcp_perso.py::test_handle_list_tools PASSED
tests/test_propose_des_recettes.py::test_propose_des_recettes_success PASSED
tests/test_propose_des_recettes.py::test_propose_des_recettes_db_connection_failure PASSED
tests/test_recipe_manager.py::test_sqlite_recipe_manager_update_recipe PASSED
tests/test_recipe_manager.py::test_sqlite_recipe_manager_search_recipes PASSED

======================== 33 passed, 19 deselected in 0.17s =========================
```

### Tests d'Intégration
Les tests d'intégration valident :
- ✅ L'intégration correcte entre les modules
- ✅ Le fonctionnement des workflows complets
- ✅ La persistance des données dans la base de données
- ✅ La communication correcte via le protocole MCP
- ✅ La gestion robuste des erreurs
- ✅ L'absence de régression lors des modifications
