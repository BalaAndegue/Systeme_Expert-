from app.agents.base_agent import BaseAgent
from typing import Dict, Any
import json
from app.data.local_data import get_region_by_name
from .prompt import get_system_prompt, get_combined_prompt, get_intent_prompt, get_extraction_prompt
from .tools import (
    fetch_weather_data,
    format_weather_data,
    get_agricultural_weather_summary,
    get_weather_forecast,
    get_irrigation_advice,
    get_climate_alerts,
    analyze_rainfall_patterns,
    get_frost_risk,
    get_optimal_planting_conditions,
    get_crop_monitoring_plan,
    REGION_COORDINATES,
)


def _normalize_region(region_name: str) -> str:
    """Normalise le nom de région (case-insensitive, gestion accents)."""
    # Correspondance exacte d'abord
    for key in REGION_COORDINATES:
        if key.lower() == region_name.lower():
            return key
    # Correspondance partielle
    for key in REGION_COORDINATES:
        if region_name.lower() in key.lower() or key.lower() in region_name.lower():
            return key
    # Fallback
    return "Centre"


class WeatherAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="WeatherAgent",
            description="Expert météorologue agricole pour le Cameroun. Fournit données météo RÉELLES (API Open-Meteo), prévisions 14j, plans de suivi sur période (7j/1 mois), conseils irrigation et alertes climatiques."
        )

    async def process(self, query: str, context: Dict[str, Any]) -> str:
        # Récupération et normalisation de la région
        raw_region = context.get('region', 'Centre')
        region_name = _normalize_region(raw_region)
        region_info = get_region_by_name(region_name)
        
        # 1. Intent + Culture + Période en UN SEUL appel LLM
        combined_prompt = get_combined_prompt(query)
        combined_json = await self.llm_service.generate_response(combined_prompt)
        
        try:
            cleaned = combined_json.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(cleaned)
            intent = parsed.get("intent", "GENERAL").strip().upper()
            culture = parsed.get("culture", "Non spécifié").strip()
            period_days = int(parsed.get("period_days", 7))
        except Exception:
            intent = "GENERAL"
            culture = "Non spécifié"
            period_days = 7
        
        # Validation intent
        valid_intents = ["CURRENT", "FORECAST", "IRRIGATION", "PLANTING", "ALERT", "MONITORING", "GENERAL"]
        if intent not in valid_intents:
            intent = "GENERAL"
        
        # Validation period_days
        if period_days not in [7, 14, 30]:
            period_days = 30 if period_days > 14 else 7
        
        print(f"DEBUG WeatherAgent: Intent={intent}, Region={region_name}, Culture={culture}, Period={period_days}j")
        
        # 2. Construction contexte régional
        region_desc = f"{region_name}"
        if region_info:
            region_desc += f" (Climat: {region_info.climate_description})"
        
        # 3. Dispatching vers outils
        weather_data = ""
        
        if intent == "MONITORING":
            # Plan de suivi sur période avec données réelles jour par jour
            monitoring_plan = get_crop_monitoring_plan(region_name, culture, period_days)
            # Pour MONITORING, on retourne directement le plan structuré
            # sans passer par le LLM final (le plan est déjà très structuré)
            system_prompt = get_system_prompt(region_desc)
            full_prompt = f"""{system_prompt}

PLAN DE SUIVI MÉTÉO-AGRONOMIQUE (données réelles Open-Meteo):
{monitoring_plan}

QUESTION: {query}

Présente ce plan de suivi de manière claire et actionnable. 
Garde TOUTES les données chiffrées (températures, mm de pluie, dates).
Ajoute des conseils agronomiques spécifiques à {culture} pour chaque semaine.
Maximum 400 mots."""
            return await self.llm_service.generate_response(full_prompt)
        
        elif intent == "CURRENT":
            summary = get_agricultural_weather_summary(region_name)
            alerts = get_climate_alerts(region_name)
            weather_data = f"{summary}\n{alerts}"
            
        elif intent == "FORECAST":
            forecast = get_weather_forecast(region_name)
            patterns = analyze_rainfall_patterns(region_name)
            alerts = get_climate_alerts(region_name)
            weather_data = f"**Prévisions:**\n{forecast}\n\n**Tendance pluie:**\n{patterns}\n\n**Alertes:**\n{alerts}"
            
        elif intent == "IRRIGATION":
            irrigation = get_irrigation_advice(region_name)
            summary = get_agricultural_weather_summary(region_name)
            patterns = analyze_rainfall_patterns(region_name)
            weather_data = f"{irrigation}\n\n**Contexte:**\n{summary}\n{patterns}"
            
        elif intent == "PLANTING":
            planting = get_optimal_planting_conditions(region_name, culture)
            forecast = get_weather_forecast(region_name)
            frost = get_frost_risk(region_name)
            weather_data = f"**Évaluation plantation {culture}:**\n{planting}\n\n**Prévisions:**\n{forecast}\n\n{frost}"
            
        elif intent == "ALERT":
            alerts = get_climate_alerts(region_name)
            frost = get_frost_risk(region_name)
            forecast = get_weather_forecast(region_name)
            weather_data = f"{alerts}\n\n{frost}\n\n**Prévisions courtes:**\n{forecast}"
            
        else:  # GENERAL
            summary = get_agricultural_weather_summary(region_name)
            alerts = get_climate_alerts(region_name)
            patterns = analyze_rainfall_patterns(region_name)
            weather_data = f"{summary}\n{alerts}\n{patterns}"
        
        # 4. Appel LLM final avec données météo réelles
        system_prompt = get_system_prompt(region_desc)
        
        full_prompt = f"""{system_prompt}

DONNÉES MÉTÉO RÉELLES (Open-Meteo API):
{weather_data}

QUESTION: {query}

Réponds de manière CONCISE (Max 150 mots) en utilisant le FORMAT OBLIGATOIRE."""

        return await self.llm_service.generate_response(full_prompt)
