@echo off
title HireOps - Starting Server...

echo.
echo ============================================
echo        🚀 HireOps Server Launcher 🚀
echo ============================================
echo.

:: Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo ❌ Virtual environment not found!
    echo Please make sure the virtual environment is set up correctly.
    echo.
    pause
    exit /b 1
)

:: Display startup information
echo 📦 Checking Python environment...
.\venv\Scripts\python.exe --version
echo.

echo 🔧 Starting HireOps development server...
echo ⏳ Please wait while the server initializes...
echo.

echo 📍 Server will be available at: http://127.0.0.1:8000
echo 📚 API Documentation: http://127.0.0.1:8000/docs
echo 🔧 Dashboard: http://127.0.0.1:8000/dashboard
echo.

:: Start the server in background and wait a moment
echo 🚀 Launching server...
start /min "" .\venv\Scripts\python.exe main.py

:: Wait for server to start
echo ⏳ Waiting for server to initialize...
timeout /t 8 /nobreak > nul

:: Open the application in default browser
echo 🌐 Opening HireOps in your browser...
start "" http://127.0.0.1:8000

:: Keep the window open to show server status
echo.
echo ============================================
echo            ✅ HireOps is Running!
echo ============================================
echo.
echo 🌐 Web Interface: http://127.0.0.1:8000
echo 📚 API Documentation: http://127.0.0.1:8000/docs
echo 🔧 Dashboard: http://127.0.0.1:8000/dashboard
echo.
echo 💡 Tips:
echo    - Keep this window open while using HireOps
echo    - Press Ctrl+C to stop the server
echo    - Close this window to exit
echo.
echo ============================================

:: Wait for user input to keep window open
echo Press any key to stop the server and exit...
pause > nul

:: Try to gracefully stop any Python processes (optional)
echo.
echo 🛑 Stopping HireOps server...
taskkill /f /im python.exe /fi "WINDOWTITLE eq HireOps*" > nul 2>&1

echo.
echo 👋 Thank you for using HireOps!
timeout /t 2 /nobreak > nul