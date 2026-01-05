from pydantic import BaseModel
from typing import Literal

class LoginRequest(BaseModel):
    staff_id: int
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    staff_id: int
    name: str
    role: Literal["ACADEMIC", "ADMIN", "MANAGEMENT"]
