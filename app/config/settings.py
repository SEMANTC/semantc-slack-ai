# app/config/settings.py

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # Slack Configuration
    SLACK_BOT_TOKEN: str
    SLACK_SIGNING_SECRET: str
    SLACK_APP_TOKEN: str

    # OpenAI Configuration
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4-1106-preview"  # Default to latest GPT-4
    OPENAI_TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 2000

    # Pinecone Configuration
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str
    PINECONE_INDEX_NAME: str

    # Google Cloud Settings (for future use)
    PROJECT_ID: str
    REGION: str = "us-central1"

    # Application Settings
    APP_PORT: int = 8080
    DEBUG_MODE: bool = False
    LOG_LEVEL: str = "INFO"

    # RAG Settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    MAX_CONTEXT_CHUNKS: int = 5
    SIMILARITY_THRESHOLD: float = 0.7

    # Chat Settings
    MAX_HISTORY_MESSAGES: int = 10
    SYSTEM_PROMPT: str = """You are a helpful AI assistant with access to the company's documents. 
    When asked a question, you'll search through the relevant documents and provide accurate, 
    concise answers based on the available information. If you're not sure about something or 
    if the information isn't available in the documents, please say so."""

    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_openai_config(self):
        """Get OpenAI configuration as dict"""
        return {
            "api_key": self.OPENAI_API_KEY,
            "model": self.OPENAI_MODEL,
            "temperature": self.OPENAI_TEMPERATURE,
            "max_tokens": self.MAX_TOKENS
        }

    def get_pinecone_config(self):
        """Get Pinecone configuration as dict"""
        return {
            "api_key": self.PINECONE_API_KEY,
            "environment": self.PINECONE_ENVIRONMENT,
            "index_name": self.PINECONE_INDEX_NAME
        }

    def get_slack_config(self):
        """Get Slack configuration as dict"""
        return {
            "bot_token": self.SLACK_BOT_TOKEN,
            "signing_secret": self.SLACK_SIGNING_SECRET,
            "app_token": self.SLACK_APP_TOKEN
        }

@lru_cache()
def get_settings() -> Settings:
    """Create and cache settings instance"""
    return Settings()