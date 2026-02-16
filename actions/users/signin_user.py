from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.config_db import get_session
from actions.utils import hash_password, verify_password


async def signin_user(
    db: AsyncSession,
    user_email: str | None = None,
    password: str | None = None
) -> User:
    """verifies user password asynchronously."""

    # Check for user
    stmt = select(User).where((User.email == user_email))
    
    res = await db.execute(stmt)
    user = res.scalars().first()
    if not user:
        raise ValueError("Invalid USER EMMAIL passed.")
    
    # check validity of former password

    if not verify_password(user.password_hash, password):
        raise ValueError("Failed to verify USER PASSWORD")

    return user

