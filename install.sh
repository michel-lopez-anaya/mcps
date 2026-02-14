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
  path: "/home/courses/.local/share/gourmand/recipes.db"

mbox:
  SRC: "ia_raw.mbox"
  path: "/home/michel/Mail"

server:
  protocolVersion: "2024-11-05"
  name: "perso"
  version: "1.3.3"
EOF

echo "✅ Fichier de configuration créé: config/config.yaml"
echo

# Générer un fichier de configuration MCP par défaut
echo "⚙️  Génération du fichier de configuration MCP par défaut..."
cat > config/conf_ollmcp.json << 'EOF'
{
  "mcpServers": {
    "perso": {
      "command": "/home/michel/.venv/bin/python3",
      "args": [
        "-m",
        "mcps.mcp_server.mcp_perso",
        "/home/michel/Desktop/"
      ],
      "cwd": "/home/michel/Desktop/mcps",
      "env": {
        "DISPLAY": ":1",
        "XAUTHORITY": "/home/michel/.Xauthority",
        "PATH": "/home/michel/.venv/bin:/usr/local/bin:/usr/bin:/bin",
        "VIRTUAL_ENV": "/home/michel/.venv",
        "PYTHONPATH": "/home/michel/Desktop/mcps/src"
      },
      "timeout": 30,
      "autoApprove": [
        "calcul",
        "resume_emails",
        "marque_recette_faite",
        "prepare_synthese",
        "gourmandise_recette"
      ]
    }
  }
}
EOF

echo "✅ Fichier de configuration MCP créé: config/conf_ollmcp.json"
echo

echo "🎉 Installation terminée avec succès !"
echo
echo "📋 Prochaines étapes :"
echo "1. Modifiez config/config.yaml selon vos besoins"
echo "2. Assurez-vous que les chemins vers la base de données et les fichiers mbox sont corrects"
echo "3. Copiez config/conf_ollmcp.json dans la configuration de votre client MCP (ollmcp, cline, etc.)"
echo "4. Lancez votre client MCP pour utiliser le serveur"
echo
echo "💡 Conseils :"
echo "- Le serveur MCP communiquera via stdio (JSON-RPC 2.0)"
echo "- Vous devez configurer ollmcp, cline ou d'autres clients MCP pour utiliser ce serveur"
echo "- Consultez le README.md pour plus de détails sur l'utilisation"
echo "- Pour exécuter les tests : python3 -m pytest tests/ -v"
echo "- Pour démarrer manuellement : python3 -m mcps.mcp_server.mcp_perso"
