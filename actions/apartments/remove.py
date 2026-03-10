from database.models import Apartment
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def mark_deleted(db: AsyncSession, apartment_id: UUID, landlord_id: UUID):
    stmt = select(Apartment).where(
        Apartment.is_deleted.is_(False),
        Apartment.id == apartment_id,
        Apartment.landlord_id == landlord_id
    )
    res = await db.execute(stmt)
    apartment = res.scalars().first()
    if not apartment:
        return None

    apartment.is_deleted = True
    await db.commit()
    await db.refresh(apartment)
    return apartment


async def unmark_deleted(db: AsyncSession, apartment_id: UUID, landlord_id: UUID):
    stmt = select(Apartment).where(
        Apartment.is_deleted.is_(True),
        Apartment.id == apartment_id,
        Apartment.landlord_id == landlord_id
    )
    res = await db.execute(stmt)
    apartment = res.scalars().first()
    if not apartment:
        return None

    apartment.is_deleted = False
    await db.commit()
    await db.refresh(apartment)
    return apartment