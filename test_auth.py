#!/usr/bin/env python3
"""
Test authentication endpoints for HireOps
"""

import requests
import json

API_BASE = "http://127.0.0.1:8000"

def test_login():
    """Test login endpoint"""
    print("🔐 Testing login...")
    
    # Test admin login
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/api/auth/login", 
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"   Token type: {data.get('token_type')}")
            print(f"   Access token: {data.get('access_token')[:20]}...")
            return data.get('access_token')
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_user_info(token):
    """Test getting user info with token"""
    print("👤 Testing user info...")
    
    try:
        response = requests.get(
            f"{API_BASE}/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            user = response.json()
            print("✅ User info retrieved!")
            print(f"   Username: {user.get('username')}")
            print(f"   Email: {user.get('email')}")
            print(f"   Role: {user.get('role')}")
            print(f"   Active: {user.get('is_active')}")
            return True
        else:
            print(f"❌ User info failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ User info error: {e}")
        return False

def test_register():
    """Test registration endpoint"""
    print("📝 Testing registration...")
    
    new_user = {
        "username": "testuser",
        "email": "test@hireops.com",
        "password": "test123",
        "full_name": "Test User",
        "role": "recruiter"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/api/auth/register",
            json=new_user,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            user = response.json()
            print("✅ Registration successful!")
            print(f"   User ID: {user.get('id')}")
            print(f"   Username: {user.get('username')}")
            print(f"   Email: {user.get('email')}")
            return True
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False

def main():
    print("=" * 50)
    print("🧪 HireOps Authentication Test")
    print("=" * 50)
    print()
    
    # Test login
    token = test_login()
    print()
    
    if token:
        # Test user info
        test_user_info(token)
        print()
    
    # Test registration
    test_register()
    
    print()
    print("=" * 50)
    print("✅ Authentication tests completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()