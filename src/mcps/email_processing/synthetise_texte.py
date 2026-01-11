#!/usr/bin/env python3


PROMPT_SYNTHESE = """
**OBJECTIF**: 
L'outil `perso.prepare_synthese` est conçu pour transmettre un texte que vous souhaitez synthétiser. Une fois le texte fourni, le LLM s’occupe de réaliser une synthèse structurée et concise en suivant les directives suivantes :

### Directives pour la synthèse
1. **Identifier l'essentiel** : Extraire les informations clés sans ajouter d'interprétations personnelles.
2. **Respecter la logique originale** : Conserver l'ordre des idées ou les organiser de manière cohérente.
3. **Être objective** : Éviter les jugements de valeur, sauf si le texte en contient.
4. **Être claire et précise** : Utiliser un langage simple et des phrases courtes.

### Structure de la synthèse
La synthèse sera organisée avec :
- Une section par information clé.
- Une hiérarchie des sections numérotées (I, II, III, ...).
- Les titres de niveau 2 introduits par un point.

### Fonctionnement
1. L'outil me transmet le texte à synthétiser contenu dans le clipboard.
2. Le LLM génère une synthèse structurée et concise en suivant les directives mentionnées ci-dessus.

**EXEMPLE** :                                                                       
Si l'entrée est :                                                                   
{                                                                                   
 "directive": "Synthèse",                                                            
 "texte": "ici se trouvera le texte fourni présent dans le clipboard ..."                                     
}                                                                                   

La sortie sera une synthèse structurée du texte fourni.  


"""

