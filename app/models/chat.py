# app/models/chat.py

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class MessageType(str, Enum):
    """Message types"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    ERROR = "error"

class Message(BaseModel):
    """Individual message model"""
    id: str
    channel_id: str
    user_id: str
    thread_ts: Optional[str]
    message_type: MessageType
    content: str
    timestamp: datetime
    metadata: Dict[str, Any] = {}
    relevant_docs: Optional[List[str]] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class Conversation(BaseModel):
    """Conversation model"""
    id: str
    channel_id: str
    thread_ts: Optional[str]
    participants: List[str]
    messages: List[Message]
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = {}

    def add_message(self, message: Message):
        """Add a message to the conversation"""
        self.messages.append(message)
        self.updated_at = datetime.utcnow()

    def get_context(self, max_messages: int = 5) -> List[Message]:
        """Get recent conversation context"""
        return self.messages[-max_messages:]

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }