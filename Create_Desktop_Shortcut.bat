@echo off
title Create HireOps Desktop Shortcut

echo.
echo 🔗 HireOps Desktop Shortcut Creator
echo ===================================
echo.

:: Get current directory
set "CURRENT_DIR=%CD%"
set "DESKTOP=%USERPROFILE%\Desktop"

:: Create shortcut using PowerShell
echo Creating desktop shortcut...

powershell -Command ^
"$WshShell = New-Object -comObject WScript.Shell; ^
$Shortcut = $WshShell.CreateShortcut('%DESKTOP%\HireOps.lnk'); ^
$Shortcut.TargetPath = '%CURRENT_DIR%\🚀_Launch_HireOps.bat'; ^
$Shortcut.WorkingDirectory = '%CURRENT_DIR%'; ^
$Shortcut.Description = 'HireOps - Modern Recruitment Tracking System'; ^
$Shortcut.Save()"

if exist "%DESKTOP%\HireOps.lnk" (
    echo ✅ Desktop shortcut created successfully!
    echo.
    echo You can now launch HireOps by:
    echo   • Double-clicking the "HireOps" icon on your desktop
    echo   • Or running any of the batch files in this directory
    echo.
) else (
    echo ❌ Failed to create desktop shortcut.
    echo You can still run HireOps using the batch files in this directory.
    echo.
)

echo Press any key to close...
pause >nul