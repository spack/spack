# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGrpcioStatus(PythonPackage):
    """Status proto mapping for gRPC."""

    homepage = "https://grpc.io/"
    pypi = "grpcio_status/grpcio-status-1.52.0.tar.gz"

    license("Apache-2.0")

    version("1.52.0", sha256="602a3808d485a1b69e11d150a075e3e927f647f3a8b387ee3c3f01633445b2fc")

    # https://github.com/grpc/grpc/blob/v1.52.0/src/python/grpcio_status/setup.py

    depends_on("py-protobuf@4.21.6:", type=("build", "run"))
    depends_on("py-grpcio@1.52.0:", when="@1.52.0", type=("build", "run"))
    depends_on("py-googleapis-common-protos@1.5.5:", type=("build", "run"))

    depends_on("py-setuptools", type="build")
