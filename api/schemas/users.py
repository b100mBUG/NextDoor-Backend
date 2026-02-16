from pydantic import BaseModel, EmailStr
from datetime import date, time, datetime
from typing import Optional
from uuid import UUID
from database import model_utils as mtl


class UserCreate(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    password: str

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: Optional[UUID] = None
    full_name: Optional[str]
    email: Optional[EmailStr]
    phone_number: Optional[str]
    is_verified: bool
    rating: float
    role: Optional[mtl.UserRole] = None
    report_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: Optional[str]
    email: Optional[EmailStr]
    phone_number: Optional[str]

    class Config:
        from_attributes = True


class PasswordChange(BaseModel):
    former: str
    new: str

    class Config:
        from_attributes = True


