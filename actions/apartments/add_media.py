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
        .where(
            Apartment.id == apartment_id,
            Apartment.landlord_id == landlord_id
        )
    )

    res = await db.execute(stmt)
    apartment = res.scalars().first()

    if not apartment:
        raise_exception(404, "Apartment not found")


    has_cover = any(m.is_cover for m in apartment.media)

    if not has_cover and media_list:
        media_list[0]["is_cover"] = True
        has_cover = True

    for media_data in media_list:
        is_cover = media_data.get("is_cover", False)

        if is_cover and has_cover:
            is_cover = False

        media = ApartmentMedia(
            apartment_id=apartment_id,
            media_type=media_data.get("media_type", mtl.MediaType.IMAGE),
            media_url=media_data["media_url"],
            media_key=media_data["media_key"],
            is_cover=is_cover
        )

        db.add(media)

        if is_cover:
            has_cover = True

    await db.commit()

    return apartment