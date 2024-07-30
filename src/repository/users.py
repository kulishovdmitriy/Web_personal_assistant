from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.user_db import get_user_db
from src.database.models import User


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_user_db)):
    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def update_token(user: User, token: str | None, db: AsyncSession):
    user.refresh_token = token
    await db.commit()


async def confirmed_email_task(email: str, db: AsyncSession) -> None:
    user = await get_user_by_email(email, db)
    user.is_verified = True
    await db.commit()
