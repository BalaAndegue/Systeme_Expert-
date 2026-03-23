"""Outils pour l'agent de santé des plantes."""

from typing import Dict, Any
from app.services.llm_service import LLMService

async def diagnose_plant_disease(
    llm_service: LLMService,
    crop: str,
    symptoms: str,
    region: str = "Cameroun"
) -> Dict[str, Any]:
    """Diagnostique une maladie basée sur les symptômes."""
    prompt = f"""Diagnostic phytosanitaire Cameroun.
Culture: {crop} | Symptômes: {symptoms} | Région: {region}
Fournis: Maladie probable, cause, gravité, traitement immédiat.
MAX 150 mots. Noms scientifiques, doses exactes produits."""
    
    response = await llm_service.generate_response(prompt)
    return {"tool": "diagnose_plant_disease", "crop": crop, "diagnosis": response}

async def get_treatment_recommendations(
    llm_service: LLMService,
    diagnosis: str,
    crop: str,
) -> Dict[str, Any]:
    """Fournit des recommandations de traitement."""
    prompt = f"""Traitement {diagnosis} sur {crop} au Cameroun.
Priorité: bio (neem, cendre, savon noir) puis chimique si nécessaire.
Fournis: produit, dose, fréquence, précautions.
MAX 150 mots."""
    
    response = await llm_service.generate_response(prompt)
    return {"tool": "get_treatment_recommendations", "problem": diagnosis, "recommendations": response}

async def get_pest_identification(
    llm_service: LLMService,
    description: str,
    crop: str,
) -> Dict[str, Any]:
    """Identifie un parasite ou ravageur."""
    prompt = f"""Identification ravageur Cameroun.
Description: {description} | Culture: {crop}
Fournis: Nom (commun + scientifique), dégâts, lutte immédiate.
MAX 150 mots."""
    
    response = await llm_service.generate_response(prompt)
    return {"tool": "get_pest_identification", "description": description, "identification": response}

async def get_prevention_strategies(
    llm_service: LLMService,
    crop: str,
    disease_or_pest: str = "Général"
) -> Dict[str, Any]:
    """Fournit des stratégies de prévention."""
    prompt = f"""Prévention {disease_or_pest} sur {crop} au Cameroun.
Fournis: choix variétal, pratiques culturales, surveillance, produits préventifs.
MAX 150 mots. Prioriser méthodes locales et économiques."""
    
    response = await llm_service.generate_response(prompt)
    return {"tool": "get_prevention_strategies", "target": disease_or_pest, "strategies": response}
