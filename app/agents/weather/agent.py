from app.agents.base_agent import BaseAgent
from typing import Dict, Any
from app.data.local_data import get_region_by_name
from .prompt import get_system_prompt
from .tools import format_weather_data

class WeatherAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="WeatherAgent",
            description="Expert en climatologie et météo agricole pour le Cameroun. Fournit des prévisions (simulées) et des conseils climatiques par région."
        )

    async def process(self, query: str, context: Dict[str, Any]) -> str:
        # Récupération de la région du contexte
        region_name = context.get('region', 'Centre')
        region_info = get_region_by_name(region_name)
        
        # Récupération météo réelle et outils
        from .tools import (
            fetch_weather_data, 
            format_weather_data, 
            get_weather_forecast, 
            get_irrigation_advice,
            get_climate_alerts,
            analyze_rainfall_patterns
        )
        
        real_weather = fetch_weather_data(region_name)
        weather_desc = format_weather_data(real_weather)
        forecast = get_weather_forecast(region_name)
        irrigation = get_irrigation_advice(region_name)
        alerts = get_climate_alerts(region_name)
        patterns = analyze_rainfall_patterns(region_name)

        region_desc = "Région inconnue"
        if region_info:
            region_desc = (
                f"{region_info.name} (Capitale: {region_info.capital}).\n"
                f"Climat: {region_info.climate_description}.\n"
                f"Conditions actuelles: {weather_desc}\n"
                f"Prévisions:\n{forecast}\n"
                f"Conseils Irrigation: {irrigation}\n"
                f"Alertes: {alerts}\n"
                f"Analyse Pluie: {patterns}"
            )

        system_prompt = get_system_prompt(region_desc)
        
        return await self.llm_service.generate_response(query, system_prompt)
