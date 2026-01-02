# Tests d'Intégration

Ce répertoire contient les tests d'intégration pour l'application MCP Personnelle.

## Structure des Tests

### Tests Unitaires (existant)
- `test_mail_to_json.py` - Tests unitaires pour le traitement des emails
- `test_database_manager.py` - Tests unitaires pour le gestionnaire de base de données
- `test_recipe_manager.py` - Tests unitaires pour le gestionnaire de recettes
- `test_marque_recette_faite.py` - Tests unitaires pour le marquage de recettes
- `test_propose_des_recettes.py` - Tests unitaires pour la proposition de recettes
- `test_mcp_perso.py` - Tests unitaires pour le serveur MCP

### Tests d'Intégration (nouveau)
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

Les tests d'intégration valident :
- ✅ L'intégration correcte entre les modules
- ✅ Le fonctionnement des workflows complets
- ✅ La persistance des données dans la base de données
- ✅ La communication correcte via le protocole MCP
- ✅ La gestion robuste des erreurs
- ✅ L'absence de régression lors des modifications