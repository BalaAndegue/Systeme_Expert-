from app.agents.base_agent import BaseAgent
from typing import Dict, Any
from .prompt import get_system_prompt
from .tools import fetch_market_prices, format_prices_for_prompt

class EconomicAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="EconomicAgent",
            description="Économiste agricole. Informe sur les prix du marché, les tendances et la rentabilité des cultures."
        )

    async def process(self, query: str, context: Dict[str, Any]) -> str:
        prices = fetch_market_prices()
        prices_str = format_prices_for_prompt(prices)
        
        system_prompt = get_system_prompt(prices_str)
        
        return await self.llm_service.generate_response(query, system_prompt)
