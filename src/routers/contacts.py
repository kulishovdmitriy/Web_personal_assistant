from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_database
from src.database.models import User
from src.services.auth import auth_service
from src.schemas.contact import CreateContactSchema, UpdateContactSchema, ResponseContactSchema
from src.repository.contacts import get_all_contacts, post_create_contact, put_update_contact, delete_contact

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get("/all_contacts", response_model=ResponseContactSchema, status_code=status.HTTP_200_OK)
async def all_contacts(db: AsyncSession = Depends(get_database), user: User = Depends(auth_service.get_current_user)):
    return await get_all_contacts(db)


@router.post("/create_contact", response_model=ResponseContactSchema, status_code=status.HTTP_201_CREATED)
async def create_contact(body: CreateContactSchema, db: AsyncSession = Depends(get_database),
                         user: User = Depends(auth_service.get_current_user)):
    return await post_create_contact(body, db)


@router.put("update_contact/{id}", response_model=ResponseContactSchema, status_code=status.HTTP_200_OK)
async def update_contact(contact_id: int, body: UpdateContactSchema, db: AsyncSession = Depends(get_database),
                         user: User = Depends(auth_service.get_current_user)):
    return await put_update_contact(contact_id, body, db)


@router.delete("/delete_contact/{id}", response_model=ResponseContactSchema, status_code=status.HTTP_200_OK)
async def remove_contact(contact_id: int, db: AsyncSession = Depends(get_database),
                         user: User = Depends(auth_service.get_current_user)):
    await delete_contact(contact_id, db)
