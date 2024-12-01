# app/database/conversation.py

from google.cloud import firestore
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import logging

from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class ConversationStore:
    def __init__(self):
        """Initialize Firestore for conversation storage"""
        self.db = firestore.Client(project=settings.PROJECT_ID)
        self.collection = self.db.collection('conversations')

    async def save_message(
        self,
        channel_id: str,
        user_id: str,
        message_type: str,
        content: str,
        thread_ts: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Save a conversation message
        Args:
            channel_id: Slack channel ID
            user_id: User ID
            message_type: Type of message (user/assistant)
            content: Message content
            thread_ts: Thread timestamp if in thread
            metadata: Additional metadata
        """
        try:
            message_data = {
                'channel_id': channel_id,
                'user_id': user_id,
                'message_type': message_type,
                'content': content,
                'thread_ts': thread_ts,
                'metadata': metadata or {},
                'timestamp': firestore.SERVER_TIMESTAMP
            }
            
            # Use thread_ts as document ID if available, else generate new
            doc_id = thread_ts or f"{channel_id}-{datetime.utcnow().timestamp()}"
            
            # Save to Firestore
            doc_ref = self.collection.document(doc_id)
            doc_ref.set(message_data)
            
            return doc_id
            
        except Exception as e:
            logger.error(f"Error saving message: {str(e)}")
            raise

    async def get_conversation_history(
        self,
        channel_id: str,
        thread_ts: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get conversation history
        Args:
            channel_id: Slack channel ID
            thread_ts: Thread timestamp if in thread
            limit: Maximum number of messages to return
        """
        try:
            # Build query
            query = self.collection.where('channel_id', '==', channel_id)
            
            if thread_ts:
                query = query.where('thread_ts', '==', thread_ts)
            
            # Execute query
            docs = query.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit).stream()
            
            # Format results
            messages = []
            for doc in docs:
                message_data = doc.to_dict()
                message_data['id'] = doc.id
                messages.append(message_data)
            
            return messages
            
        except Exception as e:
            logger.error(f"Error getting conversation history: {str(e)}")
            return []

    async def delete_conversation(
        self,
        channel_id: str,
        thread_ts: Optional[str] = None
    ) -> bool:
        """
        Delete conversation history
        Args:
            channel_id: Slack channel ID
            thread_ts: Thread timestamp if in thread
        """
        try:
            query = self.collection.where('channel_id', '==', channel_id)
            
            if thread_ts:
                query = query.where('thread_ts', '==', thread_ts)
            
            # Delete documents
            docs = query.stream()
            for doc in docs:
                doc.reference.delete()
            
            return True
            
        except Exception as e:
            logger.error(f"Error deleting conversation: {str(e)}")
            return False