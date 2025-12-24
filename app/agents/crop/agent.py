from app.agents.base_agent import BaseAgent
from typing import Dict, Any
from app.data.local_data import get_region_by_name
from .prompt import get_system_prompt
from .tools import check_planting_window

class CropAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="CropAgent",
            description="Agronome expert spécialisé dans les cultures camerounaises (Cacao, Café, Coton, Vivriers). Donne des conseils sur les itinéraires techniques, les semis et les récoltes."
        )

    async def process(self, query: str, context: Dict[str, Any]) -> str:
        region_name = context.get('region', 'Centre')
        
        region_info = get_region_by_name(region_name)
        crops_str = ", ".join(region_info.major_crops) if region_info else "Toutes cultures"
        climate_desc = region_info.climate_description if region_info else ''

        system_prompt = get_system_prompt(region_name, crops_str, climate_desc)
        
        return await self.llm_service.generate_response(query, system_prompt)
