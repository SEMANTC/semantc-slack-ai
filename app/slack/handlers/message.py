# app/slack/handlers/message.py

from typing import Any, Dict
import logging

from ...retrieval import ChatEngine
from ...models import Message, MessageType
from ...config import get_settings
from ...database import ConversationStore

logger = logging.getLogger(__name__)
settings = get_settings()

class MessageHandler:
    """Handles Slack messages"""
    
    def __init__(self):
        self.chat_engine = ChatEngine()
        self.conversation_store = ConversationStore()

    async def handle(self, event: Dict[str, Any], say: Any, context: Dict[str, Any]) -> None:
        """
        Handle incoming messages
        Args:
            event: Message event data
            say: Slack say function
            context: Event context
        """
        try:
            # Ignore bot messages
            if event.get('bot_id'):
                return

            # Create message object
            message = Message(
                id=event['ts'],
                channel_id=event['channel'],
                user_id=event['user'],
                thread_ts=event.get('thread_ts'),
                message_type=MessageType.USER,
                content=event['text'],
                timestamp=event['ts']
            )

            # Get conversation history if in thread
            history = []
            if message.thread_ts:
                history = await self.conversation_store.get_conversation_history(
                    channel_id=message.channel_id,
                    thread_ts=message.thread_ts
                )

            # Process message
            response = await self.chat_engine.process_message(
                message=message,
                conversation_history=history
            )

            # Save response to conversation history
            await self.conversation_store.save_message(
                channel_id=response.channel_id,
                user_id=response.user_id,
                message_type=response.message_type,
                content=response.content,
                thread_ts=response.thread_ts,
                metadata=response.metadata
            )

            # Send response
            await say(
                text=response.content,
                thread_ts=message.thread_ts
            )

        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
            await say(
                text=f"Sorry, I encountered an error: {str(e)}",
                thread_ts=message.thread_ts
            )