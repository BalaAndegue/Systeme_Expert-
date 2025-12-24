import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base config."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-agricultura-cm'
    
    # Provider config: 'openrouter', 'grok', 'gemini' (legacy), 'openai'
    LLM_PROVIDER = os.environ.get('LLM_PROVIDER', 'openrouter') 
    
    # API Keys
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
    GROK_API_KEY = os.environ.get('GROK_API_KEY')
    
    # Model configuration
    # OpenRouter defaults to a free/cheap model if not specified, e.g., google/gemini-2.0-flash-001
    # Grok: grok-beta
    LLM_MODEL = os.environ.get('LLM_MODEL', 'google/gemini-2.0-flash-001')
    
    # Defaults
    DEFAULT_REGION = "Centre"
    DEFAULT_LANGUAGE = "fr"
    CACHE_TIMEOUT = 3600  # 1 hour
    
    # Feature flags
    ENABLE_WEB_INTERFACE = True
    ENABLE_API = True

def get_config():
    return Config
