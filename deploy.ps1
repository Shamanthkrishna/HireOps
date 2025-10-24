# HireOps Production Deployment Script for Windows
# PowerShell version of deploy.sh

Write-Host "🚀 Starting HireOps Production Deployment..." -ForegroundColor Blue

function Write-Status {
    param($Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Success {
    param($Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param($Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param($Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Check if Docker is installed
if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker is not installed. Please install Docker Desktop for Windows first."
    Write-Host "Download from: https://docs.docker.com/desktop/install/windows-install/"
    exit 1
}

# Check if Docker Compose is available
if (!(Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Error "Docker Compose is not available. Please ensure Docker Desktop includes Docker Compose."
    exit 1
}

Write-Status "Docker and Docker Compose are available ✓"

# Create production environment file if it doesn't exist
if (!(Test-Path .env.production)) {
    Write-Warning "Production environment file not found. Using template..."
    if (Test-Path .env.production.template) {
        Copy-Item .env.production.template .env.production
    } else {
        Write-Warning "No template found. Please ensure .env.production exists."
    }
}

# Create necessary directories
Write-Status "Creating necessary directories..."
$directories = @("./data/postgres", "./data/redis", "./logs", "./ssl")
foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}
Write-Success "Directories created"

# Check if Docker is running
try {
    docker info | Out-Null
    Write-Status "Docker daemon is running ✓"
} catch {
    Write-Error "Docker daemon is not running. Please start Docker Desktop."
    exit 1
}

# Build Docker images
Write-Status "Building Docker images..."
try {
    docker-compose build
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Docker images built successfully"
    } else {
        throw "Build failed"
    }
} catch {
    Write-Error "Failed to build Docker images"
    exit 1
}

# Start the services
Write-Status "Starting HireOps services..."
try {
    docker-compose up -d
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Services started successfully"
    } else {
        throw "Service start failed"
    }
} catch {
    Write-Error "Failed to start services"
    exit 1
}

# Wait for services to be ready
Write-Status "Waiting for services to be ready..."
Start-Sleep -Seconds 15

# Check if services are running
$runningServices = docker-compose ps --services --filter "status=running"
if ($runningServices) {
    Write-Success "Services are running"
    docker-compose ps
} else {
    Write-Error "Some services failed to start"
    docker-compose ps
    exit 1
}

# Display deployment information
Write-Host ""
Write-Host "🎉 HireOps Deployment Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Access your application:" -ForegroundColor White
Write-Host "  🌐 Web Interface: http://localhost" -ForegroundColor Cyan
Write-Host "  📚 API Documentation: http://localhost/docs" -ForegroundColor Cyan
Write-Host "  🔧 Admin Panel: http://localhost/dashboard" -ForegroundColor Cyan
Write-Host ""
Write-Host "Default Admin Credentials:" -ForegroundColor White
Write-Host "  📧 Email: admin@hireops.com" -ForegroundColor Yellow
Write-Host "  🔑 Password: admin123" -ForegroundColor Yellow
Write-Host ""
Write-Host "Useful Commands:" -ForegroundColor White
Write-Host "  📋 View logs: docker-compose logs -f" -ForegroundColor Gray
Write-Host "  🔄 Restart services: docker-compose restart" -ForegroundColor Gray
Write-Host "  🛑 Stop services: docker-compose down" -ForegroundColor Gray
Write-Host "  📊 View status: docker-compose ps" -ForegroundColor Gray
Write-Host ""
Write-Host "Configuration Files:" -ForegroundColor White
Write-Host "  🔧 Environment: .env.production" -ForegroundColor Gray
Write-Host "  🐳 Docker: docker-compose.yml" -ForegroundColor Gray
Write-Host "  🌐 Nginx: nginx.conf" -ForegroundColor Gray
Write-Host ""
Write-Warning "IMPORTANT: Change the default admin password after first login!"
Write-Warning "IMPORTANT: Configure SSL certificates for production use!"
Write-Host ""
Write-Success "Deployment completed successfully! 🎊"