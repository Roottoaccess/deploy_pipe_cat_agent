# Deploying Pipecat Quickstart to Render

## ✅ LiveKit is NOT Required

You **do NOT need LiveKit** for Render deployment. The bot uses WebRTC transport which works perfectly on Render without any additional infrastructure.

## Environment Variables for Render

Configure these environment variables in your Render dashboard:

### Required Variables:
```
DEEPGRAM_API_KEY=your_deepgram_api_key
OPENAI_API_KEY=your_openai_api_key
CARTESIA_API_KEY=your_cartesia_api_key
```

### Optional Variables:
```
DAILY_API_KEY=your_daily_api_key  # Only if using Daily transport
```

**Note:** Render automatically provides a `PORT` environment variable. The bot will automatically use it if available.

## Render Deployment Steps

### 1. Prepare Your Repository
- Make sure your code is in a Git repository (GitHub, GitLab, or Bitbucket)
- Ensure `Dockerfile`, `bot.py`, `pyproject.toml`, and `uv.lock` are committed

### 2. Create a New Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your repository
4. Select the repository containing your bot

### 3. Configure the Service

**Basic Settings:**
- **Name:** `pipecat-quickstart` (or your preferred name)
- **Region:** Choose closest to your users
- **Branch:** `main` (or your default branch)
- **Root Directory:** `pipecat/examples/quickstart` (if deploying from root of repo)

**Build & Deploy:**
- **Environment:** `Docker`
- **Dockerfile Path:** `pipecat/examples/quickstart/Dockerfile` (or just `Dockerfile` if root is quickstart)
- **Docker Context:** `pipecat/examples/quickstart` (or `.` if root is quickstart)

**Environment Variables:**
Add the three required API keys:
- `DEEPGRAM_API_KEY`
- `OPENAI_API_KEY`
- `CARTESIA_API_KEY`

**Advanced Settings:**
- **Port:** Leave empty (bot will use Render's PORT env var automatically)
- **Health Check Path:** `/` (optional)

### 4. Deploy

Click **"Create Web Service"** and Render will:
1. Build your Docker image
2. Deploy the container
3. Provide a public URL (e.g., `https://pipecat-quickstart.onrender.com`)

### 5. Access Your Bot

Once deployed, visit your Render URL:
```
https://your-service-name.onrender.com
```

The bot interface will be available at the root URL. Click "Connect" to start talking to your bot!

## What Was Modified

### bot.py Changes:
- Added automatic `PORT` environment variable detection for Render compatibility
- Bot will use Render's provided PORT if available, otherwise defaults to 7860

### Dockerfile:
- Already configured with `--host 0.0.0.0` for external access
- Port 7860 exposed (Render will override with PORT env var)

## Troubleshooting

### Bot not starting:
- Check Render logs: Go to your service → **Logs** tab
- Verify all three API keys are set correctly
- Ensure Dockerfile path is correct

### Connection issues:
- Make sure the service is running (not sleeping)
- Check that port is correctly exposed
- Verify HTTPS is working (Render provides this automatically)

### Audio not working:
- Check browser console for errors
- Ensure microphone permissions are granted
- Verify WebRTC is supported in your browser

## Render Free Tier Notes

- Services on the free tier **sleep after 15 minutes** of inactivity
- First request after sleep may take 30-60 seconds to wake up
- For production use, consider upgrading to a paid plan for always-on service

## Next Steps

- Customize `bot.py` to change the bot's personality
- Add more features to your voice AI bot
- Monitor usage in Render dashboard
- Set up custom domain (paid plans)

