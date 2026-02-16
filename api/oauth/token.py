from jose import jwt
from datetime import timedelta, datetime
import os
from dotenv import load_dotenv

load_dotenv("api/oauth/config.env")

SECRET_KEY = os.getenv("AUTH_SECRET")
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))

    to_encode.update({"exp": expire})

    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return access_token

def verify_access_token(token = None):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        return {}