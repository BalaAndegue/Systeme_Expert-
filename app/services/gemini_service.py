import google.generativeai as genai
from config import Config

class GeminiService:
    def __init__(self):
        if Config.GEMINI_API_KEY:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        else:
            self.model = None
            print("WARNING: GEMINI_API_KEY not found. AI features will be disabled.")

    async def generate_response(self, prompt: str, system_instruction: str = None) -> str:
        if not self.model:
            return "Pardon, je ne suis pas connecté à mon cerveau (Clé API manquante)."
        
        try:
            full_prompt = prompt
            if system_instruction:
                # Gemini Pro API doesn't strictly separate system prompt in all versions, 
                # effectively prepending it is a good strategy for simple usage
                full_prompt = f"System: {system_instruction}\n\nUser: {prompt}"
            
            response = await self.model.generate_content_async(full_prompt)
            return response.text
        except Exception as e:
            return f"Erreur lors de la génération de la réponse: {str(e)}"

    def generate_sync(self, prompt: str) -> str:
        """Version synchrone pour tests simples"""
        if not self.model:
             return "Service indisponible."
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
             return f"Error: {e}"
