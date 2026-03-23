from app.agents.base_agent import BaseAgent
from typing import Dict, Any
import json
from .prompt import get_system_prompt, get_combined_prompt
from .tools import (
    calculate_npk_requirements,
    get_organic_fertilizers,
    diagnose_nutrient_deficiency,
    get_application_schedule,
    get_soil_amendment_advice,
    calculate_compost_recipe
)


class FertilizerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="FertilizerAgent",
            description="Expert en fertilisation au Cameroun. Calcule besoins NPK, recommande engrais organiques/chimiques, diagnostique carences, conseille sur compost et amendements."
        )

    async def process(self, query: str, context: Dict[str, Any]) -> str:
        # 1. Récupération contexte
        region_name = context.get('region', 'Cameroun')
        
        # 2. Intent + Extraction en UN SEUL appel LLM (optimisation latence)
        combined_prompt = get_combined_prompt(query)
        combined_json = await self.llm_service.generate_response(combined_prompt)
        
        try:
            cleaned = combined_json.replace("```json", "").replace("```", "").strip()
            entities = json.loads(cleaned)
            intent = entities.get("intent", "GENERAL").strip().upper()
            culture = entities.get("culture", "Non spécifié").strip()
            area = float(entities.get("superficie_ha", 1.0))
            symptoms = entities.get("symptomes", "Non spécifié").strip()
            stage = entities.get("stade", "Non spécifié").strip()
        except Exception as e:
            print(f"Warning: Failed to parse combined JSON for FertilizerAgent: {e}")
            intent = "GENERAL"
            culture = "Non spécifié"
            area = 1.0
            symptoms = "Non spécifié"
            stage = "mature"
        
        # Validation intent
        valid_intents = ["NPK_CALC", "ORGANIC", "DEFICIENCY", "SCHEDULE", "SOIL", "GENERAL"]
        if intent not in valid_intents:
            intent = "GENERAL"
        
        if stage == "Non spécifié":
            stage = "mature"
        
        print(f"DEBUG FertilizerAgent: Intent={intent}, Culture={culture}")
        
        # 3. Dispatching vers outils
        tool_results = ""
        
        if intent == "NPK_CALC":
            npk_data = await calculate_npk_requirements(self.llm_service, culture, area, stage)
            tool_results = f"**Calcul NPK pour {culture}:**\n{json.dumps(npk_data, indent=2, ensure_ascii=False)}"
            if "besoins_npk_kg_ha" in npk_data:
                organic_recs = await get_organic_fertilizers(self.llm_service, npk_data["besoins_npk_kg_ha"], region_name)
                tool_results += f"\n\n**Engrais organiques:**\n{json.dumps(organic_recs, indent=2, ensure_ascii=False)}"
        
        elif intent == "ORGANIC":
            if culture != "Non spécifié":
                npk_data = await calculate_npk_requirements(self.llm_service, culture, area, stage)
                if "besoins_npk_kg_ha" in npk_data:
                    organic_recs = await get_organic_fertilizers(self.llm_service, npk_data["besoins_npk_kg_ha"], region_name)
                    tool_results = f"**Engrais organiques pour {culture}:**\n{json.dumps(organic_recs, indent=2, ensure_ascii=False)}"
            else:
                compost = await calculate_compost_recipe(self.llm_service, 2.0)
                tool_results = f"**Recette compost:**\n{json.dumps(compost, indent=2, ensure_ascii=False)}"
        
        elif intent == "DEFICIENCY":
            diagnosis = await diagnose_nutrient_deficiency(self.llm_service, symptoms, culture)
            tool_results = f"**Diagnostic carence:**\n{json.dumps(diagnosis, indent=2, ensure_ascii=False)}"
        
        elif intent == "SCHEDULE":
            if culture != "Non spécifié":
                npk_data = await calculate_npk_requirements(self.llm_service, culture, area, stage)
                if "besoins_totaux_kg" in npk_data:
                    schedule = await get_application_schedule(self.llm_service, culture, npk_data["besoins_totaux_kg"])
                    tool_results = f"**Calendrier application {culture}:**\n{json.dumps(schedule, indent=2, ensure_ascii=False)}"
            else:
                tool_results = "Culture non spécifiée. Précisez pour calendrier personnalisé."
        
        elif intent == "SOIL":
            soil_type = context.get('soil_type', 'ferralitique')
            soil_advice = await get_soil_amendment_advice(self.llm_service, soil_type, culture)
            tool_results = f"**Amendements sol {soil_type}:**\n{json.dumps(soil_advice, indent=2, ensure_ascii=False)}"
        
        else:  # GENERAL
            if culture != "Non spécifié":
                npk_data = await calculate_npk_requirements(self.llm_service, culture, area, stage)
                tool_results = f"**Infos générales {culture}:**\n{json.dumps(npk_data, indent=2, ensure_ascii=False)}"
            else:
                compost = await calculate_compost_recipe(self.llm_service, 1.0)
                tool_results = f"**Conseils fertilisation:**\n{json.dumps(compost, indent=2, ensure_ascii=False)}"
        
        # 4. Construction prompt final (synthèse directe, pas de condensation)
        system_prompt = get_system_prompt()
        
        full_prompt = f"""{system_prompt}

DONNÉES OUTILS:
{tool_results}

QUESTION: {query}
RÉGION: {region_name}

Réponds de manière CONCISE (Max 150 mots) avec CHIFFRES PRÉCIS. Format avec icônes et structure claire."""

        return await self.llm_service.generate_response(full_prompt)
