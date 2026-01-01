#!/usr/bin/env python3

import os
import subprocess
import shutil
import json

PROMPT_SYNTHESE = """
**OBJECTIF**: réaliser la synthèse d’un texte.

**DÉFINITION**:
Une synthèse de texte est un résumé structuré et concis qui restitue les idées principales d'un document en les reformulant avec ses propres mots. Elle doit :

 1 Identifier l'essentiel : extraire les informations clés sans ajouter d'interprétations personnelles.

 2 Respecter la logique originale : conserver l'ordre des idées ou les organiser de manière cohérente.

 3 Être objective : éviter les jugements de valeur, sauf si le texte en contient.

 4 Être claire et précise : utiliser un langage simple et des phrases courtes. 
L'objectif est de permettre au lecteur de comprendre rapidement le contenu du texte sans avoir à le lire en entier.  

**OUTPUT**:
- Organisation avec une section par information clé
- Hiérachie des sections numérotées I, II, III, ...
- Les titres de niveau 2 seront introduit par un point

Écris un synthèse du texte qui suit :

"""

def recuperer_texte_du_presse_papier():
    try:
        xclip_path = shutil.which('xclip')
        if not xclip_path:
            raise RuntimeError("xclip n'est pas disponible")
        
        env = os.environ.copy()
        
        # Si DISPLAY n'est pas défini ou est :0, essayer de le détecter
        if not env.get('DISPLAY') or env.get('DISPLAY') == ':0':
            # Chercher les displays actifs
            try:
                # Méthode 1: depuis /tmp/.X11-unix/
                x_sockets = os.listdir('/tmp/.X11-unix/')
                if x_sockets:
                    # Prendre le premier display trouvé (ex: X0 -> :0)
                    display_num = x_sockets[0].replace('X', ':')
                    env['DISPLAY'] = display_num
            except:
                pass
            
            # Méthode 2: depuis les processus actifs de USER A
            if not env.get('DISPLAY') or env['DISPLAY'] == ':0':
                try:
                    result = subprocess.run(
                        ['ps', 'aux'],
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    # Chercher une ligne avec Xorg ou X11
                    for line in result.stdout.split('\n'):
                        if 'Xorg' in line or '/usr/bin/X' in line:
                            # Extraire le display (généralement après "vt" ou seul)
                            parts = line.split()
                            for i, part in enumerate(parts):
                                if part.startswith(':') and part[1:].split('.')[0].isdigit():
                                    env['DISPLAY'] = part
                                    break
                            break
                except:
                    pass
        
        # Tester la connexion X11
        test_result = subprocess.run(
            ['xset', 'q'],
            capture_output=True,
            text=True,
            env=env,
            timeout=2
        )
        
        if test_result.returncode != 0:
            return json.dumps(f"Erreur X11 avec DISPLAY={env.get('DISPLAY')}: {test_result.stderr}")
        
        # Récupérer le clipboard
        result = subprocess.run(
            [xclip_path, '-selection', 'primary', '-o'],
            capture_output=True,
            text=True,
            env=env,
            timeout=5
        )
        
        if result.returncode != 0:
            return json.dumps(f"Erreur xclip: {result.stderr}")
        
        if not result.stdout:
            return json.dumps("Presse-papiers PRIMARY vide")
        
        return json.dumps(result.stdout, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps(f"Erreur: {str(e)}")
