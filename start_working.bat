@echo off
title HireOps - Recruitment Tracking System
color 0A

echo.
echo  ╔═══════════════════════════════════════════════════════════╗
echo  ║                🚀 STARTING HIREOPS 🚀                   ║
echo  ║            Recruitment Tracking System                    ║
echo  ╚═══════════════════════════════════════════════════════════╝
echo.

cd /d "D:\SKB\Courses\Adarsh Project\HireOps\app"

echo 📦 Checking FastAPI...
python -c "import fastapi; print('✅ FastAPI ready')" 2>nul
if errorlevel 1 (
    echo ❌ Installing FastAPI...
    pip install fastapi uvicorn[standard] --quiet
)

echo.
echo 🔍 Finding available port...
echo 🌐 Starting application...
echo.
echo ┌─────────────────────────────────────────────────────────┐
echo │  Once started, your application will be available at:  │
echo │                                                         │
echo │  http://localhost:8001 (or next available port)        │
echo │                                                         │
echo │  ⏹️  Press Ctrl+C to stop the server                   │
echo └─────────────────────────────────────────────────────────┘
echo.

python main_working.py

echo.
echo 👋 HireOps stopped. Press any key to exit...
pause >nul
