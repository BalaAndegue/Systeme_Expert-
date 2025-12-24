from typing import Dict, Any
from app.services.llm_service import LLMService

async def analyze_soil_requirements(llm_service: LLMService, query: str) -> str:
    prompt = f"Agis comme un expert pédologue. {query}. Fais une analyse détaillée des besoins du sol en te basant sur le contexte camerounais."
    return await llm_service.generate_response(prompt)

async def recommend_fertilizers(llm_service: LLMService, query: str) -> str:
    prompt = f"Recommande des engrais (organiques et chimiques) adaptés pour cette demande : {query}. Privilégie les ressources locales du Cameroun."
    return await llm_service.generate_response(prompt)

async def optimize_irrigation(llm_service: LLMService, query: str) -> str:
    prompt = f"Propose un plan d'optimisation de l'irrigation et de gestion de l'eau pour : {query}."
    return await llm_service.generate_response(prompt)

async def assess_land_suitability(llm_service: LLMService, query: str) -> str:
    prompt = f"Évalue l'aptitude du terrain pour l'agriculture : {query}."
    return await llm_service.generate_response(prompt)

async def calculate_nutrient_needs(llm_service: LLMService, query: str) -> str:
    prompt = f"Calcule les besoins nutritifs spécifiques (NPK + micro-nutriments) pour : {query}."
    return await llm_service.generate_response(prompt)

async def suggest_soil_amendments(llm_service: LLMService, query: str) -> str:
    prompt = f"Suggère des amendements pour améliorer la structure et la fertilité du sol : {query}."
    return await llm_service.generate_response(prompt)
