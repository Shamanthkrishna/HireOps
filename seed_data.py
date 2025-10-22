"""
Seed script to populate the database with initial data
"""
from sqlmodel import Session, select
from app.database import engine, create_db_and_tables
from app.models import User, Client, Requirement, Candidate, UserRole, EmploymentMode, RequirementStatus, CandidateStatus
from app.auth import get_password_hash
from datetime import datetime

def create_seed_data():
    """Create initial seed data for the application"""
    
    # Create tables
    create_db_and_tables()
    
    with Session(engine) as session:
        # Create users
        users_data = [
            {
                "username": "admin",
                "email": "admin@hireops.com",
                "full_name": "System Administrator",
                "hashed_password": get_password_hash("admin123"),
                "role": UserRole.BUSINESS_HEAD
            },
            {
                "username": "john_am",
                "email": "john@hireops.com",
                "full_name": "John Smith",
                "hashed_password": get_password_hash("password123"),
                "role": UserRole.ACCOUNT_MANAGER
            },
            {
                "username": "alice_recruiter",
                "email": "alice@hireops.com",
                "full_name": "Alice Johnson",
                "hashed_password": get_password_hash("password123"),
                "role": UserRole.RECRUITER
            },
            {
                "username": "bob_sales",
                "email": "bob@hireops.com",
                "full_name": "Bob Wilson",
                "hashed_password": get_password_hash("password123"),
                "role": UserRole.SALES_PERSON
            },
            {
                "username": "sarah_recruiter",
                "email": "sarah@hireops.com",
                "full_name": "Sarah Davis",
                "hashed_password": get_password_hash("password123"),
                "role": UserRole.RECRUITER
            }
        ]
        
        for user_data in users_data:
            user = User(**user_data)
            session.add(user)
        
        session.commit()
        
        # Create clients
        clients_data = [
            {
                "name": "Tech Corp A",
                "contact_person": "Mike Johnson",
                "email": "mike@techcorpa.com",
                "phone": "+1-555-0101",
                "address": "123 Tech Street, Silicon Valley, CA"
            },
            {
                "name": "Innovation Inc B",
                "contact_person": "Lisa Chen",
                "email": "lisa@innovationb.com",
                "phone": "+1-555-0102",
                "address": "456 Innovation Ave, Austin, TX"
            },
            {
                "name": "StartupCo C",
                "contact_person": "David Brown",
                "email": "david@startupc.com",
                "phone": "+1-555-0103",
                "address": "789 Startup Blvd, New York, NY"
            }
        ]
        
        for client_data in clients_data:
            client = Client(**client_data)
            session.add(client)
        
        session.commit()
        
        # Get created users and clients for requirements
        admin_user = session.exec(select(User).where(User.username == "admin")).first()
        sales_user = session.exec(select(User).where(User.username == "bob_sales")).first()
        recruiter_user = session.exec(select(User).where(User.username == "alice_recruiter")).first()
        
        client_a = session.exec(select(Client).where(Client.name == "Tech Corp A")).first()
        client_b = session.exec(select(Client).where(Client.name == "Innovation Inc B")).first()
        
        # Create requirements
        requirements_data = [
            {
                "req_id": "REQ-2024-001",
                "client_id": client_a.id,
                "title": "Senior Python Developer",
                "description": "Looking for an experienced Python developer with Django/FastAPI experience",
                "experience_required": "5-8 years",
                "skills_required": "Python, Django, FastAPI, PostgreSQL, AWS",
                "budget_min": 80000.0,
                "budget_max": 120000.0,
                "location": "San Francisco, CA",
                "employment_mode": EmploymentMode.PERMANENT,
                "priority": "high",
                "status": RequirementStatus.ASSIGNED,
                "positions_count": 2,
                "created_by": sales_user.id,
                "assigned_to": recruiter_user.id,
                "notes": "Urgent requirement for new project"
            },
            {
                "req_id": "REQ-2024-002",
                "client_id": client_b.id,
                "title": "Frontend React Developer",
                "description": "React.js developer for building modern web applications",
                "experience_required": "3-5 years",
                "skills_required": "React.js, TypeScript, Next.js, Tailwind CSS",
                "budget_min": 60000.0,
                "budget_max": 90000.0,
                "location": "Austin, TX",
                "employment_mode": EmploymentMode.CONTRACT,
                "priority": "medium",
                "status": RequirementStatus.OPEN,
                "positions_count": 1,
                "created_by": sales_user.id,
                "notes": "6-month contract with possible extension"
            },
            {
                "req_id": "REQ-2024-003",
                "client_id": client_a.id,
                "title": "DevOps Engineer",
                "description": "DevOps engineer for cloud infrastructure management",
                "experience_required": "4-7 years",
                "skills_required": "AWS, Docker, Kubernetes, Terraform, Jenkins",
                "budget_min": 90000.0,
                "budget_max": 130000.0,
                "location": "Remote",
                "employment_mode": EmploymentMode.PERMANENT,
                "priority": "high",
                "status": RequirementStatus.IN_PROGRESS,
                "positions_count": 1,
                "created_by": sales_user.id,
                "assigned_to": recruiter_user.id,
                "notes": "Remote work allowed"
            }
        ]
        
        for req_data in requirements_data:
            requirement = Requirement(**req_data)
            session.add(requirement)
        
        session.commit()
        
        # Get requirements for candidates
        python_req = session.exec(select(Requirement).where(Requirement.req_id == "REQ-2024-001")).first()
        react_req = session.exec(select(Requirement).where(Requirement.req_id == "REQ-2024-002")).first()
        devops_req = session.exec(select(Requirement).where(Requirement.req_id == "REQ-2024-003")).first()
        
        # Create candidates
        candidates_data = [
            {
                "requirement_id": python_req.id,
                "name": "Emily Rodriguez",
                "email": "emily.rodriguez@email.com",
                "phone": "+1-555-1001",
                "current_company": "Tech Solutions Inc",
                "current_designation": "Senior Python Developer",
                "experience_years": 6.5,
                "current_ctc": 95000.0,
                "expected_ctc": 110000.0,
                "notice_period": "2 months",
                "location": "San Francisco, CA",
                "skills": "Python, Django, REST APIs, PostgreSQL, Redis",
                "status": CandidateStatus.INTERVIEWED,
                "notes": "Strong technical skills, good cultural fit"
            },
            {
                "requirement_id": python_req.id,
                "name": "Michael Chen",
                "email": "michael.chen@email.com",
                "phone": "+1-555-1002",
                "current_company": "DataCorp",
                "current_designation": "Python Developer",
                "experience_years": 5.0,
                "current_ctc": 85000.0,
                "expected_ctc": 100000.0,
                "notice_period": "1 month",
                "location": "San Jose, CA",
                "skills": "Python, FastAPI, MongoDB, Docker",
                "status": CandidateStatus.SUBMITTED,
                "notes": "FastAPI experience is excellent"
            },
            {
                "requirement_id": react_req.id,
                "name": "Jessica Williams",
                "email": "jessica.williams@email.com",
                "phone": "+1-555-1003",
                "current_company": "WebDev Studios",
                "current_designation": "Frontend Developer",
                "experience_years": 4.0,
                "current_ctc": 70000.0,
                "expected_ctc": 80000.0,
                "notice_period": "1 month",
                "location": "Austin, TX",
                "skills": "React.js, TypeScript, Next.js, Material-UI",
                "status": CandidateStatus.OFFERED,
                "notes": "Excellent React skills, ready to join"
            },
            {
                "requirement_id": devops_req.id,
                "name": "Robert Kumar",
                "email": "robert.kumar@email.com",
                "phone": "+1-555-1004",
                "current_company": "CloudTech",
                "current_designation": "DevOps Engineer",
                "experience_years": 6.0,
                "current_ctc": 105000.0,
                "expected_ctc": 120000.0,
                "notice_period": "2 months",
                "location": "Remote",
                "skills": "AWS, Kubernetes, Terraform, Jenkins, Python",
                "status": CandidateStatus.HIRED,
                "notes": "Hired! Excellent DevOps expertise"
            }
        ]
        
        for cand_data in candidates_data:
            candidate = Candidate(**cand_data)
            session.add(candidate)
        
        session.commit()
        
        print("✅ Seed data created successfully!")
        print("\n📝 Default Login Credentials:")
        print("👤 Admin: username='admin', password='admin123'")
        print("👤 Account Manager: username='john_am', password='password123'")
        print("👤 Recruiter: username='alice_recruiter', password='password123'")
        print("👤 Sales Person: username='bob_sales', password='password123'")
        print("👤 Recruiter 2: username='sarah_recruiter', password='password123'")

if __name__ == "__main__":
    create_seed_data()
