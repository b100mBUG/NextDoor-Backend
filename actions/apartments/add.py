from uuid import uuid4
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
    """
    Adds a new apartment to the database.

    Args:
        db (AsyncSession): async DB session
        landlord_id (str): ID of the landlord (User.id)
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

    if not apartment_detail:
        return

    # Ensure landlord exists
    stmt = select(User).where(User.id == landlord_id, User.role == mtl.UserRole.LANDLORD)
    res = await db.execute(stmt)
    landlord = res.scalars().first()
    if not landlord:
        raise ValueError("Landlord not found or invalid role.")

    # Create Apartment
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
        is_available=apartment_detail.get("is_available", True)
    )

    db.add(apartment)
    await db.commit()
    await db.refresh(apartment)

    return apartment

