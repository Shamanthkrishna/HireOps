# 🎯 HireOps Phase 1 - Quick Reference

## ⚡ Quick Start (3 Steps)

```powershell
# 1. Setup & Install
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure .env (copy from .env.example and add Google OAuth credentials)
Copy-Item .env.example .env
# Edit .env with your Google Client ID and Secret

# 3. Run
python main.py
```

**Access**: http://127.0.0.1:8000

---

## 🔑 Google OAuth Setup (5 Minutes)

1. **Console**: https://console.cloud.google.com/
2. **Create** OAuth 2.0 Client ID
3. **Add Redirect**: `http://127.0.0.1:8000/auth/callback`
4. **Copy** Client ID + Secret → `.env`
5. **Run** app and test!

---

## 📂 Project Structure

```
HireOps/
├── main.py              # FastAPI app
├── requirements.txt     # Dependencies
├── .env                 # Your config (create from .env.example)
├── static/
│   ├── css/            # Styles
│   └── js/             # Scripts
└── templates/          # HTML pages
```

---

## 🌐 Endpoints

| URL | Description | Auth |
|-----|-------------|------|
| `/` | Landing page | No |
| `/dashboard` | Dashboard | Yes |
| `/auth/login` | Google OAuth | No |
| `/auth/logout` | Logout | No |
| `/api/user` | User info | Yes |

---

## 🚀 Git Commands

```powershell
# View status
git status

# Push to GitHub
git push -u origin main

# View commits
git log --oneline

# Pull updates
git pull origin main
```

**Repository**: https://github.com/Shamanthkrishna/HireOps.git

---

## ✅ Phase 1 Features

- ✅ Landing page with Google Sign-In
- ✅ Google OAuth (no passwords)
- ✅ Protected dashboard
- ✅ User profile display
- ✅ Responsive design
- ✅ Session management

---

## 🛠️ Common Commands

```powershell
# Activate venv
venv\Scripts\activate

# Install new package
pip install package-name
pip freeze > requirements.txt

# Run with auto-reload
uvicorn main:app --reload

# Check port usage
netstat -ano | findstr :8000
```

---

## 📖 Documentation Files

- **GETTING_STARTED.md** - Detailed setup guide
- **README.md** - Project overview
- **PHASE1_COMPLETE.md** - Phase 1 summary
- **.env.example** - Configuration template

---

## 🎯 Next: Phase 2

- Database (SQLAlchemy + SQLite)
- Job Management CRUD
- Candidate Management
- Application Tracking
- Real Pipeline

---

**Status**: Phase 1 Complete ✅  
**Author**: Shamanth Krishna  
**Ready for**: Development & Testing 🚀
