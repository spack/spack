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

    version("1.60.1", sha256="61b5aab8989498e8aa142c20b88829ea5d90d18c18c853b9f9e6d407d37bf8b4")

    # https://github.com/grpc/grpc/blob/v1.60.1/src/python/grpcio_status/setup.py

    depends_on("py-protobuf@4.21.6:", type=("build", "run"))
    depends_on("py-grpcio@1.60.1:", when="@1.60.1", type=("build", "run"))
    depends_on("py-googleapis-common-protos@1.5.5:", type=("build", "run"))

    depends_on("py-setuptools", type="build")
