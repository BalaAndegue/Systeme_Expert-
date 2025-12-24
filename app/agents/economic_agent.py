from app.agents.base_agent import BaseAgent
from typing import Dict, Any
from app.data.market_prices import get_current_prices

class EconomicAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="EconomicAgent",
            description="Économiste agricole. Informe sur les prix du marché, les tendances et la rentabilité des cultures."
        )

    async def process(self, query: str, context: Dict[str, Any]) -> str:
        prices = get_current_prices()
        prices_str = "\n".join([f"- {p.crop_name}: {p.price_avg_fcfa} FCFA/{p.unit} ({p.trend})" for p in prices])
        
        system_prompt = f"""
        Tu es un conseiller économique agricole.
        Voici les prix actuels du marché (simulés) au Cameroun :
        {prices_str}
        
        Utilise ces données pour répondre aux questions sur les prix et la rentabilité.
        Si une culture n'est pas dans la liste, donne une estimation basée sur tes connaissances générales du marché camerounais (en précisant que c'est une estimation).
        """
        
        return await self.llm_service.generate_response(query, system_prompt)
