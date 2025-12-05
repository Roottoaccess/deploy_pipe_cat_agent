# Pipecat Voice Agent with LiveKit on Render

This project deploys a Pipecat voice AI agent on Render using **LiveKit Cloud** for WebRTC transport. 

## Key Features

✅ **No UDP Required** - All communication uses WebSocket signaling through LiveKit Cloud  
✅ **Render Compatible** - Works perfectly on Render's platform (TCP/WebSocket only)  
✅ **No Socket Errors** - Eliminates `asyncio:socket.send() raised exception` warnings  
✅ **Cloud WebRTC** - LiveKit Cloud handles all WebRTC peer connections  

## Architecture

```
Client Browser
    ↓ (WebSocket)
LiveKit Cloud (handles WebRTC)
    ↓ (WebSocket)
Render Server (FastAPI)
    ↓
Pipecat Agent (STT → LLM → TTS)
```

## Environment Variables

Set these in your Render dashboard:

```bash
# LiveKit Cloud (REQUIRED)
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret

# AI Services (REQUIRED)
DEEPGRAM_API_KEY=your_deepgram_api_key
OPENAI_API_KEY=your_openai_api_key
CARTESIA_API_KEY=your_cartesia_api_key

# Server (Optional - Render provides PORT automatically)
HOST=0.0.0.0
LOG_LEVEL=INFO
```

## Getting LiveKit Credentials

1. Sign up at [LiveKit Cloud](https://cloud.livekit.io)
2. Create a new project
3. Get your:
   - **URL**: `wss://your-project.livekit.cloud`
   - **API Key**: From project settings
   - **API Secret**: From project settings

## API Endpoints

### `POST /agent`
Start a new agent session in a LiveKit room.

**Request:**
```json
{
  "room": "my-room-name",
  "participant_identity": "agent"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Agent connection initiated",
  "room": "my-room-name",
  "participant": "agent"
}
```

### `POST /offer`
Get a LiveKit token for client connection.

**Request:**
```json
{
  "room": "my-room-name"
}
```

**Response:**
```json
{
  "status": "success",
  "token": "eyJ...",
  "url": "wss://your-project.livekit.cloud",
  "room": "my-room-name"
}
```

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "pipecat-livekit-agent",
  "livekit_configured": true
}
```

## Deployment on Render

1. **Connect Repository** to Render
2. **Set Environment Variables** in Render dashboard
3. **Build Settings:**
   - **Root Directory**: `pipecat/examples/quickstart`
   - **Dockerfile Path**: `Dockerfile`
4. **Deploy**

The server will automatically:
- Use Render's `PORT` environment variable
- Start on `0.0.0.0` (required for Render)
- Connect to LiveKit Cloud via WebSocket

## How It Works

1. **Client connects** to LiveKit Cloud (WebSocket)
2. **LiveKit Cloud** handles all WebRTC signaling and media
3. **Render server** receives WebSocket connections from LiveKit
4. **Pipecat agent** processes audio through STT → LLM → TTS pipeline
5. **Audio flows back** through LiveKit Cloud to client

## Differences from SmallWebRTC

| Feature | SmallWebRTC | LiveKit |
|---------|-------------|---------|
| Transport | Direct WebRTC | LiveKit Cloud |
| Signaling | WebSocket | WebSocket |
| Media | UDP (fails on Render) | LiveKit Cloud handles |
| Server Requirements | UDP ports | TCP/WebSocket only ✅ |
| Render Compatibility | ❌ | ✅ |

## Testing Locally

1. Set environment variables in `.env` file
2. Run: `python main.py`
3. Server starts on `http://localhost:7860`
4. Test endpoints with curl or Postman

## Troubleshooting

### "Missing LiveKit environment variables"
- Ensure `LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET` are set

### "Agent connection failed"
- Check LiveKit credentials are correct
- Verify room name is valid
- Check Render logs for detailed errors

### "Health check fails"
- Verify all environment variables are set
- Check that LiveKit URL is correct format: `wss://...`

## Next Steps

- Add authentication to `/agent` endpoint
- Implement room management
- Add metrics and monitoring
- Scale with multiple agent instances

