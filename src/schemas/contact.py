from pydantic import BaseModel, Field, EmailStr
from datetime import date, datetime
from typing import Optional

from src.schemas.user import UserRead


class CreateContactSchema(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=50)
    last_name: str = Field(..., min_length=3, max_length=50)
    address: str = Field(..., min_length=10, max_length=250)
    number_phone: str = Field(..., min_length=10, max_length=15)
    email: EmailStr
    birthday: date


class UpdateContactSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    number_phone: Optional[str] = None
    email: Optional[EmailStr] = None
    birthday: Optional[date] = None


class ResponseContactSchema(BaseModel):
    first_name: str
    last_name: str
    address: str
    number_phone: str
    email: EmailStr
    birthday: date | None
    create_at: datetime | None
    user: UserRead | None

    class Config:
        from_attributes = True
