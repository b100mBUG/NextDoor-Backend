from uuid import uuid4, UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Apartment, User
from database import model_utils as mtl
from database.config_db import get_session


async def update_apartment(
    db: AsyncSession,
    apartment_id: str,
    apartment_detail: dict | None = None,
) -> Apartment:
    """
    Updates an apartment in the database.
    """

    apartment_detail = apartment_detail or {}

    stmt = (
        select(Apartment)
        .where(Apartment.id == apartment_id)
        .options(selectinload(Apartment.media))
        .options(selectinload(Apartment.landlord))
    )
    res = await db.execute(stmt)
    apartment = res.scalars().first()
    if not apartment:
        raise ValueError("Apartment not found.")

    update_data = {k: v for k, v in apartment_detail.items() if v is not None}
    for key, value in update_data.items():
        setattr(apartment, key, value)

    await db.commit()
    await db.refresh(apartment)

    return apartment

