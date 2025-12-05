# Complete Step-by-Step Guide: Deploy Pipecat Bot to Render

## 📋 Prerequisites Checklist

Before starting, make sure you have:

- [ ] **GitHub/GitLab/Bitbucket account** (free)
- [ ] **Render account** (free tier available) - [Sign up here](https://dashboard.render.com/)
- [ ] **Deepgram API key** - [Get it here](https://console.deepgram.com/signup)
- [ ] **OpenAI API key** - [Get it here](https://auth.openai.com/create-account)
- [ ] **Cartesia API key** - [Get it here](https://play.cartesia.ai/sign-up)

---

## Step 1: Prepare Your Code Repository

### 1.1 Push Your Code to GitHub

1. **If you haven't already, initialize git in your project:**
   ```bash
   cd /Volumes/Biswarup_Harddisk/new_pipecat_deployment_ready/pipecat
   git init
   git add .
   git commit -m "Initial commit: Pipecat quickstart bot"
   ```

2. **Create a new repository on GitHub:**
   - Go to [GitHub.com](https://github.com)
   - Click the **"+"** icon → **"New repository"**
   - Name it: `pipecat-bot` (or any name you like)
   - Make it **Public** or **Private** (your choice)
   - **Don't** initialize with README, .gitignore, or license
   - Click **"Create repository"**

3. **Push your code to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/pipecat-bot.git
   git branch -M main
   git push -u origin main
   ```
   *(Replace `YOUR_USERNAME` with your GitHub username)*

---

## Step 2: Sign Up / Log In to Render

1. **Go to Render Dashboard:**
   - Visit: [https://dashboard.render.com/](https://dashboard.render.com/)

2. **Sign up or log in:**
   - If new: Click **"Get Started for Free"**
   - Sign up with GitHub (recommended) or email
   - Verify your email if required

---

## Step 3: Create a New Web Service

1. **In Render Dashboard:**
   - Click the **"New +"** button (top right)
   - Select **"Web Service"**

2. **Connect Your Repository:**
   - If using GitHub: Click **"Connect GitHub"** or **"Connect account"**
   - Authorize Render to access your repositories
   - Search for your repository: `pipecat-bot` (or whatever you named it)
   - Click **"Connect"** next to your repository

---

## Step 4: Configure Your Service

### 4.1 Basic Settings

Fill in these fields:

- **Name:** `pipecat-quickstart` (or any name you prefer)
- **Region:** Choose the closest region to your users (e.g., `Oregon (US West)`)
- **Branch:** `main` (or your default branch name)
- **Root Directory:** `examples/quickstart` ⚠️ **IMPORTANT!**

### 4.2 Build & Deploy Settings

- **Environment:** Select **"Docker"** from the dropdown
- **Dockerfile Path:** Leave blank (Render will auto-detect it in the root directory)
- **Docker Context:** Leave as default (`.`)

### 4.3 Environment Variables

Click **"Add Environment Variable"** and add these **three** variables:

1. **First Variable:**
   - **Key:** `DEEPGRAM_API_KEY`
   - **Value:** `your_actual_deepgram_api_key_here`
   - Click **"Add"**

2. **Second Variable:**
   - **Key:** `OPENAI_API_KEY`
   - **Value:** `your_actual_openai_api_key_here`
   - Click **"Add"**

3. **Third Variable:**
   - **Key:** `CARTESIA_API_KEY`
   - **Value:** `your_actual_cartesia_api_key_here`
   - Click **"Add"**

### 4.4 Advanced Settings (Optional)

- **Port:** Leave empty (bot will auto-detect Render's PORT)
- **Health Check Path:** `/` (optional, but recommended)
- **Auto-Deploy:** `Yes` (deploys automatically on git push)

---

## Step 5: Deploy!

1. **Review your settings:**
   - Double-check the Root Directory is `examples/quickstart`
   - Verify all 3 environment variables are added
   - Make sure Environment is set to "Docker"

2. **Click "Create Web Service"**

3. **Watch the build:**
   - Render will start building your Docker image
   - This takes 5-10 minutes the first time
   - You'll see build logs in real-time
   - Wait for "Your service is live" message

---

## Step 6: Access Your Bot

1. **Get your URL:**
   - Once deployed, Render will show your service URL
   - Format: `https://pipecat-quickstart.onrender.com`
   - (Your actual URL will be different)

2. **Open in browser:**
   - Click the URL or copy-paste it into your browser
   - You should see the Pipecat bot interface

3. **Test your bot:**
   - Click the **"Connect"** button
   - Allow microphone access when prompted
   - Start talking to your bot! 🎉

---

## Step 7: Monitor & Troubleshoot

### View Logs

1. In Render dashboard, click on your service
2. Go to **"Logs"** tab
3. Check for any errors or warnings

### Common Issues & Fixes

**❌ Build Failed:**
- Check logs for error messages
- Verify Root Directory is `examples/quickstart`
- Ensure all files (Dockerfile, bot.py, pyproject.toml, uv.lock) are committed

**❌ Service Crashes:**
- Check environment variables are set correctly
- Verify API keys are valid (not expired)
- Check logs for specific error messages

**❌ Bot Not Responding:**
- Wait 30-60 seconds if service was sleeping (free tier)
- Check browser console for errors (F12 → Console)
- Verify microphone permissions are granted

**❌ Can't Connect:**
- Make sure service is "Live" (not "Sleeping")
- Check that HTTPS is working (Render provides this automatically)
- Try a different browser

---

## Step 8: Update Your Bot (Future Changes)

When you make changes to your code:

1. **Commit and push to GitHub:**
   ```bash
   git add .
   git commit -m "Update bot"
   git push
   ```

2. **Render will automatically:**
   - Detect the push
   - Rebuild your service
   - Deploy the new version

3. **Or manually trigger:**
   - Go to Render dashboard → Your service
   - Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## 📝 Quick Reference

### Your Render Settings Summary:
```
Name: pipecat-quickstart
Root Directory: examples/quickstart
Environment: Docker
Environment Variables:
  - DEEPGRAM_API_KEY
  - OPENAI_API_KEY
  - CARTESIA_API_KEY
```

### Your Service URL:
```
https://your-service-name.onrender.com
```

---

## 🎯 Success Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Web service created
- [ ] Root Directory set to `examples/quickstart`
- [ ] All 3 environment variables added
- [ ] Service deployed successfully
- [ ] Bot accessible via URL
- [ ] Can connect and talk to bot

---

## 💡 Pro Tips

1. **Free Tier Limitations:**
   - Services sleep after 15 minutes of inactivity
   - First request after sleep takes 30-60 seconds
   - Consider paid plan for production use

2. **Custom Domain:**
   - Available on paid plans
   - Go to Settings → Custom Domains

3. **Monitoring:**
   - Check logs regularly
   - Monitor API usage in Deepgram/OpenAI/Cartesia dashboards
   - Set up alerts for errors

4. **Scaling:**
   - Free tier: 1 instance
   - Paid plans: Auto-scaling available

---

## 🆘 Need Help?

- **Render Docs:** [https://render.com/docs](https://render.com/docs)
- **Render Support:** [https://render.com/support](https://render.com/support)
- **Pipecat Docs:** [https://docs.pipecat.ai/](https://docs.pipecat.ai/)

---

**You're all set! 🚀 Your voice AI bot is now live on Render!**

