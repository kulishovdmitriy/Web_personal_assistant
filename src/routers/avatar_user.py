from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.user_db import get_database
from src.database.models import User
from src.services.auth import current_active_user

router = APIRouter()


@router.patch("/avatar")
async def avatar_patch(file: UploadFile = File(), user: User = Depends(current_active_user),
                       db: AsyncSession = Depends(get_database)):

    return user
