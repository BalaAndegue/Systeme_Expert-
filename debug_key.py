import os
from dotenv import load_dotenv
import asyncio
from app.services.llm_service import LLMService

load_dotenv()

key = os.environ.get('OPENROUTER_API_KEY')
print(f"Loaded Key: {key[:10]}...{key[-5:] if key else 'None'}")

async def test():
    service = LLMService()
    print(f"Service configured with provider: {service.provider}")
    try:
        resp = await service.generate_response("Hello")
        print(f"Response: {resp}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test())
