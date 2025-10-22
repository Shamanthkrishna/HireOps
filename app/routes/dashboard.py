from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from app.database import get_session
from app.auth import get_current_user_from_session
from app.crud import get_dashboard_stats
from app.models import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def dashboard(
    request: Request, 
    current_user: User = Depends(get_current_user_from_session),
    session: Session = Depends(get_session)
):
    """Main dashboard page"""
    # Get dashboard statistics based on user role
    stats = get_dashboard_stats(session, current_user.role, current_user.id)
    
    return templates.TemplateResponse("dashboard/dashboard.html", {
        "request": request,
        "user": current_user,
        "stats": stats
    })
