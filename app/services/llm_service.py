import asyncio
import hashlib
import time
from openai import AsyncOpenAI, OpenAI
from config import Config
import os

# Cache en mémoire : clé → (réponse, timestamp)
_llm_cache: dict = {}
_CACHE_TTL = 300  # 5 minutes


def _cache_key(prompt: str, system_instruction: str | None) -> str:
    raw = f"{system_instruction or ''}||{prompt}"
    return hashlib.md5(raw.encode()).hexdigest()


def _cache_get(key: str) -> str | None:
    entry = _llm_cache.get(key)
    if entry and (time.time() - entry[1]) < _CACHE_TTL:
        return entry[0]
    return None


def _cache_set(key: str, value: str) -> None:
    _llm_cache[key] = (value, time.time())


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

        # --- Cache non-bloquant : lecture ---
        key = _cache_key(prompt, system_instruction)
        cached = _cache_get(key)
        if cached is not None:
            return cached

        # --- Appel LLM ---
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        try:
            response = await self.client.chat.completions.create(
                model=Config.LLM_MODEL,
                messages=messages
            )
            result = response.choices[0].message.content

            # --- Cache non-bloquant : écriture en arrière-plan ---
            async def _write_cache():
                _cache_set(key, result)
            asyncio.create_task(_write_cache())

            return result
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
