# HireOps - Recruitment Tracking System

A comprehensive web-based recruitment tracking system built with Python, FastAPI, and SQLModel.

## Features

- **Role-based Access Control**: Different access levels for Business Head, Account Managers, Recruiters, and Sales Persons
- **Requirement Management**: Create, track, and manage job requirements
- **Candidate Management**: Track candidates through various stages of the recruitment process
- **Audit Trail**: Complete history of status changes with timestamps and user tracking
- **Dashboard Analytics**: KPIs and metrics based on user roles
- **Modern UI**: Bootstrap-based responsive interface

## Tech Stack

- **Backend**: FastAPI
- **Database**: SQLModel (SQLite for development, PostgreSQL for production)
- **Templates**: Jinja2
- **Styling**: Bootstrap 5
- **Authentication**: Session-based with bcrypt password hashing
- **Migrations**: Alembic

## Project Structure

```
app/
├── main.py              # FastAPI application entry point
├── models.py            # Database models
├── schemas.py           # Pydantic schemas
├── crud.py              # Database operations
├── auth.py              # Authentication and authorization
├── database.py          # Database configuration
├── routes/              # API routes
│   ├── __init__.py
│   ├── auth.py          # Authentication routes
│   ├── dashboard.py     # Dashboard routes
│   ├── requirements.py  # Requirements management
│   ├── candidates.py    # Candidates management
│   └── admin.py         # Admin operations
├── templates/           # Jinja2 HTML templates
│   ├── base.html
│   ├── auth/
│   ├── dashboard/
│   ├── requirements/
│   ├── candidates/
│   └── admin/
└── static/              # CSS, JS, and other static files
```

## Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd HireOps
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your configuration
# For development, the default SQLite settings work fine
```

### 5. Initialize Database and Seed Data
```bash
# Run the seed script to create tables and initial data
python seed_data.py
```

### 6. Run the Application
```bash
# From the project root directory
cd app
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at: `http://localhost:8000`

## Default Login Credentials

After running the seed script, you can login with these accounts:

| Role | Username | Password | Description |
|------|----------|----------|-------------|
| Business Head | `admin` | `admin123` | Full system access |
| Account Manager | `john_am` | `password123` | Manage recruiters and requirements |
| Recruiter | `alice_recruiter` | `password123` | Manage assigned candidates |
| Sales Person | `bob_sales` | `password123` | Create requirements |
| Recruiter | `sarah_recruiter` | `password123` | Additional recruiter account |

## User Roles and Permissions

### Business Head
- Full access to all features
- User management
- System administration
- View all data and analytics

### Account Manager (AM)
- Assign requirements to recruiters
- View team performance
- Manage recruiter activities
- Access to reporting

### Recruiter
- Manage assigned candidates
- Update candidate status
- View assigned requirements
- Track recruitment progress

### Sales Person
- Create new requirements
- View requirements they created
- Monitor requirement status
- Limited candidate visibility

## Key Features Explained

### Requirement Lifecycle
1. **Created** by Sales Person
2. **Assigned** to Recruiter by AM
3. **In Progress** when recruiter starts working
4. **Closed** when positions are filled

### Candidate Status Flow
- Applied → Screened → Submitted → Interview Scheduled → Interviewed → Offered → Hired
- Can be marked as Rejected or Withdrawn at any stage

### Audit Trail
- Every status change is logged with:
  - Old and new status
  - User who made the change
  - Timestamp
  - Optional notes

### Dashboard Analytics
- Total and active requirements
- Candidate pipeline metrics
- Status breakdowns
- Role-specific KPIs

## Database Schema

### Core Tables
- `users` - User accounts and roles
- `clients` - Client companies
- `requirements` - Job requirements
- `candidates` - Candidate profiles
- `candidate_status_history` - Audit trail

### Key Relationships
- Requirements belong to clients and are assigned to recruiters
- Candidates are linked to requirements
- Status changes are tracked in history table

## Development

### Running in Development Mode
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations
```bash
# Initialize Alembic (already done)
alembic init migrations

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head
```

### Running Tests
```bash
pytest tests/
```

## Production Deployment

### 1. Update Environment Variables
```bash
# Set production database URL
DATABASE_URL=postgresql://user:password@localhost/hireops

# Set secure secret key
SECRET_KEY=your-secure-secret-key

# Disable debug mode
DEBUG=False
```

### 2. Install Production Dependencies
```bash
pip install gunicorn psycopg2-binary
```

### 3. Run with Gunicorn
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 4. Set up Reverse Proxy (Nginx)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## API Endpoints

### Authentication
- `GET /auth/login` - Login page
- `POST /auth/login` - Handle login
- `GET /auth/logout` - Logout
- `GET /auth/register` - Registration page

### Dashboard
- `GET /dashboard` - Main dashboard

### Requirements
- `GET /requirements` - List requirements
- `GET /requirements/create` - Create requirement form
- `POST /requirements/create` - Handle creation
- `GET /requirements/{id}` - View requirement
- `GET /requirements/{id}/edit` - Edit form

### Candidates
- `GET /candidates` - List candidates
- `GET /candidates/create` - Create candidate form
- `POST /candidates/create` - Handle creation
- `GET /candidates/{id}` - View candidate details
- `GET /candidates/{id}/edit` - Edit form

### Admin
- `GET /admin/users` - User management
- `GET /admin/clients` - Client management

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check DATABASE_URL in .env file
   - Ensure database server is running

2. **Import Errors**
   - Activate virtual environment
   - Install all requirements: `pip install -r requirements.txt`

3. **Template Not Found**
   - Check template paths in routes
   - Ensure templates directory structure is correct

4. **Session Issues**
   - Check SECRET_KEY is set
   - Clear browser cookies

### Logs and Debugging

Enable detailed logging by setting DEBUG=True in .env file.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Add tests
5. Submit pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please contact the development team or create an issue in the repository.
