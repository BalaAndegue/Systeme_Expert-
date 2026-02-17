from typing import List, Dict, Any
from app.agents.base_agent import BaseAgent
from app.services.llm_service import LLMService

class AgentOrchestrator:
    def __init__(self, agents: List[BaseAgent]):
        self.agents = {agent.name: agent for agent in agents}
        self.llm_service = LLMService()
        self.context = {}
        self.max_response_words = 300  # Limite globale

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
        
        responses = {}
        
        # 2. Appel agents (parallèle potentiel futur)
        for name in target_agent_names:
            agent = self.agents[name]
            response = await agent.process(query, self.context)
            responses[name] = response
            
        return responses
    
    async def synthesize_response(self, query: str, agent_responses: Dict[str, str]) -> str:
        """Synthèse optimisée pour CONCISION MAXIMALE."""
        if not agent_responses:
            return "❌ Aucune réponse disponible. Reformulez votre question."
        
        # Agent unique: retour direct
        if len(agent_responses) == 1:
            response = list(agent_responses.values())[0]
            # Vérifier longueur et condenser si nécessaire
            return await self._ensure_concise(response, query)
        
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
        
        synthesized = await self.llm_service.generate_response(prompt)
        return await self._ensure_concise(synthesized, query)
    
    async def _ensure_concise(self, response: str, query: str) -> str:
        """Vérifie et force concision si dépassement."""
        word_count = len(response.split())
        
        if word_count <= self.max_response_words:
            return response
        
        # Dépassement: condensation forcée
        print(f"WARNING: Réponse trop longue ({word_count} mots). Condensation...")
        
        condense_prompt = f"""CONDENSATION URGENTE (réponse trop longue).

Réponse originale ({word_count} mots):
{response}

Question: "{query}"

Réduis à MAXIMUM {self.max_response_words} mots en gardant:
✅ Chiffres et données clés
✅ Actions immédiates
✅ Informations essentielles
❌ Éliminer détails secondaires
❌ Éliminer répétitions

Format: Bullets ultra-concis avec icônes."""
        
        condensed = await self.llm_service.generate_response(condense_prompt)
        return condensed
