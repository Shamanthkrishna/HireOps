# HireOps API Testing Guide

## 🚀 Quick Start

The HireOps API is now fully functional with comprehensive CRUD operations, authentication, and audit trails.

### Base URL
```
http://localhost:8000
```

### API Documentation
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Authentication Flow

### 1. Register a User (Admin/Initial Setup)
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@hireops.com",
    "password": "adminpassword123",
    "full_name": "System Administrator",
    "role": "admin"
  }'
```

### 2. Login to Get Token
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=adminpassword123"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Use Token for Authenticated Requests
Add the token to subsequent requests:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  "http://localhost:8000/api/jobs/"
```

## 📋 API Endpoints

### Authentication (`/api/auth`)
- `POST /register` - Register new user
- `POST /login` - User login
- `GET /me` - Get current user profile
- `PUT /me` - Update current user profile
- `POST /logout` - Logout (client-side)

### Jobs (`/api/jobs`)
- `GET /` - List jobs (with filtering & pagination)
- `POST /` - Create job (Recruiter+ required)
- `GET /{job_id}` - Get specific job
- `PUT /{job_id}` - Update job (Owner or Admin)
- `DELETE /{job_id}` - Delete job (soft delete)
- `GET /{job_id}/applications` - Get job applications

### Candidates (`/api/candidates`)
- `GET /` - List candidates (with filtering & pagination)
- `POST /` - Create candidate (Hiring team required)
- `GET /{candidate_id}` - Get specific candidate
- `PUT /{candidate_id}` - Update candidate
- `DELETE /{candidate_id}` - Delete candidate
- `POST /{candidate_id}/resume` - Upload resume file
- `GET /{candidate_id}/applications` - Get candidate applications

### Applications (`/api/applications`)
- `GET /` - List applications (with filtering & pagination)
- `POST /` - Create application (Hiring team required)
- `GET /{application_id}` - Get specific application
- `PUT /{application_id}` - Update application
- `DELETE /{application_id}` - Delete application
- `PUT /{application_id}/status` - Update application status
- `GET /{application_id}/history` - Get status change history

## 🔧 Testing Examples

### Create a Job
```bash
curl -X POST "http://localhost:8000/api/jobs/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Python Developer",
    "description": "We are looking for an experienced Python developer...",
    "requirements": "5+ years Python, FastAPI, SQLAlchemy",
    "location": "San Francisco, CA",
    "department": "Engineering",
    "employment_type": "Full-time",
    "experience_level": "Senior",
    "salary_min": 120000,
    "salary_max": 180000
  }'
```

### Create a Candidate
```bash
curl -X POST "http://localhost:8000/api/candidates/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@email.com",
    "phone": "+1-555-0123",
    "current_company": "Tech Corp",
    "current_position": "Python Developer",
    "experience_years": 6,
    "skills": "Python, FastAPI, PostgreSQL, React",
    "location": "San Francisco, CA"
  }'
```

### Create an Application
```bash
curl -X POST "http://localhost:8000/api/applications/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": 1,
    "candidate_id": 1,
    "source": "LinkedIn",
    "cover_letter": "I am very interested in this position..."
  }'
```

### Update Application Status
```bash
curl -X PUT "http://localhost:8000/api/applications/1/status" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "screening",
    "reason": "Initial screening passed",
    "notes": "Candidate looks promising"
  }'
```

## 📊 Query Parameters

### Jobs Filtering
- `page` - Page number (default: 1)
- `size` - Page size (default: 10, max: 100)
- `is_active` - Filter by active status (true/false)
- `department` - Filter by department
- `location` - Filter by location
- `search` - Search in title and description

### Applications Filtering
- `page` - Page number
- `size` - Page size
- `status` - Filter by application status
- `job_id` - Filter by specific job
- `candidate_id` - Filter by specific candidate
- `assigned_recruiter_id` - Filter by assigned recruiter
- `source` - Filter by application source

## 🔒 Role-Based Access Control

### Admin
- Full access to all operations
- Can manage users, jobs, candidates, and applications

### Recruiter
- Can create/edit jobs they own
- Can manage candidates and applications
- Can only see applications assigned to them

### Interviewer
- Read access to applications and candidates
- Can update interview feedback

### Hiring Manager
- Can create/edit jobs
- Can manage candidates and applications
- View team applications

## 📈 Status Workflow

Applications follow this status pipeline:

1. **Applied** → Initial application
2. **Screening** → Under review
3. **Interview Scheduled** → Interview arranged
4. **Interview Completed** → Interview done
5. **Offer Extended** → Job offer made
6. **Offer Accepted/Declined** → Final decision
7. **Rejected/Withdrawn** → Application closed

Each status change is tracked in the audit trail with:
- Previous status
- New status
- Changed by (user)
- Timestamp
- Reason and notes

## 🎯 Phase 2 Complete!

✅ **Authentication System** - JWT-based auth with role management
✅ **Job Management** - Full CRUD with filtering and pagination
✅ **Candidate Management** - Full CRUD with resume upload
✅ **Application Pipeline** - Complete workflow with audit trail
✅ **Status Transitions** - Business rules and history tracking
✅ **Role-Based Access** - Proper authorization controls
✅ **API Documentation** - Auto-generated OpenAPI docs
✅ **Error Handling** - Comprehensive error responses
✅ **Data Validation** - Pydantic schemas with validation

Ready for Phase 3 (Frontend Development) or Phase 4 (Advanced Features)!