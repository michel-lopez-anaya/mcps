# Documentation du projet MCPS

Ce projet est un système modulaire pour la gestion de tâches quotidiennes, notamment liées à la cuisine et à la gestion d'emails.

## Structure du projet

Le projet est organisé comme suit :

- **`src/mcps/`** : Contient les modules principaux du projet.

### Modules

#### **`email_processing/`**
Gestion et traitement des emails.

- **`jsonise.py`**
  - **Fonctions** :
    - `clean_message(message)` : Nettoie le contenu HTML d'un email et extrait le texte visible.
    - `extract_body(message)` : Extrait le corps d'un email (plain-text ou HTML nettoyé).
    - `clean_body(text)` : Nettoie le texte brut en supprimant les citations et signatures.
    - `has_attachment(message)` : Vérifie si un email contient des pièces jointes.
    - `process_email(message)` : Convertit un email en format JSON.
    - `process_mbox(mbox_path)` : Traite un fichier mbox et convertit chaque email en JSON.
    - `run_jsonise()` : Exécute le processus de conversion d'emails en JSON et retourne le résultat.

- **`synthetise_texte.py`**
  - **Constante** :
    - `PROMPT_SYNTHESE` : Prompt pour la synthèse de texte.


#### **`mcp_server/`**
Serveur pour l'exécution des tâches quotidiennes.

- **`mcp_perso.py`**
  - **Fonctions** :
    - `send_message(msg)` : Envoie un message JSON au client.
    - `handle_initialize(request_id)` : Répond à une requête d'initialisation.
    - `handle_list_tools(request_id)` : Liste les outils disponibles.
    - `handle_call_tool(request_id, params)` : Exécute un outil demandé.
    - `main()` : Boucle principale du serveur pour gérer les requêtes JSON-RPC.
  - **Outils disponibles** :
    - `calcul` : Additionne deux nombres.
    - `resume_emails` : Résume les emails.
    - `marque_recette_faite` : Met à jour la description d'une recette.
    - `propose_des_recettes` : Propose des recettes à partir d'une source.
    - `prepare_synthese` : Établit un contexte pour la synthèse de texte.
    - `gourmandise_recette` : Convertit une recette en format XML structuré.


#### **`recipes/`**
Gestion des recettes.

- **`database_manager.py`**
  - **Classes** :
    - `DatabaseManager` : Interface abstraite pour la gestion de la base de données.
    - `SQLiteDatabaseManager` : Implémentation concrète pour SQLite.
  - **Fonctions** :
    - `connect()` : Établit une connexion à la base de données.
    - `execute_query(query, params)` : Exécute une requête SQL.
    - `commit()` : Valide les changements.
    - `close()` : Ferme la connexion.

- **`gourmandise_recette.py`**
  - **Constante** :
    - `PROMPT_GOURMAND` : Prompt pour la conversion de recettes en format XML.

- **`marque_recette_faite.py`**
  - **Fonction** :
    - `marque_recette_faite(titre)` : Met à jour la date de réalisation d'une recette.

- **`propose_des_recettes.py`**
  - **Fonction** :
    - `propose_des_recettes(source, quantite)` : Propose des recettes à partir d'une source.

- **`recipe_manager.py`**
  - **Classes** :
    - `RecipeManager` : Interface abstraite pour la gestion des recettes.
    - `SQLiteRecipeManager` : Implémentation concrète pour SQLite.
  - **Fonctions** :
    - `update_recipe(titre, description)` : Met à jour la description d'une recette.
    - `get_recipe(titre)` : Récupère une recette par son titre.
    - `search_recipes(source, quantite)` : Recherche des recettes par source.


#### **`utils/`**
Utilitaires divers.

- **`send_clipboard.py`**
  - **Fonction** :
    - `recuperer_texte_du_presse_papier()` : Récupère le texte du presse-papiers.


## Fonctionnalités principales

- **Traitement des emails** : Conversion d'emails en JSON et synthèse de texte.
- **Gestion des recettes** : Mise à jour, recherche et proposition de recettes.
- **Serveur JSON-RPC** : Exécution d'outils via des requêtes JSON-RPC.
- **Utilitaires** : Récupération de texte depuis le presse-papiers.

## Configuration

Le projet utilise un fichier de configuration YAML situé dans `/config/config.yaml` pour définir les chemins des bases de données et autres paramètres.

---
