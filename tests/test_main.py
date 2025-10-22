"""
Basic tests for HireOps application
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

from app.main import app
from app.database import get_session
from app.models import User
from app.auth import get_password_hash

# Test database
TEST_DATABASE_URL = "sqlite://"
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

def get_test_session():
    with Session(test_engine) as session:
        yield session

# Override dependency
app.dependency_overrides[get_session] = get_test_session

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_health_check(client: TestClient):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_redirect(client: TestClient):
    """Test root endpoint redirects to login"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302
    assert "/auth/login" in response.headers["location"]

def test_login_page(client: TestClient):
    """Test login page loads"""
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert "Login to HireOps" in response.text

def test_register_page(client: TestClient):
    """Test register page loads"""
    response = client.get("/auth/register")
    assert response.status_code == 200
    assert "Register for HireOps" in response.text

def test_user_registration(client: TestClient, session: Session):
    """Test user registration"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpass123",
        "role": "recruiter"
    }
    
    response = client.post("/auth/register", data=user_data)
    assert response.status_code == 302  # Redirect after successful registration
    
    # Check user was created in database
    user = session.query(User).filter(User.username == "testuser").first()
    assert user is not None
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.role == "recruiter"

def test_user_login(client: TestClient, session: Session):
    """Test user login"""
    # Create a test user
    user = User(
        username="logintest",
        email="login@example.com",
        full_name="Login Test",
        hashed_password=get_password_hash("password123"),
        role="recruiter"
    )
    session.add(user)
    session.commit()
    
    # Test login
    login_data = {
        "username": "logintest",
        "password": "password123"
    }
    
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 302  # Redirect after successful login

def test_protected_route_without_login(client: TestClient):
    """Test protected route requires authentication"""
    response = client.get("/dashboard")
    assert response.status_code == 401  # Unauthorized

if __name__ == "__main__":
    pytest.main([__file__])
