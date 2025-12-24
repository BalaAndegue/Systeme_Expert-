from app.services.llm_service import LLMService
from typing import Any, Dict

class BaseAgent:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.llm_service = LLMService()

    async def process(self, query: str, context: Dict[str, Any]) -> str:
        """
        Méthode principale à surcharger ou utiliser telle quelle avec un prompt système dynamique.
        """
        system_prompt = self._build_system_prompt(context)
        response = await self.llm_service.generate_response(query, system_prompt)
        return response

    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        """Construit le prompt système avec le contexte"""
        base_prompt = f"Tu es l'agent {self.name}. Ton rôle est : {self.description}.\n"
        base_prompt += "Contexte actuel :\n"
        for k, v in context.items():
            base_prompt += f"- {k}: {v}\n"
        base_prompt += "\nRéponds de manière concise et utile pour un agriculteur camerounais."
        return base_prompt

    def can_handle(self, query: str) -> bool:
        return True
