from uuid import uuid4, UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User


async def update_user(
    db: AsyncSession,
    user_id: str | None = None,
    user_detail: dict | None = None,
) -> User:
    """Updates user details in the database asynchronously."""

    user_detail = user_detail or {}
    user_id = UUID(user_id)

    if not user_detail:
        return

    # Check for user
    stmt = select(User).where((User.id == user_id))
    
    res = await db.execute(stmt)
    user = res.scalars().first()
    if not user:
        raise ValueError("Invalid USER ID passed.")

    # update user
    user.phone_number=user_detail.get("phone_number")
    user.email=user_detail.get("email")
    user.full_name=user_detail.get("full_name")

    await db.commit()
    await db.refresh(user)

    return user
