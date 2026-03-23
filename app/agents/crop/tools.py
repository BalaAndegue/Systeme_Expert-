"""Outils pour l'agent de gestion des cultures."""

from typing import Dict, List, Any, Optional
from app.services.llm_service import LLMService

async def get_planting_calendar(
    llm_service: LLMService,
    crop: str,
    region: str,
) -> Dict[str, Any]:
    """Génère un calendrier de plantation."""
    prompt = f"""Calendrier plantation {crop} ({region}), Cameroun.
Fournis: Période semis, préparation sol, étapes croissance, récolte.
MAX 150 mots. Bullets concis, dates précises selon saison pluies locale."""
    
    response = await llm_service.generate_response(prompt)
    return {"crop": crop, "region": region, "calendar": response}


async def get_crop_rotation_advice(
    llm_service: LLMService,
    current_crop: str,
    soil_type: str,
    field_history: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Recommande un plan de rotation des cultures."""
    history_str = ", ".join(field_history) if field_history else "Non spécifié"
    
    prompt = f"""Rotation cultures Cameroun. Actuel: {current_crop}, Sol: {soil_type}, Historique: {history_str}.
Fournis: Prochaine culture, plan 3 ans, associations bénéfiques.
MAX 150 mots. Bullets, justifications courtes."""
    
    response = await llm_service.generate_response(prompt)
    return {"current_crop": current_crop, "soil_type": soil_type, "rotation_plan": response}


async def get_variety_recommendations(
    llm_service: LLMService,
    crop: str,
    region: str,
    priorities: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Recommande les meilleures variétés pour une culture."""
    priorities_str = ", ".join(priorities) if priorities else "Rendement et adaptation locale"
    
    prompt = f"""Variétés {crop} pour {region} (Cameroun). Priorités: {priorities_str}.
Par variété: nom, rendement, cycle, résistance.
MAX 150 mots. Inclure variétés locales et améliorées."""
    
    response = await llm_service.generate_response(prompt)
    return {"crop": crop, "region": region, "recommendations": response}


async def get_cultivation_techniques(
    llm_service: LLMService,
    crop: str,
    farming_system: str = "Traditionnel",
    constraints: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Fournit des techniques de culture adaptées."""
    constraints_str = ", ".join(constraints) if constraints else "Budget limité"
    
    prompt = f"""Techniques culture {crop} au Cameroun. Système: {farming_system}. Contraintes: {constraints_str}.
Fournis: Préparation sol, semis, espacement, fertilisation, récolte.
MAX 150 mots. Solutions économiques et durables."""
    
    response = await llm_service.generate_response(prompt)
    return {"crop": crop, "system": farming_system, "techniques": response}
