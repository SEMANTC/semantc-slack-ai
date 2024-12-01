# app/utils/helpers.py

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
import re

def generate_uuid() -> str:
    """Generate a unique identifier"""
    return str(uuid.uuid4())

def parse_timestamp(ts: str) -> datetime:
    """
    Parse Slack timestamp to datetime
    Args:
        ts: Slack timestamp string
    Returns:
        Datetime object
    """
    try:
        return datetime.fromtimestamp(float(ts))
    except (ValueError, TypeError):
        return datetime.utcnow()

def format_slack_message(
    text: str,
    code_blocks: bool = True,
    links: bool = True,
    mentions: bool = True
) -> str:
    """
    Format text for Slack messaging
    Args:
        text: Input text
        code_blocks: Format code blocks
        links: Format links
        mentions: Format mentions
    Returns:
        Formatted text
    """
    # Format code blocks
    if code_blocks:
        text = re.sub(r'```(.*?)```', r'```\1```', text, flags=re.DOTALL)
        text = re.sub(r'`([^`]+)`', r'`\1`', text)
    
    # Format links
    if links:
        text = re.sub(r'<(https?://[^|>]+)\|([^>]+)>', r'\2', text)
        text = re.sub(r'<(https?://[^>]+)>', r'\1', text)
    
    # Format mentions
    if mentions:
        text = re.sub(r'<@([A-Z0-9]+)>', r'@\1', text)
    
    return text

def chunk_message(
    message: str,
    max_length: int = 3000,
    chunk_prefix: str = "",
    chunk_suffix: str = ""
) -> List[str]:
    """
    Split long message into chunks for Slack
    Args:
        message: Message to split
        max_length: Maximum chunk length
        chunk_prefix: Prefix for each chunk
        chunk_suffix: Suffix for each chunk
    Returns:
        List of message chunks
    """
    if len(message) <= max_length:
        return [message]
    
    chunks = []
    current_chunk = ""
    
    # Split on newlines if possible
    lines = message.split('\n')
    
    for line in lines:
        if len(current_chunk) + len(line) + 1 <= max_length:
            current_chunk += line + '\n'
        else:
            if current_chunk:
                chunks.append(chunk_prefix + current_chunk.rstrip() + chunk_suffix)
            current_chunk = line + '\n'
    
    if current_chunk:
        chunks.append(chunk_prefix + current_chunk.rstrip() + chunk_suffix)
    
    return chunks

def format_error_message(error: Exception, include_trace: bool = False) -> str:
    """
    Format error message for Slack
    Args:
        error: Exception object
        include_trace: Include stack trace
    Returns:
        Formatted error message
    """
    message = f"Error: {str(error)}"
    
    if include_trace and settings.DEBUG_MODE:
        import traceback
        trace = traceback.format_exc()
        message += f"\n```{trace}```"
    
    return message

def sanitize_text(text: str) -> str:
    """
    Sanitize text for safe storage/display
    Args:
        text: Input text
    Returns:
        Sanitized text
    """
    # Remove control characters
    text = ''.join(char for char in text if ord(char) >= 32 or char == '\n')
    
    # Basic HTML escape
    text = (
        text.replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
        .replace("'", '&#39;')
    )
    
    return text

def parse_slack_metadata(
    metadata: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Parse and validate Slack event metadata
    Args:
        metadata: Raw metadata dictionary
    Returns:
        Parsed metadata or None if invalid
    """
    try:
        return {
            'team_id': metadata.get('team_id'),
            'channel_id': metadata.get('channel_id'),
            'user_id': metadata.get('user_id'),
            'thread_ts': metadata.get('thread_ts'),
            'event_id': metadata.get('event_id'),
            'event_time': parse_timestamp(metadata.get('event_ts', '')),
        }
    except Exception:
        return None