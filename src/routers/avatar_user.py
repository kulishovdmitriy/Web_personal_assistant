import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.user_db import get_database
from src.database.models import User
from src.schemas.user import UserRead
from src.services.auth import current_active_user
from src.repository.users import update_avatar_url
from src.conf.config import settings

router = APIRouter(tags=["avatar"])

cloudinary.config(cloud_name=settings.CLOUDINARY_NAME, api_key=settings.CLOUDINARY_API_KEY,
                  api_secret=settings.CLOUDINARY_API_SECRET, secure=True)


@router.patch("/avatar", response_model=UserRead)
async def avatar_patch(file: UploadFile = File(), user: User = Depends(current_active_user),
                       db: AsyncSession = Depends(get_database)):
    print(user)
    public_id = f"Web_personal_assistant/{user.email}"
    resource = cloudinary.uploader.upload(file.file, public_id=public_id, owerite=True)
    resource_url = cloudinary.CloudinaryImage(public_id).build_url(width=250, heigth=250, crop="fill",
                                                                   version=resource.get("version"))
    print(resource_url)
    user = await update_avatar_url(user.email, resource_url, db)
    return user
