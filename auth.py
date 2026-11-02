from datetime import datetime, timedelta
from typing import Optional
import jwt
from .config import settings
from .crud import verify_password, get_user_by_email
from sqlalchemy.ext.asyncio import AsyncSession

ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.APP_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user or not user.hashed_password:
        return None
    if not await verify_password(password, user.hashed_password):
        return None
    return user
