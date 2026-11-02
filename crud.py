from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User, File
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_email(db: AsyncSession, email: str):
    q = await db.execute(select(User).where(User.email == email))
    return q.scalars().first()

async def create_user(db: AsyncSession, email: str, password: str, full_name: str = None):
    hashed = pwd_context.hash(password) if password else None
    new_user = User(email=email, hashed_password=hashed, full_name=full_name)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def create_file_record(db: AsyncSession, filename: str, s3_key: str, content_type: str, size: int, owner_id: int):
    new_file = File(filename=filename, s3_key=s3_key, content_type=content_type, size=size, owner_id=owner_id)
    db.add(new_file)
    await db.commit()
    await db.refresh(new_file)
    return new_file

async def list_files_for_user(db: AsyncSession, owner_id: int):
    q = await db.execute(select(File).where(File.owner_id == owner_id).order_by(File.created_at.desc()))
    return q.scalars().all()
