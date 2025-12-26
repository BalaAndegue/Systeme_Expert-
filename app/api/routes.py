from flask import Blueprint, request, jsonify
import traceback
from app.core.orchestrator import AgentOrchestrator
from app.agents.weather import WeatherAgent
from app.agents.crop import CropAgent
from app.agents.health import HealthAgent
from app.agents.economic import EconomicAgent
from app.agents.resources import ResourcesAgent
import asyncio

api_bp = Blueprint('api', __name__)

# Initialisation unique des agents et de l'orchestrateur
agents = [
    WeatherAgent(),
    CropAgent(),
    HealthAgent(),
    EconomicAgent(),
    ResourcesAgent()
]
orchestrator = AgentOrchestrator(agents)

@api_bp.route('/query', methods=['POST'])
async def handle_query():
    """
    Traite une requête utilisateur via les agents spécialisés.
    ---
    tags:
      - Agriculture Agents
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - query
          properties:
            query:
              type: string
              description: La question de l'utilisateur.
              example: "Quand planter le maïs dans le Centre ?"
            region:
              type: string
              description: "La région concernée (ex: Centre, Nord)."
              default: Centre
    responses:
      200:
        description: Réponse du système multi-agents
        schema:
          type: object
          properties:
            query:
              type: string
            region:
              type: string
            final_response:
              type: string
              description: La réponse synthétisée.
            orchestration:
              type: object
              description: Détails de l'orchestration (agents consultés).
      400:
        description: Paramètre manquant
      500:
        description: Erreur interne
    """

    data = request.get_json()
    user_query = data.get('query')
    region = data.get('region', 'Centre')
    
    if not user_query:
        return jsonify({"error": "Query parameter is required"}), 400

    # Mise à jour du contexte
    orchestrator.update_context('region', region)

    try:
        # 1. Routing et réponses individuelles
        agent_responses = await orchestrator.handle_query(user_query)
        
        # 2. Synthèse
        final_response = await orchestrator.synthesize_response(user_query, agent_responses)
        
        return jsonify({
            "query": user_query,
            "region": region,
            "orchestration": {
                "selected_agents": list(agent_responses.keys()),
                "individual_responses": agent_responses
            },
            "final_response": final_response
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@api_bp.route('/agents', methods=['GET'])
def list_agents():
    """
    Liste les agents disponibles dans le système.
    ---
    tags:
      - System
    responses:
      200:
        description: Liste des agents et leurs descriptions
        schema:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
              description:
                type: string
    """

    return jsonify([
        {"name": a.name, "description": a.description} 
        for a in agents
    ])
