"""Outils pour l'agent économique."""

from typing import Dict, Any
from app.services.llm_service import LLMService
from app.data.market_prices import get_current_prices

async def get_market_prices(
    llm_service: LLMService,
    crop: str,
    region: str = "Cameroun"
) -> Dict[str, Any]:
    """Obtient les prix actuels du marché."""
    real_prices = get_current_prices()
    relevant_prices = [p for p in real_prices if crop.lower() in p.crop_name.lower()]
    prices_context = "\n".join([f"- {p.crop_name}: {p.price_avg_fcfa} FCFA/{p.unit} ({p.trend})" for p in relevant_prices])
    
    if not prices_context:
        prices_context = "Pas de données temps réel pour cette culture."

    prompt = f"""Prix marché {crop} ({region}), Cameroun.
Données disponibles: {prices_context}
Fournis: prix bord champ vs marché urbain, variations récentes.
MAX 150 mots. Chiffres FCFA uniquement."""
    
    response = await llm_service.generate_response(prompt)
    return {"tool": "get_market_prices", "crop": crop, "prices_analysis": response}

async def analyze_profitability(
    llm_service: LLMService,
    crop: str,
    area_size: str = "1 hectare"
) -> Dict[str, Any]:
    """Analyse la rentabilité d'une culture."""
    prompt = f"""Rentabilité {crop} sur {area_size} au Cameroun.
Fournis: coûts (intrants, MO, transport), rendement, revenu brut, marge nette, ROI%.
MAX 150 mots. Tous montants en FCFA."""
    
    response = await llm_service.generate_response(prompt)
    return {"tool": "analyze_profitability", "crop": crop, "profitability": response}

async def get_market_trends(
    llm_service: LLMService,
    crop: str
) -> Dict[str, Any]:
    """Identifie les tendances du marché."""
    prompt = f"""Tendances marché {crop} au Cameroun.
Fournis: demande locale vs export, évolution consommation, impact saisons, prévisions.
MAX 150 mots."""
    
    response = await llm_service.generate_response(prompt)
    return {"tool": "get_market_trends", "crop": crop, "trends": response}

async def recommend_sales_strategy(
    llm_service: LLMService,
    crop: str
) -> Dict[str, Any]:
    """Conseille sur les stratégies de vente."""
    prompt = f"""Stratégie vente {crop} au Cameroun.
Fournis: moment vente, canal recommandé, conditionnement, négociation prix.
MAX 150 mots. Conseils pratiques pour petit producteur."""
    
    response = await llm_service.generate_response(prompt)
    return {"tool": "recommend_sales_strategy", "crop": crop, "strategy": response}

async def calculate_production_costs(
    llm_service: LLMService,
    crop: str
) -> Dict[str, Any]:
    """Calcule les coûts de production."""
    prompt = f"""Coûts production 1ha {crop} au Cameroun.
Détaille: terrain, semences, fertilisants, phyto, MO, transport.
MAX 150 mots. Estimations FCFA."""
    
    response = await llm_service.generate_response(prompt)
    return {"tool": "calculate_production_costs", "crop": crop, "costs": response}

async def analyze_market_opportunities(
    llm_service: LLMService,
    region: str
) -> Dict[str, Any]:
    """Identifie les opportunités de marché."""
    prompt = f"""Opportunités agricoles à {region} (Cameroun).
Fournis: cultures haute valeur, créneaux insatisfaits, transformation locale.
MAX 150 mots."""
    
    response = await llm_service.generate_response(prompt)
    return {"tool": "analyze_market_opportunities", "region": region, "opportunities": response}
