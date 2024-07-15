from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_database
from src.repository.users import get_users, create_user, update_user, delete_user
from src.schemas.user import UserSchema, UpdateUser, ResponseUserSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/all_users", response_model=ResponseUserSchema, status_code=status.HTTP_200_OK)
async def all_users(db: AsyncSession = Depends(get_database)):
    return await get_users(db)


@router.post("/create_user", response_model=ResponseUserSchema, status_code=status.HTTP_201_CREATED)
async def user_post(body: UserSchema, db: AsyncSession = Depends(get_database)):
    return await create_user(body, db)


@router.put("/update_user/{id}", response_model=ResponseUserSchema, status_code=status.HTTP_202_ACCEPTED)
async def user_put(user_id: int, body: UpdateUser, db: AsyncSession = Depends(get_database)):
    return await update_user(user_id, body, db)


@router.delete("/delete_user/{id}", status_code=status.HTTP_202_ACCEPTED)
async def remove_user(user_id: int, db: AsyncSession = Depends(get_database)):
    return await delete_user(user_id, db)

