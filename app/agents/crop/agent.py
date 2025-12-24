from app.agents.base_agent import BaseAgent
from typing import Dict, Any
from app.data.local_data import get_region_by_name
from .prompt import get_system_prompt, get_intent_prompt, get_extraction_prompt
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
        
        # 2. Détection de l'intention
        intent_prompt = get_intent_prompt(query)
        # Note: On utilise llm_service pour classifier. C'est un appel "interne".
        intent = await self.llm_service.generate_response(intent_prompt)
        intent = intent.strip().upper()
        
        # Nettoyage basique si le LLM est bavard
        for key in ["CALENDAR", "ROTATION", "VARIETY", "TECHNIQUE", "GENERAL"]:
            if key in intent:
                intent = key
                break
        
        print(f"DEBUG: Intent detected by CropAgent: {intent}")

        # 3. Extraction de la culture (si nécessaire pour les outils)
        # On le fait systématiquement car la plupart des outils en ont besoin
        extract_prompt = get_extraction_prompt(query, region_name)
        crop_name = await self.llm_service.generate_response(extract_prompt)
        crop_name = crop_name.strip()
        
        if "Non spécifié" in crop_name and intent != "GENERAL":
            # Si on a besoin d'une culture mais qu'on ne la trouve pas, on fallback sur GENERAL
            intent = "GENERAL"

        # 4. Dispatching vers les outils
        if intent == "CALENDAR":
            result = await get_planting_calendar(self.llm_service, crop_name, region_name)
            return f"Voici le calendrier de plantation pour le {crop_name} en région {region_name} :\n\n{result.get('calendar')}"
            
        elif intent == "ROTATION":
            # Pour simplifier, on suppose sol_type générique si non connu, ou on pourrait l'extraire du contexte
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
            
        else: # GENERAL
            # Fallback sur le comportement par défaut
            crops_str = ", ".join(region_info.major_crops) if region_info else "Toutes cultures"
            climate_desc = region_info.climate_description if region_info else ''
            system_prompt = get_system_prompt(region_name, crops_str, climate_desc)
            return await self.llm_service.generate_response(query, system_prompt)
