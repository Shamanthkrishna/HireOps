from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="HireOps", version="1.0.0")

# Add session middleware with production-ready settings
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "your-secret-key-change-this"),
    session_cookie="hireops_session",
    max_age=14 * 24 * 60 * 60,  # 14 days
    same_site="lax",
    https_only=os.getenv("ENVIRONMENT", "development") == "production"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Configure OAuth
oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Helper function to get current user
def get_current_user(request: Request):
    user = request.session.get('user')
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

# Routes
@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    """Landing page"""
    user = request.session.get('user')
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "user": user}
    )

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard page - requires authentication"""
    user = request.session.get('user')
    if not user:
        return RedirectResponse(url='/')
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user}
    )

@app.get("/auth/login")
async def login(request: Request):
    """Initiate Google OAuth login"""
    # Always use the actual request URL to construct redirect_uri
    # This ensures it works in both local dev and production
    redirect_uri = f"{request.url.scheme}://{request.url.netloc}/auth/callback"
    
    # Detailed debug logging
    print("=" * 50)
    print(f"Login initiated from: {request.url}")
    print(f"Scheme: {request.url.scheme}")
    print(f"Netloc: {request.url.netloc}")
    print(f"Constructed redirect_uri: {redirect_uri}")
    print("=" * 50)
    
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/callback")
async def auth_callback(request: Request):
    """Google OAuth callback"""
    try:
        # Get the token from Google
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        
        if user_info:
            # Store user info in session
            request.session['user'] = {
                'email': user_info.get('email'),
                'name': user_info.get('name'),
                'picture': user_info.get('picture')
            }
            print(f"User logged in: {user_info.get('email')}")  # Debug log
            return RedirectResponse(url='/dashboard', status_code=303)
        else:
            print("No user info received from Google")
            return RedirectResponse(url='/?error=no_user_info', status_code=303)
            
    except Exception as e:
        print(f"Auth error: {e}")
        import traceback
        traceback.print_exc()
        return RedirectResponse(url=f'/?error=auth_failed&detail={str(e)}', status_code=303)

@app.get("/auth/logout")
async def logout(request: Request):
    """Logout user"""
    request.session.clear()
    return RedirectResponse(url='/', status_code=303)

@app.get("/api/user")
async def get_user(user: dict = Depends(get_current_user)):
    """Get current user info"""
    return user

@app.get("/api/debug/session")
async def debug_session(request: Request):
    """Debug endpoint to check session"""
    return {
        "has_session": bool(request.session),
        "session_data": dict(request.session) if request.session else {},
        "has_user": 'user' in request.session
    }

@app.get("/api/debug/oauth")
async def debug_oauth(request: Request):
    """Debug OAuth configuration"""
    redirect_uri = f"{request.url.scheme}://{request.url.netloc}/auth/callback"
    return {
        "current_url": str(request.url),
        "scheme": request.url.scheme,
        "netloc": request.url.netloc,
        "constructed_redirect_uri": redirect_uri,
        "google_client_id": os.getenv('GOOGLE_CLIENT_ID')[:10] + "..." if os.getenv('GOOGLE_CLIENT_ID') else None,
        "env_redirect_uri": os.getenv('GOOGLE_REDIRECT_URI'),
        "message": "The 'constructed_redirect_uri' above is what will be sent to Google. Make sure this EXACTLY matches what's in Google Cloud Console."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
