from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date


class UserSchema(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=50)
    last_name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=16)
    birthday: date


class UpdateUser(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None


class ResponseUserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    birthday: date

    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"



