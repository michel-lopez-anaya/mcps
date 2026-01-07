# Projet MCP (Multi-Tool Controller for Personal Tasks)

Ce projet est un serveur MCP (Multi-Tool Controller) conçu pour automatiser des tâches quotidiennes, notamment la gestion des emails et des recettes culinaires. Il utilise une architecture modulaire et une communication via JSON-RPC 2.0.

## Structure du Projet

```
.
├── config/
│   ├── conf_ollmcp.json     # Configuration pour le serveur MCP
│   └── config.yaml          # Fichier de configuration principal
├── scripts/
├── src/
│   └── mcps/
│       ├── email_processing/
│       │   ├── jsonise.py          # Module pour traiter les emails
│       │   └── synthetise_texte.py # Contexte pour la synthèse de texte
│       ├── mcp_server/
│       │   └── mcp_perso.py       # Serveur MCP principal
│       ├── recipes/
│       │   ├── database_manager.py # Gestion de la base de données SQLite
│       │   ├── gourmandise_recette.py # Contexte pour convertir des recettes
│       │   ├── marque_recette_faite.py # Met à jour la date de réalisation d'une recette
│       │   ├── propose_des_recettes.py # Propose des recettes
│       │   └── recipe_manager.py   # Gestion des recettes
│       └── utils/
│           ├── config.py           # Gestion centralisée de la configuration
│           └── send_clipboard.py  # Utilitaires pour le presse-papiers
├── README.md                 # Documentation du projet
├── requirements.txt         # Dépendances Python
├── test-requirements.txt    # Dépendances pour les tests
├── todo.md                  # Liste des tâches et améliorations
└── tests/                   # Tests unitaires et d'intégration
```

## Fonctionnalités

### 1. Gestion des Emails
- **`jsonise.py`** : Module Python qui nettoie et extrait le contenu des emails (HTML et texte brut), gère les pièces jointes et les métadonnées.
- **`synthetise_texte.py`** : Contexte pour réaliser des synthèses de textes.

### 2. Gestion des Recettes
- **`database_manager.py`** : Interface et implémentation pour la gestion de la base de données SQLite.
- **`recipe_manager.py`** : Interface et implémentation pour la gestion des recettes.
- **`marque_recette_faite.py`** : Met à jour la date de réalisation d'une recette.
- **`propose_des_recettes.py`** : Propose un nombre défini de recettes à partir d'une source donnée.
- **`gourmandise_recette.py`** : Contexte pour convertir des recettes au format gourmand.

### 3. Serveur MCP
- **`mcp_perso.py`** : Serveur MCP principal qui fournit les outils suivants :
  - **`calcul`** : Additionne deux nombres.
  - **`resume_emails`** : Exécute le script `mail_to_json.py` et résume les emails.
  - **`marque_recette_faite`** : Met à jour la date de réalisation d'une recette.
  - **`propose_des_recettes`** : Propose des recettes.
  - **`prepare_synthese`** : Établit un contexte pour réaliser des synthèses de textes.
  - **`gourmandise_recette`** : Établit un contexte pour convertir des recettes au format gourmand.

## Installation

1. Clonez ce dépôt sur votre machine locale :
   ```bash
   git clone https://github.com/votre-utilisateur/mcps.git
   cd mcps
   créer un environnement virtuel pour ce projet
   python3 -m venv ~/.venv
   activer l’environnement 
   source ~/.venv/bin/activate
   ```

2. Installez les dépendances nécessaires :
   ```bash
   pip install -r requirements.txt
   ```

3. Configurez les fichiers de configuration :
   - Modifiez `config/config.yaml` selon vos besoins.

4. Exécutez le serveur MCP :
   ```bash
   copier la configuration du serveur dans "conf_ollmcp.json" dans la configuration des serveurs de ollmcp, gemini cli, etc
   lancer ollmcp, gemini cli, etc
   ```

## Contribution

Les contributions sont les bienvenues. Veuillez ouvrir une issue ou soumettre une pull request pour toute amélioration ou correction de bug.

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENCE` pour plus de détails.
