#!/usr/bin/env python3
"""
LiveKit AgentServer for Pipecat Voice Agent on Render.

This server uses LiveKit Cloud for WebRTC transport via WebSocket signaling only.
No UDP required - all communication goes through LiveKit's cloud infrastructure.
"""

import asyncio
import os
import sys
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

# Load environment variables
load_dotenv(override=True)

# Configure logging
logger.remove()
logger.add(sys.stderr, level=os.getenv("LOG_LEVEL", "INFO"))

# Import agent after environment is loaded
from agent import VoiceAgent

# LiveKit configuration (check but don't exit - allow server to start for health checks)
LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

LIVEKIT_CONFIGURED = bool(LIVEKIT_URL and LIVEKIT_API_KEY and LIVEKIT_API_SECRET)

if not LIVEKIT_CONFIGURED:
    logger.warning(
        "⚠️  Missing LiveKit environment variables: "
        "LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET. "
        "Server will start but agent endpoints will not work until configured."
    )
else:
    logger.info("✅ LiveKit configuration found")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    logger.info("🚀 Starting LiveKit AgentServer...")
    if LIVEKIT_CONFIGURED:
        logger.info(f"LiveKit URL: {LIVEKIT_URL}")
    else:
        logger.warning("⚠️  LiveKit not configured - agent endpoints will be unavailable")
    yield
    logger.info("🛑 Shutting down LiveKit AgentServer...")


# Create FastAPI app
app = FastAPI(
    title="Pipecat LiveKit AgentServer",
    description="Voice AI agent server using LiveKit Cloud",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - redirects to health check."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/health")


@app.get("/health")
async def health_check():
    """Health check endpoint for Render."""
    return {
        "status": "healthy",
        "service": "pipecat-livekit-agent",
        "livekit_configured": LIVEKIT_CONFIGURED,
    }


@app.post("/agent")
async def agent_endpoint(request: Request, background_tasks: BackgroundTasks):
    """
    LiveKit agent endpoint.
    
    This endpoint starts a new agent session in a LiveKit room.
    The agent connects via WebSocket to LiveKit Cloud (no UDP required).
    All WebRTC is handled by LiveKit Cloud infrastructure.
    """
    if not LIVEKIT_CONFIGURED:
        raise HTTPException(
            status_code=503,
            detail="LiveKit not configured. Please set LIVEKIT_URL, LIVEKIT_API_KEY, and LIVEKIT_API_SECRET environment variables."
        )
    
    try:
        # Get the request body
        body = await request.json()
        logger.info(f"Received agent request: {body}")
        
        # Extract room and participant info
        room_name = body.get("room")
        participant_identity = body.get("participant_identity", "agent")
        
        if not room_name:
            raise HTTPException(status_code=400, detail="Missing 'room' in request body")
        
        # Create agent instance
        agent = VoiceAgent(
            room_name=room_name,
            participant_identity=participant_identity,
        )
        
        # Start agent in background task
        async def run_agent():
            try:
                await agent.start()
            except Exception as e:
                logger.error(f"Agent error: {e}", exc_info=True)
        
        background_tasks.add_task(run_agent)
        
        return {
            "status": "success",
            "message": "Agent connection initiated",
            "room": room_name,
            "participant": participant_identity,
        }
    except Exception as e:
        logger.error(f"Error in agent endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/offer")
async def offer_endpoint(request: Request):
    """
    WebRTC offer endpoint (for compatibility).
    
    Note: With LiveKit, WebRTC signaling is handled by LiveKit Cloud.
    This endpoint is kept for compatibility but redirects to LiveKit.
    """
    if not LIVEKIT_CONFIGURED:
        raise HTTPException(
            status_code=503,
            detail="LiveKit not configured. Please set LIVEKIT_URL, LIVEKIT_API_KEY, and LIVEKIT_API_SECRET environment variables."
        )
    
    try:
        body = await request.json()
        logger.info(f"Received offer request: {body}")
        
        # With LiveKit, offers are handled by LiveKit Cloud
        # We just need to return a token for the client to connect
        room_name = body.get("room") or f"room-{asyncio.get_event_loop().time()}"
        
        # Generate LiveKit token
        from livekit import api
        
        token = api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        token.with_identity("user").with_name("User").with_grants(
            api.VideoGrants(room_join=True, room=room_name)
        )
        jwt_token = token.to_jwt()
        
        return {
            "status": "success",
            "token": jwt_token,
            "url": LIVEKIT_URL,
            "room": room_name,
        }
    except Exception as e:
        logger.error(f"Error in offer endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment (Render provides this)
    # Render automatically sets PORT, but we default to 7860 for local dev
    port = int(os.getenv("PORT", "7860"))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"🚀 Starting server on {host}:{port}")
    logger.info(f"📡 Health check available at http://{host}:{port}/health")
    
    # Use uvicorn.run with app object directly for better port binding
    uvicorn.run(
        app,  # Pass app object directly instead of string
        host=host,
        port=port,
        log_level="info",
        reload=False,  # Disable reload in production
    )

