# app/utils/logger.py

import logging
import sys
from typing import Optional
from ..config import get_settings

settings = get_settings()

def setup_logger(
    name: str,
    level: Optional[int] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Setup a logger with standard configuration
    Args:
        name: Logger name
        level: Logging level
        format_string: Custom format string
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    
    if level is None:
        level = logging.DEBUG if settings.DEBUG_MODE else logging.INFO
    logger.setLevel(level)
    
    if not format_string:
        format_string = (
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            if settings.DEBUG_MODE
            else '%(levelname)s - %(message)s'
        )
    
    # Create handler if none exists
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(format_string))
        logger.addHandler(handler)
        
        # Add file handler in debug mode
        if settings.DEBUG_MODE:
            file_handler = logging.FileHandler('app.log')
            file_handler.setFormatter(logging.Formatter(format_string))
            logger.addHandler(file_handler)
    
    return logger