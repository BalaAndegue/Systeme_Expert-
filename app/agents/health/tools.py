"""Outils pour l'agent de santé des plantes."""

from typing import Dict, Any
from app.services.llm_service import LLMService

async def diagnose_plant_disease(
    llm_service: LLMService,
    crop: str,
    symptoms: str,
    region: str = "Cameroun"
) -> Dict[str, Any]:
    """Diagnostique une maladie basée sur les symptômes.
    
    Args:
        llm_service: Service LLM.
        crop: La culture concernée.
        symptoms: Description des symptômes.
        region: Région (contexte géographique).
        
    Returns:
        Résultat du diagnostic structuré.
    """
    prompt = f"""
    En tant que phytopathologiste expert au Cameroun, diagnostique le problème suivant :
    - Culture: {crop}
    - Symptômes observés: {symptoms}
    - Région: {region}
    
    Ton analyse doit inclure :
    1. Identification de la maladie ou du problème probable.
    2. Cause (pathogène, insecte, carence, etc.).
    3. Facteurs favorisants (climat, pratiques).
    4. Niveau de confiance du diagnostic.
    5. Gravité estimée.

    Si les symptômes sont trop vagues, demande des précisions.
    """
    
    response = await llm_service.generate_response(prompt)
    
    return {
        "tool": "diagnose_plant_disease",
        "crop": crop,
        "diagnosis": response
    }

async def get_treatment_recommendations(
    llm_service: LLMService,
    diagnosis: str,
    crop: str,
) -> Dict[str, Any]:
    """Fournit des recommandations de traitement.
    
    Args:
        llm_service: Service LLM.
        diagnosis: Le nom de la maladie ou du problème identifié.
        crop: La culture concernée.
        
    Returns:
        Plan de traitement détaillé.
    """
    prompt = f"""
    En tant qu'expert santé des plantes, recommande un traitement pour :
    - Problème/Maladie: {diagnosis}
    - Culture: {crop}
    
    Fournis des solutions adaptées au contexte camerounais :
    1. Traitements biologiques et naturels (priorité).
    2. Traitements chimiques (si nécessaire, avec précautions).
    3. Pratiques culturales curatives.
    4. Dosage et fréquence d'application.
    5. Mesures de sécurité.
    """
    
    response = await llm_service.generate_response(prompt)
    
    return {
        "tool": "get_treatment_recommendations",
        "problem": diagnosis,
        "recommendations": response
    }

async def get_pest_identification(
    llm_service: LLMService,
    description: str,
    crop: str,
) -> Dict[str, Any]:
    """Identifie un parasite ou ravageur.
    
    Args:
        llm_service: Service LLM.
        description: Description de l'insecte ou du ravageur.
        crop: La culture concernée.
        
    Returns:
        Identification et conseils immédiats.
    """
    prompt = f"""
    Identifie ce ravageur potentiel au Cameroun :
    - Description: {description}
    - Culture attaquée: {crop}
    
    Rends :
    1. Nom probable (commun et scientifique).
    2. Cycle de vie bref.
    3. Dégâts typiques.
    4. Méthodes de lutte immédiate (piégeage, produits naturels, etc.).
    """
    
    response = await llm_service.generate_response(prompt)
    
    return {
        "tool": "get_pest_identification",
        "description": description,
        "identification": response
    }

async def get_prevention_strategies(
    llm_service: LLMService,
    crop: str,
    disease_or_pest: str = "Général"
) -> Dict[str, Any]:
    """Fournit des stratégies de prévention.
    
    Args:
        llm_service: Service LLM.
        crop: La culture concernée.
        disease_or_pest: Maladie ou peste spécifique à prévenir (optionnel).
        
    Returns:
        Stratégies préventives.
    """
    prompt = f"""
    Établis une stratégie de prévention pour :
    - Culture: {crop}
    - Cible: {disease_or_pest} (si 'Général', couvre les problèmes majeurs au Cameroun pour cette culture).
    
    Détaille :
    1. Choix variétal.
    2. Pratiques culturales (rotation, densité, etc.).
    3. Surveillance sanitaire.
    4. Utilisation d'auxiliaires ou de produits préventifs.
    """
    
    response = await llm_service.generate_response(prompt)
    
    return {
        "tool": "get_prevention_strategies",
        "target": disease_or_pest,
        "strategies": response
    }
