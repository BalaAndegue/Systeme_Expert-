from app.agents.base_agent import BaseAgent
from typing import Dict, Any
from .prompt import get_system_prompt

class HealthAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="HealthAgent",
            description="Phytopathologiste expert. Diagnostique les maladies des plantes et propose des traitements (biologiques et chimiques) adaptés au Cameroun."
        )

    async def process(self, query: str, context: Dict[str, Any]) -> str:
        system_prompt = get_system_prompt()
        return await self.llm_service.generate_response(query, system_prompt)
