# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleapisCommonProtos(PythonPackage):
    """Common protobufs used in Google APIs."""

    homepage = "https://github.com/googleapis/python-api-common-protos"
    pypi = "googleapis-common-protos/googleapis-common-protos-1.6.0.tar.gz"

    license("Apache-2.0")

    version("1.58.0", sha256="c727251ec025947d545184ba17e3578840fc3a24a0516a020479edab660457df")
    version("1.55.0", sha256="53eb313064738f45d5ac634155ae208e121c963659627b90dfcb61ef514c03e1")
    version("1.6.0", sha256="e61b8ed5e36b976b487c6e7b15f31bb10c7a0ca7bd5c0e837f4afab64b53a0c6")

    # https://github.com/googleapis/python-api-common-protos/blob/v1.58.0/setup.py

    variant(
        "grpc",
        default=False,
        description="Enable support for gRPC Remote Procedure Call framework.",
    )

    with when("+grpc"):
        depends_on("py-grpcio@1.44:1", when="@1.57:", type="run")
        depends_on("py-grpcio@1", when="@1.56.2:", type="run")
        depends_on("py-grpcio@1:", type="run")

    depends_on("py-setuptools", type="build")
    depends_on(
        "py-protobuf@3.19.5:3.19,3.20.2:4.21.0,4.21.6:4", when="@1.58:", type=("build", "run")
    )
    depends_on("py-protobuf@3.12.0:3", when="@1.55", type=("build", "run"))
    depends_on("py-protobuf@3.6.0:3", when="@:1.6", type=("build", "run"))
