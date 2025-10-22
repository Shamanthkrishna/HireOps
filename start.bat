@echo off
ececho � Installing core packages...
pip install fastapi uvicorn[standard]

echo 🌐 Starting basic application...
echo Visit: http://localhost:8000
echo.
cd app
python main_simple.py Starting HireOps Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo 📦 Installing required packages...
pip install fastapi sqlmodel uvicorn[standard] python-multipart jinja2 starlette itsdangerous python-jose[cryptography] passlib[bcrypt] python-dotenv email-validator

echo �️ Setting up database...
python quick_start.py

pause
