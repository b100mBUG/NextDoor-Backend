from database.models import User
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def mark_deleted(db: AsyncSession, user_id: str):
    stmt = select(User).where(
        (User.is_deleted == False) &
        (User.id == UUID(user_id))
    )
    res = await db.execute(stmt)
    user = res.scalars().first()
    if not user:
        return
    
    user.is_deleted = True

    db.commit()

async def unmark_deleted(db: AsyncSession, user_id: str):
    stmt = select(User).where(
        (User.is_deleted == True) &
        (User.id == UUID(user_id))
    )
    res = await db.execute(stmt)
    user = res.scalars().first()
    if not user:
        return
    
    user.is_deleted = False

    db.commit()