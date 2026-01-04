"""
Authentication Routes - Login and User Info Endpoints

This file handles:
1. Login endpoint - where users sign in with username and password
2. Get current user endpoint - returns info about the logged-in user

Think of this as the "front desk" where people check in and get their visitor badge.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, TokenResponse, UserResponse
from app.services.auth_service import AuthService
from app.database import get_db
from app.utils.auth_guard import get_current_user
from app.models.staff import Staff

# Create a router for all authentication-related endpoints
# All routes here will start with "/api/auth"
router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate staff member and return JWT token.
    
    WHAT THIS DOES: This is the login endpoint. When a user enters their username and password,
    this function checks if they're correct and gives them a login token if successful.
    
    FLOW:
    1. User sends username and password
    2. We check if username exists in database
    3. We verify the password matches
    4. If correct, we create a login token and return it
    5. If wrong, we return an error
    
    EXAMPLE REQUEST:
    POST /api/auth/login
    {
        "username": "sf1",
        "password": "sf1"
    }
    
    EXAMPLE RESPONSE:
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer",
        "user": {
            "staff_id": 1,
            "name": "Dr. John Smith",
            "role": "ACADEMIC",
            "department": "Computer Science"
        }
    }
    
    Args:
        payload: LoginRequest with username and password (what user typed)
        db: Database session (connection to database)
        
    Returns:
        TokenResponse with access_token and user info (the login pass and user details)
    """
    try:
        # Call the login service to check username and password
        # This returns a token and staff info if login is successful
        token, staff = AuthService.login(db, payload.username, payload.password)
        
        # Return the token and user information
        return TokenResponse(
            access_token=token,  # The login pass they'll use for future requests
            token_type="bearer",  # Type of token (standard format)
            user=UserResponse(
                staff_id=staff.staff_id,
                name=staff.name,
                role=staff.role,  # ACADEMIC, ADMIN, or MANAGEMENT
                department=staff.department
            )
        )
    except HTTPException:
        # If login failed (wrong password, etc.), re-raise the error
        # This is already formatted nicely by the service
        raise
    except Exception as e:
        # Catch any unexpected errors (database issues, etc.)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: Staff = Depends(get_current_user)):
    """
    Get current authenticated user information.
    
    WHAT THIS DOES: Returns information about the currently logged-in user.
    The user must send their login token with the request to prove they're logged in.
    
    USE CASE: When the frontend needs to know "who am I?" or "what's my role?",
    it calls this endpoint with the login token.
    
    EXAMPLE REQUEST:
    GET /api/auth/me
    Headers: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    
    EXAMPLE RESPONSE:
    {
        "staff_id": 1,
        "name": "Dr. John Smith",
        "role": "ACADEMIC",
        "department": "Computer Science"
    }
    
    Returns:
        UserResponse with current user's information (who they are and their role)
    """
    # The get_current_user dependency automatically:
    # 1. Extracts the token from the request
    # 2. Validates it
    # 3. Gets the user from database
    # 4. Returns the Staff object
    
    # Just return the user's information
    return UserResponse(
        staff_id=current_user.staff_id,
        name=current_user.name,
        role=current_user.role,  # Used to determine what they can access
        department=current_user.department
    )
