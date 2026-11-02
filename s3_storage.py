import boto3
from ..config import settings

def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

def upload_bytes_to_s3(key: str, content: bytes, content_type: str = None):
    client = get_s3_client()
    client.put_object(Bucket=settings.AWS_S3_BUCKET, Key=key, Body=content, ContentType=content_type)
    return key
