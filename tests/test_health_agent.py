import asyncio
import os
import sys
import pytest

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.agents.health import HealthAgent

@pytest.mark.asyncio
async def test_health_agent():
    print("--- Test Health Agent ---")
    agent = HealthAgent()
    
    queries = [
        ("DIAGNOSIS", "Mes feuilles de cacao jaunissent et ont des taches brunes."),
        ("PEST_ID", "J'ai vu un petit insecte rouge sur les feuilles de maïs."),
        ("TREATMENT", "Comment traiter la pourriture brune du cacao ?"),
        ("PREVENTION", "Comment prévenir les maladies du plantain ?")
    ]
    
    context = {"region": "Centre"}
    
    for intent, query in queries:
        print(f"\nTesting Intent: {intent}")
        print(f"Query: {query}")
        try:
            response = await agent.process(query, context)
            print(f"Response (Prefix):\n{response[:200]}...") # Show only start
            print("Status: OK")
        except Exception as e:
            print(f"Status: FAILED - {e}")

if __name__ == "__main__":
    asyncio.run(test_health_agent())
