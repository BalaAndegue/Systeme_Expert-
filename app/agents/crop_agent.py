from app.agents.base_agent import BaseAgent
from typing import Dict, Any
from app.data.local_data import get_region_by_name
from app.data.planting_calendar import get_planting_info

class CropAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="CropAgent",
            description="Agronome expert spécialisé dans les cultures camerounaises (Cacao, Café, Coton, Vivriers). Donne des conseils sur les itinéraires techniques, les semis et les récoltes."
        )

    async def process(self, query: str, context: Dict[str, Any]) -> str:
        region_name = context.get('region', 'Centre')
        # Simple extraction de culture potentielle du contexte (si existant) ou on laisse Gemini gérer
        
        # Injection de données statiques pertinentes
        # On pourrait faire un pré-parsing pour savoir de quelle culture on parle exactement
        # Pour l'instant, on donne le contexte régional global
        region_info = get_region_by_name(region_name)
        crops_str = ", ".join(region_info.major_crops) if region_info else "Toutes cultures"

        system_prompt = f"""
        Tu es un agronome expert au Cameroun.
        Région actuelle : {region_name}.
        Cultures principales de la région : {crops_str}.
        
        Utilise tes connaissances générales sur l'agriculture tropicale ET les spécificités locales.
        Si l'utilisateur demande "quand planter", réfère-toi aux saisons des pluies de la région ({region_info.climate_description if region_info else ''}).
        
        """
        
        return await self.llm_service.generate_response(query, system_prompt)
