@echo off
setlocal enabledelayedexpansion
title HireOps - Quick Launcher

:: Set colors for better visual experience
color 0B

echo.
echo  ██╗  ██╗██╗██████╗ ███████╗ ██████╗ ██████╗ ███████╗
echo  ██║  ██║██║██╔══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝
echo  ███████║██║██████╔╝█████╗  ██║   ██║██████╔╝███████╗
echo  ██╔══██║██║██╔══██╗██╔══╝  ██║   ██║██╔═══╝ ╚════██║
echo  ██║  ██║██║██║  ██║███████╗╚██████╔╝██║     ███████║
echo  ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝     ╚══════╝
echo.
echo            Modern Recruitment Tracking System
echo ================================================================
echo.

:: Check current directory
if not exist "main.py" (
    echo ❌ Error: main.py not found!
    echo Please run this script from the HireOps project directory.
    echo Current directory: %CD%
    echo.
    pause
    exit /b 1
)

:: Check virtual environment
if not exist "venv\Scripts\python.exe" (
    echo ❌ Error: Python virtual environment not found!
    echo.
    echo 🔧 Setting up virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment.
        echo Please ensure Python is installed and in PATH.
        pause
        exit /b 1
    )
    
    echo 📦 Installing dependencies...
    .\venv\Scripts\pip.exe install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies.
        pause
        exit /b 1
    )
)

:: Check if server is already running
netstat -an | findstr ":8000" >nul 2>&1
if not errorlevel 1 (
    echo ⚠️  Server appears to be already running on port 8000
    echo.
    echo 🌐 Opening existing server in browser...
    start "" http://127.0.0.1:8000
    echo.
    echo If you're having issues, please close any existing Python processes
    echo and run this launcher again.
    pause
    exit /b 0
)

:: Display system info
echo 🔍 System Check:
.\venv\Scripts\python.exe --version
echo    Virtual Environment: ✅ Ready
echo    Project Directory: %CD%
echo.

:: Create log directory if it doesn't exist
if not exist "logs" mkdir logs

:: Start server with logging
echo 🚀 Starting HireOps Server...
echo    Starting time: %DATE% %TIME%
echo    Server URL: http://127.0.0.1:8000
echo    Log file: logs\server.log
echo.

:: Start the server and capture its process ID
echo Starting server in new window...
start "HireOps Server" /min cmd /k ".\venv\Scripts\python.exe main.py 2>&1 | tee logs\server.log"

:: Wait for server to be ready
echo ⏳ Initializing server (this may take a few seconds)...
set /a counter=0
:wait_loop
timeout /t 1 /nobreak > nul
set /a counter+=1

:: Check if server is responding
powershell -Command "try { Invoke-WebRequest -Uri 'http://127.0.0.1:8000' -TimeoutSec 1 | Out-Null; exit 0 } catch { exit 1 }" >nul 2>&1
if not errorlevel 1 (
    goto server_ready
)

if !counter! geq 15 (
    echo.
    echo ⚠️  Server is taking longer than expected to start.
    echo    This might be normal for the first run.
    echo.
    echo 🌐 Attempting to open browser anyway...
    goto open_browser
)

goto wait_loop

:server_ready
echo ✅ Server is ready and responding!
echo.

:open_browser
:: Open in browser
echo 🌐 Opening HireOps in your default browser...
start "" http://127.0.0.1:8000

:: Display success information
echo.
echo ================================================================
echo                    ✅ HireOps is Running!
echo ================================================================
echo.
echo 🌐 Web Application:     http://127.0.0.1:8000
echo 📚 API Documentation:   http://127.0.0.1:8000/docs  
echo 🔧 Admin Dashboard:     http://127.0.0.1:8000/dashboard
echo 📊 Server Logs:        logs\server.log
echo.
echo 💡 Quick Tips:
echo    • First time? Click "Sign Up" to create your account
echo    • Check the dashboard for recruitment management
echo    • Visit /docs for complete API reference
echo    • Server logs are saved in the logs directory
echo.
echo 🛑 To stop the server:
echo    • Close the "HireOps Server" window, or
echo    • Press Ctrl+C in the server window
echo.
echo ================================================================

:: Keep this window open for instructions
echo.
echo Press any key to open additional HireOps resources...
pause >nul

:: Open additional helpful resources
echo.
echo 🔗 Opening additional resources...
echo    📚 Opening API Documentation...
start "" http://127.0.0.1:8000/docs

timeout /t 2 /nobreak > nul
echo    🔧 Opening Dashboard...
start "" http://127.0.0.1:8000/dashboard

echo.
echo 🎉 HireOps is ready for use!
echo.
echo This window can be safely closed.
echo The server will continue running in its own window.
echo.
pause