from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.database import get_database
from src.database.models import User

from src.schemas.user import UserSchema, UpdateUser


async def get_users(db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(User))
    users = result.scalar_one_or_none()
    return users


async def create_user(body: UserSchema, db: AsyncSession = Depends(get_database)):
    new_user = User(**body.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_user(user_id: int, body: UpdateUser, db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(User).filter_by(id=user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in body.dict().items():
        if value is not None:
            setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(user_id: int, db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(User).filter_by(id=user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return {
        "message": "User deleted"
    }
