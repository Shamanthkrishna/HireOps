from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.database import get_db
from app.auth.auth import get_current_active_user, require_recruiter_or_admin
from app.models.models import Job, User, Application
from app.schemas.schemas import (
    JobCreate, 
    JobUpdate, 
    JobResponse, 
    JobListResponse,
    PaginationParams
)

router = APIRouter()

@router.get("/", response_model=JobListResponse)
async def get_jobs(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    is_active: Optional[bool] = Query(None),
    department: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all jobs with filtering and pagination"""
    query = db.query(Job)
    
    # Apply filters
    if is_active is not None:
        query = query.filter(Job.is_active == is_active)
    
    if department:
        query = query.filter(Job.department.ilike(f"%{department}%"))
    
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    
    if search:
        query = query.filter(
            Job.title.ilike(f"%{search}%") | 
            Job.description.ilike(f"%{search}%")
        )
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * size
    jobs = query.offset(offset).limit(size).all()
    
    # Add applications count for each job
    for job in jobs:
        job.applications_count = db.query(func.count(Application.id)).filter(
            Application.job_id == job.id
        ).scalar()
    
    pages = (total + size - 1) // size
    
    return JobListResponse(
        items=jobs,
        total=total,
        page=page,
        size=size,
        pages=pages
    )

@router.post("/", response_model=JobResponse)
async def create_job(
    job: JobCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_recruiter_or_admin)
):
    """Create a new job"""
    db_job = Job(
        **job.dict(),
        created_by=current_user.id
    )
    
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    
    # Add applications count
    db_job.applications_count = 0
    
    return db_job

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific job"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Add applications count
    job.applications_count = db.query(func.count(Application.id)).filter(
        Application.job_id == job.id
    ).scalar()
    
    return job

@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int, 
    job_update: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_recruiter_or_admin)
):
    """Update a job"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Check if user can update this job (admin can update any, others only their own)
    if current_user.role != "admin" and job.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this job"
        )
    
    # Update job fields
    update_data = job_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(job, field, value)
    
    db.commit()
    db.refresh(job)
    
    # Add applications count
    job.applications_count = db.query(func.count(Application.id)).filter(
        Application.job_id == job.id
    ).scalar()
    
    return job

@router.delete("/{job_id}")
async def delete_job(
    job_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_recruiter_or_admin)
):
    """Delete a job (soft delete - set inactive)"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Check if user can delete this job (admin can delete any, others only their own)
    if current_user.role != "admin" and job.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this job"
        )
    
    # Soft delete - set as inactive
    job.is_active = False
    db.commit()
    
    return {"message": "Job deleted successfully"}

@router.get("/{job_id}/applications", response_model=List)
async def get_job_applications(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all applications for a specific job"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    applications = db.query(Application).filter(Application.job_id == job_id).all()
    return applications