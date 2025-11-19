# 🚀 Deploy HireOps in 5 Minutes (FREE)

## Easiest Way: Render.com (No Credit Card Required)

### Step 1: Go to Render
👉 Visit: **https://render.com/**
- Click **"Get Started for Free"**
- Sign up with your **GitHub account**

### Step 2: Create Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Connect account"** if needed
4. Find and select: **HireOps** repository
5. Click **"Connect"**

### Step 3: Configure Settings

**Basic Info:**
- **Name**: `hireops` (or choose your own)
- **Region**: Pick closest to you
- **Branch**: `main`
- **Runtime**: `Python 3`

**Build & Start:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Plan:**
- Select **"Free"** tier ✅

### Step 4: Add Environment Variables

Click **"Advanced"** → Scroll to **"Environment Variables"**

Click **"Add Environment Variable"** and add these:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | `your-random-secret-key-change-this-abc123` |
| `GOOGLE_CLIENT_ID` | Your Google Client ID |
| `GOOGLE_CLIENT_SECRET` | Your Google Client Secret |
| `GOOGLE_REDIRECT_URI` | `https://hireops.onrender.com/auth/callback` |
| `HOST` | `0.0.0.0` |
| `APP_NAME` | `HireOps` |
| `ENVIRONMENT` | `production` |

**NOTE**: Replace `hireops` in the redirect URI with your actual app name if different.

### Step 5: Deploy!
1. Click **"Create Web Service"**
2. Wait 2-5 minutes (watch the logs)
3. You'll get a URL like: `https://hireops.onrender.com`

### Step 6: Update Google OAuth

⚠️ **IMPORTANT** - Go to Google Cloud Console:

1. Visit: https://console.cloud.google.com/apis/credentials
2. Click on your OAuth 2.0 Client ID
3. Under **"Authorized redirect URIs"**, click **"Add URI"**
4. Add: `https://your-app-name.onrender.com/auth/callback`
5. Under **"Authorized JavaScript origins"**, add: `https://your-app-name.onrender.com`
6. Click **"Save"**

### Step 7: Test Your App! 🎉

1. Visit your Render URL: `https://your-app-name.onrender.com`
2. Click **"Sign in with Google"**
3. It works! 🚀

---

## 📱 Share with Your Client

Send them the link:
```
https://your-app-name.onrender.com
```

They can:
- ✅ Visit the link from any device
- ✅ Sign in with their Google account
- ✅ Use the full application
- ✅ No installation needed!

---

## ⚡ Quick Tips

### Free Tier Note
- App sleeps after 15 minutes of inactivity
- First visit after sleep takes 30-60 seconds to wake up
- After that, it's fast!

### Keep It Awake (Optional)
Use **UptimeRobot** (free):
1. Go to: https://uptimerobot.com/
2. Sign up free
3. Add your Render URL
4. It will ping every 5 minutes
5. Keeps app awake during business hours

### Automatic Updates
- Every time you `git push` to GitHub
- Render automatically redeploys! 🔄
- Takes 2-3 minutes

---

## 🐛 Troubleshooting

### "Application Error"
- Check logs in Render dashboard
- Verify all environment variables are set
- Make sure Google OAuth is configured

### "Redirect URI Mismatch"
- Double-check Google Cloud Console redirect URIs
- Must match exactly: `https://your-app.onrender.com/auth/callback`
- No trailing slash!

### "App is Slow"
- Normal for free tier on first visit
- App is waking up from sleep
- Will be fast after initial load

---

## ✅ Deployment Checklist

- [ ] Signed up for Render
- [ ] Created Web Service from GitHub
- [ ] Added all environment variables
- [ ] Deployed successfully
- [ ] Updated Google OAuth redirect URIs
- [ ] Tested sign-in with Google
- [ ] Shared URL with client

---

## 🎯 You're Done!

Your app is now:
- ✅ Live on the internet
- ✅ Accessible worldwide
- ✅ Free forever
- ✅ Auto-deploys from GitHub
- ✅ Has SSL/HTTPS

**Total Cost**: $0.00 💰

Share the URL with your client and impress them! 🌟
