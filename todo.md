# Liste des Tâches à Faire

## Configuration et Installation

### Priorité Haute : Configuration Utilisateur
- [ ] **Adapter `config/conf_ollmcp.json`** pour l'installation spécifique de l'utilisateur
  - Mettre à jour les chemins absolus (`/home/michel/...`) avec les chemins de l'utilisateur
  - Adapter les variables d'environnement (`DISPLAY`, `XAUTHORITY`, `PATH`, etc.)
  - Vérifier les permissions et accès aux répertoires

### Priorité Moyenne : Format des Données
- [ ] **Documenter le format mbox pour les emails sous Linux**
  - Créer un guide d'utilisation pour le format mbox
  - Documenter les limitations et compatibilités
  - Ajouter des exemples de configuration

- [ ] **Tester la compatibilité Windows** (non testé actuellement)
  - Identifier les problèmes potentiels de chemins et permissions
  - Tester les dépendances spécifiques à Windows
  - Documenter les solutions de contournement

### Priorité Moyenne : Base de Données
- [ ] **Documenter la structure de la base de données Gourmand**
  - Créer un schéma de la base de données SQLite
  - Documenter les tables et relations
  - Expliquer le format des données stockées

- [ ] **Trouver et documenter la licence pour le format Gourmand**
  - Rechercher les informations de licence officielles
  - Documenter les restrictions d'utilisation
  - Ajouter les informations de licence dans le projet

## Améliorations Techniques

### Priorité Haute : Externalisation de la Configuration
- [ ] **Centraliser tous les chemins et paramètres dans `config.yaml`**
  - Déplacer les chemins codés en dur vers la configuration
  - Utiliser des variables d'environnement pour les chemins utilisateur
  - Créer des valeurs par défaut flexibles

### Priorité Moyenne : Scripts d'Installation
- [ ] **Créer un script d'installation automatique**
  - Détecter et installer les dépendances manquantes
  - Configurer automatiquement les chemins et permissions
  - Générer les fichiers de configuration nécessaires

### Priorité Basse : Améliorations Diverses
- [ ] **Ajouter des vérifications de santé du système**
- [ ] **Créer des messages d'erreur plus clairs**
- [ ] **Améliorer la documentation utilisateur**

## Documentation

- [ ] **Mettre à jour le README avec des instructions d'installation détaillées**
- [ ] **Créer un guide de dépannage complet**
- [ ] **Ajouter des exemples de configuration pour différents environnements**

## Tests

- [ ] **Ajouter des tests pour la configuration**
- [ ] **Tester les scénarios d'erreur de configuration**
- [ ] **Valider les chemins et permissions dans les tests**

---