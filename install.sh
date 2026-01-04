#!/bin/bash

# Script d'installation automatique pour le projet MCP
# Auteur: Assistant IA
# Date: $(date)

set -e  # Arrêter en cas d'erreur

echo "=== Installation du projet MCP (Multi-Tool Controller for Personal Tasks) ==="
echo

# Vérifier si on est sur Linux
if [[ "$OSTYPE" != "linux"* ]]; then
    echo "⚠️  Attention: Ce script est optimisé pour Linux. D'autres systèmes peuvent nécessiter des ajustements."
    echo
fi

# Vérifier les dépendances système requises
echo "🔍 Vérification des dépendances système..."
REQUIRED_CMDS=("python3" "pip3" "git")
MISSING_CMDS=()

for cmd in "${REQUIRED_CMDS[@]}"; do
    if ! command -v "$cmd" &> /dev/null; then
        MISSING_CMDS+=("$cmd")
    fi
done

if [ ${#MISSING_CMDS[@]} -ne 0 ]; then
    echo "❌ Dépendances manquantes: ${MISSING_CMDS[*]}"
    echo "Veuillez installer ces dépendances avant de continuer."
    exit 1
fi

echo "✅ Toutes les dépendances système sont présentes."
echo

# Créer l'environnement virtuel
echo "🔧 Création de l'environnement virtuel..."
python3 -m venv .venv
source .venv/bin/activate

echo "✅ Environnement virtuel activé."
echo

# Mettre à jour pip
echo "🔄 Mise à jour de pip..."
pip install --upgrade pip
echo

# Installer les dépendances Python
echo "📦 Installation des dépendances Python..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Dépendances installées avec succès."
else
    echo "❌ Fichier requirements.txt non trouvé."
    exit 1
fi
echo

# Créer les répertoires de configuration si nécessaire
echo "📁 Création des répertoires de configuration..."
mkdir -p config
echo

# Générer un fichier de configuration par défaut
echo "⚙️  Génération du fichier de configuration par défaut..."
cat > config/config.yaml << 'EOF'
# Configuration du projet MCP
# Modifiez ces valeurs selon votre environnement

database:
  # Chemin vers la base de données Gourmand
  # Laissez vide pour utiliser le chemin par défaut
  path: ""

mbox:
  # Chemin vers le fichier mbox pour les emails
  # Laissez vide pour utiliser le chemin par défaut
  path: ""

# Configuration des scripts (si utilisés)
scripts:
  jsonise_script: "scripts/jsonise.sh"

# Configuration de l'environnement
environment:
  # Ces valeurs seront utilisées par le serveur MCP
  DISPLAY: ":0"
  XAUTHORITY: "~/.Xauthority"
  PATH: "/usr/local/bin:/usr/bin:/bin"
  NODE_PATH: "/usr/lib/node_modules"
EOF

echo "✅ Fichier de configuration créé: config/config.yaml"
echo

# Générer un fichier de configuration MCP par défaut
echo "⚙️  Génération du fichier de configuration MCP par défaut..."
cat > config/conf_ollmcp.json << 'EOF'
{
  "mcpServers": {
    "perso": {
      "command": "python3",
      "args": [
        "-m", 
        "mcps.mcp_server.mcp_perso"
      ],
      "env": {
        "DISPLAY": ":0",
        "XAUTHORITY": "~/.Xauthority",
        "PATH": "/usr/local/bin:/usr/bin:/bin",
        "NODE_PATH": "/usr/lib/node_modules"
      }
    }
  }
}
EOF

echo "✅ Fichier de configuration MCP créé: config/conf_ollmcp.json"
echo

# Créer un script de démarrage
echo "🚀 Création du script de démarrage..."
cat > start.sh << 'EOF'
#!/bin/bash

# Script de démarrage du serveur MCP

# Activer l'environnement virtuel
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Environnement virtuel activé"
fi

# Démarrer le serveur MCP
echo "🚀 Démarrage du serveur MCP..."
python3 -m mcps.mcp_server.mcp_perso
EOF

chmod +x start.sh
echo "✅ Script de démarrage créé: start.sh"
echo

# Créer un script de test
echo "🧪 Création du script de test..."
cat > test.sh << 'EOF'
#!/bin/bash

# Script de test du projet

# Activer l'environnement virtuel
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

echo "🧪 Exécution des tests..."
python3 -m pytest tests/ -v
EOF

chmod +x test.sh
echo "✅ Script de test créé: test.sh"
echo

echo "🎉 Installation terminée avec succès !"
echo
echo "📋 Prochaines étapes :"
echo "1. Modifiez config/config.yaml selon vos besoins"
echo "2. Assurez-vous que les chemins vers la base de données et les fichiers mbox sont corrects"
echo "3. Exécutez './start.sh' pour démarrer le serveur MCP"
echo "4. Exécutez './test.sh' pour lancer les tests"
echo
echo "💡 Conseils :"
echo "- Le serveur MCP communiquera via stdio (JSON-RPC 2.0)"
echo "- Vous devez configurer ollmcp, gemini cli ou d'autres clients MCP pour utiliser ce serveur"
echo "- Consultez le README.md pour plus de détails sur l'utilisation"