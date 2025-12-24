from app.agents.base_agent import BaseAgent
from typing import Dict, Any
import json
from .prompt import get_system_prompt, get_intent_prompt, get_extraction_prompt, return_instructions_economic
from .tools import (
    get_market_prices,
    analyze_profitability,
    get_market_trends,
    recommend_sales_strategy,
    calculate_production_costs,
    analyze_market_opportunities
)

class EconomicAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="EconomicAgent",
            description="Économiste agricole. Analyse la rentabilité, les prix, les tendances du marché et conseille sur les stratégies commerciales."
        )

    async def process(self, query: str, context: Dict[str, Any]) -> str:
        # 1. Récupération du contexte
        region_name = context.get('region', 'Cameroun')
        
        # 2. Détection de l'intention
        intent_prompt = get_intent_prompt(query)
        intent = await self.llm_service.generate_response(intent_prompt)
        intent = intent.strip().upper()
        
        # Nettoyage de l'intention
        valid_intents = ["PRICES", "PROFITABILITY", "TRENDS", "STRATEGY", "OPPORTUNITIES", "COST_CALCULATION", "GENERAL"]
        found_intent = "GENERAL"
        for valid in valid_intents:
            if valid in intent:
                found_intent = valid
                break
        intent = found_intent
        
        print(f"DEBUG: Intent detected by EconomicAgent: {intent}")

        # 3. Extraction des entités (culture, région)
        extract_prompt = get_extraction_prompt(query)
        extraction_json = await self.llm_service.generate_response(extract_prompt)
        
        try:
            cleaned_json = extraction_json.replace("```json", "").replace("```", "").strip()
            entities = json.loads(cleaned_json)
        except Exception as e:
            print(f"Warning: Failed to parse extraction JSON: {e}")
            entities = {"culture": "Non spécifié", "region": "Non spécifié"}
            
        culture = entities.get("culture", "Non spécifié")
        region_entity = entities.get("region", region_name)
        if region_entity == "Non spécifié":
            region_entity = region_name
        
        # 4. Dispatching vers les outils
        if intent == "PRICES":
            result = await get_market_prices(self.llm_service, culture, region_entity)
            return f"Analyse des prix pour {culture} ({region_entity}) :\n\n{result.get('prices_analysis')}"
            
        elif intent == "PROFITABILITY":
            result = await analyze_profitability(self.llm_service, culture)
            return f"Étude de rentabilité pour {culture} :\n\n{result.get('profitability')}"
            
        elif intent == "TRENDS":
            result = await get_market_trends(self.llm_service, culture)
            return f"Tendances du marché pour {culture} :\n\n{result.get('trends')}"
            
        elif intent == "STRATEGY":
            result = await recommend_sales_strategy(self.llm_service, culture)
            return f"Stratégie de vente recommandée pour {culture} :\n\n{result.get('strategy')}"
            
        elif intent == "COST_CALCULATION":
            result = await calculate_production_costs(self.llm_service, culture)
            return f"Coûts de production estimés pour {culture} :\n\n{result.get('costs')}"

        elif intent == "OPPORTUNITIES":
            result = await analyze_market_opportunities(self.llm_service, region_entity)
            return f"Opportunités de marché à {region_entity} :\n\n{result.get('opportunities')}"
            
        else: # GENERAL
            system_prompt = get_system_prompt()
            full_context_prompt = f"{system_prompt}\n\nContexte actuel: Région={region_entity}, Culture={culture}"
            return await self.llm_service.generate_response(query, full_context_prompt)
