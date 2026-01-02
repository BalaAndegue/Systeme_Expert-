from app.agents.base_agent import BaseAgent
from typing import Dict, Any
from .prompt import get_system_prompt

class FertilizerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="FertilizerAgent",
            description="Expert en fertilisation et amendements des sols au Cameroun. Conseille sur les types d'engrais et les périodes d'application."
        )

    async def process(self, query: str, context: Dict[str, Any]) -> str:
        system_prompt = get_system_prompt()
        return await self.llm_service.generate_response(query, system_prompt)
