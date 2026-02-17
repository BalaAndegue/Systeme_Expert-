from app.agents.base_agent import BaseAgent
from typing import Dict, Any
import json
from .prompt import get_system_prompt, get_intent_prompt, get_extraction_prompt
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
            description="Expert agronome en fertilisation et amendements des sols au Cameroun. Calcule besoins NPK, recommande engrais organiques/chimiques, diagnostique carences, conseille sur compost et amendements."
        )

    async def process(self, query: str, context: Dict[str, Any]) -> str:
        # 1. Récupération contexte
        region_name = context.get('region', 'Cameroun')
        
        # 2. Détection intention
        intent_prompt = get_intent_prompt(query)
        intent = await self.llm_service.generate_response(intent_prompt)
        intent = intent.strip().upper()
        
        valid_intents = ["NPK_CALC", "ORGANIC", "DEFICIENCY", "SCHEDULE", "SOIL", "GENERAL"]
        found_intent = "GENERAL"
        for valid in valid_intents:
            if valid in intent:
                found_intent = valid
                break
        intent = found_intent
        
        print(f"DEBUG FertilizerAgent: Intent={intent}")
        
        # 3. Extraction entités
        extract_prompt = get_extraction_prompt(query)
        extraction_json = await self.llm_service.generate_response(extract_prompt)
        
        try:
            cleaned = extraction_json.replace("```json", "").replace("```", "").strip()
            entities = json.loads(cleaned)
        except:
            entities = {"culture": "Non spécifié", "superficie_ha": 1.0, "symptômes": "Non spécifié", "stade": "mature"}
        
        culture = entities.get("culture", "Non spécifié")
        area = entities.get("superficie_ha", 1.0)
        symptoms = entities.get("symptômes", "Non spécifié")
        stage = entities.get("stade", "mature")
        
        # 4. Dispatching vers outils
        tool_results = ""
        
        if intent == "NPK_CALC":
            # Calcul besoins NPK
            npk_data = await calculate_npk_requirements(self.llm_service, culture, area, stage)
            tool_results = f"**Calcul NPK pour {culture}:**\n{json.dumps(npk_data, indent=2, ensure_ascii=False)}"
            
            # Ajouter recommandations organiques
            if "besoins_npk_kg_ha" in npk_data:
                organic_recs = await get_organic_fertilizers(self.llm_service, npk_data["besoins_npk_kg_ha"], region_name)
                tool_results += f"\n\n**Engrais organiques:**\n{json.dumps(organic_recs, indent=2, ensure_ascii=False)}"
        
        elif intent == "ORGANIC":
            # Focus engrais organiques
            if culture != "Non spécifié":
                npk_data = await calculate_npk_requirements(self.llm_service, culture, area, stage)
                if "besoins_npk_kg_ha" in npk_data:
                    organic_recs = await get_organic_fertilizers(self.llm_service, npk_data["besoins_npk_kg_ha"], region_name)
                    tool_results = f"**Engrais organiques pour {culture}:**\n{json.dumps(organic_recs, indent=2, ensure_ascii=False)}"
            else:
                # Recette compost générique
                compost = await calculate_compost_recipe(self.llm_service, 2.0)
                tool_results = f"**Recette compost:**\n{json.dumps(compost, indent=2, ensure_ascii=False)}"
        
        elif intent == "DEFICIENCY":
            # Diagnostic carence
            diagnosis = await diagnose_nutrient_deficiency(self.llm_service, symptoms, culture)
            tool_results = f"**Diagnostic carence:**\n{json.dumps(diagnosis, indent=2, ensure_ascii=False)}"
        
        elif intent == "SCHEDULE":
            # Calendrier application
            if culture != "Non spécifié":
                npk_data = await calculate_npk_requirements(self.llm_service, culture, area, stage)
                if "besoins_totaux_kg" in npk_data:
                    schedule = await get_application_schedule(self.llm_service, culture, npk_data["besoins_totaux_kg"])
                    tool_results = f"**Calendrier application {culture}:**\n{json.dumps(schedule, indent=2, ensure_ascii=False)}"
            else:
                tool_results = "Culture non spécifiée. Précisez pour calendrier personnalisé."
        
        elif intent == "SOIL":
            # Amendements sol
            soil_type = context.get('soil_type', 'ferralitique')  # Type sol par défaut Cameroun
            soil_advice = await get_soil_amendment_advice(self.llm_service, soil_type, culture)
            tool_results = f"**Amendements sol {soil_type}:**\n{json.dumps(soil_advice, indent=2, ensure_ascii=False)}"
        
        else:  # GENERAL
            # Combinaison selon contexte
            if culture != "Non spécifié":
                npk_data = await calculate_npk_requirements(self.llm_service, culture, area, stage)
                tool_results = f"**Infos générales {culture}:**\n{json.dumps(npk_data, indent=2, ensure_ascii=False)}"
            else:
                compost = await calculate_compost_recipe(self.llm_service, 1.0)
                tool_results = f"**Conseils fertilisation:**\n{json.dumps(compost, indent=2, ensure_ascii=False)}"
        
        # 5. Construction prompt final
        system_prompt = get_system_prompt()
        
        full_prompt = f"""{system_prompt}

DONNÉES OUTILS:
{tool_results}

QUESTION: {query}
RÉGION: {region_name}

Réponds de manière CONCISE (Max 200 mots) avec CHIFFRES PRÉCIS. Format avec icônes et structure claire."""

        response = await self.llm_service.generate_response(full_prompt)
        
        # 6. Post-processing pour concision
        word_count = len(response.split())
        if word_count > 250:
            condense_prompt = f"""Condense à MAXIMUM 200 mots en gardant TOUS les chiffres et dosages:

{response}

Format: Bullets, données chiffrées essentielles uniquement."""
            response = await self.llm_service.generate_response(condense_prompt)
        
        return response
