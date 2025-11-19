from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from models import JobStatus, ApplicationStatus

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str
    picture: Optional[str] = None

class UserCreate(UserBase):
    google_id: str

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Job schemas
class JobBase(BaseModel):
    title: str
    description: str
    requirements: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    salary_range: Optional[str] = None

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    salary_range: Optional[str] = None
    status: Optional[JobStatus] = None

class Job(JobBase):
    id: int
    status: JobStatus
    created_by: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class JobWithApplicationCount(Job):
    application_count: int = 0

# Candidate schemas
class CandidateBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    skills: Optional[str] = None
    experience_years: Optional[int] = None
    current_company: Optional[str] = None
    current_position: Optional[str] = None
    linkedin_url: Optional[str] = None

class CandidateCreate(CandidateBase):
    pass

class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    skills: Optional[str] = None
    experience_years: Optional[int] = None
    current_company: Optional[str] = None
    current_position: Optional[str] = None
    linkedin_url: Optional[str] = None

class Candidate(CandidateBase):
    id: int
    resume_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Application schemas
class ApplicationBase(BaseModel):
    job_id: int
    candidate_id: int
    notes: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    notes: Optional[str] = None
    recruiter_id: Optional[int] = None

class Application(ApplicationBase):
    id: int
    status: ApplicationStatus
    recruiter_id: Optional[int] = None
    applied_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ApplicationWithDetails(Application):
    job: Job
    candidate: Candidate

# Status History schemas
class StatusHistoryBase(BaseModel):
    old_status: Optional[ApplicationStatus] = None
    new_status: ApplicationStatus
    notes: Optional[str] = None

class StatusHistory(StatusHistoryBase):
    id: int
    application_id: int
    changed_by: Optional[int] = None
    changed_at: datetime
    
    class Config:
        from_attributes = True
