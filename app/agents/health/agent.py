from app.agents.base_agent import BaseAgent
from typing import Dict, Any
import json
from .prompt import get_system_prompt, get_intent_prompt, get_extraction_prompt, return_instructions_health
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
        
        # 2. Détection de l'intention
        intent_prompt = get_intent_prompt(query)
        intent = await self.llm_service.generate_response(intent_prompt)
        intent = intent.strip().upper()
        
        # Nettoyage de l'intention
        valid_intents = ["DIAGNOSIS", "PEST_ID", "TREATMENT", "PREVENTION", "GENERAL"]
        found_intent = "GENERAL"
        for valid in valid_intents:
            if valid in intent:
                found_intent = valid
                break
        intent = found_intent
        
        print(f"DEBUG: Intent detected by HealthAgent: {intent}")

        # 3. Extraction des entités (culture, symptômes/problème)
        extract_prompt = get_extraction_prompt(query)
        extraction_json = await self.llm_service.generate_response(extract_prompt)
        
        # Tentative de parsing JSON
        try:
            # Nettoyage basique pour json (au cas où le LLM mettrait des backticks)
            cleaned_json = extraction_json.replace("```json", "").replace("```", "").strip()
            entities = json.loads(cleaned_json)
        except Exception as e:
            print(f"Warning: Failed to parse extraction JSON: {e}")
            entities = {"culture": "Non spécifié", "symptômes": "Non spécifié"}
            
        culture = entities.get("culture", "Non spécifié")
        symptomes = entities.get("symptômes", "Non spécifié")
        
        # 4. Dispatching vers les outils
        if intent == "DIAGNOSIS":
            result = await diagnose_plant_disease(self.llm_service, culture, symptomes, region_name)
            return f"Diagnostic pour {culture} ({region_name}) :\n\n{result.get('diagnosis')}"
            
        elif intent == "PEST_ID":
            # Si l'utilisateur décrit un insecte, 'symptomes' contiendra la description
            result = await get_pest_identification(self.llm_service, symptomes, culture)
            return f"Identification du ravageur sur {culture} :\n\n{result.get('identification')}"
            
        elif intent == "TREATMENT":
            # Si l'utilisateur demande un traitement, 'symptomes' peut contenir le nom de la maladie
            result = await get_treatment_recommendations(self.llm_service, symptomes, culture)
            return f"Recommandations de traitement contre {symptomes} sur {culture} :\n\n{result.get('recommendations')}"
            
        elif intent == "PREVENTION":
            result = await get_prevention_strategies(self.llm_service, culture, symptomes)
            return f"Stratégies de prévention ({symptomes}) pour {culture} :\n\n{result.get('strategies')}"
            
        else: # GENERAL
            # Utilisation du prompt système complet défini par l'utilisateur
            system_prompt = get_system_prompt()
            # On ajoute le contexte spécifique à la requête
            full_context_prompt = f"{system_prompt}\n\nContexte actuel: Région={region_name}, Culture={culture}"
            return await self.llm_service.generate_response(query, full_context_prompt)
