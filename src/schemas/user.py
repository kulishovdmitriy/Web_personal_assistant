import uuid
from datetime import date
from pydantic import Field
from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    first_name: str
    last_name: str
    birthday: date


class UserCreate(schemas.BaseUserCreate):
    first_name: str = Field(..., min_length=3, max_length=50)
    last_name: str = Field(..., min_length=3, max_length=50)
    birthday: date


class UserUpdate(schemas.BaseUserUpdate):
    pass
