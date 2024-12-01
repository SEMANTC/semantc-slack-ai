# app/slack/events.py

from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)

class EventHandler:
    """Handles Slack events"""
    
    async def handle_event(self, event: Dict[str, Any]) -> None:
        """
        Handle incoming Slack events
        Args:
            event: Slack event data
        """
        try:
            event_type = event.get('type')
            
            if event_type == 'url_verification':
                return self._handle_url_verification(event)
            
            if event_type == 'event_callback':
                return await self._handle_event_callback(event)
                
        except Exception as e:
            logger.error(f"Error handling event: {str(e)}")
            raise

    def _handle_url_verification(self, event: Dict[str, Any]) -> Dict[str, str]:
        """Handle URL verification challenge"""
        return {'challenge': event['challenge']}

    async def _handle_event_callback(self, event: Dict[str, Any]) -> None:
        """Handle event callbacks"""
        inner_event = event.get('event', {})
        event_type = inner_event.get('type')
        
        logger.info(f"Handling event callback of type: {event_type}")