from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import sessionmanager
from src.database.models import User


async def get_database() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmanager.session() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_database)):
    yield SQLAlchemyUserDatabase(session, User)
