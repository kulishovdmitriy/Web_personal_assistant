from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.models import Contact
from src.database.database import get_database
from src.schemas.contact import CreateContactSchema, UpdateContactSchema


async def get_all_contacts(db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Contact))
    all_contacts = result.scalar_one_or_none()
    if all_contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return all_contacts


async def post_create_contact(body: CreateContactSchema, db: AsyncSession = Depends(get_database)):
    now_contact = Contact(**body.model_dump())
    db.add(now_contact)
    await db.commit()
    await db.refresh(now_contact)
    return now_contact


async def put_update_contact(contact_id: int,body: UpdateContactSchema, db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Contact).filter_by(id=contact_id))
    contact = result.scalar_one_or_none()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    for key, value in body.dict().items():
        if value is not None:
            setattr(contact, key, value)
    await db.commit()
    await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Contact).filter_by(id=contact_id))
    contact = result.scalar_one_or_none()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await db.delete(contact)
    await db.commit()
    return {"message": "Contact deleted"}
