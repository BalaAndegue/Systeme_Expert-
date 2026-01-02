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
        
        # Récupération météo réelle
        from .tools import fetch_weather_data, format_weather_data
        real_weather = fetch_weather_data(region_name)
        weather_desc = format_weather_data(real_weather)

        region_desc = "Région inconnue"
        if region_info:
            region_desc = f"{region_info.name} (Capitale: {region_info.capital}). Climat: {region_info.climate_description}. Météo actuelle: {weather_desc}"

        system_prompt = get_system_prompt(region_desc)
        
        return await self.llm_service.generate_response(query, system_prompt)
