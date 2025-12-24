import asyncio
import sys
import os

# Ajout du dossier parent au path pour pouvoir importer app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.orchestrator import AgentOrchestrator
from app.agents.weather import WeatherAgent
from app.agents.crop import CropAgent

async def main():
    print("--- Exemple d'utilisation basique ---\n")
    
    # 1. Initialisation manuelle minimale
    agents = [WeatherAgent(), CropAgent()] # On n'utilise que 2 agents pour cet exemple
    orchestrator = AgentOrchestrator(agents)
    
    # 2. Définition du contexte
    orchestrator.update_context('region', 'Nord')
    
    # 3. Requête
    query = "Est-ce le bon moment pour planter du coton ?"
    print(f"Question: {query}")
    print(f"Contexte: Région Nord\n")
    
    # 4. Traitement
    print("Consultation des agents...")
    responses = await orchestrator.handle_query(query)
    
    for name, resp in responses.items():
        print(f"\n[Réponse de {name}]:\n{resp}")
        
    # 5. Synthèse
    print("\n[Synthèse]:")
    final = await orchestrator.synthesize_response(query, responses)
    print(final)

if __name__ == "__main__":
    asyncio.run(main())
