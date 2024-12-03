# app/main.py

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time

from .config import get_settings
from .slack import SlackBot
from .utils import setup_logger
from .models import Message, MessageType


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Initialize settings and logger
settings = get_settings()
logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Slack AI Assistant",
    description="A Slack bot that uses RAG to answer questions using company documents",
    version="0.1.0"
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

@app.on_event("shutdown")
async def shutdown():
    """Shutdown tasks"""
    logger.info("Shutting down Slack AI Assistant")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "0.1.0"
    }

# Slack endpoints
@app.post("/slack/events")
async def endpoint_slack_events(request: Request):
    """Handle Slack events"""
    try:
        return await slack_bot.handler.handle(request)
    except Exception as e:
        logger.error(f"Error handling event: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )

@app.post("/slack/commands")
async def endpoint_slack_commands(request: Request):
    """Handle Slack commands"""
    try:
        form_data = await request.form()
        command = form_data.get("command")
        
        # Create a say function for this request
        async def say(response):
            # Use Slack's Web API to send message
            await slack_bot.app.client.chat_postMessage(
                channel=form_data.get("channel_id"),
                text=response["text"],
                thread_ts=response.get("thread_ts")
            )

        # Create an ack function
        async def ack():
            return JSONResponse(content={
                "response_type": "ephemeral",
                "text": "Processing your request..."
            })

        command_data = {
            "command": command,
            "text": form_data.get("text"),
            "user_id": form_data.get("user_id"),
            "channel_id": form_data.get("channel_id"),
            "command_ts": str(time.time()),
            "say": say,
            "ack": ack
        }

        if command == "/ask":
            return await slack_bot.command_handler.handle_ask(command_data)
            
        return JSONResponse(content={
            "response_type": "ephemeral",
            "text": f"Unknown command: {command}"
        })

    except Exception as e:
        logger.error(f"Error processing command: {str(e)}")
        return JSONResponse(
            content={
                "response_type": "ephemeral",
                "text": "Sorry, something went wrong processing your command."
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.APP_PORT,
        reload=settings.DEBUG_MODE
    )