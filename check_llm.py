import asyncio
from app.services.llm_service import LLMService

async def test_llm():
    service = LLMService()
    response = await service.generate_response("Bonjour", "Tu es un assistant.")
    print(f"LLM Response: {response}")

if __name__ == "__main__":
    asyncio.run(test_llm())
