#!/usr/bin/env python3
"""
Serveur MCP tâches quotidiennes  :
* **calcul** – addition de deux nombres
* **resume_emails** – exécute le script ``jsonise.sh`` via le module ``run_jsonise`` et renvoie le texte préfixé.
* **marque_recette_faite** – met à jour la date de réalisation d'une recette via le module ``marque_recette_faite``.
* **propose_des_recettes** – propose des recettes via le module ``propose_des_recettes``.

Communication via stdio (stdin/stdout) au format JSON‑RPC 2.0.
"""
import json
import sys
from typing import Any

# Import helper functions from dedicated modules
from mcps.email_processing.run_jsonise import _run_jsonise
from mcps.email_processing.synthetise_texte import PROMPT_SYNTHESE

from mcps.recipes.marque_recette_faite import marque_recette_faite
from mcps.recipes.propose_des_recettes import propose_des_recettes
from mcps.recipes.gourmandise_recette import PROMPT_GOURMAND

from mcps.utils.send_clipboard import recuperer_texte_du_presse_papier

def send_message(msg: dict[str, Any]) -> None:
    """Envoie un message JSON au client via stdout."""
    json.dump(msg, sys.stdout)
    sys.stdout.write("\n")
    sys.stdout.flush()

def handle_initialize(request_id: str) -> None:
    """Répond à la requête d'initialisation en listant les capacités."""
    send_message({
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "serveur-mcp", "version": "1.0.0"},
            "capabilities": {"tools": {"calcul": {}, "resume_emails": {}, "marque_recette_faite": {}, "propose_des_recettes": {}, "prepare_synthese": {}, "gourmandise recette": {}}}
        }
    })

def handle_list_tools(request_id: str) -> None:
    """Renvoie la description des outils disponibles."""
    send_message({
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "tools": [
                {
                    "name": "calcul",
                    "description": "Additionne deux nombres",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "Premier nombre"},
                            "b": {"type": "number", "description": "Second nombre"}
                        },
                        "required": ["a", "b"]
                    }
                },
                {
                    "name": "resume_emails",
                    "description": "Lit les emails et renvoie un prompt pour le résumé.",
                    "inputSchema": {"type": "object", "properties": {}, "required": []}
                },
                {
                    "name": "marque_recette_faite",
                    "description": "Met à jour le champ description d'une recette.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"titre": {"type": "string", "description": "Titre de la recette"}},
                        "required": ["titre"]
                    }
                },
                {
                    "name": "propose_des_recettes",
                    "description": "Propose un nombre défini de recettes d'une source donnée.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "source": {"type": "string", "description": "Source des recettes"},
                            "quantite": {"type": "integer", "description": "Nombre de recettes à proposer"}
                        },
                        "required": ["source", "quantite"]
                    }
                },
                {
                    "name": "prepare_synthese",
                    "description": f"Établit un contexte pour réaliser des synthèses de textes. {PROMPT_SYNTHESE}",
                    "inputSchema": {"type": "object", "properties": {}, "required": []}
                },
                {
                    "name": "gourmandise_recette",
                    "description": f"Établit un contexte pour convertir des recettes au format gourmand. {PROMPT_GOURMAND}",
                    "inputSchema": {"type": "object", "properties": {}, "required": []}
                }

            ]
        }
    })

def handle_call_tool(request_id: str, params: dict) -> None:
    """Exécution d'un outil demandé via ``tools/call``."""
    tool_name = params.get("name")
    arguments = params.get("arguments", {})

    if tool_name == "calcul":
        a = arguments.get("a", 0)
        b = arguments.get("b", 0)
        resultat = a + b
        send_message({
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": f"Le résultat de {a} + {b} = {resultat}"}]}
        })
    elif tool_name == "resume_emails":
        result = _run_jsonise()
        send_message({
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result.get("output", "")}]}
        })
    elif tool_name == "marque_recette_faite":
        titre = arguments.get("titre")
        if not titre:
            result_text = "Veuillez spécifier le titre de la recette."
        else:
            result_text = marque_recette_faite(titre)
        send_message({
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        })
    elif tool_name == "propose_des_recettes":
        source = arguments.get("source")
        quantite = arguments.get("quantite")
        if not source or quantite is None:
            result_text = "Veuillez spécifier la source et la quantité de recettes."
        else:
            result_text = propose_des_recettes(source, quantite)
        send_message({
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        })
    elif tool_name == "prepare_synthese":
        contexte_a_etablir = recuperer_texte_du_presse_papier()
        send_message({
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": contexte_a_etablir}]}
        })
    elif tool_name == "gourmandise_recette":
        contexte_a_etablir = recuperer_texte_du_presse_papier()
        send_message({
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": contexte_a_etablir}]}
        })
    else:
        send_message({
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32601, "message": f"Outil inconnu: {tool_name}"}
        })

def main() -> None:
    """Boucle principale du serveur – lit les requêtes JSON sur stdin."""
    for line in sys.stdin:
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue
        method = message.get("method")
        request_id = message.get("id")
        params = message.get("params", {})
        if method == "initialize":
            handle_initialize(request_id)
        elif method == "tools/list":
            handle_list_tools(request_id)
        elif method == "tools/call":
            handle_call_tool(request_id, params)
        elif method == "notifications/initialized":
            pass
        else:
            send_message({
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Méthode inconnue: {method}"}
            })

if __name__ == "__main__":
    main()
