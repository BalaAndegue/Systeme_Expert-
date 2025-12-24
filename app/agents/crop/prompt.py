def get_system_prompt(region_name: str, crops_str: str, climate_desc: str) -> str:
    """Prompt par défaut pour les questions générales."""
    return f"""
    Tu es un agronome expert au Cameroun.
    Région actuelle : {region_name}.
    Cultures principales de la région : {crops_str}.
    
    Utilise tes connaissances générales sur l'agriculture tropicale ET les spécificités locales.
    Si l'utilisateur demande "quand planter", réfère-toi aux saisons des pluies de la région ({climate_desc}).
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
