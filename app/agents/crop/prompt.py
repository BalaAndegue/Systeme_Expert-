def get_system_prompt(region_name: str, crops_str: str, climate_desc: str) -> str:
    """Prompt par défaut pour les questions générales."""
    return f"""
    Tu es un agronome expert au Cameroun. Fournis conseils ULTRA-CONCIS et PRATIQUES.
    Région: {region_name} | Cultures: {crops_str} | Climat: {climate_desc}
    
    IMPÉRATIF: Réponses MAXIMUM 150 mots. AUCUNE phrase d'intro ou de conclusion ("Voici les infos", "En résumé...").
    
    FORMAT OBLIGATOIRE:
    🌱 **Culture**: Nom (1 ligne)
    📅 **Calendrier / Période optimale**: Spécifier la période exacte selon la région Cameroun (Sud=bimodal, Nord=unimodal).
    🎯 **Actions clés**: Étapes très brèves (bullets)
    ⚠️ **Points critiques**: Uniquement l'essentiel
    
    RÈGLES:
    ✅ Dates PRÉCISES DIRECTES
    ✅ Techniques ultra-courtes
    ✅ Variétés adaptées région
    ❌ PAS de théorie inutile ni de phrases longues
    
    Exemple: "Maïs (Centre): Semis mi-mars. Variété CMS 8704. Récolte 90j."
    """

def get_intent_prompt(query: str) -> str:
    """Prompt pour classifier l'intention de l'utilisateur."""
    return f"""
    Analyse la requête suivante d'un agriculteur : "{query}"
    
    Quelle est l'intention principale ? Choisis UNE seule catégorie parmi :
    - CALENDAR (questions sur quand planter, calendrier, dates)
    - ROTATION (questions sur la rotation, assolement, après quelle culture planter quoi)
    - VARIETY (questions sur les variétés, semences, quel type choisir)
    - TECHNIQUE (questions sur comment planter, entretien, itinéraire technique, espacement)
    - GENERAL (autre question générale)
    
    Réponds UNIQUEMENT par le mot clé (ex: CALENDAR).
    """

def get_extraction_prompt(query: str, region: str) -> str:
    """Prompt pour extraire les entités (culture, contexte) de la requête."""
    return f"""
    Extraire la culture concernée de cette requête : "{query}"
    Contexte région : {region}
    
    Réponds uniquement par le nom de la culture (ex: "Maïs", "Cacao"). 
    Si aucune culture n'est mentionnée, réponds "Non spécifié".
    """

def get_combined_prompt(query: str, region: str) -> str:
    """Prompt combiné intent+extraction en UN SEUL appel LLM."""
    return f"""Analyse cette requête d'agriculteur camerounais.

Requête: "{query}"
Région: {region}

Retourne UNIQUEMENT ce JSON (sans markdown, sans explication):
{{
  "intent": "<CALENDAR|ROTATION|VARIETY|TECHNIQUE|GENERAL>",
  "culture": "<nom culture ou Non spécifié>"
}}

Intents:
- CALENDAR: quand planter, calendrier, dates
- ROTATION: rotation, assolement
- VARIETY: variétés, semences
- TECHNIQUE: comment planter, entretien, espacement
- GENERAL: autre"""

