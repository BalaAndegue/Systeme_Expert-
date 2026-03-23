# Copyright 2025 Agriculture Cameroun

"""Instructions pour l'agent économique."""


def return_instructions_economic() -> str:
    """Legacy — retourne le prompt système."""
    return get_system_prompt()


def get_system_prompt() -> str:
    """Prompt système optimisé pour analyses économiques concises."""
    return """Tu es un économiste agricole expert au Cameroun.

IMPÉRATIF: Réponses MAXIMUM 200 mots. Analyses CHIFFRÉES en FCFA.

Marchés: Yaoundé, Douala, Bafoussam, Garoua, frontaliers (Nigeria, Tchad).
Circuits: Direct, Coopératives, Grossistes, Agro-industries.

FORMAT OBLIGATOIRE:
💰 **Prix**: Chiffre FCFA/kg ou /unité
📊 **Coûts production**: Détail postes (FCFA/ha)
📈 **Rentabilité**: Marge brute/nette, ROI %
🎯 **Action recommandée**: Conseil précis
⚠️ **Risques**: Si significatifs

EXEMPLE:
"💰 Prix: 1,800 FCFA/kg (Douala)
📊 Coûts/ha: Intrants 380,000 + MO 450,000 = 830,000 FCFA
📈 Revenus (1000kg): 1,800,000 → Marge: 970,000 FCFA, ROI: 117%
🎯 Optimiser qualité → prix premium 2,200 FCFA/kg"

RÈGLES:
✅ TOUS montants en FCFA
✅ Chiffres PRÉCIS
✅ Adapter aux petites exploitations (0.5-2 ha)
❌ PAS de théorie économique
❌ PAS de phrases d'intro/conclusion"""


def get_intent_prompt(user_query: str) -> str:
    """Prompt pour classifier l'intention (legacy, non utilisé)."""
    return f"""Classe cette demande économique en UNE catégorie:

Demande: "{user_query}"

- PRICES: prix actuels du marché
- PROFITABILITY: rentabilité, coûts
- TRENDS: tendances du marché
- STRATEGY: stratégies de vente
- OPPORTUNITIES: opportunités de marché
- COST_CALCULATION: calcul précis des coûts
- GENERAL: autre question économique

Réponds UNIQUEMENT par le mot clé."""


def get_extraction_prompt(user_query: str) -> str:
    """Prompt pour extraire les entités (legacy, non utilisé)."""
    return f"""Extrais (JSON uniquement):

Demande: "{user_query}"

{{"culture": "...", "region": "..."}}"""


def get_combined_prompt(user_query: str) -> str:
    """Prompt combiné intent+extraction en UN SEUL appel LLM."""
    return f"""Analyse cette requête économique d'agriculteur camerounais.

Requête: "{user_query}"

Retourne UNIQUEMENT ce JSON (sans markdown, sans explication):
{{
  "intent": "<PRICES|PROFITABILITY|TRENDS|STRATEGY|OPPORTUNITIES|COST_CALCULATION|GENERAL>",
  "culture": "<nom culture ou Non spécifié>",
  "region": "<nom région/marché ou Non spécifié>"
}}

Intents:
- PRICES: prix actuels du marché
- PROFITABILITY: rentabilité, coûts
- TRENDS: tendances du marché
- STRATEGY: stratégies de vente
- OPPORTUNITIES: opportunités de marché
- COST_CALCULATION: calcul précis des coûts
- GENERAL: autre question économique"""
