@echo off
title HireOps - Debug Mode

echo.
echo 🧪 HireOps Debug Mode Launcher
echo ================================
echo.

echo Starting test server with simplified authentication...
echo.

echo 🔐 Test Credentials:
echo    Username: admin
echo    Password: admin123
echo.
echo    OR
echo.
echo    Username: hr  
echo    Password: hr123
echo.

echo 🚀 Starting server...
start /min "" .\venv\Scripts\python.exe test_server.py

echo ⏳ Waiting for server to start...
timeout /t 5 /nobreak > nul

echo 🌐 Opening in browser...
start "" http://127.0.0.1:8000

echo.
echo ✅ HireOps Debug Mode is running!
echo.
echo 💡 This debug version has simplified authentication
echo    that should work without database issues.
echo.
echo Press any key to close...
pause >nul