from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4, UUID

from database.models import Apartment, ApartmentMedia
from database import model_utils as mtl


async def add_apartment_media(
    db: AsyncSession,
    apartment_id: UUID,
    landlord_id: UUID,
    media_list: list[dict]
) -> Apartment:

    stmt = (
        select(Apartment)
        .options(selectinload(Apartment.media))
        .options(selectinload(Apartment.landlord))
        .where(
            Apartment.id == apartment_id,
            Apartment.landlord_id == landlord_id
        )
    )

    res = await db.execute(stmt)
    apartment = res.scalars().first()

    if not apartment:
        raise ValueError("Apartment not found")

    has_cover = any(m.is_cover for m in apartment.media)

    for i, media_data in enumerate(media_list):
        is_cover = (i == 0 and not has_cover)  # ← first image is cover only if none exists

        media = ApartmentMedia(
            apartment_id=apartment_id,
            media_type=media_data.get("media_type", mtl.MediaType.IMAGE),
            media_url=media_data["media_url"],
            media_key=media_data["media_key"],
            is_cover=is_cover
        )
        db.add(media)

    await db.commit()

    # Re-fetch with relationships loaded — fixes the MissingGreenlet error
    stmt = (
        select(Apartment)
        .options(selectinload(Apartment.media))
        .options(selectinload(Apartment.landlord))
        .where(Apartment.id == apartment_id)
    )
    res = await db.execute(stmt)
    return res.scalars().first()