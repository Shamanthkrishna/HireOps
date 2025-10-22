from fastapi import APIRouter, Request, Depends, HTTPException, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel import Session
from app.database import get_session
from app.auth import authenticate_user, create_access_token
from app.crud import get_user_by_username, create_user
from app.models import UserRole
from datetime import timedelta

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login")
async def login_page(request: Request):
    """Display login page"""
    return templates.TemplateResponse("auth/login.html", {"request": request})

@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    """Handle login form submission"""
    user = authenticate_user(session, username, password)
    if not user:
        return templates.TemplateResponse(
            "auth/login.html", 
            {"request": request, "error": "Invalid username or password"}
        )
    
    # Set session
    request.session["user_id"] = user.id
    request.session["username"] = user.username
    request.session["role"] = user.role
    
    return RedirectResponse(url="/dashboard", status_code=302)

@router.get("/logout")
async def logout(request: Request):
    """Handle logout"""
    request.session.clear()
    return RedirectResponse(url="/auth/login", status_code=302)

@router.get("/register")
async def register_page(request: Request):
    """Display registration page"""
    return templates.TemplateResponse("auth/register.html", {
        "request": request,
        "roles": [role.value for role in UserRole]
    })

@router.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    session: Session = Depends(get_session)
):
    """Handle registration form submission"""
    # Check if user already exists
    if get_user_by_username(session, username):
        return templates.TemplateResponse(
            "auth/register.html", 
            {
                "request": request, 
                "error": "Username already exists",
                "roles": [role.value for role in UserRole]
            }
        )
    
    try:
        # Create user
        user_data = {
            "username": username,
            "email": email,
            "full_name": full_name,
            "password": password,
            "role": role
        }
        user = create_user(session, user_data)
        
        # Auto-login after registration
        request.session["user_id"] = user.id
        request.session["username"] = user.username
        request.session["role"] = user.role
        
        return RedirectResponse(url="/dashboard", status_code=302)
    
    except Exception as e:
        return templates.TemplateResponse(
            "auth/register.html", 
            {
                "request": request, 
                "error": f"Registration failed: {str(e)}",
                "roles": [role.value for role in UserRole]
            }
        )
