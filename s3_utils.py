from __future__ import annotations
from dataclasses import dataclass

from pathlib import Path

import boto3
from botocore.client import Config

from log_utils import logger

__all__ = ["S3Config", "S3Url", "S3Urls", "S3UrlMappedPaths"]


class S3Config:
    stage: str = "dev"
    testing: bool = False
    bucket_name: str = "filestore.spin.systems"
    dir_name: str = "pdf2up"
    region: str = "eu-west-1"
    netloc: str = f"https://{bucket_name}.s3.{region}.amazonaws.com/"
    resource_config = Config(connect_timeout=5, retries={"max_attempts": 0})
    resource = boto3.resource("s3", config=resource_config)
    bucket = resource.Bucket(bucket_name)
    identifier: str = "hires"

    @classmethod
    def key_base(cls) -> Path:
        stage_subpath = [cls.stage] if cls.stage == "dev" else []
        return Path(cls.dir_name, *stage_subpath)

    @classmethod
    def filepath2key(cls, file_path: Path, file_prefix: str = f"{identifier}_") -> str:
        """Return the key for a given file path."""
        key_path = cls.key_base() / f"{file_prefix}{file_path.name}"
        return str(key_path)


class S3Url(S3Config, str):
    def __init__(self, url: str):
        super().__init__()
        if not url.startswith(self.netloc):
            raise ValueError(f"{url} netloc is not {self.netloc}")
        self += url

    def upload(self, filename: str) -> None:
        upload_desc = f"{self.key} TO {self.bucket_name}"
        if self.testing:
            logger.info(f"(TESTING) SKIPPING UPLOAD of {upload_desc}")
        else:
            logger.info(f"UPLOADING {upload_desc}")
            self.bucket.upload_file(Filename=filename, Key=self.key)

    @property
    def key(self) -> str:
        return self[len(self.netloc) :]

    @classmethod
    def from_key(cls, key: str) -> S3Url:
        url = f"{cls.netloc}{key}"
        return cls(url)


class S3Urls(S3Config, list):
    def __init__(self, urls: list[S3Url]):
        if not all(map(lambda u: isinstance(u, S3Url), urls)):
            raise TypeError(f"One or more items in {urls} are not S3Url objects.")
        self.extend(urls)

    @classmethod
    def from_keys(cls, keys: list[str]) -> S3Urls:
        urls = list(map(S3Url.from_key, keys))
        return cls(urls)

    def upload(self, filepaths: list[str]):
        for url, filepath in zip(self, filepaths):
            url.upload(filepath)


@dataclass
class S3UrlMappedPaths:
    paths: list[Path]

    @property
    def keys(self) -> list[str]:
        return list(map(S3Config.filepath2key, self.paths))

    @property
    def urls(self) -> S3Urls:
        return S3Urls.from_keys(self.keys)

    def upload(self) -> None:
        fp = [str(p.absolute()) for p in self.paths]
        self.urls.upload(filepaths=fp)
        return
