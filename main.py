from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import os

# Import database and models
from database import engine, get_db, Base
import models
import schemas

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="HireOps", version="1.0.0")

# Database initialization
@app.on_event("startup")
async def startup():
    """Create database tables on startup"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Add session middleware with production-ready settings
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "your-secret-key-change-this"),
    session_cookie="hireops_session",
    max_age=14 * 24 * 60 * 60,  # 14 days
    same_site="lax",
    https_only=os.getenv("ENVIRONMENT", "development") == "production"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Configure OAuth
oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Helper function to get current user
def get_current_user(request: Request):
    user = request.session.get('user')
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

# Helper to get or create user in database
async def get_or_create_user(user_data: dict, db: AsyncSession) -> models.User:
    """Get user from database or create if doesn't exist"""
    result = await db.execute(
        select(models.User).where(models.User.email == user_data['email'])
    )
    db_user = result.scalar_one_or_none()
    
    if not db_user:
        db_user = models.User(
            email=user_data['email'],
            name=user_data['name'],
            picture=user_data.get('picture'),
            google_id=user_data.get('sub') or user_data.get('email')
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
    
    return db_user

# Routes
@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    """Landing page"""
    user = request.session.get('user')
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "user": user}
    )

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard page - requires authentication"""
    user = request.session.get('user')
    if not user:
        return RedirectResponse(url='/')
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user}
    )

@app.get("/jobs", response_class=HTMLResponse)
async def jobs_page(request: Request):
    """Jobs management page - requires authentication"""
    user = request.session.get('user')
    if not user:
        return RedirectResponse(url='/')
    return templates.TemplateResponse(
        "jobs.html",
        {"request": request, "user": user}
    )

@app.get("/candidates", response_class=HTMLResponse)
async def candidates_page(request: Request):
    """Candidates management page - requires authentication"""
    user = request.session.get('user')
    if not user:
        return RedirectResponse(url='/')
    return templates.TemplateResponse(
        "candidates.html",
        {"request": request, "user": user}
    )

@app.get("/applications", response_class=HTMLResponse)
async def applications_page(request: Request):
    """Applications tracking page - requires authentication"""
    user = request.session.get('user')
    if not user:
        return RedirectResponse(url='/')
    return templates.TemplateResponse(
        "applications.html",
        {"request": request, "user": user}
    )
    if not user:
        return RedirectResponse(url='/')
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user}
    )

@app.get("/auth/login")
async def login(request: Request):
    """Initiate Google OAuth login"""
    # Always use the actual request URL to construct redirect_uri
    # This ensures it works in both local dev and production
    redirect_uri = f"{request.url.scheme}://{request.url.netloc}/auth/callback"
    
    # Detailed debug logging
    print("=" * 50)
    print(f"Login initiated from: {request.url}")
    print(f"Scheme: {request.url.scheme}")
    print(f"Netloc: {request.url.netloc}")
    print(f"Constructed redirect_uri: {redirect_uri}")
    print("=" * 50)
    
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/callback")
async def auth_callback(request: Request, db: AsyncSession = Depends(get_db)):
    """Google OAuth callback"""
    try:
        # Get the token from Google
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        
        if user_info:
            # Save or update user in database
            db_user = await get_or_create_user(user_info, db)
            
            # Store user info in session with database ID
            request.session['user'] = {
                'id': db_user.id,
                'email': user_info.get('email'),
                'name': user_info.get('name'),
                'picture': user_info.get('picture')
            }
            print(f"User logged in: {user_info.get('email')}")  # Debug log
            return RedirectResponse(url='/dashboard', status_code=303)
        else:
            print("No user info received from Google")
            return RedirectResponse(url='/?error=no_user_info', status_code=303)
            
    except Exception as e:
        print(f"Auth error: {e}")
        import traceback
        traceback.print_exc()
        return RedirectResponse(url=f'/?error=auth_failed&detail={str(e)}', status_code=303)

@app.get("/auth/logout")
async def logout(request: Request):
    """Logout user"""
    request.session.clear()
    return RedirectResponse(url='/', status_code=303)

@app.get("/api/user")
async def get_user(user: dict = Depends(get_current_user)):
    """Get current user info"""
    return user

@app.get("/api/debug/session")
async def debug_session(request: Request):
    """Debug endpoint to check session"""
    return {
        "has_session": bool(request.session),
        "session_data": dict(request.session) if request.session else {},
        "has_user": 'user' in request.session
    }

@app.get("/api/debug/oauth")
async def debug_oauth(request: Request):
    """Debug OAuth configuration"""
    redirect_uri = f"{request.url.scheme}://{request.url.netloc}/auth/callback"
    return {
        "current_url": str(request.url),
        "scheme": request.url.scheme,
        "netloc": request.url.netloc,
        "constructed_redirect_uri": redirect_uri,
        "google_client_id": os.getenv('GOOGLE_CLIENT_ID')[:10] + "..." if os.getenv('GOOGLE_CLIENT_ID') else None,
        "env_redirect_uri": os.getenv('GOOGLE_REDIRECT_URI'),
        "message": "The 'constructed_redirect_uri' above is what will be sent to Google. Make sure this EXACTLY matches what's in Google Cloud Console."
    }

# ============== JOB MANAGEMENT API ==============

@app.get("/api/jobs", response_model=List[schemas.JobWithApplicationCount])
async def list_jobs(
    status: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """List all jobs with optional filters"""
    query = select(models.Job)
    
    if status:
        query = query.where(models.Job.status == status)
    
    if search:
        query = query.where(
            models.Job.title.contains(search) | 
            models.Job.description.contains(search)
        )
    
    query = query.offset(skip).limit(limit).order_by(models.Job.created_at.desc())
    result = await db.execute(query)
    jobs = result.scalars().all()
    
    # Get application counts for each job
    jobs_with_counts = []
    for job in jobs:
        count_query = select(func.count(models.Application.id)).where(
            models.Application.job_id == job.id
        )
        count_result = await db.execute(count_query)
        count = count_result.scalar()
        
        job_dict = {
            **{c.name: getattr(job, c.name) for c in job.__table__.columns},
            "application_count": count
        }
        jobs_with_counts.append(schemas.JobWithApplicationCount(**job_dict))
    
    return jobs_with_counts

@app.post("/api/jobs", response_model=schemas.Job)
async def create_job(
    job: schemas.JobCreate,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Create a new job posting"""
    db_job = models.Job(
        **job.model_dump(),
        created_by=user['id']
    )
    db.add(db_job)
    await db.commit()
    await db.refresh(db_job)
    return db_job

