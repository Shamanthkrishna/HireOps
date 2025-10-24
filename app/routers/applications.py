from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from app.database.database import get_db
from app.auth.auth import get_current_active_user, require_hiring_team
from app.models.models import (
    Application, 
    User, 
    Job, 
    Candidate, 
    ApplicationStatusHistory,
    ApplicationStatus
)
from app.schemas.schemas import (
    ApplicationCreate, 
    ApplicationUpdate, 
    ApplicationResponse, 
    ApplicationListResponse,
    ApplicationStatusUpdate,
    StatusHistoryResponse
)

router = APIRouter()

def create_status_history(
    db: Session, 
    application_id: int, 
    from_status: Optional[ApplicationStatus], 
    to_status: ApplicationStatus,
    changed_by: int,
    reason: Optional[str] = None,
    notes: Optional[str] = None
):
    """Create a status history entry"""
    history = ApplicationStatusHistory(
        application_id=application_id,
        from_status=from_status,
        to_status=to_status,
        changed_by=changed_by,
        reason=reason,
        notes=notes
    )
    db.add(history)
    return history

@router.get("/", response_model=ApplicationListResponse)
async def get_applications(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status: Optional[ApplicationStatus] = Query(None),
    job_id: Optional[int] = Query(None),
    candidate_id: Optional[int] = Query(None),
    assigned_recruiter_id: Optional[int] = Query(None),
    source: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all applications with filtering and pagination"""
    query = db.query(Application).options(
        joinedload(Application.job),
        joinedload(Application.candidate),
        joinedload(Application.assigned_recruiter)
    )
    
    # Apply filters
    if status:
        query = query.filter(Application.status == status)
    
    if job_id:
        query = query.filter(Application.job_id == job_id)
    
    if candidate_id:
        query = query.filter(Application.candidate_id == candidate_id)
    
    if assigned_recruiter_id:
        query = query.filter(Application.assigned_recruiter_id == assigned_recruiter_id)
    
    if source:
        query = query.filter(Application.source.ilike(f"%{source}%"))
    
    # Role-based filtering for non-admin users
    if current_user.role == "recruiter":
        query = query.filter(Application.assigned_recruiter_id == current_user.id)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * size
    applications = query.offset(offset).limit(size).all()
    
    pages = (total + size - 1) // size
    
    return ApplicationListResponse(
        items=applications,
        total=total,
        page=page,
        size=size,
        pages=pages
    )

@router.post("/", response_model=ApplicationResponse)
async def create_application(
    application: ApplicationCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hiring_team)
):
    """Create a new application"""
    # Verify job exists and is active
    job = db.query(Job).filter(Job.id == application.job_id, Job.is_active == True).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found or inactive"
        )
    
    # Verify candidate exists
    candidate = db.query(Candidate).filter(Candidate.id == application.candidate_id).first()
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    # Check if application already exists for this job-candidate combination
    existing_application = db.query(Application).filter(
        Application.job_id == application.job_id,
        Application.candidate_id == application.candidate_id
    ).first()
    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Application already exists for this job-candidate combination"
        )
    
    # Create application
    db_application = Application(
        **application.dict(),
        status=ApplicationStatus.APPLIED
    )
    
    db.add(db_application)
    db.flush()  # Get the ID without committing
    
    # Create initial status history
    create_status_history(
        db=db,
        application_id=db_application.id,
        from_status=None,
        to_status=ApplicationStatus.APPLIED,
        changed_by=current_user.id,
        reason="Application submitted"
    )
    
    db.commit()
    db.refresh(db_application)
    
    # Load relationships
    db_application = db.query(Application).options(
        joinedload(Application.job),
        joinedload(Application.candidate),
        joinedload(Application.assigned_recruiter)
    ).filter(Application.id == db_application.id).first()
    
    return db_application

@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific application"""
    application = db.query(Application).options(
        joinedload(Application.job),
        joinedload(Application.candidate),
        joinedload(Application.assigned_recruiter)
    ).filter(Application.id == application_id).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    # Role-based access control
    if (current_user.role == "recruiter" and 
        application.assigned_recruiter_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this application"
        )
    
    return application

@router.put("/{application_id}", response_model=ApplicationResponse)
async def update_application(
    application_id: int, 
    application_update: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hiring_team)
):
    """Update an application"""
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    # Role-based access control
    if (current_user.role == "recruiter" and 
        application.assigned_recruiter_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this application"
        )
    
    # Handle status change separately if provided
    old_status = application.status
    update_data = application_update.dict(exclude_unset=True)
    
    if "status" in update_data:
        new_status = update_data["status"]
        if new_status != old_status:
            # Create status history
            create_status_history(
                db=db,
                application_id=application_id,
                from_status=old_status,
                to_status=new_status,
                changed_by=current_user.id,
                reason="Status updated via application update"
            )
    
    # Update application fields
    for field, value in update_data.items():
        setattr(application, field, value)
    
    db.commit()
    db.refresh(application)
    
    # Load relationships
    application = db.query(Application).options(
        joinedload(Application.job),
        joinedload(Application.candidate),
        joinedload(Application.assigned_recruiter)
    ).filter(Application.id == application_id).first()
    
    return application

