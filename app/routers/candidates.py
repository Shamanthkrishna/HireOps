from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.database import get_db
from app.auth.auth import get_current_active_user, require_hiring_team
from app.models.models import Candidate, User, Application
from app.schemas.schemas import (
    CandidateCreate, 
    CandidateUpdate, 
    CandidateResponse, 
    CandidateListResponse,
    PaginationParams
)
import os
import uuid
import shutil

router = APIRouter()

# File upload configuration
UPLOAD_DIR = "uploads/resumes"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=CandidateListResponse)
async def get_candidates(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    experience_min: Optional[int] = Query(None, ge=0),
    experience_max: Optional[int] = Query(None, ge=0),
    skills: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all candidates with filtering and pagination"""
    query = db.query(Candidate)
    
    # Apply filters
    if search:
        query = query.filter(
            Candidate.first_name.ilike(f"%{search}%") | 
            Candidate.last_name.ilike(f"%{search}%") |
            Candidate.email.ilike(f"%{search}%") |
            Candidate.current_company.ilike(f"%{search}%") |
            Candidate.current_position.ilike(f"%{search}%")
        )
    
    if location:
        query = query.filter(Candidate.location.ilike(f"%{location}%"))
    
    if experience_min is not None:
        query = query.filter(Candidate.experience_years >= experience_min)
    
    if experience_max is not None:
        query = query.filter(Candidate.experience_years <= experience_max)
    
    if skills:
        query = query.filter(Candidate.skills.ilike(f"%{skills}%"))
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * size
    candidates = query.offset(offset).limit(size).all()
    
    # Add applications count for each candidate
    for candidate in candidates:
        candidate.applications_count = db.query(func.count(Application.id)).filter(
            Application.candidate_id == candidate.id
        ).scalar()
    
    pages = (total + size - 1) // size
    
    return CandidateListResponse(
        items=candidates,
        total=total,
        page=page,
        size=size,
        pages=pages
    )

@router.post("/", response_model=CandidateResponse)
async def create_candidate(
    candidate: CandidateCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hiring_team)
):
    """Create a new candidate"""
    # Check if email already exists
    existing_candidate = db.query(Candidate).filter(Candidate.email == candidate.email).first()
    if existing_candidate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Candidate with this email already exists"
        )
    
    db_candidate = Candidate(**candidate.dict())
    
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    
    # Add applications count
    db_candidate.applications_count = 0
    
    return db_candidate

@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(
    candidate_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific candidate"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    # Add applications count
    candidate.applications_count = db.query(func.count(Application.id)).filter(
        Application.candidate_id == candidate.id
    ).scalar()
    
    return candidate

@router.put("/{candidate_id}", response_model=CandidateResponse)
async def update_candidate(
    candidate_id: int, 
    candidate_update: CandidateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hiring_team)
):
    """Update a candidate"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    # Check if new email is already taken (if being updated)
    if candidate_update.email and candidate_update.email != candidate.email:
        existing_candidate = db.query(Candidate).filter(Candidate.email == candidate_update.email).first()
        if existing_candidate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken"
            )
    
    # Update candidate fields
    update_data = candidate_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(candidate, field, value)
    
    db.commit()
    db.refresh(candidate)
    
    # Add applications count
    candidate.applications_count = db.query(func.count(Application.id)).filter(
        Application.candidate_id == candidate.id
    ).scalar()
    
    return candidate

@router.delete("/{candidate_id}")
async def delete_candidate(
    candidate_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hiring_team)
):
    """Delete a candidate"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    # Check if candidate has applications
    has_applications = db.query(Application).filter(Application.candidate_id == candidate_id).first()
    if has_applications:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete candidate with existing applications"
        )
    
    # Delete resume file if exists
    if candidate.resume_path and os.path.exists(candidate.resume_path):
        os.remove(candidate.resume_path)
    
    db.delete(candidate)
    db.commit()
    
    return {"message": "Candidate deleted successfully"}

@router.post("/{candidate_id}/resume")
async def upload_resume(
    candidate_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hiring_team)
):
    """Upload resume for a candidate"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    # Validate file
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File too large. Maximum size is 10MB"
        )
    
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Allowed: PDF, DOC, DOCX"
        )
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Delete old resume if exists
    if candidate.resume_path and os.path.exists(candidate.resume_path):
        os.remove(candidate.resume_path)
    
    # Save new file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error saving file"
        )
    
    # Update candidate record
    candidate.resume_path = file_path
    db.commit()
    
    return {"message": "Resume uploaded successfully", "file_path": file_path}

@router.get("/{candidate_id}/applications", response_model=List)
async def get_candidate_applications(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all applications for a specific candidate"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    applications = db.query(Application).filter(Application.candidate_id == candidate_id).all()
    return applications