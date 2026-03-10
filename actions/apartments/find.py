from database.models import Apartment
from api.schemas.apartments import ApartmentFilter
from sqlalchemy import select, and_
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from database import model_utils as mtl


DEFAULT_LIMIT = 20
MAX_LIMIT = 100


async def fetch_apartments(
    db: AsyncSession,
    *,
    limit: int = DEFAULT_LIMIT,
    offset: int = 0,
):
    limit = min(limit, MAX_LIMIT)

    stmt = (
        select(Apartment)
        .where(
            Apartment.is_deleted == False,
            Apartment.is_available == True
        )
        .options(selectinload(Apartment.media))
        .options(selectinload(Apartment.landlord))
        .limit(limit)
        .offset(offset)
    )

    res = await db.execute(stmt)
    apartments = res.scalars().all()

    return apartments

from sqlalchemy import and_
from sqlalchemy.orm import selectinload

async def filter_apartments(db: AsyncSession, filters: ApartmentFilter):
    conditions = [Apartment.is_deleted.is_(False)]

    if filters.city:
        conditions.append(Apartment.city.ilike(f"%{filters.city}%"))
    if filters.area:
        conditions.append(Apartment.area.ilike(f"%{filters.area}%"))
    if filters.min_rent is not None:
        conditions.append(Apartment.rent >= filters.min_rent)
    if filters.max_rent is not None:
        conditions.append(Apartment.rent <= filters.max_rent)
    if filters.min_deposit is not None:
        conditions.append(Apartment.deposit >= filters.min_deposit)
    if filters.max_deposit is not None:
        conditions.append(Apartment.deposit <= filters.max_deposit)

    if filters.house_type:
        conditions.append(Apartment.house_type == mtl.HouseType(filters.house_type))
    if filters.water_supply:
        conditions.append(Apartment.water_supply == mtl.WaterSupply(filters.water_supply))
    if filters.bathroom_type:
        conditions.append(Apartment.bathroom_type == mtl.BathroomType(filters.bathroom_type))
    if filters.kitchen_type:
        conditions.append(Apartment.kitchen_type == mtl.KitchenType(filters.kitchen_type))
    if filters.security_level:
        conditions.append(Apartment.security_level == mtl.SecurityLevel(filters.security_level))

    if filters.is_available is not None:
        conditions.append(Apartment.is_available == filters.is_available)

    stmt = (
        select(Apartment)
        .where(and_(*conditions))
        .options(selectinload(Apartment.media), selectinload(Apartment.landlord))
        .limit(filters.limit)
        .offset(filters.offset)
    )
    result = await db.execute(stmt)
    apartments = result.scalars().all()
    return apartments

async def fetch_your_apartments(
    db: AsyncSession,
    *,
    limit: int = DEFAULT_LIMIT,
    offset: int = 0,
    landlord_id: UUID
):
    limit = min(limit, MAX_LIMIT)

    stmt = (
        select(Apartment)
        .options(selectinload(Apartment.media))
        .where(
            Apartment.is_deleted == False,
            Apartment.is_available == True,
            Apartment.landlord_id == landlord_id
        )
        .limit(limit)
        .offset(offset)
    )

    res = await db.execute(stmt)
    apartments = res.scalars().all()

    return apartments
    
