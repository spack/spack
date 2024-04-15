# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyProtocGenSwagger(PythonPackage):
    """A python package for swagger annotation proto files."""

    homepage = "https://github.com/universe-proton/protoc-gen-swagger"
    url = "https://github.com/universe-proton/protoc-gen-swagger/archive/refs/tags/v0.1.0.tar.gz"

    license("Apache-2.0")

    version(
        "0.1.0",
        sha256="cdc043da538865f055a7f22b304a35085cef269dc33e2f3408b12d397e8d8b4b",
        url="https://pypi.org/packages/7d/7f/d8f8d81a921f07e703cabf8a0b5bb6cbc26e3bce7614db905c3c7637315a/protoc_gen_swagger-0.1.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-protobuf@3.0.0:")
