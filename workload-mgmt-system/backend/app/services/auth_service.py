"""
Authentication Service - Business Logic for Login

This file handles the actual login logic:
1. Finding the user by username
2. Checking if account is active
3. Verifying the password
4. Creating a login token

Think of this as the "security guard" that checks IDs and issues visitor passes.
"""

from sqlalchemy.orm import Session
from app.models.staff import Staff
from app.utils.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import HTTPException, status


class AuthService:
    """
    Service class for authentication operations.
    This contains the business logic for logging in users.
    """

    @staticmethod
    def login(db: Session, username: str, password: str):
        """
        Authenticate staff member by username and return JWT token.
        
        WHAT THIS DOES: This is the core login function. It checks if a username and password
        are correct, and if so, creates a login token for the user.
        
        STEP-BY-STEP:
        1. Look up user by username in database
        2. Check if user exists (if not, login fails)
        3. Check if account is active (disabled accounts can't login)
        4. Check if password is set (some accounts might not have passwords yet)
        5. Verify the password matches (hash the typed password and compare)
        6. If all checks pass, create a login token
        7. Return the token and user info
        
        Args:
            db: Database session (connection to database)
            username: Username to authenticate (e.g., "sf1", "adm1")
            password: Plain text password (what user typed)
            
        Returns:
            Tuple of (access_token, staff_object) - the login pass and user info
            
        Raises:
            HTTPException: If authentication fails (wrong password, inactive account, etc.)
        """
        # STEP 1: Find staff member by username in the database
        # This is like looking someone up in a phone book
        staff = db.query(Staff).filter(
            Staff.username == username
        ).first()

        # STEP 2: Check if staff exists
        # If username doesn't exist, don't tell them that (security best practice)
        # Just say "invalid username or password" so hackers can't check if usernames exist
        if not staff:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        # STEP 3: Check if staff account is active
        # Inactive accounts are disabled and can't login
        # This is like checking if someone's membership is still valid
        if not staff.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )

        # STEP 4: Check if password hash exists
        # Some old accounts might not have passwords set yet
        # They need to contact admin to set a password
        if not staff.password_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Password not set. Please contact administrator."
            )

        # STEP 5: Verify password
        # Hash the password the user typed and compare it to the stored hash
        # This is like checking if a key fits a lock
        if not verify_password(password, staff.password_hash):
            # Wrong password - again, don't say "wrong password", say "invalid username or password"
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        # STEP 6: All checks passed! Create a login token
        # This token will be used for all future requests to prove they're logged in
        token = create_access_token(
            data={
                "sub": str(staff.staff_id),  # 'sub' is standard JWT claim for subject (user ID)
                "staff_id": staff.staff_id,  # User's ID
                "role": staff.role  # User's role (ACADEMIC, ADMIN, MANAGEMENT)
            }
        )

        # STEP 7: Return the token and staff info
        # The frontend will store this token and send it with every request
        return token, staff
