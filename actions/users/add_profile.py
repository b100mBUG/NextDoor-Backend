from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from database.models import User, UserProfile
from database.config_db import get_session


async def add_profile_image(
    db: AsyncSession,
    user_id: str,
    image_detail: dict
) -> UserProfile:
    """
    Adds or updates a user's profile image.

    Args:
        db (AsyncSession): async DB session
        user_id (str): ID of the user
        image_detail (dict): 
            {
                "profile_image_url": str,
                "profile_image_key": str
            }

    Returns:
        UserProfile: the updated or created profile row
    """

    stmt = select(UserProfile).where(UserProfile.user_id == user_id)
    res = await db.execute(stmt)
    profile = res.scalars().first()

    now = datetime.utcnow()

    if profile:
        # Update existing profile
        profile.profile_image_url = image_detail.get("profile_image_url")
        profile.profile_image_key = image_detail.get("profile_image_key")
        profile.profile_image_updated_at = now
    else:
        profile = UserProfile(
            id=uuid4(),
            user_id=user_id,
            profile_image_url=image_detail.get("profile_image_url"),
            profile_image_key=image_detail.get("profile_image_key"),
            profile_image_updated_at=now
        )

    db.add(profile)
    await db.commit()
    await db.refresh(profile)

    return profile
