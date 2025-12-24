import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.orchestrator import AgentOrchestrator
from app.agents.base_agent import BaseAgent
from app.services.gemini_service import GeminiService
from typing import Dict, Any

# Création d'un agent personnalisé à la volée
class CustomExpertAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ExpertSols",
            description="Expert en pédologie (étude des sols)."
        )
    
    async def process(self, query: str, context: Dict[str, Any]) -> str:
        # Logique personnalisée sans passer par Gemini pour cet exemple
        return "Analyse des sols: Sols ferrugineux tropicaux lessivés. Recommandation: Apport de matière organique."

async def main():
    print("--- Exemple d'intégration avancée (Agent Personnalisé) ---\n")
    
    # On mixe des agents standards et un agent custom
    custom_agent = CustomExpertAgent()
    orchestrator = AgentOrchestrator([custom_agent])
    
    query = "Quel type d'engrais pour mon sol ?"
    print(f"Question: {query}\n")
    
    # On force le routage pour l'exemple (bypass de Gemini pour le routing)
    # Dans la réalité, l'orchestrateur utiliserait Gemini pour choisir cet agent si la description match
    print(f"Appel direct de l'agent {custom_agent.name}...")
    response = await custom_agent.process(query, {})
    
    print(f"Réponse: {response}")

if __name__ == "__main__":
    asyncio.run(main())
