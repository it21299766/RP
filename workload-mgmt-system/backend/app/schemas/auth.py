from pydantic import BaseModel
from typing import Literal, Optional


class LoginRequest(BaseModel):
    username: str  # Changed from staff_id to username
    password: str


class UserResponse(BaseModel):
    staff_id: int
    name: str
    role: Literal["ACADEMIC", "ADMIN", "MANAGEMENT"]
    department: Optional[str] = None

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

