from app.agents.base_agent import BaseAgent
from typing import Dict, Any
import json
from .prompt import get_system_prompt, get_combined_prompt, get_intent_prompt, get_extraction_prompt, return_instructions_health
from .tools import (
    diagnose_plant_disease,
    get_treatment_recommendations,
    get_pest_identification,
    get_prevention_strategies
)

class HealthAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="HealthAgent",
            description="Phytopathologiste expert. Diagnostique les maladies, identifie les parasites et recommande des traitements adaptés au contexte camerounais."
        )

    async def process(self, query: str, context: Dict[str, Any]) -> str:
        # 1. Récupération du contexte
        region_name = context.get('region', 'Cameroun')
        
        # 2. Intent + Extraction en UN SEUL appel LLM (optimisation latence)
        combined_prompt = get_combined_prompt(query)
        combined_json = await self.llm_service.generate_response(combined_prompt)
        
        try:
            cleaned = combined_json.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(cleaned)
            intent = parsed.get("intent", "GENERAL").strip().upper()
            culture = parsed.get("culture", "Non spécifié").strip()
            symptomes = parsed.get("symptomes", "Non spécifié").strip()
        except Exception as e:
            print(f"Warning: Failed to parse combined JSON for HealthAgent: {e}")
            intent = "GENERAL"
            culture = "Non spécifié"
            symptomes = "Non spécifié"
        
        # Validation de l'intent
        valid_intents = ["DIAGNOSIS", "PEST_ID", "TREATMENT", "PREVENTION", "GENERAL"]
        if intent not in valid_intents:
            intent = "GENERAL"
        
        print(f"DEBUG: Intent detected by HealthAgent: {intent}")

        # 3. Dispatching vers les outils
        if intent == "DIAGNOSIS":
            result = await diagnose_plant_disease(self.llm_service, culture, symptomes, region_name)
            return f"Diagnostic pour {culture} ({region_name}) :\n\n{result.get('diagnosis')}"
            
        elif intent == "PEST_ID":
            result = await get_pest_identification(self.llm_service, symptomes, culture)
            return f"Identification du ravageur sur {culture} :\n\n{result.get('identification')}"
            
        elif intent == "TREATMENT":
            result = await get_treatment_recommendations(self.llm_service, symptomes, culture)
            return f"Recommandations de traitement contre {symptomes} sur {culture} :\n\n{result.get('recommendations')}"
            
        elif intent == "PREVENTION":
            result = await get_prevention_strategies(self.llm_service, culture, symptomes)
            return f"Stratégies de prévention ({symptomes}) pour {culture} :\n\n{result.get('strategies')}"
            
        else:  # GENERAL
            from .prompt import get_system_prompt
            system_prompt = get_system_prompt()
            full_context_prompt = f"{system_prompt}\n\nContexte actuel: Région={region_name}, Culture={culture}"
            return await self.llm_service.generate_response(query, full_context_prompt)
