# app/retrieval/chat.py

from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
import logging

from ..config import get_settings
from ..models import Message, MessageType
from .rag_engine import RAGEngine

logger = logging.getLogger(__name__)
settings = get_settings()

class ChatEngine:
    """Chat interaction engine"""
    
    def __init__(self):
        self.rag_engine = RAGEngine()
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=settings.OPENAI_TEMPERATURE
        )

    async def process_message(
        self,
        message: Message,
        conversation_history: Optional[List[Message]] = None
    ) -> Message:
        """
        Process a message and generate response
        Args:
            message: Incoming message
            conversation_history: Previous messages in conversation
        Returns:
            Response message
        """
        try:
            # Get RAG response
            response_data = await self.rag_engine.get_response(
                question=message.content,
                conversation_history=conversation_history,
                user_id=message.user_id
            )
            
            # Create response message
            response_message = Message(
                id=f"resp_{message.id}",
                channel_id=message.channel_id,
                user_id="BOT",  # Bot's user ID
                thread_ts=message.thread_ts,
                message_type=MessageType.ASSISTANT,
                content=response_data["response"],
                timestamp=message.timestamp,
                metadata={
                    "context_used": response_data["context_used"],
                    "model_used": response_data["model_used"]
                }
            )
            
            return response_message
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            # Return error message
            return Message(
                id=f"error_{message.id}",
                channel_id=message.channel_id,
                user_id="BOT",
                thread_ts=message.thread_ts,
                message_type=MessageType.ERROR,
                content=f"Sorry, I encountered an error: {str(e)}",
                timestamp=message.timestamp
            )