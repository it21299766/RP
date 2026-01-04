"""
Security Utilities - Password Hashing and Token Creation

This file handles:
1. Password hashing - converts plain text passwords into secure hashes
2. Password verification - checks if a password matches a stored hash
3. JWT token creation - creates login tokens that expire after 24 hours

Think of this as the "security guard" that protects user passwords and creates login passes.
"""

from datetime import datetime, timedelta
from typing import Optional, Union
from jose import jwt
import os
import bcrypt

# Get secret key from environment or use default (for development)
# This is like a master key used to sign all login tokens
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_THIS_SECRET_KEY_IN_PRODUCTION_USE_ENV_VAR")
ALGORITHM = "HS256"  # Algorithm used to sign tokens
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours - how long login tokens last


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt directly (bypassing passlib to avoid initialization issues).
    
    WHAT THIS DOES: Converts a plain text password (like "password123") into a secure hash
    (like "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqBWVHxkd0")
    This hash cannot be reversed to get the original password.
    
    WHY: We never store passwords in plain text. If someone steals our database,
    they can't see actual passwords, only these hashes.
    
    Args:
        password: Plain text password (will be truncated to 72 bytes if longer)
        
    Returns:
        Hashed password string
    """
    # Ensure password is a string (convert if it's not)
    if not isinstance(password, str):
        password = str(password)
    
    # Bcrypt has a 72-byte limit, truncate if necessary
    # This is a technical limitation - passwords longer than 72 bytes get cut off
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password = password_bytes[:72].decode('utf-8', errors='ignore')
    
    # Generate a random "salt" - this makes each hash unique even for the same password
    # Think of salt like adding random spices to make each hash different
    salt = bcrypt.gensalt()
    
    # Create the hash by combining password + salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash using bcrypt directly.
    
    WHAT THIS DOES: Checks if the password the user typed matches the stored hash.
    When a user logs in, we hash their typed password and compare it to the stored hash.
    
    EXAMPLE: User types "password123", we hash it and check if it matches the hash
    stored in the database. Returns True if they match, False otherwise.
    
    Args:
        plain_password: Plain text password to verify (what user typed)
        hashed_password: Hashed password from database (what we stored)
        
    Returns:
        True if password matches, False otherwise
    """
    if not isinstance(plain_password, str):
        plain_password = str(plain_password)
    
    # Truncate to 72 bytes if necessary (same limit as hashing)
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 72:
        plain_password = password_bytes[:72].decode('utf-8', errors='ignore')
    
    try:
        # Use bcrypt to check if the password matches the hash
        # This is like checking if a key fits a lock
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        # If anything goes wrong, assume password is wrong (fail securely)
        return False


def create_access_token(
    data: dict,
    expires_delta: Optional[Union[int, timedelta]] = None
) -> str:
    """
    Create a JWT access token.
    
    WHAT THIS DOES: Creates a "login pass" (JWT token) that proves a user is logged in.
    This token contains information like user ID and role, and expires after 24 hours.
    
    THINK OF IT LIKE: A concert ticket that:
    - Has your name and seat number (user info)
    - Expires after the show (24 hours)
    - Can't be faked because it's signed with a secret key
    
    When the user makes requests, they send this token to prove they're logged in.
    
    Args:
        data: Dictionary containing token claims (e.g., staff_id, role) - user information
        expires_delta: Optional expiration time in minutes or timedelta object.
                      If None, uses ACCESS_TOKEN_EXPIRE_MINUTES (24 hours).
        
    Returns:
        Encoded JWT token string (a long string like "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    """
    to_encode = data.copy()  # Copy user data to include in token
    
    # Set expiration time - when does this login pass expire?
    if expires_delta:
        # Custom expiration time provided
        if isinstance(expires_delta, int):
            expire = datetime.utcnow() + timedelta(minutes=expires_delta)
        else:
            expire = datetime.utcnow() + expires_delta
    else:
        # Use default: 24 hours from now
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add expiration time and "issued at" time to the token
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    
    # Sign and encode the token using our secret key
    # This creates a tamper-proof token that can't be modified
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
