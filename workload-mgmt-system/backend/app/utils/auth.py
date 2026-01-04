"""
Authentication Schemas - Legacy/Alternative Auth Models

⚠️ NOTE: This file appears to be a legacy or alternative authentication schema.
The main authentication schemas are in app/schemas/auth.py.

This file defines Pydantic models for authentication requests and responses.
These schemas are used for data validation and API serialization.

STATUS: May be deprecated - check if this is still used in the codebase.
"""

from pydantic import BaseModel
from typing import Literal

class LoginRequest(BaseModel):
    """
    Schema for login request (alternative format).
    
    NOTE: This uses staff_id instead of username.
    The main auth system uses username-based login (see app/schemas/auth.py).
    
    Fields:
    - staff_id: Staff ID (integer)
    - password: Plain text password
    """
    staff_id: int
    password: str

class TokenResponse(BaseModel):
    """
    Schema for authentication token response.
    
    Returned after successful login, contains:
    - access_token: JWT token for authenticated requests
    - token_type: Token type (always "bearer" for JWT)
    """
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    """
    Schema for user information in API responses.
    
    Contains basic user information:
    - staff_id: User's staff ID
    - name: User's full name
    - role: User's role (ACADEMIC, ADMIN, or MANAGEMENT)
    """
    staff_id: int
    name: str
    role: Literal["ACADEMIC", "ADMIN", "MANAGEMENT"]
