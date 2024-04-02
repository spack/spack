# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyS3fs(PythonPackage):
    """S3FS builds on aiobotocore to provide a convenient Python filesystem
    interface for S3."""

    homepage = "https://s3fs.readthedocs.io/en/latest/"
    pypi = "s3fs/s3fs-0.5.2.tar.gz"

    license("BSD-3-Clause")

    version(
        "2024.2.0",
        sha256="c140de37175c157cb662aa6ad7423365df732ac5f10ef5bf7b76078c6333a942",
        url="https://pypi.org/packages/7c/76/efa5f84237620d5aa38e58285945b47449d8a94bf7037cae06f680b34c41/s3fs-2024.2.0-py3-none-any.whl",
    )
    version(
        "2022.11.0",
        sha256="42d57a3ceedb478b18ee53e34bbe3305a3f07f6381ca1ab76135efe076c6a07d",
        url="https://pypi.org/packages/04/5c/6a5696e6e0fc30cfab334ed47e7e04707a6efd0ac1fe24158f5969fb4ef8/s3fs-2022.11.0-py3-none-any.whl",
    )
    version(
        "0.5.2",
        sha256="0e7a3fdab0ff66af7c8afd9cdc69723643e10ba6ce37776332fdad9f41bec3dd",
        url="https://pypi.org/packages/d0/47/8f96b4a3af8bd54dda28df960307978679b3cc64bc8ec5460697c30bc783/s3fs-0.5.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@2023.3:")
        depends_on("python@3.7:", when="@0.5.2:0,2022.2:2023.1")
        depends_on("py-aiobotocore@2.5.4:", when="@2023.12:")
        depends_on("py-aiobotocore@2.4", when="@2022.8:2022")
        depends_on("py-aiobotocore@1.0.1:", when="@0.5:2021.7")
        depends_on("py-aiohttp@:3", when="@2022.8:")
        depends_on("py-fsspec@2024:2024.2", when="@2024:2024.2")
        depends_on("py-fsspec@2022.11:2022", when="@2022.11:2022")
        depends_on("py-fsspec@0.8:", when="@0.5:0")
