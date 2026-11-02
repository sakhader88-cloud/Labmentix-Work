from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class FileOut(BaseModel):
    id: int
    filename: str
    s3_key: str
    content_type: Optional[str]
    size: Optional[int]

    class Config:
        orm_mode = True
