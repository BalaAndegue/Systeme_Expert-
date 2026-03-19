import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from app.agents.fertilizer.agent import FertilizerAgent

@pytest.mark.asyncio
@patch("app.services.llm_service.LLMService.generate_response", new_callable=AsyncMock)
async def test_fertilizer_agent_process(mock_generate_response):
    mock_generate_response.return_value = "Voici une recommandation d'engrais NPK pour le sol."
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
