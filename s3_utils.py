from __future__ import annotations

from pathlib import Path

import boto3

from console_log import logger

__all__ = ["S3Config", "S3Url", "S3Urls"]


class S3Config:
    TESTING: bool = False
    DEFAULT_BUCKET: str = "my-bucket-name"
    bucket: str
    resource = boto3.resource("s3")

    def __init__(self, bucket: str = DEFAULT_BUCKET):
        self.bucket = bucket

    def key_from_path(self, path: Path) -> str:
        return str(path.resolve()).replace("/", "-")


class S3Url(S3Config, str):
    def __init__(self, url: str):
        self += url

    def upload(self, path: Path) -> None:
        key = self.key_from_path(path)
        if self.TESTING:
            logger.info("SKIPPING S3 UPLOAD...")
        else:
            logger.info(f"UPLOADING {key} TO {self.bucket}")
            self.resource.upload_file(bucket=self.bucket, key=key)


class S3Urls(S3Config, list):
    def __init__(self, urls: list[S3Url]):
        if not all(map(lambda u: isinstance(u, S3Url), urls)):
            raise TypeError(f"One or more items in {urls} are not S3Url objects.")
        self.extend(urls)

    @classmethod
    def from_keys(cls, keys: list[str]) -> S3Urls:
        url_list = list(map(S3Url, keys))
        return cls(url_list)