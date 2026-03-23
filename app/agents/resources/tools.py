from typing import Dict, Any
from app.services.llm_service import LLMService

async def analyze_soil_requirements(llm_service: LLMService, query: str) -> str:
    prompt = f"""Expert pédologue Cameroun. {query}
Analyse besoins sol. MAX 150 mots. Bullets, chiffres FCFA, doses kg/ha."""
    return await llm_service.generate_response(prompt)

async def optimize_irrigation(llm_service: LLMService, query: str) -> str:
    prompt = f"""Expert gestion eau agricole Cameroun. {query}
Plan irrigation. MAX 150 mots. Litres/plant, fréquence, méthode."""
    return await llm_service.generate_response(prompt)

async def assess_land_suitability(llm_service: LLMService, query: str) -> str:
    prompt = f"""Expert aptitude sols Cameroun. {query}
Évalue aptitude terrain. MAX 150 mots. Score aptitude, cultures recommandées."""
    return await llm_service.generate_response(prompt)

async def suggest_soil_amendments(llm_service: LLMService, query: str) -> str:
    prompt = f"""Expert amendements sols Cameroun. {query}
Amendements recommandés. MAX 150 mots. Doses kg/ha, coûts FCFA, timing."""
    return await llm_service.generate_response(prompt)
