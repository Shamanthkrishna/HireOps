# HireOps - Advanced Recruitment Management Platform

![HireOps](https://img.shields.io/badge/Status-Phase%201%20Complete-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

HireOps is a modern recruitment tracking system designed to streamline hiring workflows with Google OAuth authentication, visual pipelines, and enterprise-grade features.

## 🎯 Phase 1 - Complete ✅

**Current Features:**
- ✅ Modern landing page with feature showcase
- ✅ Google OAuth authentication (no email/password required)
- ✅ Basic dashboard with placeholders
- ✅ Responsive design (mobile-ready)
- ✅ User session management
- ✅ Professional UI/UX

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Cloud Console account (for OAuth credentials)
- Git

### 1. Clone the Repository

```powershell
git clone https://github.com/Shamanthkrishna/HireOps.git
cd HireOps
```

### 2. Set Up Virtual Environment

```powershell
# Create virtual environment
py -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Google OAuth

#### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Google+ API** and **Google Identity**

#### Step 2: Create OAuth 2.0 Credentials
1. Navigate to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth client ID**
3. Choose **Web application**
4. Add authorized redirect URIs:
   - `http://127.0.0.1:8000/auth/callback`
   - `http://localhost:8000/auth/callback`
5. Copy **Client ID** and **Client Secret**

#### Step 3: Configure Environment Variables
1. Copy `.env.example` to `.env`:
   ```powershell
   cp .env.example .env
   ```

2. Edit `.env` and add your Google OAuth credentials:
   ```env
   # Server Configuration
   HOST=127.0.0.1
   PORT=8000
   SECRET_KEY=your-random-secret-key-here-change-this
   
   # Google OAuth Configuration
   GOOGLE_CLIENT_ID=your-google-client-id-here
   GOOGLE_CLIENT_SECRET=your-google-client-secret-here
   GOOGLE_REDIRECT_URI=http://127.0.0.1:8000/auth/callback
   
   # Application Settings
   APP_NAME=HireOps
   ENVIRONMENT=development
   ```

### 5. Run the Application

```powershell
# Make sure virtual environment is activated
python main.py
```

Or using uvicorn directly:
```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 6. Access the Application

- **Landing Page**: http://127.0.0.1:8000
- **Sign in with Google** to access the dashboard
- **Dashboard**: http://127.0.0.1:8000/dashboard (requires authentication)

## 📁 Project Structure

```
HireOps/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create from .env.example)
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── Docs/                  # Documentation
│   ├── README.md
│   ├── Notes.txt
│   └── PROJECT_COMPLETION_SUMMARY.md
├── static/                # Static files
│   ├── css/
│   │   ├── style.css      # Landing page styles
│   │   └── dashboard.css  # Dashboard styles
│   └── js/
│       ├── main.js        # Landing page scripts
│       └── dashboard.js   # Dashboard scripts
└── templates/             # HTML templates
    ├── index.html         # Landing page
    └── dashboard.html     # Dashboard page
```

## 🔐 Authentication Flow

1. User clicks "Sign in with Google" on landing page
2. Redirected to Google OAuth consent screen
3. After authorization, redirected back to `/auth/callback`
4. User session created with email, name, and profile picture
5. Redirected to dashboard
6. Session persists until logout

## 🎨 Features Overview

### Landing Page
- **Hero Section**: Eye-catching gradient background with CTA
- **Features Grid**: 6 feature cards with icons
- **About Section**: Technology stack showcase
- **Responsive Design**: Mobile, tablet, and desktop optimized

### Dashboard
- **User Profile**: Display Google profile picture and name
- **Stats Cards**: 4 metric cards with placeholder data
- **Sidebar Navigation**: 7 navigation items
- **Quick Actions**: 4 action buttons
- **Placeholders**: Ready for Phase 2 implementations

## 🛠️ Technology Stack

### Backend
- **FastAPI 0.104.1**: Modern Python web framework
- **Authlib 1.2.1**: OAuth client library
- **Uvicorn**: ASGI server
- **Starlette**: Session middleware
- **python-dotenv**: Environment management

### Frontend
- **HTML5 & CSS3**: Modern web standards
- **Vanilla JavaScript (ES6+)**: No frameworks
- **Font Awesome 6.4.0**: Icon library
- **Google Fonts (Inter)**: Typography
- **Responsive Design**: CSS Grid & Flexbox

## 📝 API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Landing page | No |
| GET | `/dashboard` | Dashboard page | Yes |
| GET | `/auth/login` | Initiate Google OAuth | No |
| GET | `/auth/callback` | OAuth callback | No |
| GET | `/auth/logout` | Logout user | No |
| GET | `/api/user` | Get current user info | Yes |

## 🚧 Coming in Phase 2

- Job posting management (CRUD)
- Candidate profile management
- Application tracking system
- Database integration (SQLAlchemy)
- Advanced pipeline visualization
- Real-time collaboration features

## 🐛 Troubleshooting

### Issue: "No module named 'authlib'"
**Solution**: Make sure virtual environment is activated and dependencies are installed:
```powershell
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: OAuth authentication fails
**Solution**: 
1. Verify Google OAuth credentials in `.env`
2. Check redirect URI matches in Google Console
3. Ensure Google+ API is enabled

### Issue: "Address already in use"
**Solution**: Change port in `.env` or kill process using port 8000:
```powershell
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

## 🤝 Contributing

This is a learning/portfolio project. Feel free to fork and experiment!

## 📄 License

MIT License - feel free to use this project for learning or as a template.

## 👤 Author

**Shamanth Krishna**
- GitHub: [@Shamanthkrishna](https://github.com/Shamanthkrishna)
- Project: [HireOps](https://github.com/Shamanthkrishna/HireOps)

## 🙏 Acknowledgments

- FastAPI documentation and community
- Google OAuth integration guides
- Modern UI/UX design principles

---

**Note**: This is Phase 1 of the HireOps project. Full recruitment management features will be implemented in subsequent phases. See `Docs/` folder for detailed project roadmap.
