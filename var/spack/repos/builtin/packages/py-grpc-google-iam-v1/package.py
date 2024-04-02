# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGrpcGoogleIamV1(PythonPackage):
    """IAM API client library."""

    homepage = "https://github.com/googleapis/python-grpc-google-iam-v1"
    pypi = "grpc_google_iam_v1/grpc-google-iam-v1-0.13.0.tar.gz"

    license("Apache-2.0")

    version(
        "0.13.0",
        sha256="53902e2af7de8df8c1bd91373d9be55b0743ec267a7428ea638db3775becae89",
        url="https://pypi.org/packages/66/a0/d27ec874fb0a86b3609b73161a15cf633924888afa05c1673b3ab5a6c3f4/grpc_google_iam_v1-0.13.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.12.6:")
        depends_on("py-googleapis-common-protos@1.56:+grpc", when="@0.12.4-beta1:")
        depends_on("py-grpcio@1.44.0:", when="@0.12.6:")
        depends_on(
            "py-protobuf@3.19.5:3.20.0-rc2,3.20.1-rc1,3.20.2:4.21.0,4.21.6:4", when="@0.12.6:"
        )

    # A workaround for invalid URL due to presence of v1 in the name.

    # https://github.com/googleapis/python-grpc-google-iam-v1/blob/v0.13.0/setup.py

    conflicts("py-protobuf@3.20.0,3.20.1,4.21.1:4.21.5")
