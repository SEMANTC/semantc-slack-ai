# app/slack/handlers/command.py
from typing import Any, Dict
import logging
import time
import asyncio  # Add this import

from ...config import get_settings
from ...retrieval import ChatEngine
from ...models import Message, MessageType

logger = logging.getLogger(__name__)
settings = get_settings()

class CommandHandler:
    async def handle_ask(self, command_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # First, acknowledge the command immediately
            await command_data['ack']()  # This tells Slack we received the command
            
            text = command_data.get("text", "").strip()
            if not text:
                return {
                    "response_type": "ephemeral",
                    "text": "Please provide a question after /ask"
                }

            # Process in background
            asyncio.create_task(self._process_and_respond(command_data))

            # Return immediate acknowledgment
            return {
                "response_type": "ephemeral",
                "text": "Processing your question..."
            }

        except Exception as e:
            logger.exception("Error in handle_ask:")
            return {
                "response_type": "ephemeral",
                "text": f"Sorry, I encountered an error: {str(e)}"
            }

    async def _process_and_respond(self, command_data: Dict[str, Any]):
        """Process the question and respond using Slack's say function"""
        try:
            message = Message(
                id=command_data["command_ts"],
                channel_id=command_data["channel_id"],
                user_id=command_data["user_id"],
                thread_ts=None,
                message_type=MessageType.USER,
                content=command_data["text"]
            )

            response = await self.chat_engine.process_message(message)
            
            # Use Slack's say function to send the response
            await command_data['say']({
                "text": response.content,
                "thread_ts": command_data.get("thread_ts")
            })

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            await command_data['say']({
                "text": "Sorry, I encountered an error processing your question.",
                "thread_ts": command_data.get("thread_ts")
            })

    async def handle_help(self, command_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle /help command
        Args:
            command_data: Command data from Slack
        Returns:
            Response to send back to Slack
        """
        try:
            help_text = """
*Available Commands:*
- `/ask [question]` - Ask a question about company documents
- `/help` - Show this help message

*Tips:*
- Be specific in your questions
- Include relevant context in your questions
- Use threads for follow-up questions
- For best results, mention specific topics or documents
            """
            
            return {
                "response_type": "ephemeral",
                "text": help_text,
                "thread_ts": command_data.get("thread_ts")
            }

        except Exception as e:
            logger.error(f"Error handling help command: {str(e)}")
            return {
                "response_type": "ephemeral",
                "text": "Sorry, I encountered an error showing the help message."
            }

    def _format_error_message(self, error: str) -> str:
        """Format error message for user display"""
        return f"Sorry, I encountered an error: {error}"