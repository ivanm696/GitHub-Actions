"""
S3-compatible object storage for artifacts (generated files, exports, images).

Works with AWS S3 out of the box. For Cloudflare R2, set S3_ENDPOINT_URL to
your R2 account endpoint — the boto3 API is fully compatible.
"""
from __future__ import annotations

from functools import lru_cache

from app.core.config import get_settings


@lru_cache
def get_s3_client():
    import boto3
    settings = get_settings()
    return boto3.client(
        "s3",
        endpoint_url=settings.s3_endpoint_url,  # None => real AWS S3
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
        region_name=settings.s3_region,
    )


def upload_bytes(key: str, data: bytes, content_type: str = "application/octet-stream") -> str:
    """Upload raw bytes under `key`. Returns the key (not a public URL —
    generate a presigned URL separately if the object should be shareable)."""
    settings = get_settings()
    client = get_s3_client()
    client.put_object(Bucket=settings.s3_bucket, Key=key, Body=data, ContentType=content_type)
    return key


def download_bytes(key: str) -> bytes:
    settings = get_settings()
    client = get_s3_client()
    obj = client.get_object(Bucket=settings.s3_bucket, Key=key)
    return obj["Body"].read()


def presigned_url(key: str, expires_in: int = 3600) -> str:
    """Generate a temporary shareable URL for a private object."""
    settings = get_settings()
    client = get_s3_client()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.s3_bucket, "Key": key},
        ExpiresIn=expires_in,
    )


def delete_object(key: str) -> None:
    settings = get_settings()
    client = get_s3_client()
    client.delete_object(Bucket=settings.s3_bucket, Key=key)
