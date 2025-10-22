from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    BUSINESS_HEAD = "business_head"
    BUSINESS_SUPPORT = "business_support"
    SALES_HEAD = "sales_head"
    ACCOUNT_MANAGER = "account_manager"
    SALES_PERSON = "sales_person"
    RECRUITER = "recruiter"

class RequirementStatus(str, Enum):
    OPEN = "open"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"
    ON_HOLD = "on_hold"

class CandidateStatus(str, Enum):
    APPLIED = "applied"
    SCREENED = "screened"
    SUBMITTED = "submitted"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEWED = "interviewed"
    OFFERED = "offered"
    HIRED = "hired"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class EmploymentMode(str, Enum):
    CONTRACT = "contract"
    PERMANENT = "permanent"

# Database Models
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    full_name: str
    hashed_password: str
    role: UserRole
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    created_requirements: List["Requirement"] = Relationship(
        back_populates="created_by_user",
        sa_relationship_kwargs={"foreign_keys": "Requirement.created_by"}
    )
    assigned_requirements: List["Requirement"] = Relationship(
        back_populates="assigned_recruiter",
        sa_relationship_kwargs={"foreign_keys": "Requirement.assigned_to"}
    )
    candidate_updates: List["CandidateStatusHistory"] = Relationship(back_populates="changed_by_user")

class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    requirements: List["Requirement"] = Relationship(back_populates="client")

class Requirement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    req_id: str = Field(unique=True, index=True)  # Custom requirement ID
    client_id: int = Field(foreign_key="client.id")
    title: str
    description: Optional[str] = None
    experience_required: Optional[str] = None
    skills_required: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    location: Optional[str] = None
    employment_mode: EmploymentMode
    priority: str = Field(default="medium")  # high, medium, low
    status: RequirementStatus = Field(default=RequirementStatus.OPEN)
    positions_count: int = Field(default=1)
    created_by: int = Field(foreign_key="user.id")
    assigned_to: Optional[int] = Field(default=None, foreign_key="user.id")
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    client: Client = Relationship(back_populates="requirements")
    created_by_user: User = Relationship(
        back_populates="created_requirements",
        sa_relationship_kwargs={"foreign_keys": "Requirement.created_by"}
    )
    assigned_recruiter: Optional[User] = Relationship(
        back_populates="assigned_requirements",
        sa_relationship_kwargs={"foreign_keys": "Requirement.assigned_to"}
    )
    candidates: List["Candidate"] = Relationship(back_populates="requirement")

class Candidate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    requirement_id: int = Field(foreign_key="requirement.id")
    name: str
    email: str = Field(index=True)
    phone: Optional[str] = None
    current_company: Optional[str] = None
    current_designation: Optional[str] = None
    experience_years: Optional[float] = None
    current_ctc: Optional[float] = None
    expected_ctc: Optional[float] = None
    notice_period: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[str] = None
    status: CandidateStatus = Field(default=CandidateStatus.APPLIED)
    resume_path: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    requirement: Requirement = Relationship(back_populates="candidates")
    status_history: List["CandidateStatusHistory"] = Relationship(back_populates="candidate")

class CandidateStatusHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    candidate_id: int = Field(foreign_key="candidate.id")
    old_status: Optional[CandidateStatus] = None
    new_status: CandidateStatus
    changed_by: int = Field(foreign_key="user.id")
    changed_at: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None
    
    # Relationships
    candidate: Candidate = Relationship(back_populates="status_history")
    changed_by_user: User = Relationship(back_populates="candidate_updates")
