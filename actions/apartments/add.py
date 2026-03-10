from uuid import uuid4
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Apartment, ApartmentMedia, User
from database import model_utils as mtl
from database.config_db import get_session


async def add_apartment(
    db: AsyncSession,
    landlord_id: str,
    apartment_detail: dict | None = None,
) -> Apartment:

    apartment_detail = apartment_detail or {}

    if not apartment_detail:
        raise ValueError("Apartment detail required")

    stmt = select(User).where(
        User.id == landlord_id,
        User.role.in_([mtl.UserRole.LANDLORD, mtl.UserRole.ADMIN])
    )

    res = await db.execute(stmt)
    landlord = res.scalars().first()

    if not landlord:
        raise ValueError("Landlord not found or invalid role.")

    apartment = Apartment(
        landlord_id=landlord_id,
        city=apartment_detail.get("city"),
        area=apartment_detail.get("area"),
        rent=apartment_detail.get("rent"),
        deposit=apartment_detail.get("deposit", 0),
        house_type=apartment_detail.get("house_type", mtl.HouseType.TWO_BEDROOM),
        water_supply=apartment_detail.get("water_supply", mtl.WaterSupply.SCHEDULED),
        bathroom_type=apartment_detail.get("bathroom_type", mtl.BathroomType.PRIVATE),
        kitchen_type=apartment_detail.get("kitchen_type", mtl.KitchenType.PRIVATE),
        security_level=apartment_detail.get("security_level", mtl.SecurityLevel.GATE),
        is_available=apartment_detail.get("is_available", True),
    )

    db.add(apartment)
    await db.commit()
    await db.refresh(apartment)

    stmt = (
        select(Apartment)
        .options(selectinload(Apartment.media))
        .options(selectinload(Apartment.landlord))
        .where(Apartment.id == apartment.id)
    )

    res = await db.execute(stmt)

    return res.scalars().first()

