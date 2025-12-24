from app.agents.base_agent import BaseAgent
from typing import Dict, Any
from .prompt import get_system_prompt, get_intent_prompt
from .tools import (
    analyze_soil_requirements,
    recommend_fertilizers,
    optimize_irrigation,
    assess_land_suitability,
    calculate_nutrient_needs,
    suggest_soil_amendments
)

class ResourcesAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ResourcesAgent",
            description="Spécialiste en gestion des sols, de l'eau et des ressources agricoles. Optimise la fertilité et l'irrigation pour une agriculture durable."
        )

    async def process(self, query: str, context: Dict[str, Any]) -> str:
        # 1. Détection de l'intention
        intent_prompt = get_intent_prompt(query)
        intent = await self.llm_service.generate_response(intent_prompt)
        intent = intent.strip().upper()
        
        print(f"DEBUG: Intent detected by ResourcesAgent: {intent}")

        # 2. Dispatching
        if "SOIL_ANALYSIS" in intent:
            return await analyze_soil_requirements(self.llm_service, query)
        elif "FERTILIZER" in intent:
            return await recommend_fertilizers(self.llm_service, query)
        elif "IRRIGATION" in intent:
            return await optimize_irrigation(self.llm_service, query)
        elif "SUITABILITY" in intent:
            return await assess_land_suitability(self.llm_service, query)
        elif "NUTRIENTS" in intent:
            return await calculate_nutrient_needs(self.llm_service, query)
        elif "AMENDMENTS" in intent:
            return await suggest_soil_amendments(self.llm_service, query)
        else:
            # Fallback général avec le prompt système riche
            system_prompt = get_system_prompt()
            return await self.llm_service.generate_response(query, system_prompt)
