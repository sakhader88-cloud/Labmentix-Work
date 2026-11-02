from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..deps import get_current_user
from ..db import get_db
from ..schemas import UserOut
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["users"])

class UserUpdate(BaseModel):
    full_name: str | None = None

@router.get("/me", response_model=UserOut)
async def read_my_profile(current_user = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=UserOut)
async def update_profile(update: UserUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    if update.full_name:
        current_user.full_name = update.full_name
        db.add(current_user)
        await db.commit()
        await db.refresh(current_user)
    return current_user

@router.delete("/me")
async def deactivate_account(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    current_user.is_active = False
    db.add(current_user)
    await db.commit()
    return {"message": "Account deactivated successfully"}
