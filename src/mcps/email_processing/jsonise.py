#!/usr/bin/env python3

import mailbox
import json
import os
import sys
from mcps.email_processing.mail_to_json import process_email


def load_config():
    """Charge la configuration depuis le fichier config.yaml."""
    config_path = "/home/michel/Desktop/mcps/config/config.yaml"
    
    if not os.path.isfile(config_path):
        print(f"Erreur : config non trouvée à {config_path}")
        sys.exit(1)
    
    import yaml
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config


def process_mbox(mbox_path):
    """Traite un fichier mbox et convertit chaque email en JSON."""
    if not os.path.isfile(mbox_path):
        print(f"Erreur : pas de mbox à {mbox_path}")
        sys.exit(1)
    
    mbox = mailbox.mbox(mbox_path)
    
    for message in mbox:
        email_data = process_email(message)
        print(json.dumps(email_data, indent=2))

def run_jsonise() -> dict:
    """Execute le processus de jsonise et retourne son output.
    
    Returns
    -------
    dict
        {"output": <text>, "error": <msg>} – la clé "error" n'est présente qu'en cas d'échec.
    """
    try:
        config = load_config()
        
        if "mbox" not in config or "SRC" not in config["mbox"] or "path" not in config["mbox"]:
            return {"error": "SRC ou path non défini dans la configuration"}
        
        mbox_path = config["mbox"]["path"]
        
        # Capture l'output de process_mbox
        from io import StringIO
        import sys
        
        # Redirige stdout pour capturer l'output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        process_mbox(mbox_path)
        
        # Rétablit stdout
        sys.stdout = old_stdout
        
        prompt = "écrit un résumé de 80 mots pour chacun des emails qui suivent : "
        output = captured_output.getvalue().strip()
        combined = f"{prompt}\n{output}" if output else prompt
        
        return {"output": combined}
        
    except Exception as exc:
        return {"error": f"exécution échouée : {exc}"}
