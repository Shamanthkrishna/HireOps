from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel import Session
from app.database import get_session
from app.auth import get_current_user_from_session, require_recruiter_or_above
from app.crud import (
    get_candidates, get_candidate, create_candidate, 
    update_candidate, get_requirements, get_candidate_status_history
)
from app.models import User, CandidateStatus
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def list_candidates(
    request: Request,
    current_user: User = Depends(get_current_user_from_session),
    session: Session = Depends(get_session),
    requirement_id: Optional[int] = None,
    status: Optional[str] = None
):
    """List all candidates with filtering"""
    # Get candidates based on filters and user role
    if current_user.role == "recruiter":
        # Recruiters see candidates for their assigned requirements
        user_requirements = get_requirements(session, assigned_to=current_user.id)
        req_ids = [req.id for req in user_requirements]
        if requirement_id and requirement_id in req_ids:
            candidates = get_candidates(session, requirement_id=requirement_id, status=status)
        else:
            # Get all candidates for recruiter's requirements
            all_candidates = []
            for req_id in req_ids:
                candidates_for_req = get_candidates(session, requirement_id=req_id, status=status)
                all_candidates.extend(candidates_for_req)
            candidates = all_candidates
    elif current_user.role == "sales_person":
        # Sales persons see candidates for their created requirements
        user_requirements = get_requirements(session, created_by=current_user.id)
        req_ids = [req.id for req in user_requirements]
        if requirement_id and requirement_id in req_ids:
            candidates = get_candidates(session, requirement_id=requirement_id, status=status)
        else:
            all_candidates = []
            for req_id in req_ids:
                candidates_for_req = get_candidates(session, requirement_id=req_id, status=status)
                all_candidates.extend(candidates_for_req)
            candidates = all_candidates
    else:
        # Admin, AM can see all candidates
        candidates = get_candidates(session, requirement_id=requirement_id, status=status)
    
    # Get available requirements for filtering
    if current_user.role == "recruiter":
        requirements = get_requirements(session, assigned_to=current_user.id)
    elif current_user.role == "sales_person":
        requirements = get_requirements(session, created_by=current_user.id)
    else:
        requirements = get_requirements(session)
    
    return templates.TemplateResponse("candidates/list.html", {
        "request": request,
        "user": current_user,
        "candidates": candidates,
        "requirements": requirements,
        "statuses": [status.value for status in CandidateStatus],
        "selected_requirement": requirement_id,
        "selected_status": status
    })

@router.get("/create")
async def create_candidate_page(
    request: Request,
    current_user: User = Depends(require_recruiter_or_above),
    session: Session = Depends(get_session),
    requirement_id: Optional[int] = None
):
    """Display create candidate form"""
    # Get available requirements based on user role
    if current_user.role == "recruiter":
        requirements = get_requirements(session, assigned_to=current_user.id)
    else:
        requirements = get_requirements(session)
    
    return templates.TemplateResponse("candidates/create.html", {
        "request": request,
        "user": current_user,
        "requirements": requirements,
        "selected_requirement": requirement_id
    })

@router.post("/create")
async def create_candidate_submit(
    request: Request,
    current_user: User = Depends(require_recruiter_or_above),
    session: Session = Depends(get_session),
    requirement_id: int = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    current_company: str = Form(""),
    current_designation: str = Form(""),
    experience_years: Optional[float] = Form(None),
    current_ctc: Optional[float] = Form(None),
    expected_ctc: Optional[float] = Form(None),
    notice_period: str = Form(""),
    location: str = Form(""),
    skills: str = Form(""),
    notes: str = Form("")
):
    """Handle candidate creation"""
    try:
        candidate_data = {
            "requirement_id": requirement_id,
            "name": name,
            "email": email,
            "phone": phone,
            "current_company": current_company,
            "current_designation": current_designation,
            "experience_years": experience_years,
            "current_ctc": current_ctc,
            "expected_ctc": expected_ctc,
            "notice_period": notice_period,
            "location": location,
            "skills": skills,
            "notes": notes
        }
        
        candidate = create_candidate(session, candidate_data)
        return RedirectResponse(url="/candidates", status_code=302)
    
    except Exception as e:
        # Return to form with error
        if current_user.role == "recruiter":
            requirements = get_requirements(session, assigned_to=current_user.id)
        else:
            requirements = get_requirements(session)
        
        return templates.TemplateResponse("candidates/create.html", {
            "request": request,
            "user": current_user,
            "requirements": requirements,
            "error": f"Failed to create candidate: {str(e)}"
        })

@router.get("/{candidate_id}")
async def view_candidate(
    request: Request,
    candidate_id: int,
    current_user: User = Depends(get_current_user_from_session),
    session: Session = Depends(get_session)
):
    """View candidate details with status history"""
    candidate = get_candidate(session, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Check permissions
    requirement = get_requirements(session, skip=0, limit=1)  # Get requirement details
    requirement = next((r for r in get_requirements(session) if r.id == candidate.requirement_id), None)
    
    if requirement:
        if (current_user.role == "recruiter" and requirement.assigned_to != current_user.id) or \
           (current_user.role == "sales_person" and requirement.created_by != current_user.id):
            raise HTTPException(status_code=403, detail="Not authorized to view this candidate")
    
    # Get status history
    status_history = get_candidate_status_history(session, candidate_id)
    
    return templates.TemplateResponse("candidates/detail.html", {
        "request": request,
        "user": current_user,
        "candidate": candidate,
        "status_history": status_history
    })

@router.get("/{candidate_id}/edit")
async def edit_candidate_page(
    request: Request,
    candidate_id: int,
    current_user: User = Depends(require_recruiter_or_above),
    session: Session = Depends(get_session)
):
    """Display edit candidate form"""
    candidate = get_candidate(session, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    return templates.TemplateResponse("candidates/edit.html", {
        "request": request,
        "user": current_user,
        "candidate": candidate,
        "statuses": [status.value for status in CandidateStatus]
    })

@router.post("/{candidate_id}/edit")
async def edit_candidate_submit(
    request: Request,
    candidate_id: int,
    current_user: User = Depends(require_recruiter_or_above),
    session: Session = Depends(get_session),
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    current_company: str = Form(""),
    current_designation: str = Form(""),
    experience_years: Optional[float] = Form(None),
    current_ctc: Optional[float] = Form(None),
    expected_ctc: Optional[float] = Form(None),
    notice_period: str = Form(""),
    location: str = Form(""),
    skills: str = Form(""),
    status: str = Form(...),
    notes: str = Form("")
):
    """Handle candidate update"""
    try:
        update_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "current_company": current_company,
            "current_designation": current_designation,
            "experience_years": experience_years,
            "current_ctc": current_ctc,
            "expected_ctc": expected_ctc,
            "notice_period": notice_period,
            "location": location,
            "skills": skills,
            "status": status,
            "notes": notes
        }
        
        candidate = update_candidate(session, candidate_id, update_data, current_user.id)
        return RedirectResponse(url=f"/candidates/{candidate_id}", status_code=302)
    
    except Exception as e:
        candidate = get_candidate(session, candidate_id)
        
        return templates.TemplateResponse("candidates/edit.html", {
            "request": request,
            "user": current_user,
            "candidate": candidate,
            "statuses": [status.value for status in CandidateStatus],
            "error": f"Failed to update candidate: {str(e)}"
        })
