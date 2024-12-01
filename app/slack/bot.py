# app/slack/bot.py

from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
import logging

from ..config import get_settings
from .events import EventHandler
from .handlers import MessageHandler, CommandHandler

logger = logging.getLogger(__name__)
settings = get_settings()

class SlackBot:
    """Slack Bot implementation"""
    
    def __init__(self):
        """Initialize Slack bot"""
        self.app = AsyncApp(
            token=settings.SLACK_BOT_TOKEN,
            signing_secret=settings.SLACK_SIGNING_SECRET
        )
        
        # Initialize handlers
        self.event_handler = EventHandler()
        self.message_handler = MessageHandler()
        self.command_handler = CommandHandler()
        
        # Register event listeners
        self.register_listeners()
        
        # Create FastAPI handler
        self.handler = AsyncSlackRequestHandler(self.app)

    def register_listeners(self):
        """Register event listeners"""
        
        @self.app.event("message")
        async def handle_message(event, say, context):
            """Handle message events"""
            try:
                await self.message_handler.handle(event, say, context)
            except Exception as e:
                logger.error(f"Error handling message: {str(e)}")
                await say(f"Sorry, I encountered an error: {str(e)}")

        @self.app.command("/ask")
        async def handle_ask_command(ack, command, say):
            """Handle /ask command"""
            await ack()
            try:
                await self.command_handler.handle_ask(command, say)
            except Exception as e:
                logger.error(f"Error handling ask command: {str(e)}")
                await say(f"Sorry, I encountered an error: {str(e)}")

        @self.app.command("/help")
        async def handle_help_command(ack, command, say):
            """Handle /help command"""
            await ack()
            try:
                await self.command_handler.handle_help(command, say)
            except Exception as e:
                logger.error(f"Error handling help command: {str(e)}")
                await say(f"Sorry, I encountered an error: {str(e)}")

    async def start(self):
        """Start the bot"""
        await self.app.start()

    async def stop(self):
        """Stop the bot"""
        await self.app.stop()