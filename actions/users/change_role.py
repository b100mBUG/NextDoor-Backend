from uuid import uuid4, UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database import model_utils as mtl


async def update_user_role(
    db: AsyncSession,
    user_id: str | None = None,
    role: mtl.UserRole = mtl.UserRole.TENANT,
) -> User:
    """Updates user role in the database asynchronously."""
    user_id = UUID(user_id)
    # Check for user
    stmt = select(User).where((User.id == user_id))
    
    res = await db.execute(stmt)
    user = res.scalars().first()
    if not user:
        raise ValueError("Invalid USER ID passed.")

    # update user role
    user.role = role

    await db.commit()
    await db.refresh(user)

    return user
