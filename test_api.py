"""
Simple test script to verify HireOps API functionality
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health Check: {response.status_code} - {response.json()}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Start with: py main.py")
        return False

def test_docs_endpoint():
    """Test if API docs are accessible"""
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"✅ API Docs accessible: Status {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ API Docs error: {e}")
        return False

def test_user_registration():
    """Test user registration"""
    try:
        user_data = {
            "username": "testuser",
            "email": "test@hireops.com",
            "password": "testpassword123",
            "full_name": "Test User",
            "role": "admin"
        }
        response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
        print(f"✅ User Registration: {response.status_code}")
        if response.status_code == 200:
            print(f"   User created: {response.json()['username']}")
        return response.status_code in [200, 400]  # 400 if user exists
    except Exception as e:
        print(f"❌ User Registration error: {e}")
        return False

def test_user_login():
    """Test user login"""
    try:
        login_data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        response = requests.post(
            f"{BASE_URL}/api/auth/login", 
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        print(f"✅ User Login: {response.status_code}")
        if response.status_code == 200:
            token = response.json()["access_token"]
            print(f"   Token received: {token[:50]}...")
            return token
        return None
    except Exception as e:
        print(f"❌ User Login error: {e}")
        return None

def test_authenticated_endpoint(token):
    """Test an authenticated endpoint"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
        print(f"✅ Authenticated Request: {response.status_code}")
        if response.status_code == 200:
            user = response.json()
            print(f"   Current user: {user['username']} ({user['role']})")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Authenticated Request error: {e}")
        return False

def run_tests():
    """Run all tests"""
    print("🚀 Testing HireOps API...")
    print(f"Base URL: {BASE_URL}")
    print("-" * 50)
    
    # Test basic connectivity
    if not test_health_endpoint():
        return
    
    # Test documentation
    test_docs_endpoint()
    
    # Test authentication flow
    test_user_registration()
    token = test_user_login()
    
    if token:
        test_authenticated_endpoint(token)
    
    print("-" * 50)
    print("🎯 Basic API tests completed!")
    print(f"📖 Visit {BASE_URL}/docs for interactive API documentation")

if __name__ == "__main__":
    run_tests()