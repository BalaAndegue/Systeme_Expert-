from app.agents.base_agent import BaseAgent
from typing import Dict, Any

class HealthAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="HealthAgent",
            description="Phytopathologiste expert. Diagnostique les maladies des plantes et propose des traitements (biologiques et chimiques) adaptés au Cameroun."
        )

    async def process(self, query: str, context: Dict[str, Any]) -> str:
        system_prompt = """
        Tu es un docteur des plantes (Phytopathologiste) pour le Cameroun.
        Ton rôle est d'identifier les maladies à partir des descriptions et de proposer des solutions.
        
        Privilégie d'abord les méthodes de lutte intégrée et biologiques avant les solutions chimiques.
        Connais les ravageurs locaux (ex: Mirides du cacao, Chenille légionnaire du maïs).
        """
        
        return await self.llm_service.generate_response(query, system_prompt)
