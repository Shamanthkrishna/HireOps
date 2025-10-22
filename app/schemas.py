from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models import UserRole, RequirementStatus, CandidateStatus, EmploymentMode

# Authentication Schemas
class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: str
    role: UserRole

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Client Schemas
class ClientCreate(BaseModel):
    name: str
    contact_person: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class ClientResponse(BaseModel):
    id: int
    name: str
    contact_person: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Requirement Schemas
class RequirementCreate(BaseModel):
    req_id: str
    client_id: int
    title: str
    description: Optional[str] = None
    experience_required: Optional[str] = None
    skills_required: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    location: Optional[str] = None
    employment_mode: EmploymentMode
    priority: str = "medium"
    positions_count: int = 1
    assigned_to: Optional[int] = None
    notes: Optional[str] = None

class RequirementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    experience_required: Optional[str] = None
    skills_required: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    location: Optional[str] = None
    employment_mode: Optional[EmploymentMode] = None
    priority: Optional[str] = None
    status: Optional[RequirementStatus] = None
    positions_count: Optional[int] = None
    assigned_to: Optional[int] = None
    notes: Optional[str] = None

class RequirementResponse(BaseModel):
    id: int
    req_id: str
    client_id: int
    title: str
    description: Optional[str]
    experience_required: Optional[str]
    skills_required: Optional[str]
    budget_min: Optional[float]
    budget_max: Optional[float]
    location: Optional[str]
    employment_mode: EmploymentMode
    priority: str
    status: RequirementStatus
    positions_count: int
    created_by: int
    assigned_to: Optional[int]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    # Nested relationships
    client: ClientResponse
    created_by_user: UserResponse
    assigned_recruiter: Optional[UserResponse]

    class Config:
        from_attributes = True

# Candidate Schemas
class CandidateCreate(BaseModel):
    requirement_id: int
    name: str
    email: EmailStr
    phone: Optional[str] = None
    current_company: Optional[str] = None
    current_designation: Optional[str] = None
    experience_years: Optional[float] = None
    current_ctc: Optional[float] = None
    expected_ctc: Optional[float] = None
    notice_period: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[str] = None
    notes: Optional[str] = None

class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    current_company: Optional[str] = None
    current_designation: Optional[str] = None
    experience_years: Optional[float] = None
    current_ctc: Optional[float] = None
    expected_ctc: Optional[float] = None
    notice_period: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[str] = None
    status: Optional[CandidateStatus] = None
    notes: Optional[str] = None

class CandidateResponse(BaseModel):
    id: int
    requirement_id: int
    name: str
    email: str
    phone: Optional[str]
    current_company: Optional[str]
    current_designation: Optional[str]
    experience_years: Optional[float]
    current_ctc: Optional[float]
    expected_ctc: Optional[float]
    notice_period: Optional[str]
    location: Optional[str]
    skills: Optional[str]
    status: CandidateStatus
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Status History Schema
class StatusHistoryResponse(BaseModel):
    id: int
    old_status: Optional[CandidateStatus]
    new_status: CandidateStatus
    changed_by: int
    changed_at: datetime
    notes: Optional[str]
    changed_by_user: UserResponse

    class Config:
        from_attributes = True

# Dashboard Schemas
class DashboardStats(BaseModel):
    total_requirements: int
    active_requirements: int
    total_candidates: int
    hired_candidates: int
    requirements_by_status: dict
    candidates_by_status: dict
