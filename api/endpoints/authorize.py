from api.oauth.oauth import get_current_user
from database import model_utils as mtl
from fastapi import Depends
from database.models import User
from fastapi import HTTPException, status

def role_checker(*allowed_roles: mtl.UserRole):
    def checker(user: User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User must have one of roles: {[r.value for r in allowed_roles]}"
            )
        return user
    return checker
