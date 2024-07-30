from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse
from src.database.user_db import get_user_db

router = APIRouter(tags=["users"])


@router.get("/{username}")
async def request_email(username: str, response: Response, db: AsyncSession = Depends(get_user_db)):
    # TODO create tracing system
    print("***********************************************************")
    print(f"{username}, open Email and save is DataBase")
    print("***********************************************************")
    return FileResponse("src/static/open_email_check.png", media_type="image/png", content_disposition_type="inline")
