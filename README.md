# HireOps - Recruitment Management Portal

A modern recruitment management portal built with FastAPI and Google OAuth authentication. This application provides a secure, professional interface for managing hiring processes with Google account integration.

## 🚀 Features

- **Google OAuth Authentication**: Secure login using Google accounts
- **Modern Dark Mode UI**: Professional, responsive design with blue accent colors
- **FastAPI Backend**: High-performance Python web framework
- **Session Management**: Secure session handling with middleware
- **Domain Restriction**: Optional email domain filtering for access control
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Authentication**: Google OAuth 2.0 with Authlib
- **Frontend**: HTML, CSS, Jinja2 Templates
- **Styling**: Custom CSS with Google Fonts (Roboto)
- **Server**: Uvicorn ASGI server

## 📋 Prerequisites

- Python 3.8+
- Google Cloud Platform account
- Git

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Shamanthkrishna/HireOps.git
cd HireOps
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Google OAuth Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API
4. Go to **APIs & Services > Credentials**
5. Click **Create Credentials > OAuth client ID**
6. Choose **Web application**
7. Set **Authorized redirect URIs** to:
   ```
   http://localhost:8000/auth
   http://127.0.0.1:8000/auth
   ```
8. Download the credentials JSON file
9. Rename it to `client_secret.json` and place it in the project root

### 4. Configure Credentials

The application will automatically load credentials from `client_secret.json`. Make sure this file is in your project root directory.

**⚠️ Security Note**: Never commit `client_secret.json` to version control. It's already included in `.gitignore`.

## 🚀 Running the Application

### Development Mode

```bash
uvicorn main:app --reload
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Access the Application

Open your browser and navigate to:
- **Homepage**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
HireOps/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── client_secret.json      # Google OAuth credentials (not in git)
├── templates/
│   ├── home.html          # Landing page with login
│   └── profile.html       # User profile page
└── README.md              # This file
```

## 🔐 Authentication Flow

1. User visits the homepage
2. Clicks "Login with Google"
3. Redirected to Google OAuth consent screen
4. After authentication, redirected back to `/auth`
5. User profile information is displayed
6. User can logout to return to homepage

## 🎨 Customization

### Domain Restriction

To restrict access to specific email domains, modify the `/auth` route in `main.py`:

```python
allowed_domain = "yourcompany.com"
user_email = user.get("email", "")
if not user_email.endswith(f"@{allowed_domain}"):
    return templates.TemplateResponse("home.html", {
        "request": request,
        "error": f"Access denied: only {allowed_domain} emails are allowed."
    })
```

### Styling

The application uses a dark theme with blue accents. You can customize the colors by modifying the CSS in the HTML templates.

## 🔒 Security Features

- OAuth 2.0 authentication flow
- Session middleware for secure session handling
- Credentials stored locally (not in version control)
- HTTPS redirect URIs for production

## 🚀 Deployment

### Environment Variables

For production deployment, set these environment variables:

```bash
export SESSION_SECRET_KEY="your-secure-secret-key"
export GOOGLE_CLIENT_ID="your-client-id"
export GOOGLE_CLIENT_SECRET="your-client-secret"
```

### Production Considerations

- Use HTTPS in production
- Set up proper session storage (Redis, database)
- Configure proper CORS settings
- Use environment variables for sensitive data
- Set up logging and monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Shamanth Krishna**
- GitHub: [@Shamanthkrishna](https://github.com/Shamanthkrishna)

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Google OAuth for secure authentication
- Authlib for OAuth integration
- The open-source community for inspiration and tools

---

**Note**: This is a demo project for learning Google OAuth integration with FastAPI. For production use, ensure proper security measures and follow best practices. 