import asyncio
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
        """Routage intelligent avec prompt optimisé."""
        agent_descriptions = "\n".join([f"- {name}: {a.description}" for name, a in self.agents.items()])
        
        prompt = f"""ROUTAGE REQUÊTE vers agents experts.

Question: "{query}"

Agents disponibles:
{agent_descriptions}

RÈGLES:
1. Sélectionner 1-2 agents MAX (combinaison si nécessaire)
2. Prioriser agent le plus spécialisé
3. Exemples:
   - "Météo demain?" → WeatherAgent
   - "Engrais pour cacao?" → FertilizerAgent
   - "Quand planter maïs et quelle météo?" → CropAgent, WeatherAgent
   - "Prix du café?" → EconomicAgent

Réponds UNIQUEMENT noms agents séparés virgules (ex: WeatherAgent, CropAgent)."""
        
        response = await self.llm_service.generate_response(prompt)
        selected_agents = [s.strip() for s in response.split(',')]
        
        # Validation
        valid_agents = [name for name in selected_agents if name in self.agents]
        
        # Limite à 2 agents max pour concision
        if len(valid_agents) > 2:
            valid_agents = valid_agents[:2]
        
        return valid_agents if valid_agents else [list(self.agents.keys())[0]]  # Fallback premier agent

    async def handle_query(self, query: str) -> Dict[str, str]:
        # 1. Routage
        target_agent_names = await self.route_query(query)
        print(f"DEBUG Orchestrator: Agents={target_agent_names}")
        
        # 2. Appel agents en PARALLÈLE via asyncio.gather
        tasks = [self.agents[name].process(query, self.context) for name in target_agent_names]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        responses = {}
        for name, result in zip(target_agent_names, results):
            if isinstance(result, Exception):
                print(f"WARNING: Agent {name} a échoué: {result}")
                responses[name] = f"⚠️ Agent {name} indisponible."
            else:
                responses[name] = result
            
        return responses
    
    async def synthesize_response(self, query: str, agent_responses: Dict[str, str]) -> str:
        """Synthèse optimisée pour CONCISION MAXIMALE."""
        if not agent_responses:
            return "❌ Aucune réponse disponible. Reformulez votre question."
        
        # Agent unique: retour direct sans appel LLM supplémentaire
        if len(agent_responses) == 1:
            return list(agent_responses.values())[0]
        
        # Multi-agents: synthèse intelligente
        combined_text = ""
        for name, resp in agent_responses.items():
            combined_text += f"\n## {name}\n{resp}\n"

        prompt = f"""SYNTHÈSE CONCISE de réponses multi-experts.

Question: "{query}"

Réponses experts:
{combined_text}

IMPÉRATIF:
✅ MAXIMUM 250 mots
✅ Intégrer informations complémentaires de manière fluide
✅ Format structuré (icônes, bullets)
✅ Chiffres précis préservés
✅ Actions pratiques prioritaires
❌ PAS "Agent X dit que..."
❌ PAS de redondances

Format: Sections courtes avec icônes thématiques."""
        
        return await self.llm_service.generate_response(prompt)
