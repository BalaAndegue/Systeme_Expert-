def get_system_prompt() -> str:
    return """Tu es un expert en fertilisation au Cameroun.

IMPÉRATIF: Réponses MAXIMUM 150 mots. AUCUNE phrase d'intro. Chiffres et dosages EXACTS.

FORMAT OBLIGATOIRE:
📊 **NPK**: Chiffres exacts kg/ha
🌿 **Engrais**: Noms locaux + doses EXACTES
💰 **Coûts**: FCFA
📅 **Planning**: Fractionnement
⚠️ **Attention**: Très bref

EXEMPLE:
"📊 Besoins: 80kg N, 40kg P, 120kg K/ha
🌿 Fientes volailles: 2.7t (80N-68P-41K) - 67,500 FCFA
📅 3 apports: début/mi/fin saison pluies
📍 Couronne 25cm du tronc, après pluie"

RÈGLES:
✅ Doses PRÉCISES (kg/ha, tonnes)
✅ Prix FCFA
✅ Timing EXPLICITE
❌ PAS de théorie
❌ PAS de phrases d'intro/conclusion"""


def get_combined_prompt(query: str) -> str:
    """Prompt combiné intent+extraction en UN SEUL appel LLM."""
    return f"""Analyse cette requête fertilisation d'agriculteur camerounais.

Requête: "{query}"

Retourne UNIQUEMENT ce JSON (sans markdown, sans explication):
{{
  "intent": "<NPK_CALC|ORGANIC|DEFICIENCY|SCHEDULE|SOIL|GENERAL>",
  "culture": "<nom culture ou Non spécifié>",
  "superficie_ha": <nombre ou 1.0>,
  "symptomes": "<description ou Non spécifié>",
  "stade": "<jeune/mature/vieux ou Non spécifié>"
}}

Intents:
- NPK_CALC: calcul besoins NPK, dosages engrais
- ORGANIC: engrais organiques, compost
- DEFICIENCY: carences, symptômes, diagnostic
- SCHEDULE: calendrier application, timing
- SOIL: type sol, amendements, chaux
- GENERAL: autre fertilisation"""


def get_intent_prompt(query: str) -> str:
    """Détecte intention pour fertilization queries (legacy, non utilisé)."""
    return f"""Classe cette question fertilisation en UNE catégorie:

Question: "{query}"

Catégories:
- NPK_CALC: Calcul besoins NPK, dosages
- ORGANIC: Engrais organiques, compost
- DEFICIENCY: Carences, symptômes, diagnostic
- SCHEDULE: Calendrier application, timing
- SOIL: Type sol, amendements, chaux
- GENERAL: Autre fertilisation

Réponds UNIQUEMENT le mot-clé (ex: NPK_CALC)"""


def get_extraction_prompt(query: str) -> str:
    """Extrait culture, superficie et symptômes (legacy, non utilisé)."""
    return f"""Extrais informations clés (JSON uniquement):

Question: "{query}"

Format exact:
{{"culture": "nom culture OU Non spécifié", "superficie_ha": nombre OU 1.0, "symptômes": "description OU Non spécifié", "stade": "jeune/mature/vieux OU Non spécifié"}}

Exemples:
"Engrais pour 2ha cacao?" → {{"culture": "cacao", "superficie_ha": 2.0, "symptômes": "Non spécifié", "stade": "Non spécifié"}}
"Feuilles jaunes sur maïs jeune" → {{"culture": "maïs", "superficie_ha": 1.0, "symptômes": "feuilles jaunes", "stade": "jeune"}}"""
