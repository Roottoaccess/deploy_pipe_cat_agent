# Migration from SmallWebRTC to LiveKit

This guide explains the changes made to migrate from SmallWebRTC to LiveKit Cloud.

## What Changed

### Removed
- ❌ `bot.py` (old SmallWebRTC implementation)
- ❌ SmallWebRTC transport dependencies
- ❌ WebRTC peer connection code
- ❌ ICE candidate handling
- ❌ STUN/TURN configuration
- ❌ Direct UDP connections

### Added
- ✅ `main.py` (FastAPI server with LiveKit endpoints)
- ✅ `agent.py` (LiveKit agent implementation)
- ✅ LiveKit Cloud integration
- ✅ WebSocket-only communication
- ✅ Render-compatible architecture

## File Changes

### `main.py` (NEW)
FastAPI server with three endpoints:
- `POST /agent` - Start agent session
- `POST /offer` - Get LiveKit token
- `GET /health` - Health check

### `agent.py` (NEW)
Voice agent implementation using:
- Pipecat's `LiveKitTransport`
- Deepgram STT
- OpenAI LLM
- Cartesia TTS

### `Dockerfile` (UPDATED)
- Removed OpenGL dependencies (not needed for LiveKit)
- Changed CMD to run `python main.py`
- Simplified build process

### `pyproject.toml` (UPDATED)
- Removed `webrtc` dependency
- Added `livekit` dependency
- Added `fastapi` and `uvicorn`
- Removed `pipecat-ai-cli` (not needed)

### `env.example` (UPDATED)
- Added LiveKit configuration
- Removed Daily/WebRTC options
- Added server configuration

## Environment Variables Migration

### Old (SmallWebRTC)
```bash
DEEPGRAM_API_KEY=...
OPENAI_API_KEY=...
CARTESIA_API_KEY=...
# Optional
DAILY_API_KEY=...
```

### New (LiveKit)
```bash
# LiveKit Cloud (REQUIRED)
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=...
LIVEKIT_API_SECRET=...

# AI Services (REQUIRED)
DEEPGRAM_API_KEY=...
OPENAI_API_KEY=...
CARTESIA_API_KEY=...

# Server (Optional)
HOST=0.0.0.0
PORT=7860
LOG_LEVEL=INFO
```

## Deployment Changes

### Render Configuration

**Before (SmallWebRTC):**
- Root Directory: `pipecat/examples/quickstart`
- Dockerfile Path: `Dockerfile`
- Environment: WebRTC (failed due to UDP)

**After (LiveKit):**
- Root Directory: `pipecat/examples/quickstart`
- Dockerfile Path: `Dockerfile`
- Environment: LiveKit (works with TCP/WebSocket only)

## How It Works Now

### Old Flow (SmallWebRTC)
```
Client → Direct WebRTC → Render Server (UDP) ❌ FAILS
```

### New Flow (LiveKit)
```
Client → LiveKit Cloud (WebSocket) → Render Server (WebSocket) ✅ WORKS
         ↓
    LiveKit handles WebRTC
```

## Benefits

1. **No UDP Required** - All communication via WebSocket
2. **Render Compatible** - Works on Render's platform
3. **No Socket Errors** - Eliminates `asyncio:socket.send()` warnings
4. **Cloud Infrastructure** - LiveKit handles WebRTC complexity
5. **Scalable** - LiveKit Cloud handles scaling

## Testing

### Local Testing
```bash
# Set environment variables
export LIVEKIT_URL=wss://your-project.livekit.cloud
export LIVEKIT_API_KEY=your_key
export LIVEKIT_API_SECRET=your_secret
export DEEPGRAM_API_KEY=your_key
export OPENAI_API_KEY=your_key
export CARTESIA_API_KEY=your_key

# Run server
python main.py

# Test endpoints
curl http://localhost:7860/health
curl -X POST http://localhost:7860/agent -d '{"room":"test-room"}'
```

## Troubleshooting

### "Module not found: livekit"
Install dependencies:
```bash
uv sync
```

### "LiveKit connection failed"
- Check `LIVEKIT_URL` format: must start with `wss://`
- Verify API key and secret are correct
- Check LiveKit Cloud dashboard for room status

### "Agent not starting"
- Check Render logs for detailed errors
- Verify all environment variables are set
- Ensure room name is valid

## Next Steps

1. **Get LiveKit Credentials**
   - Sign up at [LiveKit Cloud](https://cloud.livekit.io)
   - Create project and get credentials

2. **Update Render Environment**
   - Add LiveKit variables
   - Remove old WebRTC variables

3. **Deploy**
   - Push changes to repository
   - Render will rebuild automatically

4. **Test**
   - Check `/health` endpoint
   - Test `/agent` endpoint
   - Verify agent connects to LiveKit

## Support

For issues:
- Check Render logs
- Verify LiveKit Cloud dashboard
- Review environment variables
- Check API service credentials

