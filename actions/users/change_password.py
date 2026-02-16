from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.config_db import get_session
from actions.utils import hash_password, verify_password


async def update_user_password(
    db: AsyncSession,
    user_id: str | None = None,
    password_detail: dict | None = None,
) -> User:
    """updates user password asynchronously."""
    if password_detail["new"] == password_detail['former']:
        raise ValueError("Former cannor be same as new password")
    # Check for user
    stmt = select(User).where((User.user_id == user_id))
    
    res = await db.execute(stmt)
    user = res.scalars().first()
    if not user:
        raise ValueError("Invalid USER ID passed.")
    
    # check validity of former password

    if not verify_password(user.password_hash, password_detail.get("former")):
        raise ValueError("Failed to verify USER PASSWORD")

    # update user

    user.password_hash = password_detail.get("new"),

    await db.commit()
    await db.refresh(user)

    return user

