# Render Environment Variables Setup

## Required Environment Variables

You **must** set these in your Render dashboard for the agent to work:

### LiveKit Cloud (REQUIRED)
```
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
```

### AI Services (REQUIRED)
```
DEEPGRAM_API_KEY=your_deepgram_api_key
OPENAI_API_KEY=your_openai_api_key
CARTESIA_API_KEY=your_cartesia_api_key
```

## How to Set Environment Variables in Render

1. Go to your Render dashboard
2. Click on your service
3. Go to **Environment** tab
4. Click **Add Environment Variable**
5. Add each variable one by one:
   - Key: `LIVEKIT_URL`
   - Value: `wss://your-project.livekit.cloud`
6. Repeat for all variables
7. Click **Save Changes**
8. Render will automatically redeploy

## Getting LiveKit Credentials

1. Sign up at [LiveKit Cloud](https://cloud.livekit.io)
2. Create a new project
3. Go to **Settings** → **API Keys**
4. Copy:
   - **URL**: Your project URL (e.g., `wss://your-project.livekit.cloud`)
   - **API Key**: Your API key
   - **API Secret**: Your API secret

## Verification

After setting environment variables:

1. Check `/health` endpoint:
   ```bash
   curl https://your-service.onrender.com/health
   ```
   
   Should return:
   ```json
   {
     "status": "healthy",
     "service": "pipecat-livekit-agent",
     "livekit_configured": true
   }
   ```

2. If `livekit_configured` is `false`, check:
   - All three LiveKit variables are set
   - No typos in variable names
   - Values are correct (especially URL format: `wss://...`)

## Troubleshooting

### "Missing required LiveKit environment variables"
- ✅ **FIXED**: Server now starts even without LiveKit vars
- Server will show warning but still start
- `/health` endpoint will work
- `/agent` and `/offer` will return 503 until vars are set

### "No open ports detected"
- ✅ **FIXED**: Server now properly binds to Render's PORT
- Server uses `uvicorn.run(app, ...)` for proper port binding
- Port is read from `PORT` environment variable (set by Render)

### Server starts but agent doesn't work
- Check that all LiveKit variables are set correctly
- Verify API key and secret are valid
- Check LiveKit Cloud dashboard for room status

## Quick Test

Once variables are set, test the agent:

```bash
curl -X POST https://your-service.onrender.com/agent \
  -H "Content-Type: application/json" \
  -d '{"room": "test-room"}'
```

Should return:
```json
{
  "status": "success",
  "message": "Agent connection initiated",
  "room": "test-room",
  "participant": "agent"
}
```

