from sqlmodel import Session, select
from typing import Optional, List
from datetime import datetime
from app.models import User, Client, Requirement, Candidate, CandidateStatusHistory
from app.models import RequirementStatus, CandidateStatus
from app.auth import get_password_hash

# User CRUD operations
def get_user_by_username(session: Session, username: str) -> Optional[User]:
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def create_user(session: Session, user_data: dict) -> User:
    hashed_password = get_password_hash(user_data.pop("password"))
    user = User(**user_data, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_users(session: Session, skip: int = 0, limit: int = 100) -> List[User]:
    statement = select(User).offset(skip).limit(limit)
    return session.exec(statement).all()

def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)

# Client CRUD operations
def create_client(session: Session, client_data: dict) -> Client:
    client = Client(**client_data)
    session.add(client)
    session.commit()
    session.refresh(client)
    return client

def get_clients(session: Session, skip: int = 0, limit: int = 100) -> List[Client]:
    statement = select(Client).where(Client.is_active == True).offset(skip).limit(limit)
    return session.exec(statement).all()

def get_client(session: Session, client_id: int) -> Optional[Client]:
    return session.get(Client, client_id)

# Requirement CRUD operations
def create_requirement(session: Session, requirement_data: dict) -> Requirement:
    requirement = Requirement(**requirement_data)
    session.add(requirement)
    session.commit()
    session.refresh(requirement)
    return requirement

def get_requirements(
    session: Session, 
    skip: int = 0, 
    limit: int = 100,
    status: Optional[RequirementStatus] = None,
    assigned_to: Optional[int] = None,
    created_by: Optional[int] = None
) -> List[Requirement]:
    statement = select(Requirement)
    
    if status:
        statement = statement.where(Requirement.status == status)
    if assigned_to:
        statement = statement.where(Requirement.assigned_to == assigned_to)
    if created_by:
        statement = statement.where(Requirement.created_by == created_by)
    
    statement = statement.offset(skip).limit(limit)
    return session.exec(statement).all()

def get_requirement(session: Session, requirement_id: int) -> Optional[Requirement]:
    return session.get(Requirement, requirement_id)

def update_requirement(session: Session, requirement_id: int, update_data: dict) -> Optional[Requirement]:
    requirement = session.get(Requirement, requirement_id)
    if requirement:
        for key, value in update_data.items():
            if value is not None:
                setattr(requirement, key, value)
        requirement.updated_at = datetime.utcnow()
        session.add(requirement)
        session.commit()
        session.refresh(requirement)
    return requirement

# Candidate CRUD operations
def create_candidate(session: Session, candidate_data: dict) -> Candidate:
    candidate = Candidate(**candidate_data)
    session.add(candidate)
    session.commit()
    session.refresh(candidate)
    
    # Create initial status history entry
    create_status_history(
        session=session,
        candidate_id=candidate.id,
        old_status=None,
        new_status=candidate.status,
        changed_by=1,  # System user, should be actual user in real implementation
        notes="Initial candidate creation"
    )
    
    return candidate

def get_candidates(
    session: Session,
    skip: int = 0,
    limit: int = 100,
    requirement_id: Optional[int] = None,
    status: Optional[CandidateStatus] = None
) -> List[Candidate]:
    statement = select(Candidate)
    
    if requirement_id:
        statement = statement.where(Candidate.requirement_id == requirement_id)
    if status:
        statement = statement.where(Candidate.status == status)
    
    statement = statement.offset(skip).limit(limit)
    return session.exec(statement).all()

def get_candidate(session: Session, candidate_id: int) -> Optional[Candidate]:
    return session.get(Candidate, candidate_id)

def update_candidate(
    session: Session, 
    candidate_id: int, 
    update_data: dict, 
    changed_by: int
) -> Optional[Candidate]:
    candidate = session.get(Candidate, candidate_id)
    if candidate:
        old_status = candidate.status
        
        for key, value in update_data.items():
            if value is not None:
                setattr(candidate, key, value)
        
        candidate.updated_at = datetime.utcnow()
        session.add(candidate)
        session.commit()
        session.refresh(candidate)
        
        # Create status history if status changed
        if "status" in update_data and update_data["status"] != old_status:
            create_status_history(
                session=session,
                candidate_id=candidate.id,
                old_status=old_status,
                new_status=candidate.status,
                changed_by=changed_by,
                notes=update_data.get("notes", "Status updated")
            )
    
    return candidate

# Status History operations
def create_status_history(
    session: Session,
    candidate_id: int,
    old_status: Optional[CandidateStatus],
    new_status: CandidateStatus,
    changed_by: int,
    notes: Optional[str] = None
) -> CandidateStatusHistory:
    history = CandidateStatusHistory(
        candidate_id=candidate_id,
        old_status=old_status,
        new_status=new_status,
        changed_by=changed_by,
        notes=notes
    )
    session.add(history)
    session.commit()
    session.refresh(history)
    return history

def get_candidate_status_history(session: Session, candidate_id: int) -> List[CandidateStatusHistory]:
    statement = select(CandidateStatusHistory).where(
        CandidateStatusHistory.candidate_id == candidate_id
    ).order_by(CandidateStatusHistory.changed_at.desc())
    return session.exec(statement).all()

# Dashboard analytics
def get_dashboard_stats(session: Session, user_role: str, user_id: int) -> dict:
    """Get dashboard statistics based on user role"""
    stats = {}
    
    # Base queries
    requirements_query = select(Requirement)
    candidates_query = select(Candidate)
    
    # Filter based on user role
    if user_role == "recruiter":
        requirements_query = requirements_query.where(Requirement.assigned_to == user_id)
        # Get candidates for requirements assigned to this recruiter
        user_requirements = session.exec(requirements_query).all()
        req_ids = [req.id for req in user_requirements]
        candidates_query = candidates_query.where(Candidate.requirement_id.in_(req_ids))
    elif user_role == "sales_person":
        requirements_query = requirements_query.where(Requirement.created_by == user_id)
        # Get candidates for requirements created by this sales person
        user_requirements = session.exec(requirements_query).all()
        req_ids = [req.id for req in user_requirements]
        candidates_query = candidates_query.where(Candidate.requirement_id.in_(req_ids))
    
    # Get all requirements and candidates based on filters
    requirements = session.exec(requirements_query).all()
    candidates = session.exec(candidates_query).all()
    
    # Calculate stats
    stats["total_requirements"] = len(requirements)
    stats["active_requirements"] = len([r for r in requirements if r.status in ["open", "assigned", "in_progress"]])
    stats["total_candidates"] = len(candidates)
    stats["hired_candidates"] = len([c for c in candidates if c.status == "hired"])
    
    # Status breakdowns
    req_status_counts = {}
    for req in requirements:
        req_status_counts[req.status] = req_status_counts.get(req.status, 0) + 1
    stats["requirements_by_status"] = req_status_counts
    
    cand_status_counts = {}
    for cand in candidates:
        cand_status_counts[cand.status] = cand_status_counts.get(cand.status, 0) + 1
    stats["candidates_by_status"] = cand_status_counts
    
    return stats
