 ## Description des fichiers

 ### `conf_ollmcp.json` Fichier de configuration pour le serveur MCP. Il
 définit le chemin et les arguments pour exécuter `mcp_perso.py`
 et spécifie les variables d'environnement nécessaires.

 ### `jsonise.sh` Script shell pour traiter les emails. Il récupère
 le répertoire absolu du script, vérifie l'existence des répertoires
 `Mail` et `Desktop`, et exécute `mail_to_json.py` pour convertir les
 emails en JSON.

 ### `mail_to_json.py` Script Python pour convertir les emails en format
 JSON. Il nettoie et extrait le contenu des emails (HTML et texte brut)
 et gère les pièces jointes et les métadonnées des emails.

 ### `mcp_perso.py` Serveur MCP pour les tâches quotidiennes. Il fournit
 deux outils : - `calcul` : Additionne deux nombres.  - `resume_emails`
 : Exécute `jsonise.sh` et résume les emails.  La communication se
 fait via JSON-RPC 2.0.

 ### `mcp_persorc` Fichier de configuration pour le serveur MCP. Il
 contient les paramètres spécifiques à l'environnement.

 ## Suggestions d'amélioration

 1. **Documentation** :
    - Ajouter un fichier `README.md` pour expliquer l'utilisation des
    scripts et leur
 configuration.

 2. **Gestion des erreurs** :
    - Améliorer la gestion des erreurs dans `jsonise.sh` et
    `mail_to_json.py` pour une
 meilleure robustesse.

 3. **Tests** :
    - Ajouter des tests unitaires pour `mail_to_json.py` et
    `mcp_perso.py`.

 4. **Configuration** :
    - Centraliser les chemins et configurations dans un fichier unique
    pour faciliter
 la maintenance.

 5. **Licence** :
    - Ajouter un fichier `LICENSE` pour clarifier les droits
    d'utilisation.

 ## Installation et utilisation

 1. Clonez ce dépôt sur votre machine locale.  2. Assurez-vous
 que les dépendances nécessaires sont installées (Python, etc.).
 3. Configurez les fichiers de configuration (`conf_ollmcp.json` et
 `mcp_persorc`) selon vos besoins.  4. Exécutez le serveur MCP en
 utilisant la commande appropriée.

 ## Contribution

 Les contributions sont les bienvenues. Veuillez ouvrir une issue ou
 soumettre une pull request pour toute amélioration ou correction de bug.

 ## Licence

 Ce projet est sous licence [MIT](LICENSE). Voir le fichier `LICENSE`
 pour plus de détails.
