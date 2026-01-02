import pytest
import asyncio
from app.agents.fertilizer.agent import FertilizerAgent

@pytest.mark.asyncio
async def test_fertilizer_agent_process():
    agent = FertilizerAgent()
    query = "Quel engrais pour le maïs ?"
    context = {"region": "Centre"}
    
    response = await agent.process(query, context)
    assert response is not None
    assert len(response) > 0
    # On vérifie que la réponse contient des termes liés à la fertilisation
    keywords = ["engrais", "NPK", "sol", "fertilisant"]
    assert any(keyword.lower() in response.lower() for keyword in keywords)

def test_fertilizer_agent_metadata():
    agent = FertilizerAgent()
    assert agent.name == "FertilizerAgent"
    assert "engrais" in agent.description.lower()
