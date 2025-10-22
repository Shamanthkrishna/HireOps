#!/usr/bin/env python3
"""
Quick start script for HireOps application
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def main():
    print("🚀 Starting HireOps Application Setup...")
    
    # Check if we're in the right directory
    if not os.path.exists("app/main.py"):
        print("❌ Please run this script from the HireOps project root directory")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies. Please check the error above.")
        return False
    
    # Create and seed database
    if not run_command("python seed_data.py", "Setting up database and seed data"):
        print("❌ Failed to set up database. Please check the error above.")
        return False
    
    print("\n" + "="*60)
    print("🎉 HireOps setup completed successfully!")
    print("="*60)
    print("\n📝 Default Login Credentials:")
    print("👤 Admin: username='admin', password='admin123'")
    print("👤 Account Manager: username='john_am', password='password123'")
    print("👤 Recruiter: username='alice_recruiter', password='password123'")
    print("👤 Sales Person: username='bob_sales', password='password123'")
    print("\n🌐 Starting the application server...")
    print("📱 Access the application at: http://localhost:8000")
    print("⏹️  Press Ctrl+C to stop the server\n")
    
    # Start the server
    try:
        # Change to app directory and start uvicorn
        os.chdir("app")
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Thanks for using HireOps!")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        print("\n🔧 Manual start command:")
        print("cd app && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    main()
