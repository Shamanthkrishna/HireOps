"""
Simple test to check if the imports work correctly
"""
def test_imports():
    try:
        print("Testing imports...")
        
        # Test SQLModel imports
        from sqlmodel import SQLModel, Session, create_engine, select
        print("✅ SQLModel imports successful")
        
        # Test FastAPI imports
        from fastapi import FastAPI, Request, Depends
        from starlette.middleware.sessions import SessionMiddleware
        print("✅ FastAPI imports successful")
        
        # Test app imports
        from app.models import User, UserRole
        from app.auth import get_password_hash
        print("✅ App imports successful")
        
        print("🎉 All imports working correctly!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    test_imports()
