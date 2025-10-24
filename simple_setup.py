#!/usr/bin/env python3
"""
Simple database initialization script for HireOps
Creates tables and a basic admin user
"""

import sys
import os
import sqlite3
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_simple_user():
    """Create admin user directly in SQLite database"""
    print("🔧 Setting up database...")
    
    # Connect to SQLite database
    db_path = "hireops.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Create users table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                hashed_password VARCHAR(100) NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                role VARCHAR(20) NOT NULL DEFAULT 'recruiter',
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP
            )
        ''')
        
        # Check if admin user exists
        cursor.execute("SELECT * FROM users WHERE email = ?", ("admin@hireops.com",))
        existing_admin = cursor.fetchone()
        
        if existing_admin:
            print("ℹ️  Admin user already exists!")
            print("   Email: admin@hireops.com")
            print("   Username: admin")
            return True
        
        # Use simple password hash for now (in production, use proper bcrypt)
        import hashlib
        simple_password = "admin123"
        password_hash = hashlib.sha256(simple_password.encode()).hexdigest()
        
        # Insert admin user
        cursor.execute('''
            INSERT INTO users (username, email, hashed_password, full_name, role, is_active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            "admin",
            "admin@hireops.com", 
            password_hash,
            "Admin User",
            "admin",
            True,
            datetime.utcnow().isoformat()
        ))
        
        # Create sample HR user
        cursor.execute('''
            INSERT INTO users (username, email, hashed_password, full_name, role, is_active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            "hr_manager",
            "hr@hireops.com",
            hashlib.sha256("hr123".encode()).hexdigest(),
            "HR Manager", 
            "hr",
            True,
            datetime.utcnow().isoformat()
        ))
        
        conn.commit()
        
        print("✅ Database setup completed successfully!")
        print()
        print("Login Credentials:")
        print("📧 Email: admin@hireops.com")
        print("🔑 Password: admin123")
        print("🎯 Role: Admin")
        print()
        print("Alternative Login:")
        print("📧 Email: hr@hireops.com") 
        print("🔑 Password: hr123")
        print("🎯 Role: HR Manager")
        print()
        print("🌐 You can now start the server and login!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 HireOps Simple Database Setup")
    print("=" * 50)
    print()
    
    if create_simple_user():
        print("=" * 50)
        print("🎉 Setup Complete!")
    else:
        print("=" * 50)
        print("❌ Setup Failed!")
    
    print("=" * 50)