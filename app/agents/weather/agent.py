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
    get_optimal_planting_conditions
)


class WeatherAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="WeatherAgent",
            description="Expert météorologue agricole pour le Cameroun. Fournit données météo RÉELLES (API Open-Meteo), prévisions, conseils irrigation et alertes climatiques."
        )

    async def process(self, query: str, context: Dict[str, Any]) -> str:
        # Récupération de la région
        region_name = context.get('region', 'Centre')
        region_info = get_region_by_name(region_name)
        
        # 1. Intent + Culture en UN SEUL appel LLM (optimisation latence)
        combined_prompt = get_combined_prompt(query)
        combined_json = await self.llm_service.generate_response(combined_prompt)
        
        try:
            cleaned = combined_json.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(cleaned)
            intent = parsed.get("intent", "GENERAL").strip().upper()
            culture = parsed.get("culture", "Non spécifié").strip()
        except Exception:
            # Fallback: tenter de lire l'intent directement
            intent = "GENERAL"
            culture = "Non spécifié"
        
        # Validation intent
        valid_intents = ["CURRENT", "FORECAST", "IRRIGATION", "PLANTING", "ALERT", "GENERAL"]
        if intent not in valid_intents:
            intent = "GENERAL"
        
        print(f"DEBUG WeatherAgent: Intent={intent}, Region={region_name}")
        
        # 2. Construction contexte régional
        region_desc = f"{region_name}"
        if region_info:
            region_desc += f" (Climat: {region_info.climate_description})"
        
        # 3. Dispatching vers outils selon intention (appels API météo, non-LLM)
        weather_data = ""
        
        if intent == "CURRENT":
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
