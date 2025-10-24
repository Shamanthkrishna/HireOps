#!/bin/bash

# HireOps Production Deployment Script
# This script sets up the production environment for HireOps

echo "🚀 Starting HireOps Production Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_status "Docker and Docker Compose are available ✓"

# Create production environment file if it doesn't exist
if [ ! -f .env.production ]; then
    print_warning "Production environment file not found. Creating from template..."
    cp .env.production.template .env.production 2>/dev/null || echo "Please create .env.production file manually"
fi

# Generate secure secrets if needed
print_status "Checking security configuration..."

# Generate JWT secret if not set
if grep -q "your-super-secret-jwt-key-change-this-in-production" .env.production; then
    JWT_SECRET=$(openssl rand -hex 32)
    sed -i "s/your-super-secret-jwt-key-change-this-in-production/$JWT_SECRET/" .env.production
    print_success "Generated secure JWT secret"
fi

# Generate database password if default is used
if grep -q "hireops_password" .env.production; then
    DB_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
    sed -i "s/hireops_password/$DB_PASSWORD/g" .env.production
    print_success "Generated secure database password"
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p ./data/postgres
mkdir -p ./data/redis
mkdir -p ./logs
mkdir -p ./ssl
chmod 755 ./data/postgres ./data/redis ./logs

print_success "Directories created"

# Build Docker images
print_status "Building Docker images..."
docker-compose build

if [ $? -eq 0 ]; then
    print_success "Docker images built successfully"
else
    print_error "Failed to build Docker images"
    exit 1
fi

# Start the services
print_status "Starting HireOps services..."
docker-compose up -d

if [ $? -eq 0 ]; then
    print_success "Services started successfully"
else
    print_error "Failed to start services"
    exit 1
fi

# Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    print_success "All services are running"
else
    print_error "Some services failed to start"
    docker-compose ps
    exit 1
fi

# Run database migrations
print_status "Running database migrations..."
docker-compose exec app alembic upgrade head

if [ $? -eq 0 ]; then
    print_success "Database migrations completed"
else
    print_warning "Database migrations may have failed. Check logs with: docker-compose logs app"
fi

# Create admin user if needed
print_status "Setting up admin user..."
docker-compose exec app python -c "
from app.database.database import SessionLocal, engine
from app.models.models import Base, User
from app.auth.auth_handler import get_password_hash
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Check if admin user exists
admin_user = db.query(User).filter(User.email == 'admin@hireops.com').first()

if not admin_user:
    admin_user = User(
        email='admin@hireops.com',
        first_name='Admin',
        last_name='User',
        role='admin',
        hashed_password=get_password_hash('admin123'),
        is_active=True
    )
    db.add(admin_user)
    db.commit()
    print('Admin user created: admin@hireops.com / admin123')
else:
    print('Admin user already exists')

db.close()
"

# Display deployment information
echo ""
echo "🎉 HireOps Deployment Complete!"
echo ""
echo "Access your application:"
echo "  🌐 Web Interface: http://localhost"
echo "  📚 API Documentation: http://localhost/docs"
echo "  🔧 Admin Panel: http://localhost/dashboard"
echo ""
echo "Default Admin Credentials:"
echo "  📧 Email: admin@hireops.com"
echo "  🔑 Password: admin123"
echo ""
echo "Useful Commands:"
echo "  📋 View logs: docker-compose logs -f"
echo "  🔄 Restart services: docker-compose restart"
echo "  🛑 Stop services: docker-compose down"
echo "  📊 View status: docker-compose ps"
echo ""
echo "Configuration Files:"
echo "  🔧 Environment: .env.production"
echo "  🐳 Docker: docker-compose.yml"
echo "  🌐 Nginx: nginx.conf"
echo ""
print_warning "IMPORTANT: Change the default admin password after first login!"
print_warning "IMPORTANT: Configure SSL certificates for production use!"
echo ""
print_success "Deployment completed successfully! 🎊"