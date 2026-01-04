"""
Authentication Guard - Protects Routes and Checks User Permissions

This file handles:
1. get_current_user - Extracts and validates login tokens from requests
2. require_role - Checks if user has the right role to access a route

Think of this as the "bouncer" at a club that:
- Checks your ID (login token) to see if you're allowed in
- Checks your membership level (role) to see if you can access VIP areas
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.utils.security import SECRET_KEY, ALGORITHM
from app.database import get_db
from app.models.staff import Staff
from typing import Optional

# HTTP Bearer token security scheme
# This tells FastAPI to look for tokens in the "Authorization: Bearer <token>" header
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Staff:
    """
    Extract and validate JWT token, return current staff user.
    
    WHAT THIS DOES: This function is used as a "dependency" in routes. When a user makes
    a request, this function automatically:
    1. Extracts the login token from the request header
    2. Validates the token (checks if it's real and not expired)
    3. Gets the user from the database
    4. Returns the user object
    
    USE CASE: Any route that needs to know "who is making this request?" uses this.
    For example, when viewing your own profile, we need to know who "you" are.
    
    EXAMPLE: User sends request with header "Authorization: Bearer <token>"
    This function extracts the token, validates it, and returns the Staff object.
    
    Args:
        credentials: HTTP Bearer token credentials (the token from the request header)
        db: Database session (connection to database)
        
    Returns:
        Staff object (the user making the request)
        
    Raises:
        HTTPException: If token is invalid, expired, or staff not found
    """
    # Create a standard error message for invalid credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # STEP 1: Extract token from credentials
        # The token is in the "Authorization: Bearer <token>" header
        token = credentials.credentials
        
        # STEP 2: Decode and validate the JWT token
        # This checks if the token is real, not expired, and signed with our secret key
        # If the token is fake or expired, this will raise an error
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # STEP 3: Get staff_id from token
        # The token contains the user's ID, which we stored when they logged in
        staff_id: Optional[int] = payload.get("staff_id")
        if staff_id is None:
            # Token doesn't have a staff_id - it's invalid
            raise credentials_exception
            
    except JWTError:
        # Token is invalid, expired, or tampered with
        raise credentials_exception
    
    # STEP 4: Get staff from database using the ID from the token
    # This confirms the user still exists and gets their current info
    staff = db.query(Staff).filter(Staff.staff_id == staff_id).first()
    if staff is None:
        # User ID in token doesn't exist in database (maybe user was deleted)
        raise credentials_exception
    
    # STEP 5: Check if staff account is still active
    # Even if token is valid, inactive accounts can't access anything
    if not staff.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # STEP 6: Return the staff object
    # Now the route knows who is making the request
    return staff


def require_role(*allowed_roles: str):
    """
    Dependency to check if current user has required role.
    
    WHAT THIS DOES: This function creates a "role checker" that ensures only users
    with specific roles can access a route. For example, only ADMIN users can access
    admin-only routes.
    
    USE CASE: 
    - Admin-only pages: require_role("ADMIN")
    - Admin or Management: require_role("ADMIN", "MANAGEMENT")
    - Academic staff only: require_role("ACADEMIC")
    
    EXAMPLE:
        @router.get("/admin-only")
        def admin_endpoint(user: Staff = Depends(require_role("ADMIN"))):
            # Only ADMIN users can reach this code
            # If ACADEMIC user tries, they get a 403 Forbidden error
            ...
    
    THINK OF IT LIKE: A VIP section at a club. Only people with VIP passes (the right role)
    can enter. Others get turned away at the door.
    
    Usage:
        @router.get("/admin-only")
        def admin_endpoint(user: Staff = Depends(require_role("ADMIN"))):
            ...
    """
    def role_checker(current_user: Staff = Depends(get_current_user)) -> Staff:
        """
        Inner function that actually checks the role.
        This gets called automatically when the route is accessed.
        """
        # Check if the user's role is in the list of allowed roles
        # For example, if allowed_roles = ["ADMIN"] and user.role = "ACADEMIC", access is denied
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {', '.join(allowed_roles)}"
            )
        # If role matches, return the user (they can access the route)
        return current_user
    
    return role_checker
