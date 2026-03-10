from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from actions.users.signin_user import signin_user
from actions.users.find import get_specific_user
from api.oauth.token import create_access_token, verify_access_token
from datetime import datetime, timedelta
from database.config_db import get_session


router = APIRouter()

ACCESS_TOKEN_EXPIRES_DAYS = 15

@router.post("/token")
async def signin_client(
    form_data = Depends(OAuth2PasswordRequestForm),
    db: AsyncSession = Depends(get_session)
):

    user = await signin_user(
        db=db,
        user_email=form_data.username,
        password=form_data.password
    )
    
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    access_token = create_access_token(
        data = {"sub": user.email},
        expires_delta = timedelta(days=ACCESS_TOKEN_EXPIRES_DAYS)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_session)
):
    payload = verify_access_token(token)
    print(payload)
    if not payload:
        print("Payload not found")
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await get_specific_user(
        db=db,
        email=payload.get("sub")
    )
    print(user)

    if not user:
        print("User not found")
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return user

