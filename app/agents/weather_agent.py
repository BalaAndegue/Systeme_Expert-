from app.agents.base_agent import BaseAgent
from typing import Dict, Any
from app.data.local_data import get_region_by_name

class WeatherAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="WeatherAgent",
            description="Expert en climatologie et météo agricole pour le Cameroun. Fournit des prévisions (simulées) et des conseils climatiques par région."
        )

    async def process(self, query: str, context: Dict[str, Any]) -> str:
        # Récupération de la région du contexte ou extraction simple
        region_name = context.get('region', 'Centre') # Défaut Centre
        region_info = get_region_by_name(region_name)
        
        region_desc = "Région inconnue"
        if region_info:
            region_desc = f"{region_info.name} (Capitale: {region_info.capital}). Climat: {region_info.climate_description}"

        system_prompt = f"""
        Tu es l'agent météo spécialisé pour le Cameroun.
        La région concernée est : {region_desc}.
        
        Si l'utilisateur demande la météo "actuelle", invente une prévision plausible pour la saison actuelle au Cameroun.
        Donne des conseils agricoles liés à ce climat (irrigation, risques de maladies liés à l'humidité).
        """
        
        return await self.llm_service.generate_response(query, system_prompt)
