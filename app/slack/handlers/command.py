# app/slack/handlers/command.py

from typing import Any, Dict
import logging

from ...config import get_settings
from ...retrieval import ChatEngine
from ...models import Message, MessageType

logger = logging.getLogger(__name__)
settings = get_settings()

class CommandHandler:
    """Handles Slack commands"""
    
    def __init__(self):
        self.chat_engine = ChatEngine()

    async def handle_ask(self, command: Dict[str, Any], say: Any) -> None:
        """
        Handle /ask command
        Args:
            command: Command data
            say: Slack say function
        """
        try:
            # Create message from command
            message = Message(
                id=command['command_ts'],
                channel_id=command['channel_id'],
                user_id=command['user_id'],
                thread_ts=None,
                message_type=MessageType.USER,
                content=command['text'],
                timestamp=command['command_ts']
            )

            # Process message
            response = await self.chat_engine.process_message(message)

            # Send response
            await say(text=response.content)

        except Exception as e:
            logger.error(f"Error handling ask command: {str(e)}")
            await say(f"Sorry, I encountered an error: {str(e)}")

    async def handle_help(self, command: Dict[str, Any], say: Any) -> None:
        """
        Handle /help command
        Args:
            command: Command data
            say: Slack say function
        """
        help_text = """
*Available Commands:*
- `/ask [question]` - Ask a question about company documents
- `/help` - Show this help message

*Tips:*
- Use threads for related questions
- Be specific in your questions
- You can ask follow-up questions in threads
"""
        await say(text=help_text)