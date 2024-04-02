# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGrpcioStatus(PythonPackage):
    """Status proto mapping for gRPC."""

    homepage = "https://grpc.io/"
    pypi = "grpcio_status/grpcio-status-1.60.1.tar.gz"

    license("Apache-2.0")

    version(
        "1.60.1",
        sha256="3034fdb239185b6e0f3169d08c268c4507481e4b8a434c21311a03d9eb5889a0",
        url="https://pypi.org/packages/eb/97/e7dfe2d5566bca05f52af5d4f4a67ccb90878586d3cadbdf8de5a5d4be00/grpcio_status-1.60.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-googleapis-common-protos@1.5.5:")
        depends_on("py-grpcio@1.60.1:", when="@1.60.1:1.60")
        depends_on("py-protobuf@4.21.6:")

    # https://github.com/grpc/grpc/blob/v1.60.1/src/python/grpcio_status/setup.py
