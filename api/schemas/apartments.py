from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from database import model_utils as mtl
from uuid import UUID

class ApartmentCreate(BaseModel):
    city: Optional[str]
    area: Optional[str]
    rent: Optional[int] 
    deposit: Optional[int] 

    class Config:
        from_attributes = True

class ApartmentMedia(BaseModel):
    media_type: Optional[str]
    media_url: Optional[str]
    media_key: Optional[str]
    is_cover: Optional[bool]

    class Config:
        from_attributes = True

class ApartmentOut(BaseModel):
    id: Optional[UUID] = None
    id: Optional[UUID] = None
    city: Optional[str]
    area: Optional[str]
    rent: Optional[int]
    deposit: Optional[int]
    house_type: Optional[mtl.HouseType] = None
    water_supply: Optional[mtl.WaterSupply] = None
    bathroom_type: Optional[mtl.BathroomType] = None
    kitchen_type: Optional[mtl.KitchenType] = None
    security_level: Optional[mtl.SecurityLevel] = None
    is_available: bool
    created_at: datetime
    media: Optional[List[ApartmentMedia]] = None

    class Config:
        from_attributes = True


class ApartmentUpdate(BaseModel):
    city: Optional[str]
    area: Optional[str]
    rent: Optional[int]
    deposit: Optional[int]
    house_type: Optional[mtl.HouseType] = None
    water_supply: Optional[mtl.WaterSupply] = None
    bathroom_type: Optional[mtl.BathroomType] = None
    kitchen_type: Optional[mtl.KitchenType] = None
    security_level: Optional[mtl.SecurityLevel] = None
    is_available: Optional[bool]

    class Config:
        from_attributes = True

DEFAULT_LIMIT = 20

class ApartmentFilter(BaseModel):
    city: Optional[str]
    area: Optional[str]
    min_rent: Optional[int]
    max_rent: Optional[int]
    min_deposit: Optional[int]
    max_deposit: Optional[int]
    house_type: Optional[mtl.HouseType]
    water_supply: Optional[mtl.WaterSupply]
    bathroom_type: Optional[mtl.BathroomType]
    kitchen_type: Optional[mtl.KitchenType]
    security_level: Optional[mtl.SecurityLevel]
    is_available: Optional[bool] = True
    limit: int = DEFAULT_LIMIT
    offset: int = 0
