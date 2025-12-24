"""Outils pour l'agent économique."""

from typing import Dict, Any, List
from app.services.llm_service import LLMService

# Importation des données locales si disponibles pour enrichir le contexte
from app.data.market_prices import get_current_prices

async def get_market_prices(
    llm_service: LLMService,
    crop: str,
    region: str = "Cameroun"
) -> Dict[str, Any]:
    """Obtient les prix actuels du marché.
    
    Args:
        llm_service: Service LLM.
        crop: La culture concernée.
        region: Région ou marché spécifique.
        
    Returns:
        Prix et analyses.
    """
    # Récupérer des vraies données si disponibles
    real_prices = get_current_prices()
    relevant_prices = [p for p in real_prices if crop.lower() in p.crop_name.lower()]
    prices_context = "\n".join([f"- {p.crop_name}: {p.price_avg_fcfa} FCFA/{p.unit} ({p.trend})" for p in relevant_prices])
    
    if not prices_context:
        prices_context = "Pas de données en temps réel disponibles pour cette culture spécifique."

    prompt = f"""
    En tant qu'économiste agricole au Cameroun, fournis une analyse des prix pour :
    - Culture: {crop}
    - Région: {region}
    
    Données temps réel disponibles :
    {prices_context}
    
    Complète ces données avec tes connaissances pour fournir :
    1. Fourchette de prix actuelle (Bord champ vs Marché urbain).
    2. Variations récentes (Hausse/Baisse).
    3. Comparaison avec la moyenne saisonnière.
    """
    
    response = await llm_service.generate_response(prompt)
    
    return {
        "tool": "get_market_prices",
        "crop": crop,
        "prices_analysis": response
    }

async def analyze_profitability(
    llm_service: LLMService,
    crop: str,
    area_size: str = "1 hectare"
) -> Dict[str, Any]:
    """Analyse la rentabilité d'une culture.
    
    Args:
        llm_service: Service LLM.
        crop: La culture.
        area_size: Surface cultivée.
        
    Returns:
        Analyse de rentabilité.
    """
    prompt = f"""
    Effectue une étude de rentabilité simplifiée pour :
    - Culture: {crop}
    - Surface: {area_size}
    - Contexte: Cameroun
    
    Fournis :
    1. Coûts opérationnels estimés (Intrants, Main d'œuvre, Transport).
    2. Rendement attendu (moyen).
    3. Revenu brut potentiel (selon prix moyens).
    4. Marge nette estimée.
    5. Retour sur investissement (ROI).
    
    Sois réaliste et prudent dans les estimations.
    """
    
    response = await llm_service.generate_response(prompt)
    
    return {
        "tool": "analyze_profitability",
        "crop": crop,
        "profitability": response
    }

async def get_market_trends(
    llm_service: LLMService,
    crop: str
) -> Dict[str, Any]:
    """Identifie les tendances du marché.
    
    Args:
        llm_service: Service LLM.
        crop: La culture.
        
    Returns:
        Analyse des tendances.
    """
    prompt = f"""
    Quelles sont les grandes tendances du marché pour le {crop} au Cameroun ?
    
    Analyse :
    1. Demande locale vs Exportation.
    2. Évolution de la consommation.
    3. Impact des saisons.
    4. Prévisions pour les prochains mois.
    """
    
    response = await llm_service.generate_response(prompt)
    
    return {
        "tool": "get_market_trends",
        "crop": crop,
        "trends": response
    }

async def recommend_sales_strategy(
    llm_service: LLMService,
    crop: str
) -> Dict[str, Any]:
    """Conseille sur les stratégies de vente.
    
    Args:
        llm_service: Service LLM.
        crop: La culture.
        
    Returns:
        Recommandations stratégiques.
    """
    prompt = f"""
    Propose une stratégie de vente optimale pour un producteur de {crop} au Cameroun.
    
    Aborde :
    1. Moment idéal pour vendre (stockage vs vente immédiate).
    2. Canal de vente recommandé (Bord champ, Grossiste, Marché, Coopérative).
    3. Conditionnement et présentation pour une meilleure valeur ajoutée.
    4. Négociation des prix.
    """
    
    response = await llm_service.generate_response(prompt)
    
    return {
        "tool": "recommend_sales_strategy",
        "crop": crop,
        "strategy": response
    }

async def calculate_production_costs(
    llm_service: LLMService,
    crop: str
) -> Dict[str, Any]:
    """Calcule les coûts de production.
    
    Args:
        llm_service: Service LLM.
        crop: La culture.
        
    Returns:
        Détail des coûts.
    """
    prompt = f"""
    Détaille la structure des coûts de production pour 1 hectare de {crop} au Cameroun.
    
    Inclus les postes :
    1. Préparation du terrain.
    2. Semences/Plants.
    3. Fertilisants et produits phytosanitaires.
    4. Main d'œuvre (semis, entretien, récolte).
    5. Transport et logistique.
    
    Donne des estimations en FCFA.
    """
    
    response = await llm_service.generate_response(prompt)
    
    return {
        "tool": "calculate_production_costs",
        "crop": crop,
        "costs": response
    }

async def analyze_market_opportunities(
    llm_service: LLMService,
    region: str
) -> Dict[str, Any]:
    """Identifie les opportunités de marché.
    
    Args:
        llm_service: Service LLM.
        region: La région.
        
    Returns:
        Opportunités.
    """
    prompt = f"""
    Quelles sont les opportunités agricoles les plus porteuses actuellement dans la région {region} (ou au Cameroun en général) ?
    
    Identifie :
    1. Cultures à haute valeur ajoutée.
    2. Créneaux insatisfaits (demande > offre).
    3. Opportunités de transformation locale.
    """
    
    response = await llm_service.generate_response(prompt)
    
    return {
        "tool": "analyze_market_opportunities",
        "region": region,
        "opportunities": response
    }
