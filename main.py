import argparse
import asyncio
import os
from app import create_app
from app.agents.weather import WeatherAgent
from app.agents.crop import CropAgent
from app.agents.health import HealthAgent
from app.agents.economic import EconomicAgent
from app.agents.resources import ResourcesAgent
from app.core.orchestrator import AgentOrchestrator

def run_cli(query, region):
    print(f"--- Mode CLI - Agriculture Cameroun ---")
    print(f"Région: {region}")
    print(f"Question: {query}")
    print("Traitement en cours...\n")

    agents = [
        WeatherAgent(),
        CropAgent(),
        HealthAgent(),
        EconomicAgent(),
        ResourcesAgent()
    ]
    orchestrator = AgentOrchestrator(agents)
    orchestrator.update_context('region', region)

    async def _process():
        agent_responses = await orchestrator.handle_query(query)
        print(f"Agents consultés: {', '.join(agent_responses.keys())}\n")
        
        for name, resp in agent_responses.items():
            print(f"--- {name} ---")
            print(resp)
            print()
            
        print("--- Synthèse Finale ---")
        final = await orchestrator.synthesize_response(query, agent_responses)
        print(final)

    asyncio.run(_process())

def run_web(port):
    app = create_app()
    print(f"Démarrage du serveur Web sur le port {port}...")
    app.run(debug=True, port=port, use_reloader=False) # use_reloader=False pour éviter les pbs avec asyncio parfois

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Système Multi-Agents Agriculture Cameroun")
    parser.add_argument('mode', choices=['cli', 'web'], help="Mode de lancement (cli ou web)")
    parser.add_argument('--query', '-q', help="Question pour le mode CLI")
    parser.add_argument('--region', '-r', default='Centre', help="Région concernée (CLI)")
    parser.add_argument('--port', '-p', type=int, default=5000, help="Port pour le mode Web")

    args = parser.parse_args()

    if args.mode == 'cli':
        if not args.query:
            print("Erreur: --query est requis en mode CLI")
        else:
            run_cli(args.query, args.region)
    elif args.mode == 'web':
        run_web(args.port)
