"""
Simple startup script for HireOps that handles dependencies
"""
import subprocess
import sys
import os

def run_command(command):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def main():
    print("🚀 HireOps Quick Setup")
    print("=" * 50)
    
    # First, try to install essential packages
    essential_packages = [
        "fastapi",
        "sqlmodel", 
        "uvicorn[standard]",
        "python-multipart",
        "jinja2",
        "starlette",
        "itsdangerous",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-dotenv",
        "email-validator"
    ]
    
    print("📦 Installing essential packages...")
    for package in essential_packages:
        print(f"Installing {package}...")
        if not run_command(f"pip install {package}"):
            print(f"❌ Failed to install {package}")
        else:
            print(f"✅ {package} installed")
    
    print("\n🗄️ Setting up database...")
    # Create database and tables
    try:
        # Simple database setup without complex imports
        import sqlite3
        
        # Create SQLite database
        conn = sqlite3.connect('hireops.db')
        cursor = conn.cursor()
        
        # Create basic tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                hashed_password TEXT NOT NULL,
                role TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                contact_person TEXT,
                email TEXT,
                phone TEXT,
                address TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ Database created successfully!")
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
    
    print("\n🌐 Starting application...")
    print("Visit: http://localhost:8000")
    print("Press Ctrl+C to stop")
    
    # Start the application
    try:
        os.chdir("app")
        subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped")
    except Exception as e:
        print(f"❌ Failed to start application: {e}")

if __name__ == "__main__":
    main()
