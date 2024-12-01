# app/__init__.py

from .config import get_settings
from .slack import SlackBot
from .retrieval import ChatEngine, RAGEngine
from .database import VectorStore, ConversationStore

__version__ = "0.1.0"

__all__ = [
    'SlackBot',
    'ChatEngine',
    'RAGEngine',
    'VectorStore',
    'ConversationStore',
    'get_settings'
]