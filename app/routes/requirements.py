from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel import Session
from app.database import get_session
from app.auth import get_current_user_from_session, require_recruiter_or_above
from app.crud import (
    get_requirements, get_requirement, create_requirement, 
    update_requirement, get_clients, get_users
)
from app.models import User, RequirementStatus, EmploymentMode
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def list_requirements(
    request: Request,
    current_user: User = Depends(get_current_user_from_session),
    session: Session = Depends(get_session),
    status: Optional[str] = None
):
    """List all requirements with filtering"""
    # Filter requirements based on user role
    if current_user.role == "recruiter":
        requirements = get_requirements(session, assigned_to=current_user.id)
    elif current_user.role == "sales_person":
        requirements = get_requirements(session, created_by=current_user.id)
    else:
        # Admin, AM, etc. can see all
        requirements = get_requirements(session, status=status)
    
    return templates.TemplateResponse("requirements/list.html", {
        "request": request,
        "user": current_user,
        "requirements": requirements,
        "statuses": [status.value for status in RequirementStatus]
    })

@router.get("/create")
async def create_requirement_page(
    request: Request,
    current_user: User = Depends(get_current_user_from_session),
    session: Session = Depends(get_session)
):
    """Display create requirement form"""
    clients = get_clients(session)
    users = get_users(session)
    recruiters = [u for u in users if u.role == "recruiter"]
    
    return templates.TemplateResponse("requirements/create.html", {
        "request": request,
        "user": current_user,
        "clients": clients,
        "recruiters": recruiters,
        "employment_modes": [mode.value for mode in EmploymentMode]
    })

@router.post("/create")
async def create_requirement_submit(
    request: Request,
    current_user: User = Depends(get_current_user_from_session),
    session: Session = Depends(get_session),
    req_id: str = Form(...),
    client_id: int = Form(...),
    title: str = Form(...),
    description: str = Form(""),
    experience_required: str = Form(""),
    skills_required: str = Form(""),
    budget_min: Optional[float] = Form(None),
    budget_max: Optional[float] = Form(None),
    location: str = Form(""),
    employment_mode: str = Form(...),
    priority: str = Form("medium"),
    positions_count: int = Form(1),
    assigned_to: Optional[int] = Form(None),
    notes: str = Form("")
):
    """Handle requirement creation"""
    try:
        requirement_data = {
            "req_id": req_id,
            "client_id": client_id,
            "title": title,
            "description": description,
            "experience_required": experience_required,
            "skills_required": skills_required,
            "budget_min": budget_min,
            "budget_max": budget_max,
            "location": location,
            "employment_mode": employment_mode,
            "priority": priority,
            "positions_count": positions_count,
            "created_by": current_user.id,
            "assigned_to": assigned_to,
            "notes": notes
        }
        
        requirement = create_requirement(session, requirement_data)
        return RedirectResponse(url="/requirements", status_code=302)
    
    except Exception as e:
        # Return to form with error
        clients = get_clients(session)
        users = get_users(session)
        recruiters = [u for u in users if u.role == "recruiter"]
        
        return templates.TemplateResponse("requirements/create.html", {
            "request": request,
            "user": current_user,
            "clients": clients,
            "recruiters": recruiters,
            "employment_modes": [mode.value for mode in EmploymentMode],
            "error": f"Failed to create requirement: {str(e)}"
        })

@router.get("/{requirement_id}")
async def view_requirement(
    request: Request,
    requirement_id: int,
    current_user: User = Depends(get_current_user_from_session),
    session: Session = Depends(get_session)
):
    """View requirement details"""
    requirement = get_requirement(session, requirement_id)
    if not requirement:
        raise HTTPException(status_code=404, detail="Requirement not found")
    
    # Check permissions
    if (current_user.role == "recruiter" and requirement.assigned_to != current_user.id) or \
       (current_user.role == "sales_person" and requirement.created_by != current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to view this requirement")
    
    return templates.TemplateResponse("requirements/detail.html", {
        "request": request,
        "user": current_user,
        "requirement": requirement
    })

@router.get("/{requirement_id}/edit")
async def edit_requirement_page(
    request: Request,
    requirement_id: int,
    current_user: User = Depends(require_recruiter_or_above),
    session: Session = Depends(get_session)
):
    """Display edit requirement form"""
    requirement = get_requirement(session, requirement_id)
    if not requirement:
        raise HTTPException(status_code=404, detail="Requirement not found")
    
    clients = get_clients(session)
    users = get_users(session)
    recruiters = [u for u in users if u.role == "recruiter"]
    
    return templates.TemplateResponse("requirements/edit.html", {
        "request": request,
        "user": current_user,
        "requirement": requirement,
        "clients": clients,
        "recruiters": recruiters,
        "employment_modes": [mode.value for mode in EmploymentMode],
        "statuses": [status.value for status in RequirementStatus]
    })

@router.post("/{requirement_id}/edit")
async def edit_requirement_submit(
    request: Request,
    requirement_id: int,
    current_user: User = Depends(require_recruiter_or_above),
    session: Session = Depends(get_session),
    title: str = Form(...),
    description: str = Form(""),
    experience_required: str = Form(""),
    skills_required: str = Form(""),
    budget_min: Optional[float] = Form(None),
    budget_max: Optional[float] = Form(None),
    location: str = Form(""),
    employment_mode: str = Form(...),
    priority: str = Form("medium"),
    status: str = Form(...),
    positions_count: int = Form(1),
    assigned_to: Optional[int] = Form(None),
    notes: str = Form("")
):
    """Handle requirement update"""
    try:
        update_data = {
            "title": title,
            "description": description,
            "experience_required": experience_required,
            "skills_required": skills_required,
            "budget_min": budget_min,
            "budget_max": budget_max,
            "location": location,
            "employment_mode": employment_mode,
            "priority": priority,
            "status": status,
            "positions_count": positions_count,
            "assigned_to": assigned_to,
            "notes": notes
        }
        
        requirement = update_requirement(session, requirement_id, update_data)
        return RedirectResponse(url=f"/requirements/{requirement_id}", status_code=302)
    
    except Exception as e:
        requirement = get_requirement(session, requirement_id)
        clients = get_clients(session)
        users = get_users(session)
        recruiters = [u for u in users if u.role == "recruiter"]
        
        return templates.TemplateResponse("requirements/edit.html", {
            "request": request,
            "user": current_user,
            "requirement": requirement,
            "clients": clients,
            "recruiters": recruiters,
            "employment_modes": [mode.value for mode in EmploymentMode],
            "statuses": [status.value for status in RequirementStatus],
            "error": f"Failed to update requirement: {str(e)}"
        })
