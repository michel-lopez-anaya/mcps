#!/usr/bin/env python3
import logging
import mailbox
import yaml
import json
import os
import sys
import re
from lxml import html as lxml_html
from lxml.html.clean import Cleaner
from mcps.utils.config import get_config_value

def clean_message(message):
    # -------------------------------------------------
    # 1️⃣ Read and decode the HTML payload
    # -------------------------------------------------
    try:
        payload_bytes = message.get_payload(decode=True)
        charset = message.get_content_charset() or "utf-8"
        html_text = payload_bytes.decode(charset, errors="replace")
    except Exception:
        return ""

    # -------------------------------------------------
    # 2️⃣ Parse with lxml and clean the document
    # -------------------------------------------------
    # a) Parse the HTML string into an ElementTree
    try:
        doc = lxml_html.fromstring(html_text)
    except Exception:
        # If parsing fails, return the raw HTML (fallback)
        return html_text

    # b) Define a Cleaner to remove unwanted tags and content
    cleaner = Cleaner(
        scripts=True,        # Remove <script> elements
        javascript=True,     # Remove javascript: URLs
        style=True,          # Remove <style> elements and their content
        comments=True,       # Remove HTML comments
        page_structure=False, # Keep structural tags like <body>, <div>
        safe_attrs_only=False, # Keep most attributes (we’ll strip style later)
        remove_tags=[
            "head", "title", "meta", "link",  # Metadata tags
            "iframe", "object", "embed", "svg",  # Embedded objects
            "table", "tr", "td", "th", "tbody", "thead", "tfoot"
        ],  # Remove table structures (keep inner text later)
    )

    # c) Apply the cleaner to obtain a sanitized DOM
    cleaned_doc = cleaner.clean_html(doc)

    # d) Further strip any remaining inline style attributes and stray CSS text
    for el in cleaned_doc.iter():
        # Delete inline style attributes
        if "style" in el.attrib:
            del el.attrib["style"]
        # Remove CSS rule fragments that may appear as text nodes
        if el.text:
            el.text = re.sub(r"\b\w+\s*\{[^}]*\}", "", el.text).strip()
        if el.tail:
            el.tail = re.sub(r"\b\w+\s*\{[^}]*\}", "", el.tail).strip()

    # e) Extract the clean visible text
    body_text = cleaned_doc.text_content()
    # Collapse multiple blank lines (keeps compatibility with clean_body)
    body_text = re.sub(r"\n\s*\n+", "\n\n", body_text).strip()
    return body_text

# ----------------------------------------------------------------------------------------------

def extract_body(message):
    """Recursively walk the message tree and return the first suitable plain‑text part.
    If no plain‑text part exists, fall back to the first HTML part and extract visible text using lxml.

    :param message: the parsed email message
    :return: text body
    """
    # Base case – if this is a leaf node
    if not message.is_multipart():
        if message.get_content_type() == "text/plain":
            payload = message.get_payload(decode=True)
            charset = message.get_content_charset() or "utf-8"
            return payload.decode(charset, errors="replace")
        if message.get_content_type() == "text/html":
            return clean_message(message)

    # Recursive case – walk the children
    for part in message.walk():
        if not part.is_multipart():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                charset = part.get_content_charset() or "utf-8"
                return payload.decode(charset, errors="replace")
            if part.get_content_type() == "text/html":
                return clean_message(part)
    return ""

def clean_body(text):
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        # supprimer citations
        if line.startswith(">"):
            continue
        # couper à la signature
        if line.strip() == "--":
            break
        cleaned.append(line)
    # nettoyer lignes vides multiples
    text = "\n".join(cleaned)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def has_attachment(message):
    return any(
        part.get_content_disposition() == "attachment"
        for part in message.walk()
    )

def process_email(message):
    """Process an email message and return its JSON representation."""
    body_raw = extract_body(message)
    body_clean = clean_body(body_raw)
    body_clean = re.sub(r'(?<!\S)[^\s]{' + str(15 + 1) + r',}(?!\S)', '', body_clean)  
    body_clean = re.sub(r'[^\x00-\xFF]', '', body_clean) # supprime tous les caractères spéciaux 
    body_clean = re.sub(r'[\n\xa0]', '.', body_clean)
    body_clean = re.sub(r' +', ' ', body_clean) # Remove multiple spaces left by long word removal
    out = {
        "from": message.get("From"),
        "subject": message.get("Subject"),
        "date": message.get("Date"),
        "body": body_clean,
    }
    return json.dumps(out, ensure_ascii=False, indent=2)



def process_mbox(mbox_path):
    """Traite un fichier mbox et convertit chaque email en JSON."""
    if not os.path.isfile(mbox_path):
        logging.info(f"Erreur : pas de mbox à {mbox_path}")
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
        # Load mbox configuration from centralized configuration
        mbox_config = get_config_value("mbox", {})
        mbox_src = mbox_config.get("SRC") if isinstance(mbox_config, dict) else None
        mbox_path = mbox_config.get("path") if isinstance(mbox_config, dict) else None

        # Validate that both SRC and path are defined
        if not (mbox_src and mbox_path):
            return {"error": "SRC ou path non défini"}

        mbox_path = os.path.expanduser(mbox_path)

        # Capture l'output de process_mbox
        from io import StringIO
        import sys
        # Redirige stdout pour capturer l'output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        process_mbox(f"{mbox_path}/{mbox_src}")
        # Rétablit stdout
        sys.stdout = old_stdout
        prompt = "écrit un résumé de 80 mots pour chacun des emails qui suivent : "
        output = captured_output.getvalue().strip()
        combined = f"{prompt}\n{output}" if output else prompt
        return {"output": combined}
    except Exception as exc:
        return {"error": f"exécution échouée : {exc} {mbox_src} {mbox_path}"}
