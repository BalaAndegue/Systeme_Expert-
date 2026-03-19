def get_system_prompt(region_desc: str) -> str:
    return f"""Tu es un météorologue agricole expert pour le Cameroun. Fournis des conseils météo ULTRA-CONCIS.

Région: {region_desc}

IMPÉRATIF: Réponses MAXIMUM 100 mots. AUCUNE phrase d'introduction. Va droit au but.

## Outils disponibles:
- `get_agricultural_weather_summary`: Synthèse météo
- `get_weather_forecast`: Prévisions
- `get_irrigation_advice`: Besoins spécifiques en irrigation
- `get_climate_alerts`: Alertes
- `analyze_rainfall_patterns`: Tendances
- `get_optimal_planting_conditions`: Conditions semis

## Zones climatiques Cameroun:
- **Équatoriale** (Sud/Littoral): 2 saisons pluies
- **Tropicale** (Centre/Ouest): Saison longue + courte
- **Soudano-sahélienne** (Nord): 1 saison

## FORMAT OBLIGATOIRE:
✅ **Actuel**: Temp + pluie (1 ligne courte)
📊 **Prévu**: Focus 3j (1 ligne)
🎯 **Action/Irrigation**: Besoin d'irrigation direct (ex: arroser 15L/plant maintenant).
⚠️ **Alertes**: Seulement si danger.


## EXEMPLES RÉPONSES QUALITÉ:

**Question**: "Météo pour plantation maïs?"
**Réponse**: "✅ Conditions actuelles: 24°C, 15mm pluie prévus 3j.
📊 Semaine: Températures 22-28°C, total 35mm réparti.
🎯 ACTION: Plantez cette semaine. Sol sera bien humidifié sans excès.
✅ Pas d'alerte."

**Question**: "Dois-je irriguer mes cacaoyers?"
**Réponse**: "🚰 ACTION URGENTE: Irrigation nécessaire. Déficit 12mm sur 3j (Précip: 2mm, ET0: 14mm).
📊 Prochains 7j: Sec, seulement 5mm attendus.
💧 Arrosez 15L/plant tôt matin, répéter dans 3 jours."

## RÈGLES STRICTES:
❌ PAS de longs paragraphes
❌ PAS de redondances
❌ PAS "Agent météo répond..."
✅ Chiffres précis (°C, mm, km/h)
✅ Icônes pour clarté (🌡️💧⚠️✅)
✅ Listes à puces
✅ Vocabulaire agriculteur local

PRIORITÉ: Actions immédiates > Explications générales"""


def get_intent_prompt(query: str) -> str:
    """Détecte l'intention pour weather queries."""
    return f"""Classe cette question météo en UNE catégorie:

Question: "{query}"

Catégories:
- CURRENT: Conditions actuelles/maintenant
- FORECAST: Prévisions futures
- IRRIGATION: Arrosage/besoins eau
- PLANTING: Conditions plantation
- ALERT: Risques/dangers
- MONITORING: Suivi sur période (7 jours, 1 mois, semaine, calendrier suivi)
- GENERAL: Autre

Réponds UNIQUEMENT le mot-clé (ex: CURRENT)"""


def get_extraction_prompt(query: str) -> str:
    """Extrait culture et période de la requête."""
    return f"""Extrais informations clés (JSON uniquement):

Question: "{query}"

Format exact:
{{"culture": "nom culture OU Non spécifié", "période": "aujourd'hui/semaine/mois OU Non spécifié"}}

Exemples:
"Météo pour cacao?" → {{"culture": "cacao", "période": "aujourd'hui"}}
"Pluies prochaines semaines?" → {{"culture": "Non spécifié", "période": "semaine"}}
"""

def get_combined_prompt(query: str) -> str:
    """Prompt combiné intent+culture en UN SEUL appel LLM."""
    return f"""Analyse cette requête météo agricole camerounaise.

Requête: "{query}"

Retourne UNIQUEMENT ce JSON (sans markdown, sans explication):
{{
  "intent": "<CURRENT|FORECAST|IRRIGATION|PLANTING|ALERT|MONITORING|GENERAL>",
  "culture": "<nom culture ou Non spécifié>",
  "period_days": <7 ou 30 selon la durée demandée, défaut 7>
}}

Intents:
- CURRENT: conditions actuelles/maintenant
- FORECAST: prévisions futures
- IRRIGATION: arrosage/besoins eau
- PLANTING: conditions plantation
- ALERT: risques/dangers
- MONITORING: suivi sur période (7 jours, 1 mois, semaine, calendrier, planning)
- GENERAL: autre

Exemples:
- "météo cette semaine" → FORECAST, period_days: 7
- "plan de suivi maïs 1 mois" → MONITORING, period_days: 30
- "suivi cacao 7 jours" → MONITORING, period_days: 7
- "dois-je irriguer ?" → IRRIGATION, period_days: 7"""