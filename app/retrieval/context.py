# app/retrieval/context.py

from typing import List, Dict, Any
from datetime import datetime
import logging

from ..models import Message
from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class ContextManager:
    """Manages conversation context and history"""
    
    def format_conversation_history(
        self,
        messages: List[Message],
        max_messages: int = None
    ) -> str:
        """
        Format conversation history for context
        Args:
            messages: List of messages
            max_messages: Maximum number of messages to include
        Returns:
            Formatted conversation history
        """
        if not max_messages:
            max_messages = settings.MAX_HISTORY_MESSAGES
            
        # Get recent messages
        recent_messages = messages[-max_messages:]
        
        # Format messages
        formatted_messages = []
        for msg in recent_messages:
            role = "Human" if msg.message_type == "user" else "Assistant"
            formatted_messages.append(f"{role}: {msg.content}")
            
        return "\n".join(formatted_messages)

    def get_relevant_window(
        self,
        messages: List[Message],
        current_time: datetime,
        window_minutes: int = 30
    ) -> List[Message]:
        """
        Get messages within a time window
        Args:
            messages: List of messages
            current_time: Current timestamp
            window_minutes: Time window in minutes
        Returns:
            List of messages within the window
        """
        relevant_messages = []
        for msg in messages:
            time_diff = (current_time - msg.timestamp).total_seconds() / 60
            if time_diff <= window_minutes:
                relevant_messages.append(msg)
        return relevant_messages

    def merge_contexts(
        self,
        conversation_context: str,
        document_context: str,
        max_length: int = 3000
    ) -> str:
        """
        Merge conversation and document contexts
        Args:
            conversation_context: Formatted conversation history
            document_context: Retrieved document context
            max_length: Maximum context length
        Returns:
            Merged context
        """
        merged = f"{conversation_context}\n\nRelevant Information:\n{document_context}"
        if len(merged) > max_length:
            # Truncate while keeping structure
            truncated = merged[:max_length]
            last_newline = truncated.rfind("\n")
            if last_newline > 0:
                truncated = truncated[:last_newline]
            return truncated
        return merged