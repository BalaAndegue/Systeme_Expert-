from flask import Blueprint, request, jsonify
from app.core.orchestrator import AgentOrchestrator
from app.agents.weather import WeatherAgent
from app.agents.crop import CropAgent
from app.agents.health import HealthAgent
from app.agents.economic import EconomicAgent
import asyncio

api_bp = Blueprint('api', __name__)

# Initialisation unique des agents et de l'orchestrateur
agents = [
    WeatherAgent(),
    CropAgent(),
    HealthAgent(),
    EconomicAgent()
]
orchestrator = AgentOrchestrator(agents)

@api_bp.route('/query', methods=['POST'])
async def handle_query():
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
        return jsonify({"error": str(e)}), 500

@api_bp.route('/agents', methods=['GET'])
def list_agents():
    return jsonify([
        {"name": a.name, "description": a.description} 
        for a in agents
    ])