@app.get("/api/jobs/{job_id}", response_model=schemas.Job)
async def get_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Get a specific job by ID"""
    result = await db.execute(
        select(models.Job).where(models.Job.id == job_id)
    )
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job

@app.put("/api/jobs/{job_id}", response_model=schemas.Job)
async def update_job(
    job_id: int,
    job_update: schemas.JobUpdate,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Update a job posting"""
    result = await db.execute(
        select(models.Job).where(models.Job.id == job_id)
    )
    db_job = result.scalar_one_or_none()
    
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Update only provided fields
    update_data = job_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_job, field, value)
    
    await db.commit()
    await db.refresh(db_job)
    return db_job

@app.delete("/api/jobs/{job_id}")
async def delete_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Delete a job posting"""
    result = await db.execute(
        select(models.Job).where(models.Job.id == job_id)
    )
    db_job = result.scalar_one_or_none()
    
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    await db.delete(db_job)
    await db.commit()
    return {"message": "Job deleted successfully"}

# ============== CANDIDATE MANAGEMENT API ==============

@app.get("/api/candidates", response_model=List[schemas.Candidate])
async def list_candidates(
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """List all candidates with optional search"""
    query = select(models.Candidate)
    
    if search:
        query = query.where(
            models.Candidate.name.contains(search) | 
            models.Candidate.email.contains(search) |
            models.Candidate.skills.contains(search)
        )
    
    query = query.offset(skip).limit(limit).order_by(models.Candidate.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()

@app.post("/api/candidates", response_model=schemas.Candidate)
async def create_candidate(
    candidate: schemas.CandidateCreate,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Add a new candidate"""
    # Check if candidate with email already exists
    result = await db.execute(
        select(models.Candidate).where(models.Candidate.email == candidate.email)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(status_code=400, detail="Candidate with this email already exists")
    
    db_candidate = models.Candidate(**candidate.model_dump())
    db.add(db_candidate)
    await db.commit()
    await db.refresh(db_candidate)
    return db_candidate

@app.get("/api/candidates/{candidate_id}", response_model=schemas.Candidate)
async def get_candidate(
    candidate_id: int,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Get a specific candidate by ID"""
    result = await db.execute(
        select(models.Candidate).where(models.Candidate.id == candidate_id)
    )
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    return candidate

@app.put("/api/candidates/{candidate_id}", response_model=schemas.Candidate)
async def update_candidate(
    candidate_id: int,
    candidate_update: schemas.CandidateUpdate,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Update a candidate"""
    result = await db.execute(
        select(models.Candidate).where(models.Candidate.id == candidate_id)
    )
    db_candidate = result.scalar_one_or_none()
    
    if not db_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Update only provided fields
    update_data = candidate_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_candidate, field, value)
    
    await db.commit()
    await db.refresh(db_candidate)
    return db_candidate

@app.delete("/api/candidates/{candidate_id}")
async def delete_candidate(
    candidate_id: int,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Delete a candidate"""
    result = await db.execute(
        select(models.Candidate).where(models.Candidate.id == candidate_id)
    )
    db_candidate = result.scalar_one_or_none()
    
    if not db_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    await db.delete(db_candidate)
    await db.commit()
    return {"message": "Candidate deleted successfully"}

# ============== APPLICATION TRACKING API ==============

@app.get("/api/applications", response_model=List[schemas.ApplicationWithDetails])
async def list_applications(
    job_id: Optional[int] = None,
    candidate_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """List all applications with optional filters"""
    query = select(models.Application)
    
    if job_id:
        query = query.where(models.Application.job_id == job_id)
    
    if candidate_id:
        query = query.where(models.Application.candidate_id == candidate_id)
    
    if status:
        query = query.where(models.Application.status == status)
    
    query = query.offset(skip).limit(limit).order_by(models.Application.applied_at.desc())
    result = await db.execute(query)
    applications = result.scalars().all()
    
    # Load related job and candidate data
    applications_with_details = []
    for app in applications:
        job_result = await db.execute(select(models.Job).where(models.Job.id == app.job_id))
        candidate_result = await db.execute(select(models.Candidate).where(models.Candidate.id == app.candidate_id))
        
        app_dict = {c.name: getattr(app, c.name) for c in app.__table__.columns}
        app_dict['job'] = job_result.scalar_one()
        app_dict['candidate'] = candidate_result.scalar_one()
        
        applications_with_details.append(schemas.ApplicationWithDetails(**app_dict))
    
    return applications_with_details

@app.post("/api/applications", response_model=schemas.Application)
async def create_application(
    application: schemas.ApplicationCreate,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Create a new job application"""
    # Check if application already exists
    result = await db.execute(
        select(models.Application).where(
            models.Application.job_id == application.job_id,
            models.Application.candidate_id == application.candidate_id
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(status_code=400, detail="Application already exists for this job and candidate")
    
    db_application = models.Application(**application.model_dump())
    db.add(db_application)
    await db.commit()
    await db.refresh(db_application)
    return db_application

@app.put("/api/applications/{application_id}", response_model=schemas.Application)
async def update_application(
    application_id: int,
    application_update: schemas.ApplicationUpdate,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Update an application (including status changes)"""
    result = await db.execute(
        select(models.Application).where(models.Application.id == application_id)
    )
    db_application = result.scalar_one_or_none()
    
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Track status changes
    old_status = db_application.status
    update_data = application_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_application, field, value)
    
    # Create status history if status changed
    if 'status' in update_data and old_status != update_data['status']:
        history = models.StatusHistory(
            application_id=application_id,
            old_status=old_status,
            new_status=update_data['status'],
            changed_by=user['id'],
            notes=application_update.notes
        )
        db.add(history)
    
    await db.commit()
    await db.refresh(db_application)
    return db_application

@app.get("/api/applications/{application_id}/history", response_model=List[schemas.StatusHistory])
async def get_application_history(
    application_id: int,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Get status history for an application"""
    result = await db.execute(
        select(models.StatusHistory)
        .where(models.StatusHistory.application_id == application_id)
        .order_by(models.StatusHistory.changed_at.desc())
    )
    return result.scalars().all()

# ============== DASHBOARD STATS API ==============

@app.get("/api/stats")
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Get dashboard statistics"""
    # Total jobs
    jobs_count = await db.execute(select(func.count(models.Job.id)))
    total_jobs = jobs_count.scalar()
    
    # Active jobs
    active_jobs_count = await db.execute(
        select(func.count(models.Job.id)).where(models.Job.status == models.JobStatus.ACTIVE)
    )
    active_jobs = active_jobs_count.scalar()
    
    # Total candidates
    candidates_count = await db.execute(select(func.count(models.Candidate.id)))
    total_candidates = candidates_count.scalar()
    
    # Total applications
    applications_count = await db.execute(select(func.count(models.Application.id)))
    total_applications = applications_count.scalar()
    
    # Applications by status
    status_counts = {}
    for status in models.ApplicationStatus:
        status_result = await db.execute(
            select(func.count(models.Application.id)).where(
                models.Application.status == status
            )
        )
        status_counts[status.value] = status_result.scalar()
    
    return {
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "total_candidates": total_candidates,
        "total_applications": total_applications,
        "applications_by_status": status_counts
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
