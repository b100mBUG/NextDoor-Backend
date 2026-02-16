from passlib.context import CryptContext

import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from dotenv import load_dotenv

load_dotenv("actions/config.env")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash the user's password."""
    return pwd_context.hash(password)

def verify_password(hashed_password: str, plain_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

cloudinary.config(
  cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
  api_key = os.getenv("CLOUDINARY_API_KEY"),
  api_secret = os.getenv("CLOUDINARY_API_SECRET"),
  secure = True
)

def upload_image(file):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise ValueError("Only image uploads are allowed")

    file.file.seek(0)
    file_bytes = file.file.read()

    if not file_bytes:
        raise ValueError("Empty file uploaded")

    result = cloudinary.uploader.upload(
        file_bytes,
        folder="apartments/",
        resource_type="image"
    )

    return result