@router.delete("/{application_id}")
async def delete_application(
    application_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hiring_team)
):
    """Delete an application"""
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    # Role-based access control
    if (current_user.role != "admin" and 
        current_user.role == "recruiter" and 
        application.assigned_recruiter_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this application"
        )
    
    # Create withdrawal status history before deletion
    create_status_history(
        db=db,
        application_id=application_id,
        from_status=application.status,
        to_status=ApplicationStatus.WITHDRAWN,
        changed_by=current_user.id,
        reason="Application deleted"
    )
    
    db.delete(application)
    db.commit()
    
    return {"message": "Application deleted successfully"}

@router.put("/{application_id}/status", response_model=ApplicationResponse)
async def update_application_status(
    application_id: int, 
    status_update: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hiring_team)
):
    """Update application status with audit trail"""
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    # Role-based access control
    if (current_user.role == "recruiter" and 
        application.assigned_recruiter_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this application status"
        )
    
    old_status = application.status
    new_status = status_update.status
    
    if old_status == new_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Application is already in the specified status"
        )
    
    # Validate status transitions (basic business rules)
    valid_transitions = {
        ApplicationStatus.APPLIED: [ApplicationStatus.SCREENING, ApplicationStatus.REJECTED],
        ApplicationStatus.SCREENING: [ApplicationStatus.INTERVIEW_SCHEDULED, ApplicationStatus.REJECTED],
        ApplicationStatus.INTERVIEW_SCHEDULED: [ApplicationStatus.INTERVIEW_COMPLETED, ApplicationStatus.REJECTED],
        ApplicationStatus.INTERVIEW_COMPLETED: [ApplicationStatus.OFFER_EXTENDED, ApplicationStatus.REJECTED],
        ApplicationStatus.OFFER_EXTENDED: [ApplicationStatus.OFFER_ACCEPTED, ApplicationStatus.OFFER_DECLINED, ApplicationStatus.REJECTED],
        ApplicationStatus.OFFER_ACCEPTED: [],  # Terminal state
        ApplicationStatus.OFFER_DECLINED: [],  # Terminal state
        ApplicationStatus.REJECTED: [],  # Terminal state
        ApplicationStatus.WITHDRAWN: []  # Terminal state
    }
    
    if new_status not in valid_transitions.get(old_status, []) and new_status != ApplicationStatus.WITHDRAWN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status transition from {old_status} to {new_status}"
        )
    
    # Update status
    application.status = new_status
    
    # Create status history
    create_status_history(
        db=db,
        application_id=application_id,
        from_status=old_status,
        to_status=new_status,
        changed_by=current_user.id,
        reason=status_update.reason,
        notes=status_update.notes
    )
    
    db.commit()
    db.refresh(application)
    
    # Load relationships
    application = db.query(Application).options(
        joinedload(Application.job),
        joinedload(Application.candidate),
        joinedload(Application.assigned_recruiter)
    ).filter(Application.id == application_id).first()
    
    return application

@router.get("/{application_id}/history", response_model=List[StatusHistoryResponse])
async def get_application_history(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get status change history for an application"""
    # Verify application exists and user has access
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    # Role-based access control
    if (current_user.role == "recruiter" and 
        application.assigned_recruiter_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this application history"
        )
    
    history = db.query(ApplicationStatusHistory).options(
        joinedload(ApplicationStatusHistory.changed_by_user)
    ).filter(
        ApplicationStatusHistory.application_id == application_id
    ).order_by(ApplicationStatusHistory.changed_at.desc()).all()
    
    return history