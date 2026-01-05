"""
Main Application File - FastAPI Application Setup

This is the "main entry point" of the backend application. It:
1. Creates the FastAPI application
2. Sets up CORS (allows frontend to connect)
3. Registers all API routes (login, staff, tasks, etc.)
4. Initializes the database when the app starts

Think of this as the "reception desk" that directs requests to the right departments.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import init_db
from app.routes import staff
from app.routes import task
from app.routes import task_template
from app.routes import task_instance
from app.routes import domain
from app.routes import program
from app.routes import assignment
from app.routes import change_request
from app.routes import module
from app.routes import module_section
from app.routes import program_section
from app.routes import tariff
from app.routes import optimization
from app.routes import reports
from app.routes import dashboard
from app.routes import workload
from app.routes import auth

# Create the FastAPI application
# This is the main "app" object that handles all HTTP requests
app = FastAPI(title="University WAM API")

# CORS: allow React dev server
# CORS = Cross-Origin Resource Sharing
# This allows the frontend (running on localhost:3000) to make requests to this backend
# Without this, browsers would block requests from the frontend
from starlette.middleware.cors import CORSMiddleware
origins = ["http://localhost:3000"]  # Frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Which websites can make requests
    allow_credentials=True,  # Allow cookies/auth tokens
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers (including Authorization for tokens)
)

# Mount static files directory for serving uploaded files (profile pictures)
# This allows the frontend to access uploaded files via URL
# Example: http://localhost:8000/uploads/profiles/staff_7.jpg
import os
from pathlib import Path

# Create uploads directory structure if it doesn't exist
# Determine the base directory (backend/) - go up from app/ to backend/
# __file__ is backend/app/main.py, so parent.parent gets backend/
base_dir = Path(__file__).parent.parent  # backend/
uploads_dir = base_dir / "uploads"  # backend/uploads

# Create directory structure if it doesn't exist
uploads_dir.mkdir(parents=True, exist_ok=True)
(uploads_dir / "profiles").mkdir(parents=True, exist_ok=True)

# Mount the uploads directory for serving files (use absolute path)
app.mount("/uploads", StaticFiles(directory=str(uploads_dir.resolve())), name="uploads")

# Include routers - Register all API endpoints
# Each router handles a different part of the system:
app.include_router(auth.router)  # Login, logout, get current user
app.include_router(staff.router)  # Staff management (CRUD operations)
app.include_router(task.router)  # Legacy task routes - kept for backward compatibility
app.include_router(task_template.router)  # Task templates (reusable task definitions)
app.include_router(task_instance.router)  # Task instances (specific tasks for a semester)
app.include_router(domain.router)  # Academic domains (Computing, Engineering, etc.)
app.include_router(program.router)  # Academic programs (BSCS, BSSE, etc.)
app.include_router(assignment.router)  # Task assignments (who teaches what)
app.include_router(change_request.router)  # Change requests (staff requesting changes)
app.include_router(module.router)  # Course modules
app.include_router(module_section.router)  # Module sections
app.include_router(program_section.router)  # Program sections (Section A, B, C, etc.)
app.include_router(tariff.router)  # Tariffs (how many hours each task type takes)
app.include_router(optimization.router)  # Workload optimization (GA algorithm)
app.include_router(reports.router)  # Reports and analytics
app.include_router(dashboard.router)  # Dashboard metrics and statistics
app.include_router(workload.router)  # My Workload (assignments for current user)


@app.on_event("startup")
def startup():
    """
    This function runs when the application starts up.
    
    WHAT IT DOES: Initializes the database - creates all tables if they don't exist.
    This ensures the database is ready when the server starts.
    
    THINK OF IT LIKE: Setting up the office before employees arrive - making sure
    all the desks and equipment are in place.
    """
    init_db()  # Create database tables if they don't exist
