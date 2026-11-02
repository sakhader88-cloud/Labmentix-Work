from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import boto3
import uuid
from ..db import get_db
from ..deps import get_current_user
from ..config import settings
from ..crud import create_file_record, list_files_for_user
from ..schemas import FileOut

router = APIRouter(prefix="/files", tags=["files"])

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

@router.post("/upload", response_model=FileOut)
async def upload_file(file: UploadFile = File(...), db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    if not settings.AWS_S3_BUCKET:
        raise HTTPException(status_code=500, detail="S3 not configured")
    content = await file.read()
    key = f"user_uploads/{current_user.id}/{uuid.uuid4().hex}_{file.filename}"
    s3_client.put_object(Bucket=settings.AWS_S3_BUCKET, Key=key, Body=content, ContentType=file.content_type)
    new_rec = await create_file_record(db, filename=file.filename, s3_key=key, content_type=file.content_type, size=len(content), owner_id=current_user.id)
    return new_rec

@router.get("/", response_model=list[FileOut])
async def list_files(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    files = await list_files_for_user(db, current_user.id)
    return files
