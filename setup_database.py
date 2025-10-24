#!/usr/bin/env python3
"""
Database initialization and setup script for HireOps
This script creates the database tables and adds a test admin user
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database.database import engine, SessionLocal, Base
from app.models.models import User
from app.auth.auth import get_password_hash

def create_tables():
    """Create all database tables"""
    print("🔧 Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def create_admin_user():
    """Create a default admin user for testing"""
    print("👤 Creating admin user...")
    
    db = SessionLocal()
    try:
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.email == "admin@hireops.com").first()
        if existing_admin:
            print("ℹ️  Admin user already exists")
            print(f"   Email: admin@hireops.com")
            print(f"   Username: {existing_admin.username}")
            return True
        
        # Create admin user
        admin_user = User(
            username="admin",
            email="admin@hireops.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            role="admin",
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Admin user created successfully!")
        print(f"   Email: admin@hireops.com")
        print(f"   Username: admin")
        print(f"   Password: admin123")
        print(f"   Role: admin")
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def create_sample_users():
    """Create sample users for testing"""
    print("👥 Creating sample users...")
    
    db = SessionLocal()
    sample_users = [
        {
            "username": "hr_manager",
            "email": "hr@hireops.com",
            "password": "hr123",
            "full_name": "HR Manager",
            "role": "hr"
        },
        {
            "username": "recruiter1",
            "email": "recruiter@hireops.com", 
            "password": "recruiter123",
            "full_name": "Sarah Recruiter",
            "role": "recruiter"
        },
        {
            "username": "interviewer1",
            "email": "interviewer@hireops.com",
            "password": "interviewer123", 
            "full_name": "John Interviewer",
            "role": "interviewer"
        }
    ]
    
    try:
        created_count = 0
        for user_data in sample_users:
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if existing_user:
                continue
            
            # Create user
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=get_password_hash(user_data["password"]),
                full_name=user_data["full_name"],
                role=user_data["role"],
                is_active=True
            )
            
            db.add(user)
            created_count += 1
        
        db.commit()
        
        if created_count > 0:
            print(f"✅ Created {created_count} sample users")
            print("   Sample accounts:")
            for user_data in sample_users:
                print(f"   - {user_data['email']} / {user_data['password']} ({user_data['role']})")
        else:
            print("ℹ️  Sample users already exist")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample users: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def verify_setup():
    """Verify the database setup"""
    print("🔍 Verifying database setup...")
    
    db = SessionLocal()
    try:
        # Count users
        user_count = db.query(User).count()
        admin_count = db.query(User).filter(User.role == "admin").count()
        
        print(f"   Total users: {user_count}")
        print(f"   Admin users: {admin_count}")
        
        if user_count > 0:
            print("✅ Database setup verified successfully!")
            return True
        else:
            print("❌ No users found in database")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying setup: {e}")
        return False
    finally:
        db.close()

def main():
    """Main setup function"""
    print("=" * 50)
    print("🚀 HireOps Database Setup")
    print("=" * 50)
    print()
    
    success = True
    
    # Create tables
    if not create_tables():
        success = False
    
    print()
    
    # Create admin user
    if not create_admin_user():
        success = False
    
    print()
    
    # Create sample users
    if not create_sample_users():
        success = False
    
    print()
    
    # Verify setup
    if not verify_setup():
        success = False
    
    print()
    print("=" * 50)
    
    if success:
        print("🎉 Database setup completed successfully!")
        print()
        print("Quick Login Credentials:")
        print("📧 Email: admin@hireops.com")
        print("🔑 Password: admin123")
        print()
        print("🌐 You can now start the server and login!")
    else:
        print("❌ Database setup encountered errors")
        print("Please check the error messages above")
    
    print("=" * 50)

if __name__ == "__main__":
    main()