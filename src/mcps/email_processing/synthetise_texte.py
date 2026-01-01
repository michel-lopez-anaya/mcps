#!/usr/bin/env python3


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

