import asyncio
import os
import sys
import pytest

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.agents.economic import EconomicAgent

@pytest.mark.asyncio
async def test_economic_agent():
    print("--- Test Economic Agent ---")
    agent = EconomicAgent()
    
    queries = [
        ("PRICES", "Combien coûte le sac de maïs à Yaoundé ?"),
        ("PROFITABILITY", "Est-ce que la culture du piment est rentable ?"),
        ("TRENDS", "Le prix du cacao va-t-il monter ?"),
        ("STRATEGY", "Comment mieux vendre ma récolte de plantain ?"),
        ("OPPORTUNITIES", "Quoi planter pour gagner de l'argent rapidement ?")
    ]
    
    context = {"region": "Centre"}
    
    for intent, query in queries:
        print(f"\nTesting Intent: {intent}")
        print(f"Query: {query}")
        try:
            response = await agent.process(query, context)
            print(f"Response (Prefix):\n{response[:200]}...")
            print("Status: OK")
        except Exception as e:
            print(f"Status: FAILED - {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_economic_agent())
