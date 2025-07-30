@echo off
echo ========================================
echo  Instagram DM Automation Tool
echo ========================================
echo.
echo Starting the application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Installing/updating dependencies...
pip install -r requirements.txt

REM Check if installation was successful
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.
echo Starting Instagram DM Automation Tool...
echo.
echo The web interface will be available at:
echo http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start the Flask server
python server.py

pause