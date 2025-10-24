#!/usr/bin/env python3
"""
Simple test server to debug the authentication issue
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from pydantic import BaseModel

# Create FastAPI app
app = FastAPI(title="HireOps Test Server")

# Configure static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple test models
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    username: str
    email: str
    full_name: str
    role: str

# Test authentication endpoints
@app.post("/api/auth/login")
async def test_login(request: dict):
    """Test login endpoint - accepts both JSON and form data"""
    username = request.get("username")
    password = request.get("password")
    
    print(f"Login attempt: {username}")
    print(f"Request data: {request}")
    
    # Simple test authentication
    if username in ["admin", "admin@hireops.com"] and password == "admin123":
        return {"access_token": "test-token-123", "token_type": "bearer"}
    elif username in ["hr", "hr@hireops.com"] and password == "hr123":
        return {"access_token": "test-token-456", "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/auth/login-form")
async def test_login_form(username: str, password: str):
    """Test login endpoint for form data"""
    print(f"Form Login attempt: {username}")
    
    # Simple test authentication
    if username in ["admin", "admin@hireops.com"] and password == "admin123":
        return {"access_token": "test-token-123", "token_type": "bearer"}
    elif username in ["hr", "hr@hireops.com"] and password == "hr123":
        return {"access_token": "test-token-456", "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/auth/register")
async def test_register(user: dict):
    """Test registration endpoint"""
    print(f"Registration attempt: {user}")
    return UserResponse(
        username=user.get("username", "test"),
        email=user.get("email", "test@example.com"),
        full_name=user.get("full_name", "Test User"),
        role=user.get("role", "recruiter")
    )

@app.get("/api/auth/me")
async def test_me():
    """Test user info endpoint"""
    return UserResponse(
        username="admin",
        email="admin@hireops.com", 
        full_name="Admin User",
        role="admin"
    )

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/showcase", response_class=HTMLResponse)
async def showcase(request: Request):
    return templates.TemplateResponse("showcase.html", {"request": request})

@app.get("/test")
async def auth_test_page():
    """Serve authentication test page"""
    with open("test_auth.html", "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)

# Mock data endpoints for dashboard functionality
@app.get("/api/applications/")
async def get_applications(size: int = 100):
    """Mock applications endpoint"""
    return {
        "items": [
            {
                "id": 1,
                "candidate_name": "John Doe",
                "job_title": "Software Engineer",
                "status": "applied",
                "created_at": "2024-01-15T10:30:00Z",
                "email": "john.doe@email.com",
                "phone": "+1-555-0123"
            },
            {
                "id": 2,
                "candidate_name": "Jane Smith",
                "job_title": "Product Manager",
                "status": "screening",
                "created_at": "2024-01-14T09:15:00Z",
                "email": "jane.smith@email.com",
                "phone": "+1-555-0124"
            },
            {
                "id": 3,
                "candidate_name": "Mike Johnson",
                "job_title": "UX Designer",
                "status": "interview_scheduled",
                "created_at": "2024-01-13T14:20:00Z",
                "email": "mike.johnson@email.com",
                "phone": "+1-555-0125"
            },
            {
                "id": 4,
                "candidate_name": "Sarah Wilson",
                "job_title": "Data Scientist",
                "status": "interview_completed",
                "created_at": "2024-01-12T11:45:00Z",
                "email": "sarah.wilson@email.com",
                "phone": "+1-555-0126"
            },
            {
                "id": 5,
                "candidate_name": "David Brown",
                "job_title": "DevOps Engineer",
                "status": "offer_extended",
                "created_at": "2024-01-11T16:00:00Z",
                "email": "david.brown@email.com",
                "phone": "+1-555-0127"
            }
        ],
        "total": 5,
        "page": 1,
        "size": size
    }

@app.put("/api/applications/{application_id}/status")
async def update_application_status(application_id: int, request: dict):
    """Mock application status update endpoint"""
    return {"id": application_id, "status": request.get("status"), "message": "Status updated successfully"}

@app.get("/api/jobs/")
async def get_jobs(size: int = 20):
    """Mock jobs endpoint"""
    return {
        "items": [
            {"id": 1, "title": "Software Engineer", "department": "Engineering", "status": "open"},
            {"id": 2, "title": "Product Manager", "department": "Product", "status": "open"},
            {"id": 3, "title": "UX Designer", "department": "Design", "status": "open"},
            {"id": 4, "title": "Data Scientist", "department": "Data", "status": "open"},
            {"id": 5, "title": "DevOps Engineer", "department": "Engineering", "status": "open"}
        ],
        "total": 5
    }

@app.get("/api/candidates/")
async def get_candidates(size: int = 20):
    """Mock candidates endpoint"""
    return {
        "items": [
            {"id": 1, "name": "John Doe", "email": "john.doe@email.com", "status": "active"},
            {"id": 2, "name": "Jane Smith", "email": "jane.smith@email.com", "status": "active"},
            {"id": 3, "name": "Mike Johnson", "email": "mike.johnson@email.com", "status": "active"},
            {"id": 4, "name": "Sarah Wilson", "email": "sarah.wilson@email.com", "status": "active"},
            {"id": 5, "name": "David Brown", "email": "david.brown@email.com", "status": "active"}
        ],
        "total": 5
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Test server running"}

if __name__ == "__main__":
    import uvicorn
    print("🧪 Starting HireOps Test Server...")
    print("🌐 URL: http://127.0.0.1:8000")
    print("🔐 Test Login: admin / admin123")
    uvicorn.run(app, host="127.0.0.1", port=8000)