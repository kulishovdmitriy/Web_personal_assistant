from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.user_db import get_user_db
from src.repository.users import get_user_by_email, confirmed_email_task
from src.services.email import token_handler

router = APIRouter()


@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: AsyncSession = Depends(get_user_db)):
    email = await token_handler.get_email_from_token(token)
    user = await get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.is_verified:
        return {"message": "Your email is already confirmed"}
    await confirmed_email_task(email, db)
    return {"message": "Email confirmed"}
