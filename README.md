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
  - **`marque_recette_faite`** : Met à jour la date de réalisation d'une recette. Attend le titre exact de la recette dans la base de données et inscrit la date du jour dans l'enregistrement.
  - **`propose_des_recettes`** : Propose des recettes. Attend deux paramètres : le nombre de recettes attendues et la source d'origine (ex : marmiton, diner, etc.). Les recettes apparaissent dans l'ordre de leur dernière confection.
  - **`prepare_synthese`** : Établit un contexte pour réaliser des synthèses de textes. Travaille sur le texte présent dans le clipboard obtenu en sélectionnant du texte avec la souris.
  - **`gourmandise_recette`** : Établit un contexte pour convertir des recettes au format gourmand. Travaille sur le texte présent dans le clipboard obtenu en sélectionnant du texte avec la souris.

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

3. Installez la commande `xclip` (nécessaire pour le presse-papiers) :
   ```bash
   sudo apt-get install xclip
   ```
   **Note** : Le script d'installation ne gère pas cette dépendance système. C'est à l'utilisateur de l'installer manuellement.

3. Configurez les fichiers de configuration :
   - Modifiez `config/config.yaml` selon vos besoins.
   - **Important** : Vous devez personnaliser le fichier `config/conf_ollmcp.json` en fonction du répertoire où vous installez le serveur. Mettez à jour les chemins d'accès dans ce fichier pour qu'ils correspondent à votre environnement local.

4. Exécutez le serveur MCP :
   ```bash
   copier la configuration du serveur dans "conf_ollmcp.json" dans la configuration des serveurs de ollmcp, cline, etc
   lancer ollmcp, cline, etc
   ```

## Notes importantes

- **Base de données** : Ce projet utilise une base de données au format du logiciel libre Gourmand. La base de données n'est pas fournie avec ce projet et doit être obtenue séparément.

- **Gestion des emails** : Le serveur s'attend à trouver les emails dans un fichier au format mbox. Ce fichier doit contenir un nombre limité de mails, typiquement les nouveaux de la journée. L'utilisation de fichiers contenant trop d'emails peut saturer l'IA qui les traitera. D'autres formats de mail n'ont pas été testés.

- **Compatibilité** : Ce serveur a été testé uniquement sous Debian 13. Il peut fonctionner sur d'autres distributions Linux, mais cela n'a pas été vérifié.

## Contribution

Les contributions sont les bienvenues. Veuillez ouvrir une issue ou soumettre une pull request pour toute amélioration ou correction de bug.

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENCE` pour plus de détails.
