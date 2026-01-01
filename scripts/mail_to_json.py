#!/usr/bin/env python3

import logging
import sys
import json
import email
from email import policy
from datetime import datetime
import re
from html import unescape
from lxml import html as lxml_html
from lxml.html.clean import Cleaner


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

msg = email.message_from_file(sys.stdin, policy=policy.default)

# ----------------------------------------------------------------------------------------------

def clean_message(message):
    # -------------------------------------------------
    # 1️⃣ Read and decode the HTML payload
    # -------------------------------------------------
    try:
        payload_bytes = message.get_payload(decode=True)
        charset = message.get_content_charset() or "utf-8"
        html_text = payload_bytes.decode(charset, errors="replace")
    except Exception:
        logging.info(payload_bytes)
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
        scripts=True,            # Remove <script> elements
        javascript=True,         # Remove javascript: URLs
        style=True,              # Remove <style> elements and their content
        comments=True,           # Remove HTML comments
        page_structure=False,    # Keep structural tags like <body>, <div>
        safe_attrs_only=False,  # Keep most attributes (we’ll strip style later)
        remove_tags=[
            "head", "title", "meta", "link",      # Metadata tags
            "iframe", "object", "embed", "svg",   # Embedded objects
             "table", "tr", "td", "th", "tbody", "thead", "tfoot"
        ],                         # Remove table structures (keep inner text later)
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
    """
    Recursively walk the message tree and return the first suitable plain‑text part.
    If no plain‑text part exists, fall back to the first HTML part and extract
    visible text using lxml.

    :param message: the parsed email message
    :return: text body
    """
    logging.info("Nouveau message")
    # Base case – if this is a leaf node
    if not message.is_multipart():
        if message.get_content_type() == "text/plain":
            payload = message.get_payload(decode=True)
            charset = message.get_content_charset() or "utf-8"
            return payload.decode(charset, errors="replace")
        if message.get_content_type() == "text/html":
            logging.info("appel leaf")
            clean_message(message)

    # Recursive case – walk the children
    for part in message.walk():
        if not part.is_multipart():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                charset = part.get_content_charset() or "utf-8"
                return payload.decode(charset, errors="replace")
            if part.get_content_type() == "text/html":
                logging.info("appel multipart")
                # clean_message(message)

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


body_raw = extract_body(msg)
body_clean = clean_body(body_raw)
body_clean = re.sub( r'(?<!\S)[^\s]{' + str(15 + 1) + r',}(?!\S)', '', body_clean )

out = {
    #"id": msg.get("Message-ID"),
    "from": msg.get("From"),
    #"to": msg.get("To"),
    #"cc": msg.get("Cc"),
    "subject": msg.get("Subject"),
    "date": msg.get("Date"),
    "body": body_clean,
    #"signals": {
    #    "length": len(body_clean),
    #    "has_attachment": has_attachment(msg),
    #    "direct": msg.get("Cc") is None
    #}
}

print(json.dumps(out, ensure_ascii=False))
