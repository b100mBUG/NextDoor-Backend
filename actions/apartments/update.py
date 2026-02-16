from uuid import uuid4, UUID
from sqlalchemy import select
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

    Args:
        db (AsyncSession): async DB session
        apartment_id (str): ID of the apartment you wanna update
        apartment_detail (dict, optional): apartment data:
            {
                city: str,
                area: str,
                rent: int,
                deposit: int,
                house_type: HouseType,
                water_supply: WaterSupply,
                bathroom_type: BathroomType,
                kitchen_type: KitchenType,
                security_level: SecurityLevel,
                is_available: bool
            }

    Returns:
        Apartment: the newly created Apartment object
    """

    apartment_detail = apartment_detail or {}

    # Ensure apartment exists
    stmt = select(User).where(Apartment.id == UUID(apartment_id))
    res = await db.execute(stmt)
    apartment = res.scalars().first()
    if not apartment:
        raise ValueError("Apartment not found.")

    # Update Apartment
    apartment.city=apartment_detail.get("city")
    apartment.area=apartment_detail.get("area")
    apartment.rent=apartment_detail.get("rent")
    apartment.deposit=apartment_detail.get("deposit", 0)
    apartment.house_type=apartment_detail.get("house_type", mtl.HouseType.TWO_BEDROOM)
    apartment.water_supply=apartment_detail.get("water_supply", mtl.WaterSupply.SCHEDULED)
    apartment.bathroom_type=apartment_detail.get("bathroom_type", mtl.BathroomType.PRIVATE)
    apartment.kitchen_type=apartment_detail.get("kitchen_type", mtl.KitchenType.PRIVATE)
    apartment.security_level=apartment_detail.get("security_level", mtl.SecurityLevel.GATE)
    apartment.is_available=apartment_detail.get("is_available", True)
    
    await db.commit()
    await db.refresh(apartment)

    return apartment

