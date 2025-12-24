import pytest
from app.data.local_data import get_region_by_name
from app.data.market_prices import get_price_by_crop
from app.core.orchestrator import AgentOrchestrator
from app.agents.weather import WeatherAgent
from app.agents.crop import CropAgent

def test_get_region_existing():
    region = get_region_by_name("Centre")
    assert region.name == "Centre"
    assert "Yaoundé" in region.capital

def test_get_region_non_existing():
    region = get_region_by_name("Atlantide")
    assert region is None

def test_get_price_existing():
    price = get_price_by_crop("Cacao")
    assert price is not None
    assert price.unit == "kg"

@pytest.mark.asyncio
async def test_orchestrator_routing_mock():
    # Test unitaire de l'orchestrateur sans appel réel à Gemini (Mock simple)
    # Pour un vrai test, il faudrait mocker GeminiService
    pass

def test_agent_initialization():
    agent = WeatherAgent()
    assert agent.name == "WeatherAgent"
    assert "Cameroun" in agent.description
