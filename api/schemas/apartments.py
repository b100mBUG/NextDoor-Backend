from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from database import model_utils as mtl
from api.schemas.users import UserOut



class ApartmentCreate(BaseModel):
    city: str
    area: str
    rent: int
    deposit: int

    class Config:
        from_attributes = True



class ApartmentMedia(BaseModel):
    media_type: Optional[str] = None
    media_url: Optional[str] = None
    media_key: Optional[str] = None
    is_cover: Optional[bool] = None

    class Config:
        from_attributes = True



class ApartmentOut(BaseModel):
    id: Optional[UUID] = None
    city: Optional[str] = None
    area: Optional[str] = None
    rent: Optional[int] = None
    deposit: Optional[int] = None

    house_type: Optional[mtl.HouseType] = None
    water_supply: Optional[mtl.WaterSupply] = None
    bathroom_type: Optional[mtl.BathroomType] = None
    kitchen_type: Optional[mtl.KitchenType] = None
    security_level: Optional[mtl.SecurityLevel] = None

    is_available: Optional[bool] = None
    created_at: datetime

    landlord: Optional[UserOut] = None
    media: Optional[List[ApartmentMedia]] = None

    class Config:
        from_attributes = True



class ApartmentUpdate(BaseModel):
    city: Optional[str] = None
    area: Optional[str] = None
    rent: Optional[int] = None
    deposit: Optional[int] = None

    house_type: Optional[mtl.HouseType] = None
    water_supply: Optional[mtl.WaterSupply] = None
    bathroom_type: Optional[mtl.BathroomType] = None
    kitchen_type: Optional[mtl.KitchenType] = None
    security_level: Optional[mtl.SecurityLevel] = None

    is_available: Optional[bool] = None

    class Config:
        from_attributes = True


DEFAULT_LIMIT = 20


class ApartmentFilter(BaseModel):
    city: Optional[str] = None
    area: Optional[str] = None

    min_rent: Optional[int] = None
    max_rent: Optional[int] = None

    min_deposit: Optional[int] = None
    max_deposit: Optional[int] = None

    house_type: Optional[mtl.HouseType] = None
    water_supply: Optional[mtl.WaterSupply] = None
    bathroom_type: Optional[mtl.BathroomType] = None
    kitchen_type: Optional[mtl.KitchenType] = None
    security_level: Optional[mtl.SecurityLevel] = None

    is_available: Optional[bool] = None

    limit: int = DEFAULT_LIMIT
    offset: int = 0