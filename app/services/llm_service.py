from openai import AsyncOpenAI, OpenAI
from config import Config
import os

class LLMService:
    def __init__(self):
        self.client = None
        self.provider = Config.LLM_PROVIDER.lower()
        
        api_key = None
        base_url = None
        
        if self.provider == "openrouter":
            api_key = Config.OPENROUTER_API_KEY
            base_url = "https://openrouter.ai/api/v1"
        elif self.provider == "grok":
            api_key = Config.GROK_API_KEY
            base_url = "https://api.x.ai/v1"
        elif self.provider == "openai":
             api_key = os.getenv("OPENAI_API_KEY") 
             # default base_url

        if api_key:
            self.client = AsyncOpenAI(
                api_key=api_key,
                base_url=base_url
            )
            self.sync_client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )
        else:
            print(f"WARNING: API Key for {self.provider} not found. AI features disabled.")

    async def generate_response(self, prompt: str, system_instruction: str = None) -> str:
        if not self.client:
            return "Service IA non configuré."
        
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        try:
            response = await self.client.chat.completions.create(
                model=Config.LLM_MODEL,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Erreur LLM ({self.provider}): {str(e)}"

    def generate_sync(self, prompt: str) -> str:
        if not self.sync_client:
             return "Service IA non configuré."
        try:
            response = self.sync_client.chat.completions.create(
                model=Config.LLM_MODEL,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
             return f"Error: {e}"
