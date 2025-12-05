# LiveKit Setup Verification Guide

## Quick Verification

After deployment, check these endpoints:

### 1. Health Check
```bash
curl https://your-service.onrender.com/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "pipecat-livekit-agent",
  "livekit_configured": true,
  "livekit_token_generation": "working",
  "ai_services": {
    "deepgram": true,
    "openai": true,
    "cartesia": true
  },
  "bot_py": "available",
  "agent_py": "available"
}
```

### 2. Client Interface
Visit: `https://your-service.onrender.com/client`

You should see:
- ✅ Web interface loads
- ✅ Microphone selection dropdown
- ✅ Connect button
- ✅ Status display

### 3. Test Agent Endpoint
```bash
curl -X POST https://your-service.onrender.com/agent \
  -H "Content-Type: application/json" \
  -d '{"room": "test-room-123"}'
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Agent connection initiated",
  "room": "test-room-123",
  "participant": "agent"
}
```

### 4. Test Offer Endpoint
```bash
curl -X POST https://your-service.onrender.com/offer \
  -H "Content-Type: application/json" \
  -d '{"room": "test-room-123"}'
```

**Expected Response:**
```json
{
  "status": "success",
  "token": "eyJ...",
  "url": "wss://your-project.livekit.cloud",
  "room": "test-room-123"
}
```

## Dependency Verification

### Required Python Packages
All these should be installed (check via `/health` endpoint):

- ✅ `fastapi` - Web framework
- ✅ `uvicorn` - ASGI server
- ✅ `livekit` - LiveKit SDK
- ✅ `pipecat-ai` - Pipecat framework
- ✅ `python-dotenv` - Environment variables

### Required System Packages
- ✅ `ffmpeg` - Audio processing (installed in Dockerfile)
- ✅ `build-essential` - Compilation tools
- ✅ `curl` - For downloading uv

## Connection Flow Verification

### Step 1: Client Connects
1. User visits `/client`
2. Selects microphone
3. Clicks "Connect"
4. Client gets token from `/offer`
5. Client connects to LiveKit Cloud

### Step 2: Agent Starts
1. Client calls `/agent` endpoint
2. Server creates `VoiceAgent` from `agent.py`
3. `VoiceAgent.start()` is called
4. LiveKit transport is created
5. `bot.py`'s `run_bot()` function is called
6. Bot pipeline starts (STT → LLM → TTS)

### Step 3: Communication
1. User speaks → Microphone → LiveKit Cloud
2. LiveKit Cloud → Render Server (WebSocket)
3. Render Server → `bot.py` pipeline
4. Pipeline processes: STT → LLM → TTS
5. TTS audio → LiveKit Cloud → User

## Troubleshooting

### Health Check Shows Issues

**`livekit_configured: false`**
- Set `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET` in Render

**`livekit_token_generation: "error"`**
- Check API key and secret are correct
- Verify URL format: `wss://your-project.livekit.cloud`

**`ai_services: {deepgram: false, ...}`**
- Set missing API keys in Render environment variables

**`bot_py: "error"`**
- Check that `bot.py` is copied in Dockerfile
- Verify imports work correctly

### Connection Issues

**Client can't connect:**
- Check LiveKit URL is correct
- Verify token generation works (`/offer` endpoint)
- Check browser console for errors

**Agent doesn't start:**
- Check Render logs for errors
- Verify all environment variables are set
- Check `/agent` endpoint returns success

**No audio:**
- Check microphone permissions in browser
- Verify audio devices are available
- Check LiveKit Cloud dashboard for room status

## Testing Locally

Before deploying, test locally:

```bash
# Set environment variables
export LIVEKIT_URL=wss://your-project.livekit.cloud
export LIVEKIT_API_KEY=your_key
export LIVEKIT_API_SECRET=your_secret
export DEEPGRAM_API_KEY=your_key
export OPENAI_API_KEY=your_key
export CARTESIA_API_KEY=your_key

# Run test script
python test_setup.py

# Start server
python main.py

# Test endpoints
curl http://localhost:7860/health
curl http://localhost:7860/client
```

## Success Criteria

✅ `/health` returns all checks passing  
✅ `/client` loads web interface  
✅ `/agent` starts agent successfully  
✅ `/offer` generates valid tokens  
✅ Client can connect to LiveKit  
✅ Audio flows both ways  
✅ Bot responds to speech  

## Next Steps After Verification

1. **Monitor Logs** - Check Render logs for any errors
2. **Test Connection** - Use `/client` to connect and speak
3. **Verify Audio** - Ensure you can hear the bot and it can hear you
4. **Check Performance** - Monitor response times and latency

Your setup is working when:
- Health check shows all green ✅
- Client interface loads and connects
- Bot responds to your voice
- No errors in Render logs

