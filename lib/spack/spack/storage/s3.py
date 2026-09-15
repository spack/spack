# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import io
import os
import pathlib
import re
from datetime import datetime
from typing import IO, Iterator, Optional, Union

import spack.config as cfg
from spack.util.s3 import WrapStream, _parse_s3_endpoint_url
from spack.util.web import _list_s3_objects

from .credentials import Credentials
from .storage_base import StatResult, StorageBase, storage


@storage("s3")
class S3(StorageBase):
    def __init__(self, url, **kwargs):
        super().__init__(url)

        self.endpoint_url = kwargs.get("endpoint_url") or os.environ.get("S3_ENDPOINT_URL")
        # Configure the override endpoint URL
        if self.endpoint_url:
            self.endpoint_url = _parse_s3_endpoint_url(self.endpoint_url)

        self.creds = Credentials(**kwargs)

        # Create the s3 client
        self.client = self._get_client()

    def _real_key(self, key: Union[str, pathlib.Path]) -> str:
        prefix = re.sub(r"^/*", "/", self.url.path)
        return str(pathlib.PurePosixPath(pathlib.Path(prefix) / key))

    def read(self, key: Union[str, pathlib.Path]) -> IO[str]:
        """Read the"""
        obj = self.client.get_object(Bucket=self.url.netloc, Key=self._real_key(key))
        return WrapStream(obj["Body"])  # type: ignore

    def write(self, key: Union[str, pathlib.Path], data: Optional[IO[str]] = None):
        # Create a dummy buffer to init the s3 entry
        if not data:
            data = io.StringIO()
        self.client.put_object(Bucket=self.url.netloc, Key=self._real_key(key), Body=data.read())

    def _list(self) -> Iterator[str]:
        list_head = None
        bucket = self.url.netloc

        while True:
            contents, list_head = _list_s3_objects(
                self.client, bucket, self._real_key("/"), 1024, start_after=list_head
            )

            for x in contents:
                yield x

            if not list_head:
                break

    def delete(self, key: Union[str, pathlib.Path]):
        self.client.delete_object(Bucket=self.url.netloc, Key=self._real_key(key))

    def stat(self, key: Union[str, pathlib.Path]) -> StatResult:
        obj = self.client.head_object(Bucket=self.url.netloc, Key=self._real_key(key))
        headers = obj["ResponseMetadata"]["HTTPHeaders"]
        return StatResult(
            int(headers["Content-Length"]),
            datetime.strptime(headers["Last-Modified"], "%Y-%m-%d-%H:%M:%S.%f"),
        )

    def _get_client(self):
        from boto3 import Session
        from botocore import UNSIGNED
        from botocore._client import Config
        from botocore.exceptions import ClientError

        connection_args = dict()

        access_token = self.creds.token
        access_id = self.creds.access_id
        access_secret = self.creds.access_secret
        access_profile = self.creds.access_profile

        if access_token:
            connection_args["aws_session_token"] = access_token

        if access_id and access_secret:
            connection_args["aws_access_key_id"] = access_id
            connection_args["aws_secret_access_key"] = access_secret

        if access_profile:
            connection_args["profile_name"] = access_profile

        session = Session(**connection_args)

        client_args = {"use_ssl": cfg.get("config:verify_ssl")}

        if self.endpoint_url:
            client_args["endpoint_url"] = self.endpoint_url

        # if no access credentials provided above, then access anonymously
        if not session.get_credentials():
            client_args["config"] = Config(signature_version=UNSIGNED)

        client = session.client("s3", **client_args)
        client.ClientError = ClientError

        return client
