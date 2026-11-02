# Optional: snippet to use Firebase Storage instead of S3
# To use this, install google-cloud-storage and provide GOOGLE_APPLICATION_CREDENTIALS
from google.cloud import storage

def upload_to_firebase(bucket_name: str, destination_blob_name: str, content: bytes, content_type: str = None):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(content, content_type=content_type)
    return blob.public_url
