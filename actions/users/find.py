from database.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_specific_user(db: AsyncSession, email: str | None = None) -> User:
    if not email:
        return
    stmt = select(User).where(
        (User.email == email) &
        (User.is_deleted == False)
    )
    res = await db.execute(stmt)
    user = res.scalars().first()
    if not user:
        return 
    
    return user

async def search_users(db: AsyncSession, search_term: str) -> list[User]:
    stmt = select(User).where(
        (User.full_name.ilike(f"%{search_term}")) &
        (User.is_deleted == False)
    )
    res = await db.execute(stmt)
    users = res.scalars().all()

    if not users:
        return
    return users


async def fetch_users(db: AsyncSession, sort_term: str, sort_dir: str) -> list[User]:
    stmt = select(User).where(
        (User.is_deleted == False)
    )
    if sort_term == "name":
        stmt = stmt.order_by(User.full_name.desc()) if sort_dir == "desc" else stmt.order_by(User.full_name.asc())
    elif sort_term == "date":
        stmt = stmt.order_by(User.created_at.desc()) if sort_dir == "desc" else stmt.order_by(User.created_at.asc())
    else:
        stmt = stmt
    
    res = await db.execute(stmt)
    users = res.scalars().all()

    if not users:
        return
    
    return users
