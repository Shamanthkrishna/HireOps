from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse
import os

# Import database and models
try:
    from sqlmodel import Session
    from app.database import create_db_and_tables, get_session
    from app.auth import get_current_user_from_session
    from app.models import User
    SQLMODEL_AVAILABLE = True
except ImportError:
    print("⚠️  SQLModel not available, running in basic mode")
    SQLMODEL_AVAILABLE = False

# Import routes
try:
    from app.routes import auth, dashboard, requirements, candidates, admin
    ROUTES_AVAILABLE = True
except ImportError:
    print("⚠️  Routes not available, running in basic mode")
    ROUTES_AVAILABLE = False

# Create FastAPI app
app = FastAPI(title="HireOps - Recruitment Tracking System", version="1.0.0")

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "your-secret-key"))

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include routers if available
if ROUTES_AVAILABLE:
    app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
    app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
    app.include_router(requirements.router, prefix="/requirements", tags=["Requirements"])
    app.include_router(candidates.router, prefix="/candidates", tags=["Candidates"])
    app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.on_event("startup")
def on_startup():
    """Initialize database on startup"""
    if SQLMODEL_AVAILABLE:
        create_db_and_tables()

@app.get("/")
async def root(request: Request):
    """Root endpoint - redirect to dashboard if authenticated, else to login"""
    if ROUTES_AVAILABLE and SQLMODEL_AVAILABLE:
        try:
            from app.database import get_session
            session = next(get_session())
            user = get_current_user_from_session(request, session)
            return RedirectResponse(url="/dashboard", status_code=302)
        except:
            return RedirectResponse(url="/auth/login", status_code=302)
    else:
        return {"message": "HireOps - Setup in progress", "status": "Please install dependencies"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )
