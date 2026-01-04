@echo off
REM Backend Startup Script for Windows
REM This script runs database migrations and starts the FastAPI backend server

echo ============================================
echo   WAM Backend Startup Script
echo ============================================
echo.

REM Change to script directory (backend/)
cd /d "%~dp0"

REM Check if .env file exists
if not exist .env (
    echo [ERROR] .env file not found!
    echo Please create a .env file in the backend directory.
    echo Copy .env.example to .env and update with your database credentials.
    echo.
    pause
    exit /b 1
)

echo [INFO] .env file found
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python and try again.
    echo.
    pause
    exit /b 1
)

echo [INFO] Python found
python --version
echo.

REM Check if virtual environment exists (optional check)
if exist venv (
    echo [INFO] Virtual environment detected
    echo [INFO] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [WARNING] Virtual environment not found..creating one
    call python -m venv venv
    call venv\Scripts\activate.bat
    call pip install -r requirements.txt
    call pip install python-multipart
    echo [INFO] Virtual environment created and dependencies installed
    echo.
)

REM Check if required packages are installed
echo [INFO] Checking dependencies...
python -c "import fastapi, uvicorn, sqlalchemy, pymysql" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Required packages are not installed
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

echo [INFO] Dependencies check passed
echo.


REM Step 2: Start the FastAPI server
echo ============================================
echo   Step 2: Starting FastAPI Backend Server
echo ============================================
echo.

echo [INFO] Starting uvicorn server...
echo [INFO] Server will be available at: http://localhost:8000
echo [INFO] API documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start uvicorn server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start server
    echo Check if uvicorn is installed: pip install uvicorn
    pause
    exit /b 1
)
