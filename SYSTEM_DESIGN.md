# HireOps - Recruitment Tracking System

## System Design Overview

### Database Schema

#### Core Tables:
1. **users** - User authentication and role management
2. **clients** - Client companies (A, B, C)
3. **requirements** - Job openings/requirements
4. **candidates** - Candidate information
5. **candidate_status_history** - Audit trail for status changes
6. **requirement_assignments** - AM to Recruiter assignments

#### Relationships:
- Users have roles: Business Head, Business Support, Sales Head, AM, Sales Person, Recruiter
- Requirements belong to clients and are assigned to recruiters by AMs
- Candidates are linked to requirements and have status progression
- All status changes are logged with timestamps and user info

### Tech Stack Implementation:
- **Backend**: FastAPI
- **Database**: SQLite (dev) → PostgreSQL (prod)
- **ORM**: SQLModel
- **Templates**: Jinja2 with Bootstrap 5
- **Authentication**: Session-based with bcrypt
- **Migrations**: Alembic
- **Testing**: pytest

### API Endpoints Structure:
- `/auth/` - Login/logout/register
- `/dashboard/` - Role-based dashboards
- `/requirements/` - CRUD operations
- `/candidates/` - CRUD operations with status management
- `/admin/` - User management
- `/api/` - Data import/export

### Security:
- Role-based access decorators
- CSRF protection
- Input validation with Pydantic
- Password hashing with bcrypt
