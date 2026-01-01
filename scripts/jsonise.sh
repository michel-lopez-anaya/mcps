#!/usr/bin/env sh

APP="mcp_perso"

# Vérifier si HOME est défini et valide
if [ -z "${HOME}" ] || [ ! -d "${HOME}" ]; then
    # Récupérer HOME depuis l'UID de l'utilisateur
    HOME=$(getent passwd "$(id -u)" | cut -d: -f6)
    # Si getent échoue (système sans /etc/passwd), utiliser /home/user
    if [ -z "${HOME}" ]; then
        HOME="/home/$(id -un)"
    fi
fi

# Récupère le répertoire absolu de jsonise.sh (même si appelé via un lien symbolique)
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

if [ -f "$SCRIPT_DIR/../config/mcp_persorc" ]; then
    . "$SCRIPT_DIR/../config/mcp_persorc"
else
    echo "Erreur config non trouvée"
    echo "$HOME/.config/$APP/mcp_persorc"
    exit 1
fi

if [ ! -d "$HOME/Mail" ]; then
    echo "$HOME/Mail"
    echo "Erreur : pas de répertoire Mail"
    exit 1
fi
    

MBOX="$HOME/Mail/$SRC"

if [ ! -f "$MBOX" ] ; then
    echo "$MBOX"
    echo "Erreur : pas de mbox"
    exit 1
fi

# Appelle avec le chemin absolu
formail -s python3 $SCRIPT_DIR/mail_to_json.py < $MBOX

exit 0
