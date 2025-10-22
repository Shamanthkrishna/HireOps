from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel import Session
from app.database import get_session
from app.auth import require_admin
from app.crud import get_users, create_user, get_user, get_clients, create_client
from app.models import User, UserRole

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/users")
async def list_users(
    request: Request,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    """List all users (admin only)"""
    users = get_users(session)
    return templates.TemplateResponse("admin/users.html", {
        "request": request,
        "user": current_user,
        "users": users
    })

@router.get("/users/create")
async def create_user_page(
    request: Request,
    current_user: User = Depends(require_admin)
):
    """Display create user form"""
    return templates.TemplateResponse("admin/create_user.html", {
        "request": request,
        "user": current_user,
        "roles": [role.value for role in UserRole]
    })

@router.post("/users/create")
async def create_user_submit(
    request: Request,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session),
    username: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    role: str = Form(...)
):
    """Handle user creation"""
    try:
        user_data = {
            "username": username,
            "email": email,
            "full_name": full_name,
            "password": password,
            "role": role
        }
        
        user = create_user(session, user_data)
        return RedirectResponse(url="/admin/users", status_code=302)
    
    except Exception as e:
        return templates.TemplateResponse("admin/create_user.html", {
            "request": request,
            "user": current_user,
            "roles": [role.value for role in UserRole],
            "error": f"Failed to create user: {str(e)}"
        })

@router.get("/clients")
async def list_clients(
    request: Request,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    """List all clients"""
    clients = get_clients(session)
    return templates.TemplateResponse("admin/clients.html", {
        "request": request,
        "user": current_user,
        "clients": clients
    })

@router.get("/clients/create")
async def create_client_page(
    request: Request,
    current_user: User = Depends(require_admin)
):
    """Display create client form"""
    return templates.TemplateResponse("admin/create_client.html", {
        "request": request,
        "user": current_user
    })

@router.post("/clients/create")
async def create_client_submit(
    request: Request,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session),
    name: str = Form(...),
    contact_person: str = Form(""),
    email: str = Form(""),
    phone: str = Form(""),
    address: str = Form("")
):
    """Handle client creation"""
    try:
        client_data = {
            "name": name,
            "contact_person": contact_person,
            "email": email,
            "phone": phone,
            "address": address
        }
        
        client = create_client(session, client_data)
        return RedirectResponse(url="/admin/clients", status_code=302)
    
    except Exception as e:
        return templates.TemplateResponse("admin/create_client.html", {
            "request": request,
            "user": current_user,
            "error": f"Failed to create client: {str(e)}"
        })
