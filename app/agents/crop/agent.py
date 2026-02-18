from app.agents.base_agent import BaseAgent
from typing import Dict, Any
import json
from app.data.local_data import get_region_by_name
from .prompt import get_system_prompt, get_combined_prompt, get_intent_prompt, get_extraction_prompt
from .tools import (
    get_planting_calendar, 
    get_crop_rotation_advice, 
    get_variety_recommendations, 
    get_cultivation_techniques
)

class CropAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="CropAgent",
            description="Agronome expert spécialisé dans les cultures camerounaises (Cacao, Café, Coton, Vivriers). Donne des conseils sur les itinéraires techniques, les semis et les récoltes."
        )

    async def process(self, query: str, context: Dict[str, Any]) -> str:
        # 1. Récupération du contexte
        region_name = context.get('region', 'Centre')
        region_info = get_region_by_name(region_name)
        
        # 2. Intent + Extraction en UN SEUL appel LLM (optimisation latence)
        combined_prompt = get_combined_prompt(query, region_name)
        combined_json = await self.llm_service.generate_response(combined_prompt)
        
        try:
            cleaned = combined_json.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(cleaned)
            intent = parsed.get("intent", "GENERAL").strip().upper()
            crop_name = parsed.get("culture", "Non spécifié").strip()
        except Exception as e:
            print(f"Warning: Failed to parse combined JSON for CropAgent: {e}")
            intent = "GENERAL"
            crop_name = "Non spécifié"
        
        # Validation de l'intent
        valid_intents = ["CALENDAR", "ROTATION", "VARIETY", "TECHNIQUE", "GENERAL"]
        if intent not in valid_intents:
            intent = "GENERAL"
        
        print(f"DEBUG: Intent detected by CropAgent: {intent}")

        if crop_name == "Non spécifié" and intent != "GENERAL":
            intent = "GENERAL"

        # 3. Dispatching vers les outils
        if intent == "CALENDAR":
            result = await get_planting_calendar(self.llm_service, crop_name, region_name)
            return f"Voici le calendrier de plantation pour le {crop_name} en région {region_name} :\n\n{result.get('calendar')}"
            
        elif intent == "ROTATION":
            soil_type = "Sol ferralitique standard" 
            if region_info and region_info.soil_types:
                soil_type = region_info.soil_types[0]
            result = await get_crop_rotation_advice(self.llm_service, crop_name, soil_type)
            return f"Conseils de rotation pour {crop_name} ({soil_type}) :\n\n{result.get('rotation_plan')}"
            
        elif intent == "VARIETY":
            result = await get_variety_recommendations(self.llm_service, crop_name, region_name)
            return f"Recommandations de variétés de {crop_name} pour la région {region_name} :\n\n{result.get('recommendations')}"
            
        elif intent == "TECHNIQUE":
            result = await get_cultivation_techniques(self.llm_service, crop_name)
            return f"Guide technique pour la culture du {crop_name} :\n\n{result.get('techniques')}"
            
        else:  # GENERAL
            crops_str = ", ".join(region_info.major_crops) if region_info else "Toutes cultures"
            climate_desc = region_info.climate_description if region_info else ''
            system_prompt = get_system_prompt(region_name, crops_str, climate_desc)
            return await self.llm_service.generate_response(query, system_prompt)
