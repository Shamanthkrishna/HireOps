from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
import os
import json

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.environ.get("SESSION_SECRET_KEY", "supersecretkey1234567890abcdef!@#$%^&*()"))
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# Path to your credentials file
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "client_secret.json")

with open(CREDENTIALS_FILE, "r") as f:
    creds = json.load(f)["web"]  # or ["installed"] if you chose "Desktop app" type

GOOGLE_CLIENT_ID = creds["client_id"]
GOOGLE_CLIENT_SECRET = creds["client_secret"]

from authlib.integrations.starlette_client import OAuth

# Set up OAuth
oauth = OAuth()
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

from fastapi.responses import RedirectResponse

@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth')  # This creates the redirect URI for /auth
    print("Redirect URI:", redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get("/auth")
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    print("Token received from Google:", token)  # Debug print
    user = token.get("userinfo")
    if not user:
        # fallback to userinfo endpoint
        resp = await oauth.google.get('userinfo', token=token)
        user = resp.json()
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})