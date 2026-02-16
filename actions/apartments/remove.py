from database.models import Apartment
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def mark_deleted(db: AsyncSession, apartment_id: UUID, landlord_id: UUID):
    stmt = select(Apartment).where(
        (Apartment.is_deleted == False) &
        (Apartment.id == apartment_id) &
        (Apartment.landlord_id == landlord_id)
    )
    res = await db.execute(stmt)
    apartment = res.scalars().first()
    if not apartment:
        return
    
    apartment.is_deleted = True

    db.commit()

async def unmark_deleted(db: AsyncSession, apartment_id: str):
    stmt = select(Apartment).where(
        (Apartment.is_deleted == True) &
        (Apartment.id == apartment_id) &
        (Apartment.landlord_id == landlord_id)
    )
    res = await db.execute(stmt)
    apartment = res.scalars().first()
    if not apartment:
        return
    apartment.is_deleted = False

    db.commit()