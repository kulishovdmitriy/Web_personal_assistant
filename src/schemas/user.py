
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from datetime import date

from src.database.models import Role


class UserSchema(BaseModel):
    username: str = Field(..., min_length=5, max_length=25)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=16)
    birthday: date


class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class ResponseUserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    birthday: date
    role: Role

    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
