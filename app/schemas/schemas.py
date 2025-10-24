from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enums matching the database models
class UserRole(str, Enum):
    ADMIN = "admin"
    RECRUITER = "recruiter"
    INTERVIEWER = "interviewer"
    HIRING_MANAGER = "hiring_manager"

class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    SCREENING = "screening"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEW_COMPLETED = "interview_completed"
    OFFER_EXTENDED = "offer_extended"
    OFFER_ACCEPTED = "offer_accepted"
    OFFER_DECLINED = "offer_declined"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class InterviewType(str, Enum):
    PHONE = "phone"
    VIDEO = "video"
    IN_PERSON = "in_person"
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"

# User Schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)
    role: UserRole

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

# Job Schemas
class JobBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10)
    requirements: Optional[str] = None
    location: Optional[str] = Field(None, max_length=100)
    department: Optional[str] = Field(None, max_length=100)
    employment_type: Optional[str] = Field(None, max_length=50)
    experience_level: Optional[str] = Field(None, max_length=50)
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    is_active: bool = True

    @validator('salary_max')
    def salary_max_greater_than_min(cls, v, values):
        if v is not None and 'salary_min' in values and values['salary_min'] is not None:
            if v < values['salary_min']:
                raise ValueError('salary_max must be greater than salary_min')
        return v

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    requirements: Optional[str] = None
    location: Optional[str] = Field(None, max_length=100)
    department: Optional[str] = Field(None, max_length=100)
    employment_type: Optional[str] = Field(None, max_length=50)
    experience_level: Optional[str] = Field(None, max_length=50)
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None

class JobResponse(JobBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    applications_count: Optional[int] = 0

    class Config:
        from_attributes = True

# Candidate Schemas
class CandidateBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    current_company: Optional[str] = Field(None, max_length=100)
    current_position: Optional[str] = Field(None, max_length=100)
    experience_years: Optional[int] = Field(None, ge=0, le=50)
    skills: Optional[str] = None
    location: Optional[str] = Field(None, max_length=100)

class CandidateCreate(CandidateBase):
    pass

class CandidateUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    current_company: Optional[str] = Field(None, max_length=100)
    current_position: Optional[str] = Field(None, max_length=100)
    experience_years: Optional[int] = Field(None, ge=0, le=50)
    skills: Optional[str] = None
    location: Optional[str] = Field(None, max_length=100)

class CandidateResponse(CandidateBase):
    id: int
    resume_path: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    applications_count: Optional[int] = 0

    class Config:
        from_attributes = True

# Application Schemas
class ApplicationBase(BaseModel):
    job_id: int
    candidate_id: int
    source: Optional[str] = Field(None, max_length=100)
    cover_letter: Optional[str] = None
    notes: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    assigned_recruiter_id: Optional[int] = None
    source: Optional[str] = Field(None, max_length=100)
    cover_letter: Optional[str] = None
    notes: Optional[str] = None

class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus
    reason: Optional[str] = None
    notes: Optional[str] = None

class ApplicationResponse(ApplicationBase):
    id: int
    status: ApplicationStatus
    assigned_recruiter_id: Optional[int] = None
    applied_at: datetime
    updated_at: Optional[datetime] = None
    
    # Nested objects
    job: Optional[JobResponse] = None
    candidate: Optional[CandidateResponse] = None
    assigned_recruiter: Optional[UserResponse] = None

    class Config:
        from_attributes = True

# Interview Schemas
class InterviewBase(BaseModel):
    application_id: int
    interviewer_id: int
    interview_type: InterviewType
    scheduled_at: datetime
    duration_minutes: int = Field(default=60, ge=15, le=480)  # 15 min to 8 hours
    location: Optional[str] = Field(None, max_length=255)

class InterviewCreate(InterviewBase):
    pass

class InterviewUpdate(BaseModel):
    interview_type: Optional[InterviewType] = None
    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, ge=15, le=480)
    location: Optional[str] = Field(None, max_length=255)
    status: Optional[str] = Field(None, max_length=50)
    feedback: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=10)
    notes: Optional[str] = None

class InterviewResponse(InterviewBase):
    id: int
    status: str
    feedback: Optional[str] = None
    rating: Optional[int] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Nested objects
    application: Optional[ApplicationResponse] = None
    interviewer: Optional[UserResponse] = None

    class Config:
        from_attributes = True

# Status History Schemas
class StatusHistoryResponse(BaseModel):
    id: int
    application_id: int
    from_status: Optional[ApplicationStatus] = None
    to_status: ApplicationStatus
    changed_by: int
    reason: Optional[str] = None
    notes: Optional[str] = None
    changed_at: datetime
    
    # Nested object
    changed_by_user: Optional[UserResponse] = None

    class Config:
        from_attributes = True

# Pagination and List Responses
class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=100)

class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    size: int
    pages: int

class JobListResponse(PaginatedResponse):
    items: List[JobResponse]

class CandidateListResponse(PaginatedResponse):
    items: List[CandidateResponse]

class ApplicationListResponse(PaginatedResponse):
    items: List[ApplicationResponse]

class InterviewListResponse(PaginatedResponse):
    items: List[InterviewResponse]