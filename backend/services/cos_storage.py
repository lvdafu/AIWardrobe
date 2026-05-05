"""腾讯云 COS 存储服务"""
import asyncio
from qcloud_cos import CosConfig, CosS3Client


def _upload_sync(file_bytes: bytes, key: str, secret_id: str, secret_key: str, region: str, bucket: str) -> None:
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    client = CosS3Client(config)
    client.put_object(Bucket=bucket, Body=file_bytes, Key=key, ContentType="image/png")


async def upload_png_to_cos(
    file_bytes: bytes,
    key: str,
    secret_id: str,
    secret_key: str,
    region: str,
    bucket: str,
) -> None:
    await asyncio.to_thread(_upload_sync, file_bytes, key, secret_id, secret_key, region, bucket)
