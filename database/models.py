from sqlalchemy import Column, String, Boolean, Integer, Float, UUID, DateTime, func, Index, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from uuid import uuid4

from database import model_utils as mtl

Base = declarative_base()


class Apartment(Base):
    __tablename__ = "apartments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    landlord_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    city = Column(String, index=True)
    area = Column(String, index=True)

    rent = Column(Integer, nullable=False)
    deposit = Column(Integer, default=0)

    house_type = Column(Enum(mtl.HouseType), nullable=False, default=mtl.HouseType.TWO_BEDROOM)

    water_supply = Column(Enum(mtl.WaterSupply), default=mtl.WaterSupply.SCHEDULED)
    bathroom_type = Column(Enum(mtl.BathroomType), default=mtl.BathroomType.PRIVATE)
    kitchen_type = Column(Enum(mtl.KitchenType), default=mtl.KitchenType.PRIVATE)

    security_level = Column(Enum(mtl.SecurityLevel), default=mtl.SecurityLevel.GATE)

    is_available = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())

    landlord = relationship("User", back_populates="apartments")

    media = relationship(
        "ApartmentMedia", 
        back_populates="apartment", 
        cascade="all, delete-orphan"
    )

class ApartmentMedia(Base):
    __tablename__ = "apartment_media"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    apartment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("apartments.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    media_type = Column(Enum(mtl.MediaType), nullable=False, default=mtl.MediaType.IMAGE)
    media_url = Column(String, nullable=False)  
    media_key = Column(String, nullable=False) 
    is_cover = Column(Boolean, default=False) 
    uploaded_at = Column(DateTime, server_default=func.now())

    apartment = relationship("Apartment", back_populates="media")



class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    phone_number = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=True)

    role = Column(
        Enum(mtl.UserRole),
        nullable=False,
        default=mtl.UserRole.TENANT,
        index=True
    )

    password_hash = Column(String, nullable=False)

    full_name = Column(String)

    is_verified = Column(Boolean, default=False)

    is_deleted = Column(Boolean, default=False)

    rating = Column(Float, default=0.0)
    report_count = Column(Integer, default=0)

    created_at = Column(DateTime, server_default=func.now())

    profile = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    apartments = relationship(
        "Apartment",
        back_populates="landlord",
        cascade="all, delete-orphan"
    )


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    profile_image_url = Column(String, nullable=True)
    profile_image_key = Column(String, nullable=True)
    profile_image_updated_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="profile")


Index("idx_apartment_available", "Apartment.is_available", "Apartment.is_deleted")
