# app/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

from .config import get_settings
from .slack import SlackBot
from .utils import setup_logger

# Initialize settings and logger
settings = get_settings()
logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Slack AI Assistant",
    description="A Slack bot that uses RAG to answer questions using company documents",
    version="0.1.0",
    docs_url="/docs" if settings.DEBUG_MODE else None,
    redoc_url="/redoc" if settings.DEBUG_MODE else None
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Slack bot
slack_bot = SlackBot()

@app.on_event("startup")
async def startup():
    """Startup tasks"""
    logger.info("Starting Slack AI Assistant")
    try:
        await slack_bot.start()
    except Exception as e:
        logger.error(f"Failed to start Slack bot: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown():
    """Shutdown tasks"""
    logger.info("Shutting down Slack AI Assistant")
    try:
        await slack_bot.stop()
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "0.1.0"
    }

# Slack endpoints
app.post("/slack/events")(slack_bot.handler.handle)
app.post("/slack/commands")(slack_bot.handler.handle)

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Global error: {str(exc)}")
    return {
        "error": str(exc),
        "detail": str(exc) if settings.DEBUG_MODE else "Internal server error"
    }, 500

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.APP_PORT,
        reload=settings.DEBUG_MODE
    )