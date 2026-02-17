from app.agents.base_agent import BaseAgent
from typing import Dict, Any
from app.data.local_data import get_region_by_name
from .prompt import get_system_prompt, get_intent_prompt, get_extraction_prompt
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
import json


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
        
        # 1. Détection intention
        intent_prompt = get_intent_prompt(query)
        intent = await self.llm_service.generate_response(intent_prompt)
        intent = intent.strip().upper()
        
        # Nettoyage intention
        valid_intents = ["CURRENT", "FORECAST", "IRRIGATION", "PLANTING", "ALERT", "GENERAL"]
        found_intent = "GENERAL"
        for valid in valid_intents:
            if valid in intent:
                found_intent = valid
                break
        intent = found_intent
        
        print(f"DEBUG WeatherAgent: Intent={intent}, Region={region_name}")
        
        # 2. Extraction entités
        extract_prompt = get_extraction_prompt(query)
        extraction_json = await self.llm_service.generate_response(extract_prompt)
        
        try:
            cleaned = extraction_json.replace("```json", "").replace("```", "").strip()
            entities = json.loads(cleaned)
        except:
            entities = {"culture": "Non spécifié", "période": "Non spécifié"}
        
        culture = entities.get("culture", "Non spécifié")
        
        # 3. Construction contexte régional
        region_desc = f"{region_name}"
        if region_info:
            region_desc += f" (Climat: {region_info.climate_description})"
        
        # 4. Dispatching vers outils selon intention
        weather_data = ""
        
        if intent == "CURRENT":
            # Conditions actuelles
            summary = get_agricultural_weather_summary(region_name)
            alerts = get_climate_alerts(region_name)
            weather_data = f"{summary}\n{alerts}"
            
        elif intent == "FORECAST":
            # Prévisions détaillées
            forecast = get_weather_forecast(region_name)
            patterns = analyze_rainfall_patterns(region_name)
            alerts = get_climate_alerts(region_name)
            weather_data = f"**Prévisions:**\n{forecast}\n\n**Tendance pluie:**\n{patterns}\n\n**Alertes:**\n{alerts}"
            
        elif intent == "IRRIGATION":
            # Conseils irrigation
            irrigation = get_irrigation_advice(region_name)
            summary = get_agricultural_weather_summary(region_name)
            patterns = analyze_rainfall_patterns(region_name)
            weather_data = f"{irrigation}\n\n**Contexte:**\n{summary}\n{patterns}"
            
        elif intent == "PLANTING":
            # Conditions plantation
            planting = get_optimal_planting_conditions(region_name, culture)
            forecast = get_weather_forecast(region_name)
            frost = get_frost_risk(region_name)
            weather_data = f"**Évaluation plantation {culture}:**\n{planting}\n\n**Prévisions:**\n{forecast}\n\n{frost}"
            
        elif intent == "ALERT":
            # Focus alertes
            alerts = get_climate_alerts(region_name)
            frost = get_frost_risk(region_name)
            forecast = get_weather_forecast(region_name)
            weather_data = f"{alerts}\n\n{frost}\n\n**Prévisions courtes:**\n{forecast}"
            
        else:  # GENERAL
            # Synthèse complète mais concise
            summary = get_agricultural_weather_summary(region_name)
            alerts = get_climate_alerts(region_name)
            patterns = analyze_rainfall_patterns(region_name)
            weather_data = f"{summary}\n{alerts}\n{patterns}"
        
        # 5. Construction prompt final avec données
        system_prompt = get_system_prompt(region_desc)
        
        full_prompt = f"""{system_prompt}

DONNÉES MÉTÉO RÉELLES (Open-Meteo API):
{weather_data}

QUESTION: {query}

Réponds de manière CONCISE (Max 150 mots) en utilisant le FORMAT OBLIGATOIRE."""

        response = await self.llm_service.generate_response(full_prompt)
        
        # 6. Post-processing: vérifier longueur et ajuster si nécessaire
        word_count = len(response.split())
        if word_count > 200:
            # Trop long, demander synthèse
            condense_prompt = f"""Condense cette réponse à MAXIMUM 150 mots tout en gardant l'essentiel:

{response}

Format: Bullets, icônes, chiffres clés uniquement."""
            response = await self.llm_service.generate_response(condense_prompt)
        
        return response
