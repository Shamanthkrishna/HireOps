from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.environ.get("SESSION_SECRET_KEY", "supersecretkey1234567890abcdef!@#$%^&*()"))
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup_event():
    logger.info("=== HireOps Application Starting ===")
    logger.info(f"Application started at {datetime.now()}")
    logger.info("FastAPI server is ready to handle requests")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("=== HireOps Application Shutting Down ===")
    logger.info(f"Application stopped at {datetime.now()}")

# Error handling middleware
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    user_ip = request.client.host if request.client else 'Unknown'
    logger.error(f"[SYSTEM_ERROR] Global exception from IP: {user_ip} - Path: {request.url.path} - Method: {request.method} - Error: {str(exc)}")
    return templates.TemplateResponse("home.html", {
        "request": request,
        "error": "An unexpected error occurred. Please try again."
    })

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user_ip = request.client.host if request.client else 'Unknown'
    logger.info(f"[ANONYMOUS] Home page accessed from IP: {user_ip}")
    return templates.TemplateResponse("home.html", {"request": request})


GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

from authlib.integrations.starlette_client import OAuth

# Set up OAuth
oauth = OAuth()
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)
logger.info("OAuth client registered successfully")

from fastapi.responses import RedirectResponse

@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth')  # This creates the redirect URI for /auth
    user_ip = request.client.host if request.client else 'Unknown'
    logger.info(f"[ANONYMOUS] Google OAuth login initiated from IP: {user_ip} - Redirect URI: {redirect_uri}")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get("/auth")
async def auth(request: Request):
    try:
        user_ip = request.client.host if request.client else 'Unknown'
        logger.info(f"[AUTH_PROCESS] Google OAuth callback received from IP: {user_ip}")
        
        token = await oauth.google.authorize_access_token(request)
        logger.info("[AUTH_PROCESS] Access token successfully received from Google")
        
        user = token.get("userinfo")
        if not user:
            logger.info("[AUTH_PROCESS] No userinfo in token, fetching from userinfo endpoint")
            resp = await oauth.google.get('userinfo', token=token)
            user = resp.json()
        
        user_email = user.get('email', 'No email')
        user_name = user.get('name', 'No name')
        user_id = user.get('sub', 'No ID')
        
        logger.info(f"[USER: {user_email}] Authentication successful - Name: {user_name} - ID: {user_id} - IP: {user_ip}")
        
        # Log detailed user information for admin debugging
        logger.info(f"[USER: {user_email}] User details - Given Name: {user.get('given_name', 'N/A')} - Family Name: {user.get('family_name', 'N/A')} - Email Verified: {user.get('email_verified', 'N/A')}")
        
        # Log dashboard access
        logger.info(f"[USER: {user_email}] Dashboard accessed from IP: {user_ip}")
        
        return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})
        
    except Exception as e:
        user_ip = request.client.host if request.client else 'Unknown'
        logger.error(f"[AUTH_ERROR] Authentication failed from IP: {user_ip} - Error: {str(e)} - Type: {type(e).__name__}")
        return templates.TemplateResponse("home.html", {
            "request": request, 
            "error": f"Authentication failed: {str(e)}"
        })