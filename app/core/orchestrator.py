from typing import List, Dict, Any
from app.agents.base_agent import BaseAgent
from app.services.llm_service import LLMService

class AgentOrchestrator:
    def __init__(self, agents: List[BaseAgent]):
        self.agents = {agent.name: agent for agent in agents}
        self.llm_service = LLMService()
        self.context = {}

    def update_context(self, key: str, value: Any):
        self.context[key] = value

    async def route_query(self, query: str) -> List[str]:
        """Utilise le LLM pour déterminer quels agents doivent répondre."""
        agent_descriptions = "\n".join([f"- {name}: {a.description}" for name, a in self.agents.items()])
        prompt = f"""
        Voici une requête utilisateur : "{query}"
        
        Voici les agents disponibles :
        {agent_descriptions}
        
        Quels agents sont les plus pertinents pour répondre ? 
        Réponds UNIQUEMENT par une liste des noms d'agents séparés par des virgules (ex: WeatherAgent, CropAgent).
        Si aucun ne correspond parfaitement, choisis le plus proche.
        """
        
        response = await self.llm_service.generate_response(prompt)
        selected_agents = [s.strip() for s in response.split(',')]
        
        # Validation simple
        valid_agents = [name for name in selected_agents if name in self.agents]
        return valid_agents if valid_agents else list(self.agents.keys())[:1] # Fallback

    async def handle_query(self, query: str) -> Dict[str, str]:
        # 1. Identifier les agents
        target_agent_names = await self.route_query(query)
        print(f"DEBUG: Agents sélectionnés: {target_agent_names}")
        
        responses = {}
        
        # 2. Appeler les agents
        for name in target_agent_names:
            agent = self.agents[name]
            response = await agent.process(query, self.context)
            responses[name] = response
            
        return responses
    
    async def synthesize_response(self, query: str, agent_responses: Dict[str, str]) -> str:
        """Synthétise les réponses multiples en une seule cohérente."""
        if not agent_responses:
            return "Je n'ai pas pu trouver de réponse à votre question."
        
        if len(agent_responses) == 1:
            return list(agent_responses.values())[0]

        combined_text = ""
        for name, resp in agent_responses.items():
            combined_text += f"\n--- Réponse de {name} ---\n{resp}\n"

        prompt = f"""
        Synthétise ces réponses d'experts agricoles pour répondre à la question : "{query}".
        La réponse doit être fluide, pratique et intégrée (pas de "Agent X a dit que...").
        Contexte Camerounais.
        
        Données :
        {combined_text}
        """
        return await self.llm_service.generate_response(prompt)
