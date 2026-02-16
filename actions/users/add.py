from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, UserProfile
from database import model_utils as mtl
from database.config_db import get_session
from actions.utils import hash_password


async def add_user(
    db: AsyncSession,
    user_detail: dict | None = None,
    role: mtl.UserRole = mtl.UserRole.TENANT,
    create_profile: bool = False
) -> User:
    """Adds a new user to the database asynchronously."""

    user_detail = user_detail or {}
    if not user_detail:
        return
    # Check for duplicates
    stmt = select(User).where(
        (User.phone_number == user_detail.get("phone_number")) |
        (User.email == user_detail.get("email"))
    )
    res = await db.execute(stmt)
    existing = res.scalars().first()
    if existing:
        raise ValueError("User with this phone number or email already exists.")

    # Create user
    user = User(
        phone_number=user_detail.get("phone_number"),
        password_hash=hash_password(user_detail.get("password")),
        email=user_detail.get("email"),
        full_name=user_detail.get("full_name"),
        role=role,
        is_verified=False
    )

    # checks if user wants to create profile
    if create_profile:
        profile = UserProfile(user=user)
        user.profile = profile

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user
