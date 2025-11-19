# Deployment Guide - Free Hosting Options

## 🚀 Option 1: Render (RECOMMENDED - Easiest)

**Why Render?**
- ✅ Completely FREE tier
- ✅ Automatic deployments from GitHub
- ✅ Easy environment variables setup
- ✅ Free SSL certificate (HTTPS)
- ✅ No credit card required

### Step-by-Step Render Deployment

#### 1. Push to GitHub (Already Done ✅)
Your code is already on GitHub: https://github.com/Shamanthkrishna/HireOps

#### 2. Sign Up for Render
1. Go to https://render.com/
2. Click **"Get Started for Free"**
3. Sign up with your **GitHub account**

#### 3. Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub account (if not already)
3. Select repository: **HireOps**
4. Click **"Connect"**

#### 4. Configure the Service
Fill in these settings:

- **Name**: `hireops` (or any name you want)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: Leave blank
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Plan**: **Free** (select this!)

#### 5. Add Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**

Add these one by one:

```
SECRET_KEY = any-random-secret-key-here-abc123xyz
GOOGLE_CLIENT_ID = your-google-client-id
GOOGLE_CLIENT_SECRET = your-google-client-secret
GOOGLE_REDIRECT_URI = https://your-app-name.onrender.com/auth/callback
HOST = 0.0.0.0
APP_NAME = HireOps
ENVIRONMENT = production
```

**IMPORTANT**: For `GOOGLE_REDIRECT_URI`, you'll need to:
- First deploy to get your Render URL (like `hireops.onrender.com`)
- Then update this variable with the actual URL
- Also update it in Google Cloud Console

#### 6. Deploy
1. Click **"Create Web Service"**
2. Wait 2-5 minutes for deployment
3. Your app will be live at: `https://your-app-name.onrender.com`

#### 7. Update Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to your OAuth credentials
3. Add authorized redirect URI:
   - `https://your-app-name.onrender.com/auth/callback`
4. Update the `GOOGLE_REDIRECT_URI` environment variable in Render

### 🔄 Auto-Deploy
Every time you push to GitHub, Render will automatically redeploy! 🎉

---

## 🚀 Option 2: Railway

**Why Railway?**
- ✅ $5 free credit per month
- ✅ Very simple setup
- ✅ Great for small apps

### Railway Deployment Steps

1. **Sign Up**: https://railway.app/
2. **New Project** → **"Deploy from GitHub repo"**
3. **Select**: HireOps repository
4. **Add Variables**: Same as Render (in Variables tab)
5. **Generate Domain**: Click "Generate Domain" for public URL
6. **Update Google OAuth**: Add Railway URL to allowed redirects

---

## 🚀 Option 3: Fly.io

**Why Fly.io?**
- ✅ Free tier for small apps
- ✅ Global deployment
- ✅ Good performance

### Fly.io Deployment

```powershell
# Install Fly CLI
iwr https://fly.io/install.ps1 -useb | iex

# Login
fly auth login

# Deploy
fly launch --name hireops

# Set environment variables
fly secrets set SECRET_KEY=your-secret-key
fly secrets set GOOGLE_CLIENT_ID=your-client-id
fly secrets set GOOGLE_CLIENT_SECRET=your-client-secret
fly secrets set GOOGLE_REDIRECT_URI=https://hireops.fly.dev/auth/callback

# Deploy
fly deploy
```

---

## 📱 Share with Your Client

After deploying on Render (recommended), share:

**Live URL**: `https://hireops.onrender.com` (or your custom name)

Your client can:
1. Visit the URL
2. Click "Sign in with Google"
3. Use the application immediately
4. No installation needed!

---

## ⚠️ Important Notes

### Free Tier Limitations

**Render Free Tier:**
- ✅ Unlimited bandwidth
- ⚠️ App sleeps after 15 min of inactivity
- ⚠️ Cold start takes 30-60 seconds on first visit
- ✅ Enough for demo/testing

**Solution for Sleeping**: 
- Use a free uptime monitor like [UptimeRobot](https://uptimerobot.com/) to ping your app every 5 minutes
- This keeps it awake during demo hours

### Google OAuth Setup for Production

You need to update Google Cloud Console:

1. Go to: https://console.cloud.google.com/apis/credentials
2. Edit your OAuth Client ID
3. Add **Authorized redirect URIs**:
   ```
   https://your-app-name.onrender.com/auth/callback
   ```
4. Add **Authorized JavaScript origins**:
   ```
   https://your-app-name.onrender.com
   ```

---

## 🎯 Recommended Setup for Client Demo

**Best Choice**: **Render** (no credit card, always free)

**Steps Summary**:
1. ✅ Push to GitHub (Done!)
2. ✅ Sign up Render with GitHub
3. ✅ Create Web Service from HireOps repo
4. ✅ Add environment variables
5. ✅ Deploy (takes 3-5 minutes)
6. ✅ Update Google OAuth redirect
7. ✅ Share URL with client

**Total Time**: 10-15 minutes

---

## 🔧 Troubleshooting Deployment

### Issue: "Application Error"
- Check Render logs (click "Logs" tab)
- Verify all environment variables are set
- Ensure `PORT` is using `$PORT` variable

### Issue: OAuth Redirect Error
- Verify redirect URI in Google Console matches exactly
- Check `GOOGLE_REDIRECT_URI` environment variable
- Must use `https://` not `http://`

### Issue: App is Slow
- Free tier apps sleep after inactivity
- First request takes 30-60 seconds
- Subsequent requests are fast
- Use UptimeRobot to keep awake

---

## 📊 Monitoring Your Deployed App

**Render Dashboard**:
- View logs in real-time
- Monitor CPU/Memory usage
- See deploy history
- Check environment variables

**Free Monitoring Tools**:
- [UptimeRobot](https://uptimerobot.com/) - Uptime monitoring
- [StatusCake](https://www.statuscake.com/) - Alternative monitoring

---

## 💡 Tips for Client Demo

1. **Keep App Awake**: Set up UptimeRobot before demo
2. **Test Before Demo**: Visit URL 1-2 minutes before showing client
3. **Prepare Test Account**: Have a Google account ready for demo
4. **Share URL Early**: Send URL to client before meeting

---

## 🎉 Next Steps

1. Deploy to Render (recommended)
2. Get your live URL
3. Update Google OAuth settings
4. Test the deployment
5. Share with your client!

**Your app will be live and accessible worldwide!** 🌍
